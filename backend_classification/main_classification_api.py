from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI(title="Hospitality Cancellation Classification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any frontend (use frontend's URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# --- EDA Preprocessing for Classification ---
def eda_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies EDA preprocessing for cancellation classification.
    
    Steps:
      - Drop leaky columns ('company', 'agent')
      - Drop missing values
      - Remove rows with no guests (adults, children, babies all zero)
      - Convert 'reservation_status_date' to datetime and extract date features
      - Remove outliers using IsolationForest on numeric predictors (excluding targets)
      - Drop useless columns identified during training
      - One-hot encode categorical variables
    """
    df = df.copy()
    
    # Drop columns not needed
    df = df.drop(columns=['company', 'agent'], errors='ignore')
    df = df.dropna()
    
    # Filter out rows with no guests
    filter_mask = (df['adults'] == 0) & (df['children'] == 0) & (df['babies'] == 0)
    df = df[~filter_mask]
    
    # Convert 'reservation_status_date' and extract date features
    if 'reservation_status_date' in df.columns:
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')
        df['reservation_year'] = df['reservation_status_date'].dt.year
        df['reservation_month'] = df['reservation_status_date'].dt.month
        df['reservation_day'] = df['reservation_status_date'].dt.day
        df['reservation_weekday'] = df['reservation_status_date'].dt.weekday
        df.drop(columns=['reservation_status_date'], inplace=True, errors='ignore')
    
    # Outlier handling with IsolationForest on numeric predictors (excluding 'is_canceled' and 'adr')
    numeric_cols = df.select_dtypes(exclude='object').columns.difference(['is_canceled', 'adr'])
    try:
        if len(numeric_cols) > 0:
            iforest = IsolationForest(n_estimators=50, contamination=0.1, random_state=42)
            outlier_preds = iforest.fit_predict(df[numeric_cols])
            df = df[outlier_preds != -1]
    except Exception as e:
        print("Warning: IsolationForest encountered an error:", e)
    
    # Drop useless columns (adjust as per training)
    useless_cols = ['days_in_waiting_list', 'arrival_date_year', 'arrival_date_month', 
                    'assigned_room_type', 'booking_changes', 'reservation_status', 'country']
    df.drop(columns=useless_cols, errors='ignore', inplace=True)
    df.drop(columns=['arrival_date_week_number'], errors='ignore', inplace=True)
    
    # One-hot encode categorical variables
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=int)
    
    return df



def preprocess_for_prediction_classification(input_df):
    """
    Preprocess input data for classification.
    - Applies EDA preprocessing.
    - One-hot encodes categorical features.
    - Adds missing features with default value (0).
    - Reorders the DataFrame to match training columns.
    """
    df = eda_preprocess(input_df.copy())

    # Load saved categorical dummy column names from training
    DUMMY_COLUMNS_PATH = os.path.join(os.path.dirname(__file__), "models", "classification_dummy_columns.pkl")
    
    try:
        saved_dummy_columns = joblib.load(DUMMY_COLUMNS_PATH)
    except FileNotFoundError:
        raise RuntimeError(f"Missing required file: {DUMMY_COLUMNS_PATH}. Ensure it's created during training.")

    # 🔍 **Ensure all expected categorical dummies exist**
    for col in saved_dummy_columns:
        if col not in df.columns:
            df[col] = 0  # Add missing columns with default value 0

    # ✅ **Reorder columns to match training**
    df = df[saved_dummy_columns]

    print("✅ FINAL Features Sent to Model:", df.columns.tolist())  # Debugging
    return df




# --- Load Saved Classification Model ---
#  path for the classification model saved during training.
CLASS_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "catboost_model_class.pkl")

try:
    saved_objects_class = joblib.load(CLASS_MODEL_PATH)
    # saved_objects_class[0] contains the expected feature names from training.
    expected_features_class = saved_objects_class[0]
    # saved_objects_class[1] is the trained classification pipeline.
    model_pipeline_class = saved_objects_class[1]
except Exception as e:
    raise RuntimeError(f"Failed to load classification model from {CLASS_MODEL_PATH}: {e}")

# --- Pydantic Model for Input ---
class ClassificationInput(BaseModel):
    features: dict

# --- FastAPI Endpoint for Cancellation Prediction ---
@app.post("/predict/cancellation")
def predict_cancellation(input_data: ClassificationInput):
    try:
        # Convert input dictionary to DataFrame (assumes a single record)
        input_df = pd.DataFrame([input_data.features])

        # 🚀 Print raw input before processing
        print("🔍 Raw Input Data:\n", input_df)

        # Preprocess input to ensure it has exactly the expected feature columns
        X = preprocess_for_prediction_classification(input_df)

        # Predict cancellation using the loaded pipeline
        prediction = model_pipeline_class.predict(X)[0]

        # Get probability for cancellation (assuming class '1' indicates cancellation)
        prob = model_pipeline_class.predict_proba(X)[0][1]
        cancellation_percentage = prob * 100

        return {
            "predicted_class": int(prediction),
            "cancellation_probability": round(cancellation_percentage, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Run the Application ---
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

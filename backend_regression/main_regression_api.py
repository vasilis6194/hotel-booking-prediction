from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
import os


app = FastAPI(title="Hospitality ADR Regression API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any frontend (use frontend's URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# -------------------------------
# Constants & Paths
# -------------------------------
REG_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "catboost_model_reg.pkl")
DUMMY_COLUMNS_PATH = os.path.join(os.path.dirname(__file__), "models", "dummy_columns.pkl")

# -------------------------------
# EDA Preprocessing for Regression
# -------------------------------
def eda_preprocess_regression(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs end-to-end EDA preprocessing for ADR regression.
    - Drops unnecessary columns, handles missing values, and applies feature engineering.
    """
    df = df.copy()

    # Step 1: Drop unwanted columns
    drop_cols = ['is_canceled', 'booking_changes', 'assigned_room_type',
                 'reservation_status', 'agent', 'company', 'days_in_waiting_list']
    df.drop(columns=drop_cols, errors='ignore', inplace=True)

    # Step 2: Impute missing values
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    if num_cols:
        imp_num = SimpleImputer(strategy='median')
        df[num_cols] = imp_num.fit_transform(df[num_cols])

    if cat_cols:
        imp_cat = SimpleImputer(strategy='most_frequent')
        df[cat_cols] = imp_cat.fit_transform(df[cat_cols])

    # Step 3: Filter out rows with no guests
    if set(['adults', 'children', 'babies']).issubset(df.columns):
        no_guest_filter = (df['adults'] == 0) & (df['children'] == 0) & (df['babies'] == 0)
        df = df[~no_guest_filter]

    # Step 4: Convert 'reservation_status_date' to datetime and extract date features
    if 'reservation_status_date' in df.columns:
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')
        df['reservation_year'] = df['reservation_status_date'].dt.year
        df['reservation_month'] = df['reservation_status_date'].dt.month
        df['reservation_day'] = df['reservation_status_date'].dt.day
        df['reservation_weekday'] = df['reservation_status_date'].dt.weekday
        df.drop(columns=['reservation_status_date'], inplace=True, errors='ignore')

    # Step 5: Outlier handling using IsolationForest on numeric predictors (excluding target 'adr')
    if 'adr' in df.columns:
        predictor_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if 'adr' in predictor_cols:
            predictor_cols.remove('adr')  # Ensure ADR is removed
    else:
        predictor_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    try:
        if len(predictor_cols) > 0:
            iforest = IsolationForest(n_estimators=50, contamination=0.1, random_state=42)
            outlier_preds = iforest.fit_predict(df[predictor_cols])
            df = df[outlier_preds != -1]
    except Exception as e:
        print("Warning: IsolationForest encountered an error:", e)

    # Step 6: One-hot encode categorical variables (drop_first=False)
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=False, dtype=int)

    #Ensure 'adr' is removed if it still exists
    df.drop(columns=['adr'], errors='ignore', inplace=True)

    return df


def preprocess_for_prediction_regression(input_df: pd.DataFrame, expected_features: list) -> pd.DataFrame:
    """
    Preprocess input data so that it has exactly the expected feature columns for ADR regression.
    - Applies EDA preprocessing.
    - Loads the saved dummy columns from training (dummy_columns.pkl).
    - Adds any missing columns with 0.
    - Reindexes the DataFrame to exactly match the expected features.
    """
    # Apply EDA preprocessing
    df = eda_preprocess_regression(input_df.copy())
    
    # Remove 'adr' if present (since it is the target and not used for prediction)
    df.drop(columns=['adr'], errors='ignore', inplace=True)
    
    # Load saved dummy column names from training
    try:
        saved_dummy_columns = joblib.load(DUMMY_COLUMNS_PATH)
        print("Loaded Dummy Columns:", saved_dummy_columns)
    except FileNotFoundError:
        raise RuntimeError(f"Missing required file: {DUMMY_COLUMNS_PATH}. Ensure it's created during training.")
    
    # For every column saved during training, add it if it's missing in the processed data
    for col in saved_dummy_columns:
        if col not in df.columns:
            df[col] = 0  # Fill missing columns with 0

    # Reindex the DataFrame to contain only the columns saved during training, in that order
    df = df.reindex(columns=saved_dummy_columns, fill_value=0)
    
    return df


# -------------------------------
# Load Saved Regression Model
# -------------------------------
try:
    saved_objects_reg = joblib.load(REG_MODEL_PATH)
    expected_features_reg = saved_objects_reg[0]
    model_pipeline_reg = saved_objects_reg[1]
except Exception as e:
    raise RuntimeError(f"Failed to load regression model from {REG_MODEL_PATH}: {e}")

# -------------------------------
# Pydantic Model for Input
# -------------------------------
class RegressionInput(BaseModel):
    features: dict

# -------------------------------
# FastAPI Endpoint for ADR Regression Prediction
# -------------------------------
@app.post("/predict/adr")
def predict_adr(input_data: RegressionInput):
    try:
        # Convert the input dictionary into a DataFrame (assumes single record; can be extended for batch)
        input_df = pd.DataFrame([input_data.features])
        
        # Pass expected_features_reg explicitly
        X = preprocess_for_prediction_regression(input_df, expected_features_reg)

        # Predict in log-space using the loaded pipeline
        adr_predictions_log = model_pipeline_reg.predict(X)

        # Reverse the log transformation (using np.expm1) to get predictions on the original ADR scale
        adr_predictions = np.expm1(adr_predictions_log)
        
        return {"predicted_adr": float(adr_predictions[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# -------------------------------
# Run the Application
# -------------------------------
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

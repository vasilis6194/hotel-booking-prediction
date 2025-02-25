import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer

def eda_preprocess_regression(df):
    """
    Performs end-to-end EDA preprocessing for ADR regression.
    
    Steps:
    1. Drop columns that are not useful or may cause data leakage.
    2. Impute missing values (median for numeric, mode for categorical).
    3. Filter out rows with no guests (adults, children, and babies are all zero).
    4. Convert 'reservation_status_date' to datetime and extract date features.
    5. Remove outliers using IsolationForest on numeric columns (excluding target 'adr').
    6. One-hot encode categorical variables.
    
    Returns a cleaned DataFrame ready for regression modeling.
    """
    df = df.copy()
    
    # Step 1: Drop unwanted columns
    drop_cols = [
        'is_canceled', 'booking_changes', 'assigned_room_type',
        'reservation_status', 'agent', 'company', 'days_in_waiting_list'
    ]
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
        no_guest_filter = (
            (df['adults'] == 0) &
            (df['children'] == 0) &
            (df['babies'] == 0)
        )
        df = df[~no_guest_filter]
    
    # Step 4: Convert 'reservation_status_date' to datetime and extract date features
    if 'reservation_status_date' in df.columns:
        df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')
        df['reservation_year'] = df['reservation_status_date'].dt.year
        df['reservation_month'] = df['reservation_status_date'].dt.month
        df['reservation_day'] = df['reservation_status_date'].dt.day
        df['reservation_weekday'] = df['reservation_status_date'].dt.weekday
        df.drop(columns=['reservation_status_date'], inplace=True, errors='ignore')
    
    # Step 5: Outlier handling using IsolationForest on numeric predictors (excluding 'adr')
    if 'adr' in df.columns:
        predictor_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if 'adr' in predictor_cols:
            predictor_cols.remove('adr')
    else:
        predictor_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    try:
        if len(predictor_cols) > 0:
            iforest = IsolationForest(n_estimators=50, contamination=0.1, random_state=42)
            outlier_preds = iforest.fit_predict(df[predictor_cols])
            df = df[outlier_preds != -1]
    except Exception as e:
        print("Warning: IsolationForest encountered an error:", e)
    
    # Step 6: One-hot encode categorical variables
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=int)
    
    return df


def preprocess_for_prediction_regression(input_df, expected_features):
    """
    Preprocess input data so that it has exactly the expected feature columns for ADR regression.
    - Apply eda_preprocess_regression.
    - Keep 'adr' if it exists, but it's not strictly needed for predictions.
    - Ensure that all features in expected_features are present (add missing with default=0).
    - Reorder columns to match expected_features.
    """
    df = eda_preprocess_regression(input_df.copy())
    
    # Ensure that all expected features are present
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
    
    # Reorder the DataFrame columns to match expected_features
    df = df[expected_features]
    return df


def predict_regression(input_file, expected_features):
    """
    Load input CSV data, preprocess it for regression, and use the saved model pipeline to predict ADR.
    Returns the predicted ADR values.
    """
    # Load the input data
    data = pd.read_csv(input_file)
    # Preprocess data to get features exactly as expected
    X = preprocess_for_prediction_regression(data, expected_features)
    
    # Load saved objects for regression:
    
    path_reg = r"C:\Users\user\Desktop\Github\Hotel booking prediction\hotel-booking-prediction\models\catboost_model_reg.pkl"
    saved_objects_reg = joblib.load(path_reg)

    # Take the second object (model)
    model_pipeline_reg = saved_objects_reg[1]
    
    # Predict ADR using the loaded pipeline
    adr_predictions_log = model_pipeline_reg.predict(X)

    # Reverse the log transformation to get predictions on original scale
    adr_predictions = np.expm1(adr_predictions_log)

    return adr_predictions


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python regression_predict.py input_file.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Load the saved expected features from training for regression
    path_reg = r"C:\Users\user\Desktop\Github\Hotel booking prediction\hotel-booking-prediction\models\catboost_model_reg.pkl"
    saved_objects_reg = joblib.load(path_reg)
    expected_features_reg = saved_objects_reg[0]
    
    preds_reg = predict_regression(input_file, expected_features_reg)
    print("Predicted ADR values:")
    print(preds_reg)
    
    print("Mean predicted ADR:", np.mean(preds_reg))

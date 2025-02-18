import sys
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

def eda_preprocess(df):
    """
    Apply the EDA preprocessing steps:
      - Drop leaky columns ('company', 'agent')
      - Drop missing values
      - Remove rows where adults, children, and babies are all zero
      - Convert 'reservation_status_date' to datetime and extract date features
      - Remove outliers with IsolationForest on numeric features
      - Drop useless columns identified during training
      - Apply get_dummies for categorical variables
    """
    # Drop columns not needed
    df = df.drop(columns=['company', 'agent'], errors='ignore')
    df = df.dropna()
    
    # Filter out rows with no guests
    filter_mask = (df['adults'] == 0) & (df['children'] == 0) & (df['babies'] == 0)
    df = df[~filter_mask]
    
    # Convert reservation_status_date and extract date features
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')
    df['reservation_year'] = df['reservation_status_date'].dt.year
    df['reservation_month'] = df['reservation_status_date'].dt.month
    df['reservation_day'] = df['reservation_status_date'].dt.day
    df['reservation_weekday'] = df['reservation_status_date'].dt.weekday
    df.drop(columns=['reservation_status_date'], inplace=True, errors='ignore')
    
    # Outlier detection with IsolationForest on numeric columns (excluding targets)
    numeric_cols = df.select_dtypes(exclude='object').columns.difference(['is_canceled', 'adr'])
    try:
        iforest = IsolationForest(n_estimators=50, contamination=0.1, random_state=42)
        pred_forest = iforest.fit_predict(df[numeric_cols])
        df['anomaly_label'] = pred_forest
        df = df[df['anomaly_label'] != -1]
        df.drop(columns=['anomaly_label'], inplace=True)
    except Exception as e:
        print("Warning: IsolationForest step encountered an error:", e)
    
    # Drop useless columns 
    useless_cols = ['days_in_waiting_list', 'arrival_date_year', 'arrival_date_month', 
                    'assigned_room_type', 'booking_changes', 'reservation_status', 'country']
    df.drop(columns=useless_cols, errors='ignore', inplace=True)
    df.drop(columns=['arrival_date_week_number'], errors='ignore', inplace=True)
    
    # One-hot encode categorical variables
    dummies_columns = df.select_dtypes('object').columns
    df = pd.get_dummies(df, columns=dummies_columns, drop_first=True, dtype=int)
    
    return df

def preprocess_for_prediction(input_df, expected_features):
    """
    Preprocess input data so that it has exactly the expected feature columns.
    - Apply EDA preprocessing.
    - For classification, remove target columns ('is_canceled' and 'adr').
    - Ensure that all features in expected_features are present;
      if any are missing, add them with a default value (0).
    - Reorder the DataFrame columns to match expected_features.
    """
    df = eda_preprocess(input_df.copy())
    
    # Remove target columns for classification prediction
    df = df.drop(columns=['is_canceled', 'adr'], errors='ignore')
    
    # Ensure that all expected features are present
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
    # Reorder the DataFrame to match the expected features
    df = df[expected_features]
    return df

def predict(input_file, expected_features):
    """
    Load input CSV data, preprocess it, and use the saved model pipeline to predict.
    Returns the predictions.
    """
    # Load the input data
    data = pd.read_csv(input_file)
    # Preprocess to get features exactly as expected
    X = preprocess_for_prediction(data, expected_features)
    
    # Load saved objects: expected features and trained pipeline
    path = r"C:\Users\user\Desktop\Github\Hotel booking prediction\hotel-booking-prediction\models\catboost_model.pkl"
    saved_objects = joblib.load(path)
    # saved_objects[0] is the list of expected feature names (from training)
    # saved_objects[1] is the trained pipeline (a Pipeline object)
    model_pipeline = saved_objects[1]
    
    # Predict using the loaded pipeline
    predictions = model_pipeline.predict(X)
    return predictions

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python predict.py input_file.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Load the saved expected features from training
    path = r"C:\Users\user\Desktop\Github\Hotel booking prediction\hotel-booking-prediction\models\catboost_model.pkl"
    saved_objects = joblib.load(path)
    expected_features = saved_objects[0]
    
    preds = predict(input_file, expected_features)
    print("Predictions (classification target 'is_canceled'):")
    print(preds)

    # Calculate the percentage of canceled bookings
    if len(preds) > 0:
        percentage_canceled = (sum(preds) / len(preds)) * 100
        print("Percentage of canceled bookings: {:.2f}%".format(percentage_canceled))
    else:
        print("No predictions to calculate cancellation percentage.")
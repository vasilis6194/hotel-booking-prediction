# Hospitality Predictive Analytics: End-to-End ML Pipeline (In progress) 🚀

## Overview
This project builds an end-to-end predictive analytics pipeline for the hospitality industry. It tackles two major tasks:
- **Classification:** Predicting booking cancellations.
- **Regression:** Forecasting Average Daily Rate (ADR).

The solution is designed to deliver actionable insights for revenue management and strategic pricing while being production-ready with an API built using FastAPI and containerized with Docker.

## Project Targets 🎯
- **Predict Cancellation:** Use classification models to forecast whether a booking will be canceled.
- **Forecast ADR:** Use regression models (with target log-transformation to handle skewness) to predict ADR.
- **Deployment:** Serve predictions in real time via a FastAPI endpoint and Docker for scalability.
- **Optimization:** Leverage advanced feature engineering, Bayesian hyperparameter tuning with Optuna, robust imputation, outlier handling, and proper data preprocessing.

## Process & Workflow 🔄

1. **Data Collection & EDA** 🔍  
   - Gathered historical hotel booking data.
   - Performed comprehensive exploratory data analysis (EDA) with Pandas and visualizations with Matplotlib/Seaborn.
   - Cleaned the data by removing leakage-prone features (e.g., booking_changes, assigned_room_type) and rows with no guests.

2. **Feature Engineering & Preprocessing** ⚙️  
   - Extracted date features from reservation dates (year, month, day, weekday).
   - Applied imputation (median for numerics, mode for categoricals) and one-hot encoding.
   - Handled outliers with IsolationForest.
   - Implemented target transformation (using `np.log1p` for ADR) to reduce skewness.

3. **Modeling & Tuning** 📊  
   - **Classification:** Evaluated models like CatBoostClassifier, RandomForestClassifier, and XGBoostClassifier.
   - **Regression:** Evaluated models such as CatBoostRegressor, XGBoostRegressor, and RandomForestRegressor.
   - **Hyperparameter Tuning:** Used Bayesian optimization with Optuna to fine-tune the regression model.  
     **Best Regression Model Results:**  
     - **Best Trial:**  
       - Value (mean neg MSE): `-0.17181247463698596`  
       - Parameters:  
         - `select_k_best__k`: 30  
         - `model__depth`: 10  
         - `model__learning_rate`: 0.06131215422518232  
         - `model__iterations`: 350  
     - **Final Evaluation on Test Set:**  
       - RMSE: **24.08**  
       - MAE: **16.10**  
       - R²: **0.73**

4. **Deployment** 💻  
   - Built a production-ready API using **FastAPI**.
   - Containerized the solution using **Docker** for scalable deployment.
   - The final model pipelines (both classification and regression) are saved with joblib for easy loading in production.

## Technology Stack 🛠️
- **Programming & Data Processing:** Python, Pandas, NumPy
- **Machine Learning:** scikit-learn, CatBoost, XGBoost, RandomForest
- **Hyperparameter Tuning:** Optuna, SelectKbest
- **Visualization:** Matplotlib, Seaborn
- **Deployment:** FastAPI, Docker
- **Others:** IsolationForest, One-Hot Encoding, Target Transformation (log)


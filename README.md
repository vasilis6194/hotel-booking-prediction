# Hospitality Predictive Analytics: End-to-End ML Pipeline  
**Real-time Booking Cancellation & ADR Prediction System**  

## 📖 Overview
This project builds an **end-to-end predictive analytics pipeline** for the hospitality industry, focusing on two critical tasks:  
1. **Booking Cancellation Prediction (Classification)**: Predict whether a hotel booking will be canceled.  
2. **Average Daily Rate (ADR) Prediction (Regression)**: Forecast the price per night for a booking.  

The solution is production-ready, providing **real-time predictions** through an API built with **FastAPI**, a frontend built with **React**, and containerized with **Docker** for easy deployment.  

---

## 🎯 **Project Goals**
✔️ **Predict Booking Cancellations** – Optimize hotel management and reduce lost revenue.  
✔️ **Forecast ADR** – Improve dynamic pricing strategies for hotels.  
✔️ **Deployment-Ready** – Serve predictions via API & Docker for scalability.  
✔️ **Model Optimization** – Use feature engineering, Optuna-based hyperparameter tuning, and outlier handling.  

---

## 🔄 **Workflow & Implementation**

### **1️⃣ Data Collection & Preprocessing**
📌 **Steps Taken:**  
- ✅ Collected **hotel booking data** and explored data distributions.  
- ✅ **Feature Engineering** – Extracted date-based features (**year, month, weekday**).  
- ✅ **Handled missing values** with median/mode imputation.  
- ✅ **One-hot encoded categorical features** to prepare for ML models.  
- ✅ **Filtered out invalid bookings** (e.g., those with no guests).  
- ✅ **Handled outliers** using **IsolationForest**.  

---

### **2️⃣ Model Training & Tuning**
📌 **Classification (Cancellation Prediction)**  
- 🔹 **Models Evaluated**: CatBoost, RandomForest, XGBoost.  
- 🔹 **Final Model**: CatBoostClassifier.  
- 🔹 **Hyperparameter Tuning**: Used **Optuna** for Bayesian optimization.  

📌 **Regression (ADR Prediction)**  
- 🔹 **Models Evaluated**: CatBoostRegressor, XGBoost, RandomForest.  
- 🔹 **Final Model**: **CatBoostRegressor with Log-Transformed ADR** for improved predictions.  
- 🔹 **Hyperparameter Tuning**: **Optuna** optimized the model hyperparameters.  

**Best Regression Model Results:**  
- **RMSE:** 24.08  
- **MAE:** 16.10  
- **R²:** 0.73  

---

### **3️⃣ API Development with FastAPI**
📌 **Implemented API Endpoints:**  
- ✅ `POST /predict/cancellation` – Predicts whether a booking will be canceled.  
- ✅ `POST /predict/adr` – Predicts the Average Daily Rate (ADR).  
- ✅ **Input validation** to prevent incorrect data entry.  

---

### **4️⃣ Frontend Development (React)**
📌 **Features:**  
- ✅ **Two Forms for Predictions** – Separate forms for ADR prediction and cancellation prediction.  
- ✅ **Dropdowns for categorical fields** like Hotel Type, Meal Type, Room Type, etc.  
- ✅ **Form validation** to prevent invalid user inputs.  
- ✅ **Real-time API integration** with `axios` for fetching predictions.  

---

## 🚀 **Deployment using Docker**
This project is containerized using **Docker** with separate services for:  
- **Regression Model Backend** (Port **8000**)  
- **Classification Model Backend** (Port **8001**)  
- **Frontend (React)** (Port **3000**)  

### **1️⃣ Docker Setup**
✅ Ensure you have **Docker** installed.  
✅ Clone the repository:  
```bash
git clone https://github.com/vasilis6194/hotel-booking-prediction.git
cd hotel-booking-prediction
```
✅ Build & Run Containers using Docker Compose:

```bash
docker-compose up --build
```
✅ Stop containers when done:

```bash
docker-compose down
```

### 🔧**Using the Application**
- 1️⃣ Run the Application (via Docker Compose or manually).
- 2️⃣ Open your browser and go to http://localhost:3000.
- 3️⃣ Select the prediction type: ADR or Cancellation.
- 4️⃣ Fill in the form fields and click Predict.
- 5️⃣ View real-time predictions on the screen! 🎉

### 📌 **Next Steps**
- 🚀 Deploy on a Cloud Server (AWS, Google Cloud, or DigitalOcean).
- 📊 Store Predictions in a Database (PostgreSQL/MongoDB).
- 🔐 Add User Authentication (JWT, OAuth).
- 📉 Enable Batch Predictions (Upload CSV files for bulk processing).
- 📧 Send Email Alerts for High Cancellation Probabilities.

Hospitality Predictive Analytics: End-to-End ML Pipeline with AWS Deployment
============================================================================

🌍 **Live Application**: [https://hotel-app.duckdns.org](https://hotel-app.duckdns.org)
---------------------------------------------------------------------------------------

📖 **Overview**
---------------

This project is an **end-to-end machine learning pipeline** designed for the **hospitality industry**, capable of real-time **Booking Cancellation Prediction** and **Average Daily Rate (ADR) Forecasting**. It is **fully deployed on AWS**, leveraging **FastAPI**, **React**, **Docker**, and **Nginx**, with HTTPS secured via **Let's Encrypt**.

🚀 **Key Achievements**
-----------------------

- ✅ **Cloud Deployment with AWS EC2** – Hosted the complete application in the cloud.
- ✅ **Domain & HTTPS Setup** – Configured **DuckDNS** for a free domain & **Let's Encrypt** for SSL.
- ✅ **Production-Ready API** – Built using **FastAPI**, handling real-time predictions.
- ✅ **Scalable Architecture** – Containerized **backend, frontend, and API** using **Docker**.
- ✅ **Reverse Proxy with Nginx** – Optimized request handling for improved performance.
- ✅ **Security & Networking** – Configured AWS **security groups, firewall (UFW), and Nginx**.

🎯 **Project Goals**
--------------------

- ✔️ **Predict Booking Cancellations** – Helps hotels optimize revenue and reduce losses.
- ✔️ **Forecast ADR** – Supports dynamic pricing strategies.
- ✔️ **Cloud Deployment** – Ensures real-time access with AWS & Docker.
- ✔️ **Model Optimization** – Includes feature engineering, Optuna hyperparameter tuning, and outlier handling.

🔄 **Workflow & Implementation**
--------------------------------

### **1️⃣ Data Collection & Preprocessing**

📌 **Key Steps:**

*   **Collected & cleaned** hotel booking data.
    
*   **Feature Engineering** – Extracted **date-based** features (year, month, weekday).
    
*   **One-hot encoded categorical variables** & handled missing values.
    
*   **Filtered invalid bookings** (e.g., zero guests).
    
*   **Used IsolationForest** to handle outliers.
    

### **2️⃣ Model Training & Optimization**

📌 **Classification (Booking Cancellation Prediction)**

*   **Models Evaluated:** CatBoost, RandomForest, XGBoost.
    
*   **Best Model:** CatBoostClassifier .
    

📌 **Regression (ADR Prediction)**

*   **Models Evaluated:** CatBoostRegressor, XGBoost, RandomForest.
    
*   **Best Model:** **CatBoostRegressor** with **Log-Transformed ADR**  (Optimized via **Optuna**) for better predictions.
    

#### **Final Regression and Classification Model Results:**

*   **RMSE:** 24.08
*   **MAE:** 16.10
*   **R²:** 0.73
*   **Accuracy:** 87%
    

### **3️⃣ API Development with FastAPI**

📌 **Endpoints:**

*   POST /predict/cancellation – Predicts whether a booking will be canceled.
    
*   POST /predict/adr – Predicts the Average Daily Rate (ADR).
    
*   Includes **input validation & error handling**.
    

### **4️⃣ Frontend Development (React)**

📌 **Features:**

*   **Interactive UI** for booking cancellation & ADR prediction.
    
*   **Dropdowns & form validation** for structured inputs.
    
*   **Real-time API calls** via axios.
    

🏗 **Deployment on AWS (Step-by-Step)**
---------------------------------------

### **1️⃣ AWS EC2 Setup**

- ✅ Launched an **Ubuntu 22.04** EC2 instance.
- ✅ Configured **security groups** to allow HTTP (80), HTTPS (443), API (8000, 8001).
- ✅ Set up an **Elastic IP** for a static public IP.

### **2️⃣ Docker & Application Setup**

- ✅ **Installed Docker & Docker Compose** for containerized deployment.
- ✅ **Transferred project files** to the AWS instance using scp.
- ✅ **Built and ran the application** using docker-compose up --build -d.

### **3️⃣ Reverse Proxy with Nginx**

- ✅ Installed & configured **Nginx** as a **reverse proxy**.
- ✅ Ensured traffic from **port 80/443 → React frontend (3000)**.
- ✅ Added HTTPS **SSL certificates** using **Certbot (Let's Encrypt)**.

### **4️⃣ Domain & SSL**

- ✅ Registered a **free domain with DuckDNS** (hotel-app.duckdns.org).
- ✅ Configured **Let's Encrypt SSL** for HTTPS (certbot).
- ✅ Successfully hosted a **secure, public web application**.

🔧 **Running the Application**
------------------------------
### **1️⃣ Access the Application**

*   Visit: [**https://hotel-app.duckdns.org**](https://hotel-app.duckdns.org)
*   Make predictions for **booking cancellations & ADR**.

### **2️⃣ Clone & Deploy Locally**

```bash
git clone https://github.com/vasilis6194/hotel-booking-prediction.git
cd hotel-booking-prediction
docker-compose up --build
```

### **3️⃣ Stop Containers**

```bash
docker-compose down  
```
  

    



📌 **Key Learnings & Skills Acquired**
--------------------------------------

### **Cloud & Deployment**

- ✅ **AWS EC2** – Launched & configured a cloud instance.
- ✅ **Docker & Docker Compose** – Containerized ML models & frontend.
- ✅ **Nginx Reverse Proxy** – Managed traffic routing & API requests.
- ✅ **Let's Encrypt & Certbot** – Enabled **free HTTPS encryption**.
- ✅ **Firewall & Security Groups** – Configured UFW & AWS rules.
- ✅ **Domain Configuration** – Used **DuckDNS** for free custom domains.

### **Software Development**

- ✅ **FastAPI & React Integration** – Built a complete ML web app.
- ✅ **REST API Development** – Created & tested ML model endpoints.
- ✅ **State Management & API Calls** – Used Axios & React Hooks.
- ✅ **Frontend-Backend Communication** – Structured requests & error handling.

🚀 **Next Steps**
-----------------

*   **Integrate PostgreSQL** – Store predictions for analytics.
    
*   **Implement Authentication** – Secure API endpoints.
    
*   **Enable Batch Predictions** – Support CSV uploads.
    
*   **Improve UI/UX** – Enhance frontend design & user experience.
    

🎯 **Final Thoughts**
---------------------

This project was an incredible learning experience, covering **cloud deployment, containerization, web development, API integration, security, and networking**. Now, anyone can access and use the model **in real-time** at [**hotel-app.duckdns.org**](https://hotel-app.duckdns.org)! 🚀🔥

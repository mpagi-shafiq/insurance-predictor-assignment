## FiqHaks Insurance Predictor 🛡️

FiqHaks Predictor is an intelligent web application designed to simplify insurance premium estimation. By processing user data through a machine learning model, the app provides real-time quotes and helps users choose the most suitable coverage plan for their needs.

## 🌟 Key Highlights
Smart Estimations: Generates instant quotes using a trained machine learning backend (insurance_model.pkl). 

Plan Customization: Offers three distinct coverage tiers—Basic, Standard, and Pro.

Localized Pricing: Calculations are automatically converted into Ugandan Shillings (UGX).

Risk Assessment: Built-in safety logic limits plan availability based on age, BMI, and smoking status.

Instant Documentation: Allows users to download an official summary receipt of their chosen plan.

## 📂 Project Components
web_app_version.py: The core application logic and Streamlit interface.

insurance_model.pkl: The predictive engine used for premium calculations.

requirements.txt: Necessary libraries to run the environment.

FiqHaks logo.png: Official application branding assets.

.devcontainer: Environment configuration for developers.

## 🚀 Getting Started
Step 1: Clone the repository
git clone github.com
cd insurance-predictor-assignment
Step 2: Install necessary packages
pip install -r requirements.txt
Step 3: Launch the app
streamlit run web_app_version.py

## ⚙️ The Calculation Engine
The predictor evaluates user profiles (Age, BMI, Gender, and Smoking status) to determine a base premium. From that base, three tiers are generated:
Budget Tier (Basic): A focused plan at 60% of the standard rate.
Standard Tier: The full-coverage base prediction from the model.
Premium Tier (Pro): An enhanced plan with a 40% benefit markup, available for low-risk profiles.

## ✍️ Project Author
Developed by MPAGI SHAFIQ
GitHub: @mpagi-shafiq

import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FiqHaks Predictor | Fin-Health Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PROFESSIONAL STYLING (CSS) ---
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    /* Plan Card Styling */
    .plan-card {
        background-color: #blue;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e6e9ef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        height: 100%;
    }
    .plan-price {
        color: #1E3A8A;
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0;
    }
    .recommended {
        border: 2px solid #3B82F6;
        background-color: #blue;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MODEL & DATA LOADING ---
@st.cache_resource
def load_assets():
    try:
        with open("insurance_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'insurance_model.pkl' exists.")
        return None

model = load_assets()
EXCHANGE_RATE = 3700

# --- 4. SIDEBAR INPUTS ---
with st.sidebar:
    st.image("FiqHaks logo.png", width=150)
    st.header("👤 User Profile")
    
    name = st.text_input("Full Name", placeholder="Enter your name")
    age = st.slider("Age", 18, 100, 25)
    bmi = st.slider("BMI", 10.0, 50.0, 24.0)
    children = st.selectbox("Children", [0, 1, 2, 3, 4, 5])
    sex = st.radio("Gender", ["Male", "Female"], horizontal=True)
    smoker = st.radio("Smoker?", ["No", "Yes"], horizontal=True)
    alcohol = st.radio("Drink Alcohol?", ["No", "Yes"], horizontal=True)
    occupation = st.selectbox("Occupation Risk", ["Low risk", "High risk"])

# --- 5. CORE LOGIC ---
if model:
    # Prepare Data
    sex_val = 1 if sex == "Male" else 0
    smoker_val = 1 if smoker == "Yes" else 0
    
    input_df = pd.DataFrame([{
        'age': age, 'sex': sex_val, 'bmi': bmi, 
        'children': children, 'smoker': smoker_val
    }])
    
    # Prediction
    base_prediction = model.predict(input_df)[0]
    final_price_ugx = max(0, base_prediction * EXCHANGE_RATE)

    # --- 6. DASHBOARD TABS ---
    tab1, tab2, tab3 = st.tabs(["🛡️ Insurance Plans", "📈 Wealth Growth", "🏥 Health Insights"])

    with tab1:
        st.title("Smart Plan Selector")
        st.markdown(f"**Welcome, {name if name else 'Valued Client'}**. Based on your profile, here are your qualified plans:")
        
        col1, col2, col3 = st.columns(3)
        
        # BASIC PLAN
        with col1:
            st.markdown(f'''{get_badge('BASIC')}
                <h3>BASIC</h3>
                <p>Essential coverage</p>
                <div class="plan-price">UGX {final_price_ugx * 0.7:,.0f}</div>
                <p style="font-size: 0.8em;">Per Year</p>
                <hr>
                <p>✔️ Emergency Care<br>✔️ Hospital Stays</p>
            </div>''', unsafe_allow_html=True)
            if st.button("Select Basic", key="b1"): st.session_state.plan = "Basic"

        # STANDARD (Recommended)
        with col2:
            st.markdown(f'''{get_badge('STANDARD')}
                <span style="background:#3B82F6; color:white; padding:2px 10px; border-radius:10px; font-size:12px;">RECOMMENDED</span>
                <h3>STANDARD</h3>
                <p>Family Protection</p>
                <div class="plan-price">UGX {final_price_ugx:,.0f}</div>
                <p style="font-size: 0.8em;">Per Year</p>
                <hr>
                <p>✔️ All Basic Features<br>✔️ Dental & Vision</p>
            </div>''', unsafe_allow_html=True)
            if st.button("Select Standard", key="b2"): st.session_state.plan = "Standard"

        # PRO
        with col3:
            st.markdown(f'''{get_badge('PRO')}
                <h3>PRO</h3>
                <p>Premium Peace of Mind</p>
                <div class="plan-price">UGX {final_price_ugx * 1.4:,.0f}</div>
                <p style="font-size: 0.8em;">Per Year</p>
                <hr>
                <p>✔️ Global Coverage<br>✔️ Zero Deductible</p>
            </div>''', unsafe_allow_html=True)
            if st.button("Select Pro", key="b3"): st.session_state.plan = "Pro"

    recommendation = "STANDARD" #default
    if smoker == "Yes" or bmi > 30 or age > 50:
        recommendation = "PRO"
    elif age < 25 and bmi < 25:
        recommedation = "BASIC"

    #function to show badge only if it matches
    def get_badge(plan_name):
        if plan_name == recommendation:
            return '<span style="background: #blue; color:white; padding: 2px 10px; border-radius:10px; font-size: 12px;">RECOMMENDED</span>'
    with tab2:
        st.header("Financial Wellness")
        st.write("What if you invested the difference between the Basic and Pro plans?")
        
        savings = (final_price_ugx * 1.4) - (final_price_ugx * 0.7)
        years = 10
        growth_rate = 0.10 # 10% annual return
        future_value = savings * (((1 + growth_rate) ** years - 1) / growth_rate)
        
        c1, c2 = st.columns(2)
        c1.metric("Annual Potential Savings", f"UGX {savings:,.0f}")
        c2.metric("Projected 10-Year Wealth", f"UGX {future_value:,.0f}")
        
        st.info("💡 Investing the premium difference into a diversified fund can significantly boost your net worth.")

    with tab3:
        st.header("Personalized Health Report")
        if bmi > 25:
            st.warning(f"Your BMI is {bmi}. Reducing this to 24 could lower your premiums by approximately 15%.")
        else:
            st.success("Your BMI is in the healthy range. You are eligible for our lowest rate tiers.")
        
        if smoker == "Yes":
            st.error("🚭 Smoking status is the highest driver of your premium cost.")

    # --- 7. FINAL RECEIPT & DOWNLOAD ---
    st.divider()
    if 'plan' in st.session_state:
        st.success(f"Excellent choice! Your {st.session_state.plan} plan is being processed.")
        
        receipt_text = f"""
        FIQHAKS PREDICTOR OFFICIAL RECEIPT
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        -----------------------------------
        Client Name: {name}
        Selected Plan: {st.session_state.plan}
        Age: {age} | BMI: {bmi}
        Annual Premium: UGX {final_price_ugx:,.0f}
        -----------------------------------
        Support: fiqhaks.company@gmail.com
        """
        
        st.download_button(
            label="📄 Download Official Quote",
            data=receipt_text,
            file_name=f"{name}_Quote.txt",
            mime="text/plain"
        )

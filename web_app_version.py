
import streamlit as st
import pandas as pd
import pickle

# Page Configuration
st.set_page_config(initial_sidebar_state="expanded", page_title="FiqHaks Predictor", page_icon="FiqHaks logo.png",)

# Load Model
@st.cache_resource
def load_model():
    with open("insurance_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# Sidebar Inputs
st.sidebar.header("User Profile")
st.sidebar.image("FiqHaks logo.png", use_container_width=True)
user_name = st.sidebar.text_input("Enter your name:",placeholder = "Full name")
age = st.sidebar.slider("Age", 18, 100, 30)
bmi = st.sidebar.slider("BMI", 10.0, 50.0, 24.0)
children = st.sidebar.selectbox("Children", [0, 1, 2, 3, 4, 5])
smoker = st.sidebar.radio("Smoker?", ["No", "Yes"])
sex = st.sidebar.selectbox("Gender", ["Male", "Female"])
alcohol = st.sidebar.radio("Do you drink alcohol?", ["No","Yes"])
occupation = st.sidebar.selectbox("Ocupation risk",["Low risk","High risk"])


# Converting to model format
smoker_val = 1 if smoker == "Yes" else 0
sex_val = 1 if sex == "Male" else 0

# Prediction Logic
input_df = pd.DataFrame([[age, sex_val, bmi, children, smoker_val]], 
                        columns=['age', 'sex', 'bmi', 'children', 'smoker'])
base_prediction = model.predict(input_df)[0]
final_price = max(0, base_prediction)

if final_price > 0:
    # Header
    st.title("FiqHaks Predictor: Smart Plan Selector")
    st.markdown(f"Based on your profile, here are the plans you qualify for:")
    st.divider()

    #currency conversion
    exchange_rate = 3700
    ugx_price = final_price*exchange_rate

    # Insurance plan logic
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("BASIC")
        st.write("Essential coverage for emergencies.")
        st.header(f"UGX{(ugx_price * 0.7):,.0f}")
        st.caption("per year")
        st.write("---")
        st.write("✔ Emergency Care")
        st.write("✔ Hospital Stays")
        if smoker == "Yes" or bmi > 35:
            st.warning("Best value for your profile")

    with col2:
        st.subheader("STANDARD")
        st.write("Balanced protection for families.")
        st.header(f"UGX{ugx_price:,.0f}")
        st.caption("per year")
        st.write("---")
        st.write("✔ All Basic Features")
        st.write("✔ Prescription Drugs")
        st.write("✔ Dental Cover")
        if smoker == "No" and (20 <= bmi <= 30):
            st.info("Recommended for you")

    with col3:
        st.subheader("PRO")
        st.write("Full premium peace of mind.")
        st.header(f"UGX{(ugx_price * 1.4):,.0f}")
        st.caption("per year")
        st.write("---")
        st.write("✔ All Standard Features")
        st.write("✔ International Coverage")
        st.write("✔ Zero cash Deductible")
        if age < 40 and smoker == "No":
            st.success("You qualify for Pro")

    # 7. Final Interactive Element
    st.divider()
    selected_plan = st.selectbox("Which plan would you like to proceed with?", ["Basic", "Standard", "Pro"])

    if st.button("Generate My Official Receipt "):
        st.balloons()
        st.success(f"Excellent choice! Your {selected_plan} plan application is now being processed.")
        
        # Download logic
        summary = f"FiqHaks Predictor Receipt\nName: {user_name:}\nPlan: {selected_plan}\nAge: {age}\nBMI: {bmi}\nSmoker: {smoker}\nTotal: UGX{ugx_price:,.0f}"
        st.download_button("Download Summary", summary, file_name="my_Receipt.txt")

else:
    st.error("Application Status: Not eligible")
    st.markdown("""We regret to inform you that based on the current profile, we can't offer you a quote.""")
    st.info("Please contact our support team at fiqhaks.company@gmail.com")


hide_streamlit_style = """
                        <style>
                        #Mainmenu {visibility:hidden;}
                        header {visibility:hidden;}
                        footer {visibility:hidden;}
                        .stAppDeployButton {display:none;}
                        </style>
                      """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

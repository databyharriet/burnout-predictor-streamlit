# 🧠 Burnout Predictor - Streamlit App

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ─────────────────────────────
# Load Model and Scaler
# ─────────────────────────────
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# ─────────────────────────────
# Load Data for EDA
# ─────────────────────────────
train_data = pd.read_csv("train.csv")

# ─────────────────────────────
# App Config
# ─────────────────────────────
st.set_page_config(page_title="Burnout Predictor", layout="centered")
st.title("🔥 Burnout Risk Predictor")
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["📊 Exploratory Data Analysis", "🧠 Burnout Predictor"])

# ─────────────────────────────
# 1. EDA Section
# ─────────────────────────────
if selection == "📊 Exploratory Data Analysis":
    st.subheader("📊 Dataset Preview")
    st.dataframe(train_data.head())

    st.subheader("📌 Summary Statistics")
    st.write(train_data.describe())

    st.subheader("🧮 Correlation Matrix")
    st.dataframe(train_data.select_dtypes(include='number').corr())


    st.subheader("📊 Burnout Distribution")
    st.bar_chart(train_data["Burn Rate"].value_counts())

# ─────────────────────────────
# 2. Prediction Section
# ─────────────────────────────
elif selection == "🧠 Burnout Predictor":
    st.subheader("🧠 Predict Employee Burnout")

    st.write("Enter employee information:")

    # Sample input form – customize these fields as per your actual model features
    age = st.number_input("Age", 18, 65, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    company_type = st.selectbox("Company Type", ["Product", "Service"])
    designation = st.selectbox("Designation (0-4)", list(range(5)))
    resource_allocation = st.selectbox("Resource Allocation (0-5)", list(range(6)))
    mental_fatigue_score = st.slider("Mental Fatigue Score", 0.0, 10.0, 5.0, 0.1)
    workload = st.slider("Workload Average", 0.0, 10.0, 5.0, 0.1)

    if st.button("🔮 Predict Burnout"):
        user_input = pd.DataFrame([[
            age,
            0 if gender == "Male" else 1,
            0 if company_type == "Product" else 1,
            designation,
            resource_allocation,
            workload,
            mental_fatigue_score
        ]], columns=[
            "Age", "Gender", "Company Type", "Designation", "Resource Allocation",
            "Workload Average", "Mental Fatigue Score"
        ])

        # Scale input
        scaled_input = scaler.transform(user_input)

        # Predict
        prediction = model.predict(scaled_input)[0]
        st.success(f"🔥 Predicted Burn Rate: **{round(prediction, 3)}**")

    # Bulk CSV Upload
    st.markdown("---")
    st.subheader("📁 Bulk Prediction via CSV")
    uploaded_file = st.file_uploader("Upload a CSV file with employee details")

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)

        try:
            scaled = scaler.transform(input_df)
            preds = model.predict(scaled)

            input_df["Predicted Burn Rate"] = preds
            st.write("✅ Predictions complete:")
            st.dataframe(input_df)

            # Download predictions
            csv = input_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Predictions as CSV",
                data=csv,
                file_name="burnout_predictions.csv",
                mime='text/csv'
            )
        except Exception as e:
            st.error("⚠️ Error in file format. Please ensure it matches expected columns.")

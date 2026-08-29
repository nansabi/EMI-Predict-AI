
import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.feature_engineering import engineer_features, RAW_FORM_DEFAULTS
from utils.model_loader import load_artifacts, predict_applicant

st.set_page_config(page_title="Predict EMI", page_icon="🔮", layout="wide")
st.title("🔮 Predict EMI Eligibility & Maximum Amount")

artifacts = load_artifacts()
if "error" in artifacts:
    st.error("Models are not loaded. Go to the Home page for setup instructions.")
    st.stop()

EMI_SCENARIOS = ["Personal Loan EMI", "Home Appliances EMI", "Vehicle EMI", "Education EMI", "E-commerce Shopping EMI"]

with st.form("prediction_form"):
    st.subheader("Applicant Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Personal**")
        age = st.slider("Age", 25, 60, RAW_FORM_DEFAULTS["age"])
        gender = st.selectbox("Gender", ["MALE", "FEMALE"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married"])
        education = st.selectbox("Education", ["High School", "Graduate", "Post Graduate", "Professional"])
    with c2:
        st.markdown("**Employment & Income**")
        monthly_salary = st.number_input("Monthly Salary (Rs)", 0, 500000, RAW_FORM_DEFAULTS["monthly_salary"], step=1000)
        employment_type = st.selectbox("Employment Type", ["Private", "Government", "Self-Employed"])
        years_of_employment = st.number_input("Years of Employment", 0.0, 40.0, RAW_FORM_DEFAULTS["years_of_employment"], step=0.5)
        company_type = st.selectbox("Company Type", ["Mid-size", "MNC", "Startup", "Small", "Large Indian"])
    with c3:
        st.markdown("**Housing & Family**")
        house_type = st.selectbox("House Type", ["Own", "Rented", "Family"])
        monthly_rent = st.number_input("Monthly Rent (Rs)", 0, 100000, RAW_FORM_DEFAULTS["monthly_rent"], step=500)
        family_size = st.number_input("Family Size", 1, 15, RAW_FORM_DEFAULTS["family_size"])
        dependents = st.number_input("Dependents", 0, 10, RAW_FORM_DEFAULTS["dependents"])

    st.markdown("---")
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("**Monthly Obligations**")
        school_fees = st.number_input("School Fees (Rs)", 0, 50000, RAW_FORM_DEFAULTS["school_fees"], step=500)
        college_fees = st.number_input("College Fees (Rs)", 0, 50000, RAW_FORM_DEFAULTS["college_fees"], step=500)
        travel_expenses = st.number_input("Travel Expenses (Rs)", 0, 30000, RAW_FORM_DEFAULTS["travel_expenses"], step=500)
    with c5:
        groceries_utilities = st.number_input("Groceries & Utilities (Rs)", 0, 50000, RAW_FORM_DEFAULTS["groceries_utilities"], step=500)
        other_monthly_expenses = st.number_input("Other Monthly Expenses (Rs)", 0, 50000, RAW_FORM_DEFAULTS["other_monthly_expenses"], step=500)
        existing_loans = st.selectbox("Existing Loans?", ["No", "Yes"])
    with c6:
        current_emi_amount = st.number_input("Current EMI Amount (Rs)", 0, 100000, RAW_FORM_DEFAULTS["current_emi_amount"], step=500)
        credit_score = st.slider("Credit Score", 300, 850, RAW_FORM_DEFAULTS["credit_score"])
        bank_balance = st.number_input("Bank Balance (Rs)", 0, 5000000, RAW_FORM_DEFAULTS["bank_balance"], step=5000)

    st.markdown("---")
    c7, c8, c9 = st.columns(3)
    with c7:
        emergency_fund = st.number_input("Emergency Fund (Rs)", 0, 2000000, RAW_FORM_DEFAULTS["emergency_fund"], step=2000)
    with c8:
        emi_scenario = st.selectbox("Loan Purpose (EMI Scenario)", EMI_SCENARIOS)
    with c9:
        requested_amount = st.number_input("Requested Loan Amount (Rs)", 1000, 2000000, RAW_FORM_DEFAULTS["requested_amount"], step=5000)

    requested_tenure = st.slider("Requested Tenure (months)", 3, 84, RAW_FORM_DEFAULTS["requested_tenure"])
    submitted = st.form_submit_button("🔍 Predict", use_container_width=True, type="primary")

if submitted:
    raw = {
        "age": age, "gender": gender, "marital_status": marital_status, "education": education,
        "monthly_salary": monthly_salary, "employment_type": employment_type,
        "years_of_employment": years_of_employment, "company_type": company_type,
        "house_type": house_type, "monthly_rent": monthly_rent, "family_size": family_size,
        "dependents": dependents, "school_fees": school_fees, "college_fees": college_fees,
        "travel_expenses": travel_expenses, "groceries_utilities": groceries_utilities,
        "other_monthly_expenses": other_monthly_expenses, "existing_loans": existing_loans,
        "current_emi_amount": current_emi_amount, "credit_score": credit_score,
        "bank_balance": bank_balance, "emergency_fund": emergency_fund,
        "emi_scenario": emi_scenario, "requested_amount": requested_amount,
        "requested_tenure": requested_tenure,
    }

    try:
        engineered_df = engineer_features(raw)
        eligibility, proba, classes, max_emi = predict_applicant(engineered_df, artifacts)

        st.markdown("## 📋 Prediction Results")
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("#### Eligibility")
            color_map = {"Eligible": "🟢", "High_Risk": "🟡", "Not_Eligible": "🔴"}
            icon = color_map.get(str(eligibility), "⚪")
            st.markdown(f"## {icon} {eligibility}")
            if proba is not None:
                proba_df = pd.DataFrame({"Class": classes, "Probability": proba}).sort_values("Probability", ascending=False)
                st.bar_chart(proba_df.set_index("Class"))
        with r2:
            st.markdown("#### Maximum Safe Monthly EMI")
            st.metric("Predicted Max EMI", f"Rs {max_emi:,.0f}")
            requested_emi_estimate = requested_amount / requested_tenure if requested_tenure > 0 else 0
            st.caption(f"Estimated EMI for requested loan: Rs {requested_emi_estimate:,.0f}/month")
            if requested_emi_estimate > max_emi:
                st.warning("⚠️ Requested EMI exceeds the predicted safe maximum.")
            else:
                st.success("✅ Requested EMI is within the predicted safe maximum.")

        log_row = {**raw, "predicted_eligibility": str(eligibility), "predicted_max_emi": round(max_emi, 2),
                   "timestamp": datetime.now().isoformat(timespec="seconds")}
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        log_path = os.path.join(data_dir, "applicants.csv")
        log_df = pd.DataFrame([log_row])
        if os.path.exists(log_path):
            log_df.to_csv(log_path, mode="a", header=False, index=False)
        else:
            log_df.to_csv(log_path, index=False)

    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.exception(e)

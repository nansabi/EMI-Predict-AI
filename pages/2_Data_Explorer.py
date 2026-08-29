
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")
st.title("📊 Applicant Data Explorer (CRUD)")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATA_PATH = os.path.join(DATA_DIR, "applicants.csv")
os.makedirs(DATA_DIR, exist_ok=True)


def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()


def save_data(df):
    df.to_csv(DATA_PATH, index=False)


df = load_data()

if df.empty:
    st.info("No applicant records yet. Records are logged automatically from the Predict EMI page.")
else:
    st.markdown(f"**{len(df)} record(s) on file**")
    st.dataframe(df, use_container_width=True, height=350)

    st.markdown("### ✏️ Edit or Delete a Record")
    row_index = st.number_input("Row index to edit/delete", min_value=0, max_value=max(len(df) - 1, 0), step=1)

    if st.button("🗑️ Delete this record"):
        df = df.drop(index=row_index).reset_index(drop=True)
        save_data(df)
        st.success(f"Record {row_index} deleted.")
        st.rerun()

    st.download_button("⬇️ Export all records as CSV", data=df.to_csv(index=False),
                        file_name="emipredict_applicants.csv", mime="text/csv")

st.markdown("### ➕ Add a Record Manually")
with st.form("manual_add_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        m_age = st.number_input("Age", 25, 60, 35)
        m_gender = st.selectbox("Gender", ["MALE", "FEMALE"])
    with c2:
        m_salary = st.number_input("Monthly Salary", 0, 500000, 50000, step=1000)
        m_credit = st.slider("Credit Score", 300, 850, 700)
    with c3:
        m_scenario = st.selectbox("EMI Scenario", ["Personal Loan EMI", "Home Appliances EMI", "Vehicle EMI", "Education EMI", "E-commerce Shopping EMI"])
        m_elig = st.selectbox("Eligibility (manual entry)", ["Eligible", "High_Risk", "Not_Eligible"])

    add_submitted = st.form_submit_button("Add Record")
    if add_submitted:
        new_row = {"age": m_age, "gender": m_gender, "monthly_salary": m_salary, "credit_score": m_credit,
                   "emi_scenario": m_scenario, "predicted_eligibility": m_elig, "predicted_max_emi": None,
                   "timestamp": pd.Timestamp.now().isoformat(timespec="seconds")}
        df_new = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df_new)
        st.success("Record added.")
        st.rerun()

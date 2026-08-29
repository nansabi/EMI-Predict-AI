
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Model Insights", page_icon="📈", layout="wide")
st.title("📈 Model Insights & Comparison")

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
CLF_PATH = os.path.join(MODELS_DIR, "classification_comparison.csv")
REG_PATH = os.path.join(MODELS_DIR, "regression_comparison.csv")

st.markdown("### 🏆 Selected Production Models")
c1, c2 = st.columns(2)
with c1:
    st.info("**Classification:** XGBoost Classifier")
with c2:
    st.info("**Regression:** XGBoost Regressor")

st.markdown("---")
st.markdown("### 🧪 Classification Model Comparison")
if os.path.exists(CLF_PATH):
    st.dataframe(pd.read_csv(CLF_PATH), use_container_width=True)
else:
    st.warning("classification_comparison.csv not found in models/ folder.")

st.markdown("### 📉 Regression Model Comparison")
if os.path.exists(REG_PATH):
    st.dataframe(pd.read_csv(REG_PATH), use_container_width=True)
else:
    st.warning("regression_comparison.csv not found in models/ folder.")

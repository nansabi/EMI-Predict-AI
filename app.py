
import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(__file__))
from utils.model_loader import load_artifacts

st.set_page_config(page_title="EMIPredict AI", page_icon="💳", layout="wide", initial_sidebar_state="expanded")

# ------------------------------------------------------------------
# 🎨 CUSTOM THEME + SMOOTH ANIMATIONS
# ------------------------------------------------------------------
st.markdown("""
<style>

:root {
    --plum: #601D49;
    --rose: #BD5579;
    --blush: #EA9D9D;
    --cream: #FFEBB8;
}

/* ---------- Global fade-in ---------- */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
@keyframes floatIcon {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
}

/* ---------- App background ---------- */
.stApp {
    background: linear-gradient(160deg, var(--plum) 0%, #7a2a5e 35%, var(--rose) 100%);
    animation: fadeIn 0.8s ease-in-out;
}

/* ---------- Main content container ---------- */
.block-container {
    animation: fadeInUp 0.6s ease-out;
    padding-top: 2rem;
}

/* ---------- Titles ---------- */
h1, h2, h3 {
    color: var(--cream) !important;
    animation: fadeInUp 0.7s ease-out;
    transition: transform 0.3s ease;
}
h1:hover {
    transform: translateX(4px);
}

/* Subtitle / caption text */
.stMarkdown p, .stCaption, p {
    color: var(--cream) !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--plum) 0%, #4a1638 100%);
    border-right: 1px solid var(--rose);
    animation: fadeIn 0.9s ease-in-out;
}
section[data-testid="stSidebar"] * {
    color: var(--cream) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: var(--rose);
    opacity: 0.5;
}

/* ---------- Metrics (Project Snapshot cards) ---------- */
div[data-testid="stMetric"] {
    background: rgba(255, 235, 184, 0.08);
    border: 1px solid var(--blush);
    border-radius: 14px;
    padding: 18px 12px;
    text-align: center;
    backdrop-filter: blur(6px);
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.35s ease,
                border-color 0.35s ease;
    animation: fadeInUp 0.8s ease-out;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 10px 25px rgba(96, 29, 73, 0.45);
    border-color: var(--cream);
}
div[data-testid="stMetricLabel"] {
    color: var(--blush) !important;
    font-weight: 500;
}
div[data-testid="stMetricValue"] {
    color: var(--cream) !important;
    font-weight: 700;
}

/* ---------- Alert boxes (success / error / info) ---------- */
div[data-testid="stAlert"] {
    border-radius: 12px;
    animation: fadeInUp 0.5s ease-out;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    border: 1px solid transparent;
}
div[data-testid="stAlert"]:hover {
    transform: translateX(3px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}

/* Success */
div[data-testid="stAlert"][kind="success"] {
    background: rgba(234, 157, 157, 0.15);
    border-color: var(--blush);
}
/* Error */
div[data-testid="stAlert"][kind="error"] {
    background: rgba(189, 85, 121, 0.2);
    border-color: var(--rose);
}
/* Info */
div[data-testid="stAlert"][kind="info"] {
    background: rgba(255, 235, 184, 0.12);
    border-color: var(--cream);
}

/* ---------- Code blocks ---------- */
.stCodeBlock, pre {
    border-radius: 10px !important;
    border: 1px solid var(--rose) !important;
    animation: fadeIn 0.6s ease-in-out;
}

/* ---------- Divider ---------- */
hr {
    border-color: var(--blush) !important;
    opacity: 0.4;
}

/* ---------- Subtle shimmer accent under title ---------- */
.stApp > header {
    background: transparent;
}

/* ---------- Smooth scroll ---------- */
html {
    scroll-behavior: smooth;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("💳 EMIPredict AI")
    st.caption("Intelligent Financial Risk Assessment Platform")
    st.markdown("---")
    st.markdown("**Navigate using the pages above:**\n- 🔮 Predict EMI\n- 📊 Data Explorer\n- 📈 Model Insights")
    st.markdown("---")
    st.caption("Built with Python, scikit-learn, XGBoost, MLflow & Streamlit")

st.title("💳 EMIPredict AI")
st.subheader("Intelligent Financial Risk Assessment Platform")

st.markdown("""
Welcome! This platform uses machine learning to answer two questions for any loan applicant:

1. **Is this applicant eligible for an EMI?** (Eligible / High Risk / Not Eligible)
2. **What is the maximum monthly EMI they can safely afford?**

Head to **🔮 Predict EMI** in the sidebar to try a live prediction.
""")

st.markdown("### 📊 Project Snapshot")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Training Records", "404,800")
col2.metric("Input Features", "22")
col3.metric("EMI Scenarios", "5")
col4.metric("Best Regression RMSE", "₹1,187")

st.markdown("### ✅ Model Status")
artifacts = load_artifacts()

if "error" in artifacts:
    st.error("**Models not found.** Please place the following files in the models/ folder:")
    for label, path in artifacts["error"]:
        st.code(f"{label}: {path}")
else:
    st.success("✅ ColumnTransformer loaded")
    st.success("✅ Classification model loaded")
    st.success("✅ Regression model loaded")
    st.info("All models are ready. Go to **🔮 Predict EMI** to try a live prediction.")

st.markdown("---")
st.caption("EMIPredict AI · FinTech Capstone Project")

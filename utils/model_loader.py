
import os
import joblib
import streamlit as st

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

TRANSFORMER_FILENAME = "column_transformer.joblib"
CLASSIFIER_FILENAME = "best_classification_model.joblib"
REGRESSOR_FILENAME = "best_regression_model.joblib"


@st.cache_resource(show_spinner="Loading models...")
def load_artifacts():
    artifacts = {}
    missing = []

    transformer_path = os.path.join(MODELS_DIR, TRANSFORMER_FILENAME)
    clf_path = os.path.join(MODELS_DIR, CLASSIFIER_FILENAME)
    reg_path = os.path.join(MODELS_DIR, REGRESSOR_FILENAME)

    for label, path in [("transformer", transformer_path), ("classifier", clf_path), ("regressor", reg_path)]:
        if not os.path.exists(path):
            missing.append((label, path))

    if missing:
        return {"error": missing}

    artifacts["transformer"] = joblib.load(transformer_path)
    artifacts["classifier"] = joblib.load(clf_path)
    artifacts["regressor"] = joblib.load(reg_path)
    return artifacts


def predict_applicant(raw_features_df, artifacts):
    transformer = artifacts["transformer"]
    classifier = artifacts["classifier"]
    regressor = artifacts["regressor"]

    X_transformed = transformer.transform(raw_features_df)

    eligibility_pred = classifier.predict(X_transformed)[0]
    try:
        eligibility_proba = classifier.predict_proba(X_transformed)[0]
        classes = classifier.classes_
    except AttributeError:
        eligibility_proba = None
        classes = None

    max_emi_pred = float(regressor.predict(X_transformed)[0])
    max_emi_pred = max(0.0, max_emi_pred)

    return eligibility_pred, eligibility_proba, classes, max_emi_pred


import numpy as np
import pandas as pd

MAX_YEARS_OF_EMPLOYMENT = 40.0

EMPLOYMENT_TYPE_SCORES = {
    "Government": 3,
    "Private": 2,
    "Self-Employed": 1,
    "Self-employed": 1,
}

CREDIT_RISK_BINS = [300, 579, 669, 739, 799, 850]
CREDIT_RISK_LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"]


def engineer_features(raw: dict) -> pd.DataFrame:
    df = pd.DataFrame([raw])

    df["monthly_salary_safe"] = df["monthly_salary"].replace(0, 1e-6)
    df["requested_tenure_safe"] = df["requested_tenure"].replace(0, 1e-6)
    df["family_size_safe"] = df["family_size"].replace(0, 1e-6)

    df["total_monthly_expenses"] = (
        df["school_fees"] + df["college_fees"] + df["travel_expenses"]
        + df["groceries_utilities"] + df["other_monthly_expenses"] + df["monthly_rent"]
    )
    df["total_monthly_expenses_safe"] = df["total_monthly_expenses"].replace(0, 1e-6)

    df["debt_to_income_ratio"] = df["current_emi_amount"] / df["monthly_salary_safe"]
    df["expense_to_income_ratio"] = df["total_monthly_expenses"] / df["monthly_salary_safe"]
    df["affordability_ratio"] = (
        (df["monthly_salary_safe"] - df["total_monthly_expenses"] - df["current_emi_amount"])
        / df["monthly_salary_safe"]
    )
    df["estimated_requested_emi"] = df["requested_amount"] / df["requested_tenure_safe"]
    df["requested_emi_to_salary_ratio"] = df["estimated_requested_emi"] / df["monthly_salary_safe"]
    df["savings_ratio"] = (df["bank_balance"] + df["emergency_fund"]) / df["monthly_salary_safe"]

    for col in ["debt_to_income_ratio", "expense_to_income_ratio", "affordability_ratio",
                "requested_emi_to_salary_ratio", "savings_ratio"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(0)

    df["credit_risk_band"] = pd.cut(
        df["credit_score"], bins=CREDIT_RISK_BINS, labels=CREDIT_RISK_LABELS,
        right=True, include_lowest=True,
    ).astype(str)

    df["employment_type_score"] = (
        df["employment_type"].astype(str).map(EMPLOYMENT_TYPE_SCORES).fillna(0).astype(float)
    )
    df["employment_stability_score"] = df["employment_type_score"] * (
        1 + df["years_of_employment"] / MAX_YEARS_OF_EMPLOYMENT
    )

    df["dependents_burden"] = (df["dependents"] / df["family_size_safe"]).fillna(0)

    df["emergency_fund_months"] = (
        df["emergency_fund"] / df["total_monthly_expenses_safe"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    df["salary_x_credit_score"] = df["monthly_salary"] * df["credit_score"]
    df["age_x_employment_years"] = df["age"] * df["years_of_employment"]

    df = df.drop(columns=[
        "monthly_salary_safe", "requested_tenure_safe", "family_size_safe",
        "total_monthly_expenses_safe", "estimated_requested_emi", "family_size",
    ], errors="ignore")

    return df


RAW_FORM_DEFAULTS = {
    "age": 35, "gender": "MALE", "marital_status": "Married", "education": "Graduate",
    "monthly_salary": 50000, "employment_type": "Private", "years_of_employment": 5.0,
    "company_type": "Mid-size", "house_type": "Own", "monthly_rent": 0,
    "family_size": 4, "dependents": 2, "school_fees": 0, "college_fees": 0,
    "travel_expenses": 3000, "groceries_utilities": 8000, "other_monthly_expenses": 2000,
    "existing_loans": "No", "current_emi_amount": 0, "credit_score": 700,
    "bank_balance": 100000, "emergency_fund": 30000, "emi_scenario": "Personal Loan EMI",
    "requested_amount": 200000, "requested_tenure": 24,
}

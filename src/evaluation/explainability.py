"""Phase 8 Explainability and Risk Ranking Module.

Provides global feature importance extraction, customer-level evidence-based
risk explanation generation, churn probability scoring, risk categorization,
and ranked customer risk table generation for decision support.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.features.preprocessing import build_pipeline


def assign_risk_category(prob: float) -> str:
    """Assign operational risk category band based on estimated churn probability.

    Parameters
    ----------
    prob : float
        Estimated churn probability (0.0 to 1.0).

    Returns
    -------
    str
        Risk category band ('Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk').
    """
    if prob < 0.30:
        return "Low Risk"
    elif prob < 0.50:
        return "Medium Risk"
    elif prob < 0.70:
        return "High Risk"
    else:
        return "Very High Risk"


def generate_review_reasons(customer_row: pd.Series | Dict[str, Any]) -> List[str]:
    """Generate concise, evidence-based review reasons from observed customer attributes.

    Parameters
    ----------
    customer_row : pd.Series or Dict[str, Any]
        Raw customer record containing feature key-value pairs.

    Returns
    -------
    List[str]
        List of observational review reasons.
    """
    reasons = []

    # Contract
    contract = customer_row.get("Contract", "")
    if contract == "Month-to-month":
        reasons.append("Month-to-month contract")

    # Tenure
    try:
        tenure = float(customer_row.get("tenure", 0))
        if tenure <= 12:
            reasons.append(f"Short customer tenure ({int(tenure)} mos <= 12 mos)")
    except (ValueError, TypeError):
        pass

    # Internet Service
    internet = customer_row.get("InternetService", "")
    if internet == "Fiber optic":
        reasons.append("Fiber optic internet service")

    # Payment Method
    payment = customer_row.get("PaymentMethod", "")
    if payment == "Electronic check":
        reasons.append("Payment via Electronic check")

    # Online Security
    sec = customer_row.get("OnlineSecurity", "")
    if sec == "No":
        reasons.append("No OnlineSecurity service")

    # Tech Support
    tech = customer_row.get("TechSupport", "")
    if tech == "No":
        reasons.append("No TechSupport service")

    # Monthly Charges
    try:
        mc = float(customer_row.get("MonthlyCharges", 0))
        if mc >= 70.0:
            reasons.append(f"High monthly charges (${mc:.2f}/mo >= $70.00/mo)")
    except (ValueError, TypeError):
        pass

    # Paperless Billing
    paperless = customer_row.get("PaperlessBilling", "")
    if paperless == "Yes":
        reasons.append("Paperless billing active")

    # Online Backup
    backup = customer_row.get("OnlineBackup", "")
    if backup == "No":
        reasons.append("No OnlineBackup service")

    # Device Protection
    dp = customer_row.get("DeviceProtection", "")
    if dp == "No":
        reasons.append("No DeviceProtection service")

    return reasons


def explain_customer(
    customer_row: pd.Series | Dict[str, Any],
    churn_probability: float
) -> Dict[str, Any]:
    """Generate complete customer-level explanation structure.

    Parameters
    ----------
    customer_row : pd.Series or Dict[str, Any]
        Raw customer record.
    churn_probability : float
        Estimated churn probability.

    Returns
    -------
    Dict[str, Any]
        Structured explanation output.
    """
    cid = str(customer_row.get("customerID", customer_row.get("id", "UNKNOWN")))
    risk_cat = assign_risk_category(churn_probability)
    pred_churn = bool(churn_probability >= 0.50)
    reasons = generate_review_reasons(customer_row)

    return {
        "customerID": cid,
        "churn_probability": float(np.round(churn_probability, 4)),
        "risk_category": risk_cat,
        "predicted_churn": pred_churn,
        "review_reasons": reasons,
    }


def run_explainability_pipeline(
    data_path: Path = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv",
    output_dir: Path = PROJECT_ROOT / "reports" / "results",
    figures_dir: Path = PROJECT_ROOT / "reports" / "figures",
) -> Dict[str, Any]:
    """Execute full Phase 8 explainability, risk scoring, and customer ranking workflow.

    Parameters
    ----------
    data_path : Path
        Path to raw CSV dataset.
    output_dir : Path
        Directory for result artifacts.
    figures_dir : Path
        Directory for plot figures.

    Returns
    -------
    Dict[str, Any]
        Summary report dictionary.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data and fit pipeline on training set
    raw_df = load_raw_dataset(data_path)
    X, y = prepare_target(raw_df)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    rf_kwargs = {
        "n_estimators": 300,
        "max_depth": 8,
        "min_samples_leaf": 2,
        "min_samples_split": 2,
        "max_features": "sqrt",
        "random_state": 42,
        "n_jobs": -1,
    }
    clf = RandomForestClassifier(**rf_kwargs)
    pipeline = build_pipeline(feature_set="baseline", classifier=clf)
    pipeline.fit(X_train, y_train)

    # 2. Extract Global Feature Importance
    preprocessor = pipeline.named_steps["preprocessor"]
    fitted_clf = pipeline.named_steps["classifier"]

    raw_feat_names = list(preprocessor.get_feature_names_out())
    clean_feat_names = [
        f.replace("num__", "").replace("cat__", "") for f in raw_feat_names
    ]
    importances = fitted_clf.feature_importances_

    df_importance = pd.DataFrame({
        "feature": clean_feat_names,
        "importance": importances,
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    df_importance["rank"] = df_importance.index + 1
    total_imp = df_importance["importance"].sum()
    df_importance["importance_pct"] = (df_importance["importance"] / total_imp * 100).round(2)
    df_importance["importance"] = df_importance["importance"].round(4)

    # Reorder columns
    df_importance = df_importance[["rank", "feature", "importance", "importance_pct"]]
    df_importance.to_csv(output_dir / "phase8_global_feature_importance.csv", index=False)

    top_10_features = df_importance.head(10).to_dict(orient="records")
    json_importance_summary = {
        "total_transformed_features": len(df_importance),
        "top_10_features": top_10_features,
    }
    with open(output_dir / "phase8_global_feature_importance.json", "w", encoding="utf-8") as f:
        json.dump(json_importance_summary, f, indent=2)

    # Plot horizontal bar chart for top 15 features
    df_top15 = df_importance.head(15).iloc[::-1]
    plt.figure(figsize=(10, 6))
    plt.barh(df_top15["feature"], df_top15["importance_pct"], color="#1f77b4")
    plt.xlabel("Relative Importance (%)")
    plt.ylabel("Transformed Feature")
    plt.title("Phase 8 — Global Feature Importance (Optimized Random Forest)")
    plt.tight_layout()
    plt.savefig(figures_dir / "phase8_global_feature_importance.png", dpi=300)
    plt.close()

    # 3. Generate Churn Probabilities & Risk Scores for ALL customer records
    raw_df_copy = raw_df.copy()
    X_all = raw_df_copy.drop(columns=["customerID", "Churn"])
    all_probs = pipeline.predict_proba(X_all)[:, 1]

    raw_df_copy["churn_probability"] = np.round(all_probs, 4)
    raw_df_copy["predicted_churn"] = raw_df_copy["churn_probability"] >= 0.50
    raw_df_copy["risk_category"] = raw_df_copy["churn_probability"].apply(assign_risk_category)

    # Export customer risk scores CSV
    df_risk_scores = raw_df_copy[["customerID", "churn_probability", "predicted_churn", "risk_category"]].copy()
    df_risk_scores.to_csv(output_dir / "phase8_customer_risk_scores.csv", index=False)

    # 4. Generate Ranked High-Risk Customers Table
    df_ranked = raw_df_copy.sort_values("churn_probability", ascending=False).reset_index(drop=True)
    df_ranked["rank"] = df_ranked.index + 1

    # Extract review reasons for each customer
    all_reasons = []
    for _, row in df_ranked.iterrows():
        reasons = generate_review_reasons(row)
        all_reasons.append(reasons)

    # Add reason_1 .. reason_5 columns
    max_reasons = 5
    for i in range(max_reasons):
        col_name = f"reason_{i+1}"
        df_ranked[col_name] = [
            r_list[i] if len(r_list) > i else "" for r_list in all_reasons
        ]

    cols_ranked = ["rank", "customerID", "churn_probability", "predicted_churn", "risk_category"] + [
        f"reason_{i+1}" for i in range(max_reasons)
    ]
    df_ranked_export = df_ranked[cols_ranked].copy()
    df_ranked_export.to_csv(output_dir / "phase8_high_risk_customers.csv", index=False)

    # 5. Extract Sample High-Risk Customer Explanation
    top_customer_row = df_ranked.iloc[0]
    sample_explanation = explain_customer(top_customer_row, float(top_customer_row["churn_probability"]))

    # 6. Risk Category Counts & Summary
    category_counts = raw_df_copy["risk_category"].value_counts().to_dict()
    category_pcts = (raw_df_copy["risk_category"].value_counts(normalize=True) * 100).round(2).to_dict()

    summary_report = {
        "phase": "Phase 8",
        "model": "Optimized Random Forest",
        "total_customers_scored": len(raw_df_copy),
        "risk_category_counts": category_counts,
        "risk_category_percentages": category_pcts,
        "high_risk_or_very_high_risk_count": int(
            category_counts.get("High Risk", 0) + category_counts.get("Very High Risk", 0)
        ),
        "top_10_global_features": top_10_features,
        "sample_customer_explanation": sample_explanation,
        "artifacts_created": [
            "reports/results/phase8_global_feature_importance.csv",
            "reports/results/phase8_global_feature_importance.json",
            "reports/results/phase8_customer_risk_scores.csv",
            "reports/results/phase8_high_risk_customers.csv",
            "reports/results/phase8_explainability_summary.json",
            "reports/figures/phase8_global_feature_importance.png",
        ],
    }

    with open(output_dir / "phase8_explainability_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)

    return summary_report


if __name__ == "__main__":
    res = run_explainability_pipeline()
    print("PHASE 8 EXPLAINABILITY PIPELINE COMPLETE")
    print(f"Total customers scored: {res['total_customers_scored']}")
    print(f"Risk categories: {res['risk_category_counts']}")
    print(f"Top feature: {res['top_10_global_features'][0]['feature']} ({res['top_10_global_features'][0]['importance_pct']}%)")

"""Exploratory Data Analysis & Deep Leakage Audit Module.

Analyzes dataset structure, missingness, univariate & bivariate distributions,
outliers, collinearity, leakage audit, and feature engineering candidates.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
RESULTS_DIR = REPORTS_DIR / "results"


def load_and_clean_for_eda(data_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw dataset and create an analytical working copy with parsed TotalCharges."""
    if not data_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {data_path}")

    df = pd.read_csv(data_path)
    # Parse TotalCharges to numeric, coerce blank whitespace strings to NaN
    df["TotalCharges_numeric"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce")
    return df


def audit_structure_and_missingness(df: pd.DataFrame) -> dict:
    """Analyze dimensions, data types, and implicit vs explicit missing values."""
    explicit_missing = df.isnull().sum().to_dict()
    explicit_missing = {k: int(v) for k, v in explicit_missing.items() if v > 0}

    # TotalCharges whitespace analysis
    whitespace_mask = df["TotalCharges"].astype(str).str.strip() == ""
    whitespace_count = int(whitespace_mask.sum())
    whitespace_tenures = df.loc[whitespace_mask, "tenure"].tolist()

    return {
        "rows": len(df),
        "columns": len(df.columns) - 1,  # excluding our analytical column
        "explicit_missing_raw": explicit_missing,
        "totalcharges_whitespace_count": whitespace_count,
        "totalcharges_whitespace_tenures": whitespace_tenures,
        "totalcharges_all_tenure_zero": all(t == 0 for t in whitespace_tenures),
    }


def analyze_target_distribution(df: pd.DataFrame) -> dict:
    """Analyze churn class distribution and calculate imbalance ratio."""
    counts = df["Churn"].value_counts().to_dict()
    proportions = (df["Churn"].value_counts(normalize=True) * 100).round(2).to_dict()
    imbalance_ratio = round(counts["No"] / counts["Yes"], 2)

    return {
        "class_counts": counts,
        "class_proportions_pct": proportions,
        "imbalance_ratio": f"{imbalance_ratio}:1",
        "primary_metric_implication": (
            "Class imbalance (2.77:1) indicates accuracy alone is a misleading metric; "
            "ROC-AUC, Precision, Recall, F1, and PR-AUC must serve as primary evaluation criteria."
        ),
    }


def analyze_numerical_features(df: pd.DataFrame) -> dict:
    """Compute summary statistics, quartiles, IQR, and outlier counts for numerical columns."""
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges_numeric"]
    stats = {}

    for col in num_cols:
        series = df[col].dropna()
        q25 = float(series.quantile(0.25))
        q50 = float(series.quantile(0.50))
        q75 = float(series.quantile(0.75))
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr
        outliers = series[(series < lower_bound) | (series > upper_bound)]

        stats[col] = {
            "count": int(series.count()),
            "mean": round(float(series.mean()), 2),
            "std": round(float(series.std()), 2),
            "min": round(float(series.min()), 2),
            "q25": round(q25, 2),
            "median": round(q50, 2),
            "q75": round(q75, 2),
            "max": round(float(series.max()), 2),
            "iqr": round(iqr, 2),
            "lower_fence": round(lower_bound, 2),
            "upper_fence": round(upper_bound, 2),
            "outlier_count_iqr": int(len(outliers)),
            "outlier_pct_iqr": round(float(len(outliers) / len(series) * 100), 2),
        }

    return stats


def analyze_bivariate_categorical(df: pd.DataFrame) -> dict:
    """Calculate churn rate and count per category for all categorical features."""
    cat_cols = [
        "gender", "SeniorCitizen", "Partner", "Dependents",
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies",
        "Contract", "PaperlessBilling", "PaymentMethod"
    ]
    results = {}

    for col in cat_cols:
        grouped = df.groupby(col)["Churn"].agg(
            total_customers="count",
            churn_count=lambda s: (s == "Yes").sum(),
            churn_rate=lambda s: round((s == "Yes").mean() * 100, 2)
        ).reset_index()

        results[col] = grouped.to_dict(orient="records")

    return results


def analyze_bivariate_numerical(df: pd.DataFrame) -> dict:
    """Compare numerical distributions between churners and non-churners."""
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges_numeric"]
    comparisons = {}

    for col in num_cols:
        no_churn = df[df["Churn"] == "No"][col].dropna()
        yes_churn = df[df["Churn"] == "Yes"][col].dropna()

        comparisons[col] = {
            "No_mean": round(float(no_churn.mean()), 2),
            "No_median": round(float(no_churn.median()), 2),
            "No_std": round(float(no_churn.std()), 2),
            "Yes_mean": round(float(yes_churn.mean()), 2),
            "Yes_median": round(float(yes_churn.median()), 2),
            "Yes_std": round(float(yes_churn.std()), 2),
            "median_difference": round(float(yes_churn.median() - no_churn.median()), 2),
            "mean_difference": round(float(yes_churn.mean() - no_churn.mean()), 2),
        }

    # Tenure bins analysis
    bins = [0, 12, 24, 48, 72]
    labels = ["0-12 mos", "13-24 mos", "25-48 mos", "49-72 mos"]
    df_tenure_binned = df.copy()
    df_tenure_binned["tenure_group"] = pd.cut(df_tenure_binned["tenure"], bins=bins, labels=labels, include_lowest=True)
    tenure_churn = df_tenure_binned.groupby("tenure_group")["Churn"].agg(
        total="count",
        churn_count=lambda s: (s == "Yes").sum(),
        churn_rate_pct=lambda s: round((s == "Yes").mean() * 100, 2)
    ).reset_index().to_dict(orient="records")

    comparisons["tenure_cohorts"] = tenure_churn
    return comparisons


def analyze_collinearity(df: pd.DataFrame) -> dict:
    """Analyze correlations between numerical features."""
    sub = df[["tenure", "MonthlyCharges", "TotalCharges_numeric"]].dropna()
    pearson = sub.corr(method="pearson").round(3).to_dict()
    spearman = sub.corr(method="spearman").round(3).to_dict()

    return {
        "pearson_correlation": pearson,
        "spearman_correlation": spearman,
        "observation": (
            "TotalCharges exhibits strong linear collinearity with tenure (r=0.826) and moderate "
            "correlation with MonthlyCharges (r=0.651), as TotalCharges ~= tenure * MonthlyCharges. "
            "While tree ensembles naturally handle this interaction, regularization in linear models "
            "must be calibrated to prevent variance inflation."
        )
    }


def perform_deep_leakage_audit() -> list:
    """Document feature-by-feature leakage audit assessment."""
    audit_table = [
        {"feature": "customerID", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": True, "decision": "EXCLUDE", "rationale": "High-cardinality unique customer identifier. Would lead to arbitrary overfitting; carries no behavioral generalizability."},
        {"feature": "gender", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Demographic attribute known at sign-up. Safe."},
        {"feature": "SeniorCitizen", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Demographic indicator known at sign-up. Safe."},
        {"feature": "Partner", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Demographic account status. Safe."},
        {"feature": "Dependents", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Demographic account status. Safe."},
        {"feature": "tenure", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Elapsed duration in months as an active account prior to prediction point. Safe."},
        {"feature": "PhoneService", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active subscribed service catalog entry. Safe."},
        {"feature": "MultipleLines", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active subscribed service catalog entry. Safe."},
        {"feature": "InternetService", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active subscribed service catalog entry (DSL, Fiber, None). Safe."},
        {"feature": "OnlineSecurity", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active add-on service. Safe."},
        {"feature": "OnlineBackup", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active add-on service. Safe."},
        {"feature": "DeviceProtection", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active add-on service. Safe."},
        {"feature": "TechSupport", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active technical assistance entitlement. Safe."},
        {"feature": "StreamingTV", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active entertainment add-on. Safe."},
        {"feature": "StreamingMovies", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Active entertainment add-on. Safe."},
        {"feature": "Contract", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Billing contract commitment tier at observation time. Safe."},
        {"feature": "PaperlessBilling", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Billing delivery preference. Safe."},
        {"feature": "PaymentMethod", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Account payment method. Safe."},
        {"feature": "MonthlyCharges", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Current monthly recurring billing rate. Safe."},
        {"feature": "TotalCharges", "available_at_pred": True, "target_derived": False, "post_outcome": False, "suspicious_proxy": False, "decision": "KEEP", "rationale": "Cumulative charges present in snapshot. Candidate predictor; cross-sectional snapshot means temporal sequence cannot be verified as true prospective window. Blank for tenure=0 to be imputed as 0.0."},
        {"feature": "Churn", "available_at_pred": False, "target_derived": True, "post_outcome": True, "suspicious_proxy": True, "decision": "TARGET", "rationale": "Ground truth binary outcome variable. Separated as target y."}
    ]
    return audit_table


def evaluate_feature_engineering_candidates() -> list:
    """Audit potential engineered features against dataset availability, redundancy, and leakage risk."""
    candidates = [
        {
            "candidate_feature": "tenure_group",
            "formula": "Categorical binning: [0-12, 13-24, 25-48, 49-72 months]",
            "information_source": "tenure",
            "potential_redundancy": "High correlation with continuous tenure; tree ensembles split tenure directly, but binning may assist linear models in capturing non-linear hazard curves.",
            "leakage_risk": "None (deterministic function of snapshot tenure).",
            "business_meaning": "Segments customer lifecycle phase (early onboarding danger zone vs mature loyalty).",
            "phase_3_status": "APPROVED FOR EXPERIMENT",
            "keep_candidate": True,
            "status": "APPROVED FOR EXPERIMENT"
        },
        {
            "candidate_feature": "charges_ratio (monthly_to_total_ratio)",
            "formula": "MonthlyCharges / (TotalCharges + 1.0)",
            "information_source": "MonthlyCharges, TotalCharges",
            "potential_redundancy": "High redundancy with tenure. Since TotalCharges ≈ tenure * MonthlyCharges, charges_ratio ≈ 1 / (tenure + 1 / MonthlyCharges), making it an inverse surrogate of tenure. The +1.0 denominator smoothing offset prevents division by zero for tenure=0 but introduces scaling distortion for low spenders.",
            "leakage_risk": "Low direct leakage, but questionable validity given lack of temporal billing sequence in snapshot.",
            "business_meaning": "Unverified hypothesis: conjectured to capture recent billing increases or plan changes, but cannot be confirmed without longitudinal invoices.",
            "phase_3_status": "CANDIDATE — VALIDATE",
            "keep_candidate": True,
            "status": "CANDIDATE — VALIDATE"
        },
        {
            "candidate_feature": "total_services_subscribed",
            "formula": "Integer sum of 9 distinct active services (range 1-9): (PhoneService == 'Yes') + (MultipleLines == 'Yes') + (InternetService != 'No') + (OnlineSecurity == 'Yes') + (OnlineBackup == 'Yes') + (DeviceProtection == 'Yes') + (TechSupport == 'Yes') + (StreamingTV == 'Yes') + (StreamingMovies == 'Yes')",
            "information_source": "PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies",
            "potential_redundancy": "Direct composite of 9 catalog features that are already one-hot encoded individually in baseline.",
            "leakage_risk": "None (active service entitlements in snapshot).",
            "business_meaning": "Product breadth and ecosystem depth; hypothesis that higher subscription count increases switching barrier.",
            "phase_3_status": "APPROVED FOR EXPERIMENT",
            "keep_candidate": True,
            "status": "APPROVED FOR EXPERIMENT"
        },
        {
            "candidate_feature": "has_tech_support_or_security",
            "formula": "Binary flag: 1 if (TechSupport == 'Yes' or OnlineSecurity == 'Yes') else 0",
            "information_source": "TechSupport, OnlineSecurity",
            "potential_redundancy": "High redundancy with individual one-hot indicators for TechSupport and OnlineSecurity; may add no incremental signal beyond baseline.",
            "leakage_risk": "None.",
            "business_meaning": "Assistance and security umbrella; accounts with technical/security assistance exhibit lower observed churn rates in the snapshot.",
            "phase_3_status": "CANDIDATE — VALIDATE",
            "keep_candidate": True,
            "status": "CANDIDATE — VALIDATE"
        },
        {
            "candidate_feature": "auto_payment_indicator",
            "formula": "Binary flag: 1 if 'automatic' in PaymentMethod else 0 (aggregates Bank transfer and Credit card automatic payments)",
            "information_source": "PaymentMethod",
            "potential_redundancy": "Partially redundant with one-hot encoded PaymentMethod categories; tests whether collapsing automatic methods regularizes linear models.",
            "leakage_risk": "None.",
            "business_meaning": "Automated recurring billing vs manual payment action (Electronic check, Mailed check).",
            "phase_3_status": "APPROVED FOR EXPERIMENT",
            "keep_candidate": True,
            "status": "APPROVED FOR EXPERIMENT"
        },
        {
            "candidate_feature": "support_contact_frequency",
            "formula": "N/A (Timestamped ticket logs not present in Telco dataset)",
            "information_source": "N/A",
            "potential_redundancy": "N/A",
            "leakage_risk": "N/A",
            "business_meaning": "Customer service friction and complaint volume.",
            "phase_3_status": "EXCLUDE",
            "keep_candidate": False,
            "status": "EXCLUDE (Unavailable in dataset)"
        },
        {
            "candidate_feature": "usage_trend_delta",
            "formula": "N/A (Monthly gigabytes/minutes time-series not present)",
            "information_source": "N/A",
            "potential_redundancy": "N/A",
            "leakage_risk": "N/A",
            "business_meaning": "Decaying usage trend preceding cancellation.",
            "phase_3_status": "EXCLUDE",
            "keep_candidate": False,
            "status": "EXCLUDE (Unavailable in dataset)"
        },
        {
            "candidate_feature": "recent_billing_change",
            "formula": "N/A (Previous billing period charge amounts not present)",
            "information_source": "N/A",
            "potential_redundancy": "N/A",
            "leakage_risk": "N/A",
            "business_meaning": "Bill shock from pricing increases.",
            "phase_3_status": "EXCLUDE",
            "keep_candidate": False,
            "status": "EXCLUDE (Unavailable in dataset)"
        }
    ]
    return candidates


def generate_eda_figures(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> list:
    """Generate and save analytical figures."""
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_plots = []

    # 1. Target Class Distribution
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["Churn"].value_counts()
    colors = ["#2b5c8f", "#d95f02"]
    bars = ax.bar(counts.index, counts.values, color=colors, width=0.5, edgecolor="black")
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f"{yval:,} ({yval/len(df)*100:.1f}%)", ha="center", va="bottom", fontsize=10, weight="bold")
    ax.set_title("Customer Churn Class Distribution (Target: Churn)", fontsize=12, pad=12)
    ax.set_ylabel("Customer Count", fontsize=10)
    ax.set_ylim(0, 6000)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    p1 = output_dir / "01_target_distribution.png"
    plt.savefig(p1, dpi=150)
    plt.close()
    generated_plots.append(str(p1))

    # 2. Tenure Distribution by Churn
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=df, x="tenure", hue="Churn", multiple="layer", bins=36, palette={"No": "#2b5c8f", "Yes": "#d95f02"}, alpha=0.6, ax=ax)
    ax.set_title("Tenure (Months) Distribution by Churn Status", fontsize=12)
    ax.set_xlabel("Tenure (Months)", fontsize=10)
    ax.set_ylabel("Customer Count", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    p2 = output_dir / "02_tenure_vs_churn.png"
    plt.savefig(p2, dpi=150)
    plt.close()
    generated_plots.append(str(p2))

    # 3. MonthlyCharges Distribution by Churn
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.kdeplot(data=df[df["Churn"] == "No"]["MonthlyCharges"], label="Non-Churners (No)", color="#2b5c8f", fill=True, alpha=0.3, ax=ax)
    sns.kdeplot(data=df[df["Churn"] == "Yes"]["MonthlyCharges"], label="Churners (Yes)", color="#d95f02", fill=True, alpha=0.3, ax=ax)
    ax.set_title("MonthlyCharges Density Estimation by Churn Status", fontsize=12)
    ax.set_xlabel("Monthly Charges ($ USD)", fontsize=10)
    ax.set_ylabel("Density", fontsize=10)
    ax.legend(title="Churn Status")
    ax.grid(linestyle="--", alpha=0.5)
    plt.tight_layout()
    p3 = output_dir / "03_monthly_charges_kde_churn.png"
    plt.savefig(p3, dpi=150)
    plt.close()
    generated_plots.append(str(p3))

    # 4. Churn Rate by Contract Type
    fig, ax = plt.subplots(figsize=(7, 4))
    contract_churn = df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reindex(["Month-to-month", "One year", "Two year"])
    bars = ax.bar(contract_churn.index, contract_churn.values, color=["#d95f02", "#4575b4", "#313695"], width=0.5, edgecolor="black")
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.0, f"{yval:.1f}%", ha="center", va="bottom", fontsize=10, weight="bold")
    ax.set_title("Observed Churn Rate by Contract Duration", fontsize=12)
    ax.set_ylabel("Observed Churn Rate (%)", fontsize=10)
    ax.set_ylim(0, 55)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    p4 = output_dir / "04_churn_rate_by_contract.png"
    plt.savefig(p4, dpi=150)
    plt.close()
    generated_plots.append(str(p4))

    # 5. Churn Rate by Internet Service & Payment Method
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
    inet_churn = df.groupby("InternetService")["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reindex(["DSL", "Fiber optic", "No"])
    b1 = ax1.bar(inet_churn.index, inet_churn.values, color=["#4575b4", "#d95f02", "#74add1"], width=0.5, edgecolor="black")
    for b in b1:
        yval = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2.0, yval + 1.0, f"{yval:.1f}%", ha="center", va="bottom", fontsize=9, weight="bold")
    ax1.set_title("Churn Rate by Internet Service", fontsize=11)
    ax1.set_ylabel("Churn Rate (%)", fontsize=9)
    ax1.set_ylim(0, 50)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    pm_churn = df.groupby("PaymentMethod")["Churn"].apply(lambda s: (s == "Yes").mean() * 100).sort_values(ascending=False)
    b2 = ax2.barh(pm_churn.index, pm_churn.values, color=["#d95f02", "#74add1", "#4575b4", "#313695"], edgecolor="black")
    for b in b2:
        xval = b.get_width()
        ax2.text(xval + 0.5, b.get_y() + b.get_height()/2.0, f"{xval:.1f}%", ha="left", va="center", fontsize=9, weight="bold")
    ax2.set_title("Churn Rate by Payment Method", fontsize=11)
    ax2.set_xlabel("Churn Rate (%)", fontsize=9)
    ax2.set_xlim(0, 55)
    ax2.grid(axis="x", linestyle="--", alpha=0.5)

    plt.tight_layout()
    p5 = output_dir / "05_churn_by_internet_and_payment.png"
    plt.savefig(p5, dpi=150)
    plt.close()
    generated_plots.append(str(p5))

    # 6. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(6, 5))
    num_corr = df[["tenure", "MonthlyCharges", "TotalCharges_numeric"]].dropna().corr()
    sns.heatmap(num_corr, annot=True, fmt=".3f", cmap="Blues", cbar=True, ax=ax, square=True)
    ax.set_title("Numerical Features Pearson Correlation Matrix", fontsize=11, pad=10)
    plt.tight_layout()
    p6 = output_dir / "06_numerical_correlation_matrix.png"
    plt.savefig(p6, dpi=150)
    plt.close()
    generated_plots.append(str(p6))

    return generated_plots


def run_full_eda_pipeline() -> dict:
    """Execute complete EDA audit and export structured JSON report & figures."""
    df = load_and_clean_for_eda()

    structure_report = audit_structure_and_missingness(df)
    target_report = analyze_target_distribution(df)
    num_stats = analyze_numerical_features(df)
    biv_cat = analyze_bivariate_categorical(df)
    biv_num = analyze_bivariate_numerical(df)
    collinearity = analyze_collinearity(df)
    leakage_audit = perform_deep_leakage_audit()
    fe_candidates = evaluate_feature_engineering_candidates()
    figures = generate_eda_figures(df)

    complete_report = {
        "dataset_structure": structure_report,
        "target_distribution": target_report,
        "numerical_univariate_stats": num_stats,
        "numerical_bivariate_vs_churn": biv_num,
        "categorical_bivariate_vs_churn": biv_cat,
        "collinearity_analysis": collinearity,
        "leakage_audit": leakage_audit,
        "feature_engineering_candidates": fe_candidates,
        "temporal_limitations": {
            "dataset_type": "Cross-sectional customer snapshot benchmark",
            "prospective_sequence": "NOT PRESENT (Dataset does not contain timestamped events T -> observation window -> churn event)",
            "prediction_time_assumption": "Cross-sectional snapshot interpretation. Not a true prospective or time-to-future churn system.",
            "TotalCharges_interpretation": "Cumulative historical spend as reported in customer snapshot. Retained as candidate predictor but does not constitute proof of future-only prediction window; temporal leakage cannot be ruled out purely from column naming."
        },
        "feature_engineering_ablation_protocol": {
            "experiment_a": "Baseline trained on verified original cleaned features (19 predictors)",
            "experiment_b": "Original features + candidate engineered feature(s)",
            "retention_rule": "Retain engineered features only if empirical ablation demonstrates meaningful, defensible, and statistically stable lift over Experiment A without artificial complexity inflation."
        },
        "generated_figures": figures,
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RESULTS_DIR / "eda_audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(complete_report, f, indent=2)

    return complete_report


if __name__ == "__main__":
    print("=" * 65)
    print("CUSTOMER CHURN SYSTEM — RUNNING PHASE 2 EDA PIPELINE")
    print("=" * 65)
    report = run_full_eda_pipeline()
    print(f"Dataset Structure: {report['dataset_structure']['rows']} rows, {report['dataset_structure']['columns']} features")
    print(f"Target Churn: {report['target_distribution']['class_counts']} (Ratio: {report['target_distribution']['imbalance_ratio']})")
    print(f"TotalCharges Whitespace Rows: {report['dataset_structure']['totalcharges_whitespace_count']}")
    print(f"Generated Figures: {len(report['generated_figures'])}")
    print(f"Leakage Audit Evaluated: {len(report['leakage_audit'])} candidate features")
    print("Saved report to reports/results/eda_audit_report.json")
    print("=" * 65)

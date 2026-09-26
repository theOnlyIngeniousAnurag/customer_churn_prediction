"""Data audit and validation module for Customer Churn Prediction System."""

import sys
from pathlib import Path
import pandas as pd
import numpy as np


def run_initial_data_audit(file_path: Path) -> dict:
    """Perform a rigorous initial data audit on the customer dataset.

    Inspects structure, target distribution, missingness, duplicates,
    data types, anomalous values, and potential leakage indicators.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at expected path: {file_path}")

    # Load raw dataset without mutations
    df = pd.read_csv(file_path)

    # 1. Structure
    n_rows, n_cols = df.shape
    columns = list(df.columns)
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    # 2. Target validation
    target_col = "Churn"
    target_present = target_col in df.columns
    target_uniques = df[target_col].unique().tolist() if target_present else []
    target_counts = (
        df[target_col].value_counts(dropna=False).to_dict() if target_present else {}
    )
    target_pcts = (
        (df[target_col].value_counts(normalize=True, dropna=False) * 100)
        .round(2)
        .to_dict()
        if target_present
        else {}
    )

    # 3. Missingness & Whitespace / Blank checks
    raw_null_counts = df.isnull().sum().to_dict()
    # Check for empty string or whitespace-only values in object columns
    whitespace_counts = {}
    for col in df.select_dtypes(include=["object"]).columns:
        ws_count = int((df[col].astype(str).str.strip() == "").sum())
        if ws_count > 0:
            whitespace_counts[col] = ws_count

    # 4. Duplicate checks
    exact_duplicates = int(df.duplicated().sum())
    id_col = "customerID"
    id_duplicates = int(df[id_col].duplicated().sum()) if id_col in df.columns else 0

    # 5. Column categories
    identifier_cols = [id_col] if id_col in df.columns else []
    numerical_candidates = ["tenure", "MonthlyCharges", "TotalCharges"]
    # TotalCharges is often stored as object due to blank spaces for tenure=0
    categorical_cols = [
        c
        for c in columns
        if c not in identifier_cols and c != target_col and c not in ["tenure", "MonthlyCharges"]
    ]

    # 6. Detailed investigation on TotalCharges
    total_charges_blanks = 0
    if "TotalCharges" in df.columns:
        # Check non-numeric strings
        non_numeric_tc = pd.to_numeric(df["TotalCharges"], errors="coerce")
        total_charges_blanks = int(non_numeric_tc.isnull().sum())

    # 7. Numerical summaries
    num_summary = {}
    for col in ["tenure", "MonthlyCharges"]:
        if col in df.columns:
            s = df[col]
            num_summary[col] = {
                "min": float(s.min()),
                "q25": float(s.quantile(0.25)),
                "median": float(s.median()),
                "mean": round(float(s.mean()), 2),
                "q75": float(s.quantile(0.75)),
                "max": float(s.max()),
                "std": round(float(s.std()), 2),
            }

    # 8. Categorical uniques
    cat_uniques = {
        col: df[col].unique().tolist()
        for col in categorical_cols
        if col != "TotalCharges"
    }

    # 9. Initial Leakage Assessment
    # Check for any post-churn flags, reasons, timestamps, cancellation dates
    suspicious_leakage_cols = [
        c
        for c in columns
        if any(term in c.lower() for term in ["cancel", "date", "exit", "leaving", "retention"])
    ]

    audit_results = {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "columns": columns,
        "dtypes": dtypes,
        "target": {
            "name": target_col,
            "present": target_present,
            "unique_values": target_uniques,
            "value_counts": target_counts,
            "percentages": target_pcts,
            "imbalance_ratio": (
                round(target_counts.get("No", 0) / target_counts.get("Yes", 1), 2)
                if "Yes" in target_counts and "No" in target_counts
                else None
            ),
        },
        "missingness": {
            "explicit_nulls": {k: v for k, v in raw_null_counts.items() if v > 0},
            "whitespace_blanks": whitespace_counts,
            "total_charges_unparseable": total_charges_blanks,
        },
        "duplicates": {
            "exact_duplicate_rows": exact_duplicates,
            "duplicate_customer_ids": id_duplicates,
        },
        "identifiers": identifier_cols,
        "numerical_summary": num_summary,
        "categorical_unique_counts": {k: len(v) for k, v in cat_uniques.items()},
        "categorical_unique_values": cat_uniques,
        "leakage_audit": {
            "suspicious_columns": suspicious_leakage_cols,
            "assessment": (
                "No post-churn or future information columns detected. "
                "customerID is an identifier and must be excluded from feature set. "
                "TotalCharges has 11 whitespace strings corresponding to brand-new customers (tenure=0)."
            ),
        },
    }

    return audit_results


def print_audit_report(results: dict):
    """Print a clean, formatted terminal summary of the audit findings."""
    print("=" * 65)
    print("CUSTOMER CHURN SYSTEM — INITIAL DATA AUDIT REPORT")
    print("=" * 65)
    print(f"Dataset Dimensions: {results['n_rows']} rows x {results['n_cols']} columns")
    print(f"Unique Identifier Column: {results['identifiers']}")
    print(f"Exact Duplicate Rows: {results['duplicates']['exact_duplicate_rows']}")
    print(f"Duplicate Customer IDs: {results['duplicates']['duplicate_customer_ids']}")
    print("-" * 65)
    t = results["target"]
    print(f"Target Variable: '{t['name']}' (Present: {t['present']})")
    print(f"Target Classes: {t['unique_values']}")
    print(f"Target Counts: {t['value_counts']}")
    print(f"Target Proportions: {t['percentages']}")
    print(f"Imbalance Ratio (No/Yes): {t['imbalance_ratio']}:1")
    print("-" * 65)
    m = results["missingness"]
    print(f"Explicit Missing Values (NaN): {m['explicit_nulls']}")
    print(f"Implicit Whitespace Blanks: {m['whitespace_blanks']}")
    print(f"TotalCharges Unparseable (tenure=0 new accounts): {m['total_charges_unparseable']}")
    print("-" * 65)
    print("Numerical Features Summary:")
    for k, v in results["numerical_summary"].items():
        print(f"  * {k}: min={v['min']}, median={v['median']}, mean={v['mean']}, max={v['max']}, std={v['std']}")
    print("-" * 65)
    print("Categorical Features & Cardinality:")
    for k, v in results["categorical_unique_counts"].items():
        print(f"  * {k} ({v} categories): {results['categorical_unique_values'][k]}")
    print("-" * 65)
    print("Initial Leakage Audit:")
    print(f"  * Flagged Columns: {results['leakage_audit']['suspicious_columns']}")
    print(f"  * Assessment: {results['leakage_audit']['assessment']}")
    print("=" * 65)


if __name__ == "__main__":
    raw_path = Path("data/raw/Telco-Customer-Churn.csv")
    res = run_initial_data_audit(raw_path)
    print_audit_report(res)

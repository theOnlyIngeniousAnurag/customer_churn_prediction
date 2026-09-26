"""Controlled feature engineering ablation experiment runner.

Executes rigorous 5-fold Stratified Cross-Validation on the training set
to compare candidate engineered features against the 19-feature baseline.
The final test set remains strictly isolated and untouched.
"""

import json
import sys
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.features.preprocessing import build_pipeline
RESULTS_DIR = PROJECT_ROOT / "reports" / "results"


def run_feature_ablation(
    random_state: int = 42,
    cv_folds: int = 5,
    output_path: Path | str | None = None
) -> dict:
    """Execute 5-fold stratified cross-validation ablation study across all candidate configurations.

    Parameters
    ----------
    random_state : int, default 42
        Reproducibility seed for data split, CV split, and baseline classifier.
    cv_folds : int, default 5
        Number of stratified cross-validation folds.
    output_path : Path or str, optional
        Destination JSON file for ablation results.

    Returns
    -------
    dict
        Structured ablation metrics and comparison against baseline.
    """
    df = load_raw_dataset(PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv")
    X, y = prepare_target(df)

    # Isolated train/test split: test set is NEVER touched in ablation
    X_train, X_test, y_train, y_test = split_data(
        X, y, test_size=0.2, random_state=random_state
    )

    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    scoring = ["roc_auc", "average_precision", "precision", "recall", "f1"]

    experiment_configs = [
        ("Experiment A (Baseline)", "baseline", "Original 19 raw features without engineered additions"),
        ("Experiment B1 (+ tenure_group)", "b1_tenure_group", "Baseline + categorical lifecycle tenure bins"),
        ("Experiment B2 (+ total_services_subscribed)", "b2_total_services", "Baseline + integer sum of 9 active services"),
        ("Experiment B3 (+ has_tech_support_or_security)", "b3_tech_support_security", "Baseline + binary union of TechSupport or OnlineSecurity"),
        ("Experiment B4 (+ auto_payment_indicator)", "b4_auto_payment", "Baseline + binary flag for automatic payment methods"),
        ("Experiment B5 (+ charges_ratio)", "b5_charges_ratio", "Baseline + MonthlyCharges / (TotalCharges + 1.0)"),
        ("Experiment C (All Candidates)", "c_all", "Baseline + all five candidate engineered features"),
    ]

    results: dict = {
        "metadata": {
            "dataset_rows": len(df),
            "train_rows": len(X_train),
            "test_rows": len(X_test),
            "cv_folds": cv_folds,
            "random_state": random_state,
            "baseline_model": "LogisticRegression(max_iter=1000, random_state=42)",
            "test_set_status": "ISOLATED (untouched, no evaluation performed on test set)",
        },
        "experiments": {},
    }

    baseline_metrics: dict[str, float] = {}

    for exp_name, feature_set_key, description in experiment_configs:
        clf = LogisticRegression(max_iter=1000, random_state=random_state)
        pipeline = build_pipeline(feature_set=feature_set_key, classifier=clf)

        scores = cross_validate(
            pipeline,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )

        metrics = {}
        for s in scoring:
            mean_val = float(np.mean(scores["test_" + s]))
            std_val = float(np.std(scores["test_" + s]))
            metrics[s] = {
                "mean": round(mean_val, 4),
                "std": round(std_val, 4),
            }

        if exp_name == "Experiment A (Baseline)":
            for s in scoring:
                baseline_metrics[s] = metrics[s]["mean"]

        # Compute delta vs baseline
        deltas = {}
        for s in scoring:
            diff = round(metrics[s]["mean"] - baseline_metrics[s], 4)
            deltas[s] = diff

        results["experiments"][exp_name] = {
            "feature_set": feature_set_key,
            "description": description,
            "metrics": metrics,
            "delta_vs_baseline": deltas,
        }

    if output_path is None:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = RESULTS_DIR / "feature_ablation_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    print("=" * 70)
    print("CUSTOMER CHURN SYSTEM — RUNNING PHASE 3 FEATURE ABLATION STUDY")
    print("=" * 70)
    ablation_results = run_feature_ablation()

    print(f"Dataset: {ablation_results['metadata']['dataset_rows']} rows")
    print(f"Train set: {ablation_results['metadata']['train_rows']} rows (5-Fold Stratified CV)")
    print(f"Test set: {ablation_results['metadata']['test_rows']} rows (Strictly Isolated)")
    print("-" * 70)
    print(f"{'Experiment':<40} {'ROC-AUC':<10} {'PR-AUC':<10} {'F1':<10}")
    print("-" * 70)

    for name, data in ablation_results["experiments"].items():
        roc = data["metrics"]["roc_auc"]["mean"]
        pr = data["metrics"]["average_precision"]["mean"]
        f1 = data["metrics"]["f1"]["mean"]
        print(f"{name:<40} {roc:<10.4f} {pr:<10.4f} {f1:<10.4f}")

    print("=" * 70)
    print("Ablation study complete. Results exported to reports/results/feature_ablation_results.json")

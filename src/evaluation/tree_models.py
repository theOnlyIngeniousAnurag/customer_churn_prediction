"""Evaluation and benchmarking module for Phase 5 Tree-Based Models.

This module executes:
- 5-fold Stratified Cross-Validation on training data for Decision Tree and Random Forest
- Feature configurations: Experiment A (Original 19 features) and Experiment B1 (+ tenure_group)
- Extraction and alignment of native feature importances to preprocessed feature names
- Generation of out-of-fold confusion matrices and lightweight error diagnostics
- Export of machine-readable benchmark JSON and feature importance CSV artifacts
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_validate

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.models.baseline import build_baseline_pipeline
from src.models.tree_models import build_tree_pipeline


def evaluate_model_cv(
    pipeline: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    cv: StratifiedKFold
) -> Dict[str, Dict[str, float]]:
    """Evaluate pipeline using 5-fold Stratified CV across 5 standard metrics."""
    scoring = ["roc_auc", "average_precision", "precision", "recall", "f1"]
    cv_results = cross_validate(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        return_train_score=False
    )

    metrics_summary = {}
    for metric in scoring:
        scores = cv_results[f"test_{metric}"]
        metrics_summary[metric] = {
            "mean": float(np.round(np.mean(scores), 4)),
            "std": float(np.round(np.std(scores), 4)),
            "fold_scores": [float(np.round(s, 4)) for s in scores],
        }
    return metrics_summary


def compute_oof_diagnostics(
    pipeline: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    cv: StratifiedKFold
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Compute out-of-fold predictions, confusion matrix, and error analysis."""
    y_oof_proba = cross_val_predict(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        method="predict_proba",
        n_jobs=-1
    )[:, 1]
    y_oof_pred = (y_oof_proba >= 0.50).astype(int)

    cm = confusion_matrix(y_train, y_oof_pred)
    tn, fp, fn, tp = cm.ravel()
    total = len(y_train)

    cm_dict = {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "total_observations": int(total),
        "accuracy_default_threshold": float(np.round((tn + tp) / total, 4)),
        "false_positive_rate": float(np.round(fp / (tn + fp), 4)),
        "false_negative_rate": float(np.round(fn / (tp + fn), 4)),
        "precision_oof": float(np.round(precision_score(y_train, y_oof_pred), 4)),
        "recall_oof": float(np.round(recall_score(y_train, y_oof_pred), 4)),
        "f1_oof": float(np.round(f1_score(y_train, y_oof_pred), 4)),
        "roc_auc_oof": float(np.round(roc_auc_score(y_train, y_oof_proba), 4)),
        "average_precision_oof": float(np.round(average_precision_score(y_train, y_oof_proba), 4)),
    }

    # Error analysis breakdown
    df_eval = X_train.copy()
    df_eval["actual"] = y_train.values
    df_eval["pred"] = y_oof_pred
    df_eval["prob"] = y_oof_proba

    fp_df = df_eval[(df_eval["actual"] == 0) & (df_eval["pred"] == 1)]
    fn_df = df_eval[(df_eval["actual"] == 1) & (df_eval["pred"] == 0)]
    tp_df = df_eval[(df_eval["actual"] == 1) & (df_eval["pred"] == 1)]
    tn_df = df_eval[(df_eval["actual"] == 0) & (df_eval["pred"] == 0)]

    error_analysis = {
        "false_positives": {
            "count": int(len(fp_df)),
            "percentage_of_retained": float(np.round(100.0 * len(fp_df) / max(len(fp_df) + len(tn_df), 1), 2)),
            "median_tenure_months": float(fp_df["tenure"].median()) if len(fp_df) > 0 else 0.0,
            "median_monthly_charges": float(fp_df["MonthlyCharges"].median()) if len(fp_df) > 0 else 0.0,
            "month_to_month_contract_pct": float(np.round(100.0 * (fp_df["Contract"] == "Month-to-month").mean(), 2)) if len(fp_df) > 0 else 0.0,
            "fiber_optic_pct": float(np.round(100.0 * (fp_df["InternetService"] == "Fiber optic").mean(), 2)) if len(fp_df) > 0 else 0.0,
            "electronic_check_pct": float(np.round(100.0 * (fp_df["PaymentMethod"] == "Electronic check").mean(), 2)) if len(fp_df) > 0 else 0.0,
        },
        "false_negatives": {
            "count": int(len(fn_df)),
            "percentage_of_churners": float(np.round(100.0 * len(fn_df) / max(len(fn_df) + len(tp_df), 1), 2)),
            "median_tenure_months": float(fn_df["tenure"].median()) if len(fn_df) > 0 else 0.0,
            "median_monthly_charges": float(fn_df["MonthlyCharges"].median()) if len(fn_df) > 0 else 0.0,
            "month_to_month_contract_pct": float(np.round(100.0 * (fn_df["Contract"] == "Month-to-month").mean(), 2)) if len(fn_df) > 0 else 0.0,
            "fiber_optic_pct": float(np.round(100.0 * (fn_df["InternetService"] == "Fiber optic").mean(), 2)) if len(fn_df) > 0 else 0.0,
            "electronic_check_pct": float(np.round(100.0 * (fn_df["PaymentMethod"] == "Electronic check").mean(), 2)) if len(fn_df) > 0 else 0.0,
        }
    }

    return cm_dict, error_analysis


def run_tree_benchmarking(
    data_path: Path = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv",
    output_dir: Path = PROJECT_ROOT / "reports" / "results",
) -> Dict[str, Any]:
    """Run full Phase 5 benchmarking for Decision Tree and Random Forest."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load and split data with strict test isolation
    raw_df = load_raw_dataset(data_path)
    X, y = prepare_target(raw_df)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 2. Build model pipelines for evaluation
    pipelines = {
        "Logistic Regression (Baseline)": build_baseline_pipeline(feature_set="baseline", random_state=42),
        "Logistic Regression (+ tenure_group)": build_baseline_pipeline(feature_set="b1_tenure_group", random_state=42),
        "Decision Tree (Original)": build_tree_pipeline(model_type="decision_tree", feature_set="baseline", random_state=42),
        "Decision Tree (+ tenure_group)": build_tree_pipeline(model_type="decision_tree", feature_set="b1_tenure_group", random_state=42),
        "Random Forest (Original)": build_tree_pipeline(model_type="random_forest", feature_set="baseline", random_state=42, n_estimators=300, n_jobs=-1),
        "Random Forest (+ tenure_group)": build_tree_pipeline(model_type="random_forest", feature_set="b1_tenure_group", random_state=42, n_estimators=300, n_jobs=-1),
    }

    benchmark_results = {}
    for name, pipe in pipelines.items():
        metrics = evaluate_model_cv(pipe, X_train, y_train, cv)
        benchmark_results[name] = metrics

    # 3. Fit on full training set to extract diagnostics and feature importances
    # Decision Tree
    dt_pipe = build_tree_pipeline(model_type="decision_tree", feature_set="baseline", random_state=42)
    dt_pipe.fit(X_train, y_train)
    dt_clf = dt_pipe.named_steps["classifier"]
    dt_feat_names = list(dt_pipe.named_steps["preprocessor"].get_feature_names_out())
    dt_importances = dt_clf.feature_importances_

    dt_df_imp = pd.DataFrame({
        "feature": dt_feat_names,
        "importance": dt_importances,
    }).sort_values("importance", ascending=False)
    dt_df_imp.to_csv(output_dir / "decision_tree_feature_importance.csv", index=False)

    dt_diagnostics = {
        "tree_depth": int(dt_clf.get_depth()),
        "n_leaves": int(dt_clf.get_n_leaves()),
        "node_count": int(dt_clf.tree_.node_count),
        "train_accuracy": float(np.round(dt_pipe.score(X_train, y_train), 4)),
    }

    # Random Forest
    rf_pipe = build_tree_pipeline(model_type="random_forest", feature_set="baseline", random_state=42, n_estimators=300, n_jobs=-1)
    rf_pipe.fit(X_train, y_train)
    rf_clf = rf_pipe.named_steps["classifier"]
    rf_feat_names = list(rf_pipe.named_steps["preprocessor"].get_feature_names_out())
    rf_importances = rf_clf.feature_importances_

    rf_df_imp = pd.DataFrame({
        "feature": rf_feat_names,
        "importance": rf_importances,
    }).sort_values("importance", ascending=False)
    rf_df_imp.to_csv(output_dir / "random_forest_feature_importance.csv", index=False)

    rf_diagnostics = {
        "n_estimators": int(len(rf_clf.estimators_)),
        "max_features": str(rf_clf.max_features),
        "train_accuracy": float(np.round(rf_pipe.score(X_train, y_train), 4)),
    }

    # 4. Out-of-fold confusion matrix and error analysis
    dt_cm, dt_errors = compute_oof_diagnostics(dt_pipe, X_train, y_train, cv)
    rf_cm, rf_errors = compute_oof_diagnostics(rf_pipe, X_train, y_train, cv)

    # 5. Compile final JSON report
    report = {
        "metadata": {
            "experiment_phase": "Phase 5 Tree-Based Model Benchmarking",
            "dataset_rows_total": len(raw_df),
            "training_sample_count": len(X_train),
            "test_sample_count": len(X_test),
            "test_set_used": False,
            "test_set_fitted": False,
            "test_set_predicted": False,
            "cv_configuration": {
                "strategy": "StratifiedKFold",
                "n_splits": 5,
                "shuffle": True,
                "random_state": 42,
            },
        },
        "model_configurations": {
            "DecisionTreeClassifier": {
                "random_state": 42,
                "criterion": "gini",
                "splitter": "best",
                "max_depth": None,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
                "tuning_performed": False,
            },
            "RandomForestClassifier": {
                "n_estimators": 300,
                "random_state": 42,
                "n_jobs": -1,
                "criterion": "gini",
                "max_depth": None,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
                "class_weight": None,
                "tuning_performed": False,
            }
        },
        "benchmark_comparison": benchmark_results,
        "decision_tree_diagnostics": dt_diagnostics,
        "random_forest_diagnostics": rf_diagnostics,
        "decision_tree_oof_confusion_matrix": dt_cm,
        "decision_tree_oof_error_analysis": dt_errors,
        "random_forest_oof_confusion_matrix": rf_cm,
        "random_forest_oof_error_analysis": rf_errors,
    }

    with open(output_dir / "tree_model_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report


if __name__ == "__main__":
    results = run_tree_benchmarking()
    print("=" * 70)
    print("PHASE 5 TREE-BASED BENCHMARKING COMPLETE")
    print("=" * 70)
    for model_name, metrics in results["benchmark_comparison"].items():
        print(f"\n{model_name}:")
        for m, vals in metrics.items():
            print(f"  {m:20s}: {vals['mean']:.4f} +/- {vals['std']:.4f}")

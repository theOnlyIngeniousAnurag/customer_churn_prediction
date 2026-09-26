"""Phase 10 Quality Assurance & Comprehensive Validation Test Suite.

Validates:
- P10-01 Data Pipeline
- P10-02 Preprocessing Architecture & Leakage Audit
- P10-03 Model Loading & Hyperparameter Preservation
- P10-04 End-to-End Inference Sequence & Categorization
- P10-05 Edge Case Resilience (Missing values, Unseen categories, Numerical extremes)
- P10-06 Clean-Environment & Dependency Manifest Integrity
- P10-07 Reproducibility & Determinism
- P10-08 Artifact & UI Data Consistency
"""

import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.features.preprocessing import TotalChargesCleaner, build_pipeline
from src.evaluation.explainability import assign_risk_category, explain_customer


class TestPhase10QualityAssurance(unittest.TestCase):
    """Comprehensive QA test suite for Project 1 Machine Learning pipeline and artifacts."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures and load authoritative project artifacts."""
        cls.raw_csv_path = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
        cls.phase7_results_path = PROJECT_ROOT / "reports" / "results" / "phase7_final_test_results.json"
        cls.phase7_cm_path = PROJECT_ROOT / "reports" / "results" / "phase7_confusion_matrix.json"
        cls.phase8_summary_path = PROJECT_ROOT / "reports" / "results" / "phase8_explainability_summary.json"
        cls.phase8_ranked_csv_path = PROJECT_ROOT / "reports" / "results" / "phase8_high_risk_customers.csv"

        cls.raw_df = load_raw_dataset(cls.raw_csv_path)
        cls.X, cls.y = prepare_target(cls.raw_df)
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = split_data(cls.X, cls.y, test_size=0.2, random_state=42)

        with open(cls.phase7_results_path, "r", encoding="utf-8") as f:
            cls.p7_results = json.load(f)

        with open(cls.phase8_summary_path, "r", encoding="utf-8") as f:
            cls.p8_summary = json.load(f)

        cls.ranked_df = pd.read_csv(cls.phase8_ranked_csv_path)

    def test_p10_01_data_pipeline_validation(self):
        """P10-01: Validate raw dataset structure, integrity, and target mapping."""
        self.assertTrue(self.raw_csv_path.exists())
        self.assertEqual(len(self.raw_df), 7043)
        self.assertEqual(len(self.raw_df.columns), 21)

        # Identifier integrity
        self.assertIn("customerID", self.raw_df.columns)
        self.assertEqual(self.raw_df["customerID"].nunique(), 7043)

        # Target integrity
        self.assertIn("Churn", self.raw_df.columns)
        self.assertEqual(set(self.raw_df["Churn"].unique()), {"No", "Yes"})
        self.assertEqual(set(self.y.unique()), {0, 1})
        self.assertEqual(len(self.X), 7043)

        # Whitespace handling in TotalCharges
        raw_whitespace_count = (self.raw_df["TotalCharges"].astype(str).str.strip() == "").sum()
        self.assertEqual(raw_whitespace_count, 11)

        cleaner = TotalChargesCleaner()
        cleaner.fit(self.X_train)
        X_cleaned = cleaner.transform(self.X_test)
        self.assertFalse(X_cleaned["TotalCharges"].isna().any())

    def test_p10_02_preprocessing_and_leakage_audit(self):
        """P10-02: Validate preprocessing transformer sequence and target leakage isolation."""
        pipeline = build_pipeline(feature_set="baseline")
        pipeline.fit(self.X_train, self.y_train)

        # ColumnTransformer feature mapping (3 numerical + 27 one-hot-encoded features = 30)
        preprocessor = pipeline.named_steps["preprocessor"]
        feature_names = list(preprocessor.get_feature_names_out())
        self.assertEqual(len(feature_names), 30)

        # Verify customerID and Churn are excluded from features
        self.assertNotIn("customerID", self.X_train.columns)
        self.assertNotIn("Churn", self.X_train.columns)

        # Verify strict train/test split row counts
        self.assertEqual(len(self.X_train), 5634)
        self.assertEqual(len(self.X_test), 1409)

    def test_p10_03_model_loading_and_reconstruction(self):
        """P10-03: Validate model reconstruction and hyperparameter preservation."""
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

        # Verify estimator step
        pipe_clf = pipeline.named_steps["classifier"]
        self.assertIsInstance(pipe_clf, RandomForestClassifier)
        self.assertEqual(pipe_clf.n_estimators, 300)
        self.assertEqual(pipe_clf.max_depth, 8)
        self.assertEqual(pipe_clf.min_samples_leaf, 2)
        self.assertEqual(pipe_clf.min_samples_split, 2)
        self.assertEqual(pipe_clf.max_features, "sqrt")

    def test_p10_04_inference_sequence_and_categorization(self):
        """P10-04: Validate end-to-end inference sequence, risk bands, and review reasons."""
        rf = RandomForestClassifier(n_estimators=300, max_depth=8, min_samples_leaf=2, min_samples_split=2, max_features="sqrt", random_state=42, n_jobs=-1)
        pipe = build_pipeline(feature_set="baseline", classifier=rf)
        pipe.fit(self.X_train, self.y_train)

        sample = self.X_test.iloc[0:5]
        probs = pipe.predict_proba(sample)[:, 1]

        for p in probs:
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)

        # Risk categorization boundary tests
        self.assertEqual(assign_risk_category(0.15), "Low Risk")
        self.assertEqual(assign_risk_category(0.29), "Low Risk")
        self.assertEqual(assign_risk_category(0.30), "Medium Risk")
        self.assertEqual(assign_risk_category(0.49), "Medium Risk")
        self.assertEqual(assign_risk_category(0.50), "High Risk")
        self.assertEqual(assign_risk_category(0.69), "High Risk")
        self.assertEqual(assign_risk_category(0.70), "Very High Risk")
        self.assertEqual(assign_risk_category(0.85), "Very High Risk")

        # Explain customer function (accepts customer_row and churn_probability)
        sample_row = sample.iloc[0].copy()
        sample_row["customerID"] = "CUST-TEST-01"
        explanation = explain_customer(sample_row, probs[0])
        self.assertEqual(explanation["customerID"], "CUST-TEST-01")
        self.assertIn("churn_probability", explanation)
        self.assertIn("risk_category", explanation)
        self.assertIsInstance(explanation["review_reasons"], list)

    def test_p10_05_edge_case_resilience(self):
        """P10-05: Test pipeline resilience against missing numericals, unseen categories, and extreme values."""
        rf = RandomForestClassifier(n_estimators=300, max_depth=8, min_samples_leaf=2, min_samples_split=2, max_features="sqrt", random_state=42, n_jobs=-1)
        pipe = build_pipeline(feature_set="baseline", classifier=rf)
        pipe.fit(self.X_train, self.y_train)

        # Case A & B: Missing TotalCharges + Unseen Category in Contract / PaymentMethod
        edge_sample = self.X_test.iloc[0:1].copy()
        edge_sample["TotalCharges"] = "   "  # blank whitespace
        edge_sample["Contract"] = "Three year"  # unseen category
        edge_sample["PaymentMethod"] = "Crypto Transfer"  # unseen category

        prob = pipe.predict_proba(edge_sample)[:, 1][0]
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

        # Case C: Boundary/Extreme numerical values
        extreme_sample = self.X_test.iloc[0:1].copy()
        extreme_sample["tenure"] = 0
        extreme_sample["MonthlyCharges"] = 250.0
        extreme_sample["TotalCharges"] = 15000.0

        prob_ext = pipe.predict_proba(extreme_sample)[:, 1][0]
        self.assertGreaterEqual(prob_ext, 0.0)
        self.assertLessEqual(prob_ext, 1.0)

    def test_p10_06_clean_environment_and_manifests(self):
        """P10-06: Verify project dependency manifests for Python and Node/React requirements."""
        req_path = PROJECT_ROOT / "requirements.txt"
        pkg_path = PROJECT_ROOT / "package.json"

        self.assertTrue(req_path.exists())
        self.assertTrue(pkg_path.exists())

        req_text = req_path.read_text(encoding="utf-8")
        for pkg in ["pandas", "numpy", "scikit-learn", "matplotlib", "pytest"]:
            self.assertIn(pkg, req_text)

        pkg_json = json.loads(pkg_path.read_text(encoding="utf-8"))
        self.assertIn("dependencies", pkg_json)
        self.assertIn("react", pkg_json["dependencies"])
        self.assertIn("express", pkg_json["dependencies"])

    def test_p10_07_reproducibility_and_determinism(self):
        """P10-07: Verify random seed determinism and ranking stability."""
        # Split determinism
        X_tr1, X_te1, y_tr1, y_te1 = split_data(self.X, self.y, test_size=0.2, random_state=42)
        X_tr2, X_te2, y_tr2, y_te2 = split_data(self.X, self.y, test_size=0.2, random_state=42)
        pd.testing.assert_frame_equal(X_tr1, X_tr2)
        pd.testing.assert_series_equal(y_tr1, y_tr2)

        # Ranking order tie-breaking determinism
        self.assertTrue((self.ranked_df["rank"] == range(1, len(self.ranked_df) + 1)).all())
        probs = self.ranked_df["churn_probability"].values
        # Verify non-increasing order
        self.assertTrue(np.all(probs[:-1] >= probs[1:]))

    def test_p10_08_artifact_and_ui_consistency(self):
        """P10-08: Verify complete data consistency across Phase 7, Phase 8, and UI artifacts."""
        # Phase 7 metrics
        self.assertEqual(self.p7_results["test_set_size"], 1409)
        self.assertEqual(self.p7_results["roc_auc"], 0.8429)
        self.assertEqual(self.p7_results["pr_auc"], 0.6562)
        self.assertEqual(self.p7_results["precision"], 0.6866)
        self.assertEqual(self.p7_results["recall"], 0.4920)
        self.assertEqual(self.p7_results["f1"], 0.5732)
        self.assertEqual(self.p7_results["brier_score"], 0.1362)

        cm = self.p7_results["confusion_matrix"]
        self.assertEqual(cm["tn"], 951)
        self.assertEqual(cm["fp"], 84)
        self.assertEqual(cm["fn"], 190)
        self.assertEqual(cm["tp"], 184)
        self.assertEqual(cm["tn"] + cm["fp"] + cm["fn"] + cm["tp"], 1409)

        # Phase 8 summary metrics
        self.assertEqual(self.p8_summary["total_customers_scored"], 7043)
        self.assertEqual(self.p8_summary["risk_category_counts"]["High Risk"], 934)
        self.assertEqual(self.p8_summary["risk_category_counts"]["Very High Risk"], 428)
        self.assertEqual(self.p8_summary["high_risk_or_very_high_risk_count"], 1362)

        high_plus_very_high_pct = (
            self.p8_summary["risk_category_percentages"]["High Risk"] +
            self.p8_summary["risk_category_percentages"]["Very High Risk"]
        )
        self.assertAlmostEqual(high_plus_very_high_pct, 19.34, places=2)

        # Ranked CSV row count
        self.assertEqual(len(self.ranked_df), 7043)


if __name__ == "__main__":
    unittest.main()

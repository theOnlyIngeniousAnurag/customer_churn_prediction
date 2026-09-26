"""Automated unit test suite for Phase 5 Tree-Based Model Benchmarking."""

import json
import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.models.tree_models import (
    build_tree_pipeline,
    get_decision_tree_model,
    get_random_forest_model,
)
from src.evaluation.tree_models import run_tree_benchmarking


class TestTreeModels(unittest.TestCase):
    """Test suite for Phase 5 Decision Tree and Random Forest benchmarking."""

    @classmethod
    def setUpClass(cls):
        """Load and partition dataset once for all unit tests."""
        cls.raw_df = load_raw_dataset(PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv")
        X, y = prepare_target(cls.raw_df)
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = split_data(
            X, y, test_size=0.2, random_state=42
        )

    def test_decision_tree_model_construction_and_hyperparameters(self):
        """Verify Decision Tree classifier matches un-tuned Phase 5 specification."""
        model = get_decision_tree_model(random_state=42)
        self.assertIsInstance(model, DecisionTreeClassifier)
        self.assertEqual(model.random_state, 42)
        self.assertIsNone(model.max_depth)
        self.assertEqual(model.min_samples_split, 2)
        self.assertEqual(model.min_samples_leaf, 1)

    def test_random_forest_model_construction_and_hyperparameters(self):
        """Verify Random Forest classifier matches un-tuned Phase 5 specification."""
        model = get_random_forest_model(n_estimators=300, random_state=42, n_jobs=-1)
        self.assertIsInstance(model, RandomForestClassifier)
        self.assertEqual(model.n_estimators, 300)
        self.assertEqual(model.random_state, 42)
        self.assertEqual(model.n_jobs, -1)
        self.assertIsNone(model.max_depth)
        self.assertEqual(model.min_samples_split, 2)
        self.assertEqual(model.min_samples_leaf, 1)
        self.assertIsNone(model.class_weight)

    def test_tree_pipelines_structure(self):
        """Verify pipeline steps for both Decision Tree and Random Forest."""
        dt_pipe = build_tree_pipeline(model_type="decision_tree", feature_set="baseline", random_state=42)
        rf_pipe = build_tree_pipeline(model_type="random_forest", feature_set="baseline", random_state=42)

        self.assertEqual([name for name, _ in dt_pipe.steps], ["total_charges_cleaner", "preprocessor", "classifier"])
        self.assertEqual([name for name, _ in rf_pipe.steps], ["total_charges_cleaner", "preprocessor", "classifier"])
        self.assertIsInstance(dt_pipe.named_steps["classifier"], DecisionTreeClassifier)
        self.assertIsInstance(rf_pipe.named_steps["classifier"], RandomForestClassifier)

    def test_tree_pipelines_fit_and_probabilities(self):
        """Verify tree pipelines fit on training data and generate valid probability distributions."""
        rf_pipe = build_tree_pipeline(model_type="random_forest", feature_set="baseline", random_state=42, n_estimators=50)
        rf_pipe.fit(self.X_train, self.y_train)

        probs = rf_pipe.predict_proba(self.X_train)
        preds = rf_pipe.predict(self.X_train)

        self.assertEqual(probs.shape, (len(self.X_train), 2))
        self.assertTrue((probs >= 0.0).all() and (probs <= 1.0).all())
        np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-6)

        expected_preds = (probs[:, 1] >= 0.50).astype(int)
        np.testing.assert_array_equal(preds, expected_preds)

    def test_feature_importance_extraction_and_alignment(self):
        """Verify feature importances align exactly with preprocessed feature names."""
        dt_pipe = build_tree_pipeline(model_type="decision_tree", feature_set="baseline", random_state=42)
        dt_pipe.fit(self.X_train, self.y_train)

        feat_names = list(dt_pipe.named_steps["preprocessor"].get_feature_names_out())
        dt_importances = dt_pipe.named_steps["classifier"].feature_importances_

        self.assertEqual(len(feat_names), 30)
        self.assertEqual(len(dt_importances), 30)
        self.assertTrue((dt_importances >= 0.0).all())
        self.assertAlmostEqual(dt_importances.sum(), 1.0, places=4)

    def test_test_set_isolation_in_tree_benchmarking(self):
        """Verify tree benchmarking artifacts document that test set was not used."""
        report_path = PROJECT_ROOT / "reports" / "results" / "tree_model_benchmark.json"
        if not report_path.exists():
            run_tree_benchmarking()

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertFalse(data["metadata"]["test_set_used"])
        self.assertFalse(data["metadata"]["test_set_fitted"])
        self.assertFalse(data["metadata"]["test_set_predicted"])
        self.assertEqual(data["metadata"]["training_sample_count"], 5634)
        self.assertEqual(data["metadata"]["test_sample_count"], 1409)

    def test_benchmark_artifacts_exist_and_are_valid(self):
        """Verify JSON benchmark report and feature importance CSVs exist and contain valid data."""
        json_path = PROJECT_ROOT / "reports" / "results" / "tree_model_benchmark.json"
        dt_csv_path = PROJECT_ROOT / "reports" / "results" / "decision_tree_feature_importance.csv"
        rf_csv_path = PROJECT_ROOT / "reports" / "results" / "random_forest_feature_importance.csv"

        self.assertTrue(json_path.exists())
        self.assertTrue(dt_csv_path.exists())
        self.assertTrue(rf_csv_path.exists())

        # Check Decision Tree CSV
        df_dt = pd.read_csv(dt_csv_path)
        self.assertEqual(len(df_dt), 30)
        self.assertListEqual(list(df_dt.columns), ["feature", "importance"])

        # Check Random Forest CSV
        df_rf = pd.read_csv(rf_csv_path)
        self.assertEqual(len(df_rf), 30)
        self.assertListEqual(list(df_rf.columns), ["feature", "importance"])

        # Check JSON content
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("Decision Tree (Original)", data["benchmark_comparison"])
        self.assertIn("Random Forest (Original)", data["benchmark_comparison"])
        rf_metrics = data["benchmark_comparison"]["Random Forest (Original)"]
        self.assertAlmostEqual(rf_metrics["roc_auc"]["mean"], 0.8260, places=3)
        self.assertAlmostEqual(rf_metrics["average_precision"]["mean"], 0.6241, places=3)


if __name__ == "__main__":
    unittest.main()

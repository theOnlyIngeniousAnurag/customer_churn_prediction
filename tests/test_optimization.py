"""Automated unit test suite for Phase 6 Model Optimization and Validation."""

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class TestPhase6Optimization(unittest.TestCase):
    """Test suite to validate Phase 6 optimization results and compliance."""

    @classmethod
    def setUpClass(cls):
        """Set up and load the summary artifact."""
        cls.summary_path = PROJECT_ROOT / "reports" / "results" / "phase6_optimization_summary.json"
        cls.dt_tuning_path = PROJECT_ROOT / "reports" / "results" / "decision_tree_tuning_results.csv"
        cls.rf_tuning_path = PROJECT_ROOT / "reports" / "results" / "random_forest_tuning_results.csv"

        with open(cls.summary_path, "r", encoding="utf-8") as f:
            cls.summary = json.load(f)

    def test_summary_artifact_exists_and_is_valid(self):
        """Verify the optimization summary JSON exists and has basic structure."""
        self.assertTrue(self.summary_path.exists())
        self.assertEqual(self.summary["phase"], "Phase 6")
        self.assertFalse(self.summary["test_set_used"])

    def test_cross_validation_configuration(self):
        """Verify cross-validation setup in the summary."""
        cv_conf = self.summary["cross_validation"]
        self.assertEqual(cv_conf["method"], "StratifiedKFold")
        self.assertEqual(cv_conf["n_splits"], 5)
        self.assertTrue(cv_conf["shuffle"])
        self.assertEqual(cv_conf["random_state"], 42)
        self.assertEqual(cv_conf["primary_metric"], "average_precision")

    def test_decision_tree_results_valid(self):
        """Verify Decision Tree tuned results are recorded and reasonable."""
        dt = self.summary["decision_tree"]
        self.assertEqual(dt["iterations"], 15)
        self.assertIsNotNone(dt["best_params"])
        self.assertGreater(dt["best_cv_pr_auc"], 0.50)
        self.assertGreater(dt["roc_auc"], 0.70)
        self.assertGreater(dt["f1"], 0.50)

        diag = dt["overfitting_diagnostic"]
        self.assertGreater(diag["train_pr_auc"], diag["validation_pr_auc"])
        self.assertLess(diag["train_val_gap"], 0.10)  # Regularized tree should have < 10% gap

    def test_random_forest_results_valid(self):
        """Verify Random Forest tuned results are recorded and reasonable."""
        rf = self.summary["random_forest"]
        self.assertEqual(rf["iterations"], 20)
        self.assertIsNotNone(rf["best_params"])
        self.assertGreater(rf["best_cv_pr_auc"], 0.60)
        self.assertGreater(rf["roc_auc"], 0.80)
        self.assertGreater(rf["f1"], 0.50)

        diag = rf["overfitting_diagnostic"]
        self.assertGreater(diag["train_pr_auc"], diag["validation_pr_auc"])
        self.assertLess(diag["train_val_gap"], 0.15)  # RF should have reasonable train-val gap

    def test_tuning_history_csv_artifacts_exist(self):
        """Verify full search history was exported as CSV for reproducibility."""
        self.assertTrue(self.dt_tuning_path.exists())
        self.assertTrue(self.rf_tuning_path.exists())


if __name__ == "__main__":
    unittest.main()

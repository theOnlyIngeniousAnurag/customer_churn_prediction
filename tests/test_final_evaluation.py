"""Automated unit test suite for Phase 7 Final Evaluation."""

import json
import sys
import unittest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class TestPhase7FinalEvaluation(unittest.TestCase):
    """Validation test suite for Phase 7 final test evaluation results and compliance."""

    @classmethod
    def setUpClass(cls):
        """Set up and load Phase 7 output artifacts."""
        cls.summary_path = PROJECT_ROOT / "reports" / "results" / "phase7_final_test_results.json"
        cls.cm_path = PROJECT_ROOT / "reports" / "results" / "phase7_confusion_matrix.json"
        cls.thresholds_path = PROJECT_ROOT / "reports" / "results" / "phase7_threshold_analysis.csv"
        cls.error_path = PROJECT_ROOT / "reports" / "results" / "phase7_error_analysis.json"

        with open(cls.summary_path, "r", encoding="utf-8") as f:
            cls.summary = json.load(f)

        with open(cls.cm_path, "r", encoding="utf-8") as f:
            cls.cm = json.load(f)

        with open(cls.error_path, "r", encoding="utf-8") as f:
            cls.error_analysis = json.load(f)

        cls.df_thresholds = pd.read_csv(cls.thresholds_path)

    def test_summary_artifact_integrity(self):
        """Verify phase 7 final test summary exists and has required schema."""
        self.assertTrue(self.summary_path.exists())
        self.assertEqual(self.summary["phase"], "Phase 7")
        self.assertEqual(self.summary["model"], "Optimized Random Forest")
        self.assertEqual(self.summary["test_set_size"], 1409)
        self.assertTrue(self.summary["test_set_used"])
        self.assertEqual(self.summary["threshold_default"], 0.50)

    def test_primary_metrics_validity(self):
        """Verify that all metrics are finite and within valid probability/AUC bounds."""
        for metric_name in ["roc_auc", "pr_auc", "precision", "recall", "f1", "brier_score"]:
            val = self.summary[metric_name]
            self.assertIsNotNone(val)
            self.assertIsInstance(val, float)
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)

    def test_confusion_matrix_sum(self):
        """Verify that TN + FP + FN + TP equals exactly 1,409."""
        cm = self.summary["confusion_matrix"]
        tn, fp, fn, tp = cm["tn"], cm["fp"], cm["fn"], cm["tp"]
        self.assertEqual(tn + fp + fn + tp, 1409)
        self.assertEqual(self.cm["total_test_observations"], 1409)

    def test_threshold_grid_completeness(self):
        """Verify that the threshold analysis CSV contains all 11 requested grid points."""
        self.assertTrue(self.thresholds_path.exists())
        expected_thresholds = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
        actual_thresholds = list(self.df_thresholds["threshold"].round(2))
        self.assertEqual(actual_thresholds, expected_thresholds)

        for _, row in self.df_thresholds.iterrows():
            total_obs = row["tp"] + row["tn"] + row["fp"] + row["fn"]
            self.assertEqual(total_obs, 1409)

    def test_error_analysis_artifacts(self):
        """Verify that false positives and false negatives error breakdowns exist."""
        self.assertTrue(self.error_path.exists())
        self.assertIn("false_positives", self.error_analysis)
        self.assertIn("false_negatives", self.error_analysis)
        self.assertEqual(self.error_analysis["false_positives"]["count"], self.summary["confusion_matrix"]["fp"])
        self.assertEqual(self.error_analysis["false_negatives"]["count"], self.summary["confusion_matrix"]["fn"])


if __name__ == "__main__":
    unittest.main()

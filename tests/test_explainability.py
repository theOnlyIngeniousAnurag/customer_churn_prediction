"""Automated unit test suite for Phase 8 Explainability and Risk Ranking."""

import json
import sys
import unittest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.explainability import (
    assign_risk_category,
    explain_customer,
    generate_review_reasons,
)


class TestPhase8Explainability(unittest.TestCase):
    """Validation test suite for Phase 8 explainability and risk ranking outputs."""

    @classmethod
    def setUpClass(cls):
        """Set up and load Phase 8 output artifacts."""
        cls.importance_csv = PROJECT_ROOT / "reports" / "results" / "phase8_global_feature_importance.csv"
        cls.importance_json = PROJECT_ROOT / "reports" / "results" / "phase8_global_feature_importance.json"
        cls.risk_scores_csv = PROJECT_ROOT / "reports" / "results" / "phase8_customer_risk_scores.csv"
        cls.high_risk_csv = PROJECT_ROOT / "reports" / "results" / "phase8_high_risk_customers.csv"
        cls.summary_json = PROJECT_ROOT / "reports" / "results" / "phase8_explainability_summary.json"
        cls.figure_png = PROJECT_ROOT / "reports" / "figures" / "phase8_global_feature_importance.png"

        cls.df_importance = pd.read_csv(cls.importance_csv)
        cls.df_risk_scores = pd.read_csv(cls.risk_scores_csv)
        cls.df_high_risk = pd.read_csv(cls.high_risk_csv)

        with open(cls.summary_json, "r", encoding="utf-8") as f:
            cls.summary = json.load(f)

    def test_risk_category_boundary_mapping(self):
        """Test exact boundary values for risk category bands."""
        self.assertEqual(assign_risk_category(0.00), "Low Risk")
        self.assertEqual(assign_risk_category(0.29), "Low Risk")
        self.assertEqual(assign_risk_category(0.30), "Medium Risk")
        self.assertEqual(assign_risk_category(0.49), "Medium Risk")
        self.assertEqual(assign_risk_category(0.50), "High Risk")
        self.assertEqual(assign_risk_category(0.69), "High Risk")
        self.assertEqual(assign_risk_category(0.70), "Very High Risk")
        self.assertEqual(assign_risk_category(0.95), "Very High Risk")

    def test_global_feature_importance_validity(self):
        """Verify feature importance values are non-negative, numeric, sorted, and complete."""
        self.assertTrue(self.importance_csv.exists())
        self.assertTrue(self.importance_json.exists())
        self.assertTrue(self.figure_png.exists())

        self.assertGreater(len(self.df_importance), 0)
        importances = self.df_importance["importance"]
        self.assertTrue((importances >= 0.0).all())

        # Check descending sort
        is_sorted = (importances.diff().dropna() <= 0.0001).all()
        self.assertTrue(is_sorted)

        # Check total importance sum is close to 1.0 (or 100%)
        total_pct = self.df_importance["importance_pct"].sum()
        self.assertAlmostEqual(total_pct, 100.0, delta=0.5)

    def test_customer_risk_scoring_completeness(self):
        """Verify churn probabilities are generated for all 7,043 customers."""
        self.assertTrue(self.risk_scores_csv.exists())
        self.assertEqual(len(self.df_risk_scores), 7043)

        probs = self.df_risk_scores["churn_probability"]
        self.assertTrue((probs >= 0.0).all())
        self.assertTrue((probs <= 1.0).all())

        # Verify customer IDs are unique
        self.assertEqual(self.df_risk_scores["customerID"].nunique(), 7043)

    def test_ranked_high_risk_table(self):
        """Verify ranked high risk table is correctly sorted descending by probability."""
        self.assertTrue(self.high_risk_csv.exists())
        self.assertEqual(len(self.df_high_risk), 7043)

        top_probs = self.df_high_risk["churn_probability"]
        is_descending = (top_probs.diff().dropna() <= 0.0001).all()
        self.assertTrue(is_descending)

        # Verify ranks start at 1 and increment
        self.assertEqual(list(self.df_high_risk["rank"]), list(range(1, 7044)))

    def test_customer_level_explanation(self):
        """Verify evidence-based customer review reason generation."""
        sample_row = pd.Series({
            "customerID": "TEST-001",
            "Contract": "Month-to-month",
            "tenure": 3,
            "InternetService": "Fiber optic",
            "PaymentMethod": "Electronic check",
            "OnlineSecurity": "No",
            "TechSupport": "No",
            "MonthlyCharges": 85.50,
            "PaperlessBilling": "Yes",
        })

        explanation = explain_customer(sample_row, 0.82)
        self.assertEqual(explanation["customerID"], "TEST-001")
        self.assertEqual(explanation["risk_category"], "Very High Risk")
        self.assertTrue(explanation["predicted_churn"])

        reasons = explanation["review_reasons"]
        self.assertIn("Month-to-month contract", reasons)
        self.assertIn("Fiber optic internet service", reasons)
        self.assertIn("Payment via Electronic check", reasons)
        self.assertIn("No OnlineSecurity service", reasons)
        self.assertIn("No TechSupport service", reasons)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for Phase 2 Exploratory Data Analysis & Deep Leakage Audit."""

import sys
from pathlib import Path
import json
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.eda import (
    load_and_clean_for_eda,
    audit_structure_and_missingness,
    analyze_target_distribution,
    analyze_numerical_features,
    analyze_bivariate_categorical,
    analyze_bivariate_numerical,
    perform_deep_leakage_audit,
    evaluate_feature_engineering_candidates,
)


class TestEDAAndLeakageAudit(unittest.TestCase):
    """Test suite for Phase 2 EDA and leakage audit integrity."""

    @classmethod
    def setUpClass(cls):
        cls.df = load_and_clean_for_eda()

    def test_dataset_dimensions_and_schema(self):
        """Verify row and column dimensions match verified benchmark."""
        self.assertEqual(len(self.df), 7043)
        self.assertIn("customerID", self.df.columns)
        self.assertIn("Churn", self.df.columns)
        self.assertIn("TotalCharges_numeric", self.df.columns)

    def test_totalcharges_whitespace_and_tenure_zero(self):
        """Verify 11 whitespace values in TotalCharges strictly map to tenure=0."""
        audit = audit_structure_and_missingness(self.df)
        self.assertEqual(audit["totalcharges_whitespace_count"], 11)
        self.assertTrue(audit["totalcharges_all_tenure_zero"])
        self.assertEqual(len(audit["totalcharges_whitespace_tenures"]), 11)
        self.assertTrue(all(t == 0 for t in audit["totalcharges_whitespace_tenures"]))

    def test_target_distribution_and_imbalance(self):
        """Verify ground-truth churn counts and imbalance ratio."""
        target_info = analyze_target_distribution(self.df)
        counts = target_info["class_counts"]
        self.assertEqual(counts["No"], 5174)
        self.assertEqual(counts["Yes"], 1869)
        self.assertEqual(target_info["class_proportions_pct"]["Yes"], 26.54)
        self.assertEqual(target_info["class_proportions_pct"]["No"], 73.46)
        self.assertEqual(target_info["imbalance_ratio"], "2.77:1")

    def test_numerical_ranges_and_outliers(self):
        """Verify numerical ranges and IQR bounds."""
        num_stats = analyze_numerical_features(self.df)
        # Tenure range: 0 to 72 months
        self.assertEqual(num_stats["tenure"]["min"], 0.0)
        self.assertEqual(num_stats["tenure"]["max"], 72.0)
        self.assertEqual(num_stats["tenure"]["outlier_count_iqr"], 0)

        # MonthlyCharges: 18.25 to 118.75
        self.assertEqual(num_stats["MonthlyCharges"]["min"], 18.25)
        self.assertEqual(num_stats["MonthlyCharges"]["max"], 118.75)
        self.assertEqual(num_stats["MonthlyCharges"]["outlier_count_iqr"], 0)

        # TotalCharges parsed count: 7032 valid floats
        self.assertEqual(num_stats["TotalCharges_numeric"]["count"], 7032)

    def test_bivariate_churn_patterns(self):
        """Verify key observable patterns in bivariate analysis."""
        biv_num = analyze_bivariate_numerical(self.df)
        # Churners have substantially lower median tenure than non-churners (10 mos vs 38 mos)
        self.assertLess(biv_num["tenure"]["Yes_median"], biv_num["tenure"]["No_median"])
        self.assertEqual(biv_num["tenure"]["median_difference"], -28.0)

        # Churners have higher median monthly charges (79.65 vs 64.43)
        self.assertGreater(biv_num["MonthlyCharges"]["Yes_median"], biv_num["MonthlyCharges"]["No_median"])

        # Early tenure cohort (0-12 mos) has highest churn rate (~47%)
        cohorts = {c["tenure_group"]: c["churn_rate_pct"] for c in biv_num["tenure_cohorts"]}
        self.assertGreater(cohorts["0-12 mos"], 40.0)
        self.assertLess(cohorts["49-72 mos"], 15.0)

    def test_deep_leakage_audit_completeness(self):
        """Verify every column is evaluated in the leakage audit."""
        audit_table = perform_deep_leakage_audit()
        self.assertEqual(len(audit_table), 21)
        features_evaluated = [row["feature"] for row in audit_table]
        self.assertEqual(set(features_evaluated), set(self.df.columns.drop("TotalCharges_numeric")))

        # customerID must be EXCLUDE
        cust_id_row = next(r for r in audit_table if r["feature"] == "customerID")
        self.assertEqual(cust_id_row["decision"], "EXCLUDE")

        # Churn must be TARGET
        churn_row = next(r for r in audit_table if r["feature"] == "Churn")
        self.assertEqual(churn_row["decision"], "TARGET")

        # Predictive features must be KEEP
        keep_features = [r["feature"] for r in audit_table if r["decision"] == "KEEP"]
        self.assertEqual(len(keep_features), 19)

    def test_feature_engineering_candidates_documented(self):
        """Verify feature engineering candidates audit includes limitations on missing fields."""
        candidates = evaluate_feature_engineering_candidates()
        approved = [c for c in candidates if c["keep_candidate"]]
        unavailable = [c for c in candidates if not c["keep_candidate"]]

        self.assertGreaterEqual(len(approved), 4)
        # Missing fields from internship brief must be documented as unavailable
        unavail_names = [c["candidate_feature"] for c in unavailable]
        self.assertIn("support_contact_frequency", unavail_names)
        self.assertIn("usage_trend_delta", unavail_names)
        self.assertIn("recent_billing_change", unavail_names)

    def test_figures_and_json_report_exist(self):
        """Verify generated report and figures exist on disk and are non-empty."""
        report_path = PROJECT_ROOT / "reports" / "results" / "eda_audit_report.json"
        self.assertTrue(report_path.exists())
        with open(report_path) as f:
            data = json.load(f)
        self.assertIn("dataset_structure", data)
        self.assertIn("leakage_audit", data)

        figures = [
            "01_target_distribution.png",
            "02_tenure_vs_churn.png",
            "03_monthly_charges_kde_churn.png",
            "04_churn_rate_by_contract.png",
            "05_churn_by_internet_and_payment.png",
            "06_numerical_correlation_matrix.png",
        ]
        for fig_name in figures:
            fig_path = PROJECT_ROOT / "reports" / "figures" / fig_name
            self.assertTrue(fig_path.exists(), f"Figure {fig_name} missing")
            self.assertGreater(fig_path.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()

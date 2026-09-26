"""Unit tests for Phase 3 Feature Engineering Candidates and Transformer."""

import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target
from src.features.engineering import (
    compute_tenure_group,
    compute_total_services_subscribed,
    compute_has_tech_support_or_security,
    compute_auto_payment_indicator,
    compute_charges_ratio,
    FeatureEngineeringTransformer,
    SERVICE_CATALOG_COMPONENTS,
)


class TestFeatureEngineering(unittest.TestCase):
    """Test suite verifying candidate feature logic, boundaries, and transformer behavior."""

    @classmethod
    def setUpClass(cls):
        cls.raw_df = load_raw_dataset(PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv")
        cls.X, cls.y = prepare_target(cls.raw_df)

    def test_tenure_group_bins_and_boundary_conditions(self):
        """Verify tenure_group handles boundaries [0, 12, 13, 24, 25, 48, 49, 72] correctly."""
        test_tenures = pd.Series([0, 1, 12, 13, 24, 25, 48, 49, 72])
        binned = compute_tenure_group(test_tenures)

        expected = ["0-12", "0-12", "0-12", "13-24", "13-24", "25-48", "25-48", "49-72", "49-72"]
        self.assertEqual(binned.tolist(), expected)

        # Full dataset evaluation
        full_binned = compute_tenure_group(self.X["tenure"])
        self.assertEqual(len(full_binned), 7043)
        self.assertEqual(set(full_binned.unique()), {"0-12", "13-24", "25-48", "49-72"})

    def test_total_services_subscribed_catalog_and_range(self):
        """Verify total_services_subscribed evaluates 9 components and spans [1, 9]."""
        self.assertEqual(len(SERVICE_CATALOG_COMPONENTS), 9)

        services = compute_total_services_subscribed(self.X)
        self.assertEqual(len(services), 7043)
        self.assertEqual(services.min(), 1)
        self.assertEqual(services.max(), 9)

        # Synthetic verification of all-yes vs single-service
        synthetic_df = pd.DataFrame({
            "PhoneService": ["Yes", "No"],
            "MultipleLines": ["Yes", "No"],
            "InternetService": ["Fiber optic", "DSL"],
            "OnlineSecurity": ["Yes", "No"],
            "OnlineBackup": ["Yes", "No"],
            "DeviceProtection": ["Yes", "No"],
            "TechSupport": ["Yes", "No"],
            "StreamingTV": ["Yes", "No"],
            "StreamingMovies": ["Yes", "No"],
        })
        synth_services = compute_total_services_subscribed(synthetic_df)
        self.assertEqual(synth_services.iloc[0], 9)
        self.assertEqual(synth_services.iloc[1], 1)  # Only InternetService (DSL) is active

    def test_has_tech_support_or_security_or_logic(self):
        """Verify binary flag is 1 if either TechSupport or OnlineSecurity is Yes."""
        synthetic_df = pd.DataFrame({
            "TechSupport": ["Yes", "No", "No internet service", "Yes"],
            "OnlineSecurity": ["No", "Yes", "No internet service", "Yes"],
        })
        flag = compute_has_tech_support_or_security(synthetic_df)
        self.assertEqual(flag.tolist(), [1, 1, 0, 1])

        # Test dataset
        full_flag = compute_has_tech_support_or_security(self.X)
        self.assertEqual(len(full_flag), 7043)
        self.assertTrue(set(full_flag.unique()).issubset({0, 1}))

    def test_auto_payment_indicator_matches(self):
        """Verify auto_payment_indicator identifies automatic payment methods."""
        synthetic_methods = pd.Series([
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Electronic check",
            "Mailed check",
        ])
        auto_flag = compute_auto_payment_indicator(synthetic_methods)
        self.assertEqual(auto_flag.tolist(), [1, 1, 0, 0])

        full_flag = compute_auto_payment_indicator(self.X["PaymentMethod"])
        self.assertEqual(len(full_flag), 7043)
        self.assertTrue(set(full_flag.unique()).issubset({0, 1}))

    def test_charges_ratio_tenure_zero_safety(self):
        """Verify charges_ratio evaluates safely without division by zero when TotalCharges=0.0."""
        # When TotalCharges is 0.0, denominator is 0.0 + 1.0 = 1.0, so result is MonthlyCharges
        monthly = pd.Series([25.0, 80.0, 100.0])
        total = pd.Series([0.0, 159.0, 999.0])
        ratio = compute_charges_ratio(monthly, total)

        self.assertAlmostEqual(ratio.iloc[0], 25.0 / 1.0)
        self.assertAlmostEqual(ratio.iloc[1], 80.0 / 160.0)
        self.assertAlmostEqual(ratio.iloc[2], 100.0 / 1000.0)
        self.assertFalse(ratio.isna().any())
        self.assertFalse(np.isinf(ratio).any())

    def test_feature_engineering_transformer_all_features(self):
        """Verify FeatureEngineeringTransformer appends all 5 candidate features when configured."""
        fe = FeatureEngineeringTransformer(
            include_tenure_group=True,
            include_total_services=True,
            include_tech_support_security=True,
            include_auto_payment=True,
            include_charges_ratio=True,
        )
        fe.fit(self.X)
        X_eng = fe.transform(self.X)

        self.assertEqual(len(X_eng), 7043)
        expected_added = [
            "tenure_group",
            "total_services_subscribed",
            "has_tech_support_or_security",
            "auto_payment_indicator",
            "charges_ratio",
        ]
        for col in expected_added:
            self.assertIn(col, X_eng.columns)

        feature_names_out = fe.get_feature_names_out()
        self.assertEqual(len(feature_names_out), len(self.X.columns) + 5)

    def test_feature_engineering_stateless_integrity(self):
        """Verify transformer does not modify original DataFrame and does not access target."""
        original_cols = list(self.X.columns)
        fe = FeatureEngineeringTransformer(include_tenure_group=True)
        _ = fe.fit_transform(self.X)

        # Original dataframe columns must remain unchanged
        self.assertEqual(list(self.X.columns), original_cols)
        self.assertNotIn("Churn", self.X.columns)
        self.assertNotIn("customerID", self.X.columns)


if __name__ == "__main__":
    unittest.main()

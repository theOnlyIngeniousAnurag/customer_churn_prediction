"""Unit tests for Phase 3 Preprocessing Architecture and Leakage Controls."""

import hashlib
import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.features.preprocessing import (
    TotalChargesCleaner,
    build_column_transformer,
    build_pipeline,
    RAW_NUMERICAL_FEATURES,
    RAW_CATEGORICAL_FEATURES,
)


class TestPreprocessingArchitecture(unittest.TestCase):
    """Test suite verifying target preparation, train/test splitting, and preprocessing."""

    @classmethod
    def setUpClass(cls):
        cls.raw_df = load_raw_dataset(PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv")

    def test_raw_dataset_byte_integrity(self):
        """Verify the raw CSV has not been modified or corrupted (MD5 hash check)."""
        raw_path = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
        with open(raw_path, "rb") as f:
    raw_bytes = f.read()

# Normalize line endings so the integrity check is platform-independent.
normalized_bytes = raw_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
file_hash = hashlib.md5(normalized_bytes).hexdigest()
        self.assertEqual(
            file_hash,
            "3b0bfab28a8101b4e4fdd08025a5c235",
            "Raw dataset hash mismatch! data/raw/Telco-Customer-Churn.csv must remain untouched."
        )

    def test_target_preparation_mapping(self):
        """Verify deterministic target mapping: 'No' -> 0, 'Yes' -> 1, customerID dropped."""
        X, y = prepare_target(self.raw_df)

        self.assertEqual(len(X), 7043)
        self.assertEqual(len(y), 7043)
        self.assertNotIn("customerID", X.columns)
        self.assertNotIn("Churn", X.columns)
        self.assertEqual(y.dtype, np.int64)

        # Check target class counts
        counts = y.value_counts().to_dict()
        self.assertEqual(counts[0], 5174)
        self.assertEqual(counts[1], 1869)
        self.assertFalse(y.isna().any())

    def test_target_preparation_error_handling(self):
        """Verify error handling on invalid target categories or missing target column."""
        corrupted_df = self.raw_df.copy()
        corrupted_df.loc[0, "Churn"] = "Maybe"
        with self.assertRaises(ValueError):
            prepare_target(corrupted_df)

        missing_target_df = self.raw_df.drop(columns=["Churn"])
        with self.assertRaises(KeyError):
            prepare_target(missing_target_df)

    def test_train_test_split_properties(self):
        """Verify 80/20 stratified split, sample counts, and isolation."""
        X, y = prepare_target(self.raw_df)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

        # Dimensions
        self.assertEqual(len(X_train), 5634)
        self.assertEqual(len(X_test), 1409)
        self.assertEqual(len(X_train) + len(X_test), 7043)

        # Stratification: churn rate ~26.54% in both sets
        train_churn_pct = round(y_train.mean() * 100, 2)
        test_churn_pct = round(y_test.mean() * 100, 2)
        self.assertEqual(train_churn_pct, 26.54)
        self.assertEqual(test_churn_pct, 26.54)

        # Disjoint row indices (no overlap)
        train_indices = set(X_train.index)
        test_indices = set(X_test.index)
        self.assertEqual(len(train_indices.intersection(test_indices)), 0)

    def test_totalcharges_cleaner_tenure_zero_domain_assignment(self):
        """Verify TotalChargesCleaner sets tenure=0 blanks to 0.0 and learns median from train."""
        X, y = prepare_target(self.raw_df)
        X_train, X_test, _, _ = split_data(X, y, test_size=0.2, random_state=42)

        cleaner = TotalChargesCleaner()
        cleaner.fit(X_train)

        # Verify training median was learned
        self.assertIsNotNone(cleaner.median_total_charges_)
        self.assertGreater(cleaner.median_total_charges_, 1000.0)

        # Transform train
        X_train_clean = cleaner.transform(X_train)
        self.assertEqual(X_train_clean["TotalCharges"].isna().sum(), 0)

        # Verify tenure=0 rows in train are strictly 0.0
        tenure_zero_train = X_train_clean[X_train_clean["tenure"] == 0]["TotalCharges"]
        self.assertTrue((tenure_zero_train == 0.0).all())

        # Transform test using already-fitted cleaner
        saved_median = cleaner.median_total_charges_
        X_test_clean = cleaner.transform(X_test)
        self.assertEqual(cleaner.median_total_charges_, saved_median)
        self.assertEqual(X_test_clean["TotalCharges"].isna().sum(), 0)

        # Verify tenure=0 rows in test are strictly 0.0
        tenure_zero_test = X_test_clean[X_test_clean["tenure"] == 0]["TotalCharges"]
        self.assertTrue((tenure_zero_test == 0.0).all())

    def test_totalcharges_cleaner_fallback_imputation(self):
        """Verify fallback median is used when tenure > 0 has an unexpected missing TotalCharges."""
        synthetic_df = pd.DataFrame({
            "tenure": [10, 0, 24],
            "TotalCharges": ["100.0", " ", " "]  # row index 2 has tenure=24 but blank TotalCharges
        })
        cleaner = TotalChargesCleaner()
        cleaner.fit(synthetic_df)

        cleaned = cleaner.transform(synthetic_df)
        # Row 0: 100.0
        self.assertEqual(cleaned.loc[0, "TotalCharges"], 100.0)
        # Row 1: tenure=0 -> 0.0
        self.assertEqual(cleaned.loc[1, "TotalCharges"], 0.0)
        # Row 2: tenure=24 -> fallback to training median (100.0)
        self.assertEqual(cleaned.loc[2, "TotalCharges"], 100.0)

    def test_pipeline_fit_train_transform_test(self):
        """Verify pipeline fits on training set, transforms test set, and preserves dimensions."""
        X, y = prepare_target(self.raw_df)
        X_train, X_test, _, _ = split_data(X, y, test_size=0.2, random_state=42)

        pipeline = build_pipeline(feature_set="baseline")

        # Fit on train
        train_transformed = pipeline.fit_transform(X_train)
        self.assertIsInstance(train_transformed, np.ndarray)
        self.assertEqual(train_transformed.shape[0], len(X_train))

        # Transform on test
        test_transformed = pipeline.transform(X_test)
        self.assertIsInstance(test_transformed, np.ndarray)
        self.assertEqual(test_transformed.shape[0], len(X_test))
        self.assertEqual(train_transformed.shape[1], test_transformed.shape[1])

    def test_feature_names_out_traceability(self):
        """Verify preprocessor provides inspectable feature names out."""
        preprocessor = build_column_transformer(feature_set="baseline")
        cleaner = TotalChargesCleaner()

        X, y = prepare_target(self.raw_df)
        X_clean = cleaner.fit_transform(X)
        preprocessor.fit(X_clean)

        feature_names = preprocessor.get_feature_names_out()
        self.assertGreater(len(feature_names), 25)
        # Ensure numerical features are present
        self.assertTrue(any("num__tenure" in f for f in feature_names))
        self.assertTrue(any("num__MonthlyCharges" in f for f in feature_names))
        self.assertTrue(any("num__TotalCharges" in f for f in feature_names))
        # Ensure categorical features are present
        self.assertTrue(any("cat__Contract" in f for f in feature_names))

    def test_categorical_unseen_category_handling(self):
        """Verify OneHotEncoder handle_unknown='ignore' does not crash on unseen category."""
        X, y = prepare_target(self.raw_df)
        X_train, X_test, _, _ = split_data(X, y, test_size=0.2, random_state=42)

        pipeline = build_pipeline(feature_set="baseline")
        pipeline.fit(X_train)

        # Inject an unseen category into a test sample
        X_test_unseen = X_test.copy()
        X_test_unseen.iloc[0, X_test_unseen.columns.get_loc("Contract")] = "Three year"

        # Transform must succeed without error
        transformed = pipeline.transform(X_test_unseen)
        self.assertEqual(transformed.shape[0], len(X_test))


if __name__ == "__main__":
    unittest.main()

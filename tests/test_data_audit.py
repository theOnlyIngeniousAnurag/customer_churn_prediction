"""Test suite for dataset loading and data audit verification."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import unittest
import pandas as pd
from src.data.loader import load_raw_dataset
from src.data.audit import run_initial_data_audit


class TestDataAudit(unittest.TestCase):
    """Test suite for dataset loading and data audit verification."""

    def test_raw_dataset_exists_and_unmodified(self):
        """Verify that raw dataset exists in data/raw/ and is readable."""
        raw_path = Path("data/raw/Telco-Customer-Churn.csv")
        self.assertTrue(raw_path.exists(), "Raw dataset file must exist in data/raw/")
        df = load_raw_dataset(raw_path)
        self.assertEqual(len(df), 7043, f"Expected 7043 rows, got {len(df)}")
        self.assertEqual(df.shape[1], 21, f"Expected 21 columns, got {df.shape[1]}")

    def test_data_audit_execution(self):
        """Verify that data audit runs cleanly and accurately identifies target and attributes."""
        raw_path = Path("data/raw/Telco-Customer-Churn.csv")
        results = run_initial_data_audit(raw_path)

        # Check structural fields
        self.assertEqual(results["n_rows"], 7043)
        self.assertEqual(results["n_cols"], 21)
        self.assertIn("customerID", results["identifiers"])

        # Check target
        self.assertTrue(results["target"]["present"])
        self.assertEqual(set(results["target"]["unique_values"]), {"No", "Yes"})
        self.assertEqual(results["target"]["value_counts"]["No"], 5174)
        self.assertEqual(results["target"]["value_counts"]["Yes"], 1869)

        # Check missingness checks
        self.assertEqual(results["missingness"]["total_charges_unparseable"], 11)
        self.assertEqual(results["duplicates"]["exact_duplicate_rows"], 0)
        self.assertEqual(results["duplicates"]["duplicate_customer_ids"], 0)


if __name__ == "__main__":
    unittest.main()


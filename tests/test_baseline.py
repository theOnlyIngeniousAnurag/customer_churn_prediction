"""Automated unit test suite for Phase 4 Logistic Regression Baseline Benchmarking."""

import json
import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_dataset, prepare_target, split_data
from src.features.preprocessing import RAW_NUMERICAL_FEATURES, RAW_CATEGORICAL_FEATURES
from src.models.baseline import build_baseline_pipeline, get_baseline_model
from src.evaluation.baseline import run_baseline_benchmarking


class TestBaselineModel(unittest.TestCase):
    """Test suite for Phase 4 Logistic Regression model and evaluation architecture."""

    @classmethod
    def setUpClass(cls):
        """Load and partition dataset once for all unit tests."""
        cls.raw_df = load_raw_dataset(PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv")
        X, y = prepare_target(cls.raw_df)
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = split_data(
            X, y, test_size=0.2, random_state=42
        )

    def test_baseline_model_construction_and_hyperparameters(self):
        """Verify baseline Logistic Regression configuration satisfies Phase 4 constraints."""
        model = get_baseline_model(random_state=42, max_iter=1000)
        self.assertIsInstance(model, LogisticRegression)
        self.assertEqual(model.max_iter, 1000)
        self.assertEqual(model.random_state, 42)
        self.assertEqual(model.C, 1.0)
        self.assertEqual(model.penalty, "l2")
        self.assertEqual(model.solver, "lbfgs")

    def test_baseline_pipeline_structure(self):
        """Verify pipeline stages: TotalChargesCleaner -> ColumnTransformer -> LogisticRegression."""
        pipeline = build_baseline_pipeline(feature_set="baseline", random_state=42)
        step_names = [name for name, _ in pipeline.steps]
        self.assertEqual(step_names, ["total_charges_cleaner", "preprocessor", "classifier"])
        self.assertIsInstance(pipeline.named_steps["classifier"], LogisticRegression)

    def test_baseline_pipeline_training_and_feature_count(self):
        """Verify pipeline fits on training data and encodes exactly 30 features."""
        pipeline = build_baseline_pipeline(feature_set="baseline", random_state=42)
        pipeline.fit(self.X_train, self.y_train)

        preprocessor = pipeline.named_steps["preprocessor"]
        feature_names = preprocessor.get_feature_names_out()
        classifier = pipeline.named_steps["classifier"]

        # 3 numerical + 27 one-hot encoded categories (16 categorical columns with drop='first') = 30
        self.assertEqual(len(feature_names), 30)
        self.assertEqual(len(classifier.coef_[0]), 30)

    def test_prediction_probabilities_and_default_threshold(self):
        """Verify probability outputs [0, 1], row sums to 1.0, and default 0.50 binary mapping."""
        pipeline = build_baseline_pipeline(feature_set="baseline", random_state=42)
        pipeline.fit(self.X_train, self.y_train)

        probs = pipeline.predict_proba(self.X_train)
        preds = pipeline.predict(self.X_train)

        self.assertEqual(probs.shape, (len(self.X_train), 2))
        self.assertTrue((probs >= 0.0).all() and (probs <= 1.0).all())
        np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-6)

        # Confirm default 0.50 threshold behavior
        expected_preds = (probs[:, 1] >= 0.50).astype(int)
        np.testing.assert_array_equal(preds, expected_preds)

    def test_cross_validation_configuration(self):
        """Verify 5-fold Stratified CV preserves class distribution across folds."""
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        splits = list(cv.split(self.X_train, self.y_train))
        self.assertEqual(len(splits), 5)

        for train_idx, val_idx in splits:
            y_val = self.y_train.iloc[val_idx]
            churn_rate = y_val.mean()
            # Each fold should tightly mirror 26.54% churn rate
            self.assertAlmostEqual(churn_rate, 0.2654, delta=0.015)

    def test_coefficient_alignment_and_sorting(self):
        """Verify coefficients can be matched unambiguously to preprocessed column names."""
        pipeline = build_baseline_pipeline(feature_set="baseline", random_state=42)
        pipeline.fit(self.X_train, self.y_train)

        feat_names = list(pipeline.named_steps["preprocessor"].get_feature_names_out())
        coefs = pipeline.named_steps["classifier"].coef_[0]

        coef_map = dict(zip(feat_names, coefs))
        self.assertIn("num__tenure", coef_map)
        self.assertIn("num__MonthlyCharges", coef_map)
        self.assertIn("num__TotalCharges", coef_map)
        self.assertIn("cat__Contract_Two year", coef_map)
        self.assertIn("cat__InternetService_Fiber optic", coef_map)

        # Verify contract two year has protective negative association
        self.assertLess(coef_map["cat__Contract_Two year"], -1.0)
        # Verify tenure has protective negative association
        self.assertLess(coef_map["num__tenure"], -1.0)
        # Verify fiber optic has positive churn association
        self.assertGreater(coef_map["cat__InternetService_Fiber optic"], 1.0)

    def test_test_set_isolation_in_benchmarking(self):
        """Verify benchmarking artifacts explicitly document that the test set was not used."""
        report_path = PROJECT_ROOT / "reports" / "results" / "logistic_regression_baseline.json"
        if not report_path.exists():
            run_baseline_benchmarking()

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertFalse(data["metadata"]["test_set_used"])
        self.assertFalse(data["metadata"]["test_set_fitted"])
        self.assertEqual(data["metadata"]["training_sample_count"], 5634)
        self.assertEqual(data["metadata"]["test_sample_count"], 1409)

    def test_artifacts_exist_and_are_valid(self):
        """Verify baseline JSON report and coefficients CSV exist and contain valid data."""
        json_path = PROJECT_ROOT / "reports" / "results" / "logistic_regression_baseline.json"
        csv_path = PROJECT_ROOT / "reports" / "results" / "logistic_regression_coefficients.csv"

        self.assertTrue(json_path.exists())
        self.assertTrue(csv_path.exists())

        # Check CSV content
        df_coef = pd.read_csv(csv_path)
        self.assertEqual(len(df_coef), 30)
        self.assertListEqual(list(df_coef.columns), ["feature", "coefficient", "absolute_coefficient"])
        self.assertTrue((df_coef["absolute_coefficient"] >= 0).all())

        # Check JSON content
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("Experiment A (Baseline)", data["experiments"])
        self.assertIn("Experiment B1 (+ tenure_group)", data["experiments"])
        exp_a_metrics = data["experiments"]["Experiment A (Baseline)"]["metrics"]
        self.assertAlmostEqual(exp_a_metrics["roc_auc"]["mean"], 0.8461, places=3)
        self.assertAlmostEqual(exp_a_metrics["average_precision"]["mean"], 0.6615, places=3)


if __name__ == "__main__":
    unittest.main()

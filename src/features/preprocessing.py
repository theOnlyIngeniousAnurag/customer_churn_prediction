"""Preprocessing architecture module for Telco Customer Churn.

Provides leakage-safe scikit-learn transformers and pipeline builders for:
    - TotalCharges whitespace handling, domain tenure-zero assignment, and fallback imputation
    - Numerical standardization (StandardScaler)
    - Categorical one-hot encoding (OneHotEncoder with drop='first' and handle_unknown='ignore')
    - Seamless composability with FeatureEngineeringTransformer
    - Strict train/test isolation (no test data leakage)
"""

import sys
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.features.engineering import FeatureEngineeringTransformer

# Verified Phase 1 and Phase 2 feature schema
RAW_NUMERICAL_FEATURES = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
]

RAW_CATEGORICAL_FEATURES = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]


class TotalChargesCleaner(BaseEstimator, TransformerMixin):
    """Leakage-safe transformer for TotalCharges conversion and domain handling.

    Sequence of operations:
        1. Strips whitespace strings and converts blanks to NaN.
        2. Applies domain rule: tenure == 0 accounts have 0 accrued billing cycles,
           so TotalCharges is deterministically set to 0.0.
        3. Fallback imputer: Any remaining unexpected missing values are imputed
           using the median learned strictly on the training set during fit().
        4. Casts TotalCharges to float64.
    """

    def __init__(self):
        self.median_total_charges_: float | None = None

    def fit(self, X: pd.DataFrame, y=None):
        """Learn training set median of valid TotalCharges values."""
        if not isinstance(X, pd.DataFrame):
            raise TypeError("TotalChargesCleaner expects a pandas DataFrame.")
        if "TotalCharges" not in X.columns:
            raise KeyError("TotalCharges column not present in input DataFrame.")

        tc_series = (
            X["TotalCharges"]
            .astype(str)
            .str.strip()
            .replace("", np.nan)
        )
        tc_numeric = pd.to_numeric(tc_series, errors="coerce")
        valid_charges = tc_numeric.dropna()

        if len(valid_charges) > 0:
            self.median_total_charges_ = float(valid_charges.median())
        else:
            self.median_total_charges_ = 0.0

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply deterministic parsing, domain zero assignment, and learned fallback imputation."""
        if self.median_total_charges_ is None:
            raise RuntimeError("TotalChargesCleaner must be fit before transforming data.")
        if not isinstance(X, pd.DataFrame):
            raise TypeError("TotalChargesCleaner expects a pandas DataFrame.")

        X_out = X.copy()
        tc_series = (
            X_out["TotalCharges"]
            .astype(str)
            .str.strip()
            .replace("", np.nan)
        )
        tc_numeric = pd.to_numeric(tc_series, errors="coerce")

        # Domain rule: zero tenure implies $0.00 accumulated spend to date
        if "tenure" in X_out.columns:
            tenure_numeric = pd.to_numeric(X_out["tenure"], errors="coerce").fillna(0.0)
            zero_tenure_mask = (tenure_numeric == 0) & tc_numeric.isna()
            tc_numeric = tc_numeric.mask(zero_tenure_mask, 0.0)

        # Fallback imputation for any remaining missing values using training median
        tc_numeric = tc_numeric.fillna(self.median_total_charges_)

        X_out["TotalCharges"] = tc_numeric.astype("float64")
        return X_out


def build_column_transformer(feature_set: str = "baseline") -> ColumnTransformer:
    """Construct ColumnTransformer for numerical scaling and categorical encoding.

    Parameters
    ----------
    feature_set : str, default 'baseline'
        Experiment identifier:
            - 'baseline' / 'a': Original 19 verified features
            - 'b1_tenure_group': Baseline + tenure_group
            - 'b2_total_services': Baseline + total_services_subscribed
            - 'b3_tech_support_security': Baseline + has_tech_support_or_security
            - 'b4_auto_payment': Baseline + auto_payment_indicator
            - 'b5_charges_ratio': Baseline + charges_ratio
            - 'c_all': Baseline + all five candidate features

    Returns
    -------
    ColumnTransformer
        Configured scikit-learn ColumnTransformer.
    """
    numerical_cols = list(RAW_NUMERICAL_FEATURES)
    categorical_cols = list(RAW_CATEGORICAL_FEATURES)

    if feature_set in ["b1_tenure_group", "b1"]:
        categorical_cols.append("tenure_group")
    elif feature_set in ["b2_total_services", "b2"]:
        numerical_cols.append("total_services_subscribed")
    elif feature_set in ["b3_tech_support_security", "b3"]:
        numerical_cols.append("has_tech_support_or_security")
    elif feature_set in ["b4_auto_payment", "b4"]:
        numerical_cols.append("auto_payment_indicator")
    elif feature_set in ["b5_charges_ratio", "b5"]:
        numerical_cols.append("charges_ratio")
    elif feature_set in ["c_all", "c"]:
        categorical_cols.append("tenure_group")
        numerical_cols.extend([
            "total_services_subscribed",
            "has_tech_support_or_security",
            "auto_payment_indicator",
            "charges_ratio",
        ])

    num_pipeline = Pipeline([
        ("scaler", StandardScaler()),
    ])

    cat_pipeline = Pipeline([
        ("ohe", OneHotEncoder(
            drop="first",
            sparse_output=False,
            handle_unknown="ignore"
        )),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_cols),
            ("cat", cat_pipeline, categorical_cols),
        ],
        remainder="drop"
    )

    return preprocessor


def build_pipeline(
    feature_set: str = "baseline",
    classifier: Any | None = None
) -> Pipeline:
    """Build complete, leakage-safe pipeline from raw DataFrame to model output.

    Parameters
    ----------
    feature_set : str, default 'baseline'
        Experiment identifier ('baseline', 'b1', 'b2', 'b3', 'b4', 'b5', 'c_all').
    classifier : estimator, optional
        Scikit-learn classifier to attach at the end of the pipeline.

    Returns
    -------
    Pipeline
        Composed scikit-learn Pipeline.
    """
    steps = [
        ("total_charges_cleaner", TotalChargesCleaner()),
    ]

    # Configure feature engineering step if applicable
    include_tg = feature_set in ["b1_tenure_group", "b1", "c_all", "c"]
    include_ts = feature_set in ["b2_total_services", "b2", "c_all", "c"]
    include_tss = feature_set in ["b3_tech_support_security", "b3", "c_all", "c"]
    include_ap = feature_set in ["b4_auto_payment", "b4", "c_all", "c"]
    include_cr = feature_set in ["b5_charges_ratio", "b5", "c_all", "c"]

    if any([include_tg, include_ts, include_tss, include_ap, include_cr]):
        fe = FeatureEngineeringTransformer(
            include_tenure_group=include_tg,
            include_total_services=include_ts,
            include_tech_support_security=include_tss,
            include_auto_payment=include_ap,
            include_charges_ratio=include_cr,
        )
        steps.append(("feature_engineering", fe))

    preprocessor = build_column_transformer(feature_set)
    steps.append(("preprocessor", preprocessor))

    if classifier is not None:
        steps.append(("classifier", classifier))

    return Pipeline(steps=steps)

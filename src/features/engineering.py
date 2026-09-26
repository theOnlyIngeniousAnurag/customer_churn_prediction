"""Feature engineering module for candidate derived features.

Provides deterministic, leakage-safe functions and a scikit-learn compatible
transformer for creating candidate features under controlled ablation.
"""

from typing import Sequence
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# Exactly 9 service catalog components documented in Phase 2
SERVICE_CATALOG_COMPONENTS = [
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]

# Tenure lifecycle bins
TENURE_BINS = [-1, 12, 24, 48, 100]
TENURE_LABELS = ["0-12", "13-24", "25-48", "49-72"]


def compute_tenure_group(tenure_series: pd.Series) -> pd.Series:
    """Bin continuous customer tenure into lifecycle cohort segments.

    Parameters
    ----------
    tenure_series : pd.Series
        Customer tenure in months.

    Returns
    -------
    pd.Series
        Categorical series with levels: ['0-12', '13-24', '25-48', '49-72'].
    """
    numeric_tenure = pd.to_numeric(tenure_series, errors="coerce").fillna(0.0)
    binned = pd.cut(
        numeric_tenure,
        bins=TENURE_BINS,
        labels=TENURE_LABELS,
        right=True
    )
    return binned.astype(str)


def compute_total_services_subscribed(df: pd.DataFrame) -> pd.Series:
    """Calculate integer count of active subscribed services across 9 components.

    Components evaluated:
        1. PhoneService == 'Yes'
        2. MultipleLines == 'Yes'
        3. InternetService in ['DSL', 'Fiber optic'] (not 'No')
        4. OnlineSecurity == 'Yes'
        5. OnlineBackup == 'Yes'
        6. DeviceProtection == 'Yes'
        7. TechSupport == 'Yes'
        8. StreamingTV == 'Yes'
        9. StreamingMovies == 'Yes'

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the 9 service catalog columns.

    Returns
    -------
    pd.Series
        Integer count of active services (empirical range: 1 to 9).
    """
    for col in SERVICE_CATALOG_COMPONENTS:
        if col not in df.columns:
            raise KeyError(f"Required service component column '{col}' missing from DataFrame.")

    total_services = (
        (df["PhoneService"] == "Yes").astype(int)
        + (df["MultipleLines"] == "Yes").astype(int)
        + (df["InternetService"].isin(["DSL", "Fiber optic"])).astype(int)
        + (df["OnlineSecurity"] == "Yes").astype(int)
        + (df["OnlineBackup"] == "Yes").astype(int)
        + (df["DeviceProtection"] == "Yes").astype(int)
        + (df["TechSupport"] == "Yes").astype(int)
        + (df["StreamingTV"] == "Yes").astype(int)
        + (df["StreamingMovies"] == "Yes").astype(int)
    )
    return total_services.astype("int64")


def compute_has_tech_support_or_security(df: pd.DataFrame) -> pd.Series:
    """Compute binary flag indicating presence of TechSupport OR OnlineSecurity.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing TechSupport and OnlineSecurity columns.

    Returns
    -------
    pd.Series
        Binary integer indicator (1 if either service is active, 0 otherwise).
    """
    for col in ["TechSupport", "OnlineSecurity"]:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' missing from DataFrame.")

    has_support = (df["TechSupport"] == "Yes") | (df["OnlineSecurity"] == "Yes")
    return has_support.astype("int64")


def compute_auto_payment_indicator(payment_series: pd.Series) -> pd.Series:
    """Compute binary flag indicating automated recurring billing methods.

    Matches 'Bank transfer (automatic)' and 'Credit card (automatic)'.

    Parameters
    ----------
    payment_series : pd.Series
        PaymentMethod column.

    Returns
    -------
    pd.Series
        Binary indicator (1 if automatic payment method, 0 if manual check).
    """
    is_auto = payment_series.astype(str).str.contains("automatic", case=False, na=False)
    return is_auto.astype("int64")


def compute_charges_ratio(monthly_charges: pd.Series, total_charges: pd.Series) -> pd.Series:
    """Calculate ratio of MonthlyCharges to TotalCharges with smoothing offset.

    Formula:
        charges_ratio = MonthlyCharges / (TotalCharges + 1.0)

    For tenure == 0 (TotalCharges = 0.0), charges_ratio evaluates safely to MonthlyCharges / 1.0.

    Parameters
    ----------
    monthly_charges : pd.Series
        Monthly recurring charges.
    total_charges : pd.Series
        Cumulative total charges.

    Returns
    -------
    pd.Series
        Calculated ratio (float64).
    """
    m = pd.to_numeric(monthly_charges, errors="coerce").fillna(0.0)
    t = pd.to_numeric(total_charges, errors="coerce").fillna(0.0)
    # Ensure non-negative denominator
    denom = np.maximum(t + 1.0, 1.0)
    return (m / denom).astype("float64")


class FeatureEngineeringTransformer(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible transformer for controlled feature engineering ablation.

    Parameters
    ----------
    include_tenure_group : bool, default False
        Whether to generate the categorical 'tenure_group' feature.
    include_total_services : bool, default False
        Whether to generate the integer 'total_services_subscribed' feature.
    include_tech_support_security : bool, default False
        Whether to generate the binary 'has_tech_support_or_security' feature.
    include_auto_payment : bool, default False
        Whether to generate the binary 'auto_payment_indicator' feature.
    include_charges_ratio : bool, default False
        Whether to generate the continuous 'charges_ratio' feature.
    """

    def __init__(
        self,
        include_tenure_group: bool = False,
        include_total_services: bool = False,
        include_tech_support_security: bool = False,
        include_auto_payment: bool = False,
        include_charges_ratio: bool = False,
    ):
        self.include_tenure_group = include_tenure_group
        self.include_total_services = include_total_services
        self.include_tech_support_security = include_tech_support_security
        self.include_auto_payment = include_auto_payment
        self.include_charges_ratio = include_charges_ratio
        self.feature_names_in_: list[str] = []

    def fit(self, X: pd.DataFrame, y=None):
        """Fit transformer (stateless transformation; registers input feature names)."""
        if not isinstance(X, pd.DataFrame):
            raise TypeError("FeatureEngineeringTransformer requires a pandas DataFrame input.")
        self.feature_names_in_ = list(X.columns)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply configured feature engineering transformations deterministically."""
        if not isinstance(X, pd.DataFrame):
            raise TypeError("FeatureEngineeringTransformer requires a pandas DataFrame input.")

        X_out = X.copy()

        if self.include_tenure_group:
            X_out["tenure_group"] = compute_tenure_group(X_out["tenure"])

        if self.include_total_services:
            X_out["total_services_subscribed"] = compute_total_services_subscribed(X_out)

        if self.include_tech_support_security:
            X_out["has_tech_support_or_security"] = compute_has_tech_support_or_security(X_out)

        if self.include_auto_payment:
            X_out["auto_payment_indicator"] = compute_auto_payment_indicator(X_out["PaymentMethod"])

        if self.include_charges_ratio:
            X_out["charges_ratio"] = compute_charges_ratio(X_out["MonthlyCharges"], X_out["TotalCharges"])

        return X_out

    def get_feature_names_out(self, input_features: Sequence[str] | None = None) -> list[str]:
        """Return output feature names after engineering."""
        base_features = list(input_features) if input_features is not None else list(self.feature_names_in_)
        engineered = []
        if self.include_tenure_group:
            engineered.append("tenure_group")
        if self.include_total_services:
            engineered.append("total_services_subscribed")
        if self.include_tech_support_security:
            engineered.append("has_tech_support_or_security")
        if self.include_auto_payment:
            engineered.append("auto_payment_indicator")
        if self.include_charges_ratio:
            engineered.append("charges_ratio")
        return base_features + engineered

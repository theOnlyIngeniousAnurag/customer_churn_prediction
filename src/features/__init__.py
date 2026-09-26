"""Features package initialization."""

from src.features.engineering import (
    FeatureEngineeringTransformer,
    compute_tenure_group,
    compute_total_services_subscribed,
    compute_has_tech_support_or_security,
    compute_auto_payment_indicator,
    compute_charges_ratio,
)
from src.features.preprocessing import (
    TotalChargesCleaner,
    build_column_transformer,
    build_pipeline,
    RAW_NUMERICAL_FEATURES,
    RAW_CATEGORICAL_FEATURES,
)
from src.features.ablation import run_feature_ablation

__all__ = [
    "FeatureEngineeringTransformer",
    "compute_tenure_group",
    "compute_total_services_subscribed",
    "compute_has_tech_support_or_security",
    "compute_auto_payment_indicator",
    "compute_charges_ratio",
    "TotalChargesCleaner",
    "build_column_transformer",
    "build_pipeline",
    "RAW_NUMERICAL_FEATURES",
    "RAW_CATEGORICAL_FEATURES",
    "run_feature_ablation",
]

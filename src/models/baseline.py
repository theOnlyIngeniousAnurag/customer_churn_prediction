"""Logistic Regression baseline model definition and pipeline assembly.

Provides standard, transparent Logistic Regression baseline configuration:
    - max_iter = 1000
    - random_state = 42
    - solver = 'lbfgs' (default)
    - penalty = 'l2' (default)
    - C = 1.0 (default)
Strictly adheres to internship technology constraints (scikit-learn only).
No hyperparameter tuning, grid search, or regularization tuning is performed.
"""

import sys
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.features.preprocessing import build_pipeline


def get_baseline_model(
    random_state: int = 42,
    max_iter: int = 1000
) -> LogisticRegression:
    """Create un-tuned baseline Logistic Regression classifier.

    Parameters
    ----------
    random_state : int, default 42
        Reproducibility seed.
    max_iter : int, default 1000
        Maximum iterations to ensure numerical convergence.

    Returns
    -------
    LogisticRegression
        Configured baseline model.
    """
    return LogisticRegression(
    penalty="l2",
    C=1.0,
    max_iter=max_iter,
    random_state=random_state
)


def build_baseline_pipeline(
    feature_set: str = "baseline",
    random_state: int = 42,
    max_iter: int = 1000
) -> Pipeline:
    """Construct complete end-to-end baseline pipeline.

    Connects:
        Raw DataFrame -> TotalChargesCleaner -> (FeatureEngineering if requested)
                      -> ColumnTransformer -> LogisticRegression

    Parameters
    ----------
    feature_set : str, default 'baseline'
        Feature configuration ('baseline' for 19 raw features,
        or 'b1_tenure_group' for candidate validation).
    random_state : int, default 42
        Reproducibility seed for model.
    max_iter : int, default 1000
        Maximum iterations for logistic regression convergence.

    Returns
    -------
    Pipeline
        Full scikit-learn Pipeline.
    """
    model = get_baseline_model(random_state=random_state, max_iter=max_iter)
    return build_pipeline(feature_set=feature_set, classifier=model)

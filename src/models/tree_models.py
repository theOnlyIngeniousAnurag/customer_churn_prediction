"""Tree-based model definitions and pipeline builders for Phase 5 Benchmarking.

This module encapsulates:
- DecisionTreeClassifier baseline (random_state=42, un-tuned)
- RandomForestClassifier baseline (n_estimators=300, random_state=42, n_jobs=-1, un-tuned)
- Pipeline construction integrating TotalChargesCleaner, ColumnTransformer, and classifiers
"""

from typing import Any, Dict, Literal
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from src.features.preprocessing import build_pipeline


def get_decision_tree_model(random_state: int = 42) -> DecisionTreeClassifier:
    """Instantiate a DecisionTreeClassifier with baseline configuration.

    Parameters
    ----------
    random_state : int, default=42
        Random seed for reproducible split selections.

    Returns
    -------
    DecisionTreeClassifier
        Un-tuned baseline Decision Tree classifier.
    """
    return DecisionTreeClassifier(random_state=random_state)


def get_random_forest_model(
    n_estimators: int = 300,
    random_state: int = 42,
    n_jobs: int = -1
) -> RandomForestClassifier:
    """Instantiate a RandomForestClassifier with baseline configuration.

    Parameters
    ----------
    n_estimators : int, default=300
        Number of trees in the forest.
    random_state : int, default=42
        Random seed for reproducible bootstrapping and feature subsampling.
    n_jobs : int, default=-1
        Number of CPU cores to use.

    Returns
    -------
    RandomForestClassifier
        Un-tuned baseline Random Forest classifier.
    """
    return RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=n_jobs
    )


def build_tree_pipeline(
    model_type: Literal["decision_tree", "random_forest"] = "decision_tree",
    feature_set: Literal["baseline", "b1_tenure_group"] = "baseline",
    random_state: int = 42,
    n_estimators: int = 300,
    n_jobs: int = -1
) -> Pipeline:
    """Build a complete scikit-learn pipeline for tree-based models.

    Parameters
    ----------
    model_type : {"decision_tree", "random_forest"}, default="decision_tree"
        Type of tree classifier to include in the pipeline.
    feature_set : {"baseline", "b1_tenure_group"}, default="baseline"
        Feature configuration to transform.
    random_state : int, default=42
        Random seed for classifier.
    n_estimators : int, default=300
        Number of trees if model_type is "random_forest".
    n_jobs : int, default=-1
        CPU parallelism if model_type is "random_forest".

    Returns
    -------
    Pipeline
        Assembled pipeline ready for fitting on training folds.
    """
    if model_type == "decision_tree":
        classifier = get_decision_tree_model(random_state=random_state)
    elif model_type == "random_forest":
        classifier = get_random_forest_model(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=n_jobs
        )
    else:
        raise ValueError(f"Unsupported model_type: {model_type}. Expected 'decision_tree' or 'random_forest'.")

    return build_pipeline(
        feature_set=feature_set,
        classifier=classifier
    )

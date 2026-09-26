"""Data ingestion and loading module."""

from pathlib import Path
import pandas as pd


def load_raw_dataset(path: Path | str = "data/raw/Telco-Customer-Churn.csv") -> pd.DataFrame:
    """Load the raw customer dataset from the specified path without altering original storage.

    Parameters
    ----------
    path : Path or str
        Path to the raw CSV dataset.

    Returns
    -------
    pd.DataFrame
        Loaded raw customer DataFrame.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {file_path}")

    df = pd.read_csv(file_path)
    return df


def prepare_target(
    df: pd.DataFrame,
    target_col: str = "Churn",
    id_col: str = "customerID"
) -> tuple[pd.DataFrame, pd.Series]:
    """Isolate prediction target and administrative identifier from predictive features.

    Applies deterministic binary mapping:
        'No'  -> 0 (retained customer)
        'Yes' -> 1 (churned customer)

    Parameters
    ----------
    df : pd.DataFrame
        Raw or cleaned customer DataFrame.
    target_col : str, default 'Churn'
        Name of the target column.
    id_col : str, default 'customerID'
        Name of the customer identifier column to exclude.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series]
        X: Feature matrix with id_col and target_col excluded.
        y: Integer target Series (0 or 1).
    """
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame.")
    if id_col not in df.columns:
        raise KeyError(f"Identifier column '{id_col}' not found in DataFrame.")

    raw_target = df[target_col]

    # Verify target domain validity
    unique_vals = set(raw_target.dropna().unique())
    expected_vals = {"No", "Yes"}
    if not unique_vals.issubset(expected_vals):
        unexpected = unique_vals - expected_vals
        raise ValueError(f"Unexpected target values detected: {unexpected}")

    if raw_target.isna().any():
        raise ValueError(f"Missing values detected in target column '{target_col}'.")

    # Deterministic mapping
    target_mapping = {"No": 0, "Yes": 1}
    y = raw_target.map(target_mapping).astype("int64")
    y.name = target_col

    # Feature matrix: strictly exclude identifier and target
    X = df.drop(columns=[id_col, target_col]).copy()

    return X, y


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Partition features and target into reproducible stratified train and test sets.

    Parameters
    ----------
    X : pd.DataFrame
        Predictive feature matrix.
    y : pd.Series
        Target vector.
    test_size : float, default 0.2
        Proportion of dataset to reserve for isolated final test evaluation.
    random_state : int, default 42
        Reproducibility seed.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        X_train, X_test, y_train, y_test
    """
    from sklearn.model_selection import train_test_split

    if len(X) != len(y):
        raise ValueError(f"X length ({len(X)}) must match y length ({len(y)}).")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    if len(X_train) + len(X_test) != len(X):
        raise AssertionError("Train and test row counts do not sum to total dataset length.")

    return X_train, X_test, y_train, y_test

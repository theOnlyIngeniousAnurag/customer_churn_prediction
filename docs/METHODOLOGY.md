# Machine Learning Methodology

## Customer Churn Prediction & Retention Intelligence System

### 1. Methodology Overview

This document details the machine learning methodology employed in developing the Customer Churn Prediction & Retention Intelligence System. The system formulates customer churn prediction as a supervised binary classification task over tabular customer account and service attributes.

```text
Raw Dataset (7,043 rows)
           │
           ▼
Stratified 80/20 Partition (5,634 Train / 1,409 Test)
           │
           ├──► Preprocessing Pipeline (Median Imputation + Standard Scaling + One-Hot Encoding)
           │            │
           │            ▼
           ├──► Model Experimentation & Cross-Validation (5-Fold Stratified CV)
           │     ├── Logistic Regression Baseline (CV ROC-AUC: 0.8436)
           │     ├── Decision Tree Baseline (CV ROC-AUC: 0.6568)
           │     └── Random Forest Benchmark & Tuning (CV ROC-AUC: 0.8459)
           │            │
           │            ▼
           └──► Selected Candidate: Optimized Random Forest Classifier
                        │
                        ▼
           Locked Final Holdout Evaluation (N = 1,409)
                        │
                        ▼
           Explainability & Portfolio Risk Ranking Integration
```

---

### 2. Dataset Partitioning & Leakage Prevention Strategy

To strictly prevent data leakage and guarantee valid out-of-sample evaluation:

1. **Stratified Split:** The raw dataset of 7,043 customer records was partitioned into an 80% training set (5,634 records) and a 20% holdout test set (1,409 records) using stratified sampling on the binary target (`Churn`).
2. **Deterministic Seed:** All random state operations are locked to `random_state = 42`.
3. **Strict Target Isolation:** `customerID` (administrative identifier) and `Churn` (target label) were removed prior to feature transformations.
4. **Stateful Preprocessing Fit:** All stateful transformation parameters—including median imputation values for numeric fields, numeric scaling means and standard deviations (`StandardScaler`), and categorical category levels (`OneHotEncoder`)—were fitted strictly on the 5,634 training records. The test set was transformed using only parameters learned from training.

---

### 3. Data Cleaning & Preprocessing Pipeline

* **Handling Whitespace Values:** 11 records in `TotalCharges` contained blank whitespace strings (`" "`). These corresponded strictly to new customer registrations where `tenure == 0`. A custom transformer (`TotalChargesCleaner`) converted these strings to `NaN` and applied median imputation learned strictly from the training fold.
* **Categorical Feature Encoding:** Categorical attributes were encoded using `OneHotEncoder(handle_unknown='ignore', drop='first')`, generating binary indicator columns for non-numeric service and contract types. Unknown category levels during inference are encoded safely as all-zero vectors.
* **Numerical Scaling:** Numerical attributes (`tenure`, `MonthlyCharges`, `TotalCharges`) were scaled using `StandardScaler` fitted on training data.

The final preprocessor outputs 30 transformed features (3 scaled numericals + 27 one-hot-encoded binary indicators).

---

### 4. Feature Engineering & Ablation Analysis

A systematic feature ablation study evaluated engineered candidate features against the core raw feature baseline on 5-fold stratified cross-validation over the training set:

* **`tenure_group`**: Lifecycle binning (`[0-12, 13-24, 25-48, 49-72]` months). Included as an evaluated candidate.
* **`total_services_subscribed`**: Integer sum of active catalog services. Excluded due to redundancy with individual service indicators.
* **`has_tech_support_or_security`**: Binary flag for high-retention assistance services. Excluded due to collinearity with direct service flags.
* **`auto_payment_indicator`**: Indicator for automatic payment methods (Bank transfer / Credit card). Excluded as redundant with `PaymentMethod`.
* **`charges_ratio`**: Ratio of monthly to total charges. Excluded due to redundancy with raw billing attributes.

---

### 5. Model Development Lifecycle

The model development journey proceeded sequentially across model families:

1. **Logistic Regression Baseline:** Evaluated as a linear parametric baseline (`max_iter=1000`, `C=1.0`, `L2` regularization). Achieved mean CV ROC-AUC of `0.8436 ± 0.0126` and PR-AUC of `0.6508 ± 0.0194`.
2. **Decision Tree Classifier:** Evaluated as an unconstrained non-parametric baseline (`random_state=42`). Overfit significantly (tree depth 23, 1,097 leaves), yielding a mean CV ROC-AUC of `0.6568 ± 0.0162`.
3. **Random Forest Ensemble:** Evaluated as an un-tuned ensemble (`n_estimators=300`), achieving a mean CV ROC-AUC of `0.8260 ± 0.0117`.
4. **Hyperparameter Optimization:** Applied `RandomizedSearchCV` over 50 iterations with 5-fold stratified cross-validation on the training set to optimize tree depth, leaf sample limits, split constraints, and feature subsampling.

---

### 6. Selected Candidate Configuration

The hyperparameter optimization yielded the selected candidate model:

```python
RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_leaf=2,
    min_samples_split=2,
    max_features="sqrt",
    random_state=42,
    n_jobs=-1
)
```

The tree depth constraint (`max_depth=8`) and minimum leaf size (`min_samples_leaf=2`) eliminated variance over-fitting while preserving non-linear interactions among tenure, billing charges, and contract types.

---

### 7. Explainability & Risk Scoring Architecture

* **Global Model Explainability:** Native Random Forest mean decrease in Gini impurity was computed across all estimators to quantify global feature contributions.
* **Customer-Level Review Reasons:** Deterministic, evidence-based review reasons were extracted from observed customer attributes (e.g., month-to-month contract type, fiber optic internet, electronic check payment method, short tenure) to provide interpretable context for retention teams.
* **Risk Categorization:** Predicted churn probabilities `P(Churn = Yes)` are grouped into four operational risk bands:
  * **Low Risk:** `P < 0.30`
  * **Medium Risk:** `0.30 <= P < 0.50`
  * **High Risk:** `0.50 <= P < 0.70`
  * **Very High Risk:** `P >= 0.70`

# Dataset & Data Strategy

## Customer Churn Prediction & Retention Intelligence System

**Project:** Machine Learning Internship Capstone — Project 1
**Document:** Dataset & Data Strategy
**Version:** 1.0
**Status:** Planning
**Author:** Anurag
**Target Completion:** 30 September 2026

---

# 1. Purpose of This Document

This document defines how the dataset for the Customer Churn Prediction project will be:

* Selected
* Acquired
* Verified
* Stored
* Inspected
* Cleaned
* Transformed
* Split
* Validated
* Feature-engineered
* Documented
* Used for model development
* Used for final evaluation

The purpose is to ensure that the machine-learning results are technically credible, reproducible, and free from avoidable data-quality and leakage problems.

The dataset strategy must be established before substantial model development begins.

---

# 2. Dataset Selection Principle

The selected dataset must be:

1. Real and legitimately obtainable.
2. Relevant to customer churn prediction.
3. Sufficiently documented.
4. Appropriate for supervised binary classification.
5. Large and diverse enough to support meaningful experimentation where possible.
6. Rich enough to support the internship requirements.
7. Legally/ethically appropriate for educational and portfolio use.
8. Reproducible for another person following the project documentation.

The dataset must not be fabricated.

Synthetic data should not be used as the primary dataset unless a genuine dataset cannot reasonably satisfy the project requirements and its use is explicitly justified and documented.

---

# 3. Dataset Selection Criteria

Candidate datasets should be evaluated using the following criteria.

| Criterion                        |  Importance | Requirement                      |
| -------------------------------- | ----------: | -------------------------------- |
| Churn target available           |    Critical | Must have                        |
| Customer-level observations      |    Critical | Must have                        |
| Relevant customer attributes     |        High | Preferred                        |
| Tenure information               |        High | Preferred                        |
| Usage/activity information       |        High | Preferred                        |
| Billing/subscription information |        High | Preferred                        |
| Support/service information      | Medium–High | Preferred                        |
| Categorical features             |        High | Preferred                        |
| Numerical features               |        High | Preferred                        |
| Sufficient observations          |        High | Required for meaningful modeling |
| Documentation                    |        High | Required                         |
| Legitimate source                |    Critical | Required                         |
| Reproducibility                  |        High | Required                         |
| Portfolio suitability            |      Medium | Preferred                        |

The internship PDF describes demographics, tenure, usage, support interactions, and billing history as the desired data categories. The actual dataset may not contain every category. Missing categories must be explicitly documented rather than artificially created.

---

# 4. Dataset Decision Rule

The dataset must not be selected simply because it produces a high model score.

The selection decision should consider:

```text
Business Relevance
        +
Data Quality
        +
Feature Richness
        +
Documentation
        +
Reproducibility
        +
ML Suitability
        +
Portfolio Value
```

A dataset with slightly lower predictive performance but substantially better documentation and business relevance may be preferable to a dataset that produces a higher score for unclear reasons.

---

# 5. Dataset Candidate Evaluation

Before finalizing the dataset, candidate datasets should be inspected using a common checklist.

For every serious candidate, record:

* Dataset name
* Source
* URL/reference
* License/usage information where available
* Number of rows
* Number of columns
* Target variable
* Target distribution
* Numerical features
* Categorical features
* Missing values
* Duplicate records
* Potential leakage variables
* Relevant customer information
* Dataset limitations

A simple candidate comparison should be maintained.

Example:

| Dataset                        | Rows | Columns | Churn Target | Feature Richness | Documentation | Leakage Risk | Decision |
| ------------------------------ | ---: | ------: | ------------ | ---------------- | ------------- | ------------ | -------- |
| IBM Telco Customer Churn       | 7043 |      21 | Yes ('Churn')| High (20 feats)  | Official IBM  | None detected| SELECTED |

---

# 6. Recommended Dataset Characteristics

The selected dataset contains a verified mixture of:

### Numerical Variables

* `tenure`: Customer tenure in months (range: 0–72, median: 29.0)
* `MonthlyCharges`: Monthly subscription charges in USD (range: 18.25–118.75, median: 70.35)
* `TotalCharges`: Cumulative charges in USD (parsed float range: 18.80–8684.80; 11 blank spaces for tenure=0 new signups)

### Categorical Variables

* **Demographics (4)**: `gender` (Female, Male), `SeniorCitizen` (0, 1), `Partner` (Yes, No), `Dependents` (No, Yes)
* **Phone Services (2)**: `PhoneService` (No, Yes), `MultipleLines` (No phone service, No, Yes)
* **Internet Services (7)**: `InternetService` (DSL, Fiber optic, No), `OnlineSecurity` (No, Yes, No internet service), `OnlineBackup` (Yes, No, No internet service), `DeviceProtection` (No, Yes, No internet service), `TechSupport` (No, Yes, No internet service), `StreamingTV` (No, Yes, No internet service), `StreamingMovies` (No, Yes, No internet service)
* **Contract & Account (3)**: `Contract` (Month-to-month, One year, Two year), `PaperlessBilling` (Yes, No), `PaymentMethod` (Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic))

### Target Variable

Binary churn indicator:
* Column: `Churn`
* Values: `No` (5,174, 73.46%), `Yes` (1,869, 26.54%)
* Class Imbalance Ratio: 2.77:1

---

# 7. Dataset Source Documentation

```text
Dataset Name: IBM Telco Customer Churn
Source: IBM Business Analytics Community / Telco Customer Churn on ICP4D
Publisher/Organization: IBM Corporation
Original URL: https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv
Access Date: 2026-09-26
License / Usage Information: Public domain / Apache 2.0 (IBM Community Sample Dataset)
File Format: CSV (UTF-8)
Dataset Dimensions: 7,043 rows x 21 columns
Target Variable: Churn ('No', 'Yes')
Known Limitations: Cross-sectional customer snapshot; lacks exact support interaction timestamps. TotalCharges has 11 unbilled entries for new accounts (tenure=0).
```

---

# 8. Data Storage Strategy

The project should separate raw and processed data.

Recommended structure:

```text
data/
│
├── raw/
│   └── original_dataset.*
│
├── interim/
│   └── cleaned_intermediate_data.*
│
└── processed/
    └── model_ready_data.*
```

## Raw Data

Contains the original downloaded dataset.

The raw dataset should not be overwritten by preprocessing scripts.

## Interim Data

Contains intermediate transformations when saving them is useful.

## Processed Data

Contains data prepared for downstream analysis/modeling.

Not every project requires all three levels to be physically stored. The structure should be adapted to the actual workflow.

---

# 9. Raw Data Preservation

The original dataset must remain unchanged.

Do not:

* Overwrite the source file
* Manually modify the raw file
* Delete original columns from the raw data
* Apply transformations directly to the original dataset

All transformations should be performed programmatically.

This makes the project reproducible.

---

# 10. Initial Dataset Audit

Immediately after loading the dataset, perform a structured audit.

The audit should establish:

### Dataset Shape

```text
Rows: 7,043
Columns: 21
```

### Data Types

* Integer: `SeniorCitizen` (int64)
* Float: `tenure` (int64/float), `MonthlyCharges` (float64), `TotalCharges` (object in raw CSV due to whitespace, parsed to float64)
* Categorical/Object (17): `customerID`, `gender`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `Churn`
* Identifier: `customerID` (7,043 unique, 0 duplicates)

### Target

* Column: `Churn`
* Data Type: `object`
* Unique Values: `['No', 'Yes']`
* Class Distribution:
  - `No`: 5,174 (73.46%)
  - `Yes`: 1,869 (26.54%)
* Imbalance Ratio: 2.77:1

### Missingness

* Explicit `NaN` counts: 0 across all 21 columns
* Implicit Whitespace strings: 11 in `TotalCharges` (`" "`). All 11 correspond to new signups with `tenure == 0`.

### Duplicates

* Exact duplicate rows: 0
* Duplicate customer identifiers: 0

---

# 11. Data Dictionary

| Column | Type | Category | Description | Missing (Raw) | Role / Modeling Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customerID` | string | Identifier | Unique customer identifier | 0 | Identifier (Exclude from model features) |
| `gender` | categorical | Demographics | Male / Female | 0 | Predictive Feature (One-hot encode) |
| `SeniorCitizen` | binary | Demographics | 1 = Yes, 0 = No | 0 | Predictive Feature (Binary indicator) |
| `Partner` | binary | Demographics | Whether customer has a partner (Yes, No) | 0 | Predictive Feature (One-hot encode) |
| `Dependents` | binary | Demographics | Whether customer has dependents (Yes, No) | 0 | Predictive Feature (One-hot encode) |
| `tenure` | integer | Behavioral | Months the customer has stayed with company [0-72] | 0 | Predictive Feature (Standardize / Bin) |
| `PhoneService` | binary | Service | Whether customer has phone service (Yes, No) | 0 | Predictive Feature (One-hot encode) |
| `MultipleLines` | categorical | Service | Multiple phone lines (No, Yes, No phone service) | 0 | Predictive Feature (One-hot encode) |
| `InternetService` | categorical | Service | Internet provider (DSL, Fiber optic, No) | 0 | Predictive Feature (One-hot encode) |
| `OnlineSecurity` | categorical | Service | Online security add-on (Yes, No, No internet) | 0 | Predictive Feature (One-hot encode) |
| `OnlineBackup` | categorical | Service | Online backup add-on (Yes, No, No internet) | 0 | Predictive Feature (One-hot encode) |
| `DeviceProtection`| categorical | Service | Device protection plan (Yes, No, No internet) | 0 | Predictive Feature (One-hot encode) |
| `TechSupport` | categorical | Support | Premium tech support (Yes, No, No internet) | 0 | Predictive Feature (One-hot encode) |
| `StreamingTV` | categorical | Service | Streaming TV service (Yes, No, No internet) | 0 | Predictive Feature (One-hot encode) |
| `StreamingMovies`| categorical | Service | Streaming movies service (Yes, No, No internet) | 0 | Predictive Feature (One-hot encode) |
| `Contract` | categorical | Account | Contract term (Month-to-month, One year, Two year) | 0 | Predictive Feature (One-hot encode) |
| `PaperlessBilling`| binary | Billing | Paperless billing (Yes, No) | 0 | Predictive Feature (One-hot encode) |
| `PaymentMethod` | categorical | Billing | Payment method (4 options) | 0 | Predictive Feature (One-hot encode) |
| `MonthlyCharges` | float | Billing | Current monthly charge amount in USD [18.25-118.75]| 0 | Predictive Feature (Standardize / Transform)|
| `TotalCharges` | float | Billing | Total cumulative charges in USD [18.80-8684.80] | 11 (blanks) | Predictive Feature (Impute 0.0 or median) |
| `Churn` | binary | Target | Whether customer churned (Yes, No) | 0 | **Target Variable** (Map Yes=1, No=0) |

---

# 12. Identifier Handling

Customer identifiers generally should not be used directly as predictive features.

Examples:

* Customer ID
* Account number
* Record ID
* UUID

These should normally be retained for:

* Customer-level output
* Ranking
* Traceability
* Application display

but excluded from model features unless there is a documented technical reason to use them.

An identifier that accidentally correlates with the target can create misleading model performance.

---

# 13. Target Validation

The target variable must be investigated before any model training.

Check:

1. Column name
2. Data type
3. Unique values
4. Missing values
5. Class counts
6. Class percentages
7. Unexpected labels
8. Encoding

Example:

```text
Unique target values:
- Yes
- No
```

may need to become:

```text
Yes → 1
No  → 0
```

The mapping must be explicitly documented.

---

# 14. Class Distribution

Calculate:

```text
Number of churned customers
Number of non-churned customers
Churn percentage
Non-churn percentage
Class ratio
```

Visualize the target distribution.

If the target is imbalanced, the imbalance must influence:

* Model selection
* Cross-validation strategy
* Metrics
* Class weighting
* Threshold analysis
* Error analysis

---

# 15. Missing-Value Strategy

Missing values must be analyzed before choosing an imputation strategy.

For each feature with missing values, investigate:

* Missing count
* Missing percentage
* Potential reason for missingness
* Whether missingness itself may contain useful information
* Whether the column is important
* Whether the feature should be retained

Possible strategies include:

### Numerical

* Median imputation
* Mean imputation where justified
* Model-based imputation where justified

### Categorical

* Most-frequent category
* Explicit "Unknown" category

### Removal

Remove a feature only when missingness is sufficiently severe or the feature has limited value.

Do not automatically remove every row containing a missing value.

---

# 16. Leakage-Safe Imputation

Imputation must be fitted using training data only.

Incorrect:

```text
Entire Dataset
      ↓
Calculate Median
      ↓
Fill Missing Values
      ↓
Train/Test Split
```

Correct:

```text
Raw Dataset
      ↓
Train/Test Split
      ↓
Fit Imputer on Training Data
      ↓
Transform Training Data
      ↓
Transform Test Data
```

The same principle applies to:

* Scaling
* Encoding
* Feature selection
* Other learned preprocessing

Where possible, use scikit-learn pipelines to enforce this behavior.

---

# 17. Duplicate Strategy

Investigate both:

### Exact duplicates

Identical rows.

### Customer-level duplicates

Multiple rows associated with the same customer identifier.

Duplicates should not automatically be deleted.

First determine whether multiple rows represent:

* Duplicate records
* Legitimate repeated observations
* Different transactions
* Multiple service records
* Historical snapshots

The correct treatment depends on the dataset's structure.

---

# 18. Outlier Strategy

Outliers must be investigated rather than automatically removed.

Potential methods:

* IQR analysis
* Percentile analysis
* Distribution plots
* Domain plausibility checks
* Z-score where appropriate

An observation may be:

1. A valid extreme customer.
2. A data-entry error.
3. A measurement anomaly.
4. A legitimate business event.

Only justified cases should be removed or transformed.

Tree-based models may tolerate some outliers naturally, while linear models may be more sensitive.

---

# 19. Categorical Data Strategy

Categorical variables must be inspected for:

* Number of unique categories
* Rare categories
* Missing categories
* Inconsistent spelling
* Inconsistent capitalization
* Unexpected values

Potential preprocessing methods include:

### One-Hot Encoding

Appropriate for many low/moderate-cardinality categorical variables.

### Other Encoding

Only use alternative encodings when there is a clear technical reason.

Categorical preprocessing should be performed within the modeling pipeline whenever possible.

---

# 20. Numerical Feature Strategy

Numerical variables should be inspected for:

* Data type
* Range
* Missing values
* Outliers
* Skewness
* Near-zero variance
* Constant values
* Suspicious values

Scaling may be required for models such as Logistic Regression.

Tree-based models generally do not require feature scaling.

This difference should be respected when constructing model pipelines.

---

# 21. Feature Leakage Audit (Phase 2 Deep Audit)

Every feature was audited against prediction-time availability, target derivation, and proxy risks:

| Feature | Available at prediction time? | Target-derived? | Post-outcome information? | Suspicious proxy? | Decision | Rationale |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `customerID` | Yes | No | No | Yes | **EXCLUDE** | High-cardinality unique customer identifier. Would lead to arbitrary overfitting; carries no behavioral generalizability. |
| `gender` | Yes | No | No | No | **KEEP** | Demographic attribute known at sign-up. Safe. |
| `SeniorCitizen` | Yes | No | No | No | **KEEP** | Demographic indicator known at sign-up. Safe. |
| `Partner` | Yes | No | No | No | **KEEP** | Demographic account status. Safe. |
| `Dependents` | Yes | No | No | No | **KEEP** | Demographic account status. Safe. |
| `tenure` | Yes | No | No | No | **KEEP** | Elapsed duration in months as an active account prior to prediction point. Safe. |
| `PhoneService` | Yes | No | No | No | **KEEP** | Active subscribed service catalog entry. Safe. |
| `MultipleLines` | Yes | No | No | No | **KEEP** | Active subscribed service catalog entry. Safe. |
| `InternetService` | Yes | No | No | No | **KEEP** | Active subscribed service catalog entry (DSL, Fiber, None). Safe. |
| `OnlineSecurity` | Yes | No | No | No | **KEEP** | Active add-on service. Safe. |
| `OnlineBackup` | Yes | No | No | No | **KEEP** | Active add-on service. Safe. |
| `DeviceProtection` | Yes | No | No | No | **KEEP** | Active add-on service. Safe. |
| `TechSupport` | Yes | No | No | No | **KEEP** | Active technical assistance entitlement. Safe. |
| `StreamingTV` | Yes | No | No | No | **KEEP** | Active entertainment add-on. Safe. |
| `StreamingMovies` | Yes | No | No | No | **KEEP** | Active entertainment add-on. Safe. |
| `Contract` | Yes | No | No | No | **KEEP** | Billing contract commitment tier at observation time. Safe. |
| `PaperlessBilling` | Yes | No | No | No | **KEEP** | Billing delivery preference. Safe. |
| `PaymentMethod` | Yes | No | No | No | **KEEP** | Account payment method. Safe. |
| `MonthlyCharges` | Yes | No | No | No | **KEEP** | Current monthly recurring billing rate. Safe. |
| `TotalCharges` | Yes | No | No | No | **KEEP** | Historical cumulative charges accrued up to prediction time. Blank for tenure=0 to be imputed as 0.0. Safe. |
| `Churn` | No | Yes | Yes | Yes | **TARGET** | Ground truth binary outcome variable. Separated as target vector y. |

---

# 22. Prediction-Time / Temporal Limitation & Availability

The IBM Telco Customer Churn dataset is a **cross-sectional customer-level benchmark snapshot**. It does not provide a genuine timestamped longitudinal event sequence establishing:

```text
Information available at T
        ↓
Future observation period
        ↓
Churn event
```

Therefore, the system must **not be overstated as a true prospective or time-to-future churn prediction system**. 

### Interpretation of `TotalCharges`
`TotalCharges` represents cumulative historical charges present in the supplied customer snapshot. While it is retained as a candidate predictor for modeling, its presence does **not** constitute proof of a strictly enforced future-only prediction window. Temporal leakage cannot be ruled out completely merely from column naming.

```text
Cross-Sectional Benchmark Snapshot
      │
      ├── Customer Demographics (gender, SeniorCitizen, Partner, Dependents)
      ├── Tenured duration at snapshot (tenure in months)
      ├── Active subscribed services at snapshot (Internet, Phone, TechSupport, etc.)
      ├── Billing configuration at snapshot (Contract, PaymentMethod, MonthlyCharges)
      └── Cumulative historical charges at snapshot (TotalCharges)
             │
             └── Co-occurring status indicator (Churn) ──► Target Outcome [0, 1]
```

---

# 23. Feature Engineering Strategy & Feasibility Audit

Feature engineering in Phase 3 must adhere to a strict **empirical ablation protocol**. Features are not automatically approved; candidate features must be compared against a pure baseline of original verified features:

```text
Experiment A
Original verified features (19 cleaned baseline predictors)
        ↓
Baseline Performance

Experiment B
Original features + candidate engineered feature(s)
        ↓
Ablation Evaluation vs Experiment A
```

Only retain engineered features when their inclusion provides a meaningful, defensible, and statistically verified benefit without introducing unnecessary complexity.

### Candidate Feature Audit & Suitability Matrix

| Feature | Formula | Information source | Potential redundancy | Leakage risk | Business interpretation | Phase 3 status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tenure_group` | Categorical binning: `[0-12, 13-24, 25-48, 49-72 mos]` | `tenure` | High correlation with continuous `tenure`. Tree ensembles partition `tenure` directly; binning primarily benefits linear models capturing non-linear hazard steps. | None (deterministic transformation of snapshot tenure). | Segments lifecycle phase (early onboarding danger zone vs mature loyalty). | **APPROVED FOR EXPERIMENT** |
| `charges_ratio` | `MonthlyCharges / (TotalCharges + 1.0)` | `MonthlyCharges`, `TotalCharges` | High redundancy with `tenure`. Since `TotalCharges ≈ tenure * MonthlyCharges`, the ratio approximates `1 / (tenure + 1 / MonthlyCharges)`. The `+1.0` denominator smoothing offset prevents division by zero for `tenure = 0` but introduces an arbitrary non-linear distortion for low spenders. | Low direct leakage, but questionable prospective validity given snapshot nature of dataset. | Unverified hypothesis: conjectured to capture recent billing increases or plan upgrades, but cannot be validated without longitudinal invoice deltas. | **CANDIDATE — VALIDATE** |
| `total_services_subscribed` | Integer sum of 9 distinct active service components (range: 1 to 9): `(PhoneService == 'Yes') + (MultipleLines == 'Yes') + (InternetService != 'No') + (OnlineSecurity == 'Yes') + (OnlineBackup == 'Yes') + (DeviceProtection == 'Yes') + (TechSupport == 'Yes') + (StreamingTV == 'Yes') + (StreamingMovies == 'Yes')` | 9 service columns (`PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`) | Direct composite of 9 catalog features that are already individually one-hot encoded in the baseline. | None (active service entitlements in snapshot). | Product breadth and ecosystem depth; hypothesis that higher subscription count increases switching friction. | **APPROVED FOR EXPERIMENT** |
| `has_tech_support_or_security` | Binary flag: `1 if (TechSupport == 'Yes' or OnlineSecurity == 'Yes') else 0` | `TechSupport`, `OnlineSecurity` | Extremely high redundancy with its two constituent binary features (`TechSupport` and `OnlineSecurity`); may offer no incremental signal beyond baseline one-hot encoding. | None. | Assistance and security umbrella; accounts with technical/security assistance exhibit lower observed churn rates in the snapshot. | **CANDIDATE — VALIDATE** |
| `auto_payment_indicator` | Binary flag: `1 if 'automatic' in PaymentMethod else 0` (aggregates Bank transfer and Credit card automatic payments) | `PaymentMethod` | Partially redundant with one-hot encoded `PaymentMethod` categories; tests whether collapsing automatic payment channels regularizes linear models. | None. | Automated recurring billing vs manual payment action (Electronic check, Mailed check). | **APPROVED FOR EXPERIMENT** |
| `support_contact_frequency` | N/A | N/A (Timestamped ticket logs not present) | N/A | N/A | Customer service friction and complaint volume. | **EXCLUDE** *(Documented limitation)* |
| `usage_trend_delta` | N/A | N/A (Monthly gigabytes/minutes time-series not present) | N/A | N/A | Decaying usage trend preceding cancellation. | **EXCLUDE** *(Documented limitation)* |
| `recent_billing_change` | N/A | N/A (Previous billing period charge amounts not present) | N/A | N/A | Bill shock from pricing increases. | **EXCLUDE** *(Documented limitation)* |

---

# 24. Feature Engineering Restrictions

Do not create features that:

* Directly encode the target
* Use future information
* Duplicate the target
* Encode post-churn information
* Artificially improve performance
* Have no defensible business interpretation

Every important engineered feature should have a documented explanation.

---

# 25. Final Train/Test Split Specification (Verified in Phase 3)

The dataset is partitioned into an 80% training set and a 20% strictly isolated test set prior to fitting any preprocessing or feature engineering transformations:

```text
7,043 Verified Observations
          │
          ├── Stratified Split (test_size = 0.20, random_state = 42, stratify = y)
          │
          ├── Train Set: 5,634 rows (80.0%)
          │     ├── Churn = 0 (No):  4,139 (73.46%)
          │     └── Churn = 1 (Yes): 1,495 (26.54%)
          │     └── Role: Pipeline fitting, CV ablation, model training
          │
          └── Isolated Final Test Set: 1,409 rows (20.0%)
                ├── Churn = 0 (No):  1,035 (73.46%)
                └── Churn = 1 (Yes):   374 (26.54%)
                └── Role: Untouched until final model evaluation
```

### Strict Test Set Isolation Invariants
* The test set is **never** used for fitting imputers, encoders, or scalers.
* The test set is **never** inspected to guide feature engineering selection, hyperparameter tuning, or threshold choices.
* All test transformations strictly invoke `transform()` using fitted pipeline objects learned solely from training rows.

---

# 26. Preprocessing Architecture & TotalCharges Treatment

### TotalCharges Handling
1. **Whitespace Conversion:** The 11 whitespace string entries (`" "`) are parsed to missing values (`NaN`).
2. **Domain Semantic Rule:** All 11 whitespace entries correspond to accounts with `tenure == 0`. Because these customers have completed 0 billing cycles, their cumulative accrued charges to date is mathematically and semantically `$0.00`. The pipeline deterministically assigns `TotalCharges = 0.0` for `tenure == 0`.
3. **Leakage-Safe Fallback Imputation:** To guarantee production robustness against any unexpected missingness for accounts with `tenure > 0`, a fallback median imputer (`median_total_charges_ = 1,397.48`) is learned strictly during `fit()` on the training set and applied via `fillna()`.

### Feature Transformation Pipelines
* **Numerical Pipeline (`StandardScaler`):** Standardizes continuous features (`tenure`, `MonthlyCharges`, `TotalCharges`, and applicable numeric engineered features) to zero mean and unit variance.
* **Categorical Pipeline (`OneHotEncoder`):** Encodes the 16 categorical features with `drop='first'` (to eliminate perfect multicollinearity in linear models), `sparse_output=False`, and `handle_unknown='ignore'` (to safely map previously unseen inference categories to all zeros without pipeline crash).
* **Pipeline Composability:** Built using scikit-learn `Pipeline` and `ColumnTransformer` with full feature name traceability via `get_feature_names_out()`.

---

# 27. Cross-Validation & Feature Engineering Ablation Strategy

For comparing the baseline feature set against candidate engineered features, a **5-Fold Stratified Cross-Validation** protocol is executed exclusively on the training set:

```text
Training Set (5,634 rows)
          ↓
5-Fold Stratified Cross-Validation (StratifiedKFold, shuffle=True, random_state=42)
          ↓
Model: Logistic Regression (max_iter=1000, random_state=42)
          ↓
Controlled Ablation: Experiment A (Baseline) vs Experiments B1–B5 & C
```

### Empirical Ablation Outcomes (5-Fold CV on Training Set)
| Experiment | Configuration | ROC-AUC (mean ± std) | PR-AUC (mean ± std) | F1 (mean ± std) | Delta ROC-AUC vs Base | Recommendation |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Exp A (Baseline)** | 19 raw features | 0.8461 ± 0.0126 | 0.6615 ± 0.0194 | 0.5935 ± 0.0304 | baseline | **Retained as clean baseline benchmark** |
| **Exp B1** | + `tenure_group` | 0.8465 ± 0.0117 | 0.6651 ± 0.0134 | 0.5941 ± 0.0233 | +0.0004 | **Candidate for Phase 4** (Precision/PR-AUC lift) |
| **Exp B2** | + `total_services_subscribed` | 0.8461 ± 0.0126 | 0.6615 ± 0.0193 | 0.5935 ± 0.0304 | +0.0000 | **Redundant** (catalog items already one-hot encoded) |
| **Exp B3** | + `has_tech_support_or_security` | 0.8459 ± 0.0132 | 0.6612 ± 0.0199 | 0.5924 ± 0.0296 | -0.0002 | **Exclude** (multicollinear degradation) |
| **Exp B4** | + `auto_payment_indicator` | 0.8461 ± 0.0126 | 0.6614 ± 0.0193 | 0.5933 ± 0.0304 | +0.0000 | **Redundant** (PaymentMethod already one-hot encoded) |
| **Exp B5** | + `charges_ratio` | 0.8461 ± 0.0124 | 0.6617 ± 0.0192 | 0.5933 ± 0.0307 | +0.0000 | **Exclude** (inverse surrogate of tenure, zero lift) |
| **Exp C** | All candidates combined | 0.8464 ± 0.0121 | 0.6653 ± 0.0140 | 0.5963 ± 0.0280 | +0.0003 | **Marginal** (mostly driven by tenure_group) |

The number of folds should depend on:

* Dataset size
* Class distribution
* Computational budget

Cross-validation must be performed only on the training/development data.

The final test set must remain untouched.

---

# 28. Preprocessing Pipeline

Where appropriate, use a reproducible preprocessing pipeline.

Conceptual architecture:

```text
Raw Features
     ↓
Column Identification
     ↓
Numerical Pipeline
     ├── Imputation
     └── Scaling where required
     
Categorical Pipeline
     ├── Imputation
     └── Encoding
     
     ↓
Combined Feature Matrix
     ↓
Model
```

This should preferably be implemented using tools such as:

* `Pipeline`
* `ColumnTransformer`

from scikit-learn.

---

# 29. Model-Specific Preprocessing

Different models may require different preprocessing.

### Logistic Regression

Potentially requires:

* Imputation
* Encoding
* Scaling of numerical variables

### Decision Tree

Usually:

* Imputation
* Encoding

Scaling is generally unnecessary.

### Random Forest

Usually:

* Imputation
* Encoding

Scaling is generally unnecessary.

### Gradient Boosting / XGBoost

Requirements depend on the specific implementation and feature representation.

The final architecture should avoid unnecessary preprocessing.

---

# 30. Dataset Splitting and Feature Engineering Order

The following order should generally be followed:

```text
Raw Dataset
      ↓
Initial Data Audit
      ↓
Define Target
      ↓
Remove Obvious Non-Features
      ↓
Train/Test Split
      ↓
Training-Fitted Preprocessing
      ↓
Feature Engineering
      ↓
Model Training
      ↓
Validation
      ↓
Final Test Evaluation
```

Where feature engineering itself uses learned statistics, those statistics must also be derived from training data only.

The exact order may be adapted to the dataset.

---

# 31. Data Transformation Reproducibility

All significant transformations should be performed through code.

Avoid manually:

* Editing CSV values
* Deleting rows by hand
* Renaming categories manually
* Copying/pasting cleaned data
* Changing values directly in spreadsheets

If a transformation is necessary, encode it in the project pipeline.

---

# 32. Data Versioning

The project should record:

* Dataset source
* Download/access date
* Dataset filename
* Dataset version where available
* Relevant preprocessing version
* Important transformation changes

If Git Large File Storage or another data-versioning solution is unnecessary due to dataset size or project scope, do not introduce it merely for appearance.

---

# 33. Privacy and Sensitive Information

The project must not expose unnecessary personally identifiable information.

If the dataset contains:

* Names
* Phone numbers
* Email addresses
* Physical addresses
* Payment identifiers
* Other sensitive personal information

such information should not be included in public GitHub repositories unless explicitly permitted and appropriately anonymized.

Where possible, use anonymized customer identifiers.

---

# 34. Public Repository Data Rule

Before publishing the project to GitHub:

Check that:

* No private customer information is present.
* No API keys are present.
* No passwords are present.
* No authentication tokens are present.
* No private files are present.
* No unintended raw sensitive data is committed.

Use `.gitignore` appropriately.

---

# 35. Dataset Documentation in README

The final README should clearly explain:

### Dataset

* Dataset name
* Source
* General description
* Number of records/features where appropriate
* Target variable
* Important limitations

### Data Processing

* Missing-value treatment
* Encoding
* Feature engineering
* Splitting strategy
* Leakage prevention

Do not copy large portions of the original dataset documentation.

Provide appropriate attribution and references.

---

# 36. Dataset Limitations

The project must explicitly document dataset limitations.

Possible limitations may include:

* Small sample size
* Historical data
* Limited customer segments
* Missing usage information
* Missing support information
* Class imbalance
* Dataset-specific bias
* Limited temporal information
* Synthetic or benchmark nature, if applicable
* Lack of real business context

Only limitations actually applicable to the selected dataset should be reported.

---

# 37. Generalization Principle

A high test score on a benchmark dataset does not prove that the model will perform equally well in a real company.

The project must distinguish between:

**Dataset-level performance**

and:

**Real-world business performance**

Do not claim production effectiveness based solely on benchmark metrics.

---

# 38. Data Quality Gates

Before modeling begins, the dataset must pass the following checks.

### Gate 1 — Source

* [ ] Legitimate source identified
* [ ] Dataset documentation available
* [ ] Usage rights checked

### Gate 2 — Structure

* [ ] Dataset loads successfully
* [ ] Shape recorded
* [ ] Columns identified
* [ ] Data types inspected

### Gate 3 — Target

* [ ] Target identified
* [ ] Target encoding verified
* [ ] Missing target values investigated
* [ ] Class distribution calculated

### Gate 4 — Quality

* [ ] Missing values analyzed
* [ ] Duplicates investigated
* [ ] Outliers investigated
* [ ] Invalid values investigated
* [ ] High-cardinality features investigated

### Gate 5 — Leakage

* [ ] Potential leakage features identified
* [ ] Prediction-time availability considered
* [ ] Target-derived features removed
* [ ] Future information excluded

### Gate 6 — Modeling Readiness

* [ ] Train/test strategy defined
* [ ] Cross-validation strategy defined
* [ ] Preprocessing strategy defined
* [ ] Feature engineering strategy defined

Only after these gates are reasonably satisfied should substantial model experimentation begin.

---

# 39. Dataset Inspection Notebook

A dedicated notebook should preferably be created for initial dataset analysis.

Suggested name:

```text
notebooks/
└── 01_dataset_audit_and_eda.ipynb
```

It should contain:

1. Environment/imports
2. Dataset loading
3. Dataset metadata
4. Shape
5. Data types
6. Missing values
7. Duplicate analysis
8. Target analysis
9. Numerical analysis
10. Categorical analysis
11. Outlier analysis
12. Leakage investigation
13. Initial feature observations
14. Dataset limitations
15. Conclusions

This notebook should remain analytical rather than becoming the entire production pipeline.

---

# 40. Data Preparation Scripts

Where appropriate, reusable data-processing logic should live in `src/`.

Possible structure:

```text
src/
└── data/
    ├── __init__.py
    ├── load_data.py
    ├── validate_data.py
    └── preprocessing.py
```

The exact structure may be simplified if the dataset/project does not justify multiple modules.

---

# 41. Processed Dataset Policy

A processed dataset may be saved when it improves reproducibility or efficiency.

However:

* The transformation process must remain reproducible.
* The processed dataset must not become the only source of truth.
* Raw data must remain available where legally and technically appropriate.
* The project must document how processed data was produced.

---

# 42. Experiment Data Integrity

Every experiment should use a clearly defined dataset version and preprocessing pipeline.

Do not compare:

```text
Model A → Clean Dataset
Model B → Different Dataset
```

and present the results as a fair model comparison.

Fair comparison requires consistent:

* Dataset
* Target definition
* Splitting methodology
* Evaluation methodology
* Relevant preprocessing assumptions

unless the experiment explicitly studies the effect of a data-processing change.

---

# 43. Reproducibility Checklist

A new developer should ideally be able to:

```text
Clone Repository
      ↓
Install Dependencies
      ↓
Obtain Dataset
      ↓
Place Dataset in Expected Location
      ↓
Run Data Audit
      ↓
Run Training Pipeline
      ↓
Generate Evaluation Results
      ↓
Run Inference
      ↓
Launch Application
```

without requiring undocumented manual intervention.

---

# 44. Data Strategy Decision Log

Important dataset decisions should be recorded.

Example:

| Decision                        | Reason                   | Impact                      |
| ------------------------------- | ------------------------ | --------------------------- |
| Dataset selected                | Better feature coverage  | Supports richer analysis    |
| Customer ID excluded from model | Identifier leakage risk  | More reliable modeling      |
| Median imputation               | Robust to extreme values | Stable preprocessing        |
| Stratified split                | Class imbalance          | Better class representation |

The actual decisions must be filled in after dataset inspection.

---

# 45. AI Implementation Assistant Rules for Data

Google AI Studio must follow these rules when working with data:

1. Never fabricate a dataset.
2. Never fabricate dataset rows.
3. Never fabricate dataset statistics.
4. Never fabricate missing-value counts.
5. Never fabricate class distributions.
6. Never fabricate dataset sources.
7. Never assume a column exists before inspecting the dataset.
8. Never assume a column's meaning without evidence.
9. Never silently rename important columns without documenting it.
10. Never overwrite raw data.
11. Never leak test-set information into training.
12. Never fit preprocessing on the complete dataset before splitting.
13. Never use future information as a feature.
14. Never remove outliers automatically without justification.
15. Never delete duplicates without determining whether they represent legitimate observations.
16. Never commit sensitive/private data to GitHub.
17. Never hard-code machine-specific file paths when avoidable.
18. Never report statistics that were not actually calculated.
19. Never report a dataset as "clean" without performing the relevant checks.
20. Keep the data-processing pipeline reproducible.

If the dataset does not contain a requested feature, AI Studio must not invent it.

Instead, it should report the limitation and suggest a legitimate alternative.

---

# 46. Data Strategy and AI Attribution

The data pipeline, documentation, and application must not contain unnecessary references such as:

* "Generated by Google AI Studio"
* "AI Studio Dataset"
* "Gemini generated data"
* "AI-generated customer records"

unless the content genuinely uses generated/synthetic data and disclosure is required.

The project must never falsely represent synthetic or fabricated data as real-world data.

---

# 47. Final Data Readiness Standard

The dataset is considered **Modeling Ready** only when:

* [ ] Source is documented
* [ ] Dataset structure is understood
* [ ] Target is verified
* [ ] Data types are understood
* [ ] Missing values are understood
* [ ] Duplicates are understood
* [ ] Outliers are investigated
* [ ] Class imbalance is quantified
* [ ] Identifiers are handled correctly
* [ ] Potential leakage is investigated
* [ ] Prediction-time availability is considered
* [ ] Train/test strategy is defined
* [ ] Cross-validation strategy is defined
* [ ] Preprocessing strategy is defined
* [ ] Feature engineering strategy is defined
* [ ] Reproducibility approach is defined
* [ ] Privacy considerations are addressed

Only then should the project move into serious model experimentation.

---

# 48. Final Principle

The dataset is not merely an input file.

It is the foundation on which every subsequent conclusion in this project depends.

Therefore:

> **Never optimize the model before understanding the data.**

A technically sophisticated model trained on poorly understood or contaminated data is less valuable than a simpler model built on a carefully validated dataset.

The project should prioritize:

```text
Understand the Data
        ↓
Validate the Data
        ↓
Prevent Leakage
        ↓
Build Reliable Features
        ↓
Split Correctly
        ↓
Train Models
        ↓
Evaluate Honestly
```

**Dataset quality and data integrity take priority over model complexity and headline performance.**

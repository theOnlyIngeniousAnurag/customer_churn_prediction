# Customer Churn Prediction & Retention Intelligence System

> A reproducible machine-learning decision-support system for predicting customer churn, ranking high-risk customers, and providing interpretable insights for retention review.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Classification-orange)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E)
![Status](https://img.shields.io/badge/Status-Phase%2010%20Complete-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Project Objectives](#project-objectives)
* [Key Features](#key-features)
* [Machine Learning Approach](#machine-learning-approach)
* [System Workflow](#system-workflow)
* [Dataset](#dataset)
* [Data Preparation & Leakage Audit](#data-preparation--leakage-audit)
* [Exploratory Data Analysis](#exploratory-data-analysis)
* [Feature Engineering Feasibility](#feature-engineering-feasibility)
* [Model Development](#model-development)
* [Model Evaluation](#model-evaluation)
* [Model Selection](#model-selection)
* [Explainability](#explainability)
* [Risk Ranking](#risk-ranking)
* [Project Structure](#project-structure)
* [Technology Stack](#technology-stack)
* [Installation](#installation)
* [Usage](#usage)
* [Reproducibility](#reproducibility)
* [Results](#results)
* [Limitations](#limitations)
* [Quality Assurance](#quality-assurance)
* [Documentation](#documentation)
* [Author](#author)
* [License](#license)

---

# Overview

Customer churn is a major challenge for subscription-based and recurring-service businesses. Acquiring a new customer can require significantly more effort than retaining an existing one. Identifying customers at elevated risk of churn empowers customer success and retention teams to prioritize proactive interventions.

This project develops an end-to-end, technically sound machine-learning system that analyzes historical customer information and estimates the probability that a customer will churn.

Rather than producing only a binary prediction, the system provides:
* Churn probability
* Risk category (High, Medium, Low)
* Customer risk ranking
* Model-supported contributing factors
* Evaluation metrics and calibration curves
* Interpretable insights for retention teams

---

# Problem Statement

The objective of this project is to predict whether a customer is likely to leave a subscription or recurring service based on historical customer information.

The machine-learning problem is formulated as a **supervised binary classification task**:

```text
Customer Historical Data
          ↓
    Feature Processing
          ↓
     ML Classifier
          ↓
   Churn Probability
          ↓
  Risk Classification
          ↓
 Customer Risk Ranking
          ↓
Retention Review Support
```

---

# Dataset

## Dataset Source

* **Dataset:** IBM Telco Customer Churn
* **Source:** IBM Business Analytics Community / Telco Customer Churn on ICP4D
* **Original URL:** `https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv`
* **License / Usage Terms:** Public domain / Apache 2.0 (IBM Community Sample Dataset)
* **Dataset Size:** 7,043 rows x 21 columns
* **Target Variable:** `Churn` ('No', 'Yes')
  * Non-churners (`No`): 5,174 (73.46%)
  * Churners (`Yes`): 1,869 (26.54%)
  * Imbalance Ratio: 2.77:1
* **Customer Identifier:** `customerID` (7,043 unique, 0 duplicates, excluded from feature set)

## Dataset Characteristics

The verified dataset contains 20 attributes covering:

1. **Customer Demographics (4)**: `gender`, `SeniorCitizen`, `Partner`, `Dependents`
2. **Account Tenure (1)**: `tenure` (0 to 72 months, median 29.0)
3. **Phone Services (2)**: `PhoneService`, `MultipleLines`
4. **Internet Services (7)**: `InternetService` (DSL, Fiber optic, None), `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
5. **Contract & Account (3)**: `Contract` (Month-to-month, One year, Two year), `PaperlessBilling`, `PaymentMethod` (Electronic check, Mailed check, Bank transfer, Credit card)
6. **Billing History (2)**: `MonthlyCharges` (USD 18.25 to 118.75), `TotalCharges` (USD 18.80 to 8684.80)
7. **Target (1)**: `Churn` (Yes / No)

---

# Data Preparation & Leakage Audit

Before training any model, the dataset underwent a systematic data-quality and deep leakage audit:
* **Missing Values:** 0 explicit `NaN` values across all 21 columns. 11 whitespace strings in `TotalCharges` (`" "`) corresponding strictly to new customer registrations where `tenure == 0` (unbilled signups).
* **Duplicates:** 0 duplicate rows and 0 duplicate `customerID` entries.
* **Leakage Audit:** Every feature was verified for prediction-time availability. 0 post-churn fields, cancellation dates, or target-derived indicators are present. `customerID` is isolated as an administrative identifier and excluded from candidate feature vectors.
* **Outliers:** Evaluated IQR fences for numerical variables; 0 observations exceeded IQR fences (`tenure`: 0-72 mos, `MonthlyCharges`: $18.25-$118.75, `TotalCharges`: $18.80-$8684.80).

---

# Exploratory Data Analysis

Phase 2 exploratory analysis uncovered strong empirical associations with customer churn:

1. **Contract Duration Effect:**
   * Month-to-month contracts experience a **42.71% churn rate** (1,655 / 3,875).
   * One-year contracts drop to **11.27% churn rate** (166 / 1,473).
   * Two-year contracts drop to **2.83% churn rate** (48 / 1,695).
2. **Tenure Lifecycle Dynamics:**
   * Median tenure for churners is **10.0 months**, compared to **38.0 months** for non-churners (28-month difference).
   * Cohort churn rate: 0–12 months = **47.44%**, 13–24 months = **28.71%**, 25–48 months = **20.39%**, 49–72 months = **9.51%**.
3. **Internet Service & Pricing:**
   * Fiber optic subscribers show an elevated churn rate of **41.89%** (1,297 / 3,096), compared to DSL (**18.96%**) and No Internet (**7.40%**).
   * Churners have a median monthly charge of **$79.65**, vs **$64.43** for non-churners (associated with higher-tier unbundled plans).
4. **Payment Method Friction:**
   * Electronic check users experience a **45.29% churn rate** (1,071 / 2,365).
   * Automated payment methods (Bank transfer: **16.71%**, Credit card: **15.24%**) demonstrate significantly lower churn rates.
5. **Support & Security Value Services:**
   * Customers without `TechSupport` churn at **41.64%** vs **15.17%** with TechSupport.
   * Customers without `OnlineSecurity` churn at **41.77%** vs **14.61%** with OnlineSecurity.
6. **Collinearity Observations:**
   * `TotalCharges` exhibits strong linear collinearity with `tenure` ($r = 0.826$) and moderate correlation with `MonthlyCharges` ($r = 0.651$), reflecting the cumulative accounting identity $\text{TotalCharges} \approx \text{tenure} \times \text{MonthlyCharges}$.

All 6 analytical charts are generated reproducibly in `reports/figures/`.

---

# Feature Engineering Feasibility & Ablation Findings

Candidate features audited in Phase 2 and evaluated in Phase 3 ablation:
* **`tenure_group`**: Lifecycle binning ([0-12, 13-24, 25-48, 49-72 mos]) — **Candidate for Phase 4**
* **`total_services_subscribed`**: Integer sum of 9 catalog services (range 1-9) — **Redundant**
* **`has_tech_support_or_security`**: Binary flag for high-retention assistance services — **Redundant**
* **`auto_payment_indicator`**: Automated vs manual payment friction indicator — **Redundant**
* **`charges_ratio`**: `MonthlyCharges / (TotalCharges + 1.0)` — **Redundant**
* *Documented Limitations*: Support ticket logs, time-series usage volume deltas, and prior billing cycle changes are not available in this dataset and will not be artificially fabricated.

### Phase 3 Ablation Results (5-Fold Stratified Cross-Validation on Training Set, N=5,634)
| Feature Set | ROC-AUC | PR-AUC | Precision | Recall | F1 | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Experiment A (Baseline, 19 raw)** | **0.8461** | **0.6615** | **0.6549** | **0.5438** | **0.5935** | Core Baseline |
| **Exp B1 (+ `tenure_group`)** | 0.8465 | 0.6651 | 0.6685 | 0.5358 | 0.5941 | Phase 4 Candidate |
| **Exp B2 (+ `total_services_subscribed`)** | 0.8461 | 0.6615 | 0.6549 | 0.5438 | 0.5935 | Excluded (Redundant) |
| **Exp B3 (+ `has_tech_support_or_security`)** | 0.8459 | 0.6612 | 0.6540 | 0.5425 | 0.5924 | Excluded (Collinear) |
| **Exp B4 (+ `auto_payment_indicator`)** | 0.8461 | 0.6614 | 0.6543 | 0.5438 | 0.5933 | Excluded (Redundant) |
| **Exp B5 (+ `charges_ratio`)** | 0.8461 | 0.6617 | 0.6544 | 0.5438 | 0.5933 | Excluded (Redundant) |
| **Exp C (All Candidates)** | 0.8464 | 0.6653 | 0.6668 | 0.5405 | 0.5963 | Excluded (Bloat) |

*Assessment:* `tenure_group` produced a small observed improvement in PR-AUC and Precision in the training-only cross-validation experiment. It is retained as a candidate for Phase 4 validation rather than being considered conclusively beneficial. The final test set (N=1,409) remains strictly isolated and untouched.

---

# Model Development

## Baseline
* **Model:** Logistic Regression (`sklearn.linear_model.LogisticRegression`)
* **Parameters:** `max_iter=1000`, `random_state=42`, `C=1.0`, `penalty='l2'`, `solver='lbfgs'`
* **Pipeline:** `TotalChargesCleaner` -> `ColumnTransformer` (`StandardScaler`, `OneHotEncoder(drop='first', handle_unknown='ignore')`) -> `LogisticRegression`
* **Status:** **Phase 4 Complete** (5-fold Stratified CV on training set; test set untouched)

## Candidate Models (Phase 5 Benchmarking)
* **Decision Tree:** `DecisionTreeClassifier(random_state=42)` (un-tuned baseline)
* **Random Forest:** `RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)` (un-tuned baseline)
* **Status:** **Phase 10 Complete** (Benchmarking on identical 5-fold Stratified CV; test set untouched)

---

# Model Evaluation

The primary evaluation metrics include:
* **ROC-AUC:** Discrimination ability across all decision thresholds
* **PR-AUC (Average Precision):** Area under the Precision-Recall curve
* **Precision:** True Positive proportion among flagged customers (default 0.50 threshold)
* **Recall:** Sensitivity to actual churners (default 0.50 threshold)
* **F1-Score:** Harmonic balance of precision and recall (default 0.50 threshold)

### Benchmarking Comparison (Identical 5-Fold Stratified CV on Training Set, N=5,634)
| Model | Features | ROC-AUC | PR-AUC | Precision | Recall | F1 | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | **Original** | **0.8461 ± 0.0126** | **0.6615 ± 0.0194** | **0.6549 ± 0.0284** | **0.5438 ± 0.0409** | **0.5935 ± 0.0304** | Core Baseline (19 raw features) |
| Logistic Regression | + `tenure_group` | 0.8465 ± 0.0117 | 0.6651 ± 0.0134 | 0.6685 ± 0.0195 | 0.5358 ± 0.0360 | 0.5941 ± 0.0233 | Small lift in PR-AUC & Precision |
| **Decision Tree** | **Original** | **0.6568 ± 0.0162** | **0.3793 ± 0.0173** | **0.4914 ± 0.0244** | **0.4983 ± 0.0208** | **0.4948 ± 0.0222** | Un-tuned (depth=23, 1097 leaves, overfit) |
| Decision Tree | + `tenure_group` | 0.6660 ± 0.0159 | 0.3889 ± 0.0179 | 0.5034 ± 0.0255 | 0.5144 ± 0.0234 | 0.5087 ± 0.0225 | Un-tuned baseline |
| **Random Forest** | **Original** | **0.8260 ± 0.0117** | **0.6241 ± 0.0309** | **0.6298 ± 0.0369** | **0.4769 ± 0.0230** | **0.5425 ± 0.0254** | Un-tuned 300 trees baseline |
| Random Forest | + `tenure_group` | 0.8262 ± 0.0134 | 0.6214 ± 0.0334 | 0.6331 ± 0.0527 | 0.4729 ± 0.0341 | 0.5413 ± 0.0411 | Un-tuned 300 trees baseline |

### Training Out-of-Fold Confusion Matrices (Default 0.50 Threshold, N=5,634)
*Note on Metrics:* The fold-level cross-validation scores reported in the comparison table represent the arithmetic mean (and standard deviation) of metrics across the 5 independent evaluation folds. In contrast, the confusion matrix metrics below are calculated globally from the pooled out-of-fold predictions across all 5,634 training observations. Due to non-linear pooling across varying fold denominators, small differences (e.g., Random Forest CV mean Recall of 47.69% vs. pooled OOF Recall of 48.23%; Decision Tree CV mean Recall of 49.83% vs. pooled OOF Recall of 49.97%) are expected and statistically sound.

* **Logistic Regression (Baseline):** TN: 3,710 | FP: 429 | FN: 682 | TP: 813 (Accuracy: 80.28%, Precision: 65.46%, Recall: 54.38%, F1: 59.41%)
* **Decision Tree (Original):** TN: 3,365 | FP: 774 | FN: 748 | TP: 747 (Accuracy: 72.99%, Precision: 49.11%, Recall: 49.97%, F1: 49.54%)
* **Random Forest (Original):** TN: 3,714 | FP: 425 | FN: 774 | TP: 721 (Accuracy: 78.72%, Precision: 62.91%, Recall: 48.23%, F1: 54.60%)

### Feature Importance Highlights (Model-Based Impurity Reduction)
* **Random Forest (Top 5):** `TotalCharges` (0.1893), `tenure` (0.1727), `MonthlyCharges` (0.1691), `InternetService_Fiber optic` (0.0400), `PaymentMethod_Electronic check` (0.0391)
* **Decision Tree (Top 5):** `TotalCharges` (0.2016), `Contract_Two year` (0.1989), `MonthlyCharges` (0.1706), `tenure` (0.1017), `InternetService_Fiber optic` (0.0487)

*Interpretation Notice:* The importance values are descriptive of how the fitted tree models reduced Gini impurity using the available encoded features. Correlation among `tenure`, `TotalCharges`, and `MonthlyCharges` can distribute or concentrate importance and therefore limits independent interpretation. These values reflect model-internal split criteria and do not represent causal effects.

Full artifacts exported to `reports/results/decision_tree_feature_importance.csv` and `reports/results/random_forest_feature_importance.csv`.

---

# Project Structure

```text
customer-churn-prediction/
│
├── data/
│   ├── raw/
│   │   └── Telco-Customer-Churn.csv
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── audit.py
│   │   └── eda.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── engineering.py
│   │   ├── preprocessing.py
│   │   └── ablation.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── baseline.py
│   │   └── tree_models.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── baseline.py
│   │   └── tree_models.py
│   └── utils/
│       └── __init__.py
│
├── models/
├── reports/
│   ├── figures/
│   └── results/
│       ├── eda_audit_report.json
│       ├── feature_ablation_results.json
│       ├── logistic_regression_baseline.json
│       ├── logistic_regression_coefficients.csv
│       ├── tree_model_benchmark.json
│       ├── decision_tree_feature_importance.csv
│       └── random_forest_feature_importance.csv
│
├── tests/
│   ├── test_data_audit.py
│   ├── test_eda.py
│   ├── test_preprocessing.py
│   ├── test_features.py
│   ├── test_baseline.py
│   └── test_tree_models.py
│
├── docs/
│   ├── PRD.md
│   ├── PROJECT_SPECIFICATIONS.md
│   ├── ML_REQUIREMENTS.md
│   ├── DATASET_AND_DATA_STRATEGY.md
│   ├── EXPERIMENT_PLAN.md
│   ├── ARCHITECTURE.md
│   ├── RULES.md
│   ├── CODING_STANDARDS.md
│   ├── GIT_GITHUB_STRATEGY.md
│   ├── QUALITY_ASSURANCE.md
│   └── TASK_TRACKER.md
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technology Stack

* **Language:** Python 3.11
* **Data Processing & ML:** `numpy`, `pandas`, `scikit-learn`
* **Version Control:** Git & GitHub

*(Adheres strictly to the internship technology constraints. No unapproved frameworks or external libraries).*

---

# Installation

```bash
# Clone the repository
git clone <REPOSITORY_URL>
cd customer-churn-prediction

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install approved dependencies
pip install -r requirements.txt
```

---

# Usage

### Run Data Quality Audit
```bash
python3 -m src.data.audit
```

### Run EDA & Leakage Audit Pipeline
```bash
python3 -m src.data.eda
```

### Run Phase 3 Feature Ablation Study
```bash
python3 -m src.features.ablation
```

### Run Phase 4 Baseline Benchmarking
```bash
python3 -m src.evaluation.baseline
```

### Run Phase 5 Tree-Based Model Benchmarking
```bash
python3 -m src.evaluation.tree_models
```

### Run Complete Test Suite
```bash
python3 -m unittest discover -s tests -v
# or: pytest tests
# Authoritative Result: 41 collected, 41 passed, 0 failed
```

---

# Project Status

**Current Status:** Phase 10 Complete (Tree-Based Model Benchmarking)

* [x] Phase 0 — Project Setup & Environment Configuration
* [x] Phase 1 — Dataset Acquisition & Quality Audit
* [x] Phase 2 — Exploratory Data Analysis & Leakage Audit
* [x] Phase 3 — Preprocessing & Feature Engineering Ablation
* [x] Phase 4 — Logistic Regression Baseline
* [x] Phase 5 — Candidate Model Comparison
* [x] Phase 6 — Hyperparameter Tuning & Model Selection
* [x] Phase 7 — Final Evaluation & Calibration
* [x] Phase 8 — Error Analysis & Explainability
* [x] Phase 9 — Application / Demo
* [x] Phase 10 — Testing & QA Sign-Off

---

# Author

**Anurag**
Machine Learning Internship Capstone Project

---

# License

MIT License. Dataset provided under public domain sample by IBM Corporation.

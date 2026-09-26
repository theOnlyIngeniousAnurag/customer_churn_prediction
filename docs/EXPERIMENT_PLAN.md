# EXPERIMENT PLAN

## Customer Churn Prediction & Retention Intelligence System

**Project:** Customer Churn Prediction
**Experimentation Type:** Supervised Binary Classification
**Primary Goal:** Reliable, fair, reproducible model comparison
**Status:** Planning
**Version:** 1.0
**Author:** Anurag
**Deadline:** 30 September 2026

---

# 1. Purpose of This Document

This document defines the complete experimentation methodology for the Customer Churn Prediction project.

The purpose is to ensure that model development is:

* Systematic
* Reproducible
* Leakage-safe
* Fair
* Interpretable
* Evidence-based
* Efficient within the internship deadline

The project must not select a model simply because it produces the highest single metric.

Every significant model decision must be supported by experimental evidence.

---

# 2. Core Experimentation Principle

The experimentation process must follow:

```text
Dataset Understanding
        ↓
Data Quality Validation
        ↓
Train / Validation / Test Strategy
        ↓
Baseline
        ↓
Candidate Models
        ↓
Feature Engineering
        ↓
Model Comparison
        ↓
Hyperparameter Tuning
        ↓
Calibration / Threshold Analysis
        ↓
Error Analysis
        ↓
Final Model Selection
        ↓
Final Test Evaluation
```

The process must be incremental.

Do not perform large-scale tuning before establishing a baseline.

---

# 3. Research / Engineering Questions

The experiments should answer the following questions.

### Q1. Can customer features provide useful churn predictions?

Establish whether a meaningful predictive signal exists.

### Q2. How strong is a simple interpretable baseline?

Use Logistic Regression as the primary baseline.

### Q3. Do nonlinear tree-based models improve performance?

Compare suitable tree-based approaches against the baseline.

### Q4. Which model generalizes best?

Evaluate using consistent validation methodology.

### Q5. How does class imbalance affect predictions?

Investigate the impact on precision, recall, F1, and other relevant metrics.

### Q6. Does feature engineering improve useful predictive performance?

Compare models before and after meaningful feature engineering.

### Q7. Are predicted probabilities reliable?

Evaluate calibration.

### Q8. What types of customers does the model get wrong?

Perform error analysis.

### Q9. Which model should be selected for the final system?

Consider performance, calibration, interpretability, complexity, and practical usefulness together.

---

# 4. Experimental Rules

The following rules are mandatory.

## Rule 1 — No fabricated results

Never invent:

* Accuracy
* ROC-AUC
* Precision
* Recall
* F1
* PR-AUC
* Calibration results
* Confusion matrices
* Feature importance
* Training time
* Experiment outcomes

Every result must come from an actual execution.

---

## Rule 2 — No data leakage

The experiment pipeline must ensure that information from validation/test data does not influence training.

This includes:

* Imputation
* Scaling
* Encoding
* Feature selection
* Feature engineering where applicable
* Hyperparameter selection

Use pipelines where appropriate.

---

## Rule 3 — Preserve the final test set

The final test set should remain untouched during model development.

It must only be used for final evaluation after:

1. Model strategy is finalized.
2. Hyperparameters are finalized.
3. Threshold strategy is finalized where applicable.
4. Final model is selected.

---

## Rule 4 — Fair model comparison

Models must be evaluated using:

* The same target definition
* The same data split strategy
* Comparable preprocessing
* The same primary evaluation framework
* The same test set for final evaluation

---

## Rule 5 — No metric shopping

Do not select whichever metric makes a model look best.

Metrics must be selected according to the actual business and ML objective.

---

## Rule 6 — No unnecessary experiments

Only perform experiments that can answer a meaningful technical question.

The project deadline is limited.

---

# 5. Experiment Phases

The project will use the following experiment phases:

```text
E0 — Dataset & Data Validation
E1 — Baseline
E2 — Candidate Model Comparison
E3 — Feature Engineering
E4 — Imbalance Strategy
E5 — Hyperparameter Tuning
E6 — Threshold Analysis
E7 — Calibration
E8 — Error Analysis
E9 — Explainability
E10 — Final Model Validation
```

Not every phase requires a separate model.

Some phases analyze or improve an existing experiment.

---

# 6. E0 — Dataset & Data Validation

Before any model training:

### Objectives

* Confirm dataset structure.
* Confirm target.
* Confirm feature types.
* Check missing values.
* Check duplicates.
* Check class distribution.
* Identify suspicious columns.
* Identify possible leakage.
* Identify identifier columns.
* Understand available business variables.

### Required outputs

Create a data audit containing:

| Check                | Result | Action |
| -------------------- | ------ | ------ |
| Dataset shape        |        |        |
| Duplicate rows       |        |        |
| Duplicate IDs        |        |        |
| Missing values       |        |        |
| Target missingness   |        |        |
| Target classes       |        |        |
| Class distribution   |        |        |
| Numerical features   |        |        |
| Categorical features |        |        |
| Potential leakage    |        |        |
| Identifier columns   |        |        |
| Constant columns     |        |        |

No model should be trained until this audit is sufficiently understood.

---

# 7. Train / Validation / Test Strategy

The dataset must be divided appropriately.

A preferred conceptual structure is:

```text
Full Dataset
     │
     ├── Training Data
     │       ↓
     │   Cross-Validation
     │       ↓
     │   Model Development
     │
     ├── Validation Strategy
     │       ↓
     │   Model / Threshold Decisions
     │
     └── Final Test Data
             ↓
       Final Evaluation
```

The exact split ratio should be selected based on dataset size.

A common starting point may be:

* 70% training
* 15% validation
* 15% test

or an appropriate alternative.

If cross-validation is used for model development, a separate validation set may not always be necessary.

The chosen strategy must be documented and justified.

---

# 8. Stratification

Because churn classification may contain class imbalance, stratification should be considered.

For ordinary classification data:

```text
Stratified Split
```

should generally preserve the approximate target-class proportions across relevant splits.

The implementation must verify that the chosen split strategy is appropriate for the dataset.

---

# 9. E1 — Baseline Experiment

## Objective

Establish the minimum meaningful performance level.

## Primary baseline

**Logistic Regression**

Why:

* Simple
* Fast
* Interpretable
* Strong baseline for tabular binary classification
* Provides probability estimates
* Useful benchmark against nonlinear models

---

## Baseline preprocessing

The baseline should use a proper preprocessing pipeline.

Depending on the dataset:

### Numerical

Potentially:

* Missing-value imputation
* Scaling where appropriate

### Categorical

Potentially:

* Missing-value handling
* One-hot encoding

### Identifier columns

Generally exclude identifiers from predictive features unless there is a legitimate modeling reason.

---

## Baseline metrics

Record at minimum:

* ROC-AUC
* Precision
* Recall
* F1-score
* Confusion matrix
* Calibration information where feasible

Accuracy may be reported as a supplementary metric but must not dominate evaluation when class imbalance is significant.

---

# 10. Baseline Experiment Record (Phase 4 Executed)

Record every baseline experiment in a structured table.

| Field          | Value |
| -------------- | ----- |
| Experiment ID  | E1 (Baseline Benchmarking) |
| Model          | Logistic Regression (`sklearn.linear_model.LogisticRegression`) |
| Features       | 19 raw predictive features (3 numerical, 16 categorical -> 30 transformed features) |
| Preprocessing  | `TotalChargesCleaner` -> `ColumnTransformer` (`StandardScaler`, `OneHotEncoder(drop='first', handle_unknown='ignore')`) |
| Split strategy | 80/20 Stratified Split (5,634 train / 1,409 test). Test set isolated (untouched). |
| CV strategy    | 5-Fold Stratified Cross-Validation (`StratifiedKFold`, `shuffle=True`, `random_state=42`) |
| Random seed    | 42 |
| Parameters     | `max_iter=1000`, `random_state=42`, `C=1.0`, `penalty='l2'`, `solver='lbfgs'` |
| ROC-AUC        | **0.8461 ± 0.0126** |
| PR-AUC         | **0.6615 ± 0.0194** |
| Precision      | **0.6549 ± 0.0284** (default 0.50 threshold) |
| Recall         | **0.5438 ± 0.0409** (default 0.50 threshold) |
| F1             | **0.5935 ± 0.0304** (default 0.50 threshold) |
| Confusion Matrix (OOF) | TN: 3,710 \| FP: 429 \| FN: 682 \| TP: 813 (Accuracy: 80.28%) |
| Calibration    | Not calibrated in Phase 4 (reserved for Phase 7) |
| Top Coefficients | Negative: `Contract_Two year` (-1.3248), `tenure` (-1.2549), `Contract_One year` (-0.6867)<br>Positive: `InternetService_Fiber optic` (+1.2058), `TotalCharges` (+0.5275) |
| Observations   | Linear baseline establishes a solid discrimination benchmark (ROC-AUC ~0.846). Misses 45.62% of churners at 0.50 threshold (FN=682). `tenure_group` candidate (Exp B1) yielded minor lift (PR-AUC +0.0036, Precision +0.0136), retained for Phase 5 comparison. |

---

# 11. E2 — Candidate Model Comparison

After establishing the baseline, compare appropriate alternative models.

Potential candidates:

1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Gradient Boosting
5. XGBoost, if justified and practical

The exact list must depend on:

* Dataset size
* Feature characteristics
* Available dependencies
* Computational cost
* Time
* Interpretability requirements

Do not add models merely to increase the model count.

---

# 12. Candidate Model Experiment

Each model should initially be evaluated using sensible baseline/default parameters.

This first comparison is intended to answer:

> Which model families appear promising before extensive tuning?

Do not heavily tune every model at this stage.

---

# 13. Initial Model Comparison Table (Phase 5 Executed)

Maintain a table such as:

| Experiment | Model | Features | ROC-AUC | PR-AUC | Precision | Recall | F1 | Notes |
| ---------- | ----- | -------- | ------: | -----: | --------: | -----: | -: | ----- |
| E1 | Logistic Regression | Original | **0.8461 ± 0.0126** | **0.6615 ± 0.0194** | **0.6549 ± 0.0284** | **0.5438 ± 0.0409** | **0.5935 ± 0.0304** | Linear baseline benchmark |
| E1-B1 | Logistic Regression | + tenure_group | **0.8465 ± 0.0117** | **0.6651 ± 0.0134** | **0.6685 ± 0.0195** | **0.5358 ± 0.0360** | **0.5941 ± 0.0233** | Candidate feature evaluation |
| E2 | Decision Tree | Original | **0.6568 ± 0.0162** | **0.3793 ± 0.0173** | **0.4914 ± 0.0244** | **0.4983 ± 0.0208** | **0.4948 ± 0.0222** | Un-tuned (depth=23, severe overfit) |
| E2-B1 | Decision Tree | + tenure_group | **0.6660 ± 0.0159** | **0.3889 ± 0.0179** | **0.5034 ± 0.0255** | **0.5144 ± 0.0234** | **0.5087 ± 0.0225** | Un-tuned (depth=23) |
| E3 | Random Forest | Original | **0.8260 ± 0.0117** | **0.6241 ± 0.0309** | **0.6298 ± 0.0369** | **0.4769 ± 0.0230** | **0.5425 ± 0.0254** | Un-tuned 300 trees baseline |
| E3-B1 | Random Forest | + tenure_group | **0.8262 ± 0.0134** | **0.6214 ± 0.0334** | **0.6331 ± 0.0527** | **0.4729 ± 0.0341** | **0.5413 ± 0.0411** | Un-tuned 300 trees baseline |

*All results computed across identical 5-fold Stratified CV splits on 5,634 training observations ($N=5,634$). Final test set ($N=1,409$) remains strictly isolated and untouched.*

---

# 14. Model Selection Is Not Metric Maximization

The highest ROC-AUC model should not automatically become the final model.

Consider:

### Predictive performance

* ROC-AUC
* Precision
* Recall
* F1

### Probability quality

* Calibration

### Generalization

* Cross-validation stability
* Train vs validation behavior

### Interpretability

* Ease of explanation
* Feature importance

### Complexity

* Training cost
* Inference cost
* Dependencies

### Practical usefulness

* Ability to rank high-risk customers
* False-positive burden
* False-negative burden

The final selection must consider the complete evidence.

---

# 15. E3 — Feature Engineering Experiment

Feature engineering should be performed only after establishing a reliable baseline.

Potential feature categories:

### Behavioral

* Usage frequency
* Usage intensity
* Usage trend
* Recent activity

### Support

* Support-contact frequency
* Complaint intensity
* Support interaction ratios

### Billing

* Recent payment changes
* Billing amount relationships
* Payment behavior indicators

### Tenure

* Tenure groups
* Tenure-related transformations

Only features that are genuinely supported by the dataset may be created.

---

# 16. Feature Engineering Comparison & Ablation Findings (Phase 3 Executed)

A controlled 5-fold Stratified Cross-Validation ablation was executed on the 5,634 training records (random_state=42) using Logistic Regression with leakage-safe preprocessing pipelines:

```text
Experiment A (Baseline, 19 raw features)
        vs
Experiments B1–B5 (Individual Candidates)
        vs
Experiment C (All Candidates Combined)
```

### Empirical Cross-Validation Metrics (No Test Contamination)
| Feature Set | ROC-AUC | PR-AUC | Precision | Recall | F1 | Delta ROC-AUC | Verdict / Observation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Exp A (Baseline)** | **0.8461** | **0.6615** | **0.6549** | **0.5438** | **0.5935** | 0.0000 | Core baseline for all future modeling phases. |
| **Exp B1 (+ `tenure_group`)** | 0.8465 | 0.6651 | 0.6685 | 0.5358 | 0.5941 | +0.0004 | Slight lift in Precision (+0.0136) and PR-AUC (+0.0036). Retain as Phase 4 candidate. |
| **Exp B2 (+ `total_services_subscribed`)** | 0.8461 | 0.6615 | 0.6549 | 0.5438 | 0.5935 | +0.0000 | Exactly 0.0 lift across all metrics; completely redundant with individual catalog OHE vectors. |
| **Exp B3 (+ `has_tech_support_or_security`)** | 0.8459 | 0.6612 | 0.6540 | 0.5425 | 0.5924 | -0.0002 | Degrades performance slightly due to multicollinearity with constituent features. Exclude. |
| **Exp B4 (+ `auto_payment_indicator`)** | 0.8461 | 0.6614 | 0.6543 | 0.5438 | 0.5933 | +0.0000 | Zero lift; one-hot encoded `PaymentMethod` already separates payment tiers optimally. Exclude. |
| **Exp B5 (+ `charges_ratio`)** | 0.8461 | 0.6617 | 0.6544 | 0.5438 | 0.5933 | +0.0000 | Zero lift; acts as an inverse surrogate of tenure with no longitudinal delta signal. Exclude. |
| **Exp C (All Candidates Combined)** | 0.8464 | 0.6653 | 0.6668 | 0.5405 | 0.5963 | +0.0003 | Minor gains identical to tenure_group alone; introduces unnecessary feature matrix bloat. |

A feature is not retained solely because it increases a metric slightly. Based on these empirical results:
- `tenure_group` produced a small observed improvement in PR-AUC and Precision in the training-only cross-validation experiment. It is retained as a candidate for Phase 4 validation rather than being considered conclusively beneficial.
- The remaining candidates are redundant with raw features and will not clutter the primary modeling pipeline.


---

# 17. Feature Engineering Rules

Do not:

* Create features using the target.
* Use future information.
* Use post-churn information.
* Create features that would not be available at prediction time.
* Create dozens of arbitrary mathematical transformations.

Every important engineered feature should have a documented reason.

---

# 18. E4 — Class Imbalance Experiment

First determine whether the dataset is meaningfully imbalanced.

If imbalance is significant, compare appropriate strategies.

Possible strategies:

### Strategy A

No correction

### Strategy B

Class weights

### Strategy C

Appropriate resampling

### Strategy D

Threshold adjustment

The exact strategy should be selected based on experimental evidence.

---

# 19. Imbalance Comparison

Example:

| Strategy             | ROC-AUC | Precision | Recall | F1 | False Positives | False Negatives |
| -------------------- | ------: | --------: | -----: | -: | --------------: | --------------: |
| None                 |         |           |        |    |                 |                 |
| Class Weight         |         |           |        |    |                 |                 |
| Resampling           |         |           |        |    |                 |                 |
| Threshold Adjustment |         |           |        |    |                 |                 |

Do not assume oversampling is automatically better.

---

# 20. Resampling Safety

If resampling is used:

**Resampling must occur only within the training portion of the data.**

Do not oversample or undersample the complete dataset before train/test splitting.

This is a critical leakage-prevention rule.

---

# 21. E5 — Hyperparameter Tuning

Only promising model families should proceed to extensive tuning.

Potential tuning methods:

* GridSearchCV
* RandomizedSearchCV

The search space should remain focused.

---

# 22. Hyperparameter Tuning Principles

Tuning must:

1. Use cross-validation.
2. Optimize a clearly defined metric.
3. Use a controlled search space.
4. Record the best parameters.
5. Record validation performance.
6. Avoid repeatedly tuning against the test set.

---

# 23. Example Tuning Parameters

## Logistic Regression

Potential parameters:

* `C`
* `penalty`
* solver where relevant
* class weighting where appropriate

## Decision Tree

Potential parameters:

* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `criterion`

## Random Forest

Potential parameters:

* `n_estimators`
* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `max_features`
* `class_weight`

## Gradient Boosting

Potential parameters:

* `n_estimators`
* `learning_rate`
* `max_depth` or equivalent complexity control
* `subsample` where supported

## XGBoost

If used, tune only a focused set of meaningful parameters.

Do not perform an unnecessarily large search.

---

# 24. Tuning Record

We conducted controlled randomized hyperparameter optimization for both tree-based model families under strict test isolation (the 1,409-row test set remained completely untouched).

## Decision Tree Tuning Record

| Field                    | Value |
| ------------------------ | ----- |
| Experiment ID            | EXP-DT-TUNING |
| Model                    | DecisionTreeClassifier |
| Search method            | RandomizedSearchCV (n_iter=15, random_state=42) |
| CV folds                 | 5-fold StratifiedKFold (shuffle=True, random_state=42) |
| Scoring metric           | average_precision (PR-AUC) |
| Search space             | `criterion`: ["gini", "entropy"], `max_depth`: [3, 5, 7, 10, 15, 20], `min_samples_leaf`: [1, 2, 5, 10, 20], `min_samples_split`: [2, 5, 10, 20] |
| Number of configurations | 15 configurations |
| Best parameters          | `min_samples_split`: 2, `min_samples_leaf`: 2, `max_depth`: 5, `criterion`: "gini" |
| CV PR-AUC (Validation)   | 0.6132 |
| CV ROC-AUC (Validation)  | 0.8284 |
| F1 Score (Validation)    | 0.5766 (Precision: 0.6181, Recall: 0.5425) |
| Train PR-AUC             | 0.6503 (Overfitting train-val gap: 0.0371) |
| Notes                    | Regularization (max_depth=5, min_samples_leaf=2) substantially reduced the overfitting observed in the Phase 5 baseline and produced a large improvement in cross-validation performance. |

## Random Forest Tuning Record

| Field                    | Value |
| ------------------------ | ----- |
| Experiment ID            | EXP-RF-TUNING |
| Model                    | RandomForestClassifier |
| Search method            | RandomizedSearchCV (n_iter=20, random_state=42) |
| CV folds                 | 5-fold StratifiedKFold (shuffle=True, random_state=42) |
| Scoring metric           | average_precision (PR-AUC) |
| Search space             | `n_estimators`: [200, 300, 500], `max_depth`: [None, 8, 12, 16, 20], `min_samples_leaf`: [1, 2, 5, 10], `min_samples_split`: [2, 5, 10], `max_features`: ["sqrt", "log2"] |
| Number of configurations | 20 configurations |
| Best parameters          | `n_estimators`: 300, `min_samples_split`: 2, `min_samples_leaf`: 2, `max_features`: "sqrt", `max_depth`: 8 |
| CV PR-AUC (Validation)   | 0.6643 |
| CV ROC-AUC (Validation)  | 0.8459 |
| F1 Score (Validation)    | 0.5671 (Precision: 0.6784, Recall: 0.4876) |
| Train PR-AUC             | 0.7660 (Overfitting train-val gap: 0.1017) |
| Notes                    | Random Forest optimization improved cross-validation performance, while a train-validation PR-AUC gap of 0.1017 indicates some remaining overfitting. Validation fold variability remained moderate (PR-AUC SD = 0.0211). The optimized Random Forest achieved a slightly higher mean CV PR-AUC (0.6643) than the Logistic Regression baseline (0.6615). The difference is small relative to fold-to-fold variability, so this does not establish a decisive performance advantage. |

---

# 25. Overfitting Analysis

Compare:

* Training performance
* Cross-validation performance
* Validation performance
* Final test performance

Large gaps should be investigated.

Example:

```text
Training:       0.98
Validation:     0.82
Test:           0.80
```

This may indicate overfitting.

Do not attempt to hide poor generalization.

---

# 26. E6 — Threshold Analysis

The classification threshold should be treated as a decision parameter.

The model's probability output:

```text
P(churn)
```

must be separated conceptually from:

```text
Predicted Class
```

For example:

```text
P(churn) ≥ threshold → Churn
P(churn) < threshold → No Churn
```

The threshold should be analyzed rather than automatically fixed at 0.50.

---

# 27. Threshold Experiment

Evaluate a sensible range of thresholds.

For example:

```text
0.20
0.25
0.30
0.35
0.40
0.45
0.50
0.55
0.60
0.65
0.70
0.75
0.80
```

The exact range can be adapted to the model's probability distribution.

For each threshold, evaluate:

* Precision
* Recall
* F1
* Number predicted positive
* False positives
* False negatives

---

# 28. Threshold Analysis Table

| Threshold | Precision | Recall | F1 | Predicted Churners | FP | FN |
| --------: | --------: | -----: | -: | -----------------: | -: | -: |
|      0.20 |    0.4557 | 0.8663 | 0.5972 |                711 | 387 |  50 |
|      0.25 |    0.5041 | 0.8289 | 0.6269 |                615 | 305 |  64 |
|      0.30 |    0.5316 | 0.7861 | 0.6343 |                553 | 259 |  80 |
|      0.35 |    0.5572 | 0.7032 | 0.6217 |                472 | 209 | 111 |
|      0.40 |    0.6020 | 0.6390 | 0.6200 |                397 | 158 | 135 |
|      0.45 |    0.6313 | 0.5722 | 0.6003 |                339 | 125 | 160 |
|      0.50 |    0.6866 | 0.4920 | 0.5732 |                268 |  84 | 190 |
|      0.55 |    0.7109 | 0.4011 | 0.5128 |                211 |  61 | 224 |
|      0.60 |    0.7452 | 0.3128 | 0.4407 |                157 |  40 | 257 |
|      0.65 |    0.7759 | 0.2406 | 0.3673 |                116 |  26 | 284 |
|      0.70 |    0.8000 | 0.1818 | 0.2963 |                 85 |  17 | 306 |

The final threshold must be documented and justified.

---

# 29. E7 — Probability Calibration

Calibration is explicitly required by the internship project.

The objective is to determine whether predicted probabilities are reasonably aligned with observed outcomes.

For example:

If a group of customers receives approximately:

```text
Predicted probability ≈ 0.70
```

then the observed churn rate for comparable predictions should be reasonably close to 70%.

---

# 30. Calibration Methods

Potential evaluation:

* Calibration curve
* Reliability diagram
* Brier score where appropriate

Potential calibration methods:

* Platt scaling / sigmoid calibration
* Isotonic calibration

Only use calibration methods when justified by the results.

---

# 31. Calibration Experiment

Compare:

```text
Uncalibrated Model
        vs
Calibrated Model
```

Record:

| Model           | Calibration Method | Brier Score | ROC-AUC | Precision | Recall | Observation |
| --------------- | ------------------ | ----------: | ------: | --------: | -----: | ----------- |
| Optimized Random Forest | None (Raw Probabilities) | 0.1362 | 0.8429 | 0.6866 | 0.4920 | Probabilities are well-calibrated (Brier Score = 0.1362); aligned with empirical churn frequencies across bins. |

Calibration should not be applied merely because it sounds advanced.

---

# 32. E8 — Error Analysis

After selecting promising models, analyze prediction errors.

Focus on:

## False Positives

```text
Predicted churn
Actual non-churn
```

Questions:

* Are these customers unusual?
* Are they concentrated in specific segments?
* Are they borderline cases?
* Does the threshold create excessive false positives?

---

## False Negatives

```text
Predicted non-churn
Actual churn
```

Questions:

* Are high-value churners being missed?
* Are certain customer groups poorly represented?
* Are there behavioral patterns the model fails to capture?

---

# 33. Segment-Level Error Analysis

Where data permits, investigate errors by:

* Tenure
* Contract type
* Customer segment
* Usage level
* Billing characteristics
* Support activity

Do not infer sensitive characteristics unless they are explicitly present and appropriate for analysis.

The goal is to understand model limitations.

---

# 34. E9 — Explainability Experiment

The explainability approach should depend on the final model.

Potential approaches:

### Logistic Regression

* Coefficients
* Coefficient magnitude
* Direction of association

### Tree-Based Models

* Feature importance
* Permutation importance
* SHAP where justified

---

# 35. Global Explainability

Determine which features are most influential across the dataset.

**Implemented Results (Phase 8):**
Extracted Random Forest `feature_importances_` mapped to preprocessor feature names.
Top 5 Global Features:
1. `tenure` (20.21%)
2. `TotalCharges` (14.35%)
3. `MonthlyCharges` (9.15%)
4. `InternetService_Fiber optic` (9.13%)
5. `PaymentMethod_Electronic check` (7.42%)

Artifacts: `reports/results/phase8_global_feature_importance.csv`, `reports/figures/phase8_global_feature_importance.png`

---

# 36. Local Explainability

For individual high-risk customers, identify model-supported contributing factors.

Example:

```text
Customer: C00124
Churn Probability: 0.82

Important model factors:
1. Low tenure
2. High support-contact frequency
3. Recent usage decline
```

The explanation must come from actual model behavior.

Never create explanations manually just to make a prediction look convincing.

---

# 37. Risk Ranking Experiment

The final model should produce a ranked customer list.

Sort customers by:

```text
Predicted churn probability
```

descending.

Evaluate whether high-probability groups actually contain a higher proportion of churned customers.

Where appropriate, analyze:

* Top 5%
* Top 10%
* Top 20%

This helps determine whether the model is useful for prioritization.

---

# 38. Ranking Evaluation

Potential analysis:

| Customer Group | Number of Customers | Mean Predicted Risk | Actual Churn Rate |
| -------------- | ------------------: | ------------------: | ----------------: |
| Top 5%         |                     |                     |                   |
| Top 10%        |                     |                     |                   |
| Top 20%        |                     |                     |                   |
| Remaining      |                     |                     |                   |

This is supplementary to the required classification metrics.

---

# 39. Final Model Selection

The final model should be selected using a multi-factor decision.

Consider:

### 1. Predictive performance

* ROC-AUC
* Precision
* Recall
* F1

### 2. Probability quality

* Calibration

### 3. Stability

* Cross-validation variability
* Generalization gap

### 4. Interpretability

* Explainability quality

### 5. Complexity

* Model size
* Training time
* Inference complexity
* Dependencies

### 6. Business usefulness

* Ability to rank high-risk customers
* Practical precision/recall trade-off

---

# 40. Final Model Decision Record

The final experiment report must include:

```text
Final Model:
[Actual model]

Why selected:
[Evidence-based explanation]

Primary strengths:
[Actual findings]

Trade-offs:
[Actual limitations]

Selected threshold:
[Actual threshold]

Calibration:
[Actual result]

Final test performance:
[Actual metrics]
```

No generic justification should be substituted for actual experiment results.

---

# 41. Final Test Evaluation

Only after all development decisions are complete:

1. Lock the final preprocessing pipeline.
2. Lock the final model.
3. Lock hyperparameters.
4. Lock the threshold.
5. Lock calibration strategy if applicable.
6. Evaluate once on the untouched test set.

Record:

* ROC-AUC
* Precision
* Recall
* F1
* Confusion matrix
* Calibration metric
* Any additional justified metric

---

# 42. Final Experiment Table

The project should eventually contain a final summary similar to:

| Stage       | Model / Strategy    | ROC-AUC | Precision | Recall | F1 | Calibration | Decision |
| ----------- | ------------------- | ------: | --------: | -----: | -: | ----------- | -------- |
| Baseline    | Logistic Regression |         |           |        |    |             |          |
| Comparison  | Decision Tree       |         |           |        |    |             |          |
| Comparison  | Random Forest       |         |           |        |    |             |          |
| Comparison  | Gradient Boosting   |         |           |        |    |             |          |
| Tuning      | Best Candidate      |         |           |        |    |             |          |
| Calibration | Final Candidate     |         |           |        |    |             |          |
| Final       | Selected Model      |         |           |        |    |             |          |

Actual values must be generated by executed experiments.

---

# 43. Experiment Naming Convention

Use consistent experiment IDs.

Recommended:

```text
E00_DATA_AUDIT
E01_BASELINE_LOGREG
E02_DECISION_TREE
E03_RANDOM_FOREST
E04_GRADIENT_BOOSTING
E05_XGBOOST
E06_FEATURE_ENGINEERING
E07_CLASS_IMBALANCE
E08_HYPERPARAMETER_TUNING
E09_THRESHOLD_ANALYSIS
E10_CALIBRATION
E11_ERROR_ANALYSIS
E12_EXPLAINABILITY
E13_FINAL_EVALUATION
```

The list may be shortened if some experiments are unnecessary.

Do not create fake experiment IDs for experiments that were never executed.

---

# 44. Experiment Logging

Every meaningful experiment should record:

```text
Experiment ID
Date / Time
Dataset Version
Feature Set
Preprocessing
Model
Hyperparameters
Random Seed
Validation Strategy
Metrics
Observations
Decision
```

If an experiment changes something important, the reason must be recorded.

---

# 45. Random Seed Policy

Where stochastic algorithms are used:

* Set explicit random seeds.
* Record the seed.
* Keep it consistent for reproducibility.

If multiple seeds are tested to assess stability, record all relevant results.

---

# 46. Reproducibility Requirement

An experiment should be considered reproducible when another execution using the documented environment and configuration can reasonably reproduce the reported result.

Small numerical variation may occur due to:

* Hardware
* Library versions
* Parallelism
* Numerical implementation

Such variation must not be hidden.

---

# 47. Experiment Stopping Rules

Experiments should stop when additional complexity produces little practical value.

Stop adding models when:

* Candidate performance has stabilized.
* Additional models do not answer a meaningful question.
* Time cost exceeds likely benefit.
* The project already satisfies internship requirements.

Stop hyperparameter tuning when:

* Performance improvements become negligible.
* The model begins showing instability.
* Search complexity is no longer justified.

---

# 48. What Counts as a Meaningful Improvement?

A model should not be considered meaningfully better simply because:

```text
ROC-AUC:
0.842 → 0.844
```

Consider:

* Statistical/stability evidence where practical
* Cross-validation variability
* Precision/recall trade-offs
* Calibration
* Interpretability
* Computational cost
* Practical usefulness

Small numerical gains may not justify a substantially more complex model.

---

# 49. Required Visualizations

The experiment report/notebook should contain meaningful visualizations where appropriate.

Potential visualizations:

### Model Evaluation

* ROC curve
* Precision-Recall curve
* Confusion matrix

### Calibration

* Calibration curve

### Model Interpretation

* Feature importance
* SHAP summary where justified

### Threshold Analysis

* Precision vs threshold
* Recall vs threshold
* F1 vs threshold

### Risk Ranking

* Risk distribution
* Actual churn rate by risk group

Not every chart is mandatory.

Only include charts that answer a meaningful question.

---

# 50. Experiment Notebook Structure

If a notebook is used for experimentation, a recommended structure is:

```text
01. Experiment Objective
02. Dataset Loading
03. Data Validation
04. Train/Test Strategy
05. Baseline
06. Candidate Models
07. Feature Engineering
08. Imbalance Experiments
09. Hyperparameter Tuning
10. Threshold Analysis
11. Calibration
12. Error Analysis
13. Explainability
14. Final Model Selection
15. Final Test Evaluation
16. Conclusions
```

The notebook should not become a collection of disconnected code cells.

Each section should explain:

**What was tested → Why → Result → Interpretation → Decision**

---

# 51. Experiment Decision Log

Maintain a concise decision log.

Example:

| Experiment | Finding                                          | Decision                    |
| ---------- | ------------------------------------------------ | --------------------------- |
| E01        | Baseline established                             | Continue                    |
| E02        | Tree overfit                                     | Reject / constrain          |
| E03        | RF improved recall                               | Investigate                 |
| E06        | Feature engineering improved CV                  | Retain selected features    |
| E09        | Lower threshold improved recall but increased FP | Evaluate business trade-off |
| E10        | Calibration improved probability reliability     | Consider calibrated model   |

Only record actual findings after execution.

---

# 52. Mandatory Experiment Questions

Before finalizing the model, answer:

### Data

* Is the target correctly defined?
* Is there leakage?
* Is the dataset sufficiently representative for the project objective?

### Modeling

* What does the baseline achieve?
* Which model families were tested?
* Why was the final model selected?

### Evaluation

* What metric matters most for this use case?
* What is the precision/recall trade-off?
* Is the model overfitting?
* Are probabilities calibrated?

### Errors

* What does the model get wrong?
* Are errors concentrated in particular segments?

### Explainability

* Which features influence predictions?
* Are we accidentally presenting correlation as causation?

### Practical use

* Can customers be meaningfully ranked?
* Is the selected threshold defensible?
* Is the model simple enough to maintain?

---

# 53. Experiment Integrity Rules

AI Studio and all implementation code must follow these rules:

### MUST

* Execute experiments before reporting results.
* Preserve actual outputs.
* Save important metrics.
* Keep experiment logic reproducible.
* Document meaningful decisions.
* Use the same evaluation methodology for fair comparison.
* Protect the final test set.

### MUST NOT

* Generate fake metric tables.
* Fill empty results with plausible numbers.
* Claim a model is better without testing.
* Claim calibration without evaluating calibration.
* Claim feature importance without calculating it.
* Claim successful tuning without running tuning.
* Select a model based only on training performance.
* Modify test data based on model results.

---

# 54. AI Studio Implementation Behavior

When implementing experiments, AI Studio should work incrementally.

Preferred sequence:

```text
Implement E0
    ↓
Run E0
    ↓
Inspect Results
    ↓
Implement E1
    ↓
Run E1
    ↓
Inspect Results
    ↓
Implement E2–E4
    ↓
Compare
    ↓
Select candidates
    ↓
Tune
    ↓
Evaluate
```

Do not generate the entire experimentation pipeline and assume that all results will be correct without execution.

---

# 55. Human Review Checkpoint

After major experiment stages, the implementation should stop for review when practical.

Recommended checkpoints:

### Checkpoint 1

After data audit.

### Checkpoint 2

After baseline.

### Checkpoint 3

After initial model comparison.

### Checkpoint 4

After feature engineering / imbalance experiments.

### Checkpoint 5

After tuning.

### Checkpoint 6

Before final test evaluation.

### Checkpoint 7

After final evaluation.

These checkpoints allow technical review before decisions become difficult to reverse.

---

# 56. Final Experiment Deliverables

The completed project should contain, where appropriate:

* Experiment notebook
* Experiment results
* Model comparison table
* Baseline results
* Final model results
* Threshold analysis
* Calibration analysis
* Error analysis
* Explainability analysis
* Final test evaluation
* Experiment decision log
* Reproducible configuration
* Saved model/pipeline
* Supporting visualizations

---

# 57. Definition of Experimentation Complete

Experimentation is complete only when:

* [ ] Dataset audit completed
* [ ] Evaluation strategy finalized
* [ ] Baseline established
* [ ] Candidate models compared
* [ ] Feature engineering evaluated
* [ ] Class imbalance evaluated
* [ ] Promising model tuned where justified
* [ ] Threshold analyzed
* [ ] Calibration evaluated
* [ ] Error analysis completed
* [ ] Explainability completed where appropriate
* [ ] Final model selected
* [ ] Final test set evaluated
* [ ] Results documented
* [ ] No fabricated results exist
* [ ] Experiment decisions are explainable
* [ ] Reproducibility is verified

---

# 58. Final Principle

The objective of experimentation is not:

> "Find the model with the biggest number."

The objective is:

> **Find a model that provides reliable, generalizable, interpretable and practically useful churn predictions, supported by reproducible experimental evidence.**

Every model, feature, metric, threshold, and engineering decision must have a reason.

**Evidence first. Complexity second.**

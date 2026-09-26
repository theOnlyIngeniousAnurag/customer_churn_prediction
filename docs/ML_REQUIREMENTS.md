# Machine Learning Requirements

## Customer Churn Prediction & Retention Intelligence System

**Project:** Machine Learning Internship Capstone — Project 1
**ML Problem:** Supervised Binary Classification
**Domain:** Customer Churn / Retention Analytics
**Primary Framework:** scikit-learn
**Primary Language:** Python
**Status:** Technical Specification
**Version:** 1.0
**Target Completion:** 30 September 2026

---

# 1. Purpose of This Document

This document defines the technical machine-learning requirements for the Customer Churn Prediction project.

It serves as the ML-specific implementation contract for the project.

The implementation must follow these requirements unless a documented technical reason justifies a change.

Any major deviation from this document should be identified, explained, and reviewed before implementation.

This document complements:

* `PRD.md`
* `PROJECT_SPECIFICATION.md`

The PRD defines the product vision and high-level requirements.

The Project Specification defines the overall system requirements.

This document defines the **machine-learning methodology, data requirements, experimentation, evaluation, and model-quality standards**.

---

# 2. Core ML Objective

The system must predict whether a customer is likely to churn based on information available about that customer.

The primary formulation is:

```text
Input:
Historical / currently available customer information

Output:
P(Customer Churns)
+
Predicted Churn Class
```

Conceptually:

```text
Customer Features
        ↓
Preprocessing
        ↓
Feature Engineering
        ↓
ML Model
        ↓
Churn Probability
        ↓
Classification Threshold
        ↓
Churn / No Churn
```

The probability output is a first-class ML output.

The system should not depend exclusively on binary predictions.

---

# 3. Internship Minimum Requirements

The internship project requires the ML workflow to address:

1. Customer demographics
2. Customer tenure
3. Usage information
4. Support interactions
5. Billing history
6. Missing values
7. Categorical variables
8. Outliers
9. Class imbalance
10. Feature engineering
11. Logistic Regression
12. Tree-based models such as Random Forest or XGBoost
13. ROC-AUC
14. Precision
15. Recall
16. F1-score
17. Calibration
18. High-risk customer ranking
19. Suggested review reasons

These requirements must not be silently omitted.

If the selected dataset does not contain one of the desired categories of information, the limitation must be explicitly documented rather than artificially creating unavailable information.

---

# 4. ML Problem Definition

## 4.1 Learning Type

**Supervised Learning**

## 4.2 Problem Type

**Binary Classification**

## 4.3 Target

The target represents customer churn.

Expected conceptual encoding:

```text
0 → No Churn
1 → Churn
```

The actual dataset encoding must be inspected and explicitly mapped.

Do not assume the target column name.

Do not assume the target encoding.

Do not silently invert labels.

---

# 5. Prediction Unit

The prediction unit should normally be:

**One customer record at the defined prediction point.**

Each row must represent a clearly understood customer observation.

Before modeling, verify:

* Whether one row equals one customer
* Whether customers appear multiple times
* Whether records are snapshots over time
* Whether repeated customers create leakage
* Whether the dataset contains historical observations

If multiple observations per customer exist, the splitting strategy must account for customer identity and temporal structure.

---

# 6. Prediction Time

A conceptual prediction point must be established.

The model should only use information that would realistically be available at the time the churn prediction is made.

Example:

```text
Information available up to T
             ↓
       Prediction
             ↓
      Future churn event
```

Information occurring after the prediction point must not be used as a predictor.

If the dataset does not provide enough temporal information to establish a real prediction point, this limitation must be documented.

---

# 7. Target Validation

Before training, perform a target audit.

Verify:

* Target column
* Target data type
* Unique target values
* Missing target values
* Class labels
* Class frequencies
* Class proportions
* Unexpected values

The implementation must output a concise target summary during the data-validation stage.

Example:

```text
Target column: Churn

Unique values:
0, 1

Class distribution:
No Churn: XXXX
Churn: XXXX

Churn rate: XX.XX%
```

Actual values must come from the selected dataset.

---

# 8. Feature Classification

Every input column should be classified before modeling.

Possible categories:

### Numerical

Examples:

* Tenure
* Monthly charges
* Usage amount
* Support contacts

### Categorical

Examples:

* Contract type
* Payment method
* Customer segment

### Boolean

Examples:

* Has support plan
* Auto-payment enabled

### Datetime

Examples:

* Signup date
* Last activity date

### Identifier

Examples:

* Customer ID

### Potential Target

The churn label.

### Potential Leakage

Columns that contain information unavailable at prediction time.

---

# 9. Identifier Handling

Customer IDs and similar identifiers must not automatically be used as predictive features.

Identifiers should normally be:

* retained for reporting,
* excluded from model features.

If an identifier appears predictive due to accidental encoding or ordering, investigate rather than exploiting it.

The model must learn customer behavior, not arbitrary identifiers.

---

# 10. Data Leakage Requirements

Data leakage prevention is mandatory.

Potential leakage sources include:

* Target-derived features
* Post-churn information
* Future information
* Customer records duplicated across splits
* Preprocessing performed before splitting
* Feature selection using the complete dataset
* Imputation fitted on the complete dataset
* Scaling fitted on the complete dataset
* Oversampling performed before train/test separation
* Hyperparameter tuning using the final test set

The final test set must remain isolated until final evaluation.

---

# 11. Dataset Splitting

The dataset must be divided into appropriate subsets.

Preferred conceptual structure:

```text
Complete Dataset
      │
      ├── Training Set
      │
      ├── Validation / Cross-Validation
      │
      └── Final Test Set
```

The exact split must depend on:

* Dataset size
* Dataset structure
* Temporal information
* Number of observations
* Class distribution

For ordinary non-temporal customer datasets, stratified splitting should generally be considered.

If meaningful timestamps exist, a temporal split should be considered instead of blindly applying a random split.

The final test set must not be used for model selection.

---

# 12. Preprocessing Requirements

Preprocessing must be reproducible and consistent between training and inference.

Where appropriate, use scikit-learn pipelines and/or column transformers.

Conceptual structure:

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
Combined Feature Representation
     ↓
ML Model
```

Preprocessing decisions must be documented.

---

# 13. Missing-Value Handling

Missing values must be investigated before choosing an imputation method.

Analyze:

* Missing count
* Missing percentage
* Columns affected
* Missingness patterns

Potential strategies include:

* Median imputation
* Mean imputation
* Mode imputation
* Constant-category imputation
* Missing-indicator features
* Model-specific handling

The chosen method must be justified based on the feature type and dataset.

Do not blindly fill every missing value with zero.

---

# 14. Categorical Feature Handling

Categorical variables must be encoded appropriately.

Potential methods include:

* One-hot encoding
* Ordinal encoding where genuinely ordinal
* Other appropriate encoding methods when justified

Do not impose artificial numerical ordering on nominal categories.

For example:

```text
Contract:
Month-to-month
One year
Two year
```

should not automatically be encoded as:

```text
0
1
2
```

unless the numerical ordering is genuinely meaningful for the modeling approach.

---

# 15. Numerical Feature Handling

Numerical variables must be inspected for:

* Data type
* Range
* Missing values
* Outliers
* Constant values
* Highly skewed distributions

Scaling should be applied when required by the model.

For example, Logistic Regression generally benefits from appropriately scaled numerical features when feature magnitudes differ substantially.

Tree-based models generally do not require feature scaling.

The preprocessing pipeline should account for these differences.

---

# 16. Outlier Analysis

Outliers must be investigated, not automatically deleted.

Potential methods:

* IQR analysis
* Distribution analysis
* Domain plausibility checks
* Percentile analysis
* Visualization

Possible treatments:

* Keep
* Transform
* Cap/winsorize
* Remove

Any removal or transformation must have a documented justification.

Outlier handling must not be performed simply to improve model metrics.

---

# 17. Class Imbalance Analysis

The target distribution must be examined.

Example:

```text
No Churn → 80%
Churn    → 20%
```

This would represent an imbalanced classification problem.

The project must investigate whether imbalance materially affects model behavior.

Potential approaches include:

### Class Weighting

For example:

```text
class_weight="balanced"
```

where appropriate.

### Sampling

Possible methods:

* Oversampling
* Undersampling
* SMOTE or similar techniques

Sampling must only be performed on the training data.

Never oversample before train/test splitting.

### Threshold Adjustment

Changing the classification threshold may be appropriate when business costs are asymmetric.

---

# 18. Accuracy

Accuracy may be reported as a supplementary metric.

It must not automatically be treated as the primary metric, especially if the dataset is significantly imbalanced.

A model predicting the majority class for every observation could achieve high accuracy while being useless for identifying churners.

---

# 19. Primary Evaluation Metrics

The required evaluation metrics are:

## 19.1 ROC-AUC

Measures the model's ability to rank positive cases above negative cases across thresholds.

Use predicted probabilities/scores rather than only hard predictions.

---

## 19.2 Precision

```text
Precision = TP / (TP + FP)
```

Interpretation:

> Of the customers predicted as churners, how many actually churned?

---

## 19.3 Recall

```text
Recall = TP / (TP + FN)
```

Interpretation:

> Of the customers who actually churned, how many were identified?

Recall is particularly relevant when missing a potential churner is costly.

---

## 19.4 F1-score

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

F1 provides a balance between precision and recall.

---

## 19.5 Calibration

Calibration must be evaluated because the system outputs churn probabilities.

A well-calibrated model should approximately satisfy:

```text
Predicted probability ≈ Observed frequency
```

For example, among customers assigned approximately 0.70 churn probability, the observed churn rate should be reasonably close to 70% over a sufficiently large group.

Potential tools:

* Calibration curve
* Brier score
* Calibration error where appropriate

Do not claim that a model is "well calibrated" based only on a visual impression.

---

# 20. Confusion Matrix

The final evaluation should include a confusion matrix.

It should show:

```text
                  Actual
              No Churn   Churn

Pred No Churn    TN        FN

Pred Churn      FP        TP
```

The confusion matrix should support error analysis.

---

# 21. ROC Curve

Where appropriate, produce an ROC curve for candidate/final models.

The plot should include:

* False Positive Rate
* True Positive Rate
* Model ROC-AUC

The visualization must be accompanied by interpretation.

Do not include charts merely for decoration.

---

# 22. Precision-Recall Analysis

When churn is relatively rare, precision-recall behavior may provide particularly useful information.

Where appropriate, inspect:

* Precision-Recall curve
* Precision at selected thresholds
* Recall at selected thresholds

This should support threshold selection and business interpretation.

---

# 23. Threshold Selection

A classification threshold must be treated as a decision parameter.

Default:

```text
Threshold = 0.50
```

may be used as a baseline.

However, the final threshold should be examined based on:

* Precision
* Recall
* F1
* Number of customers flagged
* False positives
* False negatives
* Retention capacity

The threshold must not be selected using the final test set.

Threshold selection should occur using training/validation data, with final performance reported on the untouched test set.

---

# 24. Baseline Model

The first formal model must be:

**Logistic Regression**

The baseline should be:

* Properly preprocessed
* Reproducible
* Evaluated
* Documented

The baseline establishes a reference against which more complex models can be compared.

---

# 25. Candidate Model Requirements

At least one tree-based model must be evaluated in addition to Logistic Regression.

Recommended candidates:

### Required baseline

Logistic Regression

### Tree-based candidate

Random Forest

### Optional additional candidate

Gradient Boosting / XGBoost / another justified boosting model

The exact selection must depend on:

* Dataset size
* Dataset structure
* Available libraries
* Training time
* Interpretability
* Performance

Do not include XGBoost solely because it sounds more advanced.

---

# 26. Model Experimentation Structure

The experiment sequence should follow:

```text
Experiment 0
Baseline / Simple Benchmark
        ↓
Experiment 1
Logistic Regression
        ↓
Experiment 2
Tree-Based Model
        ↓
Experiment 3
Additional Model if Justified
        ↓
Experiment 4
Hyperparameter Tuning
        ↓
Experiment 5
Final Model / Calibration
```

Each experiment must answer a technical question.

---

# 27. Experiment Record

Every meaningful experiment must record:

* Experiment ID
* Model
* Dataset version
* Features used
* Preprocessing
* Hyperparameters
* Validation strategy
* Random seed where applicable
* Metrics
* Observations
* Limitations
* Decision

Example:

```text
Experiment: EXP-003

Model:
Random Forest

Question:
Does a nonlinear tree-based model improve churn discrimination?

Validation:
Stratified 5-fold CV

Metrics:
ROC-AUC: [actual result]
Precision: [actual result]
Recall: [actual result]
F1: [actual result]

Observation:
[actual observation]

Decision:
[actual decision]
```

Never insert placeholder results into the final report as though they were actual results.

---

# 28. Cross-Validation Requirements

Cross-validation should be used during model development where appropriate.

For ordinary imbalanced classification:

**Stratified K-Fold** should generally be considered.

The number of folds should depend on dataset size.

Typical values may include:

```text
K = 5
```

or another justified value.

Cross-validation must be performed inside the appropriate preprocessing/model pipeline to avoid leakage.

---

# 29. Hyperparameter Tuning

Hyperparameter tuning should be targeted.

Potential parameters:

### Logistic Regression

* Regularization strength
* Solver where relevant
* Class weighting

### Random Forest

* Number of trees
* Maximum depth
* Minimum samples per split
* Minimum samples per leaf
* Maximum features
* Class weighting

### Boosting Models

Tune only parameters relevant to the selected implementation.

The search space should remain computationally reasonable.

---

# 30. Model Selection Criteria

The final model must NOT be selected solely because it has the highest single metric.

Consider:

1. ROC-AUC
2. Precision
3. Recall
4. F1
5. Calibration
6. Generalization
7. Overfitting
8. Interpretability
9. Computational cost
10. Inference complexity
11. Stability
12. Business usefulness

The final selection must be documented.

Example reasoning format:

```text
Model X achieved the highest ROC-AUC, but Model Y provided
better recall and more stable validation performance.

Considering the project's objective of identifying potential
churners, Model Y was selected.
```

The actual conclusion must come from actual experiments.

---

# 31. Overfitting Analysis

Compare training and validation/test performance.

Investigate:

```text
Training Performance
        vs
Validation Performance
        vs
Test Performance
```

Large performance gaps may indicate overfitting.

Do not automatically prefer the most complex model.

---

# 32. Underfitting Analysis

If both training and validation performance are poor, investigate:

* Weak features
* Poor preprocessing
* Incorrect target formulation
* Insufficient model capacity
* Data quality
* Dataset limitations

Do not automatically solve poor performance by increasing model complexity.

---

# 33. Feature Engineering Requirements

Feature engineering should be based on real available data.

Potential features include:

### Usage Trend

If repeated usage measurements exist:

```text
Recent Usage - Earlier Usage
```

### Support Contact Frequency

For example:

```text
Support Contacts / Relevant Time Period
```

### Payment Change

If historical billing data exists:

```text
Recent Payment - Previous Payment
```

### Tenure Groups

Potential categorical grouping of tenure.

### Usage Intensity

A meaningful relationship between usage and customer/account characteristics.

Every engineered feature must have:

* Definition
* Source columns
* Transformation
* Business/technical rationale

---

# 34. Feature Selection

Feature selection should be performed carefully.

Potential approaches:

* Domain reasoning
* Correlation analysis
* Model-based importance
* Permutation importance
* Regularization

Do not remove features solely because they have low pairwise correlation with the target.

Do not select features using the entire dataset in a way that leaks test information.

---

# 35. Feature Importance

After selecting a model, investigate feature importance where appropriate.

Potential methods:

### Logistic Regression

* Coefficients

### Tree Models

* Built-in feature importance

### Model-Agnostic

* Permutation importance

### Advanced

* SHAP

The chosen approach must match the model.

---

# 36. Explainability Requirements

Explainability must be based on actual model outputs.

For individual customers, the system should ideally answer:

```text
Why was this customer assigned elevated churn risk?
```

Possible output:

```text
Customer Risk: High

Important contributing factors:
1. Short tenure
2. High support-contact frequency
3. Low recent usage
```

The system must not invent reasons.

If a factor is not supported by the model's explanation mechanism, it must not be presented as a model reason.

---

# 37. Causality Warning

Model explanations are not causal explanations.

Avoid statements such as:

> "Monthly charges caused the customer to churn."

Prefer:

> "Monthly charges were an important factor in the model's prediction."

The project is predictive, not causal.

---

# 38. Calibration Requirements

Because churn probability is a core output, probability calibration should be investigated.

Possible workflow:

```text
Raw Model
    ↓
Calibration Evaluation
    ↓
Calibration Method if Needed
    ↓
Calibrated Probabilities
```

Potential calibration methods:

* Platt scaling / sigmoid
* Isotonic regression

The calibration method should only be applied when justified by validation results.

Calibration must not be performed using the final test set for model fitting.

---

# 39. Risk Categories

Risk categories may be introduced for user-facing interpretation.

For example:

```text
Low Risk
Medium Risk
High Risk
```

However, category boundaries must be explicitly defined.

Do not present arbitrary thresholds as statistically meaningful without justification.

Possible approaches include:

* Probability-based business thresholds
* Validation-based thresholds
* Quantile-based prioritization

The chosen approach must be documented.

---

# 40. High-Risk Customer Ranking

The system must produce a ranked list of customers by estimated churn risk.

Ranking should be based on predicted churn probability.

Example:

```text
Rank | Customer ID | Probability | Risk
-----------------------------------------
1    | C001        | 0.91        | High
2    | C018        | 0.88        | High
3    | C042        | 0.84        | High
```

The ranking should be generated from the model's actual predictions.

No manually selected customer may be inserted into the ranking.

---

# 41. Review Reason Generation

Suggested review reasons must come from actual customer/model information.

Potential sources:

* Feature values
* Feature importance
* Local explanation
* Domain-supported rules

Example:

```text
High churn risk associated with:
- Low recent usage
- Short tenure
- Frequent support interactions
```

The system must distinguish between:

**Observed customer characteristic**

and:

**Model-derived explanation**

Do not state speculative business causes as facts.

---

# 42. Error Analysis Requirements

The final model must be examined for:

## False Positives

Why are non-churners being flagged?

## False Negatives

Why are actual churners being missed?

## Segment-Level Errors

Where possible, compare errors across meaningful groups.

Examples:

* Contract type
* Tenure group
* Customer segment
* Payment method

Do not infer sensitive personal characteristics or make unsupported claims.

---

# 43. Fairness / Responsible ML Considerations

Where demographic variables are present, investigate whether model performance differs meaningfully across relevant groups where appropriate and ethically permissible.

At minimum:

* Identify potentially sensitive attributes
* Document whether they are used
* Consider whether their inclusion is justified
* Avoid unsupported claims of fairness

Do not remove or include demographic variables solely to make the project appear more sophisticated.

Any fairness analysis must be based on actual data.

---

# 44. Reproducibility Requirements

The ML pipeline must be reproducible.

Required where applicable:

* Fixed random seeds
* Versioned dependencies
* Deterministic preprocessing where possible
* Saved model artifacts
* Saved preprocessing pipeline
* Documented dataset source
* Documented training command
* Documented inference command

Example:

```text
Random Seed: 42
```

The actual seed may differ, but it must be consistently documented.

---

# 45. Model Artifact Requirements

The final trained model should be saved in a reusable format where appropriate.

Prefer saving:

```text
Preprocessing + Model
```

as a single pipeline artifact where practical.

This reduces the risk of preprocessing mismatch between training and inference.

Potential format:

```text
joblib
```

or another appropriate serialization method.

The chosen format must be documented.

---

# 46. Inference Requirements

Inference must apply the exact preprocessing used during training.

Conceptually:

```text
Raw User Input
      ↓
Validation
      ↓
Saved Preprocessing Pipeline
      ↓
Saved Model
      ↓
Probability
      ↓
Risk Category
      ↓
Explanation
```

The inference path must not manually recreate preprocessing differently from training.

---

# 47. Input Validation

The application/inference layer should validate:

* Required fields
* Numeric values
* Categorical values
* Missing inputs
* Invalid ranges
* Unexpected categories

Invalid inputs should produce understandable errors rather than application crashes.

---

# 48. Data Drift Consideration

Full production monitoring is outside the scope of this internship project.

However, the documentation should acknowledge that real-world churn models may experience:

* Customer behavior changes
* Product changes
* Pricing changes
* Distribution shifts
* New customer segments

The project may identify these as future monitoring requirements.

Do not claim production monitoring has been implemented unless it actually has.

---

# 49. Computational Requirements

The solution should remain practical for a standard development machine.

Avoid unnecessarily expensive:

* Hyperparameter searches
* Huge ensembles
* Excessive cross-validation
* Complex model architectures

Computational efficiency should be considered alongside predictive performance.

---

# 50. ML Pipeline Requirement

Where practical, the final training pipeline should resemble:

```text
Data
 ↓
Validation
 ↓
Train/Test Split
 ↓
Preprocessing Pipeline
 ↓
Feature Engineering
 ↓
Model
 ↓
Cross-Validation
 ↓
Hyperparameter Tuning
 ↓
Validation
 ↓
Calibration if justified
 ↓
Final Test Evaluation
 ↓
Model Artifact
```

Feature engineering must be leakage-safe.

---

# 51. Required Final ML Outputs

The final ML implementation should provide, where supported:

### Dataset Analysis

* Dataset dimensions
* Feature types
* Missing-value summary
* Target distribution

### EDA

* Churn distribution
* Relevant numerical distributions
* Relevant categorical analysis
* Meaningful relationships

### Model Results

* Cross-validation results
* Test results
* ROC-AUC
* Precision
* Recall
* F1
* Calibration analysis

### Error Analysis

* Confusion matrix
* False positives
* False negatives

### Explainability

* Global feature importance
* Individual explanations where feasible

### Business Output

* Churn probability
* Risk category
* Ranked high-risk customers
* Review reasons

---

# 52. Required Experiment Comparison

The final project should contain a concise model comparison table.

Recommended structure:

| Model               | CV ROC-AUC | Test ROC-AUC | Precision | Recall | F1 | Calibration | Complexity | Decision |
| ------------------- | ---------: | -----------: | --------: | -----: | -: | ----------- | ---------- | -------- |
| Logistic Regression |            |              |           |        |    |             | Low        |          |
| Random Forest       |            |              |           |        |    |             | Medium     |          |
| Additional Model    |            |              |           |        |    |             |            |          |
| Tuned Final Model   |            |              |           |        |    |             |            |          |

Actual values must only be populated after experiments.

---

# 53. Experiment Interpretation Requirement

Every important experiment must answer:

### What?

What was changed?

### Why?

Why was the change made?

### Result?

What actually happened?

### Interpretation?

What does the result mean?

### Decision?

What should happen next?

This prevents experimentation from becoming random model testing.

---

# 54. No Metric Chasing

The project must not repeatedly modify the pipeline solely to maximize a metric on the validation set.

Avoid:

```text
Try model
↓
Check score
↓
Change random parameter
↓
Check score
↓
Repeat
```

Instead:

```text
Question
↓
Hypothesis
↓
Experiment
↓
Measurement
↓
Interpretation
↓
Decision
```

---

# 55. No Data Leakage for Better Metrics

The following practices are strictly prohibited:

* Using test data during training
* Using test data for feature selection
* Using test data for hyperparameter tuning
* Oversampling before splitting
* Fitting scalers on all data
* Fitting imputers on all data
* Creating target-derived features
* Using future information
* Selecting the final model based on repeated test-set inspection

A lower honest metric is preferable to an inflated invalid metric.

---

# 56. No Fabricated Results

The following must never be fabricated:

* Accuracy
* ROC-AUC
* Precision
* Recall
* F1
* Calibration
* Confusion matrix
* Feature importance
* SHAP values
* Dataset statistics
* Experiment results
* Training time
* Screenshots
* Customer predictions

Every reported result must be generated from an actual execution.

---

# 57. Dataset Limitation Handling

If the selected dataset does not support a requirement from the internship specification, document the limitation.

Example:

```text
The selected dataset does not contain historical support-contact
timestamps. Therefore, a true support-contact frequency trend
could not be derived.
```

Do not manufacture missing information.

---

# 58. Model Limitations

The final documentation should identify limitations such as:

* Dataset size
* Dataset representativeness
* Synthetic or benchmark nature if applicable
* Missing features
* Potential sampling bias
* Lack of temporal information
* Limited behavioral history
* Probability calibration limitations
* Potential distribution shift

The limitations section must reflect actual findings.

---

# 59. Final Model Acceptance Criteria

The final model must satisfy all of the following:

* Uses a valid target
* Uses leakage-safe preprocessing
* Has a documented validation strategy
* Has a baseline comparison
* Has been compared against at least one suitable alternative
* Has actual evaluation results
* Has been evaluated on an untouched test set
* Has precision/recall/F1 analysis
* Has ROC-AUC analysis
* Has calibration analysis
* Has error analysis
* Produces churn probabilities
* Produces customer risk ranking
* Provides evidence-based review reasons
* Is reproducible
* Has documented limitations

---

# 60. Final ML Review Questions

Before Project 1 is declared complete, the reviewer must be able to answer:

### Data

* Do we understand what each feature means?
* Is the target correct?
* Are there missing values?
* Are there duplicates?
* Are there outliers?
* Is the class distribution understood?

### Leakage

* Could any feature contain future information?
* Was preprocessing fitted only on training data?
* Was the test set kept untouched?

### Modeling

* Is Logistic Regression established as a baseline?
* Was at least one tree-based model tested?
* Were models compared fairly?
* Was tuning justified?

### Evaluation

* Are ROC-AUC, precision, recall and F1 reported?
* Was calibration examined?
* Was the threshold considered?
* Was the confusion matrix analyzed?

### Errors

* Do we understand false positives?
* Do we understand false negatives?
* Were meaningful segments examined?

### Explainability

* Can we explain why the model flags a customer?
* Are explanations model-based?
* Are causal claims avoided?

### Reproducibility

* Can another developer reproduce the model?
* Are dependencies documented?
* Is the model artifact saved?
* Is inference consistent with training?

### Business Usefulness

* Can customers be ranked by risk?
* Are review reasons understandable?
* Does the output support a realistic retention workflow?

If the answer to an important question is "no", Project 1 should not yet be marked complete.

---

# 61. Technical Priority Order

When time is limited, implementation priority must be:

```text
1. Correct target definition
        ↓
2. Data quality
        ↓
3. Leakage prevention
        ↓
4. Correct preprocessing
        ↓
5. Baseline
        ↓
6. Model comparison
        ↓
7. Reliable evaluation
        ↓
8. Error analysis
        ↓
9. Explainability
        ↓
10. Risk ranking
        ↓
11. Application
        ↓
12. Additional polish
```

Do not sacrifice ML correctness for UI polish.

---

# 62. ML Engineering Principle

The final system should demonstrate:

**Correct ML methodology + sound experimentation + reliable evaluation + reproducibility + interpretability.**

The objective is not to produce the highest possible metric.

The objective is to produce a model whose:

* assumptions are understood,
* methodology is defensible,
* evaluation is trustworthy,
* limitations are acknowledged,
* predictions are interpretable,
* implementation is reproducible.

---

# 63. Final Principle

> **Never optimize for an impressive-looking ML result at the expense of a technically valid result.**

A model with a slightly lower score but:

* cleaner validation,
* better calibration,
* stronger generalization,
* clearer interpretation,
* simpler implementation,
* and more defensible methodology

may be the more appropriate final model.

The final decision must be based on the actual evidence produced by the experiments.

---

# END OF ML REQUIREMENTS

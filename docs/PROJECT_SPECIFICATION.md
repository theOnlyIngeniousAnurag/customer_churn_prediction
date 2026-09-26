# Project Specification

## Customer Churn Prediction & Retention Intelligence System

**Project:** Machine Learning Internship Capstone — Project 1
**Specification Version:** 1.0
**Status:** Planning / Pre-Implementation
**Author:** Anurag
**Target Completion:** 30 September 2026
**Parent Document:** `PRD.md`

---

# 1. Purpose of This Document

This document translates the Product Requirements Document into a more precise technical and implementation specification.

It defines:

* What the system must do
* What the ML pipeline must contain
* What inputs and outputs are expected
* How experiments should be structured
* How models should be evaluated
* How the application should behave
* What constitutes successful implementation
* What Google AI Studio may and may not change
* What must be verified before the project is considered complete

This document is an implementation specification.

It does not replace `PRD.md`.

When there is a conflict:

```text
PRD.md
   ↓
PROJECT_SPECIFICATION.md
   ↓
Other project documentation
   ↓
Implementation
```

Higher-level requirements take precedence over lower-level implementation details.

---

# 2. Project Objective

Build a complete machine-learning system capable of:

1. Loading a legitimate customer churn dataset.
2. Auditing and understanding the data.
3. Preparing the data without leakage.
4. Engineering meaningful features.
5. Establishing a baseline.
6. Training multiple suitable classification models.
7. Comparing model performance fairly.
8. Tuning promising models where justified.
9. Evaluating the final model on unseen data.
10. Assessing probability calibration.
11. Performing error analysis.
12. Producing customer-level churn probabilities.
13. Ranking customers by predicted churn risk.
14. Providing evidence-based prediction explanations.
15. Exposing useful predictions through a simple application if appropriate.
16. Providing reproducible training and inference.
17. Producing professional project documentation.

---

# 3. Implementation Philosophy

The implementation must follow this principle:

> **Understand → Measure → Build → Validate → Improve → Document**

Do not begin by immediately building the final model.

The implementation must proceed through explicit stages.

```text
Dataset
   ↓
Data Audit
   ↓
Problem Definition
   ↓
EDA
   ↓
Data Split
   ↓
Preprocessing
   ↓
Feature Engineering
   ↓
Baseline
   ↓
Model Experiments
   ↓
Tuning
   ↓
Final Evaluation
   ↓
Error Analysis
   ↓
Explainability
   ↓
Inference
   ↓
Application
   ↓
Testing
   ↓
Documentation
```

---

# 4. Requirement Classification

Every requirement should be classified into one of three levels.

## 4.1 Mandatory

Required for internship completion and project acceptance.

Examples:

* Data preprocessing
* Baseline model
* Multiple suitable models
* Model comparison
* Required metrics
* Risk ranking
* Documentation
* Reproducibility

## 4.2 Recommended

Should be implemented when technically justified and time permits.

Examples:

* Calibration plots
* Threshold analysis
* SHAP
* Permutation importance
* Streamlit dashboard
* Automated tests

## 4.3 Optional

May be implemented only after all mandatory and recommended requirements are stable.

Examples:

* Advanced visual polish
* Additional model families
* Advanced monitoring
* Additional analytics

Optional features must never delay core completion.

---

# 5. System Scope

## 5.1 In Scope

The system includes:

* Customer dataset ingestion
* Data validation
* Exploratory analysis
* Feature preparation
* Feature engineering
* Classification
* Model comparison
* Hyperparameter tuning
* Evaluation
* Probability calibration analysis
* Risk scoring
* Customer ranking
* Explainability
* Model persistence
* Inference
* Optional Streamlit interface
* Documentation
* Testing

## 5.2 Out of Scope

The system does not include:

* Automated retention campaigns
* Automated customer communication
* Automated pricing decisions
* Automated account cancellation
* Production CRM integration
* Real-time customer event streaming
* Enterprise cloud deployment
* Large-scale distributed infrastructure
* Deep learning without strong justification

---

# 6. Dataset Specification

## 6.1 Dataset Selection

The dataset must be selected before substantial model implementation.

The selected dataset must be:

* Real or legitimately published
* Documented
* Accessible
* Relevant to customer churn
* Suitable for supervised classification
* Legally/appropriately usable for the project

The exact dataset must not be assumed before inspection.

---

# 7. Dataset Documentation

After dataset selection, create/update:

`docs/DATASET_AND_DATA_STRATEGY.md`

That document must record:

* Dataset name
* Source
* URL/source reference where applicable
* License/usage information where available
* Number of rows
* Number of columns
* Feature descriptions
* Target column
* Target encoding
* Missing-value information
* Class distribution
* Important limitations
* Potential leakage concerns

No dataset information may be invented.

---

# 8. Data Ingestion Requirements

The ingestion layer must:

1. Load the dataset reliably.
2. Detect file/path problems gracefully.
3. Validate that expected data exists.
4. Report dataset dimensions.
5. Display column names.
6. Identify data types.
7. Identify missing values.
8. Identify duplicate records.
9. Identify target availability.
10. Fail clearly when critical data is missing.

Avoid hard-coded absolute paths tied to one computer.

Prefer project-relative paths or configurable paths.

---

# 9. Data Validation

Before modeling, validate:

### Structure

* Row count
* Column count
* Column names
* Data types

### Target

* Target exists
* Target is not entirely missing
* Target contains expected classes
* Target encoding is understood

### Identifiers

Identify:

* Customer ID
* Other identifier columns
* Columns that should not be treated as predictive features

### Numerical Data

Check:

* Missing values
* Infinite values
* Invalid values
* Extreme values

### Categorical Data

Check:

* Missing categories
* Rare categories
* High-cardinality columns
* Unexpected values

---

# 10. Train / Validation / Test Strategy

The implementation must use a proper separation between:

```text
Training Data
Validation / Cross-Validation
Test Data
```

The test set must remain isolated until final evaluation.

Do not repeatedly tune the model against the final test set.

A suitable default approach is:

```text
Full Dataset
     ↓
Train/Test Split
     ↓
Training Data
     ↓
Cross-Validation
     ↓
Model Selection / Tuning

Test Data
     ↓
Final Evaluation
```

The exact split ratio should be selected based on dataset size and characteristics.

The chosen ratio must be documented.

---

# 11. Random State and Reproducibility

Where applicable:

* Set explicit random seeds.
* Use deterministic behavior where practical.
* Record the random seed.
* Ensure repeated runs produce consistent results within expected numerical variation.

Do not claim perfect determinism when the underlying library/hardware does not guarantee it.

---

# 12. Exploratory Data Analysis Specification

EDA must be performed before final preprocessing decisions.

## 12.1 Required EDA Areas

### Dataset Overview

Show:

* Shape
* Data types
* Summary statistics
* Missing values

### Target Analysis

Show:

* Churn counts
* Churn percentage
* Class imbalance

### Numerical Analysis

Analyze:

* Distributions
* Outliers
* Range
* Skewness where useful

### Categorical Analysis

Analyze:

* Frequency
* Cardinality
* Churn rate across meaningful categories

### Relationship Analysis

Investigate meaningful relationships between features and churn.

### Correlation Analysis

Use correlation analysis where appropriate.

Do not interpret correlation as causation.

---

# 13. EDA Visualization Rules

Every visualization must have an analytical purpose.

Good:

* Churn distribution
* Churn rate by contract type
* Tenure distribution by churn status
* Usage distribution by churn status
* Support interactions vs churn
* Feature relationship plots

Avoid:

* Decorative charts
* Redundant plots
* Dozens of nearly identical charts
* Visualizations that provide no actionable insight

Each important visualization should have a short interpretation.

---

# 14. Preprocessing Specification

Preprocessing must be implemented in a reproducible way.

Where appropriate, use a scikit-learn pipeline and/or column transformer.

Typical components may include:

```text
Numerical Features
    ↓
Imputation
    ↓
Optional Scaling
    ↓
Model

Categorical Features
    ↓
Imputation
    ↓
Encoding
    ↓
Model
```

The exact preprocessing steps must depend on the actual dataset.

---

# 15. Missing Value Handling

Missing values must be analyzed before selecting an imputation method.

Possible approaches include:

* Median imputation
* Mean imputation
* Most-frequent imputation
* Constant-value imputation
* Explicit missing-category handling
* Dataset-specific handling

Do not blindly replace all missing values with zero.

The selected approach must be documented.

---

# 16. Categorical Feature Handling

Categorical variables must be encoded appropriately.

Possible methods include:

* One-hot encoding
* Ordinal encoding where ordering is genuinely meaningful
* Other justified encoding methods

Do not assign arbitrary numerical meaning to nominal categories.

Unknown categories during inference must be handled safely.

---

# 17. Numerical Feature Handling

Numerical features should be inspected for:

* Scale
* Skewness
* Outliers
* Invalid values
* Extreme values

Scaling should be applied when beneficial or required by the selected model.

Tree-based models generally do not require feature scaling, while many linear/distance-based methods can benefit from it.

The implementation should avoid unnecessary transformations.

---

# 18. Outlier Strategy

Outliers must not automatically be removed.

For each important outlier issue, determine whether it represents:

1. Data-entry error
2. Legitimate rare observation
3. Measurement issue
4. Business-relevant extreme behavior

Only justified transformations/removals should be performed.

Document the reasoning.

---

# 19. Feature Engineering Specification

Feature engineering must use information that would legitimately be available at prediction time.

Potential features include:

### Usage

* Average usage
* Usage frequency
* Usage trend
* Recent usage
* Usage change

### Support

* Support-contact frequency
* Recent support interactions
* Complaint frequency

### Billing

* Billing amount
* Payment changes
* Payment behavior
* Billing-to-usage relationships

### Account

* Tenure
* Contract duration
* Subscription characteristics

The actual feature set must depend on the selected dataset.

---

# 20. Feature Leakage Rules

Never create a feature using:

* Target information
* Future information
* Post-churn information
* Information unavailable at prediction time

If the dataset does not contain timestamps or temporal information, do not pretend that historical trends can be calculated.

---

# 21. Baseline Specification

The first predictive model must be a simple baseline.

Preferred baseline:

**Logistic Regression**

The baseline must:

* Use the same fundamental train/test methodology
* Use proper preprocessing
* Produce probabilities
* Be evaluated with the project's primary metrics

The baseline establishes a reference for improvement.

---

# 22. Model Experiment Specification

At minimum, investigate multiple appropriate model families.

A reasonable initial experiment plan is:

```text
Experiment 0
Baseline Logistic Regression

Experiment 1
Decision Tree

Experiment 2
Random Forest

Experiment 3
Gradient Boosting / XGBoost if justified

Experiment 4
Hyperparameter tuning of strongest candidates

Experiment 5
Final calibrated/selected model if appropriate
```

This is an initial plan, not a requirement to implement every model regardless of suitability.

---

# 23. Model Selection Criteria

The final model must NOT be selected using one metric alone.

Consider:

* ROC-AUC
* Precision
* Recall
* F1
* Calibration
* Generalization
* Overfitting
* Interpretability
* Computational cost
* Inference simplicity
* Dataset size
* Business suitability

The final selection must be justified.

---

# 24. Primary Evaluation Metrics

The evaluation layer must report:

### ROC-AUC

Used to evaluate ranking/discrimination performance.

### Precision

Measures the proportion of predicted churners that actually churned.

### Recall

Measures the proportion of actual churners detected by the model.

### F1-score

Balances precision and recall.

### Calibration

Evaluates whether predicted probabilities are meaningful.

---

# 25. Secondary Metrics

Where useful, the project may report:

* Accuracy
* Specificity
* Confusion matrix
* PR-AUC / Average Precision
* Log loss
* Brier score

Secondary metrics must not replace the core internship requirements.

---

# 26. Confusion Matrix

The final evaluation should include a confusion matrix where appropriate.

The matrix should make it possible to understand:

```text
                    Actual
                No Churn | Churn
Predicted
No Churn          TN      | FN
Churn             FP      | TP
```

Use this to support error analysis.

---

# 27. Probability Calibration

Because the system is intended to rank customers by risk, predicted probabilities are important.

Where appropriate, investigate:

* Calibration curve
* Brier score
* Reliability
* Whether calibration improves after calibration methods

Potential calibration approaches may include:

* Platt scaling / sigmoid
* Isotonic regression

Do not apply calibration automatically.

Only use it if the experiment demonstrates value.

---

# 28. Threshold Specification

The system should separate:

### Probability

Continuous model output:

```text
0.00 → 1.00
```

### Classification

Decision derived from a threshold.

The threshold must be configurable.

The project should allow threshold analysis rather than hard-coding 0.5 as the only valid choice.

---

# 29. Class Imbalance Specification

If the dataset is imbalanced:

1. Measure the imbalance.
2. Explain why it matters.
3. Establish a baseline approach.
4. Test appropriate mitigation methods.

Potential approaches:

* Class weights
* Stratified splitting
* Threshold adjustment
* Oversampling/undersampling where justified

Sampling must be performed correctly inside the training workflow to avoid leakage.

Do not oversample the test set.

---

# 30. Hyperparameter Tuning Specification

Tune only meaningful parameters.

Examples:

### Logistic Regression

* Regularization strength
* Solver where relevant

### Decision Tree

* Maximum depth
* Minimum samples per split/leaf
* Criterion where appropriate

### Random Forest

* Number of estimators
* Maximum depth
* Minimum samples
* Feature sampling

### Gradient Boosting

* Learning rate
* Number of estimators
* Tree depth
* Subsampling where appropriate

The actual parameter grid must be adapted to the dataset and model.

---

# 31. Experiment Tracking

Every meaningful experiment must record:

```text
Experiment ID
Model
Preprocessing
Features
Hyperparameters
Validation Method
ROC-AUC
Precision
Recall
F1
Calibration
Observations
Decision
```

Example:

| ID  | Model               | ROC-AUC | Precision | Recall | F1 | Decision  |
| --- | ------------------- | ------: | --------: | -----: | -: | --------- |
| E01 | Logistic Regression |       — |         — |      — |  — | Baseline  |
| E02 | Decision Tree       |       — |         — |      — |  — | Compare   |
| E03 | Random Forest       |       — |         — |      — |  — | Compare   |
| E04 | Tuned Model         |       — |         — |      — |  — | Candidate |

No empty placeholder numbers should be presented as real results.

---

# 32. Error Analysis Specification

After final model selection, inspect:

## False Positives

Questions:

* What customer patterns are common?
* Are these customers genuinely similar to churners?
* Is the model threshold too aggressive?

## False Negatives

Questions:

* What churners are being missed?
* Are there customer groups with systematically poor recall?
* Are there missing predictive signals?

## Segment-Level Analysis

Where dataset fields allow, examine performance across relevant segments.

Do not make unsupported claims about fairness or causality.

---

# 33. Explainability Specification

The project should support global and, where useful, local explanations.

## Global Explanation

Examples:

* Feature importance
* Model coefficients
* Permutation importance
* SHAP summary

## Local Explanation

For an individual customer:

```text
Customer
   ↓
Prediction
   ↓
Probability
   ↓
Important contributing features
```

The explanation must reflect the selected model and method.

---

# 34. Risk Classification

Risk categories should be based on documented thresholds.

For example, conceptually:

```text
Low Risk
Medium Risk
High Risk
```

The exact thresholds must be determined from:

* Model probabilities
* Validation analysis
* Business interpretation

Do not arbitrarily choose thresholds and present them as objectively correct.

---

# 35. High-Risk Customer Ranking

The system must support ranking customers by churn probability.

Required behavior:

1. Generate probabilities.
2. Sort customers descending by probability.
3. Display the highest-risk customers first.
4. Provide relevant customer information.
5. Provide evidence-based factors where available.

The ranking must be generated from the actual trained model.

---

# 36. Inference Specification

Inference must use the same preprocessing logic used during training.

Preferred structure:

```text
Raw Input
   ↓
Validation
   ↓
Saved Preprocessing Pipeline
   ↓
Saved Model
   ↓
Probability
   ↓
Risk
   ↓
Explanation
```

Never manually reproduce training transformations separately in the application if this can cause inconsistencies.

---

# 37. Model Artifact Specification

If a model is persisted, save:

* Preprocessing pipeline
* Trained model
* Required metadata
* Feature information
* Model version where appropriate

Possible formats:

* `joblib`
* `pickle` where appropriate
* Other suitable serialization methods

Avoid loading untrusted serialized model files.

---

# 38. Application Specification

A Streamlit interface may be implemented after the ML pipeline is stable.

The application should prioritize functionality.

## Page / Section 1 — Overview

Show:

* Project description
* Dataset summary
* Churn statistics
* Model summary

## Page / Section 2 — Customer Prediction

Allow appropriate customer inputs.

Display:

* Churn probability
* Risk category
* Prediction
* Explanation

## Page / Section 3 — Risk Ranking

Show:

* Customer ID
* Probability
* Risk
* Important factors where available

## Page / Section 4 — Model Performance

Show:

* Model comparison
* Final metrics
* Confusion matrix
* ROC curve where useful
* Calibration where available

---

# 39. Application Input Validation

The application must handle:

* Missing required inputs
* Invalid numeric values
* Unexpected categories
* Incorrect data types
* Model-loading failures
* Prediction failures

User-facing error messages should be understandable.

Do not expose raw stack traces to ordinary users.

---

# 40. Application Design Principles

The interface should be:

* Clean
* Professional
* Consistent
* Simple
* Data-focused
* Easy to navigate

Avoid excessive:

* Animations
* Decorative effects
* Unnecessary cards
* 3D elements
* Visual clutter

The UI exists to communicate the ML system, not distract from it.

---

# 41. Testing Specification

Testing should cover:

## Data Tests

* Dataset loads
* Required target exists
* Expected columns are available
* Missing-value handling works

## Preprocessing Tests

* Numerical features process correctly
* Categorical features process correctly
* Unknown categories are handled
* Pipeline does not leak test information

## Model Tests

* Model trains
* Prediction works
* Probability prediction works
* Output dimensions are correct

## Inference Tests

* Valid input produces prediction
* Invalid input produces controlled error
* Saved model can be loaded

## Application Tests

* App launches
* Main navigation works
* Prediction works
* Invalid inputs are handled

---

# 42. Acceptance Criteria

The project passes technical acceptance when all mandatory criteria below are satisfied.

## AC-01 — Dataset

A legitimate dataset is loaded and documented.

**Pass condition:** Dataset source, structure, target and limitations are recorded.

---

## AC-02 — Data Audit

Data quality is systematically analyzed.

**Pass condition:** Missing values, duplicates, data types, outliers and target distribution are reviewed.

---

## AC-03 — Leakage Prevention

No known data leakage is present in the modeling pipeline.

**Pass condition:** Preprocessing is fit only on training data and future/target information is not improperly used.

---

## AC-04 — EDA

Meaningful exploratory analysis is completed.

**Pass condition:** EDA identifies relevant patterns and limitations rather than merely displaying charts.

---

## AC-05 — Baseline

A logistic-regression baseline is established.

**Pass condition:** Baseline metrics are recorded.

---

## AC-06 — Model Comparison

Multiple suitable models are evaluated.

**Pass condition:** Results are recorded in an experiment comparison table.

---

## AC-07 — Evaluation

The required evaluation metrics are calculated.

**Pass condition:** ROC-AUC, precision, recall, F1 and calibration are evaluated where technically applicable.

---

## AC-08 — Final Model

A final model is selected using documented reasoning.

**Pass condition:** Selection considers performance and practical factors rather than a single metric.

---

## AC-09 — Error Analysis

Model mistakes are investigated.

**Pass condition:** False positives and false negatives are examined.

---

## AC-10 — Risk Ranking

Customers can be ranked by churn probability.

**Pass condition:** The system generates a valid descending risk ranking.

---

## AC-11 — Explanation

Risk predictions can be interpreted.

**Pass condition:** The system provides evidence-based feature information where technically supported.

---

## AC-12 — Reproducibility

The project can be reproduced from documented instructions.

**Pass condition:** Dependencies, execution steps and model/data workflow are documented.

---

## AC-13 — Application

If a Streamlit application is included:

**Pass condition:** It launches successfully and performs its intended prediction workflow.

---

## AC-14 — Documentation

Documentation accurately reflects the actual implementation.

**Pass condition:** No documented feature or result contradicts the actual code/experiments.

---

## AC-15 — No Fabrication

No fabricated metrics, datasets, experiments, citations or claims exist.

**Pass condition:** All reported results can be traced to actual project artifacts or documented sources.

---

# 43. Definition of Technical Completion

Technical implementation is complete when:

```text
Dataset
   ✓
Data Audit
   ✓
EDA
   ✓
Preprocessing
   ✓
Feature Engineering
   ✓
Baseline
   ✓
Model Comparison
   ✓
Tuning
   ✓
Final Evaluation
   ✓
Error Analysis
   ✓
Explainability
   ✓
Inference
   ✓
Testing
   ✓
```

Only after this point should extensive documentation polish and portfolio packaging occur.

---

# 44. Definition of Final Completion

The project is fully complete only when:

```text
Technical Completion
        +
Application / Demo
        +
Testing
        +
Documentation
        +
GitHub Packaging
        +
Portfolio Materials
        +
Final External Review
        =
PROJECT 1 COMPLETE
```

---

# 45. AI Studio Implementation Boundaries

Google AI Studio is an implementation assistant.

It is NOT the project owner, technical reviewer, or source of truth.

AI Studio must not independently redefine:

* The problem
* The target
* Evaluation methodology
* Dataset requirements
* Model-selection logic
* Project scope
* Acceptance criteria

without explicit approval.

If AI Studio identifies a technically superior alternative, it should:

1. Explain the issue.
2. Explain the proposed alternative.
3. Identify affected files.
4. Wait for approval if the change materially changes the project specification.

Small implementation-level improvements may be made when they do not alter project requirements.

---

# 46. AI Studio Change Control

Before making a major architectural change, AI Studio must identify:

```text
CHANGE REQUEST

Current Approach:
...

Proposed Approach:
...

Reason:
...

Expected Benefit:
...

Trade-offs:
...

Affected Files:
...

Specification Impact:
None / Minor / Major
```

Major changes must not be silently introduced.

---

# 47. AI Studio Implementation Sequence

AI Studio should implement in stages.

### Stage 1

Read project documentation.

### Stage 2

Inspect the current repository.

### Stage 3

Determine dataset strategy.

### Stage 4

Create project structure.

### Stage 5

Implement data ingestion and validation.

### Stage 6

Implement EDA.

### Stage 7

Implement preprocessing.

### Stage 8

Implement baseline.

### Stage 9

Implement model experiments.

### Stage 10

Implement evaluation.

### Stage 11

Implement final model pipeline.

### Stage 12

Implement explainability.

### Stage 13

Implement inference.

### Stage 14

Implement application if required.

### Stage 15

Run tests.

### Stage 16

Update documentation.

Do not attempt to implement the entire project blindly in one uncontrolled generation.

---

# 48. AI Studio Verification Rule

After each major implementation stage, AI Studio must verify:

* Code syntax
* Imports
* File paths
* Functionality
* Consistency with project documentation
* Reproducibility
* No accidental regressions

If execution is available through the development environment, actual execution should be preferred over assuming correctness.

---

# 49. Results Integrity Rule

AI Studio must NEVER:

* Invent metrics
* Invent screenshots
* Invent model performance
* Invent test results
* Invent dataset statistics
* Invent experiment conclusions
* Invent citations
* Present expected output as actual output

If a result has not been executed or verified, it must be clearly marked as:

> Not yet measured.

or equivalent.

---

# 50. Documentation Synchronization

Whenever implementation materially changes:

* Architecture
* Model strategy
* Dataset
* Evaluation methodology
* Application behavior
* Dependencies

the relevant documentation must be updated.

Documentation must describe the actual project, not the intended project if implementation has diverged.

---

# 51. Repository Integrity

AI Studio must avoid unnecessary modifications to unrelated files.

Before changing an existing file:

1. Understand its purpose.
2. Check dependencies.
3. Preserve working functionality.
4. Make the smallest reasonable change.

Do not rewrite functioning modules simply because another implementation style is preferred.

---

# 52. Code Generation Rules

Generated code must be:

* Readable
* Modular
* Maintainable
* Reasonably documented
* Consistent
* PEP 8-conscious where applicable
* Free from unnecessary duplication

Avoid:

* Giant functions
* Giant scripts
* Repeated preprocessing logic
* Hard-coded absolute paths
* Magic numbers without explanation
* Dead code
* Unused dependencies
* Unused variables
* Unnecessary abstraction

---

# 53. Notebook Rules

Notebooks are for:

* EDA
* Experiments
* Analysis
* Visualization
* Results interpretation

Reusable production logic should preferably live in `src/`.

Avoid duplicating the same preprocessing/training logic in multiple notebooks.

The notebook should be understandable from top to bottom.

---

# 54. Source Code Rules

Reusable logic should be placed in modules such as:

```text
src/
├── data/
├── features/
├── models/
├── evaluation/
└── utils/
```

Exact organization may be adjusted based on implementation needs.

The goal is separation of concerns, not folder-count maximization.

---

# 55. Configuration Rules

Configuration values should not be scattered throughout the code.

Where useful, centralize:

* Random seed
* Dataset paths
* Model parameters
* Threshold
* Output directories

Avoid creating an unnecessarily complex configuration system.

---

# 56. Dependency Rules

Only dependencies that are actually required should be added.

Potential core dependencies may include:

* Python
* pandas
* NumPy
* scikit-learn
* matplotlib
* seaborn

Additional dependencies may be introduced only when justified, such as:

* XGBoost
* SHAP
* Streamlit
* joblib

The final `requirements.txt` must contain the dependencies actually required to run the project.

---

# 57. Security and Privacy

The project must not contain:

* API keys
* Passwords
* Personal credentials
* Private customer information
* Authentication secrets

Secrets must not be committed to GitHub.

Use environment variables when secrets are genuinely required.

---

# 58. Performance Requirements

The project is an internship-scale ML system.

Prioritize:

* Correctness
* Reliability
* Reproducibility
* Reasonable execution time

Do not optimize prematurely.

Performance optimization should be considered only when there is an observed bottleneck.

---

# 59. Git Checkpoints

Implementation should be organized into logical milestones.

Suggested checkpoints:

```text
commit: initialize project structure
commit: add dataset and data validation
commit: complete exploratory analysis
commit: add preprocessing pipeline
commit: add baseline model
commit: add model experiments
commit: add tuning and evaluation
commit: add explainability
commit: add inference pipeline
commit: add application
commit: complete testing and documentation
```

Actual commit names may differ.

---

# 60. Final Technical Review

Before Project 1 is marked complete, review the project as:

### ML Engineer

Is the methodology technically correct?

### Data Scientist

Are experiments and metrics meaningful?

### Software Engineer

Is the code maintainable?

### Technical Reviewer

Can every important decision be defended?

### Recruiter

Does the repository demonstrate genuine capability?

### Interviewer

Can the author explain:

* Why this dataset?
* Why this target?
* Why these features?
* Why these models?
* Why these metrics?
* Why this final model?
* Where does the model fail?
* What would be improved next?

If the answer to these questions is unclear, the project requires further work.

---

# 61. Final Acceptance Checklist

Before declaring:

**PROJECT 1 — COMPLETE**

verify:

* [ ] All mandatory requirements satisfied
* [ ] Dataset legitimate and documented
* [ ] No data leakage
* [ ] EDA complete
* [ ] Preprocessing reproducible
* [ ] Feature engineering justified
* [ ] Logistic baseline complete
* [ ] Multiple models compared
* [ ] Hyperparameter tuning justified
* [ ] Required metrics reported
* [ ] Calibration evaluated
* [ ] Error analysis completed
* [ ] Final model selected and justified
* [ ] Risk ranking works
* [ ] Explanations work
* [ ] Inference works
* [ ] Application works if included
* [ ] Tests pass
* [ ] Dependencies documented
* [ ] README complete
* [ ] GitHub structure clean
* [ ] Results verified
* [ ] No fabricated claims
* [ ] Portfolio material prepared
* [ ] Final technical review passed

---

# 62. Final Principle

The implementation must demonstrate:

**Machine Learning Understanding**

*

**Sound Experimental Methodology**

*

**Clean Software Engineering**

*

**Reproducibility**

*

**Interpretability**

*

**Professional Presentation**

The objective is not to create the largest project.

The objective is to create a project that is:

> **Technically correct, experimentally defensible, reproducible, explainable, professionally engineered, and genuinely understood by its author.**

---

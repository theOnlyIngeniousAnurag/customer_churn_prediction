# System Architecture Document

## Customer Churn Prediction & Retention Intelligence System

**Project Type:** Machine Learning Internship Capstone
**Domain:** Customer Analytics / Subscription Retention
**Architecture Version:** 1.2
**Status:** Phase 5 Complete (Tree-Based Model Benchmarking)
**Author:** Anurag
**Target Completion:** 30 September 2026

---

# 1. Purpose of This Document

This document defines the technical architecture for the Customer Churn Prediction & Retention Intelligence System.

It translates the requirements defined in:

* `PRD.md`
* `PROJECT_SPECIFICATIONS.md`
* `ML_REQUIREMENTS.md`
* `DATASET_AND_DATA_STRATEGY.md`
* `EXPERIMENT_PLAN.md`

into a coherent implementation architecture.

This document defines:

* System boundaries
* Data flow
* ML pipeline
* Training architecture
* Inference architecture
* Application architecture
* Module responsibilities
* Data and model artifacts
* Configuration strategy
* Testing boundaries
* Reproducibility requirements
* Separation of concerns
* Architectural constraints

The architecture must remain adaptable until the actual dataset has been inspected.

Do not invent dataset-specific architecture before the dataset is understood.

---

# 2. Architectural Philosophy

The system should follow these principles:

1. **Separation of concerns**
2. **Reproducibility**
3. **Leakage prevention**
4. **Modularity**
5. **Interpretability**
6. **Testability**
7. **Maintainability**
8. **Simplicity over unnecessary complexity**
9. **Training/inference consistency**
10. **Clear separation between experimentation and reusable production-style code**

The project should demonstrate good ML engineering practices without pretending to be a large-scale production platform.

---

# 3. High-Level System Architecture

The overall architecture is:

```text
                    ┌──────────────────────┐
                    │     Raw Dataset      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Ingestion &     │
                    │ Validation           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Quality &       │
                    │ Profiling            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Train / Validation / │
                    │ Test Split           │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │ Feature         │          │ Target          │
       │ Processing      │          │ Preparation     │
       └────────┬────────┘          └────────┬────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Preprocessing +      │
                    │ Feature Engineering  │
                    │ Pipeline             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Baseline Model       │
                    │ Logistic Regression  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Model Experiments    │
                    │ & Comparison         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Hyperparameter       │
                    │ Tuning               │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Final Model          │
                    │ Selection            │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼───────────────┐
                │              │               │
                ▼              ▼               ▼
       ┌─────────────┐ ┌──────────────┐ ┌──────────────┐
       │ Evaluation  │ │ Explainability│ │ Calibration  │
       └──────┬──────┘ └──────┬───────┘ └──────┬───────┘
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                    ┌──────────────────────┐
                    │ Model Artifact +     │
                    │ Metadata             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Inference Layer      │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼───────────────┐
                │              │               │
                ▼              ▼               ▼
       ┌─────────────┐ ┌──────────────┐ ┌──────────────┐
       │ Customer    │ │ Risk Ranking │ │ Explanations │
       │ Prediction  │ │              │ │              │
       └─────────────┘ └──────────────┘ └──────────────┘
                │              │               │
                └──────────────┼───────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Dashboard  │
                    │ / Demo Interface     │
                    └──────────────────────┘
```

The Streamlit layer is optional and must only be implemented if it provides meaningful value.

---

# 4. Architectural Layers

The system is divided into the following logical layers:

```text
┌─────────────────────────────────────┐
│ Presentation Layer                  │
│ Streamlit / User Interface          │
├─────────────────────────────────────┤
│ Inference Layer                     │
│ Prediction / Risk / Explanation     │
├─────────────────────────────────────┤
│ Model Layer                         │
│ Trained Model / Calibration         │
├─────────────────────────────────────┤
│ ML Pipeline Layer                   │
│ Preprocessing / Features / Training │
├─────────────────────────────────────┤
│ Evaluation Layer                    │
│ Metrics / Errors / Experiments      │
├─────────────────────────────────────┤
│ Data Layer                          │
│ Raw / Processed / Validation        │
└─────────────────────────────────────┘
```

Each layer should have a clearly defined responsibility.

---

# 5. Data Layer

## 5.1 Purpose

The data layer manages the input dataset and derived data artifacts.

Recommended structure:

```text
data/
├── raw/
└── processed/
```

---

## 5.2 Raw Data

`data/raw/` should contain the original dataset or a locally stored copy where permitted.

Raw data must not be silently modified.

If the dataset license or distribution method requires downloading it separately, the repository should document the acquisition process rather than committing restricted data.

---

## 5.3 Processed Data

`data/processed/` may contain derived datasets generated during the workflow.

Examples:

* Cleaned data
* Feature-engineered data
* Train/validation/test datasets

However, processed data should not become a hidden source of truth.

The transformation pipeline must remain reproducible from the original dataset whenever practical.

---

# 6. Data Ingestion Layer

## Responsibility

The ingestion layer should:

1. Locate/load the dataset.
2. Validate that the expected input exists.
3. Load data into an appropriate representation.
4. Perform basic structural checks.
5. Report useful errors when data is missing or malformed.

Example conceptual interface:

```python
def load_data(path):
    ...
```

The implementation should not contain extensive preprocessing logic.

---

# 7. Data Validation Layer

Before ML processing begins, the system should validate:

* Dataset existence
* Required columns
* Data types
* Row count
* Column count
* Target availability
* Missing target values
* Duplicate identifiers where applicable
* Unexpected target values

Validation failures should produce understandable error messages.

The system should fail early when critical input assumptions are violated.

---

# 8. Data Profiling Layer

The profiling/EDA layer is primarily intended for analysis and experimentation.

It should investigate:

```text
Dataset Structure
       ↓
Missing Values
       ↓
Duplicates
       ↓
Data Types
       ↓
Target Distribution
       ↓
Numerical Distributions
       ↓
Categorical Distributions
       ↓
Relationships
       ↓
Outliers
       ↓
Potential Leakage
```

EDA code may live primarily in notebooks while reusable transformations should live in `src/`.

---

# 9. Data Splitting Architecture

The dataset must be separated before learned preprocessing is fitted.

Conceptually:

```text
Full Dataset
     │
     ▼
Train / Validation / Test
     │
     ├──────────────► Training
     │
     ├──────────────► Validation / CV
     │
     └──────────────► Final Test
```

The exact split strategy must follow `ML_REQUIREMENTS.md` and `EXPERIMENT_PLAN.md`.

The final test set must remain isolated until final evaluation.

---

# 10. Preprocessing Architecture

Preprocessing should be implemented as a reusable pipeline rather than scattered transformations.

Conceptually:

```text
Raw Features
     │
     ├── Numerical Features
     │       ↓
     │   Imputation
     │       ↓
     │   Optional Scaling
     │
     └── Categorical Features
             ↓
         Imputation
             ↓
         Encoding
             │
             └──────────────┐
                            ▼
                    Combined Features
                            │
                            ▼
                     ML Model
```

The exact transformations must depend on the actual dataset.

Do not assume all datasets require every preprocessing operation.

---

# 11. Feature Engineering Layer

Feature engineering should be implemented separately from raw data loading.

Conceptual responsibility:

```text
Clean Input Data
       ↓
Feature Engineering
       ↓
Model-Ready Features
```

Potential feature groups include:

* Usage behavior
* Tenure
* Support interactions
* Billing behavior
* Recency
* Frequency
* Ratios
* Trends

Every engineered feature must have:

1. Clear definition
2. Business/technical rationale
3. No leakage
4. Reproducible implementation

---

# 12. Feature Naming

Feature names should be:

* Descriptive
* Consistent
* Machine-readable
* Stable

Avoid meaningless names such as:

```text
feature1
feature2
x1
x2
```

unless they are generated by a transformation system where the mapping is documented.

---

# 13. ML Pipeline Architecture

The central ML architecture should conceptually follow:

```text
Input Data
    ↓
Feature Engineering
    ↓
Preprocessing
    ↓
Model
    ↓
Probability Prediction
    ↓
Threshold / Risk Logic
    ↓
Output
```

Where appropriate, preprocessing and the estimator should be combined into a single scikit-learn pipeline or equivalent reproducible structure.

This prevents training and inference from using inconsistent transformations.

---

# 14. Baseline Architecture

The first model should be a simple baseline.

Preferred baseline:

```text
Preprocessing
      ↓
Logistic Regression
      ↓
Validation
      ↓
Metrics
```

The baseline establishes the reference point against which later models are evaluated.

---

# 15. Model Experiment Architecture

Each candidate model should use the same underlying evaluation methodology whenever technically appropriate.

Conceptually:

```text
                    ┌── Logistic Regression
                    │
Prepared Features ──┼── Decision Tree
                    │
                    ├── Random Forest
                    │
                    └── Boosting Model
                              │
                              ▼
                     Common Evaluation
                              │
                              ▼
                     Experiment Results
```

The objective is fair comparison rather than simply trying many models.

---

# 16. Model Selection Architecture

Final model selection must consider more than a single metric.

Selection should consider:

* ROC-AUC
* Precision
* Recall
* F1
* Calibration
* Generalization
* Error patterns
* Interpretability
* Computational cost
* Inference simplicity
* Business suitability

The highest individual metric must not automatically determine the final model.

---

# 17. Hyperparameter Tuning Architecture

Tuning should occur only after baseline and candidate-model evaluation.

Recommended flow:

```text
Baseline
   ↓
Candidate Models
   ↓
Identify Promising Models
   ↓
Hyperparameter Search
   ↓
Cross-Validation
   ↓
Compare Tuned Models
   ↓
Final Candidate
```

Tuning must be performed only using training/development data.

The final test set must not influence hyperparameter selection.

---

# 18. Evaluation Layer

The evaluation layer should provide reusable functions for metrics and analysis.

Conceptual responsibilities:

```text
Predictions
    │
    ├── ROC-AUC
    ├── Precision
    ├── Recall
    ├── F1
    ├── Confusion Matrix
    ├── Calibration
    └── Threshold Analysis
```

Example conceptual interfaces:

```python
evaluate_classification(...)
calculate_metrics(...)
plot_confusion_matrix(...)
evaluate_calibration(...)
analyze_thresholds(...)
```

Actual implementation should remain consistent with the experiment plan.

---

# 19. Error Analysis Architecture

Error analysis should operate after generating predictions.

Conceptually:

```text
Test Predictions
       │
       ├──────────────► True Positives
       │
       ├──────────────► True Negatives
       │
       ├──────────────► False Positives
       │
       └──────────────► False Negatives
                              │
                              ▼
                     Segment Analysis
```

Where the dataset permits, analyze errors by meaningful customer attributes.

Do not modify the test set based on observed errors.

---

# 20. Calibration Architecture

Because the system produces churn probabilities, calibration is an important component.

Conceptually:

```text
Raw Model Probability
          ↓
Calibration Evaluation
          ↓
Is Probability Reliable?
          │
          ├── Yes → Use
          │
          └── No → Investigate Calibration
```

If calibration is improved using a calibration method, that calibration process must itself be trained only using appropriate development data.

The system must distinguish:

* Classification prediction
* Probability estimation
* Risk categorization

These are related but not identical concepts.

---

# 21. Threshold & Risk Architecture

The prediction layer should separate probability generation from thresholding.

```text
Customer Features
       ↓
Model
       ↓
Churn Probability
       ↓
Threshold Logic
       ↓
Predicted Class
       ↓
Risk Category
```

Example:

```text
Probability
     │
     ├── Low Risk
     ├── Medium Risk
     └── High Risk
```

The actual thresholds must be defined based on analysis and documented.

Do not hard-code arbitrary thresholds without justification.

---

# 22. Explainability Architecture

Explainability should be treated as a separate component.

```text
Customer Input
      ↓
Final Model
      ↓
Prediction
      │
      └──────────────► Explanation Engine
                              │
                              ▼
                         Key Factors
```

Potential methods:

* Logistic regression coefficients
* Feature importance
* Permutation importance
* SHAP

The method must be selected according to the final model.

Explanations must be faithful to the actual model.

---

# 23. Customer Risk Ranking Architecture

Risk ranking operates on model probabilities.

```text
Customer Dataset
       ↓
Model Prediction
       ↓
Churn Probability
       ↓
Sort Descending
       ↓
Ranked Customers
```

Output example:

```text
Rank | Customer | Probability | Risk
--------------------------------------
1    | C001     | 0.91        | High
2    | C017     | 0.87        | High
3    | C042     | 0.82        | High
```

The ranking should be reproducible from the same model and input data.

---

# 24. Inference Architecture

Training and inference must be separate operations.

## Training

```text
Dataset
   ↓
Training Pipeline
   ↓
Trained Model
   ↓
Model Artifact
```

## Inference

```text
New Customer Data
       ↓
Saved Pipeline / Model
       ↓
Prediction
       ↓
Probability
       ↓
Risk
       ↓
Explanation
```

The inference layer must use the same preprocessing logic used during training.

Never manually recreate preprocessing independently in the application.

---

# 25. Model Artifact Architecture

The final trained pipeline/model should be persisted as a versioned artifact where practical.

Conceptually:

```text
models/
├── final_model.*
├── model_metadata.json
└── ...
```

The artifact should be accompanied by metadata where useful, such as:

* Model type
* Feature version
* Training date
* Dataset identifier/version
* Selected threshold
* Evaluation metrics
* Library/environment information

Do not store fabricated metadata.

---

# 26. Application Architecture

If Streamlit is implemented, the application should be a thin presentation layer over the reusable inference logic.

Recommended architecture:

```text
Streamlit UI
     ↓
Input Validation
     ↓
Inference Service
     ↓
Saved ML Pipeline
     ↓
Prediction
     ↓
Risk + Explanation
     ↓
UI Output
```

The Streamlit interface should NOT contain:

* Model training
* Hyperparameter tuning
* Large EDA operations
* Duplicate preprocessing logic
* Experimental code

The application should consume the already-trained model.

---

# 27. Streamlit Application Components

If implemented, the UI may contain:

```text
Application
│
├── Overview
│
├── Customer Prediction
│
├── Risk Ranking
│
├── Model Insights
│
└── About / Methodology
```

The exact pages should depend on the final scope.

---

# 28. Input Validation

Application inputs must be validated before inference.

Examples:

* Missing required fields
* Invalid numerical values
* Invalid categories
* Impossible values
* Incorrect data types

Invalid input should produce a clear user-facing message.

The application must fail gracefully rather than producing misleading predictions.

---

# 29. Application Error Handling

The application should handle:

* Missing model artifact
* Invalid input
* Missing required feature
* Corrupt model file
* Unexpected data type
* Prediction errors

Errors should be understandable without exposing unnecessary internal stack traces to normal users.

Detailed technical errors may be logged during development.

---

# 30. Configuration Architecture

Configuration should be centralized where useful.

Potential configuration values include:

* Dataset path
* Model path
* Random seed
* Output directory
* Selected threshold
* Application settings

Avoid scattering configuration constants throughout the codebase.

Do not hard-code machine-specific absolute paths.

---

# 31. Recommended Source Structure

The final implementation may use:

```text
src/
│
├── data/
│   ├── __init__.py
│   ├── ingestion.py
│   └── validation.py
│
├── features/
│   ├── __init__.py
│   ├── preprocessing.py
│   └── engineering.py
│
├── models/
│   ├── __init__.py
│   ├── train.py
│   ├── predict.py
│   └── selection.py
│
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py
│   ├── calibration.py
│   └── error_analysis.py
│
└── utils/
    ├── __init__.py
    └── configuration.py
```

This is a recommended starting point, not an inflexible requirement.

The actual structure may be simplified if the final project does not require all modules.

---

# 32. Notebook Architecture

Notebooks should primarily support:

* Exploration
* EDA
* Visualization
* Experimentation
* Analysis
* Presentation of findings

They should not become the only source of reusable production logic.

Recommended:

```text
notebooks/
├── 01_data_exploration.ipynb
├── 02_feature_analysis.ipynb
├── 03_model_experiments.ipynb
└── 04_final_evaluation.ipynb
```

The number of notebooks may be reduced if a smaller structure is clearer.

Avoid excessive notebook fragmentation.

---

# 33. Experiment Tracking Architecture

Every meaningful experiment should record:

```text
Experiment ID
Model
Features
Preprocessing
Parameters
Validation Method
Metrics
Observations
Decision
```

A simple CSV/JSON/Markdown-based experiment log is acceptable.

A heavyweight experiment-tracking platform is not required unless clearly justified.

---

# 34. Testing Architecture

Testing should be organized around the highest-risk components.

Potential structure:

```text
tests/
├── test_data.py
├── test_features.py
├── test_model.py
├── test_inference.py
└── test_app.py
```

Testing priorities:

### Data Tests

* Dataset loading
* Expected columns
* Target validation

### Feature Tests

* Correct transformation
* No unexpected missing output
* Consistent feature schema

### Model Tests

* Model trains
* Prediction shape is correct
* Probability values are valid

### Inference Tests

* Saved model loads
* Valid input produces output
* Invalid input is handled

### Application Tests

* UI launches
* Prediction workflow works
* Errors are handled

---

# 35. Reproducibility Architecture

The complete workflow should ideally be reproducible:

```text
Dataset
   ↓
Configuration
   ↓
Preprocessing
   ↓
Feature Engineering
   ↓
Training
   ↓
Evaluation
   ↓
Model Artifact
   ↓
Inference
```

Reproducibility requirements include:

* Fixed random seeds where appropriate
* Documented dependencies
* Deterministic processing where practical
* Documented dataset source
* Stable preprocessing
* Saved model pipeline
* Clear execution instructions

---

# 36. Dependency Architecture

The project should use a minimal dependency set.

Expected core ecosystem may include:

```text
Python
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
streamlit (if application is implemented)
```

Additional libraries such as:

* XGBoost
* SHAP
* imbalanced-learn

should only be added when their use is technically justified.

Do not add dependencies merely because they are popular.

The final `requirements.txt` must contain only dependencies actually required by the project.

---

# 37. Security and Privacy Considerations

The project should avoid storing sensitive real customer information.

If the selected dataset contains personally identifiable information:

* Avoid exposing unnecessary PII
* Do not publish sensitive customer information
* Remove unnecessary identifiers where appropriate
* Avoid committing private data to GitHub

The repository must not contain:

* API keys
* Passwords
* Access tokens
* Private credentials
* Sensitive customer information

---

# 38. Git Architecture

Git should track:

```text
Source Code
Notebooks
Configuration
Documentation
Tests
Application Code
Requirements
```

Git should generally ignore:

```text
Raw/private data
Large generated artifacts
Virtual environments
Caches
Secrets
Temporary files
Local IDE files
```

The exact Git strategy is defined separately in:

`GIT_GITHUB_STRATEGY.md`

---

# 39. Documentation Architecture

Documentation should be layered.

```text
README.md
   │
   ├── Project Overview
   ├── Setup
   ├── Usage
   └── Results
          │
          ▼
docs/
   ├── PRD.md
   ├── PROJECT_SPECIFICATION.md
   ├── ML_REQUIREMENTS.md
   ├── DATASET_AND_DATA_STRATEGY.md
   ├── EXPERIMENT_PLAN.md
   ├── ARCHITECTURE.md
   ├── RULES.md
   ├── CODING_STANDARDS.md
   ├── GIT_GITHUB_STRATEGY.md
   ├── TASK_TRACKER.md
   └── QUALITY_ASSURANCE.md
```

Documentation should describe the actual project state.

If implementation changes, relevant documentation should be updated.

---

# 40. Separation Between Experimentation and Final Pipeline

A critical architectural principle is:

```text
Exploration ≠ Production Logic
```

Notebooks may contain exploratory code.

Reusable transformations should eventually move into `src/`.

For example:

Bad:

```text
Notebook
 ├── Load data
 ├── Clean data
 ├── Train
 ├── Copy preprocessing
 └── Predict
```

Preferred:

```text
Notebook
     ↓
calls reusable src modules
     ↓
src/
 ├── preprocessing
 ├── features
 ├── training
 └── evaluation
```

This reduces duplication and improves reproducibility.

---

# 41. Training vs Inference Contract

The training pipeline must define the exact feature contract expected by inference.

Conceptually:

```text
Training Feature Schema
        │
        ▼
Preprocessing
        │
        ▼
Model
```

and:

```text
Inference Feature Schema
        │
        ▼
Same Preprocessing
        │
        ▼
Same Model
```

Training and inference must not silently use different feature definitions.

---

# 42. Architecture Decision Rules

When architectural choices are uncertain, follow this priority:

```text
Correctness
    >
Reproducibility
    >
Maintainability
    >
Interpretability
    >
Simplicity
    >
Performance Optimization
    >
Visual Complexity
```

A more complicated architecture is justified only when it provides a measurable or clearly defensible benefit.

---

# 43. What Must NOT Be Implemented

Unless a later requirement specifically justifies it, do not introduce:

* Microservices
* Kubernetes
* Message queues
* Distributed computing
* Complex cloud infrastructure
* Real-time streaming
* Deep-learning infrastructure
* Unnecessary APIs
* Multiple databases
* Authentication systems
* Payment systems
* Automated CRM integration

The project is an ML capstone, not an enterprise distributed system.

---

# 44. Architecture Adaptation Rule

This document defines the initial architecture.

After the dataset is selected and inspected, the architecture may be revised if the actual data requires it.

Examples:

* Dataset lacks time information → remove temporal feature assumptions.
* Dataset contains only categorical data → simplify numerical preprocessing.
* Dataset is small → avoid unnecessarily complex models.
* Dataset is highly imbalanced → strengthen imbalance handling.
* Dataset contains repeated customer records → reconsider splitting strategy.
* Dataset contains potential temporal information → investigate temporal leakage.

Any significant architectural change should be documented.

---

# 45. Architecture Validation Checklist

Before implementation is considered structurally complete, verify:

### Data

* [ ] Data ingestion defined
* [ ] Data validation defined
* [ ] Data quality workflow defined
* [ ] Data leakage controls defined

### ML

* [ ] Train/validation/test strategy defined
* [ ] Preprocessing architecture defined
* [ ] Feature engineering boundary defined
* [ ] Baseline architecture defined
* [ ] Candidate-model architecture defined
* [ ] Tuning architecture defined
* [ ] Evaluation architecture defined
* [ ] Error-analysis architecture defined
* [ ] Explainability architecture defined
* [ ] Calibration architecture defined

### Inference

* [ ] Model artifact strategy defined
* [ ] Prediction flow defined
* [ ] Risk-ranking flow defined
* [ ] Explanation flow defined
* [ ] Training/inference consistency defined

### Application

* [ ] UI boundary defined
* [ ] Input validation defined
* [ ] Error handling defined
* [ ] Application does not duplicate ML logic

### Engineering

* [ ] Source structure defined
* [ ] Notebook strategy defined
* [ ] Testing boundaries defined
* [ ] Dependency strategy defined
* [ ] Configuration strategy defined
* [ ] Git boundaries defined

### Documentation

* [ ] Architecture documented
* [ ] Major decisions traceable
* [ ] Architecture can evolve after dataset inspection

---

# 46. Final Architectural Principle

The Customer Churn Prediction system should be architected as a:

> **Modular, reproducible, leakage-safe, interpretable machine-learning decision-support application.**

The architecture should remain intentionally lightweight.

The objective is not to demonstrate how many technologies can be connected together.

The objective is to demonstrate that the author understands how to move from:

```text
Real-World Problem
       ↓
Data
       ↓
ML Formulation
       ↓
Reliable Pipeline
       ↓
Experiments
       ↓
Evaluation
       ↓
Interpretation
       ↓
Prediction
       ↓
Decision Support
```

Every architectural component must serve that objective.

---

# 47. Implementation Instruction

Before implementing substantial code:

1. Read this architecture document completely.
2. Read all other project control documents.
3. Inspect the actual dataset before finalizing dataset-specific components.
4. Do not assume column names, feature availability, or target encoding.
5. Do not implement unnecessary modules merely because they appear in the suggested structure.
6. Adapt the architecture to the actual project requirements.
7. Preserve separation between experimentation and reusable source code.
8. Keep training and inference preprocessing consistent.
9. Prevent data leakage at every stage.
10. Keep the implementation understandable enough that the project author can explain every major component.

**The architecture is a guide, not permission to invent requirements.**

When a conflict exists between implementation convenience and a documented project requirement, the documented requirement takes priority.

When a conflict exists between two project documents, stop and surface the conflict instead of silently choosing one.

---

# CODING STANDARDS.md

## Customer Churn Prediction & Retention Intelligence System

**Project:** Customer Churn Prediction & Retention Intelligence System
**Document:** Coding Standards & Engineering Conventions
**Version:** 1.0
**Status:** Active
**Primary Language:** Python
**Primary ML Framework:** scikit-learn
**Application Framework:** Streamlit, only where justified
**Development Assistant:** Google AI Studio
**Repository:** Git/GitHub
**Author:** Anurag

---

# 1. Purpose

This document defines the coding, engineering, organization, readability, maintainability, reproducibility, testing, and implementation standards for the Customer Churn Prediction project.

These standards apply to:

* Python source code
* Jupyter notebooks
* ML pipelines
* Data-processing modules
* Feature-engineering modules
* Model-training code
* Evaluation code
* Inference code
* Streamlit application code
* Tests
* Configuration
* Utility modules
* Documentation-related code
* Scripts

The objective is to ensure that the final repository looks and behaves like a professionally engineered machine-learning project rather than a collection of generated scripts.

---

# 2. Core Engineering Principles

All implementation decisions should follow these principles in this order:

```text
Correctness
    ↓
Clarity
    ↓
Reproducibility
    ↓
Maintainability
    ↓
Testability
    ↓
Performance
    ↓
Convenience
```

Do not sacrifice correctness or maintainability merely to reduce development time.

Do not introduce complexity unless it provides measurable or meaningful value.

---

# 3. General Coding Philosophy

Code should be:

* Simple
* Explicit
* Readable
* Modular
* Reusable
* Testable
* Reproducible
* Predictable
* Well documented
* Easy to debug

Prefer:

```python
clear_code()
```

over:

```python
clever_but_confusing_code()
```

Prefer straightforward implementations over highly abstract architectures when the simpler implementation is sufficient.

---

# 4. Python Version

Use a stable Python version compatible with the selected project dependencies.

The exact version should be recorded in:

* `README.md`
* `requirements.txt` or dependency configuration
* Environment/setup documentation

Do not use language features unavailable in the project's declared Python version.

---

# 5. PEP 8 and Formatting

Python code should broadly follow PEP 8 conventions.

Use:

* 4 spaces for indentation
* Clear line spacing
* Descriptive names
* Reasonable line lengths
* Consistent formatting
* No unnecessary whitespace

Avoid:

```python
x=1
```

Prefer:

```python
x = 1
```

Use an automated formatter where appropriate, such as:

* Black
* Ruff formatter

The project does not need to adopt every available formatting tool.

Consistency is more important than tool quantity.

---

# 6. Naming Conventions

## 6.1 Variables

Use `snake_case`.

Good:

```python
customer_count = 100
churn_probability = 0.82
```

Avoid:

```python
customerCount = 100
cp = 0.82
```

unless the abbreviation is universally clear.

---

## 6.2 Functions

Use descriptive `snake_case` names.

Good:

```python
load_customer_data()
calculate_churn_metrics()
train_baseline_model()
generate_risk_ranking()
```

Avoid:

```python
process()
run()
do_model()
```

when the purpose is unclear.

---

## 6.3 Classes

Use `PascalCase`.

Example:

```python
class ChurnPredictor:
    ...
```

---

## 6.4 Constants

Use uppercase with underscores.

```python
RANDOM_STATE = 42
DEFAULT_THRESHOLD = 0.50
```

---

## 6.5 Private/Internal Functions

A leading underscore may be used for functions that are intentionally internal to a module.

```python
def _validate_columns():
    ...
```

Do not use underscores merely for decoration.

---

# 7. Variable Naming Requirements

Variable names must communicate meaning.

Prefer:

```python
customer_data
numeric_features
categorical_features
churn_labels
validation_predictions
```

Avoid:

```python
df1
df2
x
y1
temp
stuff
data_new
final_final
```

`df` may be acceptable for a short local DataFrame operation, but meaningful names should be used when multiple datasets are involved.

---

# 8. Functions

Functions should generally perform one logical responsibility.

Bad:

```python
def process_everything():
    # load data
    # clean data
    # engineer features
    # train model
    # evaluate model
    # save model
    # create charts
    ...
```

Prefer:

```python
load_data()
validate_data()
preprocess_data()
engineer_features()
train_model()
evaluate_model()
save_model()
```

This improves:

* Testing
* Debugging
* Reusability
* Readability
* Maintenance

---

# 9. Function Size

Avoid unnecessarily large functions.

A function should normally be understandable without scrolling through hundreds of lines.

If a function contains multiple independent stages, consider splitting it into smaller functions.

Do not split every two or three lines into a separate function merely for the sake of abstraction.

Use practical judgment.

---

# 10. Function Inputs and Outputs

Functions should have clear inputs and outputs.

Prefer:

```python
def calculate_metrics(
    y_true,
    y_pred,
    y_probability,
):
    ...
```

over relying on hidden global variables.

Functions should avoid unexpectedly modifying global state.

---

# 11. Type Hints

Use type hints where they improve clarity, particularly for reusable modules.

Example:

```python
def load_customer_data(path: str) -> pd.DataFrame:
    ...
```

For more complex functions:

```python
def predict_churn(
    model,
    features: pd.DataFrame,
) -> np.ndarray:
    ...
```

Type hints do not need to be added mechanically to every trivial line.

---

# 12. Docstrings

Public functions and important classes should have concise docstrings.

Example:

```python
def load_customer_data(path: str) -> pd.DataFrame:
    """Load the customer dataset from the specified path."""
```

For important functions, document:

* Purpose
* Important parameters
* Return value
* Important assumptions

Do not write huge docstrings that simply repeat obvious code.

---

# 13. Comments

Comments should explain **why**, not merely repeat **what** the code does.

Weak:

```python
# Add 1 to count
count += 1
```

Useful:

```python
# Use the training-derived threshold so inference remains consistent
# with the threshold selected during model evaluation.
```

Comments should be:

* Accurate
* Concise
* Maintained with the code

Never leave obsolete comments after refactoring.

---

# 14. No AI-Generated Boilerplate Comments

Do not add repetitive comments such as:

```python
# This function is used to...
# The purpose of this code is...
# AI-generated implementation...
```

unless the comment provides genuine technical value.

Code should read naturally as professionally written project code.

---

# 15. Imports

Keep imports organized.

Preferred order:

```python
# Standard library
from pathlib import Path
import logging

# Third-party
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Local project
from src.data.loader import load_customer_data
from src.models.training import train_model
```

Avoid unused imports.

Remove imports that are no longer required.

---

# 16. Dependency Discipline

Do not introduce a library unless there is a legitimate reason.

Before adding a dependency, consider:

1. Is it actually required?
2. Can the task be handled cleanly with an existing dependency?
3. Does it materially improve the project?
4. Does it introduce unnecessary maintenance?
5. Is it compatible with the project environment?

Avoid dependency inflation.

For example, do not add five libraries for visualization if matplotlib and seaborn are sufficient.

---

# 17. Data Paths

Never hard-code machine-specific absolute paths such as:

```python
C:\Users\Anurag\Desktop\project\data.csv
```

or:

```python
/home/user/project/data.csv
```

Use project-relative paths or configuration.

Prefer:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "customers.csv"
```

The implementation should work when cloned to another machine after following the setup instructions.

---

# 18. Path Handling

Prefer `pathlib.Path` over manually concatenating paths.

Good:

```python
output_path = reports_dir / "model_metrics.json"
```

Avoid:

```python
output_path = reports_dir + "/model_metrics.json"
```

---

# 19. Configuration

Configuration values should not be scattered throughout the code.

Examples:

```python
RANDOM_STATE = 42
TEST_SIZE = 0.20
DEFAULT_THRESHOLD = 0.50
```

For more substantial configuration, use an appropriate configuration file or centralized module.

Do not create an unnecessarily complicated configuration framework.

---

# 20. Randomness and Reproducibility

Where algorithms support randomness, use an explicit random seed.

Example:

```python
RANDOM_STATE = 42
```

Use the same controlled random state during experiments unless there is a documented reason to vary it.

Reproducibility must include:

* Data preparation
* Train/test splitting
* Cross-validation where applicable
* Model training
* Hyperparameter search where applicable

---

# 21. Data Loading

Data-loading logic should be separated from model-training logic.

Prefer:

```text
load_data()
    ↓
validate_data()
    ↓
preprocess_data()
    ↓
train_model()
```

Do not embed large data-loading blocks directly inside model classes or UI code.

---

# 22. Data Validation

Validate assumptions before proceeding.

Examples:

* Required columns exist
* Target exists
* Target has expected values
* Dataset is not empty
* Numerical columns contain expected data types
* Identifier fields are handled correctly

Example:

```python
required_columns = {
    "customer_id",
    "tenure",
    "monthly_charges",
    "churn",
}

missing_columns = required_columns - set(data.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )
```

Errors should be clear enough to diagnose.

---

# 23. DataFrame Handling

Avoid modifying shared DataFrames unexpectedly.

Prefer explicit operations:

```python
clean_data = raw_data.copy()
```

when independent transformation is required.

Avoid unnecessary chained operations that make debugging difficult.

---

# 24. Missing Values

Missing-value handling must be explicit.

Do not silently replace missing values without documenting the strategy.

Avoid:

```python
data = data.fillna(0)
```

unless replacing missing values with zero is genuinely appropriate for the specific feature.

Use preprocessing pipelines where appropriate.

---

# 25. Categorical Features

Categorical preprocessing should be reproducible and consistent between training and inference.

When appropriate, use tools such as:

```python
OneHotEncoder(handle_unknown="ignore")
```

Do not manually encode categories in a way that can produce inconsistent mappings between training and inference.

---

# 26. Numerical Features

Numerical transformations such as:

* Scaling
* Imputation
* Transformation

should be applied consistently.

For models requiring scaling, fit the scaler on training data only.

Do not calculate normalization statistics using the entire dataset before splitting.

---

# 27. Preprocessing Pipelines

Use scikit-learn `Pipeline` and `ColumnTransformer` where they improve correctness and reproducibility.

Typical pattern:

```text
Raw Data
   ↓
ColumnTransformer
   ├── Numerical Pipeline
   └── Categorical Pipeline
   ↓
Model
```

This helps prevent preprocessing leakage and keeps training/inference behavior consistent.

---

# 28. Train/Test Separation

Do not preprocess the entire dataset using learned transformations before splitting.

Correct conceptual sequence:

```text
Raw Dataset
    ↓
Train/Test Split
    ↓
Fit preprocessing on Train
    ↓
Transform Train
    ↓
Transform Test
```

The test set must remain unseen during model development.

---

# 29. Cross-Validation

Cross-validation must be integrated correctly with preprocessing.

Prefer:

```text
Pipeline
    ↓
Cross-validation
    ↓
Model evaluation
```

rather than preprocessing the complete dataset before cross-validation.

For imbalanced classification, use stratified methods where appropriate.

---

# 30. Model Training

Model-training code should be separate from:

* Data ingestion
* Visualization
* Streamlit UI
* User input handling

A training module should primarily be responsible for training and producing artifacts/results.

---

# 31. Baseline First

The codebase must support a clear baseline experiment.

Do not immediately optimize a complex model.

The baseline should be easy to identify and reproduce.

Example:

```text
baseline_logistic_regression
```

---

# 32. Experiment Isolation

Each meaningful experiment should be identifiable.

Avoid code such as:

```python
model = RandomForestClassifier(...)
# later silently change parameters
model = RandomForestClassifier(...)
```

without recording the difference.

Experiments should have explicit configurations and recorded results.

---

# 33. Model Selection

Do not hard-code a model as the "best model" before experiments are completed.

The final model must be selected based on actual evaluation results and project requirements.

Bad:

```python
best_model = XGBClassifier(...)
```

before comparison.

Prefer a process that produces an evidence-based selection.

---

# 34. Evaluation Code

Evaluation should be centralized where practical.

Create reusable functions for metrics such as:

```python
calculate_classification_metrics()
plot_confusion_matrix()
plot_roc_curve()
plot_precision_recall_curve()
evaluate_calibration()
```

This reduces duplication and ensures consistent evaluation.

---

# 35. Metric Calculation

Metrics must use the correct prediction type.

For example:

* Classification predictions for precision/recall/F1
* Probability scores for ROC-AUC
* Probability estimates for calibration

Do not accidentally calculate probability-based metrics from hard class predictions.

---

# 36. Threshold Handling

Do not scatter threshold values throughout the codebase.

Use a clearly defined configuration value or evaluation result.

Example:

```python
decision_threshold = 0.50
```

If a threshold is selected through validation, save/document the selected threshold.

Training and inference must use the same intended threshold.

---

# 37. Model Persistence

The final model and preprocessing pipeline should be saved using an appropriate serialization mechanism.

For scikit-learn models, `joblib` may be used where appropriate.

Save the complete required preprocessing/model pipeline rather than saving only the model if preprocessing is required for inference.

Example concept:

```text
preprocessing + model
        ↓
single inference pipeline
```

---

# 38. Model Artifact Naming

Use descriptive artifact names.

Good:

```text
churn_model.joblib
preprocessor.joblib
final_pipeline.joblib
```

Avoid:

```text
model1.pkl
final_final.pkl
bestmodelnew.pkl
```

---

# 39. Artifact Safety

Never load arbitrary model artifacts from untrusted sources without understanding the security implications of serialization formats.

Only load project-generated or trusted artifacts.

---

# 40. Logging

Use Python's `logging` module where logging is useful.

Prefer:

```python
logger.info("Training model...")
logger.warning("Missing values detected in %s", column_name)
```

over excessive `print()` statements in reusable modules.

`print()` may still be appropriate for simple scripts or notebook exploration.

---

# 41. Error Handling

Handle expected errors explicitly.

Good:

```python
if not data_path.exists():
    raise FileNotFoundError(
        f"Dataset not found: {data_path}"
    )
```

Avoid:

```python
try:
    ...
except Exception:
    pass
```

Silent exception handling is prohibited unless there is a very specific and documented reason.

---

# 42. Error Messages

Error messages should explain:

1. What failed
2. Why it may have failed
3. Where appropriate, how to fix it

Example:

```text
Required column 'churn' was not found.
Verify that the dataset contains the expected target column
or update the dataset configuration.
```

---

# 43. Notebook Standards

Notebooks are for:

* Exploration
* Visualization
* Experiments
* Analysis
* Demonstration

They should not become the only source of truth for core application logic.

Reusable logic should move into `src/`.

---

# 44. Notebook Structure

A notebook should generally follow:

```text
1. Title / Objective
2. Imports
3. Configuration
4. Dataset Loading
5. Data Validation
6. EDA
7. Preprocessing
8. Baseline
9. Experiments
10. Evaluation
11. Error Analysis
12. Conclusions
```

Avoid random execution order.

---

# 45. Notebook Reproducibility

A reviewer should be able to:

1. Restart the kernel/runtime.
2. Run cells in order.
3. Reproduce the documented analysis.

Do not depend on hidden variables created in previous executions.

---

# 46. Notebook Output Discipline

Avoid leaving notebooks filled with:

* Debugging output
* Tracebacks
* Temporary variables
* Repeated plots
* Failed experiments
* Irrelevant print statements

Clean notebooks before final submission.

---

# 47. Visualization Standards

Plots should be:

* Readable
* Properly titled
* Properly labeled
* Relevant
* Consistent

Every plot should answer a meaningful analytical question.

Avoid decorative charts with no analytical purpose.

---

# 48. Visualization Naming

Use descriptive chart titles.

Bad:

```text
Graph 1
```

Better:

```text
Churn Rate by Contract Type
```

Axes should include meaningful labels and units where appropriate.

---

# 49. Streamlit Standards

If a Streamlit application is implemented:

Keep UI code separate from ML logic.

Prefer:

```text
Streamlit UI
    ↓
Inference Service
    ↓
Model Pipeline
```

Avoid putting training code directly inside the UI.

---

# 50. Streamlit Performance

Do not retrain models every time the application reruns.

Use appropriate caching mechanisms where useful.

For example:

```python
@st.cache_resource
def load_model():
    ...
```

Only cache objects when caching is technically appropriate.

---

# 51. User Input Validation

Application inputs must be validated.

Handle:

* Missing inputs
* Invalid numeric values
* Unexpected categories
* Out-of-range values
* Empty submissions

The application should fail gracefully.

---

# 52. User-Facing Errors

Do not expose raw Python tracebacks to ordinary users.

Instead, provide clear messages such as:

```text
Unable to generate a prediction.
Please verify the entered customer information.
```

Detailed technical errors should remain available through logs/debugging when appropriate.

---

# 53. Security and Secrets

Never hard-code:

* API keys
* Passwords
* Tokens
* Private credentials
* Personal access tokens

Do not commit `.env` files containing secrets.

Use environment variables or an appropriate secret-management mechanism.

---

# 54. Git Hygiene

Never commit:

* API keys
* Passwords
* Personal credentials
* Large temporary files
* Python cache files
* Virtual environments
* OS-generated files
* Debug artifacts
* Unnecessary generated files

Use `.gitignore`.

---

# 55. File Organization

Files should have one clear purpose.

Avoid creating:

```text
misc.py
helpers_final.py
utils_new.py
test2.py
model_latest.py
```

unless the names genuinely represent their purpose.

Prefer:

```text
data_validation.py
feature_engineering.py
model_training.py
evaluation.py
inference.py
```

---

# 56. Avoid Duplicate Logic

Do not copy and paste the same logic into multiple files.

If the same operation is required in multiple places, consider creating a reusable function or module.

However, do not over-abstract tiny one-off operations.

---

# 57. Dead Code

Remove:

* Unused functions
* Unused imports
* Unused variables
* Commented-out experimental code
* Obsolete model versions
* Debug statements

Historical experiments belong in experiment documentation, not abandoned source code.

---

# 58. Temporary Code

Temporary debugging code must not remain in the final repository.

Examples:

```python
print(data.head(50))
print("HERE")
print("TEST")
```

Remove or replace such statements before finalization.

---

# 59. Magic Numbers

Avoid unexplained numeric constants.

Bad:

```python
if probability > 0.73:
```

Better:

```python
HIGH_RISK_THRESHOLD = 0.73

if probability > HIGH_RISK_THRESHOLD:
```

The value must still be justified by the project's methodology.

---

# 60. Hard-Coded Business Logic

Business assumptions should be centralized and documented.

For example:

```python
RISK_THRESHOLDS = {
    "low": 0.30,
    "medium": 0.60,
    "high": 1.00,
}
```

Only use thresholds that are actually defined by the project's methodology.

Do not invent business thresholds merely for UI appearance.

---

# 61. Explainability Code

Explainability functionality should be separated from core prediction logic where practical.

For example:

```text
prediction.py
explainability.py
risk_ranking.py
```

The prediction system must still work independently of optional explanation tooling where possible.

---

# 62. Explainability Integrity

Never generate explanations by simply selecting random or visually convenient features.

Explanations must come from actual model/data evidence.

Avoid statements such as:

```text
Customer will churn because they are unhappy.
```

unless such information is explicitly represented and justified.

Prefer:

```text
The model assigned increased importance to the customer's
recent usage pattern and contract characteristics.
```

---

# 63. Data Leakage Protection in Code

The implementation must actively prevent leakage.

Review code for:

* Fitting scalers before splitting
* Encoding using the complete dataset
* Imputation using test data
* Feature calculations using future information
* Target-derived features
* Accidental test-set tuning

Any suspicious leakage must be investigated before finalization.

---

# 64. Testing Strategy

The project should include practical tests where appropriate.

At minimum, test:

### Data Loading

* Valid dataset
* Missing file
* Missing required columns

### Preprocessing

* Expected transformation
* Missing values
* Unknown categorical values

### Inference

* Valid input
* Invalid input
* Model loading

### Output

* Probability range
* Expected output fields
* Risk category consistency

---

# 65. Probability Validation

Predicted churn probabilities should satisfy:

```text
0 ≤ probability ≤ 1
```

The code should not silently produce invalid probabilities.

---

# 66. Model Input Consistency

Training and inference must use the same feature schema.

Do not allow the application to silently reorder or reinterpret features incorrectly.

Where possible, validate expected feature names and structure.

---

# 67. Testing After Refactoring

Any significant refactoring must be followed by:

* Running tests
* Running the training/inference pipeline
* Checking outputs
* Checking the application if affected

Never assume that a refactor is safe merely because the code looks cleaner.

---

# 68. Documentation Synchronization

When implementation changes a documented behavior, update the relevant documentation.

Examples:

If the final model changes:

```text
README
EXPERIMENT_PLAN
```

may need updates.

If the repository structure changes:

```text
README
ARCHITECTURE
```

may need updates.

Documentation must reflect the actual final system.

---

# 69. AI Studio Implementation Discipline

Google AI Studio must not rewrite large portions of the project unnecessarily.

When modifying existing code:

1. Understand the existing implementation.
2. Identify the problem.
3. Make the smallest reasonable change.
4. Run/verify the affected functionality.
5. Check for regressions.
6. Update documentation if behavior changed.

Avoid destructive rewrites unless the existing architecture is genuinely unsuitable.

---

# 70. AI Studio Must Not Invent Completion

AI Studio must never claim:

```text
"Implemented and tested successfully"
```

unless the corresponding implementation was actually performed and tested.

Similarly, it must not claim:

* Tests passed when they were not run
* Metrics were achieved when they were not measured
* A model was trained when training did not occur
* An application was verified when it was not run

Use truthful status reporting.

---

# 71. AI Studio Change Transparency

For significant changes, AI Studio should summarize:

* What changed
* Why it changed
* Files affected
* Tests performed
* Known limitations

Do not generate unnecessary verbose change logs for trivial edits.

---

# 72. AI Studio and Project Documentation

Before substantial implementation work, AI Studio should read and respect the relevant project documents, particularly:

```text
PRD.md
PROJECT_SPECIFICATIONS.md
ML_REQUIREMENTS.md
DATASET_AND_DATA_STRATEGY.md
EXPERIMENT_PLAN.md
ARCHITECTURE.md
RULES.md
CODING_STANDARDS.md
```

If a conflict exists between documents, AI Studio must not silently choose an interpretation.

The conflict should be surfaced for review.

---

# 73. No Unapproved Scope Expansion

AI Studio must not introduce major features simply because they appear technically interesting.

Examples:

* Deep learning
* LLM integration
* Authentication
* Cloud deployment
* Complex APIs
* Database systems
* Docker
* Microservices

Major scope changes require explicit approval.

---

# 74. Minimal Necessary Dependencies

When implementing a feature, prefer existing project dependencies before adding new ones.

Example:

If scikit-learn already provides the required preprocessing functionality, do not introduce another library solely to perform the same task.

---

# 75. Performance

The project is not intended for production-scale infrastructure.

Optimize only where there is an actual performance problem.

Priorities:

1. Correctness
2. Reliability
3. Reasonable execution time
4. Maintainability

Do not prematurely optimize simple operations.

---

# 76. Memory Usage

Avoid unnecessary copies of large datasets.

At the same time, prioritize code clarity over micro-optimizations unless the dataset size requires optimization.

---

# 77. Reproducible Training

Training should ideally be executable through a clear command or script.

For example:

```bash
python -m src.models.train
```

The exact command should match the final repository structure.

The README must document the verified command.

---

# 78. Reproducible Inference

Inference should be independently executable after the model artifact has been created.

The inference process should not require retraining the model unless explicitly intended.

---

# 79. Model Versioning

If multiple final candidate models are saved, use descriptive names or metadata.

Avoid overwriting important artifacts without reason.

Example:

```text
models/
├── baseline_logistic_regression.joblib
├── random_forest_tuned.joblib
└── final_churn_pipeline.joblib
```

Only retain artifacts that provide meaningful value.

---

# 80. Generated Files

Generated files should be organized.

Examples:

```text
models/
reports/
outputs/
```

Do not scatter generated CSVs, images, logs, and model files throughout the repository.

---

# 81. Source of Truth

The following should have clear ownership:

### Source code

`src/`

### Exploratory analysis

`notebooks/`

### Trained artifacts

`models/`

### Reports/results

`reports/`

### Application

`app/`

### Documentation

`docs/`

The exact structure may change if the final architecture requires it.

---

# 82. Final Code Review Checklist

Before the project is marked complete, review:

### Readability

* [ ] Names are descriptive
* [ ] Functions have clear responsibilities
* [ ] No unnecessary complexity
* [ ] Formatting is consistent
* [ ] Comments are useful

### Maintainability

* [ ] No duplicated logic
* [ ] No dead code
* [ ] No unnecessary dependencies
* [ ] No machine-specific paths
* [ ] Configuration is manageable

### ML Integrity

* [ ] No data leakage
* [ ] Preprocessing is reproducible
* [ ] Train/test separation is correct
* [ ] Cross-validation is correct
* [ ] Metrics are correctly calculated
* [ ] Results are genuine

### Reproducibility

* [ ] Random seeds controlled where appropriate
* [ ] Dependencies documented
* [ ] Training process documented
* [ ] Inference process documented
* [ ] Model artifacts reproducible

### Application

* [ ] Inputs validated
* [ ] Model loads correctly
* [ ] Predictions are valid
* [ ] Errors handled gracefully
* [ ] UI does not contain unnecessary complexity

### Security

* [ ] No secrets committed
* [ ] No credentials in source
* [ ] `.gitignore` configured
* [ ] Untrusted artifacts are not loaded blindly

### Documentation

* [ ] README matches implementation
* [ ] Architecture matches implementation
* [ ] Experiment results are genuine
* [ ] Commands have been verified
* [ ] No unsupported claims

---

# 83. Definition of High-Quality Code

The final implementation should allow another developer to reasonably understand:

1. Where the data comes from.
2. How it is validated.
3. How preprocessing works.
4. How features are generated.
5. How models are trained.
6. How experiments are compared.
7. How the final model was selected.
8. How predictions are generated.
9. How explanations are produced.
10. How the application uses the model.
11. How the project can be reproduced.

If understanding the system requires reading thousands of lines of tightly coupled code, the architecture should be reconsidered.

---

# 84. Final Engineering Rule

Do not confuse **more code** with **better engineering**.

A high-quality implementation is one where:

```text
Every important piece of code
        ↓
Has a clear purpose
        ↓
Uses an appropriate abstraction
        ↓
Can be tested
        ↓
Can be reproduced
        ↓
Can be explained
```

The final codebase should demonstrate engineering judgment, not merely generated code volume.

---

# 85. Final Principle

The standard for this project is:

> **Write code that another ML engineer can understand, reproduce, test, maintain, and trust.**

The implementation should be technically defensible and simple enough that the project author can explain the important decisions during an internship evaluation or technical interview.

**Correct code first. Clean code second. Clever code only when necessary.**

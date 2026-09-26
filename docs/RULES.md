# RULES.md

# Customer Churn Prediction & Retention Intelligence System

**Project:** Machine Learning Internship Capstone — Project 1
**Document:** Implementation Rules & Operating Constraints
**Version:** 1.0
**Status:** Active
**Author:** Anurag
**Target Completion:** 30 September 2026

---

# 1. PURPOSE OF THIS DOCUMENT

This document defines the mandatory rules that govern the implementation, modification, testing, documentation, and presentation of this project.

These rules exist to ensure that the project remains:

* Technically correct
* Reproducible
* Explainable
* Maintainable
* Professionally structured
* Honest about results
* Consistent with the project requirements
* Suitable for GitHub and portfolio presentation
* Achievable within the internship deadline

These rules apply to all implementation work performed with the assistance of Google AI Studio or any other coding assistant.

---

# 2. SOURCE-OF-TRUTH HIERARCHY

When making a technical decision, use the following priority order:

```text
1. Actual project data and observed evidence
        ↓
2. Project requirements
        ↓
3. PRD.md
        ↓
4. PROJECT_SPECIFICATIONS.md
        ↓
5. ML_REQUIREMENTS.md
        ↓
6. DATASET_AND_DATA_STRATEGY.md
        ↓
7. EXPERIMENT_PLAN.md
        ↓
8. ARCHITECTURE.md
        ↓
9. RULES.md
        ↓
10. Other project documentation
        ↓
11. General technical best practices
```

If two project documents appear to conflict:

1. Do not silently choose one.
2. Identify the conflict.
3. Preserve the more authoritative requirement.
4. Update the affected documentation if a decision changes.
5. Do not continue with a contradictory implementation.

The actual dataset must always take precedence over assumptions about what the dataset contains.

---

# 3. READ BEFORE IMPLEMENTING

Before making substantial implementation changes, the implementation assistant must understand the relevant project documentation.

At minimum, it must understand:

* PRD.md
* PROJECT_SPECIFICATIONS.md
* ML_REQUIREMENTS.md
* DATASET_AND_DATA_STRATEGY.md
* EXPERIMENT_PLAN.md
* ARCHITECTURE.md
* RULES.md

Do not begin major implementation based only on a single prompt when the project documentation is available.

---

# 4. DO NOT INVENT REQUIREMENTS

Never invent:

* Business requirements
* Dataset fields
* Target definitions
* Evaluation criteria
* Performance requirements
* User requirements
* Deployment requirements
* External APIs
* Dataset characteristics

If something is not specified:

1. Inspect the actual project context.
2. Determine whether it can be reasonably inferred.
3. If the decision materially affects the project, flag it for review.
4. Record the final decision in the appropriate documentation.

---

# 5. DATA IS THE SOURCE OF TRUTH

Never assume that a dataset has a particular:

* Column
* Data type
* Encoding
* Distribution
* Target
* Relationship
* Business meaning

Inspect the actual dataset first.

For every important assumption, verify it using the data.

Example:

Do NOT assume:

```text
tenure = number of months
```

until the dataset documentation and actual values confirm it.

---

# 6. NO FABRICATION

This is one of the most important project rules.

Never fabricate:

* Dataset records
* Dataset sources
* Model metrics
* Validation results
* Test results
* Experiment results
* Citations
* Business outcomes
* Customer behavior
* Feature importance
* SHAP explanations
* Screenshots
* Benchmark results
* Deployment results
* User feedback
* Performance improvements

If something has not actually been executed or measured, state that it has not been executed or measured.

---

# 7. NO FAKE METRICS

Never write a metric such as:

```text
ROC-AUC: 0.94
F1-score: 0.91
Accuracy: 95%
```

unless that number came from an actual experiment.

Never create "example" results and accidentally present them as real project results.

Before final documentation, verify that every reported metric corresponds to an actual reproducible experiment.

---

# 8. NO FABRICATED IMPROVEMENTS

Never claim:

> "The new model improved performance by 8%"

unless:

1. A previous result exists.
2. A new result exists.
3. Both were evaluated under comparable conditions.
4. The difference was actually measured.

Performance improvements must be evidence-based.

---

# 9. NO DATA LEAKAGE

Prevent data leakage at every stage.

Never:

* Fit preprocessing on the entire dataset before splitting.
* Use test-set information during training.
* Use future information unavailable at prediction time.
* Use target-derived features improperly.
* Tune models directly against the test set.
* Select a model based on repeated test-set evaluation.

The test set must remain isolated until final evaluation.

---

# 10. TRAIN / VALIDATION / TEST DISCIPLINE

Use a clearly defined data-splitting strategy.

Conceptually:

```text
Raw Data
   ↓
Train / Validation / Test
   ↓
Training → Model Development
Validation → Model Selection / Tuning
Test → Final Evaluation
```

The exact split strategy must follow the project's ML requirements and experiment plan.

Do not repeatedly inspect the test set and use its results to make modeling decisions.

---

# 11. PREPROCESSING RULE

Any preprocessing operation that learns parameters from data must be fitted only using the appropriate training data.

Examples:

* Imputation
* Scaling
* Encoding
* Feature selection
* Dimensionality reduction
* Learned transformations

Where appropriate, use a reproducible preprocessing pipeline.

---

# 12. PIPELINE PREFERENCE

Prefer a unified preprocessing/model pipeline where practical.

Example conceptual structure:

```text
Raw Features
     ↓
Column Transformer
     ├── Numerical preprocessing
     └── Categorical preprocessing
     ↓
Model
     ↓
Prediction
```

This reduces the risk of inconsistent preprocessing between training and inference.

---

# 13. IDENTIFIERS ARE NOT FEATURES BY DEFAULT

Customer IDs and other unique identifiers must not automatically be treated as predictive features.

Investigate whether an identifier contains meaningful information.

If it is only an identifier, exclude it from model training while preserving it for reporting/ranking where necessary.

---

# 14. TARGET VARIABLE RULE

The target variable must be explicitly identified and validated before model training.

Verify:

* Column name
* Data type
* Unique values
* Encoding
* Missing values
* Class distribution
* Business interpretation

Do not train a model until the target definition is understood.

---

# 15. CLASS IMBALANCE RULE

Always inspect class distribution.

Do not automatically:

* Oversample
* Undersample
* Use SMOTE
* Assign class weights

without first understanding whether imbalance exists and whether intervention is justified.

Any imbalance strategy must be applied only to the training data when appropriate.

---

# 16. ACCURACY IS NOT ENOUGH

Do not use accuracy as the sole model-selection criterion.

Churn prediction may involve class imbalance and asymmetric business costs.

The project should consider, where appropriate:

* ROC-AUC
* Precision
* Recall
* F1-score
* Calibration
* Confusion matrix
* Threshold-dependent behavior

The final choice must consider the actual project objective.

---

# 17. BASELINE FIRST

Never jump directly to a complex model.

Establish a meaningful baseline first.

The primary baseline is:

**Logistic Regression**

The baseline provides a reference point for judging whether additional complexity is justified.

---

# 18. MODEL COMPLEXITY RULE

Prefer the simplest model that adequately solves the problem.

Do not use a complex model merely because it produces a higher score.

Consider:

* Performance
* Generalization
* Interpretability
* Computational cost
* Maintainability
* Inference requirements
* Portfolio value
* Business suitability

A slightly weaker but significantly more interpretable model may be preferable when the difference is not practically meaningful.

---

# 19. NO MODEL COLLECTION FOR APPEARANCE

Do not train many models simply to make the project appear advanced.

Every model must have a reason for inclusion.

A reasonable progression may be:

```text
Logistic Regression
        ↓
Tree-Based Baseline
        ↓
Random Forest / Boosting
        ↓
Tuning
        ↓
Final Model
```

The exact models must be determined by the actual data and experiment plan.

---

# 20. EXPERIMENTATION RULE

Every meaningful experiment should record:

* Experiment ID
* Model
* Dataset/split
* Features
* Preprocessing
* Parameters
* Validation strategy
* Metrics
* Results
* Observations
* Decision

Do not rely solely on memory.

---

# 21. FAIR MODEL COMPARISON

Models must be compared using consistent evaluation methodology.

Do not compare:

```text
Model A → validation score
Model B → test score
Model C → training score
```

and call this a fair comparison.

The evaluation conditions must be comparable.

---

# 22. HYPERPARAMETER TUNING RULE

Tune only meaningful hyperparameters.

Do not perform enormous searches simply because automated search is available.

Tuning must have:

* Defined search space
* Defined evaluation strategy
* Defined objective
* Reproducibility
* Reasonable computational cost

Record the selected configuration.

---

# 23. TEST SET PROTECTION

The final test set is for final evaluation.

Do not:

* Tune repeatedly against it.
* Select features based on it.
* Select thresholds based on it without an appropriate validation methodology.
* Use it to justify model changes during development.

If the test set has been substantially used during development, document the issue and reconsider the evaluation strategy.

---

# 24. RANDOM SEEDS

Where randomness exists, use controlled random states/seeds where appropriate.

Examples:

* Train/test split
* Cross-validation
* Random forests
* Sampling
* Hyperparameter search

The chosen seed must be documented when it materially affects reproducibility.

---

# 25. REPRODUCIBILITY RULE

Another developer should be able to understand how to reproduce the main results.

Document:

* Dataset source
* Environment
* Dependencies
* Random seed
* Training process
* Evaluation process
* Model artifact
* Execution commands

Avoid undocumented manual steps.

---

# 26. FILE PATH RULE

Do not use machine-specific absolute paths such as:

```text
C:\Users\Anurag\Desktop\project\data.csv
```

Use project-relative paths or configurable paths.

The project must remain portable.

---

# 27. CROSS-PLATFORM PATHS

Prefer platform-independent path handling.

Python implementations should generally use appropriate path utilities rather than manually concatenating operating-system-specific path strings.

---

# 28. NO HARDCODED SECRETS

Never hardcode:

* API keys
* Passwords
* Tokens
* Credentials
* Private URLs
* Access tokens

Use environment variables or appropriate configuration mechanisms where credentials are genuinely required.

Never commit secrets to Git.

---

# 29. DEPENDENCY DISCIPLINE

Do not install a library merely because it is popular.

Before adding a dependency, ask:

1. Is it necessary?
2. Does the standard library or existing dependency already solve the problem?
3. Does it materially improve the implementation?
4. Is it compatible with the project?
5. Is it maintainable?

Keep dependencies reasonably minimal.

---

# 30. LIBRARY PREFERENCE

Prefer well-established libraries appropriate for the task.

Typical choices may include:

* pandas
* NumPy
* scikit-learn
* matplotlib
* seaborn
* joblib
* Streamlit

Additional libraries must have a legitimate purpose.

---

# 31. XGBOOST / EXTERNAL MODEL RULE

If XGBoost or another additional ML library is introduced:

* Justify its inclusion.
* Add it to dependencies.
* Verify reproducibility.
* Compare it fairly against baseline models.
* Do not assume it will outperform simpler models.

Do not introduce it solely because it sounds more advanced.

---

# 32. EDA RULE

Every major visualization should answer a meaningful question.

Avoid decorative charts.

Prefer questions such as:

* Is the target imbalanced?
* Which customer segments show different churn rates?
* Are numerical features heavily skewed?
* Are there suspicious values?
* Are some features strongly correlated?
* Are there potential leakage indicators?

---

# 33. VISUALIZATION HONESTY

Never manipulate visualizations to exaggerate findings.

Do not:

* Misrepresent axes
* Hide relevant categories
* Select only favorable observations
* Use misleading scales
* Remove inconvenient data without justification

Charts must represent the underlying data faithfully.

---

# 34. OUTLIER RULE

Do not automatically remove outliers.

First determine whether an observation is:

* A legitimate extreme customer
* A data-entry error
* A measurement issue
* A meaningful business case

Document any transformation or removal.

---

# 35. MISSING VALUE RULE

Do not blindly fill every missing value with zero.

Choose an imputation strategy based on:

* Feature meaning
* Missingness pattern
* Data type
* Modeling requirements

Document the decision.

---

# 36. CATEGORICAL DATA RULE

Categorical variables must be handled appropriately.

Do not arbitrarily convert categories to numeric values such as:

```text
Basic = 1
Premium = 2
Enterprise = 3
```

unless the numerical ordering is genuinely meaningful.

Use appropriate encoding methods.

---

# 37. FEATURE ENGINEERING RULE

Every engineered feature must have a clear meaning.

For each important engineered feature, be able to answer:

```text
What is it?
Why does it make sense?
How is it calculated?
Could it leak future information?
Does it improve or clarify the model?
```

Do not create dozens of arbitrary features.

---

# 38. FEATURE SELECTION RULE

Do not remove features solely because they have weak univariate correlation with the target.

Model relationships may be nonlinear or involve interactions.

Feature selection should consider:

* Data quality
* Leakage
* Redundancy
* Model behavior
* Domain meaning
* Validation performance

---

# 39. CORRELATION ≠ CAUSATION

Never write:

> "Feature X causes churn"

based solely on correlation or model importance.

Use appropriate language such as:

> "Feature X is associated with churn in the dataset."

or:

> "Feature X contributed strongly to the model's prediction."

---

# 40. EXPLAINABILITY RULE

Explainability must be based on the actual trained model.

Never generate explanations from intuition alone and present them as model explanations.

If a customer receives:

```text
High churn risk because of low tenure
```

there must be an actual evidence-based mechanism supporting that explanation.

---

# 41. SHAP RULE

SHAP is optional.

Use it only if:

* It is technically appropriate.
* It provides meaningful value.
* It can be implemented reliably.
* It does not create unnecessary complexity.

Do not use SHAP merely because it is a popular ML term.

---

# 42. RISK CATEGORY RULE

Risk categories must be defined explicitly.

For example:

```text
Low
Medium
High
```

If thresholds are used, document them.

Do not present arbitrary categories as if they have established business meaning.

---

# 43. PROBABILITY RULE

A churn probability is a model estimate, not certainty.

The application should avoid language such as:

> "This customer will definitely churn."

Prefer:

> "The model estimates a high probability of churn."

---

# 44. CALIBRATION RULE

Because churn probability is a core product output, calibration should be considered.

If probabilities are poorly calibrated:

* Do not represent them as precise real-world probabilities.
* Investigate calibration.
* Consider an appropriate calibration method if justified.
* Report limitations.

---

# 45. THRESHOLD RULE

Never assume:

```text
probability >= 0.50 → churn
```

is automatically the correct business threshold.

Threshold selection must be supported by validation evidence and the intended precision/recall trade-off.

---

# 46. ERROR ANALYSIS RULE

Do not stop after reporting aggregate metrics.

Investigate:

* False positives
* False negatives
* Confusion matrix
* Segment-level behavior where meaningful

Ask:

> "Where is the model wrong, and why might that matter?"

---

# 47. FINAL MODEL SELECTION RULE

The final model must not be selected solely because it has the highest single metric.

Consider:

* Generalization
* Multiple relevant metrics
* Calibration
* Interpretability
* Complexity
* Inference cost
* Stability
* Business suitability

The final decision must be documented.

---

# 48. APPLICATION RULE

If a Streamlit application is built:

It must be based on the actual trained model and preprocessing pipeline.

Do not create a visually convincing interface that produces disconnected or hardcoded predictions.

The UI must actually connect to the project artifacts.

---

# 49. APPLICATION INPUT VALIDATION

The application should handle invalid inputs gracefully.

Examples:

* Missing required input
* Invalid numerical values
* Impossible values
* Unknown categories
* Incorrect data types

Do not allow malformed inputs to silently produce misleading predictions.

---

# 50. MODEL ARTIFACT RULE

If a trained model is saved:

Save the components required for consistent inference, such as:

* Preprocessing
* Feature transformation
* Model
* Relevant metadata

Avoid saving only the final estimator if preprocessing is required.

---

# 51. TRAINING / INFERENCE CONSISTENCY

The same preprocessing logic must be used during:

```text
Training
   ↓
Validation
   ↓
Testing
   ↓
Inference
```

Do not manually reproduce transformations in multiple places if this creates inconsistency risk.

---

# 52. NOTEBOOK RULE

Notebooks are primarily for:

* Exploration
* EDA
* Experimentation
* Visualization
* Analysis

Reusable production/inference logic should preferably live in source modules.

Do not allow the notebook to become the only place where the project works.

---

# 53. SOURCE CODE RULE

Source code should be:

* Modular
* Readable
* Maintainable
* Reasonably commented
* Reusable
* Testable

Avoid giant functions.

Avoid unnecessary abstraction.

---

# 54. COMMENTS RULE

Comments should explain:

* Why something is done
* Important assumptions
* Non-obvious logic
* Potential pitfalls

Do not fill source code with obvious comments such as:

```python
# Import pandas
import pandas as pd
```

---

# 55. DOCUMENTATION SYNCHRONIZATION

Documentation must describe the actual implementation.

If implementation changes materially:

1. Identify affected documentation.
2. Update it.
3. Ensure README and technical documents remain consistent.

Never leave documentation describing an older architecture.

---

# 56. README HONESTY

The README must never contain:

* Fabricated metrics
* Fabricated screenshots
* Unsupported claims
* Fake user testimonials
* Fake deployment status
* Fake performance improvements

Everything presented as a project result must be verifiable.

---

# 57. SCREENSHOT RULE

Screenshots should show the actual project.

Do not create fake screenshots to represent functionality that does not exist.

If screenshots are added, ensure they correspond to the current version of the application.

---

# 58. UI BRANDING RULE

The interface should use the project's own identity.

Do not unnecessarily include:

* Google AI Studio branding
* Gemini branding
* AI-generated labels
* AI Studio logos
* Assistant-generated badges

unless explicitly required by an API/platform requirement or applicable policy.

The project should look like a professional independent ML project.

---

# 59. AUTHORSHIP & REPRESENTATION RULE

The project may be developed with coding assistance, but the final project must accurately represent the user's work and understanding.

Do not fabricate:

* Human contributions
* Research contributions
* Dataset collection
* Experiments
* User studies
* Business deployments
* Production usage

The author must be able to explain the important technical decisions and implementation.

---

# 60. NO AI-SLOP RULE

Avoid generic AI-generated project language.

Do not use unnecessary phrases such as:

* "Revolutionary AI-powered solution"
* "Cutting-edge intelligent platform"
* "Next-generation AI ecosystem"
* "State-of-the-art" without evidence
* "Enterprise-grade" without justification

Use precise technical language.

---

# 61. NO BUZZWORD INFLATION

Do not add terms such as:

* AI-powered
* intelligent
* advanced
* sophisticated
* state-of-the-art
* enterprise-grade
* production-ready

unless the term is technically justified.

---

# 62. NO UNNECESSARY TECHNOLOGIES

Do not add:

* LLMs
* Vector databases
* RAG
* Docker
* Kubernetes
* Cloud services
* Message queues
* Microservices
* CI/CD systems

unless they solve an actual project requirement.

This is a classical ML project.

---

# 63. NO UNNECESSARY DEEP LEARNING

Do not introduce neural networks unless there is a strong technical justification.

Traditional ML models are expected to be sufficient for this project unless experimentation demonstrates otherwise.

---

# 64. NO SCORE CHASING

Do not modify the methodology repeatedly simply to obtain a higher metric.

A small metric improvement is not automatically a meaningful improvement.

Consider whether the change improves:

* Generalization
* Stability
* Interpretability
* Business usefulness

---

# 65. NO TEST-SET GAMING

Never repeatedly modify the model based on final test results until the desired score is obtained.

If the test set has been used extensively during development, report the limitation honestly.

---

# 66. NO CHERRY-PICKING

Do not report only the experiments that performed well.

Important failed experiments may be documented where they provide useful technical insight.

The final report should represent the actual development process honestly.

---

# 67. FAILED EXPERIMENT RULE

A failed experiment is acceptable.

Document:

```text
What was tried
↓
Why it was tried
↓
What happened
↓
Why it was not selected
↓
What was learned
```

Failure is preferable to fabricated success.

---

# 68. COMPUTATIONAL BUDGET

Do not spend excessive time or compute resources on marginal improvements.

Given the internship deadline, prioritize:

1. Correctness
2. Required functionality
3. Evaluation
4. Documentation
5. Testing
6. High-value enhancements

---

# 69. DEADLINE RULE

The hard project deadline is:

**30 September 2026**

If time becomes limited:

### Priority 1 — Mandatory

* Correct dataset
* Correct preprocessing
* Baseline
* Model training
* Evaluation
* Final model
* Required outputs
* Documentation

### Priority 2 — High Value

* Explainability
* Calibration
* Error analysis
* Risk ranking
* Reproducible pipeline

### Priority 3 — Optional

* Advanced UI
* Extra visualizations
* Additional models
* Cosmetic improvements

Never sacrifice core ML correctness for visual polish.

---

# 70. SCOPE CREEP RULE

If a proposed feature is not required:

Ask:

1. Does it materially improve the project?
2. Does it strengthen learning?
3. Does it strengthen portfolio value?
4. Can it be implemented reliably within the deadline?

If not, do not add it.

---

# 71. CHANGE MANAGEMENT

Before making a major architectural change:

1. Explain the reason.
2. Identify affected components.
3. Identify documentation that must change.
4. Assess deadline impact.
5. Implement only after the decision is clear.

Do not silently rewrite the project architecture.

---

# 72. DO NOT DELETE WORK WITHOUT REASON

Do not delete:

* Experiments
* Useful analysis
* Documentation
* Existing functionality
* Working code

unless there is a justified reason.

When replacing an implementation, preserve useful information where practical.

---

# 73. SAFE MODIFICATION RULE

Before modifying an existing component:

* Understand what it does.
* Check its dependencies.
* Check where it is used.
* Preserve compatible behavior where possible.

Avoid breaking unrelated functionality.

---

# 74. MINIMAL CHANGE PRINCIPLE

When fixing a bug, prefer the smallest reliable change that solves the problem.

Do not rewrite the entire project to fix a local issue unless the architecture genuinely requires it.

---

# 75. ERROR HANDLING

Errors should be:

* Detectable
* Understandable
* Properly surfaced
* Handled where appropriate

Do not hide exceptions simply to make the application appear functional.

Avoid patterns such as:

```python
try:
    ...
except:
    pass
```

unless there is a specific justified reason.

---

# 76. LOGGING

Where useful, provide meaningful logs for:

* Data loading
* Training
* Evaluation
* Model loading
* Prediction failures

Avoid excessive logging that makes debugging difficult.

---

# 77. TESTING RULE

Before considering the project complete, verify:

### Data

* Data loads correctly
* Expected columns exist
* Target is valid
* Missing values are handled
* Categories are handled
* No unexpected leakage

### ML

* Training executes
* Validation executes
* Test evaluation executes
* Metrics are generated correctly
* Model artifact loads
* Predictions are reproducible

### Application

* App starts
* Inputs work
* Invalid inputs are handled
* Predictions are generated
* Model loads correctly

---

# 78. CLEAN ENVIRONMENT TEST

Where practical, verify that the project works from a clean environment using documented dependencies.

The project should not depend on undocumented local packages.

---

# 79. GIT RULE

Use Git for meaningful project history.

Commit logical milestones rather than every tiny change.

Examples:

```text
initial project structure
add dataset validation
implement preprocessing pipeline
add baseline model
add model comparison
add hyperparameter tuning
add explainability
add risk dashboard
finalize documentation
```

---

# 80. COMMIT MESSAGE RULE

Use concise, meaningful commit messages.

Prefer:

```text
feat: add churn preprocessing pipeline
feat: add baseline logistic regression
feat: add model comparison
fix: handle unseen categorical values
docs: update model evaluation
```

Avoid:

```text
update
changes
final
final2
final_final
working now
```

---

# 81. GITHUB RULE

The GitHub repository must not contain:

* Secrets
* Temporary files
* Large unnecessary generated files
* Environment-specific paths
* Debug artifacts
* Cache directories
* Personal machine information

Use an appropriate `.gitignore`.

---

# 82. MODEL FILE RULE

Large model artifacts should only be committed to GitHub if practical and appropriate.

If the artifact is too large:

* Document how to generate it.
* Use an appropriate artifact-storage approach if necessary.
* Do not silently omit the model from reproducibility instructions.

---

# 83. FINAL REVIEW RULE

Before marking the project complete, conduct a strict review.

Review from the perspective of:

### ML Engineer

Is the methodology correct?

### Software Engineer

Is the implementation clean?

### Data Scientist

Are the experiments and metrics valid?

### Technical Interviewer

Can the author explain the decisions?

### Recruiter

Does the repository communicate meaningful skills?

### Internship Evaluator

Does the project satisfy the stated requirements?

---

# 84. CRITICAL FIXES VS OPTIONAL IMPROVEMENTS

During final review, classify findings as:

## Critical Fix

Must be fixed before submission.

Examples:

* Data leakage
* Broken training pipeline
* Incorrect metric
* Fabricated result
* Broken inference
* Missing mandatory requirement

## Recommended Improvement

Significantly improves quality but is not essential.

## Optional Enhancement

Useful only if time permits.

Do not allow optional enhancements to delay critical fixes.

---

# 85. COMPLETION RULE

The project is complete only when:

```text
Implementation
      ↓
Testing
      ↓
Evaluation
      ↓
Documentation
      ↓
GitHub Review
      ↓
Technical Review
      ↓
Final QA
      ↓
Submission Package
```

A project that merely "runs" is not considered complete.

---

# 86. FINAL TRUTH RULE

The final repository must tell the truth about:

* What data was used
* What preprocessing was performed
* What models were trained
* What experiments were conducted
* What results were obtained
* What limitations exist
* What remains future work

If something is unknown, say so.

If something failed, document it.

If something was not tested, do not claim that it was tested.

---

# 87. IMPLEMENTATION ASSISTANT BEHAVIOR

The coding assistant should behave as:

**Implementation Engineer**

not:

**Project Owner**

The project owner is responsible for the overall technical direction.

The implementation assistant may:

* Write code
* Refactor code
* Debug code
* Suggest improvements
* Generate tests
* Update documentation
* Implement approved architecture
* Explain implementation choices

The implementation assistant must not silently:

* Change the project's objective
* Change the target
* Replace the dataset
* Change evaluation methodology
* Remove required functionality
* Introduce major architecture changes
* Fabricate results
* Claim unperformed experiments
* Expand scope unnecessarily

---

# 88. WHEN UNCERTAIN

If the assistant encounters a meaningful ambiguity:

### Low-impact ambiguity

Use the simplest reasonable interpretation and document it.

### High-impact ambiguity

Stop the affected implementation and request clarification.

Examples of high-impact ambiguity:

* Target definition
* Dataset replacement
* Evaluation methodology
* Major architecture change
* Final model-selection methodology
* Data leakage concern

---

# 89. DOCUMENTATION UPDATE RULE

Whenever a decision changes:

```text
Decision
   ↓
Implementation
   ↓
Affected Documentation
   ↓
Update Documentation
   ↓
Continue
```

Do not allow code and documentation to diverge.

---

# 90. PROJECT IDENTITY RULE

The project should consistently use:

**Customer Churn Prediction & Retention Intelligence System**

Avoid repeatedly changing the project name unless there is a deliberate branding decision.

---

# 91. PROFESSIONAL LANGUAGE RULE

Use clear, technically precise language throughout:

* README
* Code comments
* Documentation
* UI
* Reports
* Git commits
* Project descriptions

Avoid exaggerated marketing language.

---

# 92. PORTFOLIO INTEGRITY RULE

Any resume, LinkedIn, portfolio, or GitHub claim must be supported by the actual project.

For example:

If the project achieved a verified:

```text
ROC-AUC = 0.86
```

that may be reported.

If the model was not deployed publicly, do not claim:

> "Deployed production ML system."

If only a local Streamlit application exists, say so accurately.

---

# 93. INTERVIEW READINESS RULE

Before completion, the author should understand:

* Why the problem is classification
* Why the baseline was selected
* Why the final model was selected
* Why the metrics were selected
* How class imbalance was handled
* How leakage was prevented
* How preprocessing works
* How the model generates probabilities
* How risk ranking works
* How explainability works
* What the limitations are

The implementation is not considered successful if it cannot be explained.

---

# 94. FINAL PRINCIPLE

The project must follow this hierarchy:

```text
TRUTH
  ↓
CORRECTNESS
  ↓
REPRODUCIBILITY
  ↓
UNDERSTANDING
  ↓
ENGINEERING QUALITY
  ↓
EXPERIMENTATION
  ↓
PRESENTATION
  ↓
POLISH
```

Never reverse this order.

A simple correct project is better than an impressive-looking incorrect project.

A transparent limitation is better than a fabricated success.

A justified technical decision is better than unnecessary complexity.

A reproducible experiment is better than an unexplained high score.

---

# 95. RULE SUMMARY FOR IMPLEMENTATION ASSISTANT

Before every major implementation action, ask:

```text
1. Is this required?
2. Is this supported by the project documentation?
3. Is this supported by the actual data?
4. Does this introduce leakage?
5. Is this reproducible?
6. Is this technically justified?
7. Does this increase unnecessary complexity?
8. Does this affect another component?
9. Does documentation need updating?
10. Can the result actually be tested?
```

If the answer to any critical question is unclear, do not silently proceed.

---

# 96. GOLDEN RULE

> **Never sacrifice correctness, honesty, reproducibility, or understanding merely to make the project look more advanced.**

Build a project that can withstand technical scrutiny.

Build a project that the author can explain.

Build a project whose results can be reproduced.

Build a project that is genuinely worth putting on GitHub.

---

**End of RULES.md**

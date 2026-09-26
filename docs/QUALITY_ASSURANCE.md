# Quality Assurance & Validation Specification

## Customer Churn Prediction & Retention Intelligence System

**Project:** Machine Learning Internship Capstone — Project 1
**Domain:** Customer Churn Prediction
**Document Type:** Quality Assurance, Validation & Final Review Specification
**Version:** 1.0
**Status:** Planning
**Author:** Anurag
**Target Completion:** 30 September 2026

---

# 1. Purpose

This document defines the quality-assurance process for the Customer Churn Prediction project.

The purpose is to ensure that the final project is:

* Technically correct
* Scientifically sound
* Reproducible
* Free from avoidable data leakage
* Properly evaluated
* Robust against common implementation errors
* Professionally documented
* GitHub-ready
* Demonstrable
* Explainable by the project author

This document acts as a **quality gate** between implementation and final completion.

A project must not be declared complete merely because:

* The code runs
* A model produces predictions
* A Streamlit application opens
* A high metric is obtained
* The notebook executes without errors

The project is complete only when the implementation, ML methodology, results, documentation, and presentation have all passed the appropriate checks.

---

# 2. QA Philosophy

The project should optimize for:

```text
Correctness
    ↓
Data Integrity
    ↓
Leakage Prevention
    ↓
Valid Experimentation
    ↓
Reliable Evaluation
    ↓
Reproducibility
    ↓
Software Quality
    ↓
Application Reliability
    ↓
Documentation Accuracy
    ↓
Portfolio Readiness
```

Quality must not be judged by:

```text
More code
More models
Higher training score
More libraries
More charts
More UI effects
More buzzwords
```

A simpler implementation that is correct and well justified is preferable to a sophisticated implementation that is unreliable or difficult to explain.

---

# 3. QA Levels

The project will be reviewed at five levels.

## Level 1 — Data QA

Verifies that the dataset is understood, valid, clean enough for modeling, and properly separated.

## Level 2 — ML QA

Verifies that preprocessing, training, validation, evaluation, and model selection are technically sound.

## Level 3 — Software QA

Verifies that the implementation is modular, reproducible, maintainable, and executable.

## Level 4 — Application QA

Verifies that the optional Streamlit/demo layer behaves correctly.

## Level 5 — Documentation & Portfolio QA

Verifies that the project accurately represents the work and can be confidently presented publicly.

---

# 4. Critical QA Principle

## Never trust an impressive metric without validating how it was obtained.

A high ROC-AUC, F1-score, recall, or accuracy is not automatically evidence of a good model.

Before accepting a result, investigate:

* Dataset split
* Preprocessing
* Feature construction
* Leakage
* Class distribution
* Validation methodology
* Hyperparameter tuning
* Test-set usage
* Reproducibility

A suspiciously strong result must trigger investigation rather than celebration.

---

# 5. QA Severity Levels

All discovered issues should be classified.

### CRITICAL

The issue invalidates the model, results, application, or project integrity.

Examples:

* Data leakage
* Test-set contamination
* Fabricated results
* Incorrect target construction
* Broken inference pipeline
* Results that cannot be reproduced
* Incorrect evaluation methodology

**Action:** Must be fixed before completion.

---

### HIGH

The issue significantly reduces project quality or reliability.

Examples:

* Incorrect preprocessing
* Major mismatch between training and inference
* Poor validation strategy
* Important model-selection mistake
* Broken application workflow
* README containing materially incorrect results

**Action:** Must normally be fixed before finalization.

---

### MEDIUM

The issue does not invalidate the project but noticeably reduces quality.

Examples:

* Missing edge-case handling
* Weak error analysis
* Incomplete documentation
* Poor code organization
* Missing useful visualizations

**Action:** Fix if time permits; prioritize based on deadline.

---

### LOW

Minor polish issue.

Examples:

* Minor naming inconsistency
* Formatting issue
* Small UI improvement
* Non-critical comment/documentation issue

**Action:** Fix only after critical work is complete.

---

# 6. Dataset QA

Before model development is considered valid, verify the following.

## 6.1 Dataset Source

* [ ] Dataset source is legitimate.
* [ ] Source is documented.
* [ ] Dataset name is recorded.
* [ ] Dataset version/date is recorded where available.
* [ ] License or usage conditions are checked where applicable.
* [ ] Dataset acquisition process is documented.

---

## 6.2 Dataset Structure

Verify:

* [ ] Number of rows
* [ ] Number of columns
* [ ] Feature names
* [ ] Target column
* [ ] Data types
* [ ] Identifier columns
* [ ] Numerical features
* [ ] Categorical features
* [ ] Date/time fields if present

Record the findings.

---

## 6.3 Target Validation

Verify:

* [ ] Target exists.
* [ ] Target meaning is understood.
* [ ] Target encoding is correct.
* [ ] No unexpected target values exist.
* [ ] Missing target values are handled.
* [ ] Target distribution is documented.
* [ ] Target is not accidentally included as a feature.

The target definition must correspond to the actual churn problem.

---

## 6.4 Missing-Value QA

Check:

* [ ] Missing values by column
* [ ] Missing-value percentage
* [ ] Missing-value patterns
* [ ] Missing values in target
* [ ] Missing values in important features
* [ ] Imputation strategy

The project must not blindly fill every missing value with a single arbitrary value.

The selected strategy should be technically justified.

---

## 6.5 Duplicate QA

Check:

* [ ] Exact duplicate rows
* [ ] Duplicate customer identifiers
* [ ] Potential repeated customer records
* [ ] Whether duplicates represent legitimate repeated observations

Do not automatically delete duplicates without understanding what they represent.

---

## 6.6 Data-Type QA

Verify:

* [ ] Numeric columns are correctly represented.
* [ ] Categorical columns are correctly represented.
* [ ] Boolean values are handled correctly.
* [ ] Date fields are parsed correctly where applicable.
* [ ] Identifier fields are not accidentally treated as meaningful numerical features.

---

## 6.7 Outlier QA

For important numerical features:

* [ ] Investigate distributions.
* [ ] Identify unusual observations.
* [ ] Determine whether outliers are legitimate.
* [ ] Document any transformation/removal.
* [ ] Avoid arbitrary outlier deletion.

Outliers must be handled based on evidence.

---

# 7. Data Leakage QA

Data leakage is a **CRITICAL** issue.

The reviewer must explicitly check for:

## 7.1 Target Leakage

Verify that no feature directly or indirectly reveals the churn target.

Examples:

* Post-churn status
* Churn-related administrative fields
* Features derived directly from churn
* Future outcomes

---

## 7.2 Temporal Leakage

Where timestamps or temporal information exist, verify that features do not use information unavailable at prediction time.

---

## 7.3 Preprocessing Leakage

Verify that transformations such as:

* Imputation
* Scaling
* Encoding
* Feature selection
* Dimensionality reduction

are fitted only on training data when appropriate.

Use pipelines where suitable.

---

## 7.4 Test-Set Leakage

Verify that the final test set is not used to:

* Tune hyperparameters
* Select models repeatedly
* Design features based on results
* Choose thresholds through repeated optimization
* Make iterative modeling decisions

The test set should remain a final unbiased evaluation source.

---

# 8. Train / Validation / Test QA

Verify that the dataset splitting strategy is documented.

Where appropriate:

```text
Full Dataset
     │
     ├── Training Set
     │
     ├── Validation / Cross-Validation
     │
     └── Final Test Set
```

Check:

* [ ] Split performed correctly.
* [ ] Random state documented where applicable.
* [ ] Stratification used where appropriate.
* [ ] Test set remains isolated.
* [ ] No duplicated customers exist across splits when that would invalidate evaluation.
* [ ] Preprocessing respects split boundaries.

---

# 9. EDA QA

EDA must be reviewed for usefulness rather than quantity.

## Required Checks

* [ ] Target distribution
* [ ] Numerical distributions
* [ ] Important categorical distributions
* [ ] Missing-value analysis
* [ ] Outlier investigation
* [ ] Meaningful feature relationships
* [ ] Correlation analysis where appropriate
* [ ] Potential leakage investigation
* [ ] Dataset limitations

Every important visualization should answer a meaningful analytical question.

Avoid:

* Duplicate charts
* Decorative charts
* Charts without interpretation
* Charts included solely to increase notebook length

---

# 10. Feature Engineering QA

For every engineered feature, verify:

1. What does the feature represent?
2. Why is it useful?
3. How is it calculated?
4. Is it available at prediction time?
5. Could it leak future information?
6. Does it have a meaningful business interpretation?

Example:

```text
Feature:
Support Contact Frequency

Question:
Why?

Answer:
It may represent the intensity of customer-support interaction.

Leakage Check:
Does the calculation use post-churn support events?

If yes → INVALID
If no  → potentially valid
```

All engineered features must be traceable to real source data.

---

# 11. Preprocessing QA

Verify:

* [ ] Numerical preprocessing is appropriate.
* [ ] Categorical encoding is appropriate.
* [ ] Missing-value handling is reproducible.
* [ ] Scaling is applied where required.
* [ ] Tree-based models are not unnecessarily scaled.
* [ ] Training and inference preprocessing are identical.
* [ ] Feature order is preserved where required.
* [ ] Pipelines are used where they reduce leakage risk.

---

# 12. Baseline QA

The baseline must be established before final model selection.

Primary baseline:

**Logistic Regression**

Verify:

* [ ] Baseline trained correctly.
* [ ] Baseline uses the same appropriate data split methodology.
* [ ] Baseline metrics are recorded.
* [ ] Baseline limitations are discussed.

The baseline should serve as a meaningful benchmark rather than a checkbox.

---

# 13. Model Training QA

For each candidate model verify:

* [ ] Correct target used.
* [ ] Correct features used.
* [ ] Appropriate preprocessing.
* [ ] Training performed only on training data.
* [ ] Random state recorded where applicable.
* [ ] Model configuration recorded.
* [ ] Training errors handled.
* [ ] Model artifacts saved if required.

---

# 14. Model Comparison QA

Model comparison must be fair.

Verify:

* [ ] Same underlying evaluation methodology.
* [ ] Same target definition.
* [ ] Comparable validation strategy.
* [ ] Metrics calculated consistently.
* [ ] Test set not repeatedly used for selection.

Comparison must include, where applicable:

* ROC-AUC
* Precision
* Recall
* F1
* Calibration
* Computational considerations
* Interpretability
* Generalization

The final model must not be selected solely because it has the highest single metric.

---

# 15. Hyperparameter Tuning QA

Verify:

* [ ] Tuning performed only using training/validation data.
* [ ] Test set excluded from tuning.
* [ ] Search space is reasonable.
* [ ] Search method is documented.
* [ ] Best parameters recorded.
* [ ] Tuning improves or meaningfully changes model behavior.
* [ ] No unnecessary brute-force search.

If tuning does not meaningfully improve the model, that result should be documented rather than hidden.

---

# 16. Cross-Validation QA

Where cross-validation is used:

* [ ] Appropriate CV strategy selected.
* [ ] Stratification considered for imbalanced classification.
* [ ] Preprocessing occurs within the appropriate pipeline.
* [ ] Number of folds documented.
* [ ] Results recorded.
* [ ] Variability across folds inspected where useful.

Do not report only the best fold.

---

# 17. Evaluation QA

The final evaluation must include appropriate metrics.

## 17.1 ROC-AUC

Verify:

* [ ] Calculated from appropriate probability/score outputs.
* [ ] Correct target used.
* [ ] Final test set used only for final evaluation.

---

## 17.2 Precision

Verify:

```text
Precision = True Positives / (True Positives + False Positives)
```

Interpret the metric in the context of retention targeting.

---

## 17.3 Recall

Verify:

```text
Recall = True Positives / (True Positives + False Negatives)
```

Explain what missed churners represent in the business context.

---

## 17.4 F1

Verify that F1 is interpreted as a balance between precision and recall.

---

## 17.5 Calibration

Where probability-based decisions are used, verify:

* [ ] Calibration is evaluated.
* [ ] Calibration curve or appropriate metric is available.
* [ ] Probability interpretation is not overstated.
* [ ] Calibration methods, if used, are documented.

A probability such as `0.80` should not automatically be described as meaning "80% guaranteed chance of churn."

---

# 18. Threshold QA

Verify:

* [ ] Default 0.50 threshold is not blindly assumed to be optimal.
* [ ] Threshold selection is documented.
* [ ] Precision/recall trade-off is examined.
* [ ] Business implications are discussed.
* [ ] Threshold was not optimized on the final test set in a way that invalidates evaluation.

If a threshold is selected using validation data, final test performance should be reported using that fixed threshold.

---

# 19. Class Imbalance QA

If class imbalance exists:

* [ ] Imbalance is quantified.
* [ ] Accuracy is not treated as the only important metric.
* [ ] Appropriate metrics are used.
* [ ] Class weighting/sampling is justified if used.
* [ ] Sampling is performed only on appropriate training data.
* [ ] Validation/test distributions remain representative.

---

# 20. Error Analysis QA

The final model must be inspected beyond aggregate metrics.

Analyze:

### False Positives

```text
Predicted Churn
Actual No Churn
```

### False Negatives

```text
Predicted No Churn
Actual Churn
```

Investigate meaningful patterns.

Where data supports it, analyze errors by:

* Tenure
* Customer segment
* Contract
* Usage
* Billing
* Support interaction
* Other important features

Do not fabricate explanations for individual errors.

---

# 21. Explainability QA

Verify that explainability outputs are technically appropriate.

Possible approaches:

* Logistic Regression coefficients
* Tree-based feature importance
* Permutation importance
* SHAP

Check:

* [ ] Explanation method matches model type.
* [ ] Features are mapped correctly.
* [ ] Explanations are consistent with model output.
* [ ] No causal claims are made without causal evidence.
* [ ] Explanations are understandable to intended users.

Preferred language:

> "This feature contributed strongly to the prediction."

Avoid unsupported statements such as:

> "This feature caused the customer to churn."

---

# 22. Risk Ranking QA

Verify:

* [ ] Ranking uses actual model predictions.
* [ ] Probabilities are generated by the final model.
* [ ] Sorting direction is correct.
* [ ] Duplicate customers are not present.
* [ ] Risk categories are consistently assigned.
* [ ] Risk thresholds are documented.
* [ ] Displayed values match underlying model outputs.

---

# 23. Review-Reasons QA

Review reasons must be derived from actual evidence.

Valid sources may include:

* Model coefficients
* Feature importance
* SHAP values
* Clearly defined rule-based interpretations

Invalid behavior:

```text
Model predicts high risk
        ↓
System invents a plausible-sounding reason
```

The system must never invent a reason merely because it sounds reasonable.

---

# 24. Inference Pipeline QA

Training and inference must use compatible preprocessing.

Verify:

```text
Training Data
    ↓
Preprocessing
    ↓
Model
```

matches:

```text
New Customer
    ↓
Same Preprocessing
    ↓
Same Model
    ↓
Prediction
```

Check:

* [ ] Feature names match.
* [ ] Feature order is correct where relevant.
* [ ] Missing values are handled.
* [ ] Categorical values are handled.
* [ ] Model artifact loads correctly.
* [ ] Prediction output is valid.
* [ ] Probability is within expected range.
* [ ] Risk category is generated correctly.

---

# 25. Application QA

If Streamlit is implemented, test the application manually.

## 25.1 Startup

* [ ] Application launches successfully.
* [ ] No unexpected exceptions.
* [ ] Required dependencies are installed.
* [ ] Model artifacts load successfully.

---

## 25.2 Valid Input

Provide valid customer data.

Verify:

* [ ] Prediction generated.
* [ ] Probability displayed.
* [ ] Risk category displayed.
* [ ] Explanation displayed where supported.
* [ ] UI remains responsive.

---

## 25.3 Missing Input

Test missing required fields.

Verify:

* [ ] User receives a clear validation message.
* [ ] Application does not crash.

---

## 25.4 Invalid Input

Test:

* Negative values where impossible
* Invalid categorical values
* Incorrect data types
* Extreme values
* Empty fields

Verify graceful handling.

---

## 25.5 Boundary Testing

Test values near:

* Minimum
* Maximum
* Risk thresholds
* Expected valid ranges

Verify consistent behavior.

---

# 26. Dashboard QA

If a dashboard is implemented:

Verify:

* [ ] Metrics match source data.
* [ ] Charts display correctly.
* [ ] Filters work.
* [ ] Ranking is correct.
* [ ] Labels are understandable.
* [ ] No misleading visualizations.
* [ ] No hard-coded results unless explicitly intended.
* [ ] Refreshing the application does not corrupt state.

---

# 27. Reproducibility QA

A fresh environment should be able to reproduce the project.

Perform a clean-environment test where practical.

Verify:

* [ ] Dependencies documented.
* [ ] Installation instructions work.
* [ ] Dataset acquisition instructions work.
* [ ] Training process is documented.
* [ ] Inference process is documented.
* [ ] Random seeds are controlled where appropriate.
* [ ] File paths are portable.
* [ ] No dependency on undocumented local files.
* [ ] No hidden manual steps.

---

# 28. Code QA

Review the source code for:

### Readability

* [ ] Meaningful variable names
* [ ] Clear functions
* [ ] Reasonable function size
* [ ] Logical modules

### Maintainability

* [ ] Minimal duplication
* [ ] Reusable components
* [ ] Clear separation of concerns
* [ ] Configuration separated where useful

### Error Handling

* [ ] Expected errors handled.
* [ ] Helpful error messages.
* [ ] No silent failure.

### Security / Safety

* [ ] No secrets committed.
* [ ] No API keys in source.
* [ ] No credentials in screenshots.
* [ ] No sensitive customer information included unnecessarily.

---

# 29. Notebook QA

If notebooks are included:

* [ ] Notebook runs from top to bottom.
* [ ] Cells execute in logical order.
* [ ] No hidden state is required.
* [ ] Outputs correspond to current code.
* [ ] No stale results remain.
* [ ] Unnecessary exploratory cells are removed.
* [ ] Important conclusions are documented.
* [ ] Randomness is controlled where appropriate.

A notebook must not appear correct merely because old outputs are displayed.

---

# 30. Model Artifact QA

If trained models are saved:

* [ ] Model can be loaded.
* [ ] Preprocessing can be loaded.
* [ ] Version compatibility is documented where relevant.
* [ ] Artifact corresponds to final reported model.
* [ ] Inference works from the saved artifact.
* [ ] Artifact is not accidentally overwritten by an unrelated experiment.

---

# 31. Documentation QA

The documentation must accurately reflect the implementation.

Verify:

* [ ] Project title correct.
* [ ] Problem statement accurate.
* [ ] Dataset source accurate.
* [ ] Dataset description accurate.
* [ ] Methodology matches code.
* [ ] Model list matches experiments.
* [ ] Metrics match actual results.
* [ ] Final model matches actual model.
* [ ] Screenshots show actual application.
* [ ] Setup instructions work.
* [ ] Usage instructions work.
* [ ] Limitations are honestly documented.
* [ ] Future work is clearly separated from implemented functionality.

---

# 32. README QA

The final README should contain, where applicable:

* [ ] Project title
* [ ] Overview
* [ ] Problem statement
* [ ] Objectives
* [ ] Dataset
* [ ] Methodology
* [ ] ML pipeline
* [ ] Architecture
* [ ] Technologies
* [ ] Installation
* [ ] Usage
* [ ] Results
* [ ] Model comparison
* [ ] Visualizations
* [ ] Explainability
* [ ] Limitations
* [ ] Future improvements
* [ ] Project structure
* [ ] Reproducibility
* [ ] Author information

No section should claim functionality that does not actually exist.

---

# 33. Git/GitHub QA

Before final submission:

* [ ] Repository has logical structure.
* [ ] Meaningful commit history exists where practical.
* [ ] `.gitignore` is present.
* [ ] Secrets are excluded.
* [ ] Large unnecessary files are excluded.
* [ ] Dataset handling follows licensing/usage rules.
* [ ] README renders correctly.
* [ ] Code files are present.
* [ ] Required configuration files are present.
* [ ] No temporary/debug files remain.
* [ ] No accidental AI Studio project artifacts are included.

---

# 34. Attribution & Authenticity QA

The project must not contain unnecessary implementation-tool branding.

Check:

* [ ] No "Generated by Google AI Studio" text.
* [ ] No unnecessary "Built with Gemini" text.
* [ ] No AI Studio branding in the UI.
* [ ] No generated-by-AI comments.
* [ ] No AI-generated attribution claims.
* [ ] No fake human contributions.
* [ ] No fabricated experiment history.
* [ ] No fabricated results.

If a platform, API, library, dataset, or license requires attribution, that requirement must be respected.

The goal is not to conceal required attribution; the goal is to prevent irrelevant tool branding from being presented as part of the project.

---

# 35. Result Integrity QA

This is a **CRITICAL** review.

Every reported metric must have a traceable origin.

For example:

```text
README Metric
     ↓
Experiment Result
     ↓
Evaluation Code
     ↓
Actual Model
     ↓
Actual Dataset
```

If a number cannot be traced back to a real experiment, it must not be reported.

Never:

* Guess metrics
* Round metrics to make them look better
* Replace poor results with expected results
* Copy metrics from another project
* Use benchmark numbers as project results
* Claim improvement without comparison evidence

---

# 36. No Fabrication Policy

The following must never be fabricated:

* Dataset records
* Dataset sources
* Metrics
* Model performance
* Experiment results
* Screenshots
* Citations
* User studies
* Business impact
* Deployment claims
* Interview results
* External validation

If something has not been tested, state:

> "Not yet tested."

If something is planned but not implemented, state:

> "Planned."

If something was implemented but not validated, state:

> "Implemented; validation pending."

---

# 37. Performance QA

The project should be reasonably efficient for the dataset size.

Check:

* [ ] Training completes within reasonable time.
* [ ] No unnecessary repeated computation.
* [ ] Memory usage is reasonable.
* [ ] Application startup is reasonable.
* [ ] Prediction latency is acceptable for the intended demo.

Do not optimize prematurely.

Correctness takes priority over micro-optimization.

---

# 38. Edge-Case QA

Where applicable, test:

### Data

* Empty dataset
* Missing columns
* Unexpected categorical value
* Missing customer ID
* Missing target
* Extreme numerical values
* Duplicate customer IDs

### Model

* Model file missing
* Corrupted model file
* Incompatible feature schema
* Missing feature

### Application

* Empty input
* Invalid input
* Boundary values
* Unexpected input type

The application should fail gracefully rather than producing misleading results.

---

# 39. Security QA

Verify:

* [ ] No API keys in repository.
* [ ] No passwords.
* [ ] No access tokens.
* [ ] No private credentials.
* [ ] No unnecessary personal/customer information.
* [ ] Sensitive local files are excluded through `.gitignore`.
* [ ] Environment variables are used where secrets are required.

If external APIs are introduced later, secrets must never be hard-coded.

---

# 40. Final External Reviewer Test

Before declaring completion, review the project as if you were:

### Internship Evaluator

Ask:

> Does this satisfy the internship requirements?

### ML Engineer

Ask:

> Is the methodology technically correct?

### Senior Developer

Ask:

> Is the code maintainable?

### Data Scientist

Ask:

> Are the experiments and metrics trustworthy?

### Technical Interviewer

Ask:

> Can the author explain every important decision?

### Recruiter

Ask:

> Does the repository demonstrate meaningful skills?

### GitHub Reviewer

Ask:

> Can another developer understand and reproduce this project?

A project should pass all perspectives reasonably well.

---

# 41. Final QA Checklist

## A. Requirements

* [ ] Internship requirements implemented.
* [ ] No mandatory requirement omitted.
* [ ] Additional features are clearly distinguished from mandatory scope.

## B. Data

* [ ] Legitimate dataset.
* [ ] Source documented.
* [ ] Target verified.
* [ ] Missing values handled.
* [ ] Duplicates investigated.
* [ ] Outliers investigated.
* [ ] Class imbalance investigated.
* [ ] Leakage investigated.

## C. ML

* [ ] Baseline implemented.
* [ ] Multiple suitable models compared.
* [ ] Validation strategy sound.
* [ ] Hyperparameter tuning justified.
* [ ] Metrics appropriate.
* [ ] Calibration evaluated.
* [ ] Threshold considered.
* [ ] Error analysis completed.
* [ ] Final model justified.

## D. Explainability

* [ ] Feature importance/explanation available where appropriate.
* [ ] Review reasons evidence-based.
* [ ] No causal claims without evidence.

## E. Engineering

* [ ] Code modular.
* [ ] Dependencies documented.
* [ ] Reproducible.
* [ ] No hard-coded secrets.
* [ ] No unnecessary complexity.
* [ ] Tests/checks completed.

## F. Application

* [ ] Application launches.
* [ ] Valid inputs work.
* [ ] Invalid inputs handled.
* [ ] Model loading works.
* [ ] Predictions are correct.
* [ ] Risk ranking works.
* [ ] UI matches actual functionality.

## G. Documentation

* [ ] README complete.
* [ ] Results accurate.
* [ ] Methodology accurate.
* [ ] Limitations documented.
* [ ] Setup tested.
* [ ] Screenshots accurate.

## H. GitHub

* [ ] Repository organized.
* [ ] `.gitignore` present.
* [ ] No secrets.
* [ ] No unnecessary temporary files.
* [ ] Repository is reproducible.

## I. Authenticity

* [ ] No fabricated results.
* [ ] No fabricated citations.
* [ ] No fabricated datasets.
* [ ] No false claims.
* [ ] No unnecessary AI Studio branding.
* [ ] Required third-party attribution respected.

---

# 42. Critical Fixes Before Completion

Any of the following automatically prevents the project from being marked complete:

1. Data leakage
2. Test-set contamination
3. Incorrect target definition
4. Invalid evaluation methodology
5. Fabricated metrics
6. Fabricated results
7. Non-reproducible final model
8. Broken inference pipeline
9. Major mismatch between reported and actual implementation
10. Application producing incorrect predictions
11. Missing mandatory internship requirement
12. Exposed credentials or secrets

---

# 43. Recommended Improvements

If the project passes all critical checks, consider:

* Better probability calibration
* Better threshold analysis
* Stronger error analysis
* More meaningful explainability
* Improved feature engineering
* Cleaner application UX
* Additional validation checks
* Better README visuals
* Better experiment documentation

These should never delay critical fixes.

---

# 44. Optional Enhancements

Only if sufficient time remains:

* SHAP visualizations
* Interactive filtering
* Advanced dashboard components
* Additional model comparison
* Automated data validation
* More extensive testing
* Additional segmentation analysis

Optional enhancements must not destabilize the working project.

---

# 45. QA Decision Matrix

At the final review, classify the project as:

### ❌ NOT READY

One or more critical issues remain.

Action:

```text
Identify Issue
      ↓
Fix
      ↓
Re-test
      ↓
Re-review
```

---

### ⚠️ CONDITIONALLY READY

No critical issues remain, but important medium/high-quality improvements remain.

Action:

* Complete high-priority fixes.
* Document known limitations.
* Proceed only if deadline pressure requires it.

---

### ✅ READY FOR SUBMISSION

All mandatory requirements are satisfied.

No critical issues remain.

The project has:

* Valid ML methodology
* Reliable evaluation
* Reproducible implementation
* Working application where applicable
* Accurate documentation
* Clean repository
* Honest results

---

### ⭐ PORTFOLIO READY

The project satisfies submission requirements and additionally demonstrates:

* Strong engineering
* Meaningful experimentation
* Clear explanations
* Good documentation
* Professional presentation
* Defensible technical decisions
* Interview-level understanding

---

# 46. Final Sign-Off

The project may only be marked:

> **PROJECT 1 — COMPLETE**

when the following statement is true:

> The Customer Churn Prediction project has been implemented according to its documented requirements, tested against the defined quality criteria, evaluated using valid methodology, reviewed for leakage and reproducibility, documented accurately, and packaged in a professional form suitable for internship submission and portfolio presentation.

Final status:

```text
[ ] NOT READY
[ ] CONDITIONALLY READY
[ ] READY FOR SUBMISSION
[ ] PORTFOLIO READY
```

---

# 47. Final Principle

A project is not successful because the model achieved a high score.

A successful project is one where the author can confidently answer:

> **What problem did I solve?**

> **Why did I formulate it this way?**

> **Where did the data come from?**

> **How did I prepare it?**

> **How did I prevent leakage?**

> **Why did I choose these models?**

> **How did I evaluate them?**

> **Why did I select the final model?**

> **Where does the model fail?**

> **How do I explain its predictions?**

> **Can someone reproduce my result?**

> **What are the limitations?**

> **What would I improve next?**

If those questions can be answered honestly and technically, the project has achieved its real objective.

**Correctness before complexity.
Evidence before claims.
Understanding before presentation.
Quality before quantity.**

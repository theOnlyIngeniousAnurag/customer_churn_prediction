# Product Requirements Document (PRD)

## Customer Churn Prediction & Retention Intelligence System

**Project Type:** Machine Learning Internship Capstone
**Domain:** Customer Analytics / Subscription Retention
**ML Problem:** Binary Classification
**Primary Language:** Python
**Primary Development Environment:** Google AI Studio + Local Development Environment
**Primary ML Framework:** scikit-learn
**Optional Application Layer:** Streamlit
**Version:** 1.0
**Status:** Planning
**Author:** Anurag
**Target Completion:** 30 September 2026

---

# 1. Product Overview

## 1.1 Product Name

**Customer Churn Prediction & Retention Intelligence System**

The final project should be presented as a practical machine-learning decision-support system rather than as a simple academic classification exercise.

---

## 1.2 Product Vision

Build a reliable, reproducible, interpretable machine-learning system that estimates the probability that a customer will churn and helps a business identify and prioritize high-risk customers for retention review.

The system should not merely answer:

> "Will this customer churn?"

It should provide a more useful decision-support output:

> "How likely is this customer to churn, what factors are associated with that prediction, and which customers should be reviewed first?"

---

# 2. Problem Statement

Customer churn represents the loss of existing customers from a subscription or recurring-service business.

The objective of this project is to use historical customer information such as demographics, tenure, usage behavior, support interactions, and billing information to predict whether a customer is likely to leave the service.

The internship project requirements specifically identify:

* Customer demographics
* Customer tenure
* Usage information
* Support interactions
* Billing history
* Missing-value handling
* Categorical-variable handling
* Outlier analysis
* Class-imbalance handling
* Feature engineering
* Logistic regression
* Tree-based models
* ROC-AUC
* Precision
* Recall
* F1-score
* Calibration
* High-risk customer ranking
* Suggested review reasons

These requirements form the minimum functional scope of the project.

---

# 3. Business Objective

The system should help a hypothetical subscription business prioritize customers who may require retention attention.

The model should support the following business workflow:

```text
Historical Customer Data
        ↓
Data Quality & Preparation
        ↓
Machine Learning Model
        ↓
Churn Probability
        ↓
Risk Classification
        ↓
Customer Ranking
        ↓
Reason / Explanation
        ↓
Retention Review
```

The system is intended to support human decision-making.

It should NOT automatically make irreversible business decisions such as:

* cancelling customers,
* changing customer contracts,
* automatically issuing refunds,
* automatically changing prices,
* automatically contacting customers without explicit business logic.

---

# 4. Target Users

The project is primarily designed for demonstration and portfolio purposes, while representing a realistic business use case.

Potential users include:

### 4.1 Retention Analyst

Needs to identify customers with elevated churn risk.

### 4.2 Customer Success Team

Needs customer-level risk information and possible contributing factors.

### 4.3 Business Analyst

Needs aggregate churn patterns and model insights.

### 4.4 ML Engineer / Data Scientist

Needs reproducible preprocessing, experimentation, evaluation, and inference.

### 4.5 Technical Reviewer

Needs to inspect the project's methodology, code quality, assumptions, experiments, and reproducibility.

---

# 5. Product Goals

## 5.1 Primary Goals

The system must:

1. Load and validate customer data.
2. Analyze the dataset before modeling.
3. Identify data-quality issues.
4. Handle missing values appropriately.
5. Handle categorical variables correctly.
6. Investigate outliers.
7. Investigate class imbalance.
8. Prevent data leakage.
9. Engineer meaningful customer-behavior features where supported by the dataset.
10. Establish a baseline model.
11. Train multiple appropriate classification models.
12. Compare models using appropriate metrics.
13. Perform hyperparameter tuning where justified.
14. Evaluate model generalization.
15. Examine model calibration.
16. Perform error analysis.
17. Generate customer-level churn probabilities.
18. Rank customers according to risk.
19. Provide interpretable reasons for elevated risk where technically supported.
20. Provide reproducible inference.
21. Provide professional documentation.
22. Produce a GitHub-ready project.
23. Provide a simple application/demo if it provides meaningful value.

---

# 6. Secondary Goals

Where time and data quality permit, the project may additionally provide:

* Probability calibration visualization
* Threshold analysis
* Feature importance
* SHAP-based explanations
* Risk categories
* Customer-level prediction explanations
* Interactive Streamlit dashboard
* Model artifact saving/loading
* Reproducible training pipeline
* Automated validation checks

These are enhancements, not mandatory requirements if they compromise correctness or the project deadline.

---

# 7. Non-Goals

The following are explicitly outside the project's required scope unless later justified:

* Deep learning
* Large language models
* Computer vision
* Unnecessary external APIs
* Microservice architecture
* Kubernetes
* Complex cloud infrastructure
* Real-time streaming systems
* Automated customer communication
* Automated retention campaigns
* Production-scale distributed training
* Artificially complex model architectures

Complexity must have a legitimate technical purpose.

---

# 8. Machine Learning Objective

## 8.1 Target

The target variable should represent whether the customer churned.

Conceptually:

```text
Churn = 1 → Customer churned
Churn = 0 → Customer did not churn
```

The exact target column and encoding must be determined from the selected dataset.

Do NOT assume the target column name or encoding before inspecting the dataset.

---

# 9. ML Problem Type

This project is primarily a:

**Supervised Binary Classification Problem**

Input:

```text
Customer Features
```

Output:

```text
Probability of Churn
+
Predicted Churn Class
```

The probability output is important because customer retention is generally a prioritization problem rather than merely a yes/no classification problem.

---

# 10. Core Product Outputs

For each customer, the final system should ideally provide:

| Output                | Description                                     |
| --------------------- | ----------------------------------------------- |
| Customer ID           | Unique customer identifier where available      |
| Churn Probability     | Estimated probability of churn                  |
| Risk Category         | Interpretable risk grouping                     |
| Predicted Class       | Churn / No Churn                                |
| Key Factors           | Important contributing features where supported |
| Review Recommendation | Suggested reason for review                     |

Example conceptual output:

```text
Customer ID: CUST_00124

Churn Probability: 0.82
Risk Category: High

Predicted Churn: Yes

Potential Review Factors:
- Short customer tenure
- Declining usage
- Recent billing change
- High support-contact frequency
```

The actual factors must be generated from real model/data evidence.

They must never be fabricated.

---

# 11. Dataset Requirements

The selected dataset should contain, where reasonably available:

### Customer Information

* Customer identifier
* Demographics
* Account information
* Tenure

### Usage Information

* Usage frequency
* Usage volume
* Activity measures
* Relevant behavioral variables

### Support Information

* Number of support contacts
* Complaints
* Service interactions
* Relevant customer-service indicators

### Billing Information

* Billing amount
* Payment behavior
* Payment method
* Contract/subscription information
* Relevant billing changes

### Target

* Churn indicator

The actual availability of these variables depends on the selected real-world dataset.

Do not fabricate missing business fields.

---

# 12. Data Source Principle

The project must use a legitimate, documented dataset.

The dataset source must be recorded in the project's documentation.

The project must clearly distinguish:

* Original dataset information
* Derived features
* Assumptions
* Cleaning operations
* Transformations

No fabricated dataset or fabricated data source may be used.

---

# 13. Data Quality Requirements

Before model training, the project must investigate:

### Missing Values

* Number of missing values
* Missing-value percentage
* Columns affected
* Appropriate imputation strategy

### Duplicates

* Duplicate rows
* Duplicate customer IDs where applicable
* Potential repeated records

### Data Types

* Numerical variables
* Categorical variables
* Dates
* Boolean fields
* Identifier fields

### Outliers

Investigate unusual numerical observations.

Do not automatically remove outliers.

An outlier should only be transformed or removed when there is a justified reason.

### Target Quality

Verify:

* Target values
* Target encoding
* Class distribution
* Unexpected labels
* Missing target values

---

# 14. Data Leakage Prevention

Data leakage is a critical quality concern.

The model must not receive information during training that would not realistically be available when making a churn prediction.

Examples of potential leakage include:

* Post-churn information
* Future customer behavior
* Features derived from the target
* Information created after the prediction point
* Preprocessing fitted using the complete dataset before splitting

All preprocessing operations that learn parameters from the data must be fitted only on the appropriate training data.

---

# 15. Exploratory Data Analysis

EDA must be analytical rather than decorative.

The analysis should investigate:

### Target Distribution

* Churn vs non-churn counts
* Churn percentage
* Class imbalance

### Numerical Features

* Distributions
* Central tendency
* Spread
* Outliers

### Categorical Features

* Category frequencies
* Churn rate by category where meaningful

### Relationships

Investigate meaningful relationships between customer characteristics and churn.

### Correlations

Analyze correlations where appropriate while recognizing that correlation does not establish causation.

### Data Quality

EDA should also reveal:

* Suspicious values
* Constant columns
* High-cardinality variables
* Potential leakage
* Dataset limitations

Every visualization should answer a question.

---

# 16. Feature Engineering

Feature engineering should be driven by the available dataset and business meaning.

Potential examples include:

* Usage trend
* Support-contact frequency
* Recent payment changes
* Tenure groups
* Average usage
* Recency-related features
* Support-contact intensity
* Billing-to-usage relationships

Only features that can be legitimately derived from the available data should be created.

Do not create artificial features simply to increase model performance.

---

# 17. Baseline Model

A simple baseline must be established before complex modeling.

The primary baseline should be:

**Logistic Regression**

The baseline provides:

* A reference performance level
* An interpretable model
* A benchmark for later models

The baseline must be evaluated using the same validation methodology as competing models.

---

# 18. Candidate Models

Appropriate candidate models may include:

### Model A

Logistic Regression

### Model B

Decision Tree

### Model C

Random Forest

### Model D

Gradient Boosting / XGBoost or another appropriate boosting model

The exact model set should depend on:

* Dataset size
* Feature types
* Computational constraints
* Library availability
* Time available
* Model interpretability

Do not add models without a technical reason.

---

# 19. Model Comparison

Models should be compared fairly.

A comparison table should eventually include:

| Model    | ROC-AUC | Precision | Recall | F1 | Calibration | Notes |
| -------- | ------: | --------: | -----: | -: | ----------- | ----- |
| Baseline |         |           |        |    |             |       |
| Model A  |         |           |        |    |             |       |
| Model B  |         |           |        |    |             |       |
| Model C  |         |           |        |    |             |       |

Actual values must come from real experiments.

No performance number may be invented.

---

# 20. Evaluation Strategy

The evaluation strategy must reflect the actual business problem.

Primary metrics include:

### ROC-AUC

Measures ranking/discrimination ability across classification thresholds.

### Precision

Among customers predicted as churners, how many actually churned?

### Recall

Among customers who actually churned, how many did the model identify?

### F1-score

Harmonic mean of precision and recall.

### Calibration

Measures whether predicted probabilities correspond reasonably to observed frequencies.

---

# 21. Threshold Analysis

The default classification threshold of 0.50 must not automatically be treated as optimal.

Where appropriate, investigate different thresholds.

For example:

```text
Probability
    ↓
0.20 ───────── Low threshold
0.40 ───────── Moderate
0.60 ───────── Higher
0.80 ───────── Very high
```

The appropriate threshold should depend on the intended business trade-off between:

* False positives
* False negatives
* Retention resources

The project should explain the selected threshold rather than simply assuming one.

---

# 22. Class Imbalance

If churn classes are imbalanced, investigate:

* Class distribution
* Class weights
* Appropriate sampling techniques
* Threshold adjustment
* Precision/recall trade-offs

Accuracy should not be used as the primary metric when class imbalance makes it misleading.

---

# 23. Cross-Validation

Where appropriate, use cross-validation for model development and comparison.

The validation methodology must prevent information leakage.

For imbalanced classification, stratified cross-validation should be considered where appropriate.

The final test set must remain untouched until final evaluation.

---

# 24. Hyperparameter Tuning

Hyperparameter tuning should focus only on parameters that can meaningfully affect model performance.

Possible methods:

* Grid Search
* Randomized Search
* Other appropriate search methods

Tuning should not become an uncontrolled search over dozens of configurations.

The experiment log should record:

* Model
* Parameters
* Validation method
* Metrics
* Result
* Interpretation

---

# 25. Error Analysis

The project must investigate where the model makes mistakes.

Analyze:

### False Positives

Customers predicted to churn who did not churn.

### False Negatives

Customers who churned but were not identified.

Where possible, investigate whether errors are associated with:

* Customer segments
* Tenure
* Usage patterns
* Contract type
* Billing characteristics
* Support behavior

The purpose is to understand model limitations, not merely to improve a score.

---

# 26. Explainability

The final model should provide interpretable information where technically appropriate.

Possible methods:

* Model coefficients
* Feature importance
* Permutation importance
* SHAP

The selected method should depend on the final model.

Explainability output must distinguish:

**Model association/importance**

from:

**Causal explanation**

The system must never claim:

> "This feature caused the customer to churn."

unless causal evidence actually exists.

Preferred language:

> "This feature contributed strongly to the model's prediction."

---

# 27. Customer Risk Ranking

The final system should produce a ranked list such as:

```text
Rank | Customer | Churn Probability | Risk
------------------------------------------------
1    | C001     | 0.91              | High
2    | C042     | 0.87              | High
3    | C017     | 0.81              | High
...
```

The ranking should be based on model-generated probabilities.

Risk categories must have clearly documented definitions.

---

# 28. Application / Demo

A lightweight Streamlit application may be created if it provides meaningful value.

Potential sections:

### Dashboard

* Overall churn statistics
* Churn distribution
* Key patterns

### Customer Prediction

Allow a user to provide customer information and receive:

* Churn probability
* Risk category
* Prediction
* Key factors

### Risk Ranking

Display high-risk customers.

### Model Information

Show:

* Final model
* Evaluation metrics
* Important features
* Dataset information

The UI should remain clean and professional.

It should not introduce unnecessary visual complexity.

---

# 29. Reproducibility

The project should be reproducible.

Where applicable:

* Set random seeds
* Record dependencies
* Save preprocessing/model artifacts
* Keep training and inference logic consistent
* Document dataset acquisition
* Document execution steps
* Avoid hard-coded machine-specific paths

---

# 30. Code Architecture

The implementation should avoid putting the entire project into one enormous notebook.

A suitable structure may be:

```text
customer-churn-prediction/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 01_eda_and_experiments.ipynb
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── utils/
│
├── app/
│   └── streamlit_app.py
│
├── models/
│
├── reports/
│
├── tests/
│
├── docs/
│
├── requirements.txt
├── README.md
└── .gitignore
```

The final structure may be modified after inspecting the actual implementation requirements.

---

# 31. Documentation Requirements

The final project documentation should explain:

* Problem
* Dataset
* Methodology
* Data preparation
* Feature engineering
* Models
* Experiments
* Metrics
* Model selection
* Explainability
* Limitations
* Reproducibility
* Usage

Documentation must match the actual implementation.

---

# 32. Portfolio Requirements

The final project should be suitable for presentation on:

* GitHub
* Resume
* LinkedIn
* Portfolio
* Technical interviews

The project must never claim results that were not actually obtained.

Resume metrics must only be added after experiments produce verified results.

---

# 33. AI Implementation Assistant Rules

Google AI Studio may be used as the implementation assistant for this project.

However, AI Studio must operate under the technical direction and project specifications contained in the project's documentation.

AI Studio must:

1. Read the project documentation before making substantial implementation changes.
2. Follow the project's defined architecture.
3. Preserve documented technical decisions.
4. Ask for clarification when a requirement is genuinely ambiguous.
5. Avoid inventing missing requirements.
6. Avoid fabricating datasets.
7. Avoid fabricating metrics.
8. Avoid fabricating experiment results.
9. Avoid fabricating citations.
10. Avoid claiming that an experiment was performed when it was not.
11. Keep code modular and maintainable.
12. Prefer simple technically justified solutions.
13. Avoid unnecessary technologies.
14. Maintain reproducibility.
15. Keep documentation synchronized with the actual implementation.

---

# 34. Project Attribution / Branding Rule

The project should be presented as the user's own internship/capstone work.

Do not add unnecessary references to:

* Google AI Studio
* Gemini
* AI-generated
* AI-assisted
* Generated by AI
* Built by Google AI Studio
* AI Studio branding

to:

* Application UI
* README
* Documentation
* Source-code comments
* Project titles
* User-facing messages
* Screenshots
* Metadata

unless such attribution is explicitly required by a third-party license, API/platform requirement, or applicable policy.

Do not fabricate authorship, research, results, experiments, or contributions.

The final project must accurately represent work that the user understands and can explain.

---

# 35. Quality Principle

The project should optimize for:

```text
Correctness
    ↓
Understanding
    ↓
Reliable Evaluation
    ↓
Reproducibility
    ↓
Clean Engineering
    ↓
Interpretability
    ↓
Professional Presentation
    ↓
Portfolio Value
```

Do not optimize for:

```text
More libraries
More models
More code
More buzzwords
More visual effects
```

Technical quality takes priority over apparent complexity.

---

# 36. Definition of Done

Project 1 should not be considered complete until:

### Data

* [ ] Legitimate dataset selected
* [ ] Dataset source documented
* [ ] Data loaded successfully
* [ ] Data types checked
* [ ] Missing values analyzed
* [ ] Duplicates investigated
* [ ] Outliers investigated
* [ ] Target verified
* [ ] Class imbalance analyzed
* [ ] Leakage risks investigated

### ML

* [ ] Problem formulation finalized
* [ ] Evaluation strategy defined
* [ ] Baseline trained
* [ ] Multiple appropriate models tested
* [ ] Models fairly compared
* [ ] Hyperparameters tuned where justified
* [ ] Final model selected
* [ ] Test evaluation completed
* [ ] Calibration evaluated
* [ ] Error analysis completed
* [ ] Explainability implemented where appropriate

### Product

* [ ] Churn probabilities generated
* [ ] Risk ranking generated
* [ ] Review reasons generated from real model evidence
* [ ] Application/demo completed if justified
* [ ] Input validation implemented
* [ ] Model loading/inference tested

### Engineering

* [ ] Code organized
* [ ] Dependencies documented
* [ ] Reproducibility checked
* [ ] Tests/checks completed
* [ ] No unnecessary hard-coded paths
* [ ] No fabricated results
* [ ] No unsupported claims

### Documentation

* [ ] README completed
* [ ] Methodology documented
* [ ] Results documented
* [ ] Limitations documented
* [ ] Dataset source documented
* [ ] Setup instructions verified
* [ ] Screenshots added where appropriate
* [ ] GitHub structure finalized

### Portfolio

* [ ] Resume bullets prepared
* [ ] LinkedIn description prepared
* [ ] Interview talking points prepared
* [ ] Technical decisions explainable by the author

---

# 37. Guiding Principle

This project is not being built merely to satisfy an internship checklist.

The objective is to produce a technically correct, understandable, reproducible, and professionally presented machine-learning project that the author can confidently explain during:

* Internship evaluation
* Faculty review
* Technical interviews
* Resume discussions
* GitHub reviews
* Future ML opportunities

**Build it correctly first. Make it impressive through substance, not artificial complexity.**

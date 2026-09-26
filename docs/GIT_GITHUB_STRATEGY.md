# Git & GitHub Strategy

## Customer Churn Prediction & Retention Intelligence System

**Project:** Machine Learning Internship Capstone — Project 1
**Repository Type:** Professional Machine Learning Project
**Version:** 1.0
**Status:** Planning / Implementation Preparation
**Author:** Anurag
**Target Completion:** 30 September 2026

---

# 1. Purpose

This document defines the Git and GitHub strategy for the Customer Churn Prediction project.

The purpose is to ensure that the repository demonstrates:

* Professional software-engineering practices
* Reproducible machine-learning development
* Meaningful version history
* Clear project organization
* Traceable experimentation
* Clean documentation
* Safe handling of datasets and model artifacts
* Portfolio-ready presentation

GitHub should not merely contain the final source code.

It should communicate how the project was structured, developed, evaluated, and finalized.

---

# 2. Repository Objective

The repository should serve four purposes simultaneously:

### 2.1 Development Repository

Used to manage source code, notebooks, configuration, tests, documentation, and project assets.

### 2.2 Reproducibility Record

Used to preserve the information necessary for another developer to understand and reproduce the project.

### 2.3 Technical Portfolio

Used to demonstrate:

* Python development
* Machine-learning knowledge
* Data analysis
* Experimentation
* Evaluation
* Software engineering
* Documentation

### 2.4 Internship Submission Repository

The final repository must be clean enough to submit or share with the internship evaluator.

---

# 3. Repository Naming

Preferred repository name:

```text
customer-churn-prediction
```

Alternative names may be considered only if there is a strong reason.

Avoid names such as:

```text
ml-project-final
project1
internship-project
churn-ai-final-final
customer-churn-project-new
```

Repository names should be:

* Short
* Descriptive
* Professional
* Searchable
* Stable

---

# 4. Repository Visibility

The repository may be public if:

* The dataset permits public redistribution/reference.
* No private or sensitive customer information is included.
* No API keys or credentials are exposed.
* No restricted internship material is published.

If the dataset has redistribution restrictions, the repository must contain:

* Dataset source
* Dataset acquisition instructions
* Required license/usage information
* A clear explanation that the raw dataset is not included

Never upload confidential or sensitive customer information.

---

# 5. Recommended Repository Structure

The repository should approximately follow:

```text
customer-churn-prediction/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
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
│   ├── TASK_TRACKER.md
│   └── QUALITY_ASSURANCE.md
│
├── models/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_model_experiments.ipynb
│
├── reports/
│   ├── figures/
│   └── results/
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── utils/
│
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

The exact structure may change based on implementation requirements.

Do not create empty directories merely to match this template.

---

# 6. Directory Responsibilities

## 6.1 `app/`

Contains the user-facing application.

Example:

```text
app/
└── streamlit_app.py
```

Application code should remain separate from core ML logic.

---

## 6.2 `data/`

Contains dataset-related files.

Recommended:

```text
data/
├── raw/
├── processed/
└── README.md
```

### `raw/`

Original dataset files where legally and technically appropriate.

### `processed/`

Generated datasets created by the preprocessing pipeline.

Processed data should not be manually modified without documentation.

### `README.md`

Should explain:

* Dataset source
* Download instructions
* Expected filenames
* Data licensing
* Whether files are intentionally excluded from Git

---

# 7. Dataset and Privacy Rules

Never commit:

* Private customer information
* Personally identifiable information
* Passwords
* API keys
* Access tokens
* Private credentials
* Confidential internship files
* Unapproved proprietary datasets

If a dataset contains sensitive information, create a reproducible acquisition process instead.

Example:

```text
Repository
    ↓
Dataset instructions
    ↓
User downloads dataset
    ↓
Dataset placed in data/raw/
    ↓
Pipeline processes dataset
```

---

# 8. `src/`

All reusable production-oriented Python logic should live here.

Recommended organization:

```text
src/
├── data/
├── features/
├── models/
├── evaluation/
└── utils/
```

### `src/data/`

Data loading and validation.

### `src/features/`

Preprocessing and feature engineering.

### `src/models/`

Training, model construction, saving, and loading.

### `src/evaluation/`

Metrics, evaluation utilities, comparison reports, and error analysis.

### `src/utils/`

Small reusable helper functions.

Do not place unrelated functionality into `utils/` merely because it is convenient.

---

# 9. `notebooks/`

Notebooks should primarily be used for:

* Exploration
* Visualization
* Experiment analysis
* Demonstration
* Research-oriented investigation

Notebooks should not become the only place where important reusable logic exists.

Reusable logic should be moved into `src/`.

---

# 10. Notebook Naming Convention

Use ordered descriptive names.

Example:

```text
01_eda.ipynb
02_baseline_model.ipynb
03_model_comparison.ipynb
04_hyperparameter_tuning.ipynb
05_error_analysis.ipynb
```

Only create separate notebooks when they provide meaningful organizational value.

Avoid:

```text
final.ipynb
final2.ipynb
final_latest.ipynb
final_latest_updated.ipynb
test.ipynb
new.ipynb
```

---

# 11. `models/`

This directory may contain trained model artifacts when appropriate.

Examples:

```text
models/
├── preprocessing_pipeline.joblib
├── churn_model.joblib
└── model_metadata.json
```

Model artifacts should only be committed when:

* They are reasonably sized.
* They are necessary for the demo/application.
* Licensing permits it.
* They can be reproduced from documented training code.

Large artifacts should not be committed directly to Git.

---

# 12. `reports/`

Contains generated project outputs that are useful for review.

Possible contents:

```text
reports/
├── figures/
└── results/
```

Examples:

* Confusion matrix
* ROC curve
* Precision-recall curve
* Calibration plot
* Feature importance
* Model comparison table
* Error-analysis outputs

Generated outputs must correspond to actual experiments.

---

# 13. Documentation Files

The project documentation should be organized under `docs/`.

The primary control documents are:

```text
docs/
├── PRD.md
├── PROJECT_SPECIFICATIONS.md
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

These documents collectively define the project's development contract.

Implementation should follow them.

If implementation requires a change to a documented decision, update the relevant document rather than silently deviating from it.

---

# 14. README.md

The root `README.md` is the public-facing entry point.

It should eventually contain:

1. Project title
2. Short description
3. Problem statement
4. Key objectives
5. Features
6. Dataset information
7. ML methodology
8. Architecture/pipeline
9. Technologies
10. Installation
11. Usage
12. Results
13. Model comparison
14. Screenshots
15. Limitations
16. Future improvements
17. Repository structure
18. Reproducibility instructions
19. Author information

The README should reflect the actual completed project.

Do not write final performance claims before experiments are complete.

---

# 15. `.gitignore`

A proper `.gitignore` must be created early.

It should generally exclude:

```text
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environments
.venv/
venv/
env/

# Environment variables / secrets
.env
.env.*
!.env.example

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Local data
data/raw/*
data/processed/*

# Generated model artifacts
models/*.joblib
models/*.pkl
models/*.pickle

# Temporary outputs
*.tmp
*.log

# Local caches
.cache/
.pytest_cache/
.mypy_cache/
```

The exact `.gitignore` must be adapted to the actual project.

Do not blindly ignore files that are required to reproduce or run the application.

---

# 16. `.env` and Secrets

Never commit:

```text
.env
```

Never place secrets directly into source code.

Never commit:

* API keys
* Passwords
* Tokens
* Private URLs
* Service credentials

If configuration is required, provide:

```text
.env.example
```

containing placeholders only.

Example:

```text
API_KEY=your_api_key_here
```

Never use real credentials in the example file.

---

# 17. Branching Strategy

Because this is a small capstone project with a very short deadline, use a simple branching strategy.

Recommended:

```text
main
  │
  ├── feature/data-pipeline
  ├── feature/modeling
  ├── feature/evaluation
  ├── feature/dashboard
  └── fix/...
```

Do not create an unnecessarily complicated GitFlow structure.

---

# 18. `main` Branch

`main` represents the stable version of the project.

The `main` branch should contain code that is:

* Functional
* Tested to a reasonable degree
* Documented
* Reviewable
* Not known to be severely broken

Avoid committing experimental broken code directly to `main`.

---

# 19. Feature Branches

Use feature branches for meaningful development units.

Examples:

```text
feature/data-pipeline
feature/eda
feature/baseline-model
feature/model-comparison
feature/explainability
feature/streamlit-dashboard
feature/testing
```

For small changes, a feature branch may not be necessary if the workflow becomes unnecessarily slow.

The goal is traceability, not bureaucracy.

---

# 20. Commit Strategy

Commits should represent meaningful development steps.

Good examples:

```text
feat: add dataset loading and validation
feat: implement preprocessing pipeline
feat: add churn baseline with logistic regression
feat: add tree-based model comparison
feat: implement probability calibration
feat: add customer risk ranking
feat: add model explainability
feat: add Streamlit prediction dashboard
test: add preprocessing validation tests
docs: document dataset source and assumptions
docs: update model comparison results
fix: handle missing categorical values
fix: prevent preprocessing leakage
```

Avoid meaningless commits such as:

```text
update
changes
final
done
new
test
working
final final
```

---

# 21. Conventional Commit Style

Where practical, use:

```text
<type>: <short description>
```

Recommended types:

### `feat`

New functionality.

```text
feat: add churn prediction pipeline
```

### `fix`

Bug correction.

```text
fix: correct categorical preprocessing
```

### `docs`

Documentation.

```text
docs: add reproducibility instructions
```

### `test`

Tests.

```text
test: add model inference tests
```

### `refactor`

Code restructuring without changing intended behavior.

```text
refactor: separate training and evaluation modules
```

### `chore`

Maintenance.

```text
chore: update project dependencies
```

### `experiment`

Use only if useful for clearly identifying experimental work.

```text
experiment: compare class-weight strategies
```

---

# 22. Commit Quality Rule

A commit should ideally answer:

> "What meaningful change happened here?"

Avoid combining unrelated changes.

Prefer:

```text
feat: add preprocessing pipeline
docs: document preprocessing decisions
```

over:

```text
update everything
```

---

# 23. Commit Frequency

Do not attempt to produce an artificially large number of commits.

Do not deliberately create fake history.

The repository should have a natural development history reflecting actual work.

A small number of meaningful commits is better than dozens of meaningless ones.

---

# 24. Pull Requests

For a solo project, pull requests are optional.

They may be used for major milestones if helpful.

Potential PRs:

```text
PR #1 — Establish project structure
PR #2 — Add data pipeline and EDA
PR #3 — Add baseline and candidate models
PR #4 — Add evaluation and explainability
PR #5 — Add application and final documentation
```

Do not create pull requests merely for appearance.

---

# 25. Experiment Tracking

Model experiments should be recorded separately from ordinary Git commits.

Git records code changes.

Experiment tracking records ML results.

For each significant experiment, record:

```text
Experiment ID
Date
Dataset version
Features
Model
Hyperparameters
Validation strategy
Metrics
Observations
Decision
```

Example:

```text
EXP-003
Model: Random Forest
Features: Engineered customer behavior features
CV: Stratified 5-fold
ROC-AUC: [actual result]
F1: [actual result]
Observation: [actual observation]
Decision: [actual decision]
```

No placeholder or fabricated metrics may remain in the final report.

---

# 26. Dataset Versioning

If the dataset changes, record:

* Source
* Version/date if available
* File name
* Row count
* Column count
* Important preprocessing changes

If the dataset is externally hosted and cannot be versioned directly, document the exact source and retrieval information.

Do not assume that an external dataset will remain unchanged forever.

---

# 27. Reproducibility Strategy

The repository should allow another developer to understand:

```text
Dataset
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

The following should be documented:

* Python version
* Dependencies
* Dataset source
* Dataset preparation
* Random seeds
* Training command
* Evaluation command
* Application launch command
* Expected outputs

---

# 28. Requirements Management

Maintain:

```text
requirements.txt
```

Dependencies should be based on actual imports and actual project needs.

Do not add libraries merely because they might be useful.

After the implementation stabilizes:

* Remove unused dependencies.
* Verify installation.
* Test from a clean environment where practical.

---

# 29. Python Environment

Recommended local setup:

```text
python -m venv .venv
```

Activate the environment and install:

```text
pip install -r requirements.txt
```

The exact commands should be documented according to the actual development environment.

---

# 30. Git Tags and Releases

Once the project reaches meaningful milestones, tags may be used.

Example:

```text
v0.1.0
```

Initial functional version.

```text
v0.5.0
```

Feature-complete development version.

```text
v1.0.0
```

Final internship submission version.

The final `v1.0.0` tag must correspond to the actual reviewed final state.

Do not create releases solely for appearance.

---

# 31. Final Release Criteria

Before creating `v1.0.0`, verify:

### Code

* [ ] Application works
* [ ] Training pipeline works
* [ ] Inference works
* [ ] Tests/checks pass
* [ ] No known critical bugs

### ML

* [ ] Final model is documented
* [ ] Metrics are verified
* [ ] Test set was not improperly reused
* [ ] No leakage detected
* [ ] Model limitations documented

### Documentation

* [ ] README complete
* [ ] Setup tested
* [ ] Dataset source documented
* [ ] Results verified
* [ ] Screenshots updated
* [ ] Project structure accurate

### Repository

* [ ] `.gitignore` correct
* [ ] No secrets
* [ ] No private data
* [ ] No unnecessary generated files
* [ ] Commit history understandable
* [ ] Repository is clean

---

# 32. GitHub Repository Presentation

The repository landing page should immediately communicate:

```text
Customer Churn Prediction
        ↓
What problem does it solve?
        ↓
How does it work?
        ↓
What ML methods were used?
        ↓
What were the actual results?
        ↓
How can it be reproduced?
```

The repository should contain a concise project description.

Where appropriate, add:

* Topics
* License
* Documentation
* Screenshots
* Architecture diagram
* Results
* Demo instructions

Do not overload the repository with decorative badges.

---

# 33. GitHub Topics

Relevant topics may include:

```text
machine-learning
customer-churn
classification
python
scikit-learn
data-science
predictive-analytics
streamlit
```

Only use topics that accurately describe the actual project.

---

# 34. Screenshots

If a Streamlit application is created, include selected screenshots in the README.

Screenshots should demonstrate meaningful functionality such as:

* Dashboard
* Customer prediction
* Risk ranking
* Model insights

Avoid excessive screenshots.

Do not include:

* Personal information
* API keys
* Local machine paths
* Sensitive data
* Debug logs

---

# 35. Architecture Diagram

The repository should eventually contain a simple architecture/pipeline diagram if useful.

Example:

```text
Dataset
   ↓
Validation
   ↓
Preprocessing
   ↓
Feature Engineering
   ↓
Model
   ↓
Evaluation
   ↓
Risk Prediction
   ↓
Application
```

The diagram should reflect the actual implementation.

---

# 36. Documentation Synchronization

Whenever an important technical decision changes, update the relevant documentation.

Examples:

If the final model changes:

```text
ML_REQUIREMENTS.md
EXPERIMENT_PLAN.md
README.md
```

may need updating.

If the project architecture changes:

```text
ARCHITECTURE.md
README.md
```

may need updating.

If repository organization changes:

```text
GIT_GITHUB_STRATEGY.md
README.md
```

may need updating.

Documentation must never intentionally describe an implementation that no longer exists.

---

# 37. AI Implementation Assistant Git Rules

Google AI Studio may generate or modify code, but Git history must remain truthful.

AI Studio must:

1. Follow this Git/GitHub strategy.
2. Never fabricate commit history.
3. Never fabricate experiment history.
4. Never claim that a commit was made if it was not.
5. Never claim tests passed unless they actually ran.
6. Never claim a model was trained unless training actually occurred.
7. Never fabricate GitHub URLs.
8. Never create fake contributor identities.
9. Never add fake authors to source files.
10. Never alter Git history merely to make development appear more sophisticated.
11. Preserve meaningful existing commits.
12. Avoid destructive Git operations unless explicitly requested.
13. Never delete project history without explicit authorization.
14. Never commit secrets.
15. Never commit sensitive datasets.
16. Keep generated files out of Git when they are unnecessary.

---

# 38. AI Studio Attribution and Repository Presentation

The project should not contain unnecessary platform-specific branding or statements suggesting that the repository itself was produced by Google AI Studio.

Do not add statements such as:

```text
Generated by Google AI Studio
Built by Gemini
Created with Google AI Studio
AI-generated project
AI-assisted project
Powered by Google AI Studio
```

to the README, source code, UI, project title, documentation, screenshots, or repository description unless such disclosure is required by an applicable platform policy, license, API requirement, or other legitimate requirement.

This rule does NOT authorize:

* False claims
* Fabricated authorship
* Fabricated research
* Fabricated experiments
* Fabricated contributions
* Misrepresentation of results

The final repository should accurately represent the user's project and understanding.

---

# 39. Generated Files Policy

Do not commit temporary/generated files unless they are required.

Avoid committing:

```text
__pycache__/
.ipynb_checkpoints/
temporary CSV exports
debug logs
local cache files
temporary screenshots
unused model files
IDE configuration
```

Generated reports should only be committed when they provide meaningful value to the project.

---

# 40. Large Files

Do not commit large datasets or model files simply because Git allows it.

If a large file is necessary, evaluate:

* Git LFS
* External artifact storage
* Dataset download instructions
* Reproducible generation

The simplest reliable solution should be preferred.

---

# 41. License

A license should only be added when its implications are understood and appropriate for the project.

If using an external dataset or code under a particular license, preserve and respect its licensing requirements.

Do not copy a license from another repository without understanding whether it applies.

---

# 42. Final Repository Audit

Before submission, perform a complete repository audit.

## Security

* [ ] No API keys
* [ ] No passwords
* [ ] No access tokens
* [ ] No `.env`
* [ ] No private credentials
* [ ] No sensitive customer information

## Code

* [ ] No unnecessary files
* [ ] No debug code
* [ ] No dead code where reasonably identifiable
* [ ] No machine-specific absolute paths
* [ ] Imports are clean
* [ ] Dependencies are documented

## ML

* [ ] Results are real
* [ ] Metrics are reproducible
* [ ] Dataset source is documented
* [ ] No leakage
* [ ] Model selection is explained

## Documentation

* [ ] README matches implementation
* [ ] Setup instructions work
* [ ] Architecture matches implementation
* [ ] Results match experiments
* [ ] Screenshots match current application
* [ ] Limitations are documented

## Git

* [ ] Meaningful commit history
* [ ] No accidental secrets
* [ ] No unnecessary branches
* [ ] Main branch is stable
* [ ] Final commit represents the submitted version

---

# 43. Final Submission Structure

The final GitHub repository should make it possible for a reviewer to follow this path:

```text
GitHub Repository
       ↓
README
       ↓
Problem Understanding
       ↓
Dataset
       ↓
Methodology
       ↓
Code
       ↓
Experiments
       ↓
Results
       ↓
Application
       ↓
Reproducibility
       ↓
Technical Conclusions
```

A reviewer should not have to search through dozens of files to understand the project.

---

# 44. Definition of Git/GitHub Done

This strategy is considered successfully implemented when:

* [ ] Repository created
* [ ] Repository has professional name
* [ ] `.gitignore` created
* [ ] Directory structure finalized
* [ ] Documentation organized
* [ ] Dataset handling documented
* [ ] Secrets protected
* [ ] Meaningful Git commits used
* [ ] Branching kept simple
* [ ] Experiment history recorded
* [ ] README completed
* [ ] Repository tested from a clean setup where practical
* [ ] Final results verified
* [ ] Repository audited
* [ ] Final `main` branch is stable
* [ ] Optional `v1.0.0` release/tag created
* [ ] GitHub repository is portfolio-ready

---

# 45. Guiding Principle

Git and GitHub should document the **real development process**, not manufacture a more impressive-looking history.

The repository should communicate:

> **What was built → Why it was built → How it was built → How it was evaluated → What actually worked → What its limitations are.**

A clean and truthful repository with meaningful commits is more valuable than an artificially complicated Git history.

The final repository should be something the author can confidently walk through during an internship evaluation or technical interview.

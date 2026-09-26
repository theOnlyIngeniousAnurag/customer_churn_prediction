# Resume Bullets — Customer Churn Prediction System

The following resume bullet points provide technically accurate, metric-grounded descriptions of the project suitable for resumes, CVs, and professional portfolios. All metrics and achievements correspond strictly to verified project artifacts.

---

## Version A — ATS-Optimized (2–3 Bullets)

* **Developed an end-to-end Machine Learning customer churn prediction system** in Python using `scikit-learn`, implementing leakage-safe target isolation, median imputation for missing charges, and one-hot categorical encoding across 7,043 customer accounts.
* **Tuned an ensemble Random Forest classifier** (`300 trees`, `max_depth=8`, `random_state=42`) using 5-fold cross-validation (`CV PR-AUC 0.6643`), achieving **ROC-AUC 0.8429** and **PR-AUC 0.6562** on a locked 1,409-record holdout test set with a well-calibrated Brier Score of **0.1362**.
* **Engineered a full-stack decision-support analytics dashboard** using React 19, Express, and Tailwind CSS to rank portfolio risk across 4 operational probability tiers, display evidence-based review reasons, and present global feature importances.

---

## Version B — Technical / Engineering Focused (3 Bullets)

* **Architected a leakage-free ML training and evaluation pipeline** in Python (`pandas`, `numpy`, `scikit-learn`), strictly isolating an 80/20 stratified train/test split (`5,634` train / `1,409` test) and fitting numerical scaling and categorical encoders exclusively on training data.
* **Benchmarked baseline and ensemble models** (Logistic Regression, Decision Trees, Random Forests), selecting an optimized Random Forest (`PR-AUC 0.6562`, `Precision 0.6866`, `Recall 0.4920`) and auditing model calibration using Brier score (`0.1362`) and 10-bin probability histograms.
* **Constructed an Express API and React 19 analytics web application** serving portfolio risk categorizations (`7,043` scored records), top feature importances (`tenure` 20.21%, `TotalCharges` 14.35%), holdout confusion matrices, and interactive customer profile drawers backed by 64 automated unit tests.

---

## Version C — One-Line Project Entries (Compact Resume Layout)

* **ML Customer Churn Intelligence System (Python, scikit-learn, React, Express):** Built a leakage-safe Random Forest churn prediction pipeline achieving ROC-AUC 0.8429 on a locked test set, deployed alongside an Express API and React decision-support dashboard for portfolio risk ranking.
* **Customer Churn & Risk Analytics Pipeline (Python, React 19, Tailwind CSS):** Designed an end-to-end churn risk scoring system (`7,043` accounts) using tuned Random Forest ensembles (`PR-AUC 0.6562`, Brier score `0.1362`) with evidence-based customer review reasons and full-stack web analytics.

---

## Metric Reference Table for Resume Customization

| Metric / Dimension | Verified Value | Context |
| :--- | :--- | :--- |
| **Dataset Size** | `7,043` accounts | Cross-sectional Telco Customer Churn dataset |
| **Train / Test Partition** | `5,634` / `1,409` | Stratified 80/20 split (`random_state=42`) |
| **Selected Model** | `RandomForestClassifier` | `n_estimators=300`, `max_depth=8`, `max_features="sqrt"` |
| **Locked Holdout ROC-AUC** | **0.8429** | Final Phase 7 evaluation |
| **Locked Holdout PR-AUC** | **0.6562** | Final Phase 7 evaluation |
| **Locked Holdout Brier Score** | **0.1362** | Probability calibration assessment |
| **Holdout Confusion Matrix** | `951 TN`, `84 FP`, `190 FN`, `184 TP` | Default threshold `0.50` |
| **Portfolio High/Very High Risk** | `1,362` accounts (19.34%) | `High` (934) + `Very High` (428) risk bands |
| **Automated Test Suite** | 64 passing Python tests | `pytest` test suite coverage |

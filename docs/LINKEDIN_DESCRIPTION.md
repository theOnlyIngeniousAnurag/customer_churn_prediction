# LinkedIn Descriptions — Customer Churn Prediction & Retention Analytics

The following descriptions provide professional, factually grounded summaries of the project suitable for LinkedIn project sections, featured posts, or portfolio entries.

---

## Short Version (2–3 Sentences)

I built an end-to-end Customer Churn Prediction and Retention Analytics System using Python, scikit-learn, React 19, and Express. The project implements a leakage-safe Machine Learning pipeline featuring hyperparameter-tuned Random Forest ensembles (`ROC-AUC 0.8429`, `PR-AUC 0.6562` on a locked holdout set) paired with an interactive decision-support dashboard for portfolio risk ranking and customer profile inspection.

---

## Standard Version (Paragraph Layout)

**Project Highlight: Churn Intelligence — Customer Risk & Retention Analytics**

I developed an end-to-end Machine Learning decision-support platform designed to estimate customer churn probability, explain risk factors, and assist account managers in identifying high-risk subscriptions.

**Key Technical Highlights:**
* **Leakage-Safe Data Pipeline:** Preprocessed 7,043 customer records with strict 80/20 stratified partitioning, fitting imputation and one-hot encoding exclusively on training data to prevent target leakage.
* **Model Benchmarking & Tuning:** Benchmarked Logistic Regression, Decision Tree, and Random Forest architectures using 5-fold cross-validation. Selected an optimized Random Forest (`300 trees`, `max_depth=8`), achieving `ROC-AUC 0.8429`, `PR-AUC 0.6562`, and a well-calibrated Brier Score of `0.1362` on a locked holdout test set (`1,409` records).
* **Explainability & Risk Ranking:** Categorized 7,043 portfolio accounts into 4 operational risk bands (`Low`, `Medium`, `High`, `Very High`) and extracted global feature importances (`tenure` 20.21%, `TotalCharges` 14.35%, `MonthlyCharges` 9.15%).
* **Decision-Support Web App:** Built a dark-first analytics application using React 19, Express, and Tailwind CSS v4, featuring executive portfolio summaries, searchable customer tables, slide-over profile drawers with evidence-based review reasons, and model diagnostic views.
* **Quality Assurance:** Validated pipeline determinism and resilience through 64 automated Python unit tests (`pytest`), TypeScript linting, and clean build verification.

---

## Project Post / Article Format (Social Media / Portfolio Post)

🚀 **New Portfolio Project: Churn Intelligence — Customer Churn Prediction & Retention Analytics**

Retaining existing customers is one of the most critical drivers of unit economics for subscription businesses. I recently completed an end-to-end Machine Learning project that transforms raw customer usage and billing data into actionable, explainable risk intelligence.

Here's how I built it:

📊 **1. Data Strategy & Leakage Isolation**
* Analyzed 7,043 customer accounts across 21 numerical and categorical attributes.
* Implemented a strict 80/20 stratified train/test split (`5,634` train / `1,409` test) with `random_state=42`.
* Ensured zero target leakage by fitting numerical median imputation and categorical one-hot encoders strictly on training data.

🔬 **2. Model Development & Evaluation**
* Benchmarked Logistic Regression baselines against Decision Tree and Random Forest classifiers.
* Hyperparameter-tuned the Random Forest using 5-fold cross-validation (`CV PR-AUC 0.6643`).
* Evaluated the selected candidate on the locked holdout test set:
  * **ROC-AUC:** 0.8429
  * **PR-AUC:** 0.6562
  * **Precision:** 0.6866 | **Recall:** 0.4920 | **F1:** 0.5732
  * **Brier Score:** 0.1362 (indicating strong probability calibration)

💡 **3. Explainability & Risk Scoring**
* Scored the entire 7,043 customer portfolio into 4 operational risk bands (`Low < 0.30`, `Medium 0.30–0.49`, `High 0.50–0.69`, `Very High >= 0.70`), identifying 1,362 accounts (19.34%) in High or Very High risk categories.
* Derived global feature importances, identifying customer tenure (20.21%), total charges (14.35%), monthly charges (9.15%), and fiber optic internet service (9.13%) as primary predictive features.
* Generated evidence-based customer review reasons to help team members understand specific risk indicators per profile.

💻 **4. Decision-Support Web Application**
* Engineered a full-stack dashboard with React 19, Express, Vite, and Tailwind CSS v4.
* Features 4 primary views: Executive Overview, Searchable Customer Explorer, Risk Distribution Analysis, and Model Insights.
* Verified through 64 passing unit tests in Python (`pytest`) and clean TypeScript linting.

Check out the repository for complete code, experiment logs, and setup instructions!

#MachineLearning #DataScience #Python #ScikitLearn #React #WebDevelopment #Analytics #PortfolioProject

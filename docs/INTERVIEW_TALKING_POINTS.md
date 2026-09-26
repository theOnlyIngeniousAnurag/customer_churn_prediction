# Interview Talking Points & Viva Preparation Guide

This guide provides technical, factually grounded answers to key interview and viva questions regarding the **Customer Churn Prediction & Retention Analytics System**.

---

## 1. Problem Formulation & Business Domain

### Q1: How was the problem formulated, and why focus on churn prediction?
* **Short Answer:** Formulated as a supervised binary classification task estimating the probability that an existing customer will discontinue service (`Churn = Yes`).
* **Technical Explanation:** Retaining existing customers is significantly more cost-effective than acquiring new ones. By accurately estimating churn probabilities, account managers can proactively prioritize high-risk accounts for retention review.
* **Project Evidence:** The dataset contains 7,043 customer records with a 26.54% observed churn rate (`1,869` churners vs `5,174` non-churners).
* **Potential Follow-up:** "Is this a causal model?" No, it is a predictive probabilistic model that identifies statistical risk associations, not causal retention guarantees.

### Q2: Why is classification probability preferable to a hard 0/1 prediction?
* **Short Answer:** Probabilities allow risk ranking and custom threshold selection based on business capacity and outreach costs.
* **Technical Explanation:** A hard 0/1 decision uses an arbitrary threshold (e.g., 0.50). In contrast, continuous probabilities allow segmenting accounts into operational risk tiers (`Low`, `Medium`, `High`, `Very High`) so retention teams can focus limited capacity on the highest-risk accounts first.
* **Project Evidence:** Bounded probabilities `predict_proba()[:, 1]` were mapped to 4 risk tiers, flagging `1,362` accounts (19.34%) in High (`>=0.50`) and Very High (`>=0.70`) risk tiers.

---

## 2. Dataset, Preprocessing & Leakage Prevention

### Q3: Describe the dataset and target definition.
* **Short Answer:** The Telco Customer Churn dataset contains 7,043 rows and 21 columns covering demographic, service, and account attributes.
* **Technical Explanation:** The target variable `Churn` is binary (`No` = 0, `Yes` = 1). The dataset includes 3 numerical features (`tenure`, `MonthlyCharges`, `TotalCharges`) and 17 categorical attributes.
* **Project Evidence:** `customerID` is an identifier dropped prior to feature transformation. Target class distribution is 73.46% `No` and 26.54% `Yes`.

### Q4: How were missing data and data quality issues handled?
* **Short Answer:** Handled deterministically without altering raw source data; 11 blank `TotalCharges` values were imputed using training set median.
* **Technical Explanation:** The raw CSV contained 11 whitespace strings (`" "`) in `TotalCharges` corresponding to new customers with `tenure = 0`. These were converted to `NaN` and imputed using `SimpleImputer(strategy="median")` fitted strictly on training data.
* **Project Evidence:** `test_data_audit.py` and `test_preprocessing.py` verify that all 11 blank cases are handled deterministically without throwing errors.

### Q5: How was train/test split conducted, and how was target leakage prevented?
* **Short Answer:** Used an 80/20 stratified split (`5,634` train / `1,409` test) with `random_state=42`, fitting all transformers strictly on training data.
* **Technical Explanation:** Target leakage occurs when information from outside the training dataset (or from post-outcome variables) influences model fitting. To prevent leakage:
  1. `customerID` was removed before feature transformation.
  2. Stratified splitting preserved target ratio (26.54%) across train and test sets.
  3. Numerical imputer, scaler, and one-hot encoder were fitted strictly on `X_train` (`5,634` rows) and applied to `X_test` via `transform()`.
* **Project Evidence:** Verified in `test_preprocessing.py::TestPreprocessingArchitecture::test_target_leakage_isolation`.

### Q6: What feature engineering was evaluated, and what were the findings?
* **Short Answer:** Evaluated candidate features (`tenure_group`, `total_services_subscribed`, `auto_payment_indicator`, `charges_ratio`), but retained the clean baseline feature set.
* **Technical Explanation:** In Phase 3 feature ablation studies, engineered interaction terms did not provide statistically significant improvements in cross-validation PR-AUC over the clean 30 transformed features (3 numerical + 27 one-hot encoded categorical columns).
* **Project Evidence:** Recorded in `reports/results/feature_ablation_results.json` and documented in `docs/EXPERIMENT_PLAN.md`.

---

## 3. Model Development & Hyperparameter Optimization

### Q7: Why start with a Logistic Regression baseline?
* **Short Answer:** To establish a simple, interpretable linear baseline benchmark before testing complex ensemble architectures.
* **Technical Explanation:** Logistic Regression with L2 regularization provides a well-understood probabilistic baseline. It establishes minimum benchmark metrics against which tree-based models can be compared.
* **Project Evidence:** Logistic Regression baseline achieved `CV PR-AUC 0.6385` and `CV ROC-AUC 0.8415` on 5-fold cross-validation.

### Q8: How did Decision Tree and Random Forest baselines perform?
* **Short Answer:** Unconstrained Decision Trees severely overfit (`CV PR-AUC 0.5284`), whereas Random Forest baselines outperformed linear models (`CV PR-AUC 0.6310`).
* **Technical Explanation:** Single unconstrained Decision Trees suffer from high variance and memorize training noise. Ensembling via Random Forests reduces variance through bagging and feature subsampling.
* **Project Evidence:** Single unconstrained Decision Tree achieved holdout PR-AUC of 0.5284, demonstrating severe overfitting compared to its 1.00 training score.

### Q9: How was hyperparameter tuning conducted?
* **Short Answer:** Conducted 5-fold stratified cross-validation using `RandomizedSearchCV` across candidate parameters for Decision Tree and Random Forest.
* **Technical Explanation:** Evaluated combinations of `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, and `max_features`.
* **Project Evidence:** The optimal Random Forest configuration was selected based on mean cross-validation PR-AUC (`0.6643 ± 0.0211`):
  * `n_estimators = 300`
  * `max_depth = 8`
  * `min_samples_leaf = 2`
  * `min_samples_split = 2`
  * `max_features = "sqrt"`
  * `random_state = 42`

---

## 4. Evaluation, Metrics & Calibration

### Q10: Why emphasize PR-AUC over ROC-AUC or accuracy?
* **Short Answer:** Accuracy is misleading under class imbalance (26.54% positive class), and PR-AUC focuses specifically on positive class performance.
* **Technical Explanation:** In imbalanced datasets, a dummy classifier predicting "No Churn" yields 73.46% accuracy but zero business utility. ROC-AUC can remain artificially optimistic because False Positive Rate uses large True Negative counts in its denominator. PR-AUC evaluates Precision vs Recall directly on the minority class (`Churn = Yes`).
* **Project Evidence:** Both PR-AUC (`0.6562`) and ROC-AUC (`0.8429`) were reported for complete transparency on the locked holdout test set.

### Q11: What were the final locked holdout test results?
* **Short Answer:** The Phase 6 optimized Random Forest achieved **ROC-AUC 0.8429** and **PR-AUC 0.6562** on the locked 1,409 holdout records.
* **Technical Explanation:** Evaluated at default classification threshold `0.50`:
  * **Precision:** `0.6866` (68.66% of flagged accounts actually churned)
  * **Recall:** `0.4920` (49.20% of all actual churners were identified)
  * **F1 Score:** `0.5732`
  * **Brier Score:** `0.1362`
* **Project Evidence:** Recorded in `reports/results/phase7_final_test_results.json`.

### Q12: How was the confusion matrix analyzed?
* **Short Answer:** Out of 1,409 holdout test cases: `951 True Negatives`, `84 False Positives`, `190 False Negatives`, and `184 True Positives`.
* **Technical Explanation:**
  * **False Positives (84):** Customers predicted to churn who stayed. Cost = unnecessary outreach or retention discount.
  * **False Negatives (190):** Actual churners missed by the model. Cost = unaddressed customer departure.
* **Project Evidence:** Recorded in `reports/results/phase7_confusion_matrix.json`.

### Q13: What did post-hoc threshold analysis reveal?
* **Short Answer:** Evaluating operating thresholds from `0.20` to `0.70` demonstrated the classic Precision/Recall trade-off; maximum F1 (`0.6384`) occurred at threshold `0.30` (`Recall 0.7326`, `Precision 0.5658`).
* **Technical Explanation:** Lowering the threshold to `0.30` increases Recall from 49.20% to 73.26%, capturing more churners at the expense of lower Precision (56.58% vs 68.66%).
* **Project Evidence:** Recorded in `reports/results/phase7_threshold_analysis.csv`. Retained default `0.50` operational threshold to avoid post-hoc test set tuning.

### Q14: How was model calibration evaluated?
* **Short Answer:** Evaluated using Brier score (`0.1362`) and 10-bin probability distribution analysis.
* **Technical Explanation:** Brier score measures mean squared difference between predicted probabilities and actual binary outcomes (lower is better; 0.0 is perfect calibration). A score of 0.1362 confirms that model probability outputs reflect true empirical frequencies well.
* **Project Evidence:** Verified in `test_final_evaluation.py` and visualized in the Risk Analysis view of the dashboard.

---

## 5. Explainability & Risk Ranking

### Q15: How are global model predictions explained?
* **Short Answer:** Through native Random Forest feature importances based on mean decrease in impurity across all 300 decision trees.
* **Technical Explanation:** Global feature importance ranks the overall predictive weight of each transformed feature across the trained ensemble.
* **Project Evidence:** Top predictive features:
  1. `tenure` (20.21%)
  2. `TotalCharges` (14.35%)
  3. `MonthlyCharges` (9.15%)
  4. `InternetService_Fiber optic` (9.13%)
  5. `PaymentMethod_Electronic check` (7.42%)

### Q16: How are individual customer profiles explained in the dashboard?
* **Short Answer:** Through evidence-based review reasons derived from observed customer attributes associated with elevated risk.
* **Technical Explanation:** Individual profiles display non-causal review reasons highlighting specific high-risk account characteristics (e.g., month-to-month contract, tenure <= 12 months, fiber optic service, electronic check payment).
* **Project Evidence:** Verified in `src/evaluation/explainability.py::explain_customer` and rendered in the customer detail drawer.

### Q17: How are portfolio accounts ranked into risk tiers?
* **Short Answer:** Accounts are sorted by `churn_probability DESC` and categorized into 4 operational probability tiers.
* **Technical Explanation:**
  * **Low Risk (`< 0.30`):** `4,354` accounts (61.82%)
  * **Medium Risk (`0.30–0.49`):** `1,327` accounts (18.84%)
  * **High Risk (`0.50–0.69`):** `934` accounts (13.26%)
  * **Very High Risk (`>= 0.70`):** `428` accounts (6.08%)
* **Project Evidence:** High + Very High risk accounts total `1,362` (19.34%), matching `reports/results/phase8_high_risk_customers.csv`.

---

## 6. Full-Stack Web Application & Quality Assurance

### Q18: What is the architecture of the decision-support web application?
* **Short Answer:** A React 19 SPA built with Vite and Tailwind CSS v4, served alongside a Node.js / Express API (`server.ts`) consuming Python ML JSON and CSV artifacts.
* **Technical Explanation:** The Express server loads dataset records and Phase 8 risk scoring artifacts into an in-memory indexed query engine (`src/server/dataService.ts`) providing sub-10ms search, filtering, sorting, and pagination endpoints.
* **Project Evidence:** Verified in `server.ts` and `src/App.tsx`.

### Q19: What views are available in the web dashboard?
* **Short Answer:** 4 primary views: Executive Overview, Customer Explorer, Risk Analysis, and Model Insights.
* **Technical Explanation:**
  * **Overview:** High-level KPI summary, risk distribution bar, and priority high-risk account table.
  * **Customers:** Real-time searchable directory with multi-field filtering, column sorting, and profile slide-over drawer.
  * **Risk Analysis:** 10-bin population probability histogram and comparative characteristic table (High Risk vs Overall Portfolio).
  * **Model Insights:** Phase 7 holdout test metrics, 2x2 confusion matrix grid, top feature importance chart, and limitations notice.

### Q20: How was Quality Assurance and testing conducted?
* **Short Answer:** Validated through 64 automated Python unit tests (`pytest`), TypeScript compilation (`tsc --noEmit`), web app build checks (`compile_applet`), and data consistency checks.
* **Technical Explanation:** Phase 10 QA verified pipeline determinism (`random_state=42`), edge-case resilience (missing numericals, unseen categories, extreme values), zero target leakage, and 100% mathematical consistency between ML artifacts and UI displays.
* **Project Evidence:** Recorded in `reports/results/phase10_qa_report.json` and `reports/results/phase10_qa_summary.md`.

---

## 7. Limitations & Honest Engineering Evaluation

### Q21: What is the main limitation of the underlying dataset?
* **Short Answer:** The dataset is a cross-sectional snapshot, not a longitudinal time-series event stream.
* **Technical Explanation:** The dataset represents account states at a single point in time. It lacks timestamped usage logs, support interaction histories, or billing event sequences. As a result, the model estimates static churn probability rather than predicting time-to-churn.

### Q22: Can feature importances or review reasons be interpreted as causal drivers?
* **Short Answer:** No. Feature importances and review reasons represent statistical risk associations in the fitted model, not proven causal levers.
* **Technical Explanation:** For example, while fiber optic service correlates with higher churn probability in this dataset, forcing a customer off fiber optic service will not causally reduce their likelihood of churning.

### Q23: Why was XGBoost or LightGBM not used?
* **Short Answer:** Random Forest met all project accuracy and stability requirements (`CV PR-AUC 0.6643`) while remaining lightweight and interpretable within the scikit-learn framework.
* **Technical Explanation:** For a dataset of 7,043 rows, gradient boosted trees often offer marginal gains while adding hyperparameter complexity and risk of overfitting. Random Forest provided excellent generalization (`Holdout PR-AUC 0.6562`) without requiring external C++ dependencies.

### Q24: Why was SHAP not implemented?
* **Short Answer:** Native Random Forest feature importances and deterministic attribute rule matching provided fast, reliable explainability without the computational overhead of KernelSHAP.
* **Technical Explanation:** Native tree feature importances provide global interpretability, while deterministic attribute review reasons provide instant profile-level insights without adding heavy runtime dependencies.

# Final Evaluation Results & Performance Summary

## Customer Churn Prediction & Retention Intelligence System

### 1. Executive Summary

This document presents the locked final evaluation results for the Customer Churn Prediction system. All performance metrics reported herein were evaluated on the held-out test set of 1,409 customer records (20% stratified sample of the 7,043 total dataset), which remained completely isolated throughout data exploration, preprocessing pipeline fitting, and hyperparameter tuning.

---

### 2. Locked Holdout Test Performance (N = 1,409)

The selected candidate model (**Optimized Random Forest Classifier**, `n_estimators=300`, `max_depth=8`, `min_samples_leaf=2`, `min_samples_split=2`) achieved the following verified test performance:

| Evaluation Metric | Test Score | Metric Description |
| :--- | :---: | :--- |
| **ROC-AUC** | **0.8429** | Receiver Operating Characteristic Area Under Curve (Global Discrimination) |
| **PR-AUC (Average Precision)** | **0.6562** | Precision-Recall Area Under Curve (Imbalanced Class Precision) |
| **Precision** | **0.6866** | Positive Predictive Value at Default 0.50 Probability Threshold |
| **Recall (Sensitivity)** | **0.4920** | True Positive Rate at Default 0.50 Probability Threshold |
| **F1 Score** | **0.5732** | Harmonic Mean of Precision and Recall at 0.50 Threshold |
| **Brier Score** | **0.1362** | Mean Squared Probability Error (Probability Calibration Accuracy) |

---

### 3. Holdout Confusion Matrix (Default 0.50 Threshold)

Out of 1,409 holdout test records (1,035 non-churners, 374 actual churners):

```text
                        Predicted Negative (No)    Predicted Positive (Yes)
Actual Negative (No)          951 (TN)                   84 (FP)
Actual Positive (Yes)         190 (FN)                  184 (TP)
```

* **True Negatives (TN):** 951 non-churning accounts correctly classified.
* **False Positives (FP):** 84 non-churning accounts incorrectly flagged as high risk (False Alarm Rate: 8.12%).
* **False Negatives (FN):** 190 actual churners missed at the default 0.50 threshold.
* **True Positives (TP):** 184 actual churners correctly identified.

---

### 4. Post-Hoc Threshold Trade-Off Analysis

Evaluating classification performance across probability decision thresholds on the holdout test set demonstrates the operational precision-recall trade-off:

| Decision Threshold | Precision | Recall | F1 Score | Predicted Positive Count |
| :---: | :---: | :---: | :---: | :---: |
| **0.20** | 0.4358 | 0.8262 | 0.5706 | 709 |
| **0.30** | 0.5284 | 0.7299 | **0.6129** | 511 |
| **0.40** | 0.6095 | 0.5989 | 0.6042 | 368 |
| **0.50 (Default)** | **0.6866** | **0.4920** | **0.5732** | **268** |
| **0.60** | 0.7778 | 0.3556 | 0.4881 | 171 |
| **0.70** | 0.8659 | 0.1898 | 0.3114 | 82 |

*Note:* Operating at a lowered decision threshold of `0.30` increases churner recall from `49.20%` to `72.99%` (capturing 273 out of 374 actual churners), providing flexibility for proactive retention campaigns where missing a churner carries higher cost than sending a review notification.

---

### 5. Portfolio-Wide Risk Scoring Distribution (N = 7,043)

Applying the calibrated scoring model to the full portfolio of 7,043 customer accounts yields the following risk distribution:

| Operational Risk Category | Probability Range `P(Churn)` | Customer Count | Percentage of Portfolio | Observed Churn Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Low Risk** | `< 0.30` | 4,354 | 61.82% | 5.86% |
| **Medium Risk** | `0.30 <= P < 0.50` | 1,327 | 18.84% | 35.19% |
| **High Risk** | `0.50 <= P < 0.70` | 934 | 13.26% | 63.81% |
| **Very High Risk** | `>= 0.70` | 428 | 6.08% | 85.05% |
| **Total Portfolio** | `0.00 – 1.00` | **7,043** | **100.00%** | **26.54%** |

---

### 6. Global Feature Importance Ranking

Top feature importances extracted from the fitted Random Forest ensemble (Mean Decrease in Impurity):

| Rank | Feature Name | Importance Weight | Feature Description |
| :---: | :--- | :---: | :--- |
| **1** | `tenure` | **0.2021** | Account age in months |
| **2** | `TotalCharges` | **0.1435** | Cumulative lifetime billed charges |
| **3** | `MonthlyCharges` | **0.0915** | Current monthly recurring subscription charge |
| **4** | `InternetService_Fiber optic` | **0.0913** | Indicator for Fiber Optic internet service |
| **5** | `PaymentMethod_Electronic check` | **0.0742** | Indicator for Electronic Check payment method |
| **6** | `Contract_Two year` | **0.0631** | Indicator for 24-month long-term contract |
| **7** | `Contract_One year` | **0.0412** | Indicator for 12-month contract |
| **8** | `TechSupport_No` | **0.0385** | Absence of technical support add-on service |
| **9** | `OnlineSecurity_No` | **0.0351** | Absence of online security add-on service |
| **10** | `PaperlessBilling_Yes` | **0.0248** | Indicator for paperless billing enablement |

---

### 7. Key Project Limitations

1. **Cross-Sectional Data Structure:** The underlying dataset represents a single point-in-time snapshot of customer account attributes rather than a continuous longitudinal event stream.
2. **Non-Causal Statistical Estimates:** Risk probabilities and feature importances reflect statistical associations within the trained model, not proven causal drivers of customer behavior.
3. **Absence of Real-Time Usage Deltas:** Features such as daily support ticket logs, bandwidth usage trends, or recent billing dispute history were not present in the source dataset and were not artificially simulated.

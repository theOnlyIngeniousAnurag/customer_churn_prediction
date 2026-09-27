# System Architecture

## Customer Churn Prediction & Retention Intelligence System

### 1. High-Level Architecture Overview

The system combines a scikit-learn machine learning pipeline with a Node.js/Express API service and a dark-first React 19 web application for customer risk ranking and retention decision support.

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           OFFLINE / ML PIPELINE (Python)                        │
│                                                                                 │
│  Raw Data (CSV) ──► Data Cleaning & Audit ──► Preprocessing & Scaling (30 Feat)  │
│                                                               │                 │
│                                                               ▼                 │
│  Explainability & Risk Ranking ◄── Holdout Evaluation ◄── Trained Random Forest │
│           │                                                                     │
└───────────┼─────────────────────────────────────────────────────────────────────┘
            │ Generates Authoritative JSON / CSV Artifacts
            ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ONLINE / APPLICATION LAYER (Node / React)              │
│                                                                                 │
│  Express API Server (server.ts / dataService.ts)                                │
│       ├── GET /api/stats (Portfolio Risk Overview)                              │
│       ├── GET /api/customers (Search, Multi-Field Filter, Sort, Paginate)       │
│       └── GET /api/model-insights (ROC-AUC, Confusion Matrix, Feature Import)   │
│                               │                                                 │
│                               ▼                                                 │
│  React 19 SPA (Vite + Tailwind CSS v4)                                          │
│       ├── Overview Dashboard View                                               │
│       ├── Customer Directory Explorer & Profile Inspection Drawer              │
│       ├── Population Risk Analysis Histogram                                    │
│       └── Model Insights & Validation Dashboard                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Machine Learning Pipeline Architecture

* **Data Ingestion & Cleaning (`src/preprocessing/`):** Custom `TotalChargesCleaner` addresses missing whitespace strings (`" "`) deterministically via median imputation.
* **Feature Transformer (`sklearn.compose.ColumnTransformer`):**
  * `StandardScaler` applied to numerical attributes (`tenure`, `MonthlyCharges`, `TotalCharges`).
  * `OneHotEncoder(handle_unknown='ignore', drop='first')` applied to categorical service, contract, and billing features.
* **Model Estimator (`RandomForestClassifier`):**
  * Configured with 300 decision trees, `max_depth=8`, `min_samples_leaf=2`, `min_samples_split=2`, `max_features='sqrt'`.
  * Generates calibrated churn probabilities `P(Churn = Yes)`.

---

### 3. Application Architecture

* **API Layer (`server.ts`, `src/server/dataService.ts`):** Express API server mounting Vite development middleware. Loads raw records and risk predictions into memory for fast real-time search, multi-field filtering, sorting, and pagination across all 7,043 records.
* **UI Layer (`src/App.tsx`, `src/components/`):**
  * **Overview View (`OverviewView.tsx`):** Executive risk summary, portfolio distribution metrics, high-risk account table.
  * **Customer Explorer (`CustomersView.tsx`):** Real-time ID search, multi-field filters (Risk, Contract, Internet, Payment Method), field sorting, pagination.
  * **Customer Profile Drawer (`CustomerDetailDrawer.tsx`):** Slide-over inspection drawer rendering risk probability meters, evidence-based review reasons, and organized customer attribute tabs.
  * **Risk Analysis View (`RiskAnalysisView.tsx`):** Population probability distribution histogram and comparative segment table (High Risk vs Portfolio).
  * **Model Insights View (`ModelInsightsView.tsx`):** Holdout test evaluation metrics (`ROC-AUC = 0.8429`, `PR-AUC = 0.6562`, `Brier = 0.1362`), confusion matrix, global Random Forest feature importances.

---

### 4. Data Storage & Artifact Contracts

The application communicates via structured JSON/CSV artifacts produced during pipeline execution:

* `data/raw/Telco-Customer-Churn.csv`: Raw 7,043 customer records.
* `reports/results/phase8_high_risk_customers.csv`: Scored customer risk probabilities, operational risk categories, and review reasons.
* `reports/results/phase7_final_test_results.json`: Locked holdout evaluation metrics and confusion matrix data.
* `reports/results/phase8_explainability_summary.json`: Global feature importances and portfolio risk band totals.

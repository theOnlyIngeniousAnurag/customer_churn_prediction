import fs from 'fs';
import path from 'path';

export interface CustomerRecord {
  rank: number;
  customerID: string;
  churn_probability: number;
  predicted_churn: boolean;
  risk_category: string;
  review_reasons: string[];
  // Raw fields
  gender: string;
  SeniorCitizen: number;
  Partner: string;
  Dependents: string;
  tenure: number;
  PhoneService: string;
  MultipleLines: string;
  InternetService: string;
  OnlineSecurity: string;
  OnlineBackup: string;
  DeviceProtection: string;
  TechSupport: string;
  StreamingTV: string;
  StreamingMovies: string;
  Contract: string;
  PaperlessBilling: string;
  PaymentMethod: string;
  MonthlyCharges: number;
  TotalCharges: number;
  Churn: string;
}

export interface OverviewData {
  total_customers_scored: number;
  observed_churn_rate: number;
  observed_churn_count: number;
  risk_category_counts: Record<string, number>;
  risk_category_percentages: Record<string, number>;
  high_risk_or_very_high_risk_count: number;
  high_risk_or_very_high_risk_pct: number;
  top_high_risk_customers: Array<{
    rank: number;
    customerID: string;
    risk_category: string;
    churn_probability: number;
    primary_reason: string;
    contract: string;
    tenure: number;
    monthly_charges: number;
  }>;
}

export interface CustomerQueryParams {
  search?: string;
  risk_category?: string;
  predicted_churn?: string;
  contract?: string;
  internet_service?: string;
  payment_method?: string;
  sort_by?: 'churn_probability' | 'tenure' | 'MonthlyCharges' | 'TotalCharges' | 'rank';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

class DataService {
  private customers: CustomerRecord[] = [];
  private customerMap: Map<string, CustomerRecord> = new Map();
  private explainabilitySummary: any = null;
  private finalTestResults: any = null;
  private errorAnalysis: any = null;
  private isLoaded = false;

  constructor() {
    this.loadData();
  }

  private loadData() {
    if (this.isLoaded) return;

    try {
      const rootDir = process.cwd();
      const rawCsvPath = path.join(rootDir, 'data', 'raw', 'Telco-Customer-Churn.csv');
      const rankedCsvPath = path.join(rootDir, 'reports', 'results', 'phase8_high_risk_customers.csv');
      const expSummaryPath = path.join(rootDir, 'reports', 'results', 'phase8_explainability_summary.json');
      const testResultsPath = path.join(rootDir, 'reports', 'results', 'phase7_final_test_results.json');
      const errorAnalysisPath = path.join(rootDir, 'reports', 'results', 'phase7_error_analysis.json');

      if (fs.existsSync(expSummaryPath)) {
        this.explainabilitySummary = JSON.parse(fs.readFileSync(expSummaryPath, 'utf8'));
      }
      if (fs.existsSync(testResultsPath)) {
        this.finalTestResults = JSON.parse(fs.readFileSync(testResultsPath, 'utf8'));
      }
      if (fs.existsSync(errorAnalysisPath)) {
        this.errorAnalysis = JSON.parse(fs.readFileSync(errorAnalysisPath, 'utf8'));
      }

      // Parse ranked CSV map first
      const rankedMap = new Map<string, {
        rank: number;
        prob: number;
        pred: boolean;
        category: string;
        reasons: string[];
      }>();

      if (fs.existsSync(rankedCsvPath)) {
        const rankedLines = fs.readFileSync(rankedCsvPath, 'utf8').trim().split('\n');
        for (let i = 1; i < rankedLines.length; i++) {
          const line = rankedLines[i].trim();
          if (!line) continue;
          const parts = line.split(',');
          if (parts.length >= 5) {
            const rank = parseInt(parts[0], 10);
            const customerID = parts[1];
            const prob = parseFloat(parts[2]);
            const pred = parts[3].toLowerCase() === 'true';
            const category = parts[4];
            const reasons: string[] = [];
            for (let r = 5; r < parts.length; r++) {
              if (parts[r] && parts[r].trim()) {
                reasons.push(parts[r].trim());
              }
            }
            rankedMap.set(customerID, { rank, prob, pred, category, reasons });
          }
        }
      }

      // Parse raw CSV
      if (fs.existsSync(rawCsvPath)) {
        const rawLines = fs.readFileSync(rawCsvPath, 'utf8').trim().split('\n');
        const header = rawLines[0].split(',').map((h) => h.trim());

        for (let i = 1; i < rawLines.length; i++) {
          const line = rawLines[i].trim();
          if (!line) continue;
          const cols = line.split(',').map((c) => c.trim());
          if (cols.length < header.length) continue;

          const recordObj: any = {};
          header.forEach((colName, idx) => {
            recordObj[colName] = cols[idx];
          });

          const customerID = recordObj.customerID;
          const rankedInfo = rankedMap.get(customerID);

          const tenure = parseInt(recordObj.tenure, 10) || 0;
          const monthlyCharges = parseFloat(recordObj.MonthlyCharges) || 0;
          let totalCharges = parseFloat(recordObj.TotalCharges);
          if (isNaN(totalCharges)) totalCharges = 0;

          const record: CustomerRecord = {
            rank: rankedInfo ? rankedInfo.rank : 999999,
            customerID,
            churn_probability: rankedInfo ? rankedInfo.prob : 0.0,
            predicted_churn: rankedInfo ? rankedInfo.pred : false,
            risk_category: rankedInfo ? rankedInfo.category : 'Low Risk',
            review_reasons: rankedInfo ? rankedInfo.reasons : [],
            gender: recordObj.gender || '',
            SeniorCitizen: parseInt(recordObj.SeniorCitizen, 10) || 0,
            Partner: recordObj.Partner || '',
            Dependents: recordObj.Dependents || '',
            tenure,
            PhoneService: recordObj.PhoneService || '',
            MultipleLines: recordObj.MultipleLines || '',
            InternetService: recordObj.InternetService || '',
            OnlineSecurity: recordObj.OnlineSecurity || '',
            OnlineBackup: recordObj.OnlineBackup || '',
            DeviceProtection: recordObj.DeviceProtection || '',
            TechSupport: recordObj.TechSupport || '',
            StreamingTV: recordObj.StreamingTV || '',
            StreamingMovies: recordObj.StreamingMovies || '',
            Contract: recordObj.Contract || '',
            PaperlessBilling: recordObj.PaperlessBilling || '',
            PaymentMethod: recordObj.PaymentMethod || '',
            MonthlyCharges: monthlyCharges,
            TotalCharges: totalCharges,
            Churn: recordObj.Churn || 'No',
          };

          this.customers.push(record);
          this.customerMap.set(customerID, record);
        }

        // Sort default customers by rank ascending
        this.customers.sort((a, b) => a.rank - b.rank);
      }

      this.isLoaded = true;
      console.log(`[DataService] Successfully loaded ${this.customers.length} customer records.`);
    } catch (err) {
      console.error('[DataService] Error loading dataset:', err);
    }
  }

  public getOverview(): OverviewData {
    const total = this.customers.length;
    const churnCount = this.customers.filter((c) => c.Churn === 'Yes').length;
    const observedChurnRate = total > 0 ? (churnCount / total) * 100 : 0;

    const counts = {
      'Low Risk': 0,
      'Medium Risk': 0,
      'High Risk': 0,
      'Very High Risk': 0,
    };

    this.customers.forEach((c) => {
      if (counts[c.risk_category as keyof typeof counts] !== undefined) {
        counts[c.risk_category as keyof typeof counts]++;
      }
    });

    const highPlusVeryHigh = counts['High Risk'] + counts['Very High Risk'];
    const highPlusVeryHighPct = total > 0 ? (highPlusVeryHigh / total) * 100 : 0;

    const topHighRisk = this.customers
      .slice(0, 10)
      .map((c) => ({
        rank: c.rank,
        customerID: c.customerID,
        risk_category: c.risk_category,
        churn_probability: c.churn_probability,
        primary_reason: c.review_reasons[0] || 'Month-to-month contract',
        contract: c.Contract,
        tenure: c.tenure,
        monthly_charges: c.MonthlyCharges,
      }));

    return {
      total_customers_scored: total,
      observed_churn_rate: parseFloat(observedChurnRate.toFixed(2)),
      observed_churn_count: churnCount,
      risk_category_counts: counts,
      risk_category_percentages: {
        'Low Risk': parseFloat(((counts['Low Risk'] / total) * 100).toFixed(2)),
        'Medium Risk': parseFloat(((counts['Medium Risk'] / total) * 100).toFixed(2)),
        'High Risk': parseFloat(((counts['High Risk'] / total) * 100).toFixed(2)),
        'Very High Risk': parseFloat(((counts['Very High Risk'] / total) * 100).toFixed(2)),
      },
      high_risk_or_very_high_risk_count: highPlusVeryHigh,
      high_risk_or_very_high_risk_pct: parseFloat(highPlusVeryHighPct.toFixed(2)),
      top_high_risk_customers: topHighRisk,
    };
  }

  public getCustomers(params: CustomerQueryParams) {
    let filtered = [...this.customers];

    if (params.search) {
      const q = params.search.trim().toLowerCase();
      filtered = filtered.filter((c) => c.customerID.toLowerCase().includes(q));
    }

    if (params.risk_category && params.risk_category !== 'all') {
      filtered = filtered.filter((c) => c.risk_category === params.risk_category);
    }

    if (params.predicted_churn && params.predicted_churn !== 'all') {
      const isPredicted = params.predicted_churn.toLowerCase() === 'yes';
      filtered = filtered.filter((c) => c.predicted_churn === isPredicted);
    }

    if (params.contract && params.contract !== 'all') {
      filtered = filtered.filter((c) => c.Contract === params.contract);
    }

    if (params.internet_service && params.internet_service !== 'all') {
      filtered = filtered.filter((c) => c.InternetService === params.internet_service);
    }

    if (params.payment_method && params.payment_method !== 'all') {
      filtered = filtered.filter((c) => c.PaymentMethod === params.payment_method);
    }

    // Sort
    const sortBy = params.sort_by || 'churn_probability';
    const sortOrder = params.sort_order || 'desc';
    const multiplier = sortOrder === 'desc' ? -1 : 1;

    filtered.sort((a, b) => {
      let valA = a[sortBy as keyof CustomerRecord];
      let valB = b[sortBy as keyof CustomerRecord];

      if (typeof valA === 'number' && typeof valB === 'number') {
        return (valA - valB) * multiplier;
      }
      return String(valA).localeCompare(String(valB)) * multiplier;
    });

    // Pagination
    const page = Math.max(1, params.page || 1);
    const limit = Math.max(1, params.limit || 20);
    const totalItems = filtered.length;
    const totalPages = Math.ceil(totalItems / limit);
    const startIndex = (page - 1) * limit;
    const paginatedItems = filtered.slice(startIndex, startIndex + limit);

    return {
      customers: paginatedItems,
      pagination: {
        total_items: totalItems,
        page,
        limit,
        total_pages: totalPages,
      },
    };
  }

  public getCustomerById(customerID: string): CustomerRecord | null {
    return this.customerMap.get(customerID) || null;
  }

  public getRiskAnalysis() {
    const total = this.customers.length;

    // Histogram bins [0.0-0.1, 0.1-0.2, ..., 0.9-1.0]
    const bins = [
      { bin: '0.00 - 0.10', count: 0 },
      { bin: '0.10 - 0.20', count: 0 },
      { bin: '0.20 - 0.30', count: 0 },
      { bin: '0.30 - 0.40', count: 0 },
      { bin: '0.40 - 0.50', count: 0 },
      { bin: '0.50 - 0.60', count: 0 },
      { bin: '0.60 - 0.70', count: 0 },
      { bin: '0.70 - 0.80', count: 0 },
      { bin: '0.80 - 0.90', count: 0 },
      { bin: '0.90 - 1.00', count: 0 },
    ];

    this.customers.forEach((c) => {
      const idx = Math.min(9, Math.floor(c.churn_probability * 10));
      bins[idx].count++;
    });

    const highRiskGroup = this.customers.filter((c) => c.churn_probability >= 0.50);

    // Median tenure helper
    const getMedian = (arr: number[]) => {
      if (!arr.length) return 0;
      const sorted = [...arr].sort((a, b) => a - b);
      const mid = Math.floor(sorted.length / 2);
      return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    };

    const overallTenures = this.customers.map((c) => c.tenure);
    const highRiskTenures = highRiskGroup.map((c) => c.tenure);

    const overallMonthly = this.customers.map((c) => c.MonthlyCharges);
    const highRiskMonthly = highRiskGroup.map((c) => c.MonthlyCharges);

    const overallM2M = (this.customers.filter((c) => c.Contract === 'Month-to-month').length / total) * 100;
    const highRiskM2M = highRiskGroup.length > 0
      ? (highRiskGroup.filter((c) => c.Contract === 'Month-to-month').length / highRiskGroup.length) * 100
      : 0;

    const overallFiber = (this.customers.filter((c) => c.InternetService === 'Fiber optic').length / total) * 100;
    const highRiskFiber = highRiskGroup.length > 0
      ? (highRiskGroup.filter((c) => c.InternetService === 'Fiber optic').length / highRiskGroup.length) * 100
      : 0;

    const overallECheck = (this.customers.filter((c) => c.PaymentMethod === 'Electronic check').length / total) * 100;
    const highRiskECheck = highRiskGroup.length > 0
      ? (highRiskGroup.filter((c) => c.PaymentMethod === 'Electronic check').length / highRiskGroup.length) * 100
      : 0;

    return {
      total_customers: total,
      probability_histogram: bins,
      high_risk_concentration: {
        high_and_very_high_count: highRiskGroup.length,
        high_and_very_high_pct: parseFloat(((highRiskGroup.length / total) * 100).toFixed(2)),
      },
      comparative_characteristics: {
        overall: {
          median_tenure: getMedian(overallTenures),
          median_monthly_charges: parseFloat(getMedian(overallMonthly).toFixed(2)),
          month_to_month_pct: parseFloat(overallM2M.toFixed(2)),
          fiber_optic_pct: parseFloat(overallFiber.toFixed(2)),
          electronic_check_pct: parseFloat(overallECheck.toFixed(2)),
        },
        high_risk_segment: {
          median_tenure: getMedian(highRiskTenures),
          median_monthly_charges: parseFloat(getMedian(highRiskMonthly).toFixed(2)),
          month_to_month_pct: parseFloat(highRiskM2M.toFixed(2)),
          fiber_optic_pct: parseFloat(highRiskFiber.toFixed(2)),
          electronic_check_pct: parseFloat(highRiskECheck.toFixed(2)),
        },
      },
    };
  }

  public getModelInsights() {
    return {
      explainability_summary: this.explainabilitySummary,
      final_test_results: this.finalTestResults,
      error_analysis: this.errorAnalysis,
    };
  }
}

export const dataService = new DataService();

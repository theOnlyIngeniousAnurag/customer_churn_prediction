import React from 'react';
import { ShieldAlert, Users, AlertTriangle, ArrowRight, UserCheck } from 'lucide-react';

interface OverviewViewProps {
  overviewData: any;
  onSelectCustomer: (id: string) => void;
  onNavigateToCustomers: () => void;
}

export const OverviewView: React.FC<OverviewViewProps> = ({
  overviewData,
  onSelectCustomer,
  onNavigateToCustomers,
}) => {
  if (!overviewData) {
    return (
      <div className="p-8 text-center text-slate-400">
        Loading customer risk overview...
      </div>
    );
  }

  const {
    total_customers_scored = 7043,
    observed_churn_rate = 26.54,
    observed_churn_count = 1869,
    risk_category_counts = { 'Low Risk': 4354, 'Medium Risk': 1327, 'High Risk': 934, 'Very High Risk': 428 },
    risk_category_percentages = { 'Low Risk': 61.82, 'Medium Risk': 18.84, 'High Risk': 13.26, 'Very High Risk': 6.08 },
    high_risk_or_very_high_risk_count = 1362,
    high_risk_or_very_high_risk_pct = 19.34,
    top_high_risk_customers = [],
  } = overviewData;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto text-slate-200">
      {/* 4 Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Customers Scored</span>
            <Users className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-bold text-slate-100">{total_customers_scored.toLocaleString()}</div>
          <p className="text-xs text-slate-400 mt-1">Full dataset portfolio evaluated</p>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">High + Very High Risk</span>
            <AlertTriangle className="w-4 h-4 text-orange-400" />
          </div>
          <div className="text-2xl font-bold text-orange-400">
            {high_risk_or_very_high_risk_count.toLocaleString()}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            <span className="font-semibold text-orange-400">{high_risk_or_very_high_risk_pct}%</span> of total scored portfolio
          </p>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Very High Risk</span>
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-rose-400">
            {risk_category_counts['Very High Risk']?.toLocaleString() || 428}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            <span className="font-semibold text-rose-400">{risk_category_percentages['Very High Risk']}%</span> (prob ≥ 0.70)
          </p>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Observed Churn Rate</span>
            <UserCheck className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-bold text-slate-100">{observed_churn_rate}%</div>
          <p className="text-xs text-slate-400 mt-1">{observed_churn_count.toLocaleString()} actual churn cases recorded</p>
        </div>
      </div>

      {/* Risk Category Distribution Bar */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-semibold text-slate-100">Portfolio Risk Distribution</h3>
            <p className="text-xs text-slate-400 mt-0.5">Categorized into 4 operational probability bands</p>
          </div>
          <button
            onClick={onNavigateToCustomers}
            className="text-xs font-medium text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
          >
            <span>Explorer Customers</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Stacked Bar */}
        <div className="w-full h-4 bg-slate-800 rounded-full overflow-hidden flex shadow-inner">
          <div
            style={{ width: `${risk_category_percentages['Low Risk']}%` }}
            className="bg-emerald-500 h-full transition-all duration-300"
            title={`Low Risk: ${risk_category_counts['Low Risk']} (${risk_category_percentages['Low Risk']}%)`}
          />
          <div
            style={{ width: `${risk_category_percentages['Medium Risk']}%` }}
            className="bg-amber-500 h-full transition-all duration-300"
            title={`Medium Risk: ${risk_category_counts['Medium Risk']} (${risk_category_percentages['Medium Risk']}%)`}
          />
          <div
            style={{ width: `${risk_category_percentages['High Risk']}%` }}
            className="bg-orange-500 h-full transition-all duration-300"
            title={`High Risk: ${risk_category_counts['High Risk']} (${risk_category_percentages['High Risk']}%)`}
          />
          <div
            style={{ width: `${risk_category_percentages['Very High Risk']}%` }}
            className="bg-rose-500 h-full transition-all duration-300"
            title={`Very High Risk: ${risk_category_counts['Very High Risk']} (${risk_category_percentages['Very High Risk']}%)`}
          />
        </div>

        {/* Category Legend */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
          <div className="flex items-center space-x-2.5">
            <span className="w-3 h-3 rounded-full bg-emerald-500 shrink-0"></span>
            <div>
              <div className="text-xs font-medium text-slate-200">
                Low Risk <span className="text-slate-400 text-2xs">(prob &lt; 0.30)</span>
              </div>
              <div className="text-xs text-slate-400 font-semibold">
                {risk_category_counts['Low Risk']?.toLocaleString()} ({risk_category_percentages['Low Risk']}%)
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2.5">
            <span className="w-3 h-3 rounded-full bg-amber-500 shrink-0"></span>
            <div>
              <div className="text-xs font-medium text-slate-200">
                Medium Risk <span className="text-slate-400 text-2xs">(0.30–0.49)</span>
              </div>
              <div className="text-xs text-slate-400 font-semibold">
                {risk_category_counts['Medium Risk']?.toLocaleString()} ({risk_category_percentages['Medium Risk']}%)
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2.5">
            <span className="w-3 h-3 rounded-full bg-orange-500 shrink-0"></span>
            <div>
              <div className="text-xs font-medium text-slate-200">
                High Risk <span className="text-slate-400 text-2xs">(0.50–0.69)</span>
              </div>
              <div className="text-xs text-slate-400 font-semibold">
                {risk_category_counts['High Risk']?.toLocaleString()} ({risk_category_percentages['High Risk']}%)
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2.5">
            <span className="w-3 h-3 rounded-full bg-rose-500 shrink-0"></span>
            <div>
              <div className="text-xs font-medium text-slate-200">
                Very High Risk <span className="text-slate-400 text-2xs">(prob ≥ 0.70)</span>
              </div>
              <div className="text-xs text-slate-400 font-semibold">
                {risk_category_counts['Very High Risk']?.toLocaleString()} ({risk_category_percentages['Very High Risk']}%)
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* High-Risk Exposure Banner */}
      <div className="bg-gradient-to-r from-orange-950/40 via-slate-900 to-slate-900 border border-orange-500/30 p-5 rounded-xl flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-orange-500/10 rounded-lg text-orange-400 border border-orange-500/20 shrink-0">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-orange-200">High-Risk Portfolio Concentration</h4>
            <p className="text-xs text-slate-300 mt-0.5">
              <strong className="text-orange-400">{high_risk_or_very_high_risk_count.toLocaleString()} accounts ({high_risk_or_very_high_risk_pct}%)</strong> exhibit elevated churn probability scores and qualify for decision-support review.
            </p>
          </div>
        </div>
        <button
          onClick={onNavigateToCustomers}
          className="px-4 py-2 text-xs font-medium bg-orange-500/20 text-orange-300 hover:bg-orange-500/30 border border-orange-500/30 rounded-lg transition-all shrink-0 ml-4"
        >
          View High-Risk Accounts
        </button>
      </div>

      {/* Top Customers to Review Table */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h3 className="text-base font-semibold text-slate-100">Top Priority Accounts for Review</h3>
            <p className="text-xs text-slate-400 mt-0.5">Highest estimated churn probabilities from the validated model</p>
          </div>
          <span className="text-xs text-slate-400 bg-slate-800 px-2.5 py-1 rounded-md border border-slate-700/50">
            Showing Top {top_high_risk_customers.length}
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 uppercase text-2xs tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Rank</th>
                <th className="py-3 px-4">Customer ID</th>
                <th className="py-3 px-4">Risk Category</th>
                <th className="py-3 px-4 text-right">Probability</th>
                <th className="py-3 px-4">Contract</th>
                <th className="py-3 px-4">Primary Review Reason</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
              {top_high_risk_customers.map((customer: any) => {
                const probPct = (customer.churn_probability * 100).toFixed(2);
                const isVeryHigh = customer.risk_category === 'Very High Risk';

                return (
                  <tr key={customer.customerID} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-sans text-slate-400">#{customer.rank}</td>
                    <td className="py-3 px-4 font-semibold text-slate-100">{customer.customerID}</td>
                    <td className="py-3 px-4 font-sans">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-md text-2xs font-semibold border ${
                          isVeryHigh
                            ? 'bg-rose-500/15 text-rose-400 border-rose-500/30'
                            : 'bg-orange-500/15 text-orange-400 border-orange-500/30'
                        }`}
                      >
                        {customer.risk_category}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-semibold text-rose-400">{probPct}%</td>
                    <td className="py-3 px-4 font-sans text-slate-300">{customer.contract}</td>
                    <td className="py-3 px-4 font-sans text-slate-400 truncate max-w-xs">
                      {customer.primary_reason}
                    </td>
                    <td className="py-3 px-4 text-right font-sans">
                      <button
                        onClick={() => onSelectCustomer(customer.customerID)}
                        className="text-xs text-indigo-400 hover:text-indigo-300 font-medium px-2.5 py-1 rounded bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 transition-all"
                      >
                        Review Profile
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

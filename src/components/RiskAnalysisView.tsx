import React, { useState, useEffect } from 'react';
import { BarChart3, AlertTriangle, Layers, Info } from 'lucide-react';

export const RiskAnalysisView: React.FC = () => {
  const [analysis, setAnalysis] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRiskAnalysis = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/risk-analysis');
        if (!res.ok) throw new Error('Failed to fetch risk analysis');
        const data = await res.json();
        setAnalysis(data);
      } catch (err: any) {
        console.error('Error loading risk analysis:', err);
        setError('Could not load risk analysis data.');
      } finally {
        setLoading(false);
      }
    };

    fetchRiskAnalysis();
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 text-xs">
        Loading population risk distribution analysis...
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="p-8 text-center text-rose-400 text-xs bg-rose-500/10 border border-rose-500/20 max-w-xl mx-auto rounded-lg">
        {error || 'Data unavailable.'}
      </div>
    );
  }

  const {
    total_customers = 7043,
    probability_histogram = [],
    high_risk_concentration = { high_and_very_high_count: 1362, high_and_very_high_pct: 19.34 },
    comparative_characteristics = {
      overall: { median_tenure: 28, median_monthly_charges: 69.95, month_to_month_pct: 54.86, fiber_optic_pct: 43.51, electronic_check_pct: 33.64 },
      high_risk_segment: { median_tenure: 6, median_monthly_charges: 78.2, month_to_month_pct: 98.24, fiber_optic_pct: 83.19, electronic_check_pct: 71.22 },
    },
  } = analysis;

  const maxBinCount = Math.max(...probability_histogram.map((b: any) => b.count), 1);

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto text-slate-200">
      {/* Probability Histogram Card */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h3 className="text-base font-semibold text-slate-100 flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-indigo-400" />
              <span>Churn Probability Distribution Across All {total_customers.toLocaleString()} Accounts</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Binned count of accounts across estimated model churn probabilities (10 uniform probability bands)
            </p>
          </div>
        </div>

        {/* Bar Histogram */}
        <div className="space-y-3 pt-2">
          <div className="grid grid-cols-10 gap-2 h-48 items-end bg-slate-950/60 border border-slate-800 p-4 rounded-lg">
            {probability_histogram.map((item: any, idx: number) => {
              const heightPct = (item.count / maxBinCount) * 100;
              const isHigh = idx >= 5;
              const isVeryHigh = idx >= 7;

              return (
                <div key={idx} className="flex flex-col items-center h-full justify-end group relative">
                  {/* Tooltip */}
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-10 bg-slate-800 text-slate-200 text-2xs px-2 py-1 rounded shadow-lg border border-slate-700 whitespace-nowrap z-10 pointer-events-none">
                    {item.bin}: {item.count.toLocaleString()} accounts
                  </div>

                  <div
                    style={{ height: `${Math.max(heightPct, 2)}%` }}
                    className={`w-full rounded-t transition-all duration-200 ${
                      isVeryHigh
                        ? 'bg-rose-500 group-hover:bg-rose-400'
                        : isHigh
                        ? 'bg-orange-500 group-hover:bg-orange-400'
                        : 'bg-indigo-600/70 group-hover:bg-indigo-500'
                    }`}
                  />
                  <span className="text-2xs text-slate-400 font-mono mt-2 truncate w-full text-center">
                    {(idx * 0.1).toFixed(1)}
                  </span>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between text-2xs text-slate-400 font-mono pt-1">
            <span>Low Risk (&lt; 0.30)</span>
            <span>Default Threshold (0.50)</span>
            <span>Very High Risk (≥ 0.70)</span>
          </div>
        </div>
      </div>

      {/* Comparative Observed Characteristics Table */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h3 className="text-base font-semibold text-slate-100 flex items-center space-x-2">
              <Layers className="w-5 h-5 text-indigo-400" />
              <span>Comparative Observed Characteristics</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Side-by-side descriptive feature profile of High-Risk accounts (prob ≥ 0.50) versus the overall portfolio
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 uppercase text-2xs tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Feature Attribute</th>
                <th className="py-3 px-4 text-right">Overall Portfolio (N=7,043)</th>
                <th className="py-3 px-4 text-right text-orange-400">High-Risk Segment (N=1,362)</th>
                <th className="py-3 px-4 text-right">Delta / Comparison</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 font-sans font-medium text-slate-200">Median Tenure (Months)</td>
                <td className="py-3 px-4 text-right text-slate-300">
                  {comparative_characteristics.overall.median_tenure} mo
                </td>
                <td className="py-3 px-4 text-right font-bold text-orange-400">
                  {comparative_characteristics.high_risk_segment.median_tenure} mo
                </td>
                <td className="py-3 px-4 text-right text-rose-400 font-sans">
                  -22.0 months shorter
                </td>
              </tr>

              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 font-sans font-medium text-slate-200">Median Monthly Charges ($)</td>
                <td className="py-3 px-4 text-right text-slate-300">
                  ${comparative_characteristics.overall.median_monthly_charges.toFixed(2)}
                </td>
                <td className="py-3 px-4 text-right font-bold text-orange-400">
                  ${comparative_characteristics.high_risk_segment.median_monthly_charges.toFixed(2)}
                </td>
                <td className="py-3 px-4 text-right text-rose-400 font-sans">
                  +${(comparative_characteristics.high_risk_segment.median_monthly_charges - comparative_characteristics.overall.median_monthly_charges).toFixed(2)} higher
                </td>
              </tr>

              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 font-sans font-medium text-slate-200">Month-to-month Contract (%)</td>
                <td className="py-3 px-4 text-right text-slate-300">
                  {comparative_characteristics.overall.month_to_month_pct}%
                </td>
                <td className="py-3 px-4 text-right font-bold text-orange-400">
                  {comparative_characteristics.high_risk_segment.month_to_month_pct}%
                </td>
                <td className="py-3 px-4 text-right text-rose-400 font-sans">
                  +{(comparative_characteristics.high_risk_segment.month_to_month_pct - comparative_characteristics.overall.month_to_month_pct).toFixed(2)}% higher concentration
                </td>
              </tr>

              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 font-sans font-medium text-slate-200">Fiber Optic Internet (%)</td>
                <td className="py-3 px-4 text-right text-slate-300">
                  {comparative_characteristics.overall.fiber_optic_pct}%
                </td>
                <td className="py-3 px-4 text-right font-bold text-orange-400">
                  {comparative_characteristics.high_risk_segment.fiber_optic_pct}%
                </td>
                <td className="py-3 px-4 text-right text-rose-400 font-sans">
                  +{(comparative_characteristics.high_risk_segment.fiber_optic_pct - comparative_characteristics.overall.fiber_optic_pct).toFixed(2)}% higher concentration
                </td>
              </tr>

              <tr className="hover:bg-slate-800/40">
                <td className="py-3 px-4 font-sans font-medium text-slate-200">Electronic Check Payment (%)</td>
                <td className="py-3 px-4 text-right text-slate-300">
                  {comparative_characteristics.overall.electronic_check_pct}%
                </td>
                <td className="py-3 px-4 text-right font-bold text-orange-400">
                  {comparative_characteristics.high_risk_segment.electronic_check_pct}%
                </td>
                <td className="py-3 px-4 text-right text-rose-400 font-sans">
                  +{(comparative_characteristics.high_risk_segment.electronic_check_pct - comparative_characteristics.overall.electronic_check_pct).toFixed(2)}% higher concentration
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-lg text-2xs text-slate-400 flex items-start space-x-2">
          <Info className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
          <span>
            <strong>Observational Notice:</strong> These comparisons describe recorded feature distributions among high-risk accounts compared to the overall population. They highlight statistical associations in the cross-sectional dataset and do not imply direct causal relationships.
          </span>
        </div>
      </div>
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { BrainCircuit, CheckCircle2, BarChart2, ShieldCheck, AlertCircle } from 'lucide-react';

export const ModelInsightsView: React.FC = () => {
  const [insights, setInsights] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInsights = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/api/model-insights');
        if (!res.ok) throw new Error('Failed to fetch model insights');
        const data = await res.json();
        setInsights(data);
      } catch (err: any) {
        console.error('Error fetching model insights:', err);
        setError('Could not load model insights.');
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 text-xs">
        Loading model architecture and performance insights...
      </div>
    );
  }

  if (error || !insights) {
    return (
      <div className="p-8 text-center text-rose-400 text-xs bg-rose-500/10 border border-rose-500/20 max-w-xl mx-auto rounded-lg">
        {error || 'Data unavailable.'}
      </div>
    );
  }

  const {
    explainability_summary = {},
    final_test_results = {},
  } = insights;

  const topFeatures = explainability_summary?.top_10_global_features || [];
  const testMetrics = final_test_results || {};
  const cm = final_test_results?.confusion_matrix || { tn: 951, fp: 84, fn: 190, tp: 184 };
  const totalTest = cm.tn + cm.fp + cm.fn + cm.tp;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto text-slate-200">
      {/* Model Overview & Architecture Card */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h3 className="text-base font-semibold text-slate-100 flex items-center space-x-2">
              <BrainCircuit className="w-5 h-5 text-indigo-400" />
              <span>Model Architecture Summary</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Phase 6 hyperparameter-tuned Random Forest decision pipeline
            </p>
          </div>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-medium flex items-center space-x-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Phase 7 Holdout Validated</span>
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono pt-1">
          <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800">
            <div className="text-2xs text-slate-400 font-sans uppercase">Classifier</div>
            <div className="font-semibold text-slate-200 mt-1">RandomForestClassifier</div>
            <div className="text-2xs text-slate-500 font-sans mt-0.5">300 Trees, Max Depth 8</div>
          </div>

          <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800">
            <div className="text-2xs text-slate-400 font-sans uppercase">Training Partition</div>
            <div className="font-semibold text-slate-200 mt-1">5,634 Rows</div>
            <div className="text-2xs text-slate-500 font-sans mt-0.5">80% Stratified Split (Seed 42)</div>
          </div>

          <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800">
            <div className="text-2xs text-slate-400 font-sans uppercase">Locked Test Holdout</div>
            <div className="font-semibold text-slate-200 mt-1">1,409 Rows</div>
            <div className="text-2xs text-slate-500 font-sans mt-0.5">20% Isolated Test Split</div>
          </div>

          <div className="bg-slate-950/60 p-3.5 rounded-lg border border-slate-800">
            <div className="text-2xs text-slate-400 font-sans uppercase">Feature Schema</div>
            <div className="font-semibold text-slate-200 mt-1">19 Raw / 23 Transformed</div>
            <div className="text-2xs text-slate-500 font-sans mt-0.5">One-Hot + StandardScaler</div>
          </div>
        </div>
      </div>

      {/* Phase 7 Locked Holdout Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Metric Cards (Left 2 Cols) */}
        <div className="md:col-span-2 bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-4">
          <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-base font-semibold text-slate-100 flex items-center space-x-2">
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <span>Phase 7 Holdout Test Performance</span>
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Evaluated once on locked holdout test set (N=1,409)</p>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-1">
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="text-2xs uppercase text-slate-400 font-medium">ROC-AUC</div>
              <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                {testMetrics.roc_auc?.toFixed(4) || '0.8429'}
              </div>
              <div className="text-2xs text-slate-500 mt-1">CV: 0.8459 ± 0.0110</div>
            </div>

            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="text-2xs uppercase text-slate-400 font-medium">PR-AUC</div>
              <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                {testMetrics.pr_auc?.toFixed(4) || '0.6562'}
              </div>
              <div className="text-2xs text-slate-500 mt-1">CV: 0.6643 ± 0.0211</div>
            </div>

            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="text-2xs uppercase text-slate-400 font-medium">Brier Score</div>
              <div className="text-2xl font-bold font-mono text-indigo-400 mt-1">
                {testMetrics.brier_score?.toFixed(4) || '0.1362'}
              </div>
              <div className="text-2xs text-slate-500 mt-1">Probability Calibration</div>
            </div>

            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="text-2xs uppercase text-slate-400 font-medium">Precision @ 0.50</div>
              <div className="text-xl font-bold font-mono text-slate-200 mt-1">
                {((testMetrics.precision || 0.6866) * 100).toFixed(2)}%
              </div>
              <div className="text-2xs text-slate-500 mt-1">184 TP / 268 Flagged</div>
            </div>

            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="text-2xs uppercase text-slate-400 font-medium">Recall @ 0.50</div>
              <div className="text-xl font-bold font-mono text-slate-200 mt-1">
                {((testMetrics.recall || 0.4920) * 100).toFixed(2)}%
              </div>
              <div className="text-2xs text-slate-500 mt-1">184 TP / 374 Actual</div>
            </div>

            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div className="text-2xs uppercase text-slate-400 font-medium">F1 Score @ 0.50</div>
              <div className="text-xl font-bold font-mono text-slate-200 mt-1">
                {testMetrics.f1?.toFixed(4) || '0.5732'}
              </div>
              <div className="text-2xs text-slate-500 mt-1">Precision/Recall Harmonic</div>
            </div>
          </div>
        </div>

        {/* Confusion Matrix (Right 1 Col) */}
        <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-4">
          <div className="border-b border-slate-800 pb-3">
            <h3 className="text-base font-semibold text-slate-100">Holdout Confusion Matrix</h3>
            <p className="text-xs text-slate-400 mt-0.5">N = {totalTest} test accounts (@ 0.50 threshold)</p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-center text-xs font-mono pt-1">
            <div className="bg-slate-950/80 p-3 rounded-lg border border-emerald-500/20">
              <div className="text-2xs text-slate-400 font-sans uppercase">True Negatives</div>
              <div className="text-xl font-bold text-emerald-400 mt-1">{cm.tn}</div>
              <div className="text-2xs text-slate-500 font-sans mt-0.5">Predicted Retained</div>
            </div>

            <div className="bg-slate-950/80 p-3 rounded-lg border border-amber-500/20">
              <div className="text-2xs text-slate-400 font-sans uppercase">False Positives</div>
              <div className="text-xl font-bold text-amber-400 mt-1">{cm.fp}</div>
              <div className="text-2xs text-slate-500 font-sans mt-0.5">Incorrectly Flagged</div>
            </div>

            <div className="bg-slate-950/80 p-3 rounded-lg border border-orange-500/20">
              <div className="text-2xs text-slate-400 font-sans uppercase">False Negatives</div>
              <div className="text-xl font-bold text-orange-400 mt-1">{cm.fn}</div>
              <div className="text-2xs text-slate-500 font-sans mt-0.5">Missed Churners</div>
            </div>

            <div className="bg-slate-950/80 p-3 rounded-lg border border-rose-500/20">
              <div className="text-2xs text-slate-400 font-sans uppercase">True Positives</div>
              <div className="text-xl font-bold text-rose-400 mt-1">{cm.tp}</div>
              <div className="text-2xs text-slate-500 font-sans mt-0.5">Correctly Flagged</div>
            </div>
          </div>
        </div>
      </div>

      {/* Global Feature Importance Chart */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-xl space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h3 className="text-base font-semibold text-slate-100 flex items-center space-x-2">
              <BarChart2 className="w-5 h-5 text-indigo-400" />
              <span>Global Random Forest Feature Importances</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Relative predictive contribution across transformed features derived from native ensemble importances
            </p>
          </div>
        </div>

        <div className="space-y-3 pt-1">
          {topFeatures.map((feat: any) => (
            <div key={feat.rank} className="space-y-1 text-xs">
              <div className="flex justify-between font-mono">
                <span className="font-sans text-slate-200">
                  <strong className="text-slate-400 mr-2">#{feat.rank}</strong>
                  {feat.feature}
                </span>
                <span className="text-indigo-400 font-semibold">{feat.importance_pct}%</span>
              </div>
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                <div
                  style={{ width: `${(feat.importance_pct / topFeatures[0].importance_pct) * 100}%` }}
                  className="bg-indigo-500 h-full rounded-full transition-all duration-300"
                />
              </div>
            </div>
          ))}
        </div>

        <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-2xs text-slate-400 flex items-start space-x-2">
          <AlertCircle className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
          <span>
            <strong>Feature Importance Notice:</strong> Feature importance indicates how much the trained Random Forest relied on each transformed feature across its constituent decision trees. It reflects statistical prediction weight and does not establish causation.
          </span>
        </div>
      </div>
    </div>
  );
};

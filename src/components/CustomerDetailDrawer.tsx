import React, { useState, useEffect } from 'react';
import { X, ShieldAlert, AlertCircle, CheckCircle2, CreditCard, User, Layers, Receipt } from 'lucide-react';

interface CustomerDetailDrawerProps {
  customerID: string | null;
  onClose: () => void;
}

export const CustomerDetailDrawer: React.FC<CustomerDetailDrawerProps> = ({
  customerID,
  onClose,
}) => {
  const [customer, setCustomer] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!customerID) {
      setCustomer(null);
      return;
    }

    const fetchDetail = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`/api/customers/${customerID}`);
        if (!res.ok) throw new Error(`Customer '${customerID}' not found.`);
        const data = await res.json();
        setCustomer(data);
      } catch (err: any) {
        console.error('Error fetching customer detail:', err);
        setError(err.message || 'Failed to load customer profile');
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [customerID]);

  if (!customerID) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex justify-end transition-opacity">
      <div className="w-full max-w-2xl bg-slate-900 border-l border-slate-800 h-full overflow-y-auto flex flex-col shadow-2xl text-slate-200 animate-in slide-in-from-right duration-200">
        {/* Drawer Header */}
        <div className="p-6 border-b border-slate-800 flex items-center justify-between sticky top-0 bg-slate-900/95 backdrop-blur-md z-10">
          <div>
            <div className="flex items-center space-x-3">
              <h3 className="text-xl font-bold font-mono text-slate-100">{customerID}</h3>
              {customer && (
                <span
                  className={`px-2.5 py-0.5 rounded-md text-xs font-semibold border ${
                    customer.risk_category === 'Very High Risk'
                      ? 'bg-rose-500/15 text-rose-400 border-rose-500/30'
                      : customer.risk_category === 'High Risk'
                      ? 'bg-orange-500/15 text-orange-400 border-orange-500/30'
                      : customer.risk_category === 'Medium Risk'
                      ? 'bg-amber-500/15 text-amber-400 border-amber-500/30'
                      : 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                  }`}
                >
                  {customer.risk_category}
                </span>
              )}
            </div>
            <p className="text-xs text-slate-400 mt-1">Customer Profile &amp; Model Evidence Breakdown</p>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-100 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Drawer Body */}
        <div className="p-6 space-y-6 flex-1">
          {loading ? (
            <div className="py-16 text-center text-slate-400 text-xs">
              Loading customer record details...
            </div>
          ) : error ? (
            <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-400 text-xs">
              {error}
            </div>
          ) : customer ? (
            <>
              {/* Estimated Churn Probability Gauge */}
              <div className="bg-slate-950/60 border border-slate-800 p-5 rounded-xl space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-xs text-slate-400 font-medium">
                    <ShieldAlert className="w-4 h-4 text-slate-400" />
                    <span>Estimated Churn Probability</span>
                  </div>
                  <span className="text-2xl font-bold font-mono text-rose-400">
                    {(customer.churn_probability * 100).toFixed(2)}%
                  </span>
                </div>

                <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                  <div
                    style={{ width: `${customer.churn_probability * 100}%` }}
                    className={`h-full transition-all duration-300 ${
                      customer.churn_probability >= 0.70
                        ? 'bg-rose-500'
                        : customer.churn_probability >= 0.50
                        ? 'bg-orange-500'
                        : customer.churn_probability >= 0.30
                        ? 'bg-amber-500'
                        : 'bg-emerald-500'
                    }`}
                  />
                </div>

                <div className="flex justify-between text-2xs text-slate-500">
                  <span>0% (Safest)</span>
                  <span>Default Threshold (50%)</span>
                  <span>100% (Highest)</span>
                </div>
              </div>

              {/* Evidence-Based Review Reasons */}
              <div className="bg-slate-950/60 border border-slate-800 p-5 rounded-xl space-y-3">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-orange-400" />
                  <span>Why This Customer Was Flagged</span>
                </h4>

                {customer.review_reasons && customer.review_reasons.length > 0 ? (
                  <ul className="space-y-2 pt-1">
                    {customer.review_reasons.map((reason: string, idx: number) => (
                      <li
                        key={idx}
                        className="text-xs bg-slate-900/90 border border-slate-800/80 px-3 py-2 rounded-lg text-slate-300 flex items-start space-x-2.5"
                      >
                        <span className="w-1.5 h-1.5 rounded-full bg-orange-400 mt-1.5 shrink-0" />
                        <span>{reason}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-slate-400 italic">
                    No elevated risk flags observed for this account.
                  </p>
                )}
              </div>

              {/* Account Attributes Grid */}
              <div className="space-y-4">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-2">
                  Observed Account Characteristics
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Account Info */}
                  <div className="bg-slate-950/40 border border-slate-800/80 p-4 rounded-xl space-y-2 text-xs">
                    <div className="flex items-center space-x-2 text-slate-400 font-medium mb-3">
                      <User className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Account Info</span>
                    </div>

                    <div className="flex justify-between">
                      <span className="text-slate-400">Tenure:</span>
                      <span className="font-semibold text-slate-200">{customer.tenure} months</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Contract:</span>
                      <span className="font-semibold text-slate-200">{customer.Contract}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Senior Citizen:</span>
                      <span className="text-slate-300">{customer.SeniorCitizen === 1 ? 'Yes' : 'No'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Partner:</span>
                      <span className="text-slate-300">{customer.Partner}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Dependents:</span>
                      <span className="text-slate-300">{customer.Dependents}</span>
                    </div>
                  </div>

                  {/* Services Subscribed */}
                  <div className="bg-slate-950/40 border border-slate-800/80 p-4 rounded-xl space-y-2 text-xs">
                    <div className="flex items-center space-x-2 text-slate-400 font-medium mb-3">
                      <Layers className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Services</span>
                    </div>

                    <div className="flex justify-between">
                      <span className="text-slate-400">Internet:</span>
                      <span className="font-semibold text-slate-200">{customer.InternetService}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Tech Support:</span>
                      <span className="text-slate-300">{customer.TechSupport}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Online Security:</span>
                      <span className="text-slate-300">{customer.OnlineSecurity}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Online Backup:</span>
                      <span className="text-slate-300">{customer.OnlineBackup}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Streaming TV/Movies:</span>
                      <span className="text-slate-300">{customer.StreamingTV === 'Yes' || customer.StreamingMovies === 'Yes' ? 'Active' : 'None'}</span>
                    </div>
                  </div>

                  {/* Billing & Payment */}
                  <div className="bg-slate-950/40 border border-slate-800/80 p-4 rounded-xl space-y-2 text-xs">
                    <div className="flex items-center space-x-2 text-slate-400 font-medium mb-3">
                      <Receipt className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Billing &amp; Payment</span>
                    </div>

                    <div className="flex justify-between">
                      <span className="text-slate-400">Monthly Charges:</span>
                      <span className="font-semibold text-slate-200">${customer.MonthlyCharges.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Total Charges:</span>
                      <span className="font-semibold text-slate-200">${customer.TotalCharges.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Paperless Billing:</span>
                      <span className="text-slate-300">{customer.PaperlessBilling}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Payment Method:</span>
                      <span className="text-slate-300 truncate max-w-[110px]" title={customer.PaymentMethod}>
                        {customer.PaymentMethod}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Disclaimer */}
              <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-2xs text-slate-500 leading-relaxed">
                <strong>Model Evidence Notice:</strong> Review reasons represent statistical risk indicators derived from historical model behavior across the customer dataset. They summarize recorded account characteristics and do not establish direct causation.
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};

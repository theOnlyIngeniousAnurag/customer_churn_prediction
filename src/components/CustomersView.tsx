import React, { useState, useEffect } from 'react';
import { Search, Filter, ArrowUpDown, ChevronLeft, ChevronRight, RefreshCw, Eye } from 'lucide-react';

interface CustomersViewProps {
  onSelectCustomer: (id: string) => void;
}

export const CustomersView: React.FC<CustomersViewProps> = ({ onSelectCustomer }) => {
  const [customers, setCustomers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters & Search
  const [search, setSearch] = useState('');
  const [riskCategory, setRiskCategory] = useState('all');
  const [predictedChurn, setPredictedChurn] = useState('all');
  const [contract, setContract] = useState('all');
  const [internetService, setInternetService] = useState('all');
  const [paymentMethod, setPaymentMethod] = useState('all');

  // Sorting & Pagination
  const [sortBy, setSortBy] = useState('churn_probability');
  const [sortOrder, setSortOrder] = useState('desc');
  const [page, setPage] = useState(1);
  const [limit] = useState(20);
  const [pagination, setPagination] = useState({
    total_items: 0,
    page: 1,
    limit: 20,
    total_pages: 1,
  });

  const fetchCustomers = async () => {
    setLoading(true);
    setError(null);
    try {
      const query = new URLSearchParams({
        search,
        risk_category: riskCategory,
        predicted_churn: predictedChurn,
        contract,
        internet_service: internetService,
        payment_method: paymentMethod,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: page.toString(),
        limit: limit.toString(),
      });

      const res = await fetch(`/api/customers?${query.toString()}`);
      if (!res.ok) throw new Error('Failed to fetch customer data');
      const data = await res.json();
      setCustomers(data.customers || []);
      setPagination(data.pagination || { total_items: 0, page: 1, limit: 20, total_pages: 1 });
    } catch (err: any) {
      console.error('Error fetching customers:', err);
      setError('Could not load customer records. Please check the server connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, [search, riskCategory, predictedChurn, contract, internetService, paymentMethod, sortBy, sortOrder, page]);

  const handleResetFilters = () => {
    setSearch('');
    setRiskCategory('all');
    setPredictedChurn('all');
    setContract('all');
    setInternetService('all');
    setPaymentMethod('all');
    setSortBy('churn_probability');
    setSortOrder('desc');
    setPage(1);
  };

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto text-slate-200">
      {/* Search & Filter Header Toolbar */}
      <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* Search Input */}
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search by Customer ID (e.g., 9300-AGZNL)..."
              className="w-full bg-slate-950/70 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500/60 placeholder-slate-500"
            />
          </div>

          <div className="flex items-center space-x-3 text-xs">
            {/* Sort Field */}
            <div className="flex items-center space-x-2 bg-slate-950/70 border border-slate-800 rounded-lg px-3 py-1.5">
              <ArrowUpDown className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-400 font-medium">Sort:</span>
              <select
                value={sortBy}
                onChange={(e) => {
                  setSortBy(e.target.value);
                  setPage(1);
                }}
                className="bg-transparent text-slate-200 focus:outline-none cursor-pointer"
              >
                <option value="churn_probability" className="bg-slate-900 text-slate-200">Probability</option>
                <option value="tenure" className="bg-slate-900 text-slate-200">Tenure</option>
                <option value="MonthlyCharges" className="bg-slate-900 text-slate-200">Monthly Charges</option>
                <option value="TotalCharges" className="bg-slate-900 text-slate-200">Total Charges</option>
                <option value="rank" className="bg-slate-900 text-slate-200">Rank</option>
              </select>
              <button
                onClick={() => setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc')}
                className="text-indigo-400 font-bold ml-1 uppercase hover:text-indigo-300"
                title="Toggle Sort Order"
              >
                {sortOrder}
              </button>
            </div>

            <button
              onClick={handleResetFilters}
              className="px-3 py-1.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 text-slate-300 rounded-lg flex items-center space-x-1.5 transition-all"
            >
              <RefreshCw className="w-3 h-3 text-slate-400" />
              <span>Reset</span>
            </button>
          </div>
        </div>

        {/* Filter Dropdowns Grid */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 pt-2 border-t border-slate-800/80 text-xs">
          <div>
            <label className="block text-2xs text-slate-400 font-medium mb-1">Risk Category</label>
            <select
              value={riskCategory}
              onChange={(e) => {
                setRiskCategory(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-950/70 border border-slate-800 rounded-md px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500/60"
            >
              <option value="all">All Risk Levels</option>
              <option value="Very High Risk">Very High Risk</option>
              <option value="High Risk">High Risk</option>
              <option value="Medium Risk">Medium Risk</option>
              <option value="Low Risk">Low Risk</option>
            </select>
          </div>

          <div>
            <label className="block text-2xs text-slate-400 font-medium mb-1">Predicted Churn</label>
            <select
              value={predictedChurn}
              onChange={(e) => {
                setPredictedChurn(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-950/70 border border-slate-800 rounded-md px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500/60"
            >
              <option value="all">All Predictions</option>
              <option value="yes">Predicted Churn (Yes)</option>
              <option value="no">Predicted Retained (No)</option>
            </select>
          </div>

          <div>
            <label className="block text-2xs text-slate-400 font-medium mb-1">Contract Type</label>
            <select
              value={contract}
              onChange={(e) => {
                setContract(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-950/70 border border-slate-800 rounded-md px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500/60"
            >
              <option value="all">All Contracts</option>
              <option value="Month-to-month">Month-to-month</option>
              <option value="One year">One year</option>
              <option value="Two year">Two year</option>
            </select>
          </div>

          <div>
            <label className="block text-2xs text-slate-400 font-medium mb-1">Internet Service</label>
            <select
              value={internetService}
              onChange={(e) => {
                setInternetService(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-950/70 border border-slate-800 rounded-md px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500/60"
            >
              <option value="all">All Internet</option>
              <option value="Fiber optic">Fiber optic</option>
              <option value="DSL">DSL</option>
              <option value="No">No Internet</option>
            </select>
          </div>

          <div>
            <label className="block text-2xs text-slate-400 font-medium mb-1">Payment Method</label>
            <select
              value={paymentMethod}
              onChange={(e) => {
                setPaymentMethod(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-950/70 border border-slate-800 rounded-md px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500/60 truncate"
            >
              <option value="all">All Payment Methods</option>
              <option value="Electronic check">Electronic check</option>
              <option value="Mailed check">Mailed check</option>
              <option value="Bank transfer (automatic)">Bank transfer</option>
              <option value="Credit card (automatic)">Credit card</option>
            </select>
          </div>
        </div>
      </div>

      {/* Customer Data Table */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <span>
            Showing <strong className="text-slate-200">{customers.length}</strong> of{' '}
            <strong className="text-slate-200">{pagination.total_items.toLocaleString()}</strong> matching accounts
          </span>
          <span>Page {pagination.page} of {pagination.total_pages}</span>
        </div>

        {error ? (
          <div className="p-8 text-center text-rose-400 text-xs bg-rose-500/10 border border-rose-500/20 m-4 rounded-lg">
            {error}
          </div>
        ) : loading ? (
          <div className="p-12 text-center text-slate-400 text-xs">
            Loading matching customer records...
          </div>
        ) : customers.length === 0 ? (
          <div className="p-12 text-center text-slate-400 text-xs">
            No customers match the current filter criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950/60 text-slate-400 uppercase text-2xs tracking-wider border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Rank</th>
                  <th className="py-3 px-4">Customer ID</th>
                  <th className="py-3 px-4">Risk Category</th>
                  <th className="py-3 px-4 text-right">Probability</th>
                  <th className="py-3 px-4 text-center">Predicted Churn</th>
                  <th className="py-3 px-4 text-right">Tenure</th>
                  <th className="py-3 px-4 text-right">Monthly</th>
                  <th className="py-3 px-4">Contract</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
                {customers.map((c) => {
                  const probPct = (c.churn_probability * 100).toFixed(2);
                  const isVeryHigh = c.risk_category === 'Very High Risk';
                  const isHigh = c.risk_category === 'High Risk';
                  const isMed = c.risk_category === 'Medium Risk';

                  return (
                    <tr
                      key={c.customerID}
                      onClick={() => onSelectCustomer(c.customerID)}
                      className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                    >
                      <td className="py-3 px-4 font-sans text-slate-400">#{c.rank}</td>
                      <td className="py-3 px-4 font-semibold text-slate-100">{c.customerID}</td>
                      <td className="py-3 px-4 font-sans">
                        <span
                          className={`inline-block px-2 py-0.5 rounded-md text-2xs font-semibold border ${
                            isVeryHigh
                              ? 'bg-rose-500/15 text-rose-400 border-rose-500/30'
                              : isHigh
                              ? 'bg-orange-500/15 text-orange-400 border-orange-500/30'
                              : isMed
                              ? 'bg-amber-500/15 text-amber-400 border-amber-500/30'
                              : 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                          }`}
                        >
                          {c.risk_category}
                        </span>
                      </td>
                      <td
                        className={`py-3 px-4 text-right font-semibold ${
                          c.churn_probability >= 0.50 ? 'text-rose-400' : 'text-slate-300'
                        }`}
                      >
                        {probPct}%
                      </td>
                      <td className="py-3 px-4 text-center font-sans">
                        {c.predicted_churn ? (
                          <span className="px-2 py-0.5 rounded text-2xs bg-rose-500/10 text-rose-400 font-semibold border border-rose-500/20">
                            Yes
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-2xs bg-slate-800 text-slate-400 font-medium">
                            No
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-right font-sans text-slate-300">{c.tenure} mo</td>
                      <td className="py-3 px-4 text-right font-sans text-slate-300">${c.MonthlyCharges.toFixed(2)}</td>
                      <td className="py-3 px-4 font-sans text-slate-300">{c.Contract}</td>
                      <td className="py-3 px-4 text-right font-sans" onClick={(e) => e.stopPropagation()}>
                        <button
                          onClick={() => onSelectCustomer(c.customerID)}
                          className="text-xs text-indigo-400 hover:text-indigo-300 font-medium px-2.5 py-1 rounded bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 transition-all flex items-center space-x-1 ml-auto"
                        >
                          <Eye className="w-3 h-3" />
                          <span>Review</span>
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Footer */}
        <div className="p-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <span>
            Page <strong className="text-slate-200">{pagination.page}</strong> of{' '}
            <strong className="text-slate-200">{pagination.total_pages}</strong>
          </span>

          <div className="flex items-center space-x-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage(page - 1)}
              className="p-1.5 rounded-lg bg-slate-800 border border-slate-700/60 hover:bg-slate-700/80 disabled:opacity-40 disabled:cursor-not-allowed text-slate-300 transition-all"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={page >= pagination.total_pages}
              onClick={() => setPage(page + 1)}
              className="p-1.5 rounded-lg bg-slate-800 border border-slate-700/60 hover:bg-slate-700/80 disabled:opacity-40 disabled:cursor-not-allowed text-slate-300 transition-all"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

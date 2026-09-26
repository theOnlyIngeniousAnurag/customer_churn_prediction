import React from 'react';
import { LayoutDashboard, Users, BarChart3, BrainCircuit, ShieldAlert } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  highRiskCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, highRiskCount }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'customers', label: 'Customers', icon: Users },
    { id: 'risk_analysis', label: 'Risk Analysis', icon: BarChart3 },
    { id: 'model_insights', label: 'Model Insights', icon: BrainCircuit },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 h-screen sticky top-0 text-slate-300">
      <div>
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-800/80">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-bold shadow-sm">
              CI
            </div>
            <div>
              <h1 className="font-semibold text-slate-100 text-base leading-tight">Churn Intelligence</h1>
              <p className="text-xs text-slate-400 mt-0.5">Risk & Retention Analytics</p>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-1 mt-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-indigo-600/15 text-indigo-300 border border-indigo-500/20 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.id === 'customers' && highRiskCount > 0 && (
                  <span className="px-1.5 py-0.5 text-xs font-semibold bg-rose-500/15 text-rose-400 rounded-full border border-rose-500/20">
                    {highRiskCount}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Model Status Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-950/40">
        <div className="flex items-center space-x-2 text-xs text-slate-400 mb-1.5">
          <ShieldAlert className="w-3.5 h-3.5 text-emerald-400" />
          <span className="font-medium text-slate-300">Model Pipeline</span>
        </div>
        <div className="bg-slate-800/60 rounded-md p-2.5 border border-slate-700/50 space-y-1">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Model:</span>
            <span className="font-semibold text-slate-200">Random Forest</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Status:</span>
            <span className="text-emerald-400 font-medium">v1 / Validated</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Scored:</span>
            <span className="text-slate-300">7,043 Accounts</span>
          </div>
        </div>
      </div>
    </aside>
  );
};

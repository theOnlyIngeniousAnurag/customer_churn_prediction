import React from 'react';

interface HeaderProps {
  activeTab: string;
}

export const Header: React.FC<HeaderProps> = ({ activeTab }) => {
  const titles: Record<string, { title: string; subtitle: string }> = {
    overview: {
      title: 'Customer Risk Overview',
      subtitle: 'A clear view of churn exposure across the current customer portfolio.',
    },
    customers: {
      title: 'Customer Explorer & Risk Ranking',
      subtitle: 'Search, filter, and inspect risk profiles for individual accounts.',
    },
    risk_analysis: {
      title: 'Risk Distribution & Exposure Analysis',
      subtitle: 'Population-level probability distribution and segment characteristics.',
    },
    model_insights: {
      title: 'Model Architecture & Insights',
      subtitle: 'Holdout test performance, confusion matrix, and feature importances.',
    },
  };

  const current = titles[activeTab] || titles.overview;

  return (
    <header className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 px-8 py-4 flex items-center justify-between sticky top-0 z-10">
      <div>
        <h2 className="text-xl font-bold text-slate-100 tracking-tight">{current.title}</h2>
        <p className="text-xs text-slate-400 mt-0.5">{current.subtitle}</p>
      </div>

      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700/60 text-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="text-slate-300 font-medium">Model: Random Forest</span>
          <span className="text-slate-500">•</span>
          <span className="text-emerald-400 font-medium">Validated</span>
        </div>
      </div>
    </header>
  );
};

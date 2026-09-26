import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { OverviewView } from './components/OverviewView';
import { CustomersView } from './components/CustomersView';
import { RiskAnalysisView } from './components/RiskAnalysisView';
import { ModelInsightsView } from './components/ModelInsightsView';
import { CustomerDetailDrawer } from './components/CustomerDetailDrawer';

export default function App() {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [selectedCustomerId, setSelectedCustomerId] = useState<string | null>(null);
  const [overviewData, setOverviewData] = useState<any | null>(null);

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        const res = await fetch('/api/overview');
        if (res.ok) {
          const data = await res.json();
          setOverviewData(data);
        }
      } catch (err) {
        console.error('Failed to fetch overview data:', err);
      }
    };

    fetchOverview();
  }, []);

  const handleSelectCustomer = (id: string) => {
    setSelectedCustomerId(id);
  };

  const handleCloseDrawer = () => {
    setSelectedCustomerId(null);
  };

  return (
    <div className="flex min-h-screen bg-slate-950 font-sans text-slate-100 antialiased selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        highRiskCount={overviewData?.high_risk_or_very_high_risk_count || 1362}
      />

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header activeTab={activeTab} />

        <main className="flex-1 pb-16">
          {activeTab === 'overview' && (
            <OverviewView
              overviewData={overviewData}
              onSelectCustomer={handleSelectCustomer}
              onNavigateToCustomers={() => setActiveTab('customers')}
            />
          )}

          {activeTab === 'customers' && (
            <CustomersView onSelectCustomer={handleSelectCustomer} />
          )}

          {activeTab === 'risk_analysis' && <RiskAnalysisView />}

          {activeTab === 'model_insights' && <ModelInsightsView />}
        </main>
      </div>

      {/* Customer Detail Profile Slide-Over Drawer */}
      <CustomerDetailDrawer
        customerID={selectedCustomerId}
        onClose={handleCloseDrawer}
      />
    </div>
  );
}

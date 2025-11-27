import React, { useState, useEffect } from 'react';
import CategoryManager from './CategoryManager';
import ProposalForm from './ProposalForm';
import ProposalsList from './ProposalsList';
import ContractUpload from './ContractUpload';
import Dashboard from './Dashboard';
import HistoryView from './HistoryView';
import Login from './Login';
import Sidebar from './Sidebar';
import RoleGuard from './RoleGuard';
import { UserProvider, useUser } from './UserContext';
import './App.css';
import './theme.css';

const Header = () => {
  const { user, logout } = useUser();
  
  return (
    <header className="app-header">
      <div className="header-content">
        <div className="header-left">
          <h1>Government Spending Tracker</h1>
        </div>
        {user && (
          <div className="header-actions">
            <span style={{ marginRight: '15px', color: '#666', fontSize: '14px' }}>
              {user.username} ({user.role})
            </span>
            <button className="btn btn-secondary btn-small" onClick={logout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

function AppContent() {
  const [proposalRefreshKey, setProposalRefreshKey] = useState(0);
  const { user, loading } = useUser();
  
  // Set default tab based on user role
  const getDefaultTab = (userRole) => {
    if (userRole === 'finance') {
      return 'dashboard';
    } else if (userRole === 'ministry') {
      return 'proposals';
    }
    return 'dashboard'; // fallback
  };
  
  const [activeTab, setActiveTab] = useState(() => getDefaultTab(user?.role));

  // Update activeTab when user changes
  useEffect(() => {
    if (user) {
      const defaultTab = getDefaultTab(user.role);
      setActiveTab(defaultTab);
    }
  }, [user]);

  const handleProposalCreated = () => {
    setProposalRefreshKey(prevKey => prevKey + 1);
  };

    const renderContent = () => {
    // Additional security check - redirect unauthorized users
    if (activeTab === 'dashboard' && user?.role !== 'finance') {
      setActiveTab('proposals'); // Redirect ministry users to proposals
      return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
    }
    if (activeTab === 'categories' && user?.role !== 'finance') {
      setActiveTab('proposals'); // Redirect ministry users to proposals
      return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
    }
    if ((activeTab === 'create-proposal' || activeTab === 'upload-contract') && user?.role !== 'ministry') {
      setActiveTab('dashboard'); // Redirect finance users to dashboard
      return (
        <RoleGuard allowedRoles={['finance']}>
          <Dashboard key={`dashboard-${proposalRefreshKey}`} />
        </RoleGuard>
      );
    }
    
    switch (activeTab) {
      case 'dashboard':
        return (
          <RoleGuard allowedRoles={['finance']}>
            <Dashboard key={`dashboard-${proposalRefreshKey}`} />
          </RoleGuard>
        );
      case 'categories':
        return (
          <RoleGuard allowedRoles={['finance']}>
            <CategoryManager />
          </RoleGuard>
        );
      case 'proposals':
        return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
      case 'create-proposal':
        return (
          <RoleGuard allowedRoles={['ministry']}>
            <ProposalForm onCreated={handleProposalCreated} />
          </RoleGuard>
        );
      case 'upload-contract':
        return (
          <RoleGuard allowedRoles={['ministry']}>
            <ContractUpload onProposalsCreated={handleProposalCreated} />
          </RoleGuard>
        );
      case 'history':
        return <HistoryView />;
      default:
        // Default based on user role
        const defaultTab = getDefaultTab(user?.role);
        if (defaultTab === 'dashboard') {
          return (
            <RoleGuard allowedRoles={['finance']}>
              <Dashboard key={`dashboard-${proposalRefreshKey}`} />
            </RoleGuard>
          );
        } else {
          return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
        }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <span>Loading application...</span>
      </div>
    );
  }

  if (!user) {
    return <Login />;
  }

  return (
    <div className="App">
      <Header />
      <div className="app-layout">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="main-content">
          <div className="content-container">
            {renderContent()}
          </div>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <UserProvider>
      <AppContent />
    </UserProvider>
  );
}

export default App;

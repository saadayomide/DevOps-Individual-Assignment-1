import React, { useState } from 'react';
import CategoryManager from './CategoryManager';
import ProposalForm from './ProposalForm';
import ProposalsList from './ProposalsList';
import ContractUpload from './ContractUpload';
import Dashboard from './Dashboard';
import './App.css';

function App() {
  const [proposalRefreshKey, setProposalRefreshKey] = useState(0);

  const handleProposalCreated = () => {
    setProposalRefreshKey(prev => prev + 1);
  };

  return (
    <div className="App">
      <CategoryManager />
      <ProposalForm onCreated={handleProposalCreated} />
      <ProposalsList key={proposalRefreshKey} />
      <Dashboard refreshKey={proposalRefreshKey} />
      <ContractUpload onCreated={handleProposalCreated} />
    </div>
  );
}

export default App;

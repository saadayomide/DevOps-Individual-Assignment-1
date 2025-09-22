import React from 'react';
import CategoryManager from './CategoryManager';
import ProposalForm from './ProposalForm';
import ProposalsList from './ProposalsList';
import './App.css';

function App() {
  return (
    <div className="App">
      <CategoryManager />
      <ProposalForm onCreated={() => {}} />
      <ProposalsList />
    </div>
  );
}

export default App;

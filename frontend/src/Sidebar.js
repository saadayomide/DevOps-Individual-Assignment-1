import React from 'react';
import { useUser } from './UserContext';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const { user } = useUser();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      description: 'Financial Overview',
      roles: ['finance']
    },
    {
      id: 'categories',
      label: 'Categories',
      description: 'Budget Categories',
      roles: ['finance']
    },
    {
      id: 'proposals',
      label: 'Proposals',
      description: 'All Proposals',
      roles: ['finance', 'ministry']
    },
    {
      id: 'create-proposal',
      label: 'Create Proposal',
      description: 'New Proposal',
      roles: ['ministry']
    },
    {
      id: 'upload-contract',
      label: 'Upload Contract',
      description: 'Contract Upload',
      roles: ['ministry']
    },
    {
      id: 'history',
      label: 'History',
      description: 'Transaction History',
      roles: ['finance', 'ministry']
    }
  ];

  const filteredItems = navigationItems.filter(item => 
    item.roles.includes(user?.role)
  );

    const handleItemClick = (itemId) => {
    // Prevent ministry users from accessing finance-only features
    if (itemId === 'dashboard' && user?.role !== 'finance') {
      return; // Don't allow access
    }
    if (itemId === 'categories' && user?.role !== 'finance') {
      return; // Don't allow access
    }
    if ((itemId === 'create-proposal' || itemId === 'upload-contract') && user?.role !== 'ministry') {
      return; // Don't allow access
    }
    
    setActiveTab(itemId);
  };

  // Group items by role for better organization
  const financeItems = filteredItems.filter(item => item.roles.includes('finance') && !item.roles.includes('ministry'));
  const ministryItems = filteredItems.filter(item => item.roles.includes('ministry') && !item.roles.includes('finance'));
  const commonItems = filteredItems.filter(item => item.roles.includes('finance') && item.roles.includes('ministry'));

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-user-info">
          <div className="sidebar-user-name">{user?.username}</div>
          <div className="sidebar-user-role">{user?.role === 'finance' ? 'Finance Department' : 'Ministry User'}</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {financeItems.length > 0 && (
          <div className="sidebar-section">
            <div className="sidebar-section-title">Finance</div>
            {financeItems.map((item) => (
            <button
              key={item.id}
                className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => handleItemClick(item.id)}
              title={item.description}
            >
                <span className="sidebar-item-label">{item.label}</span>
                <span className="sidebar-item-desc">{item.description}</span>
              </button>
            ))}
              </div>
        )}
        
        {ministryItems.length > 0 && (
          <div className="sidebar-section">
            <div className="sidebar-section-title">Ministry</div>
            {ministryItems.map((item) => (
              <button
                key={item.id}
                className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => handleItemClick(item.id)}
                title={item.description}
              >
                <span className="sidebar-item-label">{item.label}</span>
                <span className="sidebar-item-desc">{item.description}</span>
            </button>
          ))}
        </div>
        )}
        
        {commonItems.length > 0 && (
          <div className="sidebar-section">
            <div className="sidebar-section-title">General</div>
            {commonItems.map((item) => (
              <button
                key={item.id}
                className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => handleItemClick(item.id)}
                title={item.description}
              >
                <span className="sidebar-item-label">{item.label}</span>
                <span className="sidebar-item-desc">{item.description}</span>
              </button>
            ))}
          </div>
        )}
      </nav>
    </div>
  );
};

export default Sidebar;

import React from 'react';
import { useUser } from './UserContext';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const { user } = useUser();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: '📊',
      description: 'Financial Overview',
      roles: ['finance']
    },
    {
      id: 'categories',
      label: 'Categories',
      icon: '📁',
      description: 'Budget Categories',
      roles: ['finance']
    },
    {
      id: 'proposals',
      label: 'Proposals',
      icon: '📋',
      description: 'All Proposals',
      roles: ['finance', 'ministry']
    },
    {
      id: 'create-proposal',
      label: 'Create Proposal',
      icon: '➕',
      description: 'New Proposal',
      roles: ['ministry']
    },
    {
      id: 'upload-contract',
      label: 'Upload Contract',
      icon: '📄',
      description: 'Contract Upload',
      roles: ['ministry']
    },
    {
      id: 'history',
      label: 'History',
      icon: '📜',
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

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-icon">🏛️</span>
          <div className="logo-text">
            <h3>GovTracker</h3>
            <p>Spending Portal</p>
          </div>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <div className="nav-section">
          <h4 className="nav-section-title">Navigation</h4>
          {filteredItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => handleItemClick(item.id)}
              title={item.description}
            >
              <span className="nav-icon">{item.icon}</span>
              <div className="nav-content">
                <span className="nav-label">{item.label}</span>
                <span className="nav-description">{item.description}</span>
              </div>
              {activeTab === item.id && (
                <div className="nav-indicator"></div>
              )}
            </button>
          ))}
        </div>
        
        <div className="nav-section">
          <h4 className="nav-section-title">User Info</h4>
          <div className="user-card">
            <div className="user-avatar">
              <span>{user?.role === 'finance' ? '💰' : '🏢'}</span>
            </div>
            <div className="user-details">
              <span className="user-name">{user?.username}</span>
              <span className="user-role">{user?.role === 'finance' ? 'Finance Ministry' : 'Ministry User'}</span>
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;

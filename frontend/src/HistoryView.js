import React, { useEffect, useState, useCallback } from 'react';
import { historyAPI, categoryAPI } from './api';

const HistoryView = () => {
  const [proposals, setProposals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ 
    ministry: '', 
    category_id: '', 
    status: '', 
    date_from: '', 
    date_to: '' 
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
    totalRequested: 0,
    totalApproved: 0
  });

  const cleanFilters = (f) => Object.fromEntries(Object.entries(f).filter(([_, v]) => v !== '' && v != null));

  const loadHistory = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await historyAPI.list(cleanFilters(filters));
      setProposals(data);
      
      // Calculate stats
      const stats = {
        total: data.length,
        pending: data.filter(p => p.status === 'Pending').length,
        approved: data.filter(p => p.status === 'Approved').length,
        rejected: data.filter(p => p.status === 'Rejected').length,
        totalRequested: data.reduce((sum, p) => sum + (p.requested_amount || 0), 0),
        totalApproved: data.reduce((sum, p) => sum + (p.approved_amount || 0), 0)
      };
      setStats(stats);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load proposal history');
      console.error('History loading error:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const loadCategories = useCallback(async () => {
    try {
      const data = await categoryAPI.getAll();
      setCategories(data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  }, []);

  useEffect(() => {
    loadHistory();
    loadCategories();
  }, [loadHistory, loadCategories]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const applyFilters = () => {
    loadHistory();
  };

  const clearFilters = () => {
    setFilters({ ministry: '', category_id: '', status: '', date_from: '', date_to: '' });
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'Pending': { icon: '⏳', class: 'status-pending', color: '#f59e0b' },
      'Approved': { icon: '✅', class: 'status-approved', color: '#10b981' },
      'Rejected': { icon: '❌', class: 'status-rejected', color: '#ef4444' }
    };
    
    const config = statusConfig[status] || { icon: '❓', class: 'status-unknown', color: '#6b7280' };
    
    return (
      <span className={`status-badge ${config.class}`} style={{ backgroundColor: `${config.color}20`, color: config.color }}>
        <span className="status-icon">{config.icon}</span>
        {status}
      </span>
    );
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD', 
      minimumFractionDigits: 0 
    }).format(amount || 0);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="card history-card">
      <div className="card-header">
        <h2>📜 Proposal History</h2>
        <p>Complete transaction history and approval records</p>
      </div>

      {/* Statistics Cards */}
      <div className="history-stats">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Total Proposals</h3>
            <p>{stats.total}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <h3>Pending</h3>
            <p>{stats.pending}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Approved</h3>
            <p>{stats.approved}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">❌</div>
          <div className="stat-content">
            <h3>Rejected</h3>
            <p>{stats.rejected}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>Total Requested</h3>
            <p>{formatCurrency(stats.totalRequested)}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Total Approved</h3>
            <p>{formatCurrency(stats.totalApproved)}</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <h3>🔍 Filters</h3>
        <div className="filters-grid">
          <div className="form-group">
            <label htmlFor="ministry">Ministry</label>
            <input
              type="text"
              id="ministry"
              name="ministry"
              value={filters.ministry}
              onChange={handleFilterChange}
              placeholder="Filter by ministry"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="status">Status</label>
            <select name="status" value={filters.status} onChange={handleFilterChange}>
              <option value="">All Statuses</option>
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="category_id">Category</label>
            <select name="category_id" value={filters.category_id} onChange={handleFilterChange}>
              <option value="">All Categories</option>
              {categories.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="date_from">Date From</label>
            <input
              type="date"
              id="date_from"
              name="date_from"
              value={filters.date_from}
              onChange={handleFilterChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="date_to">Date To</label>
            <input
              type="date"
              id="date_to"
              name="date_to"
              value={filters.date_to}
              onChange={handleFilterChange}
            />
          </div>
        </div>
        
        <div className="filter-actions">
          <button 
            className="btn btn-primary" 
            onClick={applyFilters} 
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Loading...
              </>
            ) : (
              <>
                <span>🔍</span>
                Apply Filters
              </>
            )}
          </button>
          <button className="btn btn-secondary" onClick={clearFilters}>
            <span>🔄</span>
            Clear Filters
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <span>⚠️</span> {error}
        </div>
      )}

      {/* Proposals Table */}
      <div className="table-section">
        <div className="table-header">
          <h3>📋 Proposal Records</h3>
          <div className="table-actions">
            <button className="btn btn-secondary btn-small">
              <span>📊</span>
              Export CSV
            </button>
          </div>
        </div>

        {loading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
            <span>Loading proposal history...</span>
          </div>
        ) : proposals.length === 0 ? (
          <div className="no-data">
            <div className="no-data-icon">📭</div>
            <h3>No Proposals Found</h3>
            <p>No proposals match your current filters. Try adjusting your search criteria.</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="proposals-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Ministry</th>
                  <th>Category</th>
                  <th>Title</th>
                  <th>Requested</th>
                  <th>Status</th>
                  <th>Approved</th>
                  <th>Decided At</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {proposals.map(proposal => (
                  <tr key={proposal.id}>
                    <td>
                      <span className="proposal-id">#{proposal.id}</span>
                    </td>
                    <td>
                      <span className="ministry-name">{proposal.ministry}</span>
                    </td>
                    <td>
                      <span className="category-name">
                        {categories.find(c => c.id === proposal.category_id)?.name || 'Unknown'}
                      </span>
                    </td>
                    <td>
                      <span className="proposal-title" title={proposal.title}>
                        {proposal.title}
                      </span>
                    </td>
                    <td>
                      <span className="amount requested">{formatCurrency(proposal.requested_amount)}</span>
                    </td>
                    <td>{getStatusBadge(proposal.status)}</td>
                    <td>
                      <span className="amount approved">
                        {proposal.approved_amount ? formatCurrency(proposal.approved_amount) : '-'}
                      </span>
                    </td>
                    <td>
                      <span className="date">{formatDate(proposal.decided_at)}</span>
                    </td>
                    <td>
                      <span className="date">{formatDate(proposal.created_at)}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryView;

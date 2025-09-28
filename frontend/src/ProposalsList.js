import React, { useEffect, useState } from 'react';
import { proposalAPI, categoryAPI } from './api';
import ApprovalDialog from './ApprovalDialog';
import { useUser } from './UserContext';

const ProposalsList = () => {
  const [proposals, setProposals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ ministry: '', status: '', category_id: '' });
  const [error, setError] = useState(null);
  const [selectedProposal, setSelectedProposal] = useState(null);
  const { user } = useUser();
  const [deletingId, setDeletingId] = useState(null);

  const load = async () => {
    try {
      const params = {};
      if (filters.ministry) params.ministry = filters.ministry;
      if (filters.status) params.status = filters.status;
      if (filters.category_id) params.category_id = filters.category_id;
      const data = await proposalAPI.getAll(params);
      setProposals(data);
      setError(null);
    } catch (e) {
      // Handle different error formats
      let errorMessage = 'Failed to load proposals';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const loadCategories = async () => {
    try { 
      const data = await categoryAPI.getAll();
      setCategories(data);
    } catch(e) {
      // ignore category loading errors
    }
  }
  const handleApprove = async (proposalId, data) => {
    try {
      await proposalAPI.approve(proposalId, data);
      setSelectedProposal(null);
      load(); // Reload proposals
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to approve proposal';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const handleReject = async (proposalId, data) => {
    try {
      await proposalAPI.reject(proposalId, data);
      setSelectedProposal(null);
      load(); // Reload proposals
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to reject proposal';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const handleDelete = async (proposal) => {
    if (proposal.status !== 'Pending') {
      alert('Only pending proposals can be deleted.');
      return;
    }
    const reason = window.prompt('Please provide a reason for deleting this proposal:');
    if (!reason || !reason.trim()) {
      return; // require a reason
    }
    try {
      setDeletingId(proposal.id);
      await proposalAPI.delete(proposal.id, { reason });
      await load();
    } catch (e) {
      let errorMessage = 'Failed to delete proposal';
      if (e?.response?.data) {
        const errorData = e.response.data;
        if (typeof errorData.detail === 'string') errorMessage = errorData.detail;
        else if (typeof errorData === 'string') errorMessage = errorData;
      }
      setError(errorMessage);
    } finally {
      setDeletingId(null);
    }
  };


  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
    load();
    loadCategories();
  }, []);

  const onChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const onApplyFilters = () => {
    load();
  };

  const onClearFilters = () => {
    setFilters({ ministry: '', status: '', category_id: '' });
    load();
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
    <>
      <div className="card">
        <h2>Proposals</h2>
        {error && <div className="error-message">{error}</div>}

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
                onChange={onChange}
                placeholder="Filter by ministry"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="status">Status</label>
              <select name="status" value={filters.status} onChange={onChange}>
                <option value="">All Statuses</option>
                <option value="Pending">Pending</option>
                <option value="Approved">Approved</option>
                <option value="Rejected">Rejected</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="category_id">Category</label>
              <select name="category_id" value={filters.category_id} onChange={onChange}>
                <option value="">All Categories</option>
                {categories.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
          </div>
          
          <div className="filter-actions">
            <button className="btn btn-primary" onClick={onApplyFilters}>
              <span>🔍</span>
              Apply Filters
            </button>
            <button className="btn btn-secondary" onClick={onClearFilters}>
              <span>🔄</span>
              Clear Filters
            </button>
          </div>
        </div>

        <div className="table-section">
          <div className="table-header">
            <h3>📋 All Proposals</h3>
          </div>

          {proposals.length === 0 ? (
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
                    <th>Actions</th>
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
                      <td>
                        {proposal.status === 'Pending' && user?.role === 'finance' && (
                          <button 
                            className="btn btn-small btn-primary"
                            onClick={() => setSelectedProposal(proposal)}
                          >
                            Review
                          </button>
                        )}
                        {proposal.status === 'Pending' && user?.role === 'ministry' && (
                          <button
                            className="btn btn-small btn-danger"
                            disabled={deletingId === proposal.id}
                            onClick={() => handleDelete(proposal)}
                          >
                            {deletingId === proposal.id ? 'Deleting…' : 'Delete'}
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

                  {selectedProposal && (
        <ApprovalDialog
          proposal={selectedProposal}
          categories={categories}
          onApprove={handleApprove}
          onReject={handleReject}
          onClose={() => setSelectedProposal(null)}
        />
      )}
    </>
  );
};

export default ProposalsList;

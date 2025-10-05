import React, { useEffect, useState } from 'react';
import { proposalAPI, categoryAPI } from './api';
import ApprovalDialog from './ApprovalDialog';
import EditProposalDialog from './EditProposalDialog';
import { useUser } from './UserContext';

const ProposalsList = () => {
  const [proposals, setProposals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ category_id: '', min_amount: '', max_amount: '' });
  const [error, setError] = useState(null);
  const [selectedProposal, setSelectedProposal] = useState(null);
  const { user } = useUser();
  const [deletingId, setDeletingId] = useState(null);
  const [editingProposal, setEditingProposal] = useState(null);

  const load = async () => {
    try {
      const params = { status: 'Pending' }; // Always filter for pending proposals
      if (filters.category_id) params.category_id = filters.category_id;
      if (filters.min_amount) params.min_amount = parseFloat(filters.min_amount);
      if (filters.max_amount) params.max_amount = parseFloat(filters.max_amount);
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
    setFilters({ category_id: '', min_amount: '', max_amount: '' });
    load();
  };

  // Edit validation logic
  const canEditProposal = (proposal) => {
    if (!user || user.role !== 'ministry') return false;
    if (proposal.status !== 'Pending') return false;
    
    // Check ministry match
    if (user.ministry !== proposal.ministry) return false;
    
    return true;
  };

  const handleEdit = (proposal) => {
    setEditingProposal(proposal);
  };

  const handleEditSubmit = async (formData) => {
    try {
      await proposalAPI.update(editingProposal.id, formData);
      setEditingProposal(null);
      load(); // Reload proposals
    } catch (err) {
      let errorMessage = 'Failed to update proposal';
      if (err?.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      }
      setError(errorMessage);
    }
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
        <h2>Pending Proposals</h2>
        <p className="page-description">Review and manage pending budget proposals</p>
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
              <label htmlFor="min_amount">Min Amount</label>
              <input
                type="text"
                id="min_amount"
                name="min_amount"
                value={filters.min_amount}
                onChange={onChange}
                placeholder="e.g., 100000"
                pattern="[0-9]*"
                inputMode="numeric"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="max_amount">Max Amount</label>
              <input
                type="text"
                id="max_amount"
                name="max_amount"
                value={filters.max_amount}
                onChange={onChange}
                placeholder="e.g., 5000000"
                pattern="[0-9]*"
                inputMode="numeric"
              />
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
                        <span className="ministry-name">{proposal.ministry?.name || 'Unknown'}</span>
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
                          <div className="action-buttons">
                            {canEditProposal(proposal) && (
                              <button
                                className="btn btn-small btn-secondary"
                                onClick={() => handleEdit(proposal)}
                              >
                                Edit
                              </button>
                            )}
                            <button
                              className="btn btn-small btn-danger"
                              disabled={deletingId === proposal.id}
                              onClick={() => handleDelete(proposal)}
                            >
                              {deletingId === proposal.id ? 'Deleting…' : 'Delete'}
                            </button>
                          </div>
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

      {editingProposal && (
        <EditProposalDialog
          proposal={editingProposal}
          categories={categories}
          onSubmit={handleEditSubmit}
          onClose={() => setEditingProposal(null)}
        />
      )}
    </>
  );
};

export default ProposalsList;

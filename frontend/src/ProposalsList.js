import React, { useEffect, useState } from 'react';
import { proposalAPI, categoryAPI } from './api';
import ApprovalDialog from './ApprovalDialog';

const ProposalsList = () => {
  const [proposals, setProposals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ ministry: '', status: '', category_id: '' });
  const [error, setError] = useState(null);
  const [selectedProposal, setSelectedProposal] = useState(null);

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
      setError('Failed to load proposals');
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
    load();
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await categoryAPI.getAll();
      setCategories(data);
    } catch (e) {
      // ignore
    }
  };

  const onFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const onApplyFilters = () => load();

  const handleApprove = async (proposalId, data) => {
    try {
      await proposalAPI.approve(proposalId, data);
      load();
      loadCategories();
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to approve proposal');
    }
  };

  const handleReject = async (proposalId, data) => {
    try {
      await proposalAPI.reject(proposalId, data);
      load();
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to reject proposal');
    }
  };

  return (
    <>
      <div className="categories-table" style={{ marginTop: 20 }}>
        <h3>Proposals</h3>
        {error && <div className="error">{error}</div>}

        <div className="form-container" style={{ margin: 0, marginBottom: 20 }}>
          <div className="form-group">
            <label>Ministry</label>
            <input name="ministry" value={filters.ministry} onChange={onFilterChange} placeholder="Filter by ministry" />
          </div>
          <div className="form-group">
            <label>Status</label>
            <select name="status" value={filters.status} onChange={onFilterChange}>
              <option value="">All</option>
              <option value="Pending">Pending</option>
              <option value="Approved" disabled>Approved (Phase 3)</option>
              <option value="Rejected" disabled>Rejected (Phase 3)</option>
            </select>
          </div>
          <div className="form-group">
            <label>Category ID</label>
            <input name="category_id" value={filters.category_id} onChange={onFilterChange} placeholder="e.g., 1" />
          </div>
          <div className="form-actions">
            <button className="btn btn-secondary" onClick={onApplyFilters}>Apply Filters</button>
          </div>
        </div>

        {proposals.length === 0 ? (
          <p className="no-data">No proposals found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Ministry</th>
                <th>Category ID</th>
                <th>Title</th>
                <th>Requested</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {proposals.map(p => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.ministry}</td>
                  <td>{p.category_id}</td>
                  <td>{p.title}</td>
                  <td>{new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(p.requested_amount)}</td>
                  <td>{p.status}</td>
                  <td>{new Date(p.created_at).toLocaleString()}</td>
                  <td>
                    {p.status === 'Pending' && (
                      <button 
                        className="btn btn-small btn-primary"
                        onClick={() => setSelectedProposal(p)}
                      >
                        Decide
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
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

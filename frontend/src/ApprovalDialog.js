import React, { useState } from 'react';

const ApprovalDialog = ({ proposal, categories, onApprove, onReject, onClose }) => {
  const [showApprove, setShowApprove] = useState(false);
  const [showReject, setShowReject] = useState(false);
  const [approvedAmount, setApprovedAmount] = useState('');
  const [decisionNotes, setDecisionNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const category = categories && Array.isArray(categories) 
    ? categories.find(c => c.id === proposal.category_id)
    : null;
  const maxAmount = Math.min(proposal.requested_amount, category?.remaining_budget || 0);

  const handleApprove = async () => {
    const amount = parseFloat(approvedAmount);
    if (isNaN(amount) || amount <= 0 || amount > maxAmount) {
      setError(`Invalid amount. Must be greater than 0 and not exceed $${maxAmount.toLocaleString()}`);
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await onApprove(proposal.id, { approved_amount: amount, decision_notes: decisionNotes || null });
    } catch (err) {
      setError('Failed to approve proposal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    setLoading(true);
    setError('');
    
    try {
      await onReject(proposal.id, { decision_notes: decisionNotes || null });
    } catch (err) {
      setError('Failed to reject proposal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (showApprove) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h3>Approve Proposal</h3>
          <p><strong>{proposal.title}</strong> - {proposal.ministry?.name || 'Unknown'}</p>
          <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
          <p>Category remaining: ${category?.remaining_budget?.toLocaleString() || 'N/A'}</p>
          
          {error && (
            <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '15px', fontSize: '14px' }}>
              {error}
            </div>
          )}
          
          <div className="form-group">
            <label>Approved Amount (max: ${maxAmount.toLocaleString()})</label>
            <input
              type="number"
              value={approvedAmount}
              onChange={(e) => setApprovedAmount(e.target.value)}
              min="0"
              step="1000"
              placeholder={maxAmount.toString()}
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label>Decision Notes (optional)</label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Reason for approval..."
              rows="3"
              disabled={loading}
            />
          </div>
          
          <div className="form-actions">
            <button 
              className="btn btn-primary" 
              onClick={handleApprove}
              disabled={loading}
            >
              {loading ? 'Approving...' : 'Approve'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => setShowApprove(false)}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (showReject) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h3>Reject Proposal</h3>
          <p><strong>{proposal.title}</strong> - {proposal.ministry?.name || 'Unknown'}</p>
          <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
          
          {error && (
            <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '15px', fontSize: '14px' }}>
              {error}
            </div>
          )}
          
          <div className="form-group">
            <label>Rejection Reason (optional)</label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Reason for rejection..."
              rows="3"
              disabled={loading}
            />
          </div>
          
          <div className="form-actions">
            <button 
              className="btn btn-danger" 
              onClick={handleReject}
              disabled={loading}
            >
              {loading ? 'Rejecting...' : 'Reject'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => setShowReject(false)}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>Decision Required</h3>
        <p><strong>{proposal.title}</strong> - {proposal.ministry}</p>
        <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
        
        <div className="form-actions">
          <button className="btn btn-primary" onClick={() => setShowApprove(true)}>Approve</button>
          <button className="btn btn-danger" onClick={() => setShowReject(true)}>Reject</button>
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ApprovalDialog;

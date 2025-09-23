import React, { useState } from 'react';

const ApprovalDialog = ({ proposal, categories, onApprove, onReject, onClose }) => {
  const [showApprove, setShowApprove] = useState(false);
  const [showReject, setShowReject] = useState(false);
  const [approvedAmount, setApprovedAmount] = useState('');
  const [decisionNotes, setDecisionNotes] = useState('');

  const category = categories.find(c => c.id === proposal.category_id);
  const maxAmount = Math.min(proposal.requested_amount, category?.remaining_budget || 0);

  const handleApprove = () => {
    const amount = parseFloat(approvedAmount);
    if (isNaN(amount) || amount <= 0 || amount > maxAmount) {
      alert(`Invalid amount. Must be greater than 0 and not exceed ${maxAmount.toLocaleString()}`);
      return;
    }
    onApprove(proposal.id, { approved_amount: amount, decision_notes: decisionNotes || null });
    onClose();
  };

  const handleReject = () => {
    onReject(proposal.id, { decision_notes: decisionNotes || null });
    onClose();
  };

  if (showApprove) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h3>Approve Proposal</h3>
          <p><strong>{proposal.title}</strong> - {proposal.ministry}</p>
          <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
          <p>Category remaining: ${category?.remaining_budget.toLocaleString() || 'N/A'}</p>
          
          <div className="form-group">
            <label>Approved Amount (max: ${maxAmount.toLocaleString()})</label>
            <input
              type="number"
              value={approvedAmount}
              onChange={(e) => setApprovedAmount(e.target.value)}
              min="0"
              step="1000"
              placeholder={maxAmount.toString()}
            />
          </div>
          
          <div className="form-group">
            <label>Decision Notes (optional)</label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Reason for approval..."
              rows="3"
            />
          </div>
          
          <div className="form-actions">
            <button className="btn btn-primary" onClick={handleApprove}>Approve</button>
            <button className="btn btn-secondary" onClick={() => setShowApprove(false)}>Cancel</button>
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
          <p><strong>{proposal.title}</strong> - {proposal.ministry}</p>
          <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
          
          <div className="form-group">
            <label>Rejection Reason (optional)</label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Reason for rejection..."
              rows="3"
            />
          </div>
          
          <div className="form-actions">
            <button className="btn btn-danger" onClick={handleReject}>Reject</button>
            <button className="btn btn-secondary" onClick={() => setShowReject(false)}>Cancel</button>
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

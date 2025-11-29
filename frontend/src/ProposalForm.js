import React, { useState, useEffect } from 'react';
import { proposalAPI, categoryAPI, ministryAPI } from './api';
import { useUser } from './UserContext';

const ProposalForm = ({ onCreated }) => {
  const { user } = useUser();
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    category_id: '',
    title: '',
    description: '',
    requested_amount: ''
  });
  const [error, setError] = useState(null);

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    // Client-side validation
    if (!form.title || !form.category_id || !form.requested_amount) {
      setError('Please fill all required fields.');
      return;
    }
    if (!user?.ministry?.id) {
      setError('You must be assigned to a ministry to submit proposals.');
      return;
    }
    const amount = parseFloat(form.requested_amount);
    if (isNaN(amount) || amount <= 0) {
      setError('Requested amount must be a number greater than 0.');
      return;
    }
    try {
      await proposalAPI.create({
        ministry_id: user.ministry.id, // Use the logged-in user's ministry
        category_id: parseInt(form.category_id, 10),
        title: form.title,
        description: form.description || null,
        requested_amount: amount,
      });
      setForm({ category_id: '', title: '', description: '', requested_amount: '' });
      onCreated && onCreated();
    } catch (e) {
      // Handle different error formats
      let errorMessage = 'Failed to submit proposal.';
      
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

  useEffect(() => {
    const reload = async () => {
      try {
        const cats = await categoryAPI.getAll();
        setCategories(cats);
      } catch (e) {
        console.error('Failed to load categories:', e);
      }
    };
    
    reload(); // Load categories immediately
    const handler = () => reload();
    window.addEventListener('categories-updated', handler);
    return () => window.removeEventListener('categories-updated', handler);
  }, []);


  return (
    <div className="card">
      <h2 className="page-title">Submit Proposal</h2>
      <p className="page-description">Create a new budget proposal for approval</p>
      {error && <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '16px', fontSize: '14px' }}>{error}</div>}
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label>Ministry</label>
          <input 
            type="text"
            value={user?.ministry?.name || 'Not assigned to a ministry'} 
            disabled
            style={{ 
              backgroundColor: '#f5f5f5', 
              cursor: 'not-allowed',
              opacity: 0.7
            }}
            title="Your ministry is locked to your account"
          />
          {!user?.ministry?.id && (
            <p style={{ fontSize: '12px', color: '#dc3545', marginTop: '5px' }}>
              You must be assigned to a ministry to submit proposals.
            </p>
          )}
        </div>
        <div className="form-group">
          <label>Category</label>
          <select name="category_id" value={form.category_id} onChange={onChange} required>
            <option value="">Select category</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Title</label>
          <input name="title" value={form.title} onChange={onChange} placeholder="Project title" required />
        </div>
        <div className="form-group">
          <label>Description</label>
          <input name="description" value={form.description} onChange={onChange} placeholder="Optional details" />
        </div>
        <div className="form-group">
          <label>Requested Amount</label>
          <input name="requested_amount" type="number" min="1" value={form.requested_amount} onChange={onChange} required />
        </div>
        <div className="form-actions">
          <button className="btn btn-primary" type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
};

export default ProposalForm;

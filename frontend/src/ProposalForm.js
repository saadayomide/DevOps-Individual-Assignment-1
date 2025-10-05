import React, { useState, useEffect } from 'react';
import { proposalAPI, categoryAPI, ministryAPI } from './api';
import { useUser } from './UserContext';

const ProposalForm = ({ onCreated }) => {
  const { user } = useUser();
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    ministry_name: '',
    category_id: '',
    title: '',
    description: '',
    requested_amount: ''
  });
  const [error, setError] = useState(null);
  const [defaultMinistrySet, setDefaultMinistrySet] = useState(false);

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    // Client-side validation
    if (!form.ministry_name || !form.title || !form.category_id || !form.requested_amount) {
      setError('Please fill all required fields.');
      return;
    }
    const amount = parseFloat(form.requested_amount);
    if (isNaN(amount) || amount <= 0) {
      setError('Requested amount must be a number greater than 0.');
      return;
    }
    try {
      await proposalAPI.create({
        ministry_name: form.ministry_name,
        category_id: parseInt(form.category_id, 10),
        title: form.title,
        description: form.description || null,
        requested_amount: amount,
      });
      setForm({ ministry_name: '', category_id: '', title: '', description: '', requested_amount: '' });
      setDefaultMinistrySet(false); // Reset flag so default ministry can be set again
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

  // Set default ministry name when user loads (only once)
  useEffect(() => {
    if (user?.ministry?.name && !defaultMinistrySet) {
      setForm(prev => ({ ...prev, ministry_name: user.ministry.name }));
      setDefaultMinistrySet(true);
    }
  }, [user, defaultMinistrySet]);

  return (
    <div className="form-container">
      <h3>Submit Proposal</h3>
      {error && <div className="error">{error}</div>}
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label>Ministry</label>
          <input 
            name="ministry_name" 
            value={form.ministry_name} 
            onChange={onChange}
            placeholder={user?.ministry?.name || "Enter ministry name"} 
            required
          />
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

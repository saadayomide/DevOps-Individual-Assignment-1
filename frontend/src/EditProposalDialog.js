import React, { useState } from 'react';

const EditProposalDialog = ({ proposal, categories, onSubmit, onClose }) => {
  const [formData, setFormData] = useState({
    title: proposal.title || '',
    description: proposal.description || '',
    requested_amount: proposal.requested_amount?.toString() || '',
    category_id: proposal.category_id?.toString() || ''
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    const errors = [];
    
    if (!formData.title.trim()) {
      errors.push('Title is required');
    }
    
    if (!formData.requested_amount || parseFloat(formData.requested_amount) <= 0) {
      errors.push('Requested amount must be greater than 0');
    }
    
    if (!formData.category_id) {
      errors.push('Category is required');
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setError(validationErrors.join('; '));
      return;
    }
    
    setLoading(true);
    
    try {
      const submitData = {
        title: formData.title.trim(),
        description: formData.description.trim() || null,
        requested_amount: parseFloat(formData.requested_amount),
        category_id: parseInt(formData.category_id)
      };
      
      await onSubmit(submitData);
    } catch (err) {
      setError(err.message || 'Failed to update proposal');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Edit Proposal #{proposal.id}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows="3"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="requested_amount">Requested Amount *</label>
            <input
              type="text"
              id="requested_amount"
              name="requested_amount"
              value={formData.requested_amount}
              onChange={handleInputChange}
              placeholder="e.g., 1000000"
              pattern="[0-9]*"
              inputMode="numeric"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="category_id">Category *</label>
            <select
              id="category_id"
              name="category_id"
              value={formData.category_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Select Category</option>
              {categories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Updating...' : 'Update Proposal'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditProposalDialog;

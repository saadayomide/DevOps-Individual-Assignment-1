import React, { useState, useEffect } from 'react';
import { categoryAPI } from './api';
import './CategoryManager.css';

const CategoryManager = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    allocated_budget: ''
  });

  // Load categories on component mount
  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const data = await categoryAPI.getAll();
      setCategories(data);
      // notify other parts of the app (e.g., ProposalForm)
      if (typeof window !== "undefined") {
        window.dispatchEvent(new Event("categories-updated"));
      }
      setError(null);
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to load categories';
      
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
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      // Validate name
      if (!formData.name.trim()) {
        setError('Category name is required.');
        return;
      }

      // Validate budget
      const budgetString = (formData.allocated_budget || '').toString().trim();
      if (!budgetString) {
        setError('Allocated budget is required.');
        return;
      }

      const budget = parseFloat(budgetString);
      if (isNaN(budget) || budget <= 0) {
        setError('Allocated budget must be a number greater than 0.');
        return;
      }

      if (editingCategory) {
        await categoryAPI.update(editingCategory.id, {
          name: formData.name,
          allocated_budget: budget
        });
      } else {
        await categoryAPI.create({
          name: formData.name,
          allocated_budget: budget
        });
      }

      setFormData({ name: '', allocated_budget: '' });
      setShowForm(false);
      setEditingCategory(null);
      await loadCategories();
    } catch (err) {
      // Handle different error formats
      let errorMessage = editingCategory ? 'Failed to update category' : 'Failed to create category';
      
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

  const handleEdit = (category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name || '',
      allocated_budget: category.allocated_budget ? category.allocated_budget.toString() : ''
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this category?')) {
      return;
    }

    try {
      await categoryAPI.delete(id);
      await loadCategories();
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to delete category';
      
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

  const handleCancel = () => {
    setFormData({ name: '', allocated_budget: '' });
    setShowForm(false);
    setEditingCategory(null);
    setError(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  if (loading) {
    return (
      <div className="card">
        <h2>Category Management</h2>
        <div className="loading">Loading categories...</div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Category Management</h2>
      {error && <div className="error-message">{error}</div>}

      {!showForm ? (
        <div>
          <div className="form-actions">
            <button 
              className="btn btn-primary" 
              onClick={() => setShowForm(true)}
            >
              Add New Category
            </button>
          </div>

          <table className="categories-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Allocated Budget</th>
                <th>Remaining Budget</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(category => (
                <tr key={category.id}>
                  <td>{category.name}</td>
                  <td>${category.allocated_budget.toLocaleString()}</td>
                  <td>${category.remaining_budget.toLocaleString()}</td>
                  <td>{new Date(category.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      className="btn btn-small btn-secondary" 
                      onClick={() => handleEdit(category)}
                    >
                      Edit
                    </button>
                    <button 
                      className="btn btn-small btn-secondary" 
                      onClick={() => handleDelete(category.id)}
                      style={{ marginLeft: '8px', backgroundColor: '#ef4444', color: 'white' }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Category Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="e.g., Education, Health, Defense"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="allocated_budget">Allocated Budget</label>
            <input
              type="text"
              id="allocated_budget"
              name="allocated_budget"
              value={formData.allocated_budget}
              onChange={handleInputChange}
              placeholder="e.g., 1000000"
              pattern="[0-9]*"
              inputMode="numeric"
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              {editingCategory ? 'Update Category' : 'Create Category'}
            </button>
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={handleCancel}
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default CategoryManager;

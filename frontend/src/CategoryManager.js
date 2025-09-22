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
      setError('Failed to load categories. Make sure the backend server is running.');
      console.error('Error loading categories:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const amount = parseFloat(formData.allocated_budget);
      if (!formData.name || isNaN(amount) || amount < 0) {
        setError('Please provide a name and a non-negative allocated budget.');
        return;
      }
      const categoryData = {
        name: formData.name.trim(),
        allocated_budget: amount
      };

      if (editingCategory) {
        await categoryAPI.update(editingCategory.id, categoryData);
      } else {
        await categoryAPI.create(categoryData);
      }

      // Reset form and reload categories
      setFormData({ name: '', allocated_budget: '' });
      setEditingCategory(null);
      setShowForm(false);
      loadCategories();
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(detail || 'Failed to save category. Please try again.');
      console.error('Error saving category:', err);
    }
  };

  const handleEdit = (category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      allocated_budget: category.allocated_budget.toString()
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this category?')) {
      try {
        await categoryAPI.delete(id);
        loadCategories();
      } catch (err) {
        setError('Failed to delete category. Please try again.');
        console.error('Error deleting category:', err);
      }
    }
  };

  const handleCancel = () => {
    setFormData({ name: '', allocated_budget: '' });
    setEditingCategory(null);
    setShowForm(false);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  if (loading) {
    return <div className="loading">Loading categories...</div>;
  }

  return (
    <div className="category-manager">
      <div className="header">
        <h1>Government Spending Tracker</h1>
        <h2>Budget Categories Management</h2>
        {error && <div className="error">{error}</div>}
      </div>

      <div className="actions">
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(true)}
        >
          Add New Category
        </button>
        <button 
          className="btn btn-secondary"
          onClick={loadCategories}
        >
          Refresh
        </button>
      </div>

      {showForm && (
        <div className="form-container">
          <h3>{editingCategory ? 'Edit Category' : 'Add New Category'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Category Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                placeholder="e.g., Education, Health, Defense"
              />
            </div>
            <div className="form-group">
              <label htmlFor="allocated_budget">Allocated Budget:</label>
              <input
                type="number"
                id="allocated_budget"
                name="allocated_budget"
                value={formData.allocated_budget}
                onChange={handleInputChange}
                required
                min="0"
                step="1000"
                placeholder="e.g., 5000000"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                {editingCategory ? 'Update Category' : 'Create Category'}
              </button>
              <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="categories-table">
        <h3>Budget Categories</h3>
        {categories.length === 0 ? (
          <p className="no-data">No categories found. Create your first category above.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Category Name</th>
                <th>Allocated Budget</th>
                <th>Remaining Budget</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(category => (
                <tr key={category.id}>
                  <td>{category.id}</td>
                  <td>{category.name}</td>
                  <td>{formatCurrency(category.allocated_budget)}</td>
                  <td>{formatCurrency(category.remaining_budget)}</td>
                  <td>{new Date(category.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      className="btn btn-small btn-primary"
                      onClick={() => handleEdit(category)}
                    >
                      Edit
                    </button>
                    <button 
                      className="btn btn-small btn-danger"
                      onClick={() => handleDelete(category.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default CategoryManager;

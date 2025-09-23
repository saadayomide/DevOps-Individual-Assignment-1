import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Category API functions
export const categoryAPI = {
  // Get all categories
  getAll: async () => {
    const response = await api.get('/categories');
    return response.data;
  },

  // Get single category
  getById: async (id) => {
    const response = await api.get(`/categories/${id}`);
    return response.data;
  },

  // Create new category
  create: async (categoryData) => {
    const response = await api.post('/categories', categoryData);
    return response.data;
  },

  // Update category
  update: async (id, categoryData) => {
    const response = await api.put(`/categories/${id}`, categoryData);
    return response.data;
  },

  // Delete category
  delete: async (id) => {
    const response = await api.delete(`/categories/${id}`);
    return response.data;
  },
};




// Proposal API functions
export const proposalAPI = {
  approve: async (id, data) => {
    const response = await api.post(`/proposals/${id}/approve`, data);
    return response.data;
  },
  reject: async (id, data) => {
    const response = await api.post(`/proposals/${id}/reject`, data);
    return response.data;
  },
  getAll: async (params = {}) => {
    const response = await api.get('/proposals', { params });
    return response.data;
  },
  getById: async (id) => {
    const response = await api.get(`/proposals/${id}`);
    return response.data;
  },
  create: async (proposalData) => {
    const response = await api.post('/proposals', proposalData);
    return response.data;
  },
  update: async (id, proposalData) => {
    const response = await api.put(`/proposals/${id}`, proposalData);
    return response.data;
  },
  delete: async (id) => {
    const response = await api.delete(`/proposals/${id}`);
    return response.data;
  },
};

export default api;

// Upload/Parse API
export const uploadAPI = {
  parse: async (file) => {
    const form = new FormData();
    form.append('file', file);
    const response = await api.post('/contracts/parse', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },
};

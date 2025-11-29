import axios from 'axios';

// Read API base URL from environment variable (defaults to localhost for dev)
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Ministry API functions
export const ministryAPI = {
  getAll: async () => {
    const response = await api.get('/ministries');
    return response.data;
  },
  create: async (ministry) => {
    const response = await api.post('/ministries', ministry);
    return response.data;
  },
  findOrCreate: async (ministryName) => {
    const response = await api.post('/ministries/find-or-create', null, {
      params: { ministry_name: ministryName }
    });
    return response.data;
  }
};

// Category API functions
export const categoryAPI = {
  getAll: async () => {
    const response = await api.get('/categories');
    return response.data;
  },
  create: async (category) => {
    const response = await api.post('/categories', category);
    return response.data;
  },
  update: async (id, category) => {
    const response = await api.put(`/categories/${id}`, category);
    return response.data;
  },
  delete: async (id) => {
    await api.delete(`/categories/${id}`);
  }
};

// Proposal API functions
export const proposalAPI = {
  getAll: async (filters = {}) => {
    const query = new URLSearchParams(filters).toString();
    const response = await api.get(`/proposals${query ? `?${query}` : ''}`);
    return response.data;
  },
  create: async (proposal) => {
    const response = await api.post('/proposals', proposal);
    return response.data;
  },
  getById: async (id) => {
    const response = await api.get(`/proposals/${id}`);
    return response.data;
  },
  update: async (id, proposal) => {
    const response = await api.put(`/proposals/${id}`, proposal);
    return response.data;
  },
  delete: async (id, data) => {
    // send reason in body with axios.delete
    const response = await api.delete(`/proposals/${id}`, { data });
    return response.data;
  },
  approve: async (id, data) => {
    const response = await api.post(`/proposals/${id}/approve`, data);
    return response.data;
  },
  reject: async (id, data) => {
    const response = await api.post(`/proposals/${id}/reject`, data);
    return response.data;
  }
};

// Upload API functions
export const uploadAPI = {
  parse: async (file) => {
    const form = new FormData();
    form.append('file', file);
    const response = await api.post('/contracts/parse', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  }
};

// Dashboard API functions
export const dashboardAPI = {
  getSummary: async () => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  }
};

// Auth API functions
export const authAPI = {
  login: async (username, password) => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// History API functions
export const historyAPI = {
  list: async (filters = {}) => {
    const response = await api.get('/proposals', { params: filters });
    return response.data;
  },
};

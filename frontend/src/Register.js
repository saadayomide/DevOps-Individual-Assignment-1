import React, { useState, useEffect } from 'react';
import { authAPI } from './api';
import { ministryAPI } from './api';
import { useUser } from './UserContext';

const Register = ({ onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'ministry',
    ministry_id: ''
  });
  const [ministries, setMinistries] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const { login } = useUser();

  useEffect(() => {
    const loadMinistries = async () => {
      try {
        const data = await ministryAPI.getAll();
        setMinistries(data);
      } catch (err) {
        console.error('Failed to load ministries:', err);
      }
    };
    loadMinistries();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (formData.password.length < 3) {
      setError('Password must be at least 3 characters');
      setLoading(false);
      return;
    }

    if (formData.role === 'ministry' && !formData.ministry_id) {
      setError('Please select a ministry');
      setLoading(false);
      return;
    }

    try {
      const registrationData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: formData.role,
        ministry_id: formData.role === 'ministry' ? parseInt(formData.ministry_id, 10) : null
      };

      await authAPI.register(registrationData);
      setSuccess(true);
      
      // Auto-login after successful registration
      setTimeout(async () => {
        try {
          const response = await authAPI.login(formData.username, formData.password);
          localStorage.setItem('authToken', response.access_token);
          localStorage.setItem('user', JSON.stringify(response.user));
          login(response.user);
        } catch (loginErr) {
          // If auto-login fails, just show success and let user login manually
          console.error('Auto-login failed:', loginErr);
        }
      }, 1000);
    } catch (err) {
      let errorMessage = 'Registration failed';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(e => e.msg || e.message || String(e)).join(', ');
        } else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        } else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        backgroundColor: '#f5f5f5'
      }}>
        <div className="card" style={{ width: '400px', maxWidth: '90%' }}>
          <h2 style={{ marginBottom: '10px', fontSize: '20px', color: '#28a745' }}>Registration Successful!</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>Your account has been created. Logging you in...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      <div className="card" style={{ width: '400px', maxWidth: '90%' }}>
        <h2 style={{ marginBottom: '10px', fontSize: '20px' }}>Create Account</h2>
        <p style={{ color: '#666', marginBottom: '30px', fontSize: '14px' }}>Register for a new account</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              className="form-input"
              value={formData.username}
              onChange={handleChange}
              required
              minLength={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              className="form-input"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              minLength={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="role">Role</label>
            <select
              id="role"
              name="role"
              className="form-input"
              value={formData.role}
              onChange={handleChange}
              required
            >
              <option value="ministry">Ministry</option>
              <option value="finance">Finance</option>
            </select>
          </div>

          {formData.role === 'ministry' && (
            <div className="form-group">
              <label className="form-label" htmlFor="ministry_id">Ministry</label>
              <select
                id="ministry_id"
                name="ministry_id"
                className="form-input"
                value={formData.ministry_id}
                onChange={handleChange}
                required
              >
                <option value="">Select a ministry</option>
                {ministries.map(ministry => (
                  <option key={ministry.id} value={ministry.id}>
                    {ministry.name}
                  </option>
                ))}
              </select>
            </div>
          )}
          
          {error && (
            <div style={{ 
              padding: '10px', 
              backgroundColor: '#f8d7da', 
              color: '#721c24', 
              borderRadius: '4px',
              marginBottom: '15px',
              fontSize: '14px'
            }}>
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ width: '100%', marginTop: '10px' }}
            disabled={loading}
          >
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <button
            type="button"
            onClick={onSwitchToLogin}
            style={{
              background: 'none',
              border: 'none',
              color: '#007bff',
              cursor: 'pointer',
              textDecoration: 'underline',
              fontSize: '14px'
            }}
          >
            Already have an account? Sign in
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;


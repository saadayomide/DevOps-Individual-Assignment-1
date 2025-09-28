import React, { useState } from 'react';
import { authAPI } from './api';
import { useUser } from './UserContext';

const Login = () => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useUser();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(credentials.username, credentials.password);
      localStorage.setItem('authToken', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      login(response.user); // Use the context login function
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Login failed';
      
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

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleQuickLogin = (username, password) => {
    setCredentials({ username, password });
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h2>🏛️ Government Spending Tracker</h2>
          <h3>Secure Access Portal</h3>
          <p>Transparent budget management and proposal tracking</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={credentials.username}
              onChange={handleChange}
              placeholder="Enter your username"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>
          
          {error && (
            <div className="error-message">
              <span>⚠️</span> {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="btn btn-primary login-btn" 
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Authenticating...
              </>
            ) : (
              <>
                <span>🔐</span>
                Sign In
              </>
            )}
          </button>
        </form>
        
        <div className="login-help">
          <h4>🚀 Quick Access</h4>
          <div className="quick-login-buttons">
            <button 
              type="button"
              className="btn btn-secondary quick-btn"
              onClick={() => handleQuickLogin('test', 'test')}
            >
              <span>💰</span>
              Finance User
            </button>
            <button 
              type="button"
              className="btn btn-secondary quick-btn"
              onClick={() => handleQuickLogin('ministry', 'ministry')}
            >
              <span>🏢</span>
              Ministry User
            </button>
          </div>
          <div className="credentials-info">
            <p><strong>Finance:</strong> username: test, password: test</p>
            <p><strong>Ministry:</strong> username: ministry, password: ministry</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

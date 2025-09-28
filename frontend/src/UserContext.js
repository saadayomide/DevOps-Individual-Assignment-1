import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from './api';

const UserContext = createContext();

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('authToken');
      const savedUser = localStorage.getItem('user');
      
      if (token && savedUser) {
        try {
          // Validate the token by calling the /auth/me endpoint
          const currentUser = await authAPI.getMe();
          setUser(currentUser);
        } catch (error) {
          // Token is invalid, clear it
          console.log('Token validation failed, clearing auth data');
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
          setUser(null);
        }
      } else {
        // No saved auth data
        setUser(null);
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  const login = (userData) => {
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  };

  const isFinance = () => user?.role === 'finance';
  const isMinistry = () => user?.role === 'ministry';

  const value = {
    user,
    login,
    logout,
    isFinance,
    isMinistry,
    loading
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

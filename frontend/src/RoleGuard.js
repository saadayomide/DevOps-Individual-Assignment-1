import React from 'react';
import { useUser } from './UserContext';

const RoleGuard = ({ allowedRoles, children, fallback = null }) => {
  const { user } = useUser();
  
  if (!user) {
    return fallback;
  }
  
  if (!allowedRoles.includes(user.role)) {
    return fallback || (
      <div className="card">
        <div className="error-message">
          <span>🚫</span> Access Denied
          <p>You don't have permission to access this feature.</p>
          <p>Required role: {allowedRoles.join(' or ')}</p>
          <p>Your role: {user.role}</p>
        </div>
      </div>
    );
  }
  
  return children;
};

export default RoleGuard;

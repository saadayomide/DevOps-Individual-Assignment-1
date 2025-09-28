// Error handling utility functions

export const extractErrorMessage = (error) => {
  // Handle different error formats
  let errorMessage = 'An error occurred';
  
  if (error?.response?.data) {
    const errorData = error.response.data;
    
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
  } else if (typeof error === 'string') {
    errorMessage = error;
  } else if (error?.message) {
    errorMessage = error.message;
  }
  
  return errorMessage;
};

export const handleApiError = (error, defaultMessage = 'An error occurred') => {
  console.error('API Error:', error);
  return extractErrorMessage(error) || defaultMessage;
};

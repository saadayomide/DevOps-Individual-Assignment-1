import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock('axios', () => {
  const mockResponse = Promise.resolve({ data: {} });
  const mockRequest = jest.fn().mockImplementation(() => mockResponse);

  const mockInstance = {
    get: mockRequest,
    post: mockRequest,
    put: mockRequest,
    delete: mockRequest,
    interceptors: {
      request: { use: jest.fn() },
      response: { use: jest.fn() },
    },
  };

  return {
    __esModule: true,
    default: {
      ...mockInstance,
      create: jest.fn(() => ({ ...mockInstance })),
    },
    create: jest.fn(() => ({ ...mockInstance })),
  };
});

test('renders login heading and button', () => {
  render(<App />);
  expect(screen.getByText(/government spending tracker/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
});

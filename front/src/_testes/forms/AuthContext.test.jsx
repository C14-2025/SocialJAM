import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { AuthProvider, useAuth } from '@/context/AuthContext';

vi.mock('@/api', () => ({
  isAuthenticated: vi.fn(() => false),
  getToken: vi.fn(() => null),
  logoutUser: vi.fn()
}));

const TestComponent = () => {
  const { isLoggedIn, isLoading } = useAuth();
  return (
    <div>
      <div data-testid="logged-in">{isLoggedIn ? 'true' : 'false'}</div>
      <div data-testid="loading">{isLoading ? 'true' : 'false'}</div>
    </div>
  );
};

describe('AuthContext - Teste Simples', () => {
  it('deve fornecer valores do contexto', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('logged-in')).toBeInTheDocument();
    expect(screen.getByTestId('loading')).toBeInTheDocument();
  });
});

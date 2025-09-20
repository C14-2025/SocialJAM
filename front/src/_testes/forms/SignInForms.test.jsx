import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SigninForms from '@/_auth/forms/SigninForms';

// Mock simples da API
vi.mock('@/api', () => ({
  loginUser: vi.fn()
}));

// Mock simples do contexto de auth
vi.mock('@/context/AuthContext', () => ({
  useAuth: vi.fn(() => ({
    login: vi.fn()
  }))
}));

// Mock simples da navegação
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => vi.fn()
  };
});

const TestWrapper = ({ children }) => (
  <BrowserRouter>{children}</BrowserRouter>
);

describe('SigninForms - Teste Simples', () => {
  it('deve renderizar o formulário de login', () => {
    render(
      <TestWrapper>
        <SigninForms />
      </TestWrapper>
    );

    expect(screen.getByText('Entre com sua conta')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Senha')).toBeInTheDocument();
  });
});
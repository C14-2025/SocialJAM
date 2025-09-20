import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SignupForms from '@/_auth/forms/SignupForms';
import api from '@/api';

vi.mock('@/api', () => ({
  default: {
    post: vi.fn(),
  },
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

global.alert = vi.fn();

const TestWrapper = ({ children }) => (
  <BrowserRouter>
    {children}
  </BrowserRouter>
);

describe('SignupForms', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve aceitar dados válidos', () => {
    render(
      <TestWrapper>
        <SignupForms />
      </TestWrapper>
    );

    expect(screen.getByText('Crie sua conta')).toBeInTheDocument();
    expect(screen.getByLabelText('Nome')).toBeInTheDocument();
    expect(screen.getByLabelText('Nome de Usuário')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Senha')).toBeInTheDocument();
  });

  it('deve permitir preencher campo de email', () => {
    render(
      <TestWrapper>
        <SignupForms />
      </TestWrapper>
    );

    const emailInput = screen.getByLabelText('Email');
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    
    expect(emailInput.value).toBe('test@example.com');
  });

  it('deve mostrar alert após cadastro bem-sucedido', async () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});
    
    api.post.mockResolvedValue({
      data: { message: 'Usuário criado com sucesso' }
    });

    render(
      <TestWrapper>
        <SignupForms />
      </TestWrapper>
    );

    // preencher o formulário com dados válidos
    fireEvent.change(screen.getByLabelText('Nome'), { 
      target: { value: 'Maria Santos' } 
    });
    fireEvent.change(screen.getByLabelText('Nome de Usuário'), { 
      target: { value: 'mariasantos' } 
    });
    fireEvent.change(screen.getByLabelText('Email'), { 
      target: { value: 'maria@teste.com' } 
    });
    fireEvent.change(screen.getByLabelText('Senha'), { 
      target: { value: 'minhasenha123' } 
    });

    fireEvent.click(screen.getByRole('button', { name: /enviar/i }));


    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith("Cadastro realizado com sucesso!");
    });

    alertSpy.mockRestore();
  });

  it('deve mostrar mensagens de erro para campos obrigatórios', async () => {
    render(
      <TestWrapper>
        <SignupForms />
      </TestWrapper>
    );

    // Tentar submeter formulário vazio
    fireEvent.click(screen.getByRole('button', { name: /enviar/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/Nome deve ter no mínimo 2 caracteres/i)
      ).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(
        screen.getByText(/Username deve ter no mínimo 2 caracteres/i)
      ).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(
        screen.getByText(/Email inválido/i)
      ).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(
        screen.getByText(/Senha deve ter no mínimo 8 caracteres/i)
      ).toBeInTheDocument();
    });
  });
});
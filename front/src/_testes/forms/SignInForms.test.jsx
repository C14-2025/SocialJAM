import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SigninForms from '@/_auth/forms/SigninForms';
import { loginUser } from '@/api';
import { useAuth } from '@/context/AuthContext';

//mock simples da API
vi.mock('@/api', () => ({
  loginUser: vi.fn() //ele cria uma cópia da função
}));

//mock simples do contexto de auth
vi.mock('@/context/AuthContext', () => ({
  useAuth: vi.fn() //cria uma cópia do objeto
}));

//mock simples da navegação
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom'); 
  return {
    ...actual,
    useNavigate: () => mockNavigate //cria um mock da função de navegar do router dom
  };
});

const TestWrapper = ({ children }) => (
  <BrowserRouter>{children}</BrowserRouter>
);

describe('SigninForms - Testes com Mocks', () => {
  const mockLogin = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    useAuth.mockReturnValue({ login: mockLogin });
  });

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

  it('deve chamar loginUser com email e senha ao submeter', async () => {
    loginUser.mockResolvedValue({ success: true, token: 'fake-token' });

    render(
      <TestWrapper>
        <SigninForms />
      </TestWrapper>
    );

    
    const emailInput = screen.getByLabelText('Email'); 
    const passwordInput = screen.getByLabelText('Senha');
    
    fireEvent.change(emailInput, { target: { value: 'test@test.com' } }); //aqui ele escreve a senha e o email
    fireEvent.change(passwordInput, { target: { value: '12345678' } });

    
    const submitButton = screen.getByRole('button', { name: /enviar/i });
    fireEvent.click(submitButton); //aqui clica no submit

    // berifica se loginUser foi chamado com os valores corretos
    await waitFor(() => {
      expect(loginUser).toHaveBeenCalledWith('test@test.com', '12345678'); //assert que o login user está sendo chamado corretamente
    });
  });

  it('deve chamar login do contexto e navegar para home em caso de sucesso', async () => {
    loginUser.mockResolvedValue({ success: true, token: 'fake-token' });

    render(
      <TestWrapper>
        <SigninForms />
      </TestWrapper>
    );

    // preenche e manda o formulário
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'test@test.com' } });
    fireEvent.change(screen.getByLabelText('Senha'), { target: { value: '12345678' } });
    fireEvent.click(screen.getByRole('button', { name: /enviar/i }));

    // verifica se login do contexto foi chamado
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalled(); //assert q vai chamar o login
    });

    // verifica se navegou para a home
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/'); //assert q foi pra home
    });
  });

  it('deve exibir mensagem de erro quando o login falha', async () => {
    loginUser.mockResolvedValue({ 
      success: false, 
      error: 'Email ou senha incorretos' 
    });

    render(
      <TestWrapper>
        <SigninForms />
      </TestWrapper>
    );

    //preenche e submete o formulário
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'errado@test.com' } });
    fireEvent.change(screen.getByLabelText('Senha'), { target: { value: 'senhaerrada' } });
    fireEvent.click(screen.getByRole('button', { name: /enviar/i }));

    //verifica se a mensagem de erro aparece
    await waitFor(() => {
      expect(screen.getByText('Email ou senha incorretos')).toBeInTheDocument();
    });

    //verifica que NÃO chamou login nem navegou
    expect(mockLogin).not.toHaveBeenCalled(); 
    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it('deve exibir loader enquanto está fazendo login', async () => {
    loginUser.mockImplementation(() => new Promise(resolve => 
      setTimeout(() => resolve({ success: true }), 100)
    ));

    render(
      <TestWrapper>
        <SigninForms />
      </TestWrapper>
    );

    //preenche e submete
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'test@test.com' } });
    fireEvent.change(screen.getByLabelText('Senha'), { target: { value: '12345678' } });
    fireEvent.click(screen.getByRole('button', { name: /enviar/i }));

    //verifica se o loader aparece
    await waitFor(() => {
      expect(screen.getByText(/carregando/i)).toBeInTheDocument();
    });
  });
});
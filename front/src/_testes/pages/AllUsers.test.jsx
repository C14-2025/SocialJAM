import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AllUsers from '@/_root/pages/AllUsers';
import { searchUsers, sendFriendRequest, getSentFriendRequests, getFriends, getReceivedFriendRequests, getMe } from '@/api';
import { useAuth } from '@/context/AuthContext';

vi.mock('@/api', () => ({
  searchUsers: vi.fn(),
  sendFriendRequest: vi.fn(),
  getSentFriendRequests: vi.fn(),
  getFriends: vi.fn(),
  getReceivedFriendRequests: vi.fn(),
  getMe: vi.fn(),
  getUserById: vi.fn(),
  respondToFriendRequest: vi.fn(),
  removeFriend: vi.fn()
}));

vi.mock('@/context/AuthContext', () => ({
  useAuth: vi.fn()
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useParams: () => ({})
  };
});

const TestWrapper = ({ children }) => (
  <BrowserRouter>{children}</BrowserRouter>
);

describe('AllUsers - Testes com Mocks', () => {
  const mockUser = {
    username: 'testuser',
    id: 1,
    favorite_artist: 'testartist'
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useAuth.mockReturnValue({ 
      user: mockUser,
      isLoggedIn: true 
    });
    
    getMe.mockResolvedValue({ success: true, me: mockUser });
    getSentFriendRequests.mockResolvedValue({ success: true, data: [] });
    getReceivedFriendRequests.mockResolvedValue({ success: true, data: [] });
    getFriends.mockResolvedValue({ success: true, data: [] });
    searchUsers.mockResolvedValue({ success: true, users: [] });
  });

  it('deve renderizar o componente com título correto', async () => {
    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText(/busque por usuários/i)).toBeInTheDocument();
    });
  });

  it('deve alternar para aba de solicitações ao clicar', async () => {
    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    const requestsTab = screen.getByText(/solicitações/i);
    fireEvent.click(requestsTab);

    await waitFor(() => {
      expect(screen.getByText(/solicitações de amizade/i)).toBeInTheDocument();
    });
  });

  it('deve buscar usuários quando digitar no campo de busca', async () => {
    const mockUsers = [
      { id: 2, username: 'user1', favorite_artist: 'Artist 1' },
      { id: 3, username: 'user2', favorite_artist: 'Artist 2' }
    ];

    searchUsers.mockResolvedValue({ success: true, users: mockUsers });

    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    const searchInput = screen.getByPlaceholderText(/busque usuários/i);
    fireEvent.change(searchInput, { target: { value: 'user' } });

    await waitFor(() => {
      expect(searchUsers).toHaveBeenCalledWith('user');
    }, { timeout: 1000 });
  });

  it('deve exibir lista de usuários após busca', async () => {
    const mockUsers = [
      { id: 2, username: 'dudu1', favorite_artist: 'Milton Nascimento' },
      { id: 3, username: 'dudu2', favorite_artist: 'Lo Borges' }
    ];

    searchUsers.mockResolvedValue({ success: true, users: mockUsers });

    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    const searchInput = screen.getByPlaceholderText(/busque usuários/i);
    fireEvent.change(searchInput, { target: { value: 'du' } });

    await waitFor(() => {
      expect(screen.getByText('dudu1')).toBeInTheDocument();
      expect(screen.getByText('dudu2')).toBeInTheDocument();
    });
  });

  it('deve ativar switch de "mostrar apenas amigos"', async () => {
    const mockFriends = [
      { id: 2, username: 'amigo1', favorite_artist: 'artista1' }
    ];

    getFriends.mockResolvedValue({ success: true, data: mockFriends });

    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    const switchElement = screen.getByRole('switch');
    fireEvent.click(switchElement);

    await waitFor(() => {
      expect(screen.getByText(/seus amigos/i)).toBeInTheDocument();
    });
  });

  it('deve exibir mensagem quando não há solicitações pendentes', async () => {
    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    const requestsTab = screen.getByText(/solicitações/i);
    fireEvent.click(requestsTab);

    await waitFor(() => {
      expect(screen.getByText(/nenhuma solicitação pendente/i)).toBeInTheDocument();
    });
  });

  it('deve exibir loader enquanto está carregando usuários', async () => {
    searchUsers.mockImplementation(() => new Promise(resolve => 
      setTimeout(() => resolve({ success: true, users: [] }), 100)
    ));

    render(
      <TestWrapper>
        <AllUsers />
      </TestWrapper>
    );

    const searchInput = screen.getByPlaceholderText(/busque usuários/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });

    await waitFor(() => {
      expect(screen.getByAltText(/carregando/i)).toBeInTheDocument();
    });
  });
});

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import TopBar from '@/components/shared/TopBar';
import { AuthProvider } from '@/context/AuthContext';

const renderComponent = () => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <TopBar />
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('TopBar', () => {
  it('deve renderizar o logo', () => {
    renderComponent();
    const logo = screen.getByAltText('logo');
    expect(logo).toBeInTheDocument();
    expect(logo).toHaveAttribute('src', '/assets/images/Logo_SJ.svg');
  });

  it('deve renderizar link do logo apontando para home', () => {
    renderComponent();
    const logoLink = screen.getByAltText('logo').closest('a');
    expect(logoLink).toHaveAttribute('href', '/');
  });

  it('deve renderizar botão de logout', () => {
    renderComponent();
    const logoutButton = screen.getByRole('button');
    expect(logoutButton).toBeInTheDocument();
  });

  it('deve renderizar ícone de logout', () => {
    renderComponent();
    const logoutIcon = screen.getByAltText('Logout');
    expect(logoutIcon).toBeInTheDocument();
    expect(logoutIcon).toHaveAttribute('src', '/assets/icons/logout.svg');
  });

  it('deve renderizar link para o perfil', () => {
    renderComponent();
    const profileLink = screen.getByAltText('Profile').closest('a');
    expect(profileLink).toHaveAttribute('href', '/profile');
  });

  it('deve renderizar imagem de perfil', () => {
    renderComponent();
    const profileImg = screen.getByAltText('Profile');
    expect(profileImg).toBeInTheDocument();
    expect(profileImg).toHaveAttribute('src', '/assets/images/profile.png');
  });
});
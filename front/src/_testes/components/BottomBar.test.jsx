import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import BottomBar from '@/components/shared/BottomBar';
import { bottombarLinks } from '@/constants';

const renderComponent = (initialRoute = '/') => {
  return render(
    <MemoryRouter initialEntries={[initialRoute]}>
      <BottomBar />
    </MemoryRouter>
  );
};

describe('BottomBar - Renderização', () => {
  it('deve renderizar todos os links da bottom bar', () => {
    renderComponent();
    
    bottombarLinks.forEach(link => {
      const linkElement = screen.getByText(link.label);
      expect(linkElement).toBeInTheDocument();
    });
  });

  it('deve renderizar exatamente 4 links', () => {
    renderComponent();
    
    const links = screen.getAllByRole('link');
    expect(links.length).toBe(4);
  });

  it('todos os links devem ter ícones', () => {
    renderComponent();
    
    bottombarLinks.forEach(link => {
      const icon = screen.getByAltText(link.label);
      expect(icon).toBeInTheDocument();
    });
  });

  it('cada link deve apontar para a rota correta', () => {
    renderComponent();
    
    bottombarLinks.forEach(link => {
      const linkElement = screen.getByText(link.label).closest('a');
      expect(linkElement).toHaveAttribute('href', link.route);
    });
  });

  it('deve ter a classe bottom-bar', () => {
    const { container } = renderComponent();
    const bottomBar = container.querySelector('.bottom-bar');
    expect(bottomBar).toBeInTheDocument();
  });
});

describe('BottomBar - Estado Ativo', () => {
  // it('deve destacar link Home quando na rota /', () => {
  //   renderComponent('/');
    
  //   const homeLink = screen.getByText('Home').closest('a');
  //   expect(homeLink).toHaveClass('bg-primary-500');
  // });

  it('deve destacar link Explore quando na rota /explore', () => {
    renderComponent('/explore');
    
    const exploreLink = screen.getByText('Explore').closest('a');
    expect(exploreLink).toHaveClass('bg-primary-500');
  });

  it('deve destacar link Saved quando na rota /saved', () => {
    renderComponent('/saved');
    
    const savedLink = screen.getByText('Saved').closest('a');
    expect(savedLink).toHaveClass('bg-primary-500');
  });

  // it('deve destacar link Create quando na rota /create-post', () => {
  //   renderComponent('/create-post');
    
  //   const createLink = screen.getByText('Create').closest('a');
  //   expect(createLink).toHaveClass('bg-primary-500');
  // });

  // it('ícone deve ter classe invert-white quando link está ativo', () => {
  //   renderComponent('/');
    
  //   const homeIcon = screen.getByAltText('Home');
  //   expect(homeIcon).toHaveClass('invert-white');
  // });
});
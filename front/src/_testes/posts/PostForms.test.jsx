import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import PostForms from "@/components/forms/PostForms";

// Mock da função createPost
vi.mock("@/api", () => ({
  createPost: vi.fn(),
}));

// Mock do useParams para retornar um artistId
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useParams: () => ({ artistId: "test_artist_123" }),
    useNavigate: () => vi.fn(),
  };
});

const TestWrapper = ({ children }) => <BrowserRouter>{children}</BrowserRouter>;

describe("PostForms - Testes de Renderização", () => {
  it("deve renderizar o formulário de post", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    // Verifica se o campo de descrição existe
    expect(screen.getByText("Descrição")).toBeInTheDocument();
  });

  it("deve renderizar o campo de texto para descrição", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    const descriptionField = screen.getByLabelText("Descrição");
    expect(descriptionField).toBeInTheDocument();
  });

  it("deve renderizar o botão de publicar", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    const publishButton = screen.getByText("Publicar");
    expect(publishButton).toBeInTheDocument();
  });

  it("deve renderizar o botão de cancelar", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    const cancelButton = screen.getByText("Cancelar");
    expect(cancelButton).toBeInTheDocument();
  });

  it("deve renderizar a label de adicionar foto", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    expect(screen.getByText("Adicionar foto")).toBeInTheDocument();
  });

  it("deve renderizar a descrição do campo de descrição", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    expect(screen.getByText("Essa é a descrição do seu post.")).toBeInTheDocument();
  });

  it("deve renderizar a descrição do campo de imagens", () => {
    render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    expect(screen.getByText("Adicione fotos ao seu post (opcional).")).toBeInTheDocument();
  });

  it("deve ter um formulário com os campos corretos", () => {
    const { container } = render(
      <TestWrapper>
        <PostForms />
      </TestWrapper>
    );

    const form = container.querySelector("form");
    expect(form).toBeInTheDocument();
  });
});

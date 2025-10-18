import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import SignupForms from "@/_auth/forms/SignupForms";

// Mock simples da API
vi.mock("@/api", () => ({
  default: {
    post: vi.fn(),
  },
}));

// Mock simples da navegação
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  };
});

const TestWrapper = ({ children }) => <BrowserRouter>{children}</BrowserRouter>;

describe("SignupForms - Teste Simples", () => {
  it("deve renderizar o formulário de cadastro", () => {
    render(
      <TestWrapper>
        <SignupForms />
      </TestWrapper>
    );

    expect(screen.getByText("Crie sua conta")).toBeInTheDocument();
    expect(screen.getByLabelText("Nome")).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
  });
});
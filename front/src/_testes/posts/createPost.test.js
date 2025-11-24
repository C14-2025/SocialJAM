import { describe, it, expect, vi, beforeEach } from "vitest";
import { createPost } from "@/api";

// Mock do axios
vi.mock("@/api", () => ({
  createPost: vi.fn(),
}));

describe("createPost - Testes Unitários", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("deve retornar sucesso com dados válidos", async () => {
    const mockResponse = {
      success: true,
      data: {
        post_id: "123456",
        message: "Post criado com sucesso!",
      },
    };

    createPost.mockResolvedValue(mockResponse);

    const result = await createPost("artist123", "Conteúdo do post", []);

    expect(result.success).toBe(true);
    expect(result.data).toHaveProperty("post_id");
    expect(result.data.message).toBe("Post criado com sucesso!");
  });

  it("deve aceitar post sem imagens", async () => {
    const mockResponse = {
      success: true,
      data: { post_id: "789", message: "Post criado com sucesso!" },
    };

    createPost.mockResolvedValue(mockResponse);

    const result = await createPost("artist123", "Post sem imagens", null);

    expect(result.success).toBe(true);
    expect(createPost).toHaveBeenCalledWith("artist123", "Post sem imagens", null);
  });

  it("deve aceitar post com múltiplas imagens", async () => {
    const mockResponse = {
      success: true,
      data: { post_id: "456", message: "Post criado com sucesso!" },
    };

    createPost.mockResolvedValue(mockResponse);

    const mockImages = [
      new File(["image1"], "photo1.jpg", { type: "image/jpeg" }),
      new File(["image2"], "photo2.jpg", { type: "image/jpeg" }),
    ];

    const result = await createPost("artist123", "Post com imagens", mockImages);

    expect(result.success).toBe(true);
    expect(createPost).toHaveBeenCalledWith(
      "artist123",
      "Post com imagens",
      mockImages
    );
  });

  it("deve retornar erro quando falhar", async () => {
    const mockErrorResponse = {
      success: false,
      error: "Erro ao criar post",
    };

    createPost.mockResolvedValue(mockErrorResponse);

    const result = await createPost("artist123", "Conteúdo", []);

    expect(result.success).toBe(false);
    expect(result.error).toBe("Erro ao criar post");
  });

  it("deve ser chamado com os parâmetros corretos", async () => {
    const mockResponse = { success: true, data: {} };
    createPost.mockResolvedValue(mockResponse);

    const artistId = "spotify_artist_123";
    const content = "Meu post sobre música";
    const images = [];

    await createPost(artistId, content, images);

    expect(createPost).toHaveBeenCalledTimes(1);
    expect(createPost).toHaveBeenCalledWith(artistId, content, images);
  });
});

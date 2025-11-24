import { describe, it, expect } from "vitest";

// Funções utilitárias simples para posts
const formatPostData = (artistId, content, images) => {
  return {
    artist_id: artistId,
    content: content,
    images: images || [],
  };
};

const isValidFileType = (file) => {
  const validTypes = ["image/jpeg", "image/png", "image/jpg", "image/gif", "image/webp"];
  return validTypes.includes(file.type);
};

const getImageCount = (images) => {
  return images ? images.length : 0;
};

const hasImages = (images) => {
  return images && images.length > 0;
};

const createFormDataStructure = (artistId, content, images) => {
  const data = {
    artist_id: artistId,
    content: content,
    hasImages: hasImages(images),
    imageCount: getImageCount(images),
  };
  return data;
};

describe("Post Utils - Funções Utilitárias", () => {
  describe("formatPostData", () => {
    it("deve formatar dados do post corretamente", () => {
      const result = formatPostData("artist123", "Conteúdo", []);
      expect(result).toEqual({
        artist_id: "artist123",
        content: "Conteúdo",
        images: [],
      });
    });

    it("deve formatar post com imagens", () => {
      const mockImages = [new File([""], "photo.jpg")];
      const result = formatPostData("artist123", "Texto", mockImages);
      expect(result.images).toBe(mockImages);
    });

    it("deve usar array vazio se images for null", () => {
      const result = formatPostData("artist123", "Texto", null);
      expect(result.images).toEqual([]);
    });

    it("deve usar array vazio se images for undefined", () => {
      const result = formatPostData("artist123", "Texto", undefined);
      expect(result.images).toEqual([]);
    });
  });

  describe("isValidFileType", () => {
    it("deve aceitar JPEG", () => {
      const file = new File([""], "photo.jpg", { type: "image/jpeg" });
      expect(isValidFileType(file)).toBe(true);
    });

    it("deve aceitar JPG", () => {
      const file = new File([""], "photo.jpg", { type: "image/jpg" });
      expect(isValidFileType(file)).toBe(true);
    });

    it("deve aceitar PNG", () => {
      const file = new File([""], "photo.png", { type: "image/png" });
      expect(isValidFileType(file)).toBe(true);
    });

    it("deve aceitar GIF", () => {
      const file = new File([""], "animation.gif", { type: "image/gif" });
      expect(isValidFileType(file)).toBe(true);
    });

    it("deve aceitar WEBP", () => {
      const file = new File([""], "photo.webp", { type: "image/webp" });
      expect(isValidFileType(file)).toBe(true);
    });

    it("deve rejeitar PDF", () => {
      const file = new File([""], "document.pdf", { type: "application/pdf" });
      expect(isValidFileType(file)).toBe(false);
    });

    it("deve rejeitar arquivo de texto", () => {
      const file = new File([""], "file.txt", { type: "text/plain" });
      expect(isValidFileType(file)).toBe(false);
    });
  });

  describe("getImageCount", () => {
    it("deve retornar 0 para null", () => {
      expect(getImageCount(null)).toBe(0);
    });

    it("deve retornar 0 para undefined", () => {
      expect(getImageCount(undefined)).toBe(0);
    });

    it("deve retornar 0 para array vazio", () => {
      expect(getImageCount([])).toBe(0);
    });

    it("deve retornar 1 para array com uma imagem", () => {
      const images = [new File([""], "photo.jpg")];
      expect(getImageCount(images)).toBe(1);
    });

    it("deve retornar a quantidade correta de imagens", () => {
      const images = [
        new File([""], "photo1.jpg"),
        new File([""], "photo2.jpg"),
        new File([""], "photo3.jpg"),
      ];
      expect(getImageCount(images)).toBe(3);
    });
  });

  describe("hasImages", () => {
    it("deve retornar false para array vazio", () => {
      expect(hasImages([])).toBe(false);
    });

    it("deve retornar true para array com imagens", () => {
      const images = [new File([""], "photo.jpg")];
      expect(hasImages(images)).toBe(true);
    });
  });

  describe("createFormDataStructure", () => {
    it("deve criar estrutura com imagens", () => {
      const images = [new File([""], "photo1.jpg"), new File([""], "photo2.jpg")];
      const result = createFormDataStructure("artist123", "Texto", images);
      expect(result).toEqual({
        artist_id: "artist123",
        content: "Texto",
        hasImages: true,
        imageCount: 2,
      });
    });

    it("deve incluir todos os campos necessários", () => {
      const result = createFormDataStructure("artist123", "Conteúdo", []);
      expect(result).toHaveProperty("artist_id");
      expect(result).toHaveProperty("content");
      expect(result).toHaveProperty("hasImages");
      expect(result).toHaveProperty("imageCount");
    });
  });
});

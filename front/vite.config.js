import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "tailwindcss";
import path from "path";
import { fileURLToPath } from "url";

// Create __dirname equivalent for ES modules
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.js",
    include: [
      'src/**/*.{test,spec}.{js,jsx,ts,tsx}',
      'src/_testes/**/*.{test,spec}.{js,jsx,ts,tsx}'
    ],
  },
});

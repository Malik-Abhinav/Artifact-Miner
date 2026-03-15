import { defineConfig, type Plugin } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

// Strip Next.js "use client" / "use server" directives before Vitest processes files
const stripNextDirectives: Plugin = {
  name: "strip-next-directives",
  transform(code, id) {
    if (id.endsWith(".tsx") || id.endsWith(".ts")) {
      return code.replace(/^["']use (client|server)["'];?\n?/m, "");
    }
  },
};

export default defineConfig({
  plugins: [stripNextDirectives, react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});

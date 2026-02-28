import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";
import { svelteTesting } from "@testing-library/svelte/vite";

export default defineConfig({
  plugins: [sveltekit(), svelteTesting()],
  test: {
    environment: "happy-dom",
    setupFiles: ["./vitest-setup.js"],
    clearMocks: true,
  },
  resolve: process.env.VITEST
    ? {
        conditions: ["browser"],
        alias: [
          {
            find: "msw/node",
            replacement: "/node_modules/msw/lib/native/index.mjs",
          },
        ],
      }
    : undefined,
});

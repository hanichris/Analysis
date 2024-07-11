import { defineConfig } from 'vite'
import * as path from "path";
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    emptyOutDir: true,
    manifest: "manifest.json",
    outDir: path.resolve('../backend/static'),
    rollupOptions: {
      input: {
        key0001: "./src/main.tsx",
      },
      output: {
        entryFileNames: "index-bundle.js",
      }
    }
  }
})

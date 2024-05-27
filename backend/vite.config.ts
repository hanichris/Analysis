import { defineConfig } from 'vite'
import * as path from "path";

import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: path.resolve('./static'),
    rollupOptions: {
      input: {
        key0001: "./assets/main.tsx"
      },
      output: {
        entryFileNames: "index-bundle.js"
      }
    },
  },
})


import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/generate': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      },
      '/parse-dxf': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      }
    },
    host: true,
  },
  build: {
    outDir: '../backend/static',
    emptyOutDir: true,
  }
})

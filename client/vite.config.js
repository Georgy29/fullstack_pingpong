import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,                   // важно в Codespaces
    port: 5173,                   // можно явно указать
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
})
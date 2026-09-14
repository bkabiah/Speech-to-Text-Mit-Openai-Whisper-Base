import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Wichtig für VPS-Zugriff
    proxy: {
      '/api': {
        target: 'http://localhost:8002', // Leitet alles an /api an dein Backend weiter
        changeOrigin: true,
      }
    }
  }
})

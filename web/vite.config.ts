import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // so that api url is reachable in both local and production envirnoments
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})

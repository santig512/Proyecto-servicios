import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'https://tech-solutions-lgi4.onrender.com:10000',
        changeOrigin: true,
      },
    },
  },
})

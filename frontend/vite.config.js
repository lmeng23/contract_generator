import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  base: './', // 确保在部署到相对路径时资源能正确加载
  build: {
    outDir: 'dist', // 打包目录
  },
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})

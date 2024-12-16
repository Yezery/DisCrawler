import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  // // 配置服务器的代理设置
  // server: {
  //   // 代理配置，用于重定向请求到其他服务器
  //   proxy: {
  //     '/': {
  //       // 目标服务器的地址
  //       target: 'http://localhost:8000',
  //       // 更改请求的origin为代理服务器的origin，以便与目标服务器交互
  //       changeOrigin: true,
  //       // 重写请求路径，移除/前缀
  //       rewrite: path => path.replace(/^\//, ''),
  //     },
  //   },
  // },
})

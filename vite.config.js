import { defineConfig } from 'vite'

export default defineConfig({
  root: '.',
  base: '/buddhist-lineage-tree-for-web/',
  server: {
    port: 3000,
    open: true,
    host: true
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
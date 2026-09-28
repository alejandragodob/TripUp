import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// base './' keeps asset paths relative so the same build works on Vercel (root)
// and on GitHub Pages (served from /<repo>/tripup/).
export default defineConfig({
  plugins: [react()],
  base: './',
})

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import dotenv from 'dotenv';
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  dotenv.config({ path: `./.env.${mode}` });
  return {
    plugins: [
      vue(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    }
  }
})

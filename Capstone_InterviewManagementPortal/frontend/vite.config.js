import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite build configuration for the React frontend.
 *
 * The React plugin enables JSX transformation and Fast Refresh during local
 * development.
 */
export default defineConfig({
  plugins: [react()],
})

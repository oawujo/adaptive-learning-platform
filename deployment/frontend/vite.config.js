
export default defineConfig({
  root: ".",
  build: {
  import { defineConfig } from 'vite';
  import react from '@vitejs/plugin-react';

  export default defineConfig({
    plugins: [react()],
    outDir: "dist",
  },
});


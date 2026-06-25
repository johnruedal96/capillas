import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    lib: {
      entry: 'src/widget/index.ts',
      name: 'CapillasWidget',
      formats: ['iife'],
      fileName: () => 'widget.iife.js',
    },
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
    },
    minify: 'terser',
    cssCodeSplit: false,
    target: 'es2022',
  },
  server: {
    port: 5173,
  },
});

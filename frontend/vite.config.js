import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
    test: {
        environment: 'happy-dom', // Active la simulation de l'objet window
        globals: true
    },
    build: {
        rollupOptions: {
            input: resolve(__dirname, 'src/js/main.js'),
        },
    },
})
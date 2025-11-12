import { defineConfig } from "vite";

export default defineConfig({
    root: "src",
    base: '/sherlock-data/grist_plugins/v2/dist/',
    build: {
        outDir: "../dist",
    },
});
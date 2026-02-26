import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
import process from "node:process";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [
      react({
        babel: {
          plugins: [["babel-plugin-react-compiler"]],
        },
      }),
      VitePWA({
        registerType: "autoUpdate",
        workbox: {
          skipWaiting: true,
          clientsClaim: true,
        },
        includeAssets: [
          "blu-logo-192.png",
          "blu-logo-512.png",
          "blu-logo-apple-icon.png",
        ],
        manifest: {
          name: "bluTape",
          short_name: "bluTape",
          start_url: "/",
          display: "standalone",
          background_color: "#8999af",
          theme_color: "#262f4c",
          icons: [
            {
              src: "/blu-logo-192.png",
              sizes: "192x192",
              type: "image/png",
            },
            {
              src: "/blu-logo-512.png",
              sizes: "512x512",
              type: "image/png",
            },
          ],
        },
      }),
    ],
    server: {
      proxy: {
        "/api": {
          target: env.VITE_SERVER_URL,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
});

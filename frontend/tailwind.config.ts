import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand:   { DEFAULT: "#00D4FF", dark: "#0099BB" },
        surface: { DEFAULT: "#0F1117", card: "#1A1D27", border: "#2A2D3E" },
        profit:  "#00C896",
        loss:    "#FF4757",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;

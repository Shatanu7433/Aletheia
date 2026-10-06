import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { night: "#070914", glass: "rgba(255,255,255,0.12)", edge: "rgba(255,255,255,0.28)", signal: "#FFFFFF", good: "#A8F0C6", bad: "#FFB4A8", mute: "rgba(255,255,255,0.72)" },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        serif: ["var(--font-serif)", "Georgia", "serif"],
      },
    },
  },
} satisfies Config;

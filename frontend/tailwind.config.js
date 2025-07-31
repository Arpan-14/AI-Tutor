/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      animation: {
        'typing': 'typing 1.5s steps(40, end) infinite',
        'blink': 'blink 1s infinite',
      },
      keyframes: {
        typing: {
          '0%': { width: '0' },
          '100%': { width: '100%' },
        },
        blink: {
          '0%, 50%': { 'border-color': 'transparent' },
          '51%, 100%': { 'border-color': 'currentColor' },
        },
      },
    },
  },
  plugins: [],
}

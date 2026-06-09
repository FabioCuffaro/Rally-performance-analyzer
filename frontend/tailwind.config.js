/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Motorsport dark palette
        surface: {
          DEFAULT: '#09090b',   // page background
          card:    '#18181b',   // card background
          hover:   '#27272a',   // hover state
          border:  '#3f3f46',   // borders
        },
        rally: {
          red:    '#ef4444',    // primary accent
          gold:   '#f59e0b',    // podium gold / P1
          silver: '#94a3b8',    // P2
          bronze: '#b45309',    // P3
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
}

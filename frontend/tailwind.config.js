/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Palette officielle DéclaTogo — inspirée du drapeau togolais
        vert: {
          DEFAULT: '#005A3C',
          light:   '#007A52',
          xl:      '#E8F4F0',
        },
        rouge: {
          DEFAULT: '#C41230',
          light:   '#E8192F',
        },
        or: {
          DEFAULT: '#D4A017',
          light:   '#F5E6A8',
        },
        creme: '#FAF7F2',
        texte: '#1A2E22',
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans:  ['"DM Sans"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'card':    '0 4px 24px rgba(0,90,60,.10)',
        'card-lg': '0 12px 48px rgba(0,90,60,.16)',
      },
      borderRadius: {
        'card': '12px',
      },
    },
  },
  plugins: [],
}
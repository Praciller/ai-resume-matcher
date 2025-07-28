/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        'mono': ['Courier New', 'monospace'],
      },
      colors: {
        'pure-black': '#000000',
        'pure-white': '#FFFFFF',
        'light-gray': '#F5F5F5',
      },
      borderWidth: {
        '4': '4px',
      }
    },
  },
  plugins: [],
}

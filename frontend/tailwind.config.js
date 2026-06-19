/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Nirukta design system
        background: '#E8F0DE',
        dashlet: '#FDF0E2',
        primary: '#44546A',
        'status-healthy': '#639922',
        'status-warning': '#BA7517',
        'status-error': '#C0392B',
        surface: '#FFFFFF',
        border: '#D5DCE8',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

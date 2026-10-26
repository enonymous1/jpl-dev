/** @type {import('tailwindcss').Config} */
module.exports = {
  // Scan all template files plus global scripts.
  content: [
    './templates/**/*.html',
    './static/script.js',
    './static/global-theme.js',
  ],
  // Mirror the site's existing [data-theme="dark"] CSS variable system.
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    extend: {},
  },
  plugins: [],
};

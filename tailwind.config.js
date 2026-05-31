/** @type {import('tailwindcss').Config} */
module.exports = {
  // Scan all template files (all routes) plus global scripts.
  // schedule_maker has its own tailwind.config.js in projects/schedule_maker/.
  content: [
    './templates/**/*.html',
    './projects/**/templates/**/*.html',
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

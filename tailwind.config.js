/** @type {import('tailwindcss').Config} */
module.exports = {
  // Scan all template files plus scripts. The JS modules in static/js/
  // build repo cards from template strings, so their Tailwind classes
  // (flex, gap-1, font-semibold, ...) must be scanned too, or the
  // purged bundle drops them and the cards render unstyled.
  content: [
    './templates/**/*.html',
    './static/global-theme.js',
    './static/js/**/*.js',
  ],
  // Mirror the site's existing [data-theme="dark"] CSS variable system.
  darkMode: ['selector', '[data-theme="dark"]'],
  theme: {
    extend: {},
  },
  plugins: [],
};

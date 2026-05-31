/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Schedule Maker template and its JS (for literal class strings).
    // Paths are relative to this config file (projects/schedule_maker/).
    './templates/**/*.html',
    '../../static/projects/schedule_maker/script.js',
  ],
  safelist: [
    // Employee pill colors are dynamically constructed in addEmployee() as
    // `bg-${color}-100 text-${color}-800` — not statically scannable.
    // The full color range used by both addEmployee() and loadSeedData().
    { pattern: /^(bg|text)-(blue|green|yellow|purple|pink|indigo|red|teal|orange|cyan)-(100|800)$/ },
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    // Disable Tailwind's Preflight CSS reset. base.html loads Bootstrap 5.3
    // (which includes Reboot). Running both resets on the same elements causes
    // unpredictable base styling and requires !important patches to compensate.
    // Disabling Preflight here means Bootstrap Reboot is the sole CSS reset,
    // while all Tailwind utility classes remain available. (E6a)
    preflight: false,
  },
};

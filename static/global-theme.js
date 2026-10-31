/**
 * Global Theme Management
 * Handles light/dark theme switching across all pages: reads the saved
 * preference (or the OS preference), writes data-theme, and keeps the
 * #theme-toggle button in sync. The inline script in each page's <head>
 * duplicates _loadTheme on purpose — it must run before this file loads
 * so the theme never flashes on first paint.
 */

const GLOBAL_THEME_STORAGE_KEY = 'jpl_dev_global_theme';

function _loadTheme() {
    const savedTheme = localStorage.getItem(GLOBAL_THEME_STORAGE_KEY);
    if (savedTheme) return savedTheme;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

function _applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(GLOBAL_THEME_STORAGE_KEY, theme);
    _updateThemeToggleButton(theme);
}

function _updateThemeToggleButton(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Icon-based toggle (sidebar and base.html nav).
    const lightIcon = themeToggle.querySelector('.theme-icon-light');
    const darkIcon  = themeToggle.querySelector('.theme-icon-dark');
    if (lightIcon && darkIcon) {
        lightIcon.classList.toggle('hidden', theme === 'dark');
        darkIcon.classList.toggle('hidden', theme !== 'dark');
    }

    themeToggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    themeToggle.setAttribute('title',      theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

document.addEventListener('DOMContentLoaded', function () {
    _applyTheme(_loadTheme());

    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            _applyTheme(current === 'dark' ? 'light' : 'dark');
        });
    }

    // Follow OS preference changes only when the user has no saved preference
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
            if (!localStorage.getItem(GLOBAL_THEME_STORAGE_KEY)) {
                _applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
});

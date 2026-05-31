/**
 * Global Theme Management
 * Handles light/dark theme switching across all pages.
 * Writes both data-theme (custom CSS) and data-bs-theme (Bootstrap 5.3) in sync.
 * Dispatches 'themeChange' CustomEvent for dependent components (widgets, charts).
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
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem(GLOBAL_THEME_STORAGE_KEY, theme);
    _updateThemeToggleButton(theme);
    document.dispatchEvent(new CustomEvent('themeChange', { detail: { theme } }));
}

function _updateThemeToggleButton(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Icon-based toggle (base.html)
    const lightIcon = themeToggle.querySelector('.theme-icon-light');
    const darkIcon  = themeToggle.querySelector('.theme-icon-dark');
    if (lightIcon && darkIcon) {
        lightIcon.classList.toggle('d-none', theme === 'dark');
        darkIcon.classList.toggle('d-none', theme !== 'dark');
    }

    // Label-based toggle (legacy / schedule_maker)
    const lightLabel = document.querySelector('.theme-label.light-label');
    const darkLabel  = document.querySelector('.theme-label.dark-label');
    if (lightLabel && darkLabel) {
        lightLabel.classList.toggle('active', theme !== 'dark');
        darkLabel.classList.toggle('active', theme === 'dark');
    }

    themeToggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    themeToggle.setAttribute('title',      theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

// ThemeUtils — utilities for theme-aware components (widgets, charts, etc.)
const ThemeUtils = {
    getCurrentTheme() {
        return document.documentElement.getAttribute('data-theme') || 'light';
    },
    isDarkTheme() {
        return this.getCurrentTheme() === 'dark';
    },
    getThemeColor(lightColor, darkColor) {
        return this.isDarkTheme() ? darkColor : lightColor;
    },
    getCSSVariable(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    },
    onThemeChange(callback) {
        document.addEventListener('themeChange', callback);
    },
    offThemeChange(callback) {
        document.removeEventListener('themeChange', callback);
    }
};

window.ThemeUtils = ThemeUtils;

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

/**
 * Global Theme Management
 * Handles light/dark theme switching across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Theme Storage Key - shared across all pages
    const GLOBAL_THEME_STORAGE_KEY = 'jpl_dev_global_theme';
    
    // Load saved theme or default to system preference
    function loadTheme() {
        const savedTheme = localStorage.getItem(GLOBAL_THEME_STORAGE_KEY);
        if (savedTheme) {
            return savedTheme;
        }
        
        // Default to system preference if no saved theme
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }
    
    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(GLOBAL_THEME_STORAGE_KEY, theme);
        
        // Update theme toggle button appearance
        updateThemeToggleButton(theme);
    }
    
    // Update the theme toggle button icons and labels
    function updateThemeToggleButton(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;
        
        const lightLabel = document.querySelector('.theme-label.light-label');
        const darkLabel = document.querySelector('.theme-label.dark-label');
        
        // Update accessible state for the toggle button
        themeToggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
        themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
        themeToggle.setAttribute('title', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
        
        // Update label highlighting
        if (lightLabel && darkLabel) {
            if (theme === 'dark') {
                lightLabel.classList.remove('active');
                darkLabel.classList.add('active');
            } else {
                lightLabel.classList.add('active');
                darkLabel.classList.remove('active');
            }
        }
    }
    
    // Initialize theme
    const currentTheme = loadTheme();
    applyTheme(currentTheme);
    
    // Theme toggle button handler
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }
    
    // Smooth transition for theme changes
    document.documentElement.style.setProperty('--transition-duration', '0.3s');
});

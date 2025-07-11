/**
 * Global Theme Management
 * Handles light/dark theme switching across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Theme Storage Key - shared across all pages
    const GLOBAL_THEME_STORAGE_KEY = 'jpl_dev_global_theme';
    
    // Load saved theme or default to light
    function loadTheme() {
        const savedTheme = localStorage.getItem(GLOBAL_THEME_STORAGE_KEY);
        return savedTheme || 'light';
    }
    
    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(GLOBAL_THEME_STORAGE_KEY, theme);
        
        // Update theme toggle button appearance
        updateThemeToggleButton(theme);
    }
    
    // Update the theme toggle button icons
    function updateThemeToggleButton(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;
        
        const sunIcon = themeToggle.querySelector('.sun-icon');
        const moonIcon = themeToggle.querySelector('.moon-icon');
        
        if (theme === 'dark') {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
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

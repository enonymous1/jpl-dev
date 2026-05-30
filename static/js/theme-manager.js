/**
 * Theme Manager
 * Handles light/dark theme switching with Bootstrap integration
 */

class ThemeManager {
    constructor() {
        this.storageKey = 'jpl-dev-theme';
        this.init();
    }

    init() {
        // Get saved theme or default to light
        const savedTheme = localStorage.getItem(this.storageKey) || 'light';
        this.setTheme(savedTheme);
        
        // Set up theme toggle button
        this.setupThemeToggle();
        
        // Listen for system theme changes
        this.setupSystemThemeListener();
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    }

    setupSystemThemeListener() {
        // Listen for system theme preference changes
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                // Only auto-switch if user hasn't set a preference
                if (!localStorage.getItem(this.storageKey)) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    getCurrentTheme() {
        return document.documentElement.getAttribute('data-bs-theme') || 'light';
    }

    setTheme(theme) {
        // Update HTML data attribute for Bootstrap
        document.documentElement.setAttribute('data-bs-theme', theme);
        
        // Update CSS custom property for existing styles
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update theme toggle button
        this.updateThemeToggleButton(theme);
        
        // Save to localStorage
        localStorage.setItem(this.storageKey, theme);
        
        // Dispatch custom event for other components
        this.dispatchThemeChangeEvent(theme);
        
        // Update meta theme-color for mobile browsers
        this.updateMetaThemeColor(theme);
    }

    toggleTheme() {
        const currentTheme = this.getCurrentTheme();
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    updateThemeToggleButton(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const lightIcon = themeToggle.querySelector('.theme-icon-light');
            const darkIcon = themeToggle.querySelector('.theme-icon-dark');
            
            if (lightIcon && darkIcon) {
                if (theme === 'dark') {
                    lightIcon.classList.add('d-none');
                    darkIcon.classList.remove('d-none');
                    themeToggle.setAttribute('title', 'Switch to light mode');
                } else {
                    lightIcon.classList.remove('d-none');
                    darkIcon.classList.add('d-none');
                    themeToggle.setAttribute('title', 'Switch to dark mode');
                }
            }
        }
    }

    updateMetaThemeColor(theme) {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        const color = theme === 'dark' ? '#1a1a1a' : '#ffffff';
        metaThemeColor.content = color;
    }

    dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themeChange', {
            detail: { theme }
        });
        document.dispatchEvent(event);
    }

    // Auto-detect system preference if no saved preference
    detectSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    // Reset to system preference
    resetToSystemTheme() {
        localStorage.removeItem(this.storageKey);
        const systemTheme = this.detectSystemTheme();
        this.setTheme(systemTheme);
    }

    // Get theme preference with fallback
    getPreferredTheme() {
        const savedTheme = localStorage.getItem(this.storageKey);
        if (savedTheme) {
            return savedTheme;
        }
        return this.detectSystemTheme();
    }
}

// Utility functions for theme-aware components
const ThemeUtils = {
    // Get current theme
    getCurrentTheme() {
        return document.documentElement.getAttribute('data-bs-theme') || 'light';
    },

    // Check if dark theme is active
    isDarkTheme() {
        return this.getCurrentTheme() === 'dark';
    },

    // Get theme-appropriate color
    getThemeColor(lightColor, darkColor) {
        return this.isDarkTheme() ? darkColor : lightColor;
    },

    // Get CSS custom property value
    getCSSVariable(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    },

    // Wait for theme change
    onThemeChange(callback) {
        document.addEventListener('themeChange', callback);
    },

    // Remove theme change listener
    offThemeChange(callback) {
        document.removeEventListener('themeChange', callback);
    }
};

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ThemeManager, ThemeUtils };
} else {
    window.ThemeManager = ThemeManager;
    window.ThemeUtils = ThemeUtils;
}

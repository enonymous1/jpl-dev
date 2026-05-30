/**
 * Widget Utility Functions
 * Helper functions for common widget operations and Bootstrap integration
 */

// Widget Templates for Dynamic Creation
const WidgetTemplates = {
    // Create a Bootstrap card widget
    createCard: function(title, content, options = {}) {
        const cardClass = options.cardClass || 'card h-100 border-0 shadow-sm';
        const headerClass = options.headerClass || 'card-header border-0 bg-transparent';
        const bodyClass = options.bodyClass || 'card-body';
        const footerClass = options.footerClass || 'card-footer border-0 bg-transparent';
        
        return `
            <div class="${cardClass}">
                ${title ? `
                <div class="${headerClass}">
                    <h5 class="card-title mb-0">${title}</h5>
                    ${options.actions ? `<div class="card-actions">${options.actions}</div>` : ''}
                </div>
                ` : ''}
                <div class="${bodyClass}">
                    ${content}
                </div>
                ${options.footer ? `
                <div class="${footerClass}">
                    ${options.footer}
                </div>
                ` : ''}
            </div>
        `;
    },

    // Create a stat display widget
    createStatWidget: function(stats, title = 'Statistics') {
        const statsHTML = stats.map(stat => `
            <div class="text-center">
                <div class="display-6 fw-bold text-primary">${stat.value}</div>
                <div class="text-muted small">${stat.label}</div>
            </div>
        `).join('');

        return this.createCard(title, `
            <div class="row g-3">
                ${stats.map(stat => `
                    <div class="col-${12 / Math.min(stats.length, 4)}">
                        <div class="text-center">
                            <div class="display-6 fw-bold text-primary">${stat.value}</div>
                            <div class="text-muted small">${stat.label}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `);
    },

    // Create a progress bar widget
    createProgressWidget: function(items, title = 'Progress') {
        const progressHTML = items.map(item => `
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-medium">${item.label}</span>
                    <span class="text-muted small">${item.value}%</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar bg-gradient" role="progressbar" 
                         style="width: ${item.value}%" 
                         aria-valuenow="${item.value}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                    </div>
                </div>
            </div>
        `).join('');

        return this.createCard(title, progressHTML);
    },

    // Create a list widget
    createListWidget: function(items, title = 'List', options = {}) {
        const listClass = options.listClass || 'list-group list-group-flush';
        const itemClass = options.itemClass || 'list-group-item border-0 px-0';
        
        const listHTML = `
            <ul class="${listClass}">
                ${items.map(item => `
                    <li class="${itemClass}">
                        ${typeof item === 'string' ? item : item.content}
                    </li>
                `).join('')}
            </ul>
        `;

        return this.createCard(title, listHTML);
    },

    // Create a social links widget
    createSocialWidget: function(links, title = 'Connect') {
        const linksHTML = links.map(link => `
            <a href="${link.url}" class="btn btn-outline-primary btn-sm d-flex align-items-center gap-2 mb-2" 
               target="_blank" rel="noopener">
                <i class="bi bi-${link.icon}"></i>
                ${link.label}
            </a>
        `).join('');

        return this.createCard(title, `<div class="d-grid gap-2">${linksHTML}</div>`);
    }
};

// Widget Animation Utilities
const WidgetAnimations = {
    // Animate number counting
    countUp: function(element, target, duration = 1000) {
        const start = parseInt(element.textContent) || 0;
        const range = target - start;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (range * progress));
            
            element.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    },

    // Animate progress bars
    animateProgressBars: function(container, delay = 200) {
        const progressBars = container.querySelectorAll('.progress-bar');
        progressBars.forEach((bar, index) => {
            setTimeout(() => {
                const width = bar.style.width;
                bar.style.width = '0%';
                bar.style.transition = 'width 1s ease-out';
                
                setTimeout(() => {
                    bar.style.width = width;
                }, 50);
            }, index * delay);
        });
    },

    // Fade in animation
    fadeIn: function(element, duration = 500) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease-in-out`;
        
        setTimeout(() => {
            element.style.opacity = '1';
        }, 10);
    },

    // Slide in animation
    slideIn: function(element, direction = 'up', duration = 500) {
        const transforms = {
            up: 'translateY(20px)',
            down: 'translateY(-20px)',
            left: 'translateX(20px)',
            right: 'translateX(-20px)'
        };

        element.style.transform = transforms[direction];
        element.style.opacity = '0';
        element.style.transition = `all ${duration}ms ease-out`;
        
        setTimeout(() => {
            element.style.transform = 'translate(0)';
            element.style.opacity = '1';
        }, 10);
    }
};

// Bootstrap Integration Utilities
const BootstrapUtils = {
    // Create a Bootstrap modal
    createModal: function(id, title, content, options = {}) {
        const size = options.size ? `modal-${options.size}` : '';
        const centered = options.centered ? 'modal-dialog-centered' : '';
        
        return `
            <div class="modal fade" id="${id}" tabindex="-1" aria-labelledby="${id}Label" aria-hidden="true">
                <div class="modal-dialog ${size} ${centered}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="${id}Label">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        ${options.footer ? `
                        <div class="modal-footer">
                            ${options.footer}
                        </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    },

    // Create a Bootstrap toast
    createToast: function(id, title, message, type = 'info') {
        const bgClass = {
            success: 'bg-success',
            error: 'bg-danger',
            warning: 'bg-warning',
            info: 'bg-primary'
        }[type] || 'bg-primary';

        return `
            <div class="toast align-items-center text-white ${bgClass} border-0" id="${id}" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>${title}</strong><br>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
    },

    // Show a toast notification
    showToast: function(title, message, type = 'info', duration = 5000) {
        const toastId = 'toast-' + Date.now();
        const toastHTML = this.createToast(toastId, title, message, type);
        
        // Create toast container if it doesn't exist
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        
        container.insertAdjacentHTML('beforeend', toastHTML);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            delay: duration
        });
        
        toast.show();
        
        // Remove from DOM after hiding
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },

    // Create a Bootstrap alert
    createAlert: function(message, type = 'info', dismissible = true) {
        const alertClass = `alert alert-${type}`;
        const dismissButton = dismissible ? `
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        ` : '';
        
        return `
            <div class="${alertClass} ${dismissible ? 'alert-dismissible' : ''}" role="alert">
                ${message}
                ${dismissButton}
            </div>
        `;
    }
};

// Theme-aware utilities
const ThemeAwareUtils = {
    // Get theme-appropriate classes
    getThemeClasses: function(lightClasses, darkClasses) {
        const theme = document.documentElement.getAttribute('data-bs-theme');
        return theme === 'dark' ? darkClasses : lightClasses;
    },

    // Get theme-appropriate colors
    getThemeColors: function() {
        const theme = document.documentElement.getAttribute('data-bs-theme');
        return {
            primary: theme === 'dark' ? '#4dabf7' : '#007bff',
            secondary: theme === 'dark' ? '#6c757d' : '#6c757d',
            success: theme === 'dark' ? '#51cf66' : '#28a745',
            danger: theme === 'dark' ? '#ff6b6b' : '#dc3545',
            warning: theme === 'dark' ? '#ffd43b' : '#ffc107',
            info: theme === 'dark' ? '#74c0fc' : '#17a2b8',
            light: theme === 'dark' ? '#495057' : '#f8f9fa',
            dark: theme === 'dark' ? '#f8f9fa' : '#343a40'
        };
    },

    // Update chart colors based on theme
    updateChartColors: function(chart) {
        const colors = this.getThemeColors();
        // Implementation would depend on the charting library used
        console.log('Update chart colors for theme:', colors);
    }
};

// Intersection Observer utilities for animations
const ObserverUtils = {
    // Observe elements for scroll animations
    observeElements: function(selector, callback, options = {}) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '50px',
            ...options
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    callback(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll(selector).forEach(el => observer.observe(el));
        
        return observer;
    },

    // Animate elements when they come into view
    animateOnScroll: function(selector, animationType = 'fadeIn') {
        this.observeElements(selector, (element) => {
            switch (animationType) {
                case 'fadeIn':
                    WidgetAnimations.fadeIn(element);
                    break;
                case 'slideIn':
                    WidgetAnimations.slideIn(element);
                    break;
                case 'countUp':
                    const target = parseInt(element.dataset.target) || parseInt(element.textContent);
                    WidgetAnimations.countUp(element, target);
                    break;
                case 'progressBar':
                    WidgetAnimations.animateProgressBars(element);
                    break;
            }
        });
    }
};

// Export utilities for global use
if (typeof window !== 'undefined') {
    window.WidgetTemplates = WidgetTemplates;
    window.WidgetAnimations = WidgetAnimations;
    window.BootstrapUtils = BootstrapUtils;
    window.ThemeAwareUtils = ThemeAwareUtils;
    window.ObserverUtils = ObserverUtils;
}

// Auto-initialize common animations
document.addEventListener('DOMContentLoaded', function() {
    // Animate stats on scroll
    ObserverUtils.animateOnScroll('.stat-value', 'countUp');
    
    // Animate progress bars on scroll
    ObserverUtils.animateOnScroll('.widget-skills', 'progressBar');
    
    // Fade in cards on scroll
    ObserverUtils.animateOnScroll('.card', 'fadeIn');
    
    // Update hover effects for cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

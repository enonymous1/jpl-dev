/**
 * Widget Manager with GridStack.js Integration
 * Handles widget layout, drag-and-drop, and state management
 */

class WidgetManager {
    constructor(containerId = 'grid-stack-container') {
        this.containerId = containerId;
        this.grid = null;
        this.widgets = new Map();
        this.storageKey = 'jpl-dev-widget-layout';
        this.init();
    }

    init() {
        this.setupGridStack();
        this.loadWidgetLayout();
        this.setupEventListeners();
    }

    setupGridStack() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.warn(`GridStack container with id "${this.containerId}" not found`);
            return;
        }

        // Initialize GridStack
        this.grid = GridStack.init({
            cellHeight: 120,
            minRow: 1,
            float: true,
            resizable: {
                handles: 'se'
            },
            draggable: {
                handle: '.widget-handle'
            },
            margin: 10,
            animate: true
        }, container);

        // Listen for changes
        this.grid.on('change', (event, items) => {
            this.saveWidgetLayout();
        });

        this.grid.on('resizestop', (event, element) => {
            this.handleWidgetResize(element);
        });

        this.grid.on('dragstop', (event, element) => {
            this.handleWidgetMove(element);
        });
    }

    setupEventListeners() {
        // Listen for window resize to adjust grid
        window.addEventListener('resize', () => {
            if (this.grid) {
                this.grid.compact();
            }
        });

        // Listen for theme changes to update widget styles
        document.addEventListener('themeChange', (event) => {
            this.updateWidgetStyles(event.detail.theme);
        });
    }

    // Widget Creation and Management
    createWidget(type, config = {}) {
        const widgetId = config.id || `widget-${Date.now()}`;
        const widget = this.generateWidgetHTML(type, widgetId, config);
        
        // Add to GridStack
        const gridOptions = {
            w: config.width || 4,
            h: config.height || 3,
            x: config.x || 0,
            y: config.y || 0,
            id: widgetId,
            content: widget
        };

        const element = this.grid.addWidget(gridOptions);
        this.widgets.set(widgetId, { type, config, element });
        
        // Initialize widget functionality
        this.initializeWidget(widgetId, type, element);
        
        return widgetId;
    }

    generateWidgetHTML(type, id, config) {
        const templates = {
            profile: this.generateProfileWidget,
            stats: this.generateStatsWidget,
            projects: this.generateProjectsWidget,
            skills: this.generateSkillsWidget,
            social: this.generateSocialWidget,
            calendar: this.generateCalendarWidget,
            chart: this.generateChartWidget
        };

        const generator = templates[type];
        if (!generator) {
            throw new Error(`Unknown widget type: ${type}`);
        }

        return generator.call(this, id, config);
    }

    generateProfileWidget(id, config) {
        return `
            <div class="widget widget-profile" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Profile'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <img src="${config.image || 'https://via.placeholder.com/80'}" alt="Profile" class="profile-image">
                    <h4 class="profile-name">${config.name || 'John Doe'}</h4>
                    <p class="profile-title">${config.title || 'Developer'}</p>
                    <p class="text-muted">${config.description || 'Software developer and technology enthusiast.'}</p>
                </div>
            </div>
        `;
    }

    generateStatsWidget(id, config) {
        const stats = config.stats || [
            { label: 'Projects', value: '12' },
            { label: 'Years Exp', value: '5+' },
            { label: 'Technologies', value: '15' }
        ];

        const statsHTML = stats.map(stat => `
            <div class="stat-item">
                <h3 class="stat-value">${stat.value}</h3>
                <p class="stat-label">${stat.label}</p>
            </div>
        `).join('');

        return `
            <div class="widget widget-stats" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Quick Stats'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="stats-grid">
                        ${statsHTML}
                    </div>
                </div>
            </div>
        `;
    }

    generateProjectsWidget(id, config) {
        const projects = config.projects || [
            { name: 'Project 1', status: 'active', description: 'Description here', tech: ['React', 'Node.js'] },
            { name: 'Project 2', status: 'development', description: 'Another project', tech: ['Python', 'Flask'] }
        ];

        const projectsHTML = projects.map(project => `
            <div class="project-card-compact">
                <div class="project-header-compact">
                    <h5 class="project-title-compact">${project.name}</h5>
                    <span class="project-status-badge ${project.status}">${project.status}</span>
                </div>
                <p class="project-description-compact">${project.description}</p>
                <div class="project-tech-tags">
                    ${project.tech.map(tech => `<span class="tech-tag-compact">${tech}</span>`).join('')}
                </div>
                <a href="#" class="project-link-compact">View Project <i class="bi bi-arrow-right"></i></a>
            </div>
        `).join('');

        return `
            <div class="widget widget-projects" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Featured Projects'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content scroll">
                    ${projectsHTML}
                </div>
            </div>
        `;
    }

    generateSkillsWidget(id, config) {
        const skills = config.skills || [
            { name: 'JavaScript', level: 90 },
            { name: 'Python', level: 85 },
            { name: 'React', level: 80 },
            { name: 'Node.js', level: 75 }
        ];

        const skillsHTML = skills.map(skill => `
            <div class="skill-item">
                <span class="skill-name">${skill.name}</span>
                <div class="skill-bar">
                    <div class="skill-progress" style="width: ${skill.level}%"></div>
                </div>
                <span class="skill-percentage">${skill.level}%</span>
            </div>
        `).join('');

        return `
            <div class="widget widget-skills" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Skills'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="skills-grid">
                        ${skillsHTML}
                    </div>
                </div>
            </div>
        `;
    }

    generateSocialWidget(id, config) {
        const links = config.links || [
            { name: 'GitHub', url: '#', icon: 'github' },
            { name: 'LinkedIn', url: '#', icon: 'linkedin' },
            { name: 'Twitter', url: '#', icon: 'twitter' }
        ];

        const linksHTML = links.map(link => `
            <a href="${link.url}" class="social-link" target="_blank" rel="noopener">
                <i class="bi bi-${link.icon} social-icon"></i>
                <span class="social-label">${link.name}</span>
            </a>
        `).join('');

        return `
            <div class="widget widget-social" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Connect'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="social-links">
                        ${linksHTML}
                    </div>
                </div>
            </div>
        `;
    }

    generateCalendarWidget(id, config) {
        return `
            <div class="widget widget-calendar" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Calendar'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="calendar-header">
                        <button class="calendar-nav-btn" onclick="widgetManager.navigateCalendar('${id}', -1)">
                            <i class="bi bi-chevron-left"></i>
                        </button>
                        <span class="calendar-title">December 2024</span>
                        <button class="calendar-nav-btn" onclick="widgetManager.navigateCalendar('${id}', 1)">
                            <i class="bi bi-chevron-right"></i>
                        </button>
                    </div>
                    <div class="calendar-grid">
                        <!-- Calendar content will be rendered here -->
                        <p class="text-center text-muted">Calendar view</p>
                    </div>
                </div>
            </div>
        `;
    }

    generateChartWidget(id, config) {
        return `
            <div class="widget widget-chart" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${config.title || 'Analytics'}</h3>
                    <div class="widget-actions">
                        <button class="widget-action-btn widget-handle" title="Drag to move">
                            <i class="bi bi-grip-vertical"></i>
                        </button>
                        <button class="widget-action-btn" onclick="widgetManager.removeWidget('${id}')" title="Remove widget">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
                <div class="widget-content">
                    <div class="chart-container">
                        <!-- Chart will be rendered here -->
                        <p class="text-center text-muted">Chart visualization</p>
                    </div>
                </div>
            </div>
        `;
    }

    initializeWidget(id, type, element) {
        // Initialize widget-specific functionality
        switch (type) {
            case 'skills':
                this.animateSkillBars(element);
                break;
            case 'chart':
                this.initializeChart(element);
                break;
            case 'calendar':
                this.initializeCalendar(element);
                break;
        }
    }

    animateSkillBars(element) {
        const skillBars = element.querySelectorAll('.skill-progress');
        skillBars.forEach((bar, index) => {
            setTimeout(() => {
                bar.style.transition = 'width 1s ease-out';
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }, index * 200);
        });
    }

    initializeChart(element) {
        // Placeholder for chart initialization
        // Could integrate with Chart.js or other charting library
    }

    initializeCalendar(element) {
        // Placeholder for calendar initialization
    }

    removeWidget(id) {
        const widget = this.widgets.get(id);
        if (widget) {
            this.grid.removeWidget(widget.element);
            this.widgets.delete(id);
            this.saveWidgetLayout();
        }
    }

    handleWidgetResize(element) {
        const widgetId = element.querySelector('[data-widget-id]')?.getAttribute('data-widget-id');
        if (widgetId) {
            // Handle any resize-specific logic
            this.saveWidgetLayout();
        }
    }

    handleWidgetMove(element) {
        const widgetId = element.querySelector('[data-widget-id]')?.getAttribute('data-widget-id');
        if (widgetId) {
            // Handle any move-specific logic
            this.saveWidgetLayout();
        }
    }

    updateWidgetStyles(theme) {
        // Update widget styles based on theme
        this.widgets.forEach((widget, id) => {
            const element = widget.element;
            if (theme === 'dark') {
                element.classList.add('dark-theme');
            } else {
                element.classList.remove('dark-theme');
            }
        });
    }

    // Layout Persistence
    saveWidgetLayout() {
        if (!this.grid) return;

        const layout = this.grid.engine.nodes.map(node => ({
            id: node.id,
            x: node.x,
            y: node.y,
            w: node.w,
            h: node.h,
            type: this.widgets.get(node.id)?.type
        }));

        localStorage.setItem(this.storageKey, JSON.stringify(layout));
    }

    loadWidgetLayout() {
        const savedLayout = localStorage.getItem(this.storageKey);
        if (savedLayout) {
            try {
                const layout = JSON.parse(savedLayout);
                // Note: This would typically restore widgets from saved layout
                // Implementation depends on specific requirements
            } catch (e) {
                console.warn('Failed to load widget layout:', e);
            }
        }
    }

    clearWidgetLayout() {
        localStorage.removeItem(this.storageKey);
        this.widgets.clear();
        if (this.grid) {
            this.grid.removeAll();
        }
    }

    // Utility Methods
    getWidget(id) {
        return this.widgets.get(id);
    }

    getAllWidgets() {
        return Array.from(this.widgets.values());
    }

    getGridLayout() {
        return this.grid ? this.grid.engine.nodes : [];
    }

    // Navigation helper for calendar widget
    navigateCalendar(widgetId, direction) {
        // Implementation for calendar navigation
        console.log(`Navigate calendar ${widgetId} by ${direction} month(s)`);
    }
}

// Initialize widget manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if GridStack container exists
    if (document.getElementById('grid-stack-container')) {
        window.widgetManager = new WidgetManager();
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WidgetManager;
} else {
    window.WidgetManager = WidgetManager;
}

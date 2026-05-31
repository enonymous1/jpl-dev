/**
 * Widget Manager with GridStack.js Integration
 * Handles widget layout, drag-and-drop, and state management
 */

// Escape HTML entities — prevents XSS when config values are interpolated into innerHTML. (F5a)
function _escHtml(s) {
    if (s == null) return '';
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Block dangerous URL schemes (javascript:, vbscript:, data:) in href/src. (F5a)
function _safeUrl(url) {
    if (typeof url !== 'string') return '#';
    const t = url.trim().toLowerCase();
    if (t.startsWith('javascript:') || t.startsWith('vbscript:') || t.startsWith('data:')) return '#';
    return url;
}

class WidgetManager {
    constructor(containerId = 'grid-stack-container', options = {}) {
        this.containerId = containerId;
        this.grid = null;
        this.widgets = new Map();
        this.options = options;
        this.init();
    }

    init() {
        this.setupGridStack();
        this.setupEventListeners();
    }

    setupGridStack() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.warn(`GridStack container with id "${this.containerId}" not found`);
            return;
        }

        // Initialize GridStack
        this.grid = GridStack.init(Object.assign({
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
        }, this.options), container);

        // Listen for changes
        this.grid.on('change', (event, items) => {
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
        // F5c: Strip non-alphanumeric chars from caller-supplied IDs before use in HTML attribute context.
        const rawId = config.id || `widget-${Date.now()}`;
        const widgetId = rawId.replace(/[^a-zA-Z0-9_-]/g, '');
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
                    <h3 class="widget-title">${_escHtml(config.title || 'Profile')}</h3>
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
                    <img src="${_escHtml(_safeUrl(config.image || 'https://via.placeholder.com/80'))}" alt="Profile" class="profile-image">
                    <h4 class="profile-name">${_escHtml(config.name || 'John Doe')}</h4>
                    <p class="profile-title">${_escHtml(config.title || 'Developer')}</p>
                    <p class="text-muted">${_escHtml(config.description || 'Software developer and technology enthusiast.')}</p>
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
                <h3 class="stat-value">${_escHtml(stat.value)}</h3>
                <p class="stat-label">${_escHtml(stat.label)}</p>
            </div>
        `).join('');

        return `
            <div class="widget widget-stats" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${_escHtml(config.title || 'Quick Stats')}</h3>
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
                    <h5 class="project-title-compact">${_escHtml(project.name)}</h5>
                    <span class="project-status-badge ${_escHtml(project.status)}">${_escHtml(project.status)}</span>
                </div>
                <p class="project-description-compact">${_escHtml(project.description)}</p>
                <div class="project-tech-tags">
                    ${project.tech.map(tech => `<span class="tech-tag-compact">${_escHtml(tech)}</span>`).join('')}
                </div>
                <a href="#" class="project-link-compact">View Project <i class="bi bi-arrow-right"></i></a>
            </div>
        `).join('');

        return `
            <div class="widget widget-projects" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${_escHtml(config.title || 'Featured Projects')}</h3>
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
                <span class="skill-name">${_escHtml(skill.name)}</span>
                <div class="skill-bar">
                    <div class="skill-progress" style="width: ${_escHtml(skill.level)}%"></div>
                </div>
                <span class="skill-percentage">${_escHtml(skill.level)}%</span>
            </div>
        `).join('');

        return `
            <div class="widget widget-skills" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${_escHtml(config.title || 'Skills')}</h3>
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
            <a href="${_escHtml(_safeUrl(link.url))}" class="social-link" target="_blank" rel="noopener">
                <i class="bi bi-${_escHtml(link.icon)} social-icon"></i>
                <span class="social-label">${_escHtml(link.name)}</span>
            </a>
        `).join('');

        return `
            <div class="widget widget-social" data-widget-id="${id}">
                <div class="widget-header">
                    <h3 class="widget-title">${_escHtml(config.title || 'Connect')}</h3>
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
                    <h3 class="widget-title">${_escHtml(config.title || 'Calendar')}</h3>
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
                    <h3 class="widget-title">${_escHtml(config.title || 'Analytics')}</h3>
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
        }
    }

    handleWidgetResize(element) {
        const widgetId = element.querySelector('[data-widget-id]')?.getAttribute('data-widget-id');
        if (widgetId) {
            // Handle any resize-specific logic
        }
    }

    handleWidgetMove(element) {
        const widgetId = element.querySelector('[data-widget-id]')?.getAttribute('data-widget-id');
        if (widgetId) {
            // Handle any move-specific logic
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

// WidgetManager is instantiated explicitly by pages that use it (e.g. index.html).
// No auto-init here — each page passes its own GridStack options via the constructor.

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WidgetManager;
} else {
    window.WidgetManager = WidgetManager;
}

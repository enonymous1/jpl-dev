#!/usr/bin/env python3
"""
JPL Development Portfolio - Flask Web Application

A Flask-based web application showcasing development projects and tools.
This application supports both live development and static site generation
for deployment to GitHub Pages.

Features:
- Modular project architecture using Flask Blueprints
- Static site generation with Flask-Frozen
- Custom template filters for enhanced rendering
- Responsive design with modern CSS architecture

Author: JPL Development
Date: July 2025
"""

import importlib
import logging
import os
import pkgutil

from flask import Flask, Blueprint, render_template
from flask_frozen import Freezer
from config.data_access import get_all_projects
from config.models import ProjectStatus

logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Configure Flask-Frozen for static site generation
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = True
# Protect manually-placed files in docs/ from being deleted on local freeze runs.
# FREEZER_REMOVE_EXTRA_FILES defaults to True — without this, `python freeze.py`
# silently deletes docs/CNAME, breaking the custom domain until CI re-injects it.
app.config['FREEZER_DESTINATION_IGNORE'] = ['CNAME']

# Initialize the static site generator
freezer = Freezer(app)

# ============================================================================
# BLUEPRINT REGISTRATION
# ============================================================================

def register_project_blueprints(application, strict=False):
    """Auto-discover and register project blueprints from the projects package.

    Args:
        strict: When True, re-raises import errors instead of continuing. Use
                this in CI / freeze.py to surface broken blueprints before they
                produce a silent gap in the generated site.
    """
    project_package = 'projects'
    project_path = os.path.join(os.path.dirname(__file__), 'projects')

    for finder, name, ispkg in pkgutil.iter_modules([project_path]):
        if name.startswith('_'):
            continue

        module_name = f'{project_package}.{name}'
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            logger.error('Failed to import project module %s: %s', module_name, exc)
            if strict:
                raise
            continue

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                if attr.name in application.blueprints:
                    continue
                application.register_blueprint(attr)
                logger.info('Registered blueprint: %s from %s.%s', attr.name, module_name, attr_name)


# Use strict mode during freeze/CI builds (FLASK_BLUEPRINT_STRICT=1) so any
# broken blueprint raises immediately rather than silently dropping a route. (B1c)
_blueprint_strict = os.environ.get('FLASK_BLUEPRINT_STRICT', '0') == '1'
register_project_blueprints(app, strict=_blueprint_strict)


# ============================================================================
# CUSTOM TEMPLATE FILTERS
# ============================================================================

@app.template_filter('nl2br')
def nl2br_filter(text):
    """
    Convert newline characters to HTML line breaks.
    
    This custom Jinja2 filter transforms plain text newlines (\n) into
    HTML <br> tags, preserving line breaks when rendering text in templates.
    
    Args:
        text (str or None): The input text to process
        
    Returns:
        str: Text with newlines converted to HTML breaks, or empty string if input is None
        
    Example:
        In template: {{ some_text | nl2br | safe }}
        Input: "Line 1\nLine 2"
        Output: "Line 1<br>\nLine 2"
    """
    if text is None:
        return ''
    return text.replace('\n', '<br>\n')


# ============================================================================
# ROUTE DEFINITIONS
# ============================================================================

@app.route('/')
def index():
    """
    Render the main homepage.
    
    Returns:
        str: Rendered HTML template for the homepage
    """
    return render_template('index.html')


@app.route('/projects/')
def projects():
    """
    Render the projects overview page.
    
    This page displays a list of all available project demonstrations
    and tools in the portfolio, loaded from the projects_data configuration.
    
    Returns:
        str: Rendered HTML template for the projects page with project data
    """
    projects_list = get_all_projects()
    return render_template('projects.html', projects=projects_list, ProjectStatus=ProjectStatus)


@app.route('/widget-demo/')
def widget_demo():
    """
    Render the widget system demonstration page.
    
    This page showcases the Bootstrap and GridStack.js widget system
    with interactive examples and controls for testing widget functionality.
    
    Returns:
        str: Rendered HTML template for the widget demo page
    """
    return render_template('widget_demo.html')


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Run the Flask development server only when FLASK_ENV=development.
    # Production deployment uses the static files generated by freeze.py.
    debug_mode = os.environ.get('FLASK_ENV', '').lower() == 'development'
    app.run(debug=debug_mode)

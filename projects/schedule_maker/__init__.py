#!/usr/bin/env python3
"""
Schedule Maker Blueprint

Flask blueprint for the Schedule Maker project - a tool for creating and managing schedules.

Author: JPL Development
Date: July 2025
"""

from flask import Blueprint

# Create the blueprint
schedule_maker_bp = Blueprint(
    'schedule_maker',
    __name__,
    url_prefix='/projects/schedule-maker',
    template_folder='templates',
    static_folder='../../static/projects/schedule_maker'
)

# Import routes after blueprint creation to avoid circular imports
from . import routes

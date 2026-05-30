#!/usr/bin/env python3
"""
Schedule Maker Routes

Flask routes for the Schedule Maker project.

Author: JPL Development
Date: July 2025
"""

from flask import render_template
from . import schedule_maker_bp


@schedule_maker_bp.route('/')
def schedule_maker():
    """
    Render the main Schedule Maker application.

    This project uses client-side persistence to stay compatible with static
    deployment on GitHub Pages. Saved schedules are stored in browser storage
    and exported as JSON files, so no backend save/load API is required.

    Returns:
        str: Rendered HTML template for the Schedule Maker
    """
    return render_template('schedule_maker.html')

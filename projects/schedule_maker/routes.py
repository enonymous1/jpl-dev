#!/usr/bin/env python3
"""
Schedule Maker Routes

Flask routes for the Schedule Maker project.

Author: JPL Development
Date: July 2025
"""

from flask import render_template, request, jsonify
from . import schedule_maker_bp


@schedule_maker_bp.route('/')
def schedule_maker():
    """
    Render the main Schedule Maker application.
    
    Returns:
        str: Rendered HTML template for the Schedule Maker
    """
    return render_template('schedule_maker.html')


@schedule_maker_bp.route('/api/save-schedule', methods=['POST'])
def save_schedule():
    """
    API endpoint to save schedule data.
    
    This endpoint handles saving schedule configurations sent from the frontend.
    In a production environment, this would save to a database.
    
    Returns:
        JSON: Response indicating success or failure
    """
    try:
        schedule_data = request.get_json()
        
        # Validate required fields
        if not schedule_data or 'name' not in schedule_data:
            return jsonify({'error': 'Schedule name is required'}), 400
        
        # In a real application, you would save to a database here
        # For now, we'll just return success
        
        return jsonify({
            'success': True,
            'message': 'Schedule saved successfully',
            'schedule_id': 'temp_id_123'  # Would be actual ID from database
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@schedule_maker_bp.route('/api/load-schedule/<schedule_id>')
def load_schedule(schedule_id):
    """
    API endpoint to load a saved schedule.
    
    Args:
        schedule_id (str): The ID of the schedule to load
        
    Returns:
        JSON: Schedule data or error message
    """
    try:
        # In a real application, you would load from a database here
        # For now, return a sample schedule
        
        sample_schedule = {
            'id': schedule_id,
            'name': 'Sample Schedule',
            'description': 'A sample schedule for demonstration',
            'events': [
                {
                    'id': '1',
                    'title': 'Sample Event',
                    'start_time': '09:00',
                    'end_time': '10:00',
                    'description': 'This is a sample event'
                }
            ],
            'created_at': '2025-07-11T10:00:00Z'
        }
        
        return jsonify(sample_schedule)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

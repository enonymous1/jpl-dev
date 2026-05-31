"""
GSA MAS Checklist Routes

Flask routes for the GSA MAS Checklist project.
"""

from flask import render_template
from . import gsa_mas_checklist_bp, load_checklist_data, create_pdf_link


@gsa_mas_checklist_bp.route('/')
def gsa_mas_checklist():
    """Main route handler for the GSA MAS Checklist project."""
    data = load_checklist_data()

    # Group items by section while preserving order
    ordered_sections = []
    section_map = {}
    for item in data:
        section_name = item['Section']
        if section_name not in section_map:
            section_map[section_name] = []
            ordered_sections.append({'name': section_name, 'item_list': section_map[section_name]})
        section_map[section_name].append(item)

    return render_template(
        'gsa_mas_checklist.html',
        sections=ordered_sections,
        create_pdf_link=create_pdf_link,
    )

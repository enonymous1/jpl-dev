"""
GSA MAS Checklist Blueprint

Flask blueprint for the Interactive GSA MAS New Offeror Checklist project,
including route handlers, data loading helpers, and provision text lookups.
"""

from flask import Blueprint, current_app, g, url_for
import json
import os
from functools import lru_cache

gsa_mas_checklist_bp = Blueprint(
    'gsa_mas_checklist',
    __name__,
    url_prefix='/projects/gsa-mas-checklist',
    template_folder='templates',
)

# ---------------------------------------------------------------------------
# D2a: PROVISION_TEXT_MAP externalized to provision_text.json.
# Edit the JSON file to change legal text without touching Python.
# Loaded once per process via lru_cache.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_provision_text() -> dict:
    """Load provision text from JSON file. Cached once per process."""
    data_path = os.path.join(
        current_app.root_path,
        'static', 'projects', 'gsa_mas_checklist', 'data', 'provision_text.json'
    )
    with open(data_path, encoding='utf-8') as f:
        return json.load(f)


def get_provision_text(reference_text):
    """Get provision text using direct lookup from provision_text.json."""
    if not reference_text:
        return "No reference provided."
    ref_key = reference_text.replace('Provision SCP-FSS-001', '').strip()
    return load_provision_text().get(ref_key, f'Could not find provision text for reference: "{ref_key}"')


def create_pdf_link(reference_text, pdf_filename):
    """Create a PDF link and get content using direct lookup.

    D3b: url_for() is called at most once per request per unique pdf_filename.
    The resolved URL is cached on flask.g so repeated calls across checklist
    items (O(n_items)) do not each invoke url_for().
    """
    if not reference_text or 'SCP-FSS-001' not in reference_text:
        return {'link': reference_text, 'content': None}
    # Cache the url_for result on g; all checklist items share the same URL.
    cache_key = f'_pdf_url_{pdf_filename}'
    if not hasattr(g, cache_key):
        setattr(g, cache_key, url_for('static', filename=f'projects/gsa_mas_checklist/files/{pdf_filename}'))
    pdf_url = getattr(g, cache_key)
    pdf_link = reference_text.replace('SCP-FSS-001', f'<a href="{pdf_url}" target="_blank" class="pdf-link">SCP-FSS-001</a>')
    pdf_content = get_provision_text(reference_text)
    return {'link': pdf_link, 'content': pdf_content}


@lru_cache(maxsize=1)
def load_checklist_data():
    """Load the checklist data from the project-specific JSON file. Cached once per process."""
    data_path = os.path.join(
        current_app.root_path,
        'static', 'projects', 'gsa_mas_checklist', 'data', 'checklist_data.json'
    )
    with open(data_path, encoding='utf-8') as f:
        return json.load(f)


# Import routes after blueprint creation to avoid circular imports
from . import routes

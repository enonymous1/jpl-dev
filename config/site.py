#!/usr/bin/env python3
"""Site identity: the single source of truth for values used across the app.

``app.py``, ``freeze.py``, ``fetch_repos.py`` and the templates all used to
derive these independently (same env var, same default, same ``rstrip``),
which is how a renamed user or a moved domain drifts out of sync one file
at a time. Import from here; never re-derive them elsewhere.
"""

import os

SITE_URL = os.environ.get('SITE_URL', 'https://justinlyons.dev').rstrip('/')
GITHUB_USER = os.environ.get('GITHUB_USER', 'enonymous1')
LINKEDIN_SLUG = os.environ.get('LINKEDIN_SLUG', 'justinplyons')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'justin@jpl-dev.com')

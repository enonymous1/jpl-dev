#!/usr/bin/env python3
"""
Static Site Generator for the JPL Development Portfolio.

This script uses Flask-Frozen to crawl the Flask application and generate a
static version suitable for GitHub Pages deployment. It is intended to run at
build time and produce flat HTML/CSS/JS output in the configured output
directory.
"""

import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Enable strict blueprint registration: any import error raises immediately
# instead of being swallowed, so a broken blueprint fails the build visibly
# rather than silently dropping a route from the generated site. (B1c)
os.environ.setdefault('FLASK_BLUEPRINT_STRICT', '1')

from app import freezer

logger = logging.getLogger(__name__)


def _warn_about_dynamic_routes():
    """
    Inspect the Flask URL map for parameterized routes.

    Flask-Frozen cannot freeze routes containing URL parameters without an
    explicit generator. This helper reports any dynamic rules so the build
    author can add a corresponding @freezer.register_generator handler.
    """
    dynamic_rules = [
        rule for rule in freezer.app.url_map.iter_rules()
        if '<' in rule.rule and rule.endpoint != 'static'
    ]
    if dynamic_rules:
        logger.warning('Parameterized dynamic routes detected:')
        for rule in dynamic_rules:
            logger.warning('  - %s: %s', rule.endpoint, rule.rule)
        logger.warning(
            'Add a custom @freezer.register_generator function in freeze.py to handle these endpoints.'
        )
    else:
        logger.info('No parameterized dynamic routes found. Static freezing is safe for current app.')


def main():
    """
    Generate the static site using Flask-Frozen.

    This function performs a build-time freeze of the Flask application,
    rendering every discovered route to static HTML and copying static assets.

    Raises:
        Exception: If static generation fails for any reason.
    """
    try:
        logger.info('Starting static site generation...')
        _warn_about_dynamic_routes()
        freezer.freeze()
        logger.info('✓ Static site generated successfully in docs/ directory')
        logger.info('  Ready for GitHub Pages deployment')
    except Exception:
        logger.exception('✗ Error during static site generation')
        raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        main()
    except Exception:
        sys.exit(1)
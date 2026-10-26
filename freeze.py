#!/usr/bin/env python3
"""
Static Site Generator for the JPL Development Portfolio.

This script uses Flask-Frozen to crawl the Flask application and generate a
static version suitable for GitHub Pages deployment. It is intended to run at
build time and produce flat HTML/CSS/JS output in the configured output
directory.

After freezing it also writes the files Flask-Frozen does not generate on
its own: ``404.html`` (served by GitHub Pages for unknown paths),
``robots.txt`` and ``sitemap.xml`` (both built from the frozen routes).
"""

import logging
import os
import sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Enable strict blueprint registration: any import error raises immediately
# instead of being swallowed, so a broken blueprint fails the build visibly
# rather than silently dropping a route from the generated site. (B1c)
os.environ.setdefault('FLASK_BLUEPRINT_STRICT', '1')

from app import freezer  # noqa: E402

logger = logging.getLogger(__name__)

SITE_URL = os.environ.get('SITE_URL', 'https://justinlyons.dev').rstrip('/')


def _warn_about_dynamic_routes():
    """
    Inspect the Flask URL map for parameterized routes.

    Flask-Frozen cannot freeze routes containing URL parameters without an
    explicit generator. This helper reports any dynamic rules so the build
    author can add a corresponding @freezer.register_generator handler.
    """
    dynamic_rules = [
        rule
        for rule in freezer.app.url_map.iter_rules()
        if '<' in rule.rule and rule.endpoint != 'static'
    ]
    if dynamic_rules:
        logger.warning('Parameterized dynamic routes detected:')
        for rule in dynamic_rules:
            logger.warning('  - %s: %s', rule.endpoint, rule.rule)
        logger.warning(
            'Add a custom @freezer.register_generator function in freeze.py '
            'to handle these endpoints.'
        )
    else:
        logger.info(
            'No parameterized dynamic routes found. Static freezing is safe for current app.'
        )


def _static_routes():
    """All frozen, parameter-free routes except the static endpoint itself."""
    routes = []
    for rule in freezer.app.url_map.iter_rules():
        if rule.endpoint == 'static' or '<' in rule.rule:
            continue
        routes.append(rule.rule)
    return sorted(set(routes))


def _write_static_extras(destination):
    """Write 404.html, robots.txt and sitemap.xml into the frozen output."""
    # 404: render through the app so it shares base.html, then write it flat.
    # GitHub Pages serves docs/404.html for any unknown path.
    with freezer.app.test_request_context():
        from flask import render_template

        not_found = render_template('404.html')
    with open(os.path.join(destination, '404.html'), 'w', encoding='utf-8') as f:
        f.write(not_found)

    with open(os.path.join(destination, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')

    routes = _static_routes()
    today = date.today().isoformat()
    urls = ''.join(
        f'  <url><loc>{SITE_URL}{route}</loc><lastmod>{today}</lastmod></url>\n' for route in routes
    )
    with open(os.path.join(destination, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f'{urls}</urlset>\n'
        )
    logger.info('Wrote 404.html, robots.txt and sitemap.xml (%d routes)', len(routes))


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
        _write_static_extras(freezer.app.config['FREEZER_DESTINATION'])
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

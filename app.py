#!/usr/bin/env python3
"""
JPL Development Portfolio - Flask Web Application

A Flask-based web application showcasing development projects and tools.
This application supports both live development and static site generation
for deployment to GitHub Pages.

Features:
- Project data comes from GitHub (repos.json / live API), not a baked-in catalog
- Static site generation with Flask-Frozen
- Custom template filters for enhanced rendering
- Responsive design with modern CSS architecture

Author: JPL Development
Date: July 2025
"""

import os
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xml_escape

from flask import Flask, Response, abort, render_template
from flask_frozen import Freezer

from config.blog import load_posts
from config.projects import ABOUT_ME, GLOSSARY, ROLE_DEFINITIONS
from config.resume import (
    RESUME_CERTIFICATIONS,
    RESUME_EDUCATION,
    RESUME_EDUCATION_NOTE,
    RESUME_HEADLINE,
    RESUME_JOBS,
    RESUME_LANGUAGES,
    RESUME_LOCATION,
    RESUME_SUMMARY,
    RESUME_TOP_SKILLS,
)

SITE_URL = os.environ.get('SITE_URL', 'https://justinlyons.dev').rstrip('/')


def create_app():
    """Application factory.

    The module-level ``app`` below is still created for ``freeze.py`` and for
    ``python app.py``, but tests and any future tooling should call this
    factory so each caller gets a fresh application instead of sharing
    import-time global state.
    """
    application = Flask(__name__)

    # Configure Flask-Frozen for static site generation
    application.config['FREEZER_DESTINATION'] = 'docs'
    application.config['FREEZER_RELATIVE_URLS'] = False
    # Protect manually-placed files in docs/ from being deleted on local freeze runs.
    # FREEZER_REMOVE_EXTRA_FILES defaults to True — without this, `python freeze.py`
    # silently deletes docs/CNAME, breaking the custom domain until CI re-injects it.
    application.config['FREEZER_DESTINATION_IGNORE'] = ['CNAME']

    @application.template_filter('nl2br')
    def nl2br_filter(text):
        """
        Convert newline characters to HTML line breaks.

        This custom Jinja2 filter transforms plain text newlines (\\n) into
        HTML <br> tags, preserving line breaks when rendering text in templates.

        Args:
            text (str or None): The input text to process

        Returns:
            str: Text with newlines converted to HTML breaks, or empty string if input is None

        Example:
            In template: {{ some_text | nl2br | safe }}
            Input: "Line 1\\nLine 2"
            Output: "Line 1<br>\\nLine 2"
        """
        if text is None:
            return ''
        return text.replace('\n', '<br>\n')

    @application.route('/')
    def index():
        """
        Render the main homepage.

        Returns:
            str: Rendered HTML template for the homepage
        """
        return render_template(
            'index.html',
            about=ABOUT_ME,
            glossary_data={
                term: {'definition': entry.definition, 'url': entry.url}
                for term, entry in GLOSSARY.items()
            },
            role_definitions={
                term: {'definition': entry.definition, 'url': entry.url}
                for term, entry in ROLE_DEFINITIONS.items()
            },
            posts=load_posts(),
            resume_headline=RESUME_HEADLINE,
            resume_location=RESUME_LOCATION,
            resume_summary=RESUME_SUMMARY,
            resume_jobs=RESUME_JOBS,
            resume_education=RESUME_EDUCATION,
            resume_education_note=RESUME_EDUCATION_NOTE,
            resume_certifications=RESUME_CERTIFICATIONS,
            resume_languages=RESUME_LANGUAGES,
            resume_top_skills=RESUME_TOP_SKILLS,
        )

    @application.route('/blog/<slug>/')
    def blog_post(slug):
        """Render one blog post. Unknown slugs 404 like any other route."""
        for post in load_posts():
            if post.slug == slug:
                return render_template(
                    'blog_post.html',
                    post=post,
                    about=ABOUT_ME,
                    site_url=SITE_URL,
                    glossary_data={
                        term: {'definition': entry.definition, 'url': entry.url}
                        for term, entry in GLOSSARY.items()
                    },
                    role_definitions={
                        term: {'definition': entry.definition, 'url': entry.url}
                        for term, entry in ROLE_DEFINITIONS.items()
                    },
                )
        abort(404)

    @application.route('/feed.xml')
    def feed():
        """RSS feed for the blog, generated from the same post data."""
        items = ''
        for post in load_posts():
            pub_date = datetime.combine(post.date, datetime.min.time(), tzinfo=timezone.utc)
            items += (
                '  <item>\n'
                f'    <title>{xml_escape(post.title)}</title>\n'
                f'    <link>{SITE_URL}{post.url_path}</link>\n'
                f'    <guid>{SITE_URL}{post.url_path}</guid>\n'
                f'    <pubDate>{pub_date.strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>\n'
                f'    <description>{xml_escape(post.summary)}</description>\n'
                '  </item>\n'
            )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0">\n'
            '<channel>\n'
            '  <title>Justin P. Lyons — Blog</title>\n'
            f'  <link>{SITE_URL}/</link>\n'
            '  <description>Posts by Justin P. Lyons.</description>\n'
            f'{items}</channel>\n'
            '</rss>\n'
        )
        return Response(xml, mimetype='application/rss+xml')

    @application.route('/retro/')
    def retro():
        """Render the optional retro mode: a MySpace-style skin over the
        same About and Projects data as the clean homepage. The clean site
        stays the default; this page is reached only via its link, and it
        links back. It is frozen like any other route, so it works on the
        static GitHub Pages site with no live Python runtime."""
        return render_template('retro.html', about=ABOUT_ME)

    @application.errorhandler(404)
    def page_not_found(error):
        """Render the 404 page. ``freeze.py`` also writes it to ``docs/404.html``
        so GitHub Pages serves it for unknown paths on the static site."""
        return render_template('404.html'), 404

    return application


# Module-level application, kept for freeze.py and `python app.py`.
app = create_app()

# Initialize the static site generator
freezer = Freezer(app)


if __name__ == '__main__':
    # Run the Flask development server only when FLASK_ENV=development.
    # Production deployment uses the static files generated by freeze.py.
    # Note: earlier versions killed a previous dev server via a PID file
    # (.flask.pid / taskkill). That was removed: it could kill an unrelated
    # process if a PID was reused, and restarting the dev server in a fresh
    # terminal is the standard replacement.
    debug_mode = os.environ.get('FLASK_ENV', '').lower() == 'development'
    app.run(debug=debug_mode)

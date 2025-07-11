#!/usr/bin/env python3
"""
Static Site Generator for JPL Development Portfolio

This script generates a static version of the Flask web application for deployment
to GitHub Pages. It uses Flask-Frozen to crawl all routes and generate static HTML
files, making the site suitable for hosting on static file servers.

Usage:
    python freeze.py

Output:
    Static files are generated in the docs/ directory, which is configured
    for GitHub Pages deployment.

Author: JPL Development
Date: July 2025
"""

from app import freezer


def main():
    """
    Generate the static site using Flask-Frozen.
    
    This function freezes the Flask application into static HTML files,
    preserving all routes, templates, and static assets. The output is
    placed in the docs/ directory for GitHub Pages deployment.
    
    The freezing process:
    1. Discovers all URL routes in the Flask application
    2. Renders each route to static HTML
    3. Copies static assets (CSS, JS, images, files)
    4. Maintains the same directory structure as the live app
    
    Raises:
        Exception: If the freezing process encounters any errors
    """
    try:
        print("Starting static site generation...")
        
        # Generate the static site using Flask-Frozen
        # This crawls all routes and renders them to static files
        freezer.freeze()
        
        print("✓ Static site generated successfully in docs/ directory")
        print("  Ready for GitHub Pages deployment")
        
    except Exception as e:
        print(f"✗ Error during static site generation: {e}")
        raise


if __name__ == '__main__':
    # Entry point: only run if script is executed directly
    main()

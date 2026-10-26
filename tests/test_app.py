"""Smoke tests for the portfolio app: every route renders, 404s are handled."""

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


ROUTES = [
    '/',
    '/retro/',
    '/projects/',
    '/widget-demo/',
    '/projects/gsa-mas-checklist/',
    '/projects/schedule-maker/',
]


@pytest.mark.parametrize('route', ROUTES)
def test_routes_render_200(client, route):
    resp = client.get(route)
    assert resp.status_code == 200, route
    assert resp.data  # non-empty body


def test_unknown_path_returns_404_page(client):
    resp = client.get('/no-such-page/')
    assert resp.status_code == 404
    assert b'404' in resp.data


def test_nl2br_filter(client):
    app = client.application
    with app.test_request_context():
        text = 'a' + chr(10) + 'b'
        rendered = app.jinja_env.from_string('{{ text | nl2br | safe }}').render(text=text)
    assert rendered == 'a<br>' + chr(10) + 'b'


def test_homepage_is_a_portfolio_hero_not_a_dashboard(client):
    resp = client.get('/')
    assert b'I build tools that automate repetitive work.' in resp.data
    assert b'Dashboard' not in resp.data
    assert b'Quick Stats' not in resp.data
    # The old hardcoded stats had no source; the replacement names real work.
    assert b'What I Build' in resp.data
    assert b'repo-sync' in resp.data


def test_nav_does_not_link_internal_components_demo(client):
    for route in ('/', '/projects/'):
        resp = client.get(route)
        assert b'Components' not in resp.data
        assert b'widget-demo' not in resp.data


def test_projects_page_lists_shipped_tools(client):
    resp = client.get('/projects/')
    for title in (b'repo-sync', b'gas-auditor', b'photo-stitcher', b'sms-toolkit'):
        assert title in resp.data
    assert b'More Projects Coming Soon' not in resp.data


def test_homepage_links_to_retro_mode(client):
    resp = client.get('/')
    assert b'/retro/' in resp.data
    assert b'Retro mode' in resp.data


def test_retro_page_is_a_skin_not_a_second_portfolio(client):
    resp = client.get('/retro/')
    assert resp.status_code == 200
    assert b'Back to the clean site' in resp.data
    assert b'Justin P. Lyons' in resp.data
    assert b'repo-sync' in resp.data
    # Guardrails agreed for retro mode: no autoplay audio element. The page
    # says "no autoplay" in prose, so test for the attribute/element, not
    # the word, or the note itself trips the test.
    assert b'autoplay=' not in resp.data
    assert b'<audio' not in resp.data
    assert b'Top 8 here means a curated showcase of 8 repos' in resp.data
    assert b'SHOWCASE' in resp.data


def test_retro_grid_cannot_overflow_on_long_repo_names():
    import pathlib

    css = pathlib.Path('static/css/retro.css').read_text()
    # Grid tracks must allow shrinking below their longest unbreakable word
    # (repo names with underscores), or the right-hand cards flow past the
    # page container — the bug reported from the Top 8 screenshot.
    assert 'minmax(0, 1fr)' in css
    assert 'overflow-wrap: anywhere' in css


def test_profile_photo_is_a_local_image_not_the_silhouette():
    import pathlib

    from config.projects import ABOUT_ME

    assert ABOUT_ME.profile_image == 'images/profile.jpg'
    photo = pathlib.Path('static') / ABOUT_ME.profile_image
    assert photo.exists()
    assert photo.read_bytes()[:3] == b'\xff\xd8\xff'  # JPEG magic bytes


def test_homepage_vcard_tabs(client):
    resp = client.get('/')
    assert b'vcard-layout' in resp.data
    assert b'vcard-sidebar' in resp.data
    for tab in (
        b'data-vcard-tab="about"',
        b'data-vcard-tab="projects"',
        b'data-vcard-tab="contact"',
    ):
        assert tab in resp.data
    assert b'data-vcard-section="projects"' in resp.data
    # The old sticky contact footer is gone: sidebar + Contact tab cover it.
    assert b"Let's Connect" not in resp.data


def test_retro_theme_toggle(client):
    import pathlib

    resp = client.get('/retro/')
    assert b'id="retro-theme-toggle"' in resp.data
    assert b'jpl_retro_theme' in resp.data
    css = pathlib.Path('static/css/retro.css').read_text()
    assert '[data-theme="dark"]' in css
    assert '--retro-content-bg' in css


def test_all_blueprint_routes_registered():
    app = create_app()
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert 'gsa_mas_checklist.gsa_mas_checklist' in endpoints
    assert 'schedule_maker.schedule_maker' in endpoints

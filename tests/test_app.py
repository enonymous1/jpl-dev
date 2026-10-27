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
    # The component demo page is gone; the homepage must not link it.
    resp = client.get('/')
    assert b'Components' not in resp.data
    assert b'widget-demo' not in resp.data


@pytest.mark.parametrize(
    'route',
    [
        '/projects/',
        '/projects/gsa-mas-checklist/',
        '/projects/schedule-maker/',
    ],
)
def test_removed_pages_return_404(client, route):
    # The GSA checklist, Schedule Maker, and the /projects page were
    # removed from this repo; project data now comes from GitHub.
    assert client.get(route).status_code == 404


def test_homepage_projects_come_from_github_not_a_catalog(client):
    resp = client.get('/')
    assert b'recent-projects' in resp.data
    assert b'featured-projects' in resp.data
    assert b'github.com/enonymous1?tab=repositories' in resp.data
    # No baked-in project routes remain on the homepage.
    assert b'gsa-mas-checklist' not in resp.data
    assert b'schedule-maker' not in resp.data


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


def test_vcard_section_titles_repeat_the_active_tab(client):
    resp = client.get('/')
    # Each section opens with a title mirroring its tab, like the demo:
    # About -> "About Me", Projects -> "Projects", Contact -> "Contact".
    assert b'class="vcard-section-title">About Me</h2>' in resp.data
    assert b'class="vcard-section-title">Projects</h2>' in resp.data
    assert b'class="vcard-section-title">Contact</h2>' in resp.data
    assert b'Featured Projects' not in resp.data
    # Poppins, the demo's font, loaded only on the homepage.
    assert b'family=Poppins' in resp.data
    import pathlib

    css = pathlib.Path('static/css/vcard.css').read_text()
    assert '--vcard-radius: 20px' in css
    assert 'vcard-section-title::after' in css
    # Avatar is a rounded square now, not a circle.
    assert 'border-radius: 50%' not in css


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
    # Homepage is standalone: no global top nav, but the theme toggle
    # moved into the sidebar so light/dark is still reachable.
    assert b'id="main-navbar"' not in resp.data
    assert b'id="theme-toggle"' in resp.data


def test_other_pages_keep_global_nav(client):
    # base.html now serves only the 404 page; it still carries the nav.
    resp = client.get('/no-such-page/')
    assert resp.status_code == 404
    assert b'id="main-navbar"' in resp.data


def test_vcard_layout_is_stable_across_tabs(client):
    import pathlib

    css = pathlib.Path('static/css/vcard.css').read_text()
    # Tabs are anchored top-right inside the card, and the layout reserves
    # scrollbar space + a minimum card height.
    assert 'scrollbar-gutter: stable' in css
    assert 'min-height: 560px' in css
    assert 'position: absolute' in css
    # The actual Contact-shift cause: base.css makes <body> a flex column
    # app shell, and a standalone homepage with mx-auto shrinks to its
    # content width (Contact is narrow, About/Projects hit the cap).
    # The homepage body is a normal block document instead, and the
    # wrapper is explicitly full-width, so its width no longer depends
    # on which tab is active.
    assert 'body.vcard-page' in css
    assert 'display: block' in css
    resp = client.get('/')
    assert b'class="vcard-page"' in resp.data
    assert b'w-full max-w-7xl' in resp.data


def test_retro_theme_toggle(client):
    import pathlib

    resp = client.get('/retro/')
    assert b'id="retro-theme-toggle"' in resp.data
    assert b'jpl_retro_theme' in resp.data
    css = pathlib.Path('static/css/retro.css').read_text()
    assert '[data-theme="dark"]' in css
    assert '--retro-content-bg' in css


def test_no_baked_in_project_routes_remain():
    app = create_app()
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert 'gsa_mas_checklist.gsa_mas_checklist' not in endpoints
    assert 'schedule_maker.schedule_maker' not in endpoints
    assert 'projects' not in endpoints
    # What remains: homepage, retro, and the 404 handler (not a route).
    assert 'widget_demo' not in endpoints
    assert {'index', 'retro'} <= endpoints

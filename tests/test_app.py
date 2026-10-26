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


def test_all_blueprint_routes_registered():
    app = create_app()
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert 'gsa_mas_checklist.gsa_mas_checklist' in endpoints
    assert 'schedule_maker.schedule_maker' in endpoints

"""Tests for fetch_repos.py: filtering and Link-header pagination parsing."""

from fetch_repos import filter_repos, parse_next_link


def test_filter_drops_forks_and_archived():
    repos = [
        {'name': 'live', 'fork': False, 'archived': False},
        {'name': 'forked', 'fork': True, 'archived': False},
        {'name': 'old', 'fork': False, 'archived': True},
        {'name': 'plain'},  # missing keys default to kept
    ]
    assert [r['name'] for r in filter_repos(repos)] == ['live', 'plain']


def test_parse_next_link():
    header = (
        '<https://api.github.com/users/enonymous1/repos?page=2>; rel="next", '
        '<https://api.github.com/users/enonymous1/repos?page=1>; rel="prev"'
    )
    assert parse_next_link(header) == 'https://api.github.com/users/enonymous1/repos?page=2'


def test_parse_next_link_none_when_last_page():
    header = '<https://api.github.com/users/enonymous1/repos?page=1>; rel="prev"'
    assert parse_next_link(header) is None
    assert parse_next_link(None) is None
    assert parse_next_link('') is None


def test_slim_keeps_only_used_fields():
    from fetch_repos import REPO_FIELDS, _slim

    repo = {
        'name': 'demo',
        'full_name': 'enonymous1/demo',
        'html_url': 'https://github.com/enonymous1/demo',
        'license': {'key': 'mit', 'name': 'MIT License', 'url': 'https://example.invalid'},
        'owner': {'login': 'enonymous1'},
        'node_id': 'abc',
        'url': 'https://api.github.com/repos/enonymous1/demo',
        'clone_url': 'https://github.com/enonymous1/demo.git',
    }
    slim = _slim(repo)
    assert set(slim) == REPO_FIELDS | {'license'}
    assert slim['license'] == {'name': 'MIT License'}
    assert 'owner' not in slim and 'node_id' not in slim and 'url' not in slim
    assert _slim({'name': 'plain', 'license': None})['license'] is None
    assert _slim({'name': 'plain'})['license'] is None


def test_main_falls_back_to_cache(monkeypatch, tmp_path):
    import json

    import fetch_repos

    cache = tmp_path / 'repos.json'
    cache.write_text(json.dumps([{'name': 'kept'}]), encoding='utf-8')
    monkeypatch.setattr(fetch_repos, 'OUTPUT_PATH', str(cache))
    monkeypatch.setattr(
        fetch_repos, 'fetch_repos', lambda: (_ for _ in ()).throw(RuntimeError('boom'))
    )
    assert fetch_repos.main() == 0
    assert json.loads(cache.read_text(encoding='utf-8')) == [{'name': 'kept'}]


def test_main_fails_without_cache(monkeypatch, tmp_path):
    import fetch_repos

    monkeypatch.setattr(fetch_repos, 'OUTPUT_PATH', str(tmp_path / 'missing.json'))
    monkeypatch.setattr(
        fetch_repos, 'fetch_repos', lambda: (_ for _ in ()).throw(RuntimeError('boom'))
    )
    assert fetch_repos.main() == 1

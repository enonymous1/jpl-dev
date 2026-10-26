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

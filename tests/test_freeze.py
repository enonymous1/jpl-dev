"""End-to-end freeze tests: the static output Pages actually serves."""

import app as app_module
import freeze


def test_freeze_writes_404_robots_and_sitemap(monkeypatch, tmp_path):
    # Redirect the module-level freezer's destination at a temp dir so
    # the test never touches the real docs/ build output.
    monkeypatch.setitem(app_module.freezer.app.config, 'FREEZER_DESTINATION', str(tmp_path))
    freeze.main()
    assert (tmp_path / 'index.html').is_file()
    assert (tmp_path / 'retro' / 'index.html').is_file()
    assert (tmp_path / 'feed.xml').is_file()
    not_found = (tmp_path / '404.html').read_text(encoding='utf-8')
    assert '404' in not_found
    robots = (tmp_path / 'robots.txt').read_text(encoding='utf-8')
    assert 'Sitemap: https://justinlyons.dev/sitemap.xml' in robots
    sitemap = (tmp_path / 'sitemap.xml').read_text(encoding='utf-8')
    assert '<loc>https://justinlyons.dev/</loc>' in sitemap
    assert '<loc>https://justinlyons.dev/retro/</loc>' in sitemap
    assert '<loc>https://justinlyons.dev/blog/interesting-links/</loc>' in sitemap


def test_freeze_fails_on_uncovered_dynamic_route(monkeypatch):
    # A parameterized route without a generator must break the build,
    # not warn and ship a site missing pages. The check reads the
    # module-level freezer, so stub it instead of mutating the real app.
    import pytest

    class Rule:
        def __init__(self, rule, endpoint):
            self.rule = rule
            self.endpoint = endpoint

    class Map:
        def __init__(self, rules):
            self._rules = rules

        def iter_rules(self):
            return iter(self._rules)

    class FakeApp:
        def __init__(self, rules):
            self.url_map = Map(rules)

    class FakeFreezer:
        def __init__(self, rules):
            self.app = FakeApp(rules)

    monkeypatch.setattr(
        freeze,
        'freezer',
        FakeFreezer([Rule('/example/<name>/', 'example')]),
    )
    with pytest.raises(RuntimeError, match='example'):
        freeze._check_dynamic_routes()

    # A covered endpoint (blog_post has a generator) must not raise.
    monkeypatch.setattr(
        freeze,
        'freezer',
        FakeFreezer([Rule('/blog/<slug>/', 'blog_post')]),
    )
    freeze._check_dynamic_routes()

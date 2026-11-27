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


def test_homepage_is_a_portfolio_hero_not_a_dashboard(client):
    resp = client.get('/')
    assert b'I build tools that automate repetitive work.' in resp.data
    assert b'Dashboard' not in resp.data
    assert b'Quick Stats' not in resp.data
    # The old hardcoded stats had no source; the replacement names real work.
    assert b'What I Build' in resp.data
    assert b'repetitive data work' in resp.data


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


def test_projects_language_filters_are_derived_from_repo_data(client):
    resp = client.get('/')
    # The static HTML carries only the "All" chip; the language chips
    # themselves are built by JS from the loaded repos, so a language
    # with no repos never gets a chip. The JS-built All pill carries
    # the total count, matching the default unfiltered load.
    assert b'id="language-filters"' in resp.data
    assert b'aria-label="Filter projects by language"' in resp.data
    assert b'data-language-filter="All"' in resp.data
    assert b'data-language-filter="Python"' not in resp.data
    assert b'data-language-filter="PowerShell"' not in resp.data
    # The chip builder lives in the extracted modules now, not inline.
    assert b'js/projects.js' in resp.data
    assert b'js/repo-loader.js' in resp.data
    projects_js = client.get('/static/js/projects.js').data
    assert b"chip('All', repos.length, false)" in projects_js
    assert b"selectedLanguage = (lang === selectedLanguage) ? 'All' : lang" in projects_js
    assert b'renderLanguageFilters' in projects_js
    loader_js = client.get('/static/js/repo-loader.js').data
    assert b'LANGUAGE_COLORS' in loader_js

    css = client.get('/static/css/vcard.css').data.decode()
    assert '.language-filter-btn' in css
    assert '.lang-dot' in css


def test_vcard_tab_sections_animate_on_switch(client):
    resp = client.get('/')
    assert b'js/tabs.js' in resp.data
    tabs_js = client.get('/static/js/tabs.js').data
    assert b'vcard-section-enter' in tabs_js
    assert b'void s.offsetWidth' in tabs_js
    css = client.get('/static/css/vcard.css').data.decode()
    assert '@keyframes vcard-section-in' in css
    assert '.vcard-section-enter' in css


def test_blog_post_parsing_sorting_and_scaffold(tmp_path):
    from datetime import date

    from config.blog import build_post_source, load_posts, slugify

    assert slugify('Hello, World! 2026') == 'hello-world-2026'
    assert slugify('---') == 'post'
    source = build_post_source('My Title', date(2026, 10, 28), 'my-title')
    assert 'title: My Title' in source
    assert 'slug: my-title' in source
    assert 'date: 2026-10-28' in source

    (tmp_path / 'a.md').write_text(
        '---\ntitle: Newer\nslug: newer\ndate: 2026-01-02\nsummary: New.\n---\n\nBody **bold**.\n',
        encoding='utf-8',
    )
    (tmp_path / 'b.md').write_text(
        '---\ntitle: Pinned Older\nslug: pinned-older\ndate: 2025-12-01\n'
        'summary: P.\npinned: true\ntags: [bookmarks, links]\n---\n\nPinned body.\n',
        encoding='utf-8',
    )
    posts = load_posts(tmp_path)
    assert [post.slug for post in posts] == ['pinned-older', 'newer']
    assert posts[0].tags == ['bookmarks', 'links']
    assert posts[1].date_label == 'January 2, 2026'
    assert '<strong>bold</strong>' in posts[1].html
    assert posts[1].url_path == '/blog/newer/'


def test_blog_loader_rejects_bad_posts(tmp_path):
    from config.blog import load_posts

    cases = {
        'duplicate': [
            '---\ntitle: A\nslug: same\ndate: 2026-01-01\nsummary: A.\n---\n\nBody.\n',
            '---\ntitle: B\nslug: same\ndate: 2026-01-02\nsummary: B.\n---\n\nBody.\n',
        ],
        'bad-date': ['---\ntitle: A\nslug: a\ndate: 2026-13-01\nsummary: A.\n---\n\nBody.\n'],
        'unknown-key': [
            '---\ntitle: A\nslug: a\ndate: 2026-01-01\nsummary: A.\nsummery: x\n---\n\nBody.\n'
        ],
        'empty-body': ['---\ntitle: A\nslug: a\ndate: 2026-01-01\nsummary: A.\n---\n'],
        'missing-summary': ['---\ntitle: A\nslug: a\ndate: 2026-01-01\n---\n\nBody.\n'],
    }
    for name, texts in cases.items():
        directory = tmp_path / name
        directory.mkdir()
        for i, text in enumerate(texts):
            (directory / f'{i}.md').write_text(text, encoding='utf-8')
        with pytest.raises(ValueError):
            load_posts(directory)


def _sidebar_block(data: bytes) -> str:
    text = data.decode()
    start = text.index('<aside class="vcard-sidebar">')
    end = text.index('</aside>', start) + len('</aside>')
    return '\n'.join(line.strip() for line in text[start:end].splitlines() if line.strip())


def test_blog_post_uses_vcard_shell_and_shared_sidebar(client):
    post = client.get('/blog/interesting-links/')
    assert post.status_code == 200
    assert b'id="main-navbar"' not in post.data
    assert b'vcard-layout' in post.data
    assert b'data-vcard-tab' not in post.data
    assert b'href="/#about"' in post.data
    assert b'href="/#projects"' in post.data
    assert b'href="/#blog" aria-current="page"' in post.data
    assert b'href="/#contact"' in post.data
    assert b'<title>Interesting Links' in post.data
    assert b'https://justinlyons.dev/blog/interesting-links/' in post.data
    home = client.get('/')
    assert _sidebar_block(home.data) == _sidebar_block(post.data)


def test_avatar_quips_script_is_external_and_shared(client):
    script = client.get('/static/avatar-easter-egg.js')
    assert script.status_code == 200
    assert b'is-spinning' in script.data
    home = client.get('/')
    assert b'avatar-easter-egg.js' in home.data
    # The quip lines live in the JS file now, not inline in the page.
    assert b'Okay, you found the clicky photo.' not in home.data
    post = client.get('/blog/interesting-links/')
    assert b'avatar-easter-egg.js' in post.data


def test_cv_tab_renders_profile_data(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'data-vcard-tab="cv"' in resp.data
    assert b'data-vcard-section="cv"' in resp.data
    assert b'Curriculum Vitae' in resp.data
    assert b'course of life' in resp.data
    assert b'data-vcard-tab="resume"' not in resp.data
    assert b'Systems Automation Specialist' in resp.data
    # Headline, Mobile detail, EM3 title, and education notes come
    # from the user's CV PDF (merged 2026-10-30).
    assert b'Full-Stack and Mobile Developer' in resp.data
    assert b'offline-first' in resp.data
    assert b'Jetpack Compose' in resp.data
    # Jinja escapes the apostrophe in the rendered title.
    assert b'Electrician&#39;s Mate Third Class (EM3)' in resp.data
    assert b'United States Navy Reserve (USNR)' in resp.data
    assert b'Salutatorian' in resp.data
    assert b'weight in Mobile Application Development' in resp.data
    assert b'Millennium Partners' in resp.data
    assert b'July 2024' in resp.data
    assert b'Full Sail University' in resp.data
    assert b'Bachelor' in resp.data
    assert b'April 2024' in resp.data
    assert b'Agile Foundations' in resp.data
    assert b'IT Infrastructure Management' in resp.data
    assert b'id="resume-print-btn"' in resp.data
    # The blog post pages share the sidebar, not the CV tab.
    post = client.get('/blog/interesting-links/')
    assert b'data-vcard-section="cv"' not in post.data


def test_resume_omits_private_contact_details(client):
    # The LinkedIn PDF carries a mobile number and a Gmail address; the
    # public site publishes neither.
    resp = client.get('/')
    assert b'322-7999' not in resp.data
    assert b'justinplyons@gmail.com' not in resp.data


def test_resume_data_is_complete():
    from config.resume import RESUME_EDUCATION, RESUME_JOBS

    assert RESUME_JOBS
    assert RESUME_EDUCATION
    for job in RESUME_JOBS:
        assert job.title and job.employer and job.start and job.end
    # The CV merge filled in the Mobile Application Developer entry,
    # which the LinkedIn PDF left bare. Freelancer stays bare: neither
    # source gives it any detail, and none is invented here.
    mobile = next(j for j in RESUME_JOBS if j.title == 'Mobile Application Developer')
    assert mobile.description and 'offline-first' in mobile.description
    for entry in RESUME_EDUCATION:
        assert entry.degree and entry.school and entry.date


def test_projects_search_and_sort_controls(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'id="projects-search"' in resp.data
    assert b'Search projects...' in resp.data
    assert b'id="projects-sort"' in resp.data
    assert b'value="updated"' in resp.data
    assert b'value="name"' in resp.data
    assert b'value="stars"' in resp.data
    # Retro renders its own server-side list: no client-side controls.
    retro = client.get('/retro/')
    assert b'id="projects-search"' not in retro.data
    assert b'id="projects-sort"' not in retro.data
    post = client.get('/blog/interesting-links/')
    assert b'id="projects-search"' not in post.data


def test_websites_search_sort_and_language_filters(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'id="websites-search"' in resp.data
    assert b'Search websites...' in resp.data
    assert b'id="websites-sort"' in resp.data
    assert b'value="web"' in resp.data
    assert b'value="recent"' in resp.data
    assert b'value="name"' in resp.data
    # The static HTML carries only the "All" pill; the language pills
    # are built by JS from the loaded site repos, like the Projects chips.
    assert b'id="website-language-filters"' in resp.data
    assert b'aria-label="Filter websites by language"' in resp.data
    assert b'data-website-language="All"' in resp.data
    assert b'data-website-language="Python"' not in resp.data
    # Retro and post pages carry no Websites controls.
    retro = client.get('/retro/')
    assert b'id="websites-search"' not in retro.data
    assert b'id="websites-sort"' not in retro.data
    post = client.get('/blog/interesting-links/')
    assert b'id="websites-search"' not in post.data


def test_goatcounter_snippet_on_every_page(client):
    # The jpl-dev GoatCounter site — never the whenwherebiz one: each
    # domain gets its own site because GoatCounter records the path
    # only, not the domain.
    for route, status in (
        ('/', 200),
        ('/retro/', 200),
        ('/blog/interesting-links/', 200),
        ('/blog/tag/gig-work/', 200),
        ('/no-such-page/', 404),
    ):
        resp = client.get(route)
        assert resp.status_code == status, route
        assert b'https://jpl-dev.goatcounter.com/count' in resp.data, route
        assert b'https://gc.zgo.at/count.js' in resp.data, route
        assert b'whenwherebiz.goatcounter.com' not in resp.data, route


def test_videos_tab_lists_both_channels(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'id="videos-search"' in resp.data
    assert b'Enonymous1 Gaming' in resp.data
    assert b'https://www.youtube.com/@enonymous1gaming' in resp.data
    # The gaming channel's newest and oldest uploads.
    assert b'ANVIL   Brone   no3   Symphonia' in resp.data
    assert b'Lego Worlds 1 Billion studs method! Works with current patch' in resp.data
    assert b'Titanfall Assault' in resp.data
    # 75 cards across both channels; long-form durations render as H:MM:SS.
    assert resp.data.count(b'class="video-card"') == 75
    assert b'3:33:15' in resp.data
    # Cards show the first paragraph of a description only: the Lego
    # video's later paragraphs never reach the page.
    assert b'Search no more, 1 Billion studs is achievable' in resp.data
    assert b'Requirements' not in resp.data
    assert b'Cronusmax' not in resp.data
    # The three upcoming/offline stream placeholders are not videos.
    assert b'Enonymous1 Gaming Live Stream' not in resp.data
    assert b'Overwatch Arcade fun' not in resp.data


def test_videos_tab_lists_youtube_uploads(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'data-vcard-tab="videos"' in resp.data
    assert b'data-vcard-section="videos"' in resp.data
    # The four real uploads from the channel, newest first.
    assert b'Xbox One COD Ghosts FFA Tremor 30 3' in resp.data
    assert b'enonymous1 - MW3 Game Clip' in resp.data
    assert b'25ToCBeasts.mp4' in resp.data
    assert b'10HToCBoss2' in resp.data
    assert b'https://www.youtube.com/watch?v=xp-cd9AwNr8' in resp.data
    assert b'https://www.youtube.com/@JustinLyons364' in resp.data
    # Retro and post pages carry no Videos tab.
    retro = client.get('/retro/')
    assert b'data-vcard-tab="videos"' not in retro.data
    post = client.get('/blog/interesting-links/')
    assert b'data-vcard-tab="videos"' not in post.data


def test_video_sections_reference_real_uploads():
    # Every listed video is a real public upload: an 11-char YouTube
    # id, an ISO date, and a thumbnail file that actually exists.
    import os
    import re
    from datetime import date

    from config.videos import VIDEO_SECTIONS

    assert VIDEO_SECTIONS
    seen = set()
    for section in VIDEO_SECTIONS:
        assert section['channel_url'].startswith('https://www.youtube.com/')
        for video in section['videos']:
            assert re.fullmatch(r'[A-Za-z0-9_-]{11}', video['id'])
            assert video['id'] not in seen
            seen.add(video['id'])
            date.fromisoformat(video['date'])
            assert video['title'] and video['date_label']
            assert video['duration'] == '' or re.fullmatch(
                r'[0-9]+:[0-9][0-9](:[0-9][0-9])?', video['duration']
            )
            thumb = os.path.join('static/images/video-thumbs', video['thumbnail'])
            assert os.path.isfile(thumb), f'missing video thumbnail: {thumb}'
            assert os.path.getsize(thumb) > 0


def test_about_build_cards_and_tool_labels(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # The repetitive intro paragraph is gone; the hero line and bio stay.
    assert b'shipped as tested, documented tools, not demos' not in resp.data
    assert b'I build tools that automate repetitive work.' in resp.data
    assert b'What I Build' in resp.data
    # Four What I Build cards plus the Contributions and site cards below them.
    assert resp.data.count(b'class="build-card"') == 6
    assert b'Automation &amp; data' in resp.data
    assert b'Desktop tools' in resp.data
    assert b'Data pipelines' in resp.data
    assert b'bi bi-gear' in resp.data
    assert b'bi bi-pc-display' in resp.data
    assert b'bi bi-globe' in resp.data
    assert b'bi bi-diagram-3' in resp.data
    assert resp.data.count(b'class="build-card-header"') == 6
    # Contributions sits above the stack block, as one card per project.
    assert b'Contributions' in resp.data
    assert resp.data.index(b'Contributions') < resp.data.index(b'How This Site Is Built')
    assert b'Skybrush' in resp.data
    assert b'href="https://skybrush.io"' in resp.data
    assert b'skybrush-io/skybrush-server/pull/52' in resp.data
    assert b'skybrush-io/live/pull/262' in resp.data
    assert b'href="https://github.com/skybrush-io/skybrush-server"' in resp.data
    assert b'href="https://github.com/skybrush-io/live"' in resp.data
    # The stack block is a card too, titled with the repo name.
    assert b'jpl-dev' in resp.data
    assert b'bi bi-code-slash' in resp.data
    # What I Build cards are informative only: no product links, no
    # product-name row (the Web card's unfinished-looking
    # "this site, voxel-portfolio" line went with them).
    assert b'build-card-link' not in resp.data
    assert b'build-card-links' not in resp.data
    assert b'this site, voxel-portfolio' not in resp.data
    # Blurbs describe the actual work behind each card (reviewed
    # 2026-10-30 against the live repos), not the category.
    assert b'repetitive data work' in resp.data
    assert b'photo-scan stitching wizard' in resp.data
    assert b'voxel world you walk through' in resp.data
    assert b'recorded to Parquet' in resp.data
    assert b'deduped, queryable datasets' in resp.data
    assert b'client-side billing analyzer' in resp.data
    # Tool-group labels are larger and full-strength text color.
    assert b'font-size:0.85rem;color:var(--text-color)' in resp.data


def test_blog_tab_post_page_and_feed(client):
    resp = client.get('/')
    assert b'data-vcard-tab="blog"' in resp.data
    assert b'Interesting Links' in resp.data
    assert b'Pinned' in resp.data
    post = client.get('/blog/interesting-links/')
    assert post.status_code == 200
    assert b'Interesting Links' in post.data
    assert b'A running list of links' in post.data
    assert client.get('/blog/no-such-post/').status_code == 404
    feed = client.get('/feed.xml')
    assert feed.status_code == 200
    assert feed.headers['Content-Type'].startswith('application/rss+xml')
    assert b'<rss' in feed.data
    assert b'https://justinlyons.dev/blog/interesting-links/' in feed.data
    retro = client.get('/retro/')
    assert b'data-vcard-tab="blog"' not in retro.data


def test_blog_tag_page_lists_only_matching_posts(client):
    # gig-work is the one tag shared by two published posts.
    resp = client.get('/blog/tag/gig-work/')
    assert resp.status_code == 200
    assert b'Posts tagged' in resp.data
    assert b'GigSmart Explained' in resp.data
    assert b'iSecretShop Explained' in resp.data
    assert b'Choosing a Password Manager' not in resp.data
    assert b'2 posts' in resp.data
    # A single-post tag still renders, with the singular count.
    single = client.get('/blog/tag/passwords/')
    assert single.status_code == 200
    assert b'Choosing a Password Manager' in single.data
    assert b'1 post' in single.data
    assert b'2 posts' not in single.data
    assert client.get('/blog/tag/no-such-tag/').status_code == 404


def test_blog_tab_has_search_sort_and_tag_filters(client):
    resp = client.get('/')
    assert resp.status_code == 200
    html = resp.data.decode()
    assert 'id="blog-search"' in html
    assert 'placeholder="Search posts..."' in html
    assert 'id="blog-sort"' in html
    assert '<option value="newest" selected>Newest</option>' in html
    assert '<option value="oldest">Oldest</option>' in html
    assert '<option value="title">Title A' in html
    # All pill leads with the total; pills carry counts, most-used first.
    assert '>All <span class="lang-count">8</span>' in html
    assert '>gig-work <span class="lang-count">2</span>' in html
    assert 'data-blog-tag="far"' in html
    # Items carry the data the filter reads; the filter script loads.
    assert 'data-blog-date="2026-11-25"' in html
    assert 'data-blog-pinned="true"' in html
    assert 'id="blog-no-results"' in html
    assert 'js/blog.js' in html


def test_blog_tag_pills_are_links_on_homepage_and_post_pages(client):
    resp = client.get('/')
    assert b'href="/blog/tag/gig-work/"' in resp.data
    assert b'href="/blog/tag/passwords/"' in resp.data
    post = client.get('/blog/choosing-a-password-manager/')
    assert post.status_code == 200
    assert b'href="/blog/tag/passwords/"' in post.data
    # Linked pills keep the badge look and get a hover state.
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.blog-tags a.badge-theme' in css
    assert '.blog-tags a.badge-theme:hover' in css


def test_blog_tag_helpers_are_sorted_and_deduplicated():
    from config.blog import all_tags, posts_for_tag, tag_url_path

    tags = all_tags()
    assert tags == sorted(tags)
    assert len(tags) == len(set(tags))
    assert 'gig-work' in tags
    assert [p.slug for p in posts_for_tag('gig-work')] == [
        'gigsmart-explained-what-it-is-and-how-to-use-it',
        'isecretshop-explained-what-it-is-and-how-it-works',
    ]
    assert posts_for_tag('no-such-tag') == []
    assert tag_url_path('gmail') == '/blog/tag/gmail/'


def test_blog_tag_counts_are_sorted_by_count_then_name():
    from datetime import date

    from config.blog import Post, tag_counts

    def post(slug, tags):
        return Post(slug=slug, title=slug, date=date(2026, 11, 25), summary='x', tags=tags)

    # Most-used first, ties broken by name; an untagged post adds nothing.
    assert tag_counts([post('a', ['gig-work', 'far']), post('b', ['gig-work']), post('c', [])]) == [
        ('gig-work', 2),
        ('far', 1),
    ]
    assert tag_counts([]) == []


def test_blog_related_posts_by_tag(client):
    # GigSmart and iSecretShop share gig-work, so each links the other —
    # and never itself.
    gig = client.get('/blog/gigsmart-explained-what-it-is-and-how-to-use-it/')
    assert gig.status_code == 200
    assert b'Related posts' in gig.data
    assert b'iSecretShop Explained' in gig.data
    assert b'href="/blog/isecretshop-explained-what-it-is-and-how-it-works/"' in gig.data
    secret = client.get('/blog/isecretshop-explained-what-it-is-and-how-it-works/')
    assert b'GigSmart Explained' in secret.data
    # The password-manager post shares no tag with anything, so the
    # section stays hidden rather than showing an empty heading.
    passwords = client.get('/blog/choosing-a-password-manager/')
    assert passwords.status_code == 200
    assert b'Related posts' not in passwords.data


def test_blog_related_posts_rank_by_shared_tag_count():
    from datetime import date

    from config.blog import Post, related_posts

    def post(slug, tags, day):
        return Post(
            slug=slug,
            title=slug,
            date=date(2026, 11, day),
            summary='x',
            tags=tags,
        )

    current = post('current', ['a', 'b'], 10)
    one_tag = post('one-tag', ['a'], 20)
    two_tags = post('two-tags', ['a', 'b'], 1)
    unrelated = post('unrelated', ['c'], 25)
    assert [p.slug for p in related_posts(current, [current, one_tag, two_tags, unrelated])] == [
        'two-tags',
        'one-tag',
    ]
    assert related_posts(post('lonely', [], 10), [current, one_tag]) == []
    assert related_posts(current, [current, one_tag, two_tags], limit=1) == [two_tags]


def test_blog_tab_hidden_with_no_posts(client, tmp_path, monkeypatch):
    monkeypatch.setattr('config.blog.POSTS_DIR', tmp_path)
    resp = client.get('/')
    assert b'data-vcard-tab="blog"' not in resp.data
    assert b'vcard-blog' not in resp.data


def test_glossary_covers_every_tool_pill():
    from config.projects import ABOUT_ME, GLOSSARY

    pills = [tool for group in ABOUT_ME.tool_groups for tool in group.tools]
    assert len(pills) == 27
    assert set(GLOSSARY) == set(pills)
    for term, entry in GLOSSARY.items():
        assert entry.definition.strip(), term
        assert entry.url is None or entry.url.startswith('https://'), term
    assert GLOSSARY['Team Building'].url is None
    assert GLOSSARY['Mentorship'].url is None


def test_glossary_modal_rendered_on_homepage_and_post_pages(client):
    resp = client.get('/')
    assert b'id="glossary-modal"' in resp.data
    assert b'data-glossary-term="Swift"' in resp.data
    assert b'data-glossary-term="Team Building"' in resp.data
    assert b'https://developer.apple.com/swift/' in resp.data
    # tojson escapes the apostrophe as \u0027; match the unescaped part.
    assert b'programming language for iOS' in resp.data
    assert b'glossary-hint' in resp.data
    assert b'glossary-modal.js' in resp.data
    post = client.get('/blog/interesting-links/')
    assert b'id="glossary-modal"' in post.data
    assert b'glossary-modal.js' in post.data
    retro = client.get('/retro/')
    assert b'glossary-modal' not in retro.data
    assert b'data-glossary-term' not in retro.data


def test_location_modal_rendered_on_homepage_and_post_pages(client):
    resp = client.get('/')
    assert b'id="location-modal-open"' in resp.data
    assert b'id="location-modal"' in resp.data
    assert b'location-modal.js' in resp.data
    assert b'maps.google.com/maps?q=Fredericksburg' in resp.data
    assert b'google.com/maps/search/?api=1' in resp.data
    for title in (
        b'The birth of the power chord',
        b'The blueprint for the First Amendment',
        b'The first Civil Rights stop',
        b'A massive crossing to freedom',
        b'Royal street names',
        b'The true Washington home',
        b'19th-century big data',
        b'The hydroelectric shift',
        b'The mystery tunnels',
        b'The local maker hub',
        b'The 2026 arcade expansion',
    ):
        assert title in resp.data
    # The sidebar entry is a button now, not plain text.
    assert b'<i class="bi bi-geo-alt"></i> Fredericksburg, VA</li>' not in resp.data
    post = client.get('/blog/interesting-links/')
    assert b'id="location-modal"' in post.data
    assert b'location-modal.js' in post.data
    retro = client.get('/retro/')
    assert b'location-modal' not in retro.data
    assert b'location-modal-open' not in retro.data


def test_location_facts_carousel_controls(client):
    resp = client.get('/')
    assert b'id="location-track"' in resp.data
    assert b'class="location-carousel-viewport"' in resp.data
    assert b'id="location-fact-prev"' in resp.data
    assert b'id="location-fact-next"' in resp.data
    assert b'Fact 1 of 11' in resp.data
    assert resp.data.count(b'class="location-slide"') == 11
    assert b'id="location-fact-status"' in resp.data
    script = client.get('/static/location-modal.js')
    assert b'nextFactIndex' in script.data
    assert b'prevFactIndex' in script.data


def test_location_facts_shape(client):
    from config.projects import LOCATION_FACTS

    assert len(LOCATION_FACTS) == 11
    for fact in LOCATION_FACTS:
        assert fact['title'].strip()
        assert fact['body'].strip()


def test_role_definition_modals_use_approved_wording(client):
    from config.projects import ABOUT_ME, ROLE_DEFINITIONS

    assert set(ROLE_DEFINITIONS) == set(ABOUT_ME.badges)
    assert ROLE_DEFINITIONS['IT Manager'].definition.startswith(
        "Directs an organization's IT infrastructure"
    )
    assert 'At Millennium Partners' in ROLE_DEFINITIONS['IT Manager'].definition
    assert 'GSA pricing and vendor data' in ROLE_DEFINITIONS['Automation Engineer'].definition
    assert 'Flask and Jinja2' in ROLE_DEFINITIONS['Full-Stack Developer'].definition
    for entry in ROLE_DEFINITIONS.values():
        assert entry.definition.strip()
        assert entry.url is None
    for page in ('/', '/blog/interesting-links/'):
        resp = client.get(page)
        for badge in ABOUT_ME.badges:
            assert f'data-glossary-term="{badge}"'.encode() in resp.data
        assert b'Directs an organization' in resp.data


def test_avatar_easter_egg_quips_homepage_only(client):
    resp = client.get('/')
    assert b'id="avatar-easter-egg"' in resp.data
    assert b'id="avatar-quip"' in resp.data
    assert b'role="status"' in resp.data
    # The quip lines live in the shared JS file, not inline in the page.
    script = client.get('/static/avatar-easter-egg.js')
    for line in (
        b"Hey. That's me.",
        b'Yep, still me.',
        b'The projects are in the next tab over.',
        b'Okay, you found the clicky photo.',
        b'Alright, you win. Go poke a repo instead.',
    ):
        assert line in script.data
    css = client.get('/static/css/vcard.css').data.decode()
    assert '@keyframes avatar-spin' in css
    assert '.vcard-bubble' in css
    assert '.vcard-quip' not in css
    assert 'prefers-reduced-motion' in css
    # Hovering (or focusing) the photo greets; clicking still cycles.
    assert b'Hello, World!' in script.data
    assert b'mouseenter' in script.data
    assert b'vcard-bubble-wrap' in resp.data
    # Retro keeps its plain photo: the easter egg is shared by the
    # homepage and the blog post pages only.
    retro = client.get('/retro/')
    assert b'avatar-easter-egg' not in retro.data


def test_face_stretch_play_modal_is_gone(client):
    # The ten-rapid-clicks face-stretch egg and its play modal were
    # removed 2026-11-22; the base five-click quip egg stays. Assert
    # the modal, its markup, its stretch math and its styles are all
    # gone from the homepage and the blog post pages, while the base
    # egg (button, bubble) is still there.
    for path in ('/', '/blog/interesting-links/'):
        resp = client.get(path)
        assert b'avatar-play-modal' not in resp.data
        assert b'avatar-play-photo' not in resp.data
        assert b'Drag the photo to stretch it' not in resp.data
        assert b'id="avatar-easter-egg"' in resp.data
        assert b'id="avatar-quip"' in resp.data
    script = client.get('/static/avatar-easter-egg.js').data
    assert b'computeStretch' not in script
    assert b'avatar-play-modal' not in script
    assert b'RAPID_CLICKS' not in script
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.avatar-play-photo' not in css
    assert '.avatar-play-card' not in css


def test_sidebar_and_retro_use_role_pills_not_a_title_line(client):
    resp = client.get('/')
    assert b'class="vcard-title"' not in resp.data
    assert b'IT Manager | Automation' not in resp.data
    # Role pills, in order, in the sidebar; the first takes the primary
    # badge style. The degree stays in the About bio, not in a pill.
    # The pills are buttons that open definition modals.
    assert b'>IT Manager</button>' in resp.data
    assert b'>Automation Engineer</button>' in resp.data
    assert b'>Full-Stack Developer</button>' in resp.data
    assert b'>AS &amp; BS in CS</span>' not in resp.data
    retro = client.get('/retro/')
    assert retro.status_code == 200
    assert b'IT Manager | Automation' not in retro.data
    assert b'>IT Manager</span>' in retro.data
    assert b'>Automation Engineer</span>' in retro.data
    assert b'>Full-Stack Developer</span>' in retro.data
    assert b'<p>Fredericksburg, VA</p>' in retro.data


def test_sidebar_has_myspace_tooltip_and_social_row(client):
    resp = client.get('/')
    assert b'View Projects' not in resp.data
    assert b"'My' Space" in resp.data
    assert b'id="retro-tooltip"' in resp.data
    assert b'Same portfolio, same information' in resp.data
    assert b'Retro mode is the same portfolio' not in resp.data
    assert b'id="theme-toggle"' in resp.data
    assert b'class="vcard-social"' in resp.data
    assert b'aria-label="GitHub"' in resp.data
    assert b'aria-label="LinkedIn"' in resp.data
    assert b'aria-label="Email"' in resp.data
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.vcard-tooltip' in css
    assert '.vcard-social' in css
    assert '.vcard-small' not in css


def test_repo_card_footer_anchors_github_button_and_socials_centered(client):
    # Card markup is rendered by the extracted grid module, not inline.
    projects_js = client.get('/static/js/projects.js').data
    assert b'repo-card-tags' in projects_js
    assert b'repo-card-actions' in projects_js
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.repo-card-actions' in css
    assert 'margin-left: auto' in css
    social_block = css.split('.vcard-social')[1].split('}')[0]
    assert 'justify-content: center' in social_block


def test_projects_single_grid_with_expand_control(client):
    resp = client.get('/')
    # One grid showing the full inventory, no view toggle: the first
    # 10 show, the expand control reveals the rest.
    assert b'id="projects-grid"' in resp.data
    assert b'id="projects-expand-btn"' in resp.data
    projects_js = client.get('/static/js/projects.js').data
    assert b'PROJECTS_INITIAL_COUNT = 10' in projects_js
    assert b'toggleProjectsView' not in resp.data
    assert b'id="recentBtn"' not in resp.data
    assert b'id="featuredBtn"' not in resp.data
    assert b'id="allBtn"' not in resp.data
    assert b'recent-projects' not in resp.data
    assert b'featured-projects' not in resp.data
    assert b'all-projects' not in resp.data
    # The About eyebrow repeated name + location; both already live in
    # the sidebar card, so the eyebrow is gone from the main card.
    assert b'Justin P. Lyons &mdash; Fredericksburg, VA' not in resp.data
    assert b'Justin P. Lyons' in resp.data
    assert b'Fredericksburg, VA' in resp.data


def test_homepage_projects_come_from_github_not_a_catalog(client):
    resp = client.get('/')
    assert b'projects-grid' in resp.data
    assert b'github.com/enonymous1?tab=repositories' in resp.data
    # No baked-in project routes remain on the homepage.
    assert b'gsa-mas-checklist' not in resp.data
    assert b'schedule-maker' not in resp.data


def test_contact_section_has_map_and_mailto_form(client):
    resp = client.get('/')
    # Map + form, like the demo's Contact card, instead of a second
    # copy of the sidebar's contact list. No phone or birthday fields:
    # those were the demo's fictional data, not Justin's.
    assert b'id="contact-form"' in resp.data
    assert b'js/contact.js' in resp.data
    contact_js = client.get('/static/js/contact.js').data
    assert b'buildContactMailto' in contact_js
    # No inline handler: the form submits through the module listener.
    assert b'onsubmit' not in resp.data
    assert b'Open in Maps' in resp.data
    assert b'maps.google.com/maps?q=Fredericksburg' in resp.data
    assert b'Send Message' in resp.data
    assert b'No contact form on purpose' not in resp.data
    assert b'placeholder="Full name"' in resp.data
    assert b'placeholder="Email address"' in resp.data
    assert b'placeholder="Your Message"' in resp.data
    # The contact list appears once, in the sidebar only.
    assert resp.data.count(b'class="vcard-contact"') == 1
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.contact-map' in css
    assert '.contact-form' in css


def test_homepage_links_to_retro_mode(client):
    resp = client.get('/')
    assert b'/retro/' in resp.data
    assert b"'My' Space" in resp.data


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
    # The showcase list reaches the page as config JSON, and the grid
    # module reads it from there.
    assert b'retroShowcase' in resp.data
    top8_js = client.get('/static/js/retro-top8.js').data
    assert b'retroShowcase' in top8_js


def test_retro_grid_cannot_overflow_on_long_repo_names():

    import pathlib

    css = pathlib.Path('static/css/retro.css').read_text()
    # Grid tracks must allow shrinking below their longest unbreakable word
    # (repo names with underscores), or the right-hand cards flow past the
    # page container — the bug reported from the Top 8 screenshot.
    assert 'minmax(0, 1fr)' in css
    assert 'overflow-wrap: anywhere' in css


def test_profile_photo_is_a_local_image_not_the_silhouette():

    from config.projects import ABOUT_ME

    assert ABOUT_ME.profile_image == 'images/profile.jpg'
    import pathlib

    photo = pathlib.Path('static') / ABOUT_ME.profile_image
    assert photo.exists()
    assert photo.read_bytes()[:3] == b'\xff\xd8\xff'  # JPEG magic bytes


def test_vcard_section_titles_repeat_the_active_tab(client):
    resp = client.get('/')
    # Each section opens with a title mirroring its tab, like the demo:
    # About -> "About Me", Projects -> "Projects", Contact -> "Contact".
    assert b'class="vcard-section-title">About Me</h2>' in resp.data
    assert b'class="vcard-section-title">Projects</h2>' in resp.data
    assert b'class="vcard-section-title">Websites</h2>' in resp.data
    assert b'class="vcard-section-title">Contact</h2>' in resp.data
    assert b'Featured Projects' not in resp.data
    # Poppins, the demo's font, loaded only on the homepage.
    assert b'family=Poppins' in resp.data

    css = client.get('/static/css/vcard.css').data.decode()
    assert '--vcard-radius: 20px' in css
    assert 'font-size: 36px' in css
    assert 'vcard-section-title::after' in css
    assert '.vcard-main .vcard-section-title' in css
    # Avatar is a rounded square now, not a circle. (The 50% in the
    # file belongs to .lang-dot, which is meant to be round.)
    avatar_rule = css.split('.vcard-avatar')[1].split('}')[0]
    assert '50%' not in avatar_rule


def test_vcard_css_is_cache_busted(client):
    resp = client.get('/')
    assert b'css/vcard.css?v=' in resp.data


def test_repo_preview_modal_present(client):
    resp = client.get('/')
    assert b'id="repo-modal"' in resp.data
    assert b'id="repo-modal-content"' in resp.data
    assert b'data-modal-close' in resp.data
    # Card markup (including data-repo-name) is rendered by the grid module.
    assert b'data-repo-name' in client.get('/static/js/projects.js').data
    # The modal code lives in modules; the GitHub user reaches it
    # through page config, not a hardcoded URL in the markup.
    assert b'js/repo-modal.js' in resp.data
    assert b'js/readme-md.js' in resp.data
    modal_js = client.get('/static/js/repo-modal.js').data
    assert b'openRepoModal' in modal_js
    assert b'api.github.com/repos/' in modal_js
    readme_js = client.get('/static/js/readme-md.js').data
    assert b'renderMarkdown' in readme_js
    assert b'githubUser' in resp.data
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.repo-modal' in css
    assert '.repo-modal-card' in css
    assert '.repo-card-thumb' in css


def test_sidebar_pokemon_go_button_opens_modal(client):
    # The Poké Ball sits in the sidebar social row next to GitHub,
    # LinkedIn and email; it opens a modal with the trainer name and
    # friend code, plus a Copy button. The About highlights no longer
    # carry the line — the modal is its only home on the clean site.
    home = client.get('/').data
    assert b'id="pokemon-modal-open"' in home
    assert 'Pokémon GO — Trainer enonymous1'.encode() in home
    assert b'id="pokemon-modal"' in home
    assert b'Trainer enonymous1' in home
    assert b'8456 7104 2978' in home
    assert b'id="pokemon-copy-code"' in home
    assert 'Plays Pokémon GO'.encode() not in home
    # The modal is shared with the blog post pages, and the narrow card
    # and button box rules ship in the same stylesheet.
    post = client.get('/blog/interesting-links/').data
    assert b'id="pokemon-modal"' in post
    assert b'repo-modal-card pokemon-card' in home
    assert b'.vcard-social button' in client.get('/static/css/vcard.css?v=20261121-02').data


def test_retro_contact_lists_pokemon_go(client):
    # Retro has no modals, so the trainer card stays a plain line in
    # its Contacting Justin list instead of disappearing with the
    # About highlight it used to ride on.
    retro = client.get('/retro/').data
    assert b'Trainer enonymous1' in retro
    assert b'8456 7104 2978' in retro


def test_websites_tab_sorts_web_languages_first(client):
    # The Websites tab's default order is web-first (HTML/JavaScript/
    # TypeScript), then the rest, recently updated inside each group.
    # The default sort key is 'web', and that branch delegates to the
    # shared sortWebsites helper in repo-loader.js.
    projects_js = client.get('/static/js/projects.js').data
    assert b"websiteSortKey = 'web'" in projects_js
    assert b'return sortWebsites(repos);' in projects_js
    loader_js = client.get('/static/js/repo-loader.js').data
    assert b"WEBSITE_FIRST_LANGUAGES = ['HTML', 'JavaScript', 'TypeScript']" in loader_js


def test_homepage_vcard_tabs(client):
    resp = client.get('/')
    assert b'vcard-layout' in resp.data
    assert b'vcard-sidebar' in resp.data
    for tab in (
        b'data-vcard-tab="about"',
        b'data-vcard-tab="projects"',
        b'data-vcard-tab="websites"',
        b'data-vcard-tab="contact"',
    ):
        assert tab in resp.data
    assert b'data-vcard-section="projects"' in resp.data
    assert b'data-vcard-section="websites"' in resp.data
    assert b'id="websites-grid"' in resp.data
    # The Websites tab deep-links like the others.
    tabs_js = client.get('/static/js/tabs.js').data
    assert b"'websites'" in tabs_js
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

    css = client.get('/static/css/vcard.css').data.decode()
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
    # Wrapper cap widened 1280px -> 1600px on 2026-11-25 (dead space at
    # 2560px fell from ~640px to ~480px per side); the w-full + cap
    # structure above is unchanged, so the width still cannot depend
    # on which tab is active.
    assert b'w-full max-w-[1600px]' in resp.data


def test_retro_theme_toggle(client):

    resp = client.get('/retro/')
    assert b'id="retro-theme-toggle"' in resp.data
    assert b'jpl_retro_theme' in resp.data
    import pathlib

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


def test_latin_quips_easter_egg(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'id="latin-quip"' in resp.data
    assert b'course of life' in resp.data
    assert b'latin-quips.js' in resp.data
    # The quips live in the JS file, not the initial HTML.
    js = client.get('/static/latin-quips.js')
    assert js.status_code == 200
    assert b'Ex memoria' in js.data
    assert b'dum (verum) { spero; }' in js.data
    assert b'Condo, ergo sum' in js.data
    assert b'in localhost' in js.data
    assert b'Tabula rasa' in js.data
    assert b'Deus ex machina' in js.data
    # Blog post pages have no CV section, so no Latin quip button.
    post = client.get('/blog/interesting-links/')
    assert b'id="latin-quip"' not in post.data


def test_project_thumbnails_mapping(client):
    import os

    from config.projects import PROJECT_THUMBNAILS

    assert PROJECT_THUMBNAILS
    for repo, path in PROJECT_THUMBNAILS.items():
        assert repo and path.startswith('images/project-thumbs/')
        full = os.path.join('static', path)
        assert os.path.isfile(full), f'missing thumbnail file: {full}'
        assert os.path.getsize(full) > 0
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'projectThumbnails' in resp.data
    for path in PROJECT_THUMBNAILS.values():
        assert path.encode() in resp.data
    # No thumbnail or site button on the retro list: cards only.
    retro = client.get('/retro/')
    assert b'repo-card-thumb' not in retro.data


def test_wide_thumbnails_mapping(client):
    import os

    from config.projects import PROJECT_THUMBNAILS, WIDE_THUMBNAILS

    # Wide composites are a subset of the thumbnail map, one file each,
    # and the homepage injects the set so renderRepoCard can add the
    # wider thumb class for exactly those repos.
    assert WIDE_THUMBNAILS
    assert WIDE_THUMBNAILS <= set(PROJECT_THUMBNAILS)
    for repo in WIDE_THUMBNAILS:
        full = os.path.join('static', PROJECT_THUMBNAILS[repo])
        assert os.path.isfile(full), f'missing wide thumbnail file: {full}'
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'wideThumbnails' in resp.data
    for repo in WIDE_THUMBNAILS:
        assert repo.encode() in resp.data
    css = client.get('/static/css/vcard.css').data.decode()
    wide_rule = css.split('.repo-card-thumb-wide')[1].split('}')[0]
    assert 'aspect-ratio: 9 / 4' in wide_rule


def test_project_card_buttons_are_labeled(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # Buttons carry their destination as visible text now; the old
    # ambiguous hover-only "Preview" hint is gone. Button labels live
    # in the grid module's card template.
    assert b'Pages site' in client.get('/static/js/projects.js').data
    assert b'repo-card-hint' not in resp.data


def test_project_thumbnails_fit_container(client):
    css = client.get('/static/css/vcard.css').data.decode()
    # The thumbnail rule scales to fit (contain), never crop: cover
    # cut the top and bottom off non-16:9 screenshots. (The avatar
    # rule elsewhere legitimately still uses cover.)
    thumb_rule = css.split('.repo-card-thumb')[1].split('}')[0]
    assert 'object-fit: contain' in thumb_rule


def test_project_modal_scrollbar_is_themed(client):
    css = client.get('/static/css/vcard.css').data.decode()
    thumb_rule = css.split('.repo-modal-card::-webkit-scrollbar-thumb')[1].split('}')[0]
    # Thumb in the border color, not the secondary text color: #b0b0b0
    # in dark mode read as a bright, unstyled bar (caught from a
    # screenshot of the voice-generator preview).
    assert 'var(--border-color)' in thumb_rule
    assert 'scrollbar-width: thin' in css
    assert 'scrollbar-color: var(--border-color)' in css


def test_repo_preview_modal_is_wide(client):
    # The repo preview renders README tables, so it alone gets the
    # 920px card; glossary/location/avatar modals keep the 720px one.
    # At 720px "Backend" squeezed into "Backe nd" in the
    # voice-generator preview. Table cells break words only when a
    # token cannot fit, instead of the container's `anywhere`.
    resp = client.get('/')
    assert b'repo-modal-card repo-modal-wide' in resp.data
    css = client.get('/static/css/vcard.css').data.decode()
    wide_rule = css.split('.repo-modal-card.repo-modal-wide')[1].split('}')[0]
    assert 'min(920px, 100%)' in wide_rule
    cell_rule = css.split('.repo-modal-readme td,')[1].split('}')[0]
    assert 'overflow-wrap: break-word' in cell_rule


def test_homepage_and_retro_load_js_modules_with_config(client):
    # Page config carries site identity to the modules; retro loads its
    # own pair of modules, not the homepage grid/modal code.
    home = client.get('/')
    assert b'js/repo-loader.js' in home.data
    assert b'js/projects.js' in home.data
    assert b'js/repo-modal.js' in home.data
    assert b'js/tabs.js' in home.data
    assert b'js/contact.js' in home.data
    assert b'githubUser' in home.data
    assert b'contactEmail' in home.data
    retro = client.get('/retro/')
    assert b'js/repo-loader.js' in retro.data
    assert b'js/retro-top8.js' in retro.data
    assert b'js/retro-theme.js' in retro.data
    assert b'retroShowcase' in retro.data
    assert b'js/projects.js' not in retro.data
    assert b'js/repo-modal.js' not in retro.data

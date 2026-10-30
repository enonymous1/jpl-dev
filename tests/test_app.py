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
    assert b"chip('All', repos.length, false)" in resp.data
    assert b"selectedLanguage = (lang === selectedLanguage) ? 'All' : lang" in resp.data
    assert b'renderLanguageFilters' in resp.data
    assert b'LANGUAGE_COLORS' in resp.data

    css = client.get('/static/css/vcard.css').data.decode()
    assert '.language-filter-btn' in css
    assert '.lang-dot' in css


def test_vcard_tab_sections_animate_on_switch(client):
    resp = client.get('/')
    assert b'vcard-section-enter' in resp.data
    assert b'void s.offsetWidth' in resp.data
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


def test_about_build_cards_and_tool_labels(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # The repetitive intro paragraph is gone; the hero line and bio stay.
    assert b'shipped as tested, documented tools, not demos' not in resp.data
    assert b'I build tools that automate repetitive work.' in resp.data
    assert b'What I Build' in resp.data
    assert resp.data.count(b'class="build-card"') == 4
    assert b'Automation &amp; data' in resp.data
    assert b'Desktop tools' in resp.data
    assert b'Data pipelines' in resp.data
    assert b'bi bi-gear' in resp.data
    assert b'bi bi-pc-display' in resp.data
    assert b'bi bi-globe' in resp.data
    assert b'bi bi-diagram-3' in resp.data
    assert resp.data.count(b'class="build-card-header"') == 4
    assert resp.data.count(b'badge-theme build-card-link') == 5
    assert b'GSA pricing toolkits</span>' in resp.data
    assert b'replace repetitive manual work' in resp.data
    assert b'photos, messages, and video' in resp.data
    assert b'Minecraft-style voxel landing page' in resp.data
    assert b'capture and process market data' in resp.data
    assert b'href="https://github.com/enonymous1/repo-sync"' in resp.data
    assert b'href="https://github.com/enonymous1/kalshi-recorder"' in resp.data
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
    assert '.vcard-quip' in css
    assert 'prefers-reduced-motion' in css
    # Retro keeps its plain photo: the easter egg is shared by the
    # homepage and the blog post pages only.
    retro = client.get('/retro/')
    assert b'avatar-easter-egg' not in retro.data


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
    resp = client.get('/')
    assert b'repo-card-tags' in resp.data
    assert b'repo-card-actions' in resp.data
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
    assert b'PROJECTS_INITIAL_COUNT = 10' in resp.data
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
    assert b'buildContactMailto' in resp.data
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
    assert b'openRepoModal' in resp.data
    assert b'renderMarkdown' in resp.data
    assert b'data-repo-name' in resp.data
    assert b'api.github.com/repos/enonymous1/' in resp.data
    css = client.get('/static/css/vcard.css').data.decode()
    assert '.repo-modal' in css
    assert '.repo-modal-card' in css
    assert '.repo-card-hint' in css


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
    assert b'w-full max-w-7xl' in resp.data


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

# templates/

Jinja2 templates for the Flask application. All templates here are
rendered by routes defined in `app.py`. There are no blueprints: every
route renders one of these files directly.

## Structure

```
templates/
├── index.html           # Homepage (route: /) — vCard sidebar + tabbed card
├── blog_post.html       # One blog post (route: /blog/<slug>/), vCard shell
├── retro.html           # Retro skin (route: /retro/)
├── base.html            # Shell used ONLY by the 404 page (nav + theme)
├── 404.html             # Not-found page (also written to docs/404.html by freeze.py)
├── _vcard_sidebar.html  # Shared sidebar (homepage + blog post pages)
└── _glossary_modal.html # Shared glossary/role modal shell
```

`base.html` is not a master layout: the homepage and retro are standalone
pages with no global top nav (the sidebar carries contact, the retro
link, and the theme toggle, so a top bar was duplication). Only the 404
page extends `base.html`.

## Homepage scripts

`index.html` loads its behavior from `static/js/` modules, in order:

```
global-theme.js   # theme toggle (also loaded by blog posts + 404)
JPL_CONFIG        # inline: githubUser, contactEmail, projectThumbnails,
                  # glossary data — rendered server-side, read at call time
js/repo-loader.js # shared repo fetch/filter/site-URL/language helpers
js/readme-md.js   # dependency-free Markdown renderer for READMEs
js/projects.js    # Projects grid: chips, search, sort, expand
js/repo-modal.js  # preview modal: README fetch, focus trap, clone copy
js/tabs.js        # vCard tab switching + deep links + CV print button
js/contact.js     # mailto contact form
avatar-easter-egg.js, latin-quips.js, glossary-modal.js
```

`retro.html` loads `js/repo-loader.js` plus its own `js/retro-top8.js`
(Top 8 grid) and `js/retro-theme.js` (independent theme toggle). It does
not load the homepage grid/modal code.

## Context variables

Routes pass site identity from `config/site.py` (`site_url`,
`github_user`, `linkedin_slug`, `contact_email`) to every template, so
no template hardcodes the domain, the GitHub user, or the contact
address. The homepage additionally receives `about`, `posts`,
`glossary_data`, `role_definitions`, `project_thumbnails`, and the
`resume_*` values; retro receives `about` and `retro_showcase`.

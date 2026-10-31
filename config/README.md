# config/

Python data modules for the site. No route logic lives here — `app.py`
imports these values and passes them to templates.

## `site.py` — Site identity (single source of truth)

`SITE_URL`, `GITHUB_USER`, `LINKEDIN_SLUG`, `CONTACT_EMAIL`, each read
from the environment with the live value as default. `app.py`,
`freeze.py`, `fetch_repos.py`, and the templates all import from here;
nothing re-derives these values, so a renamed user or a moved domain
changes in exactly one place.

## `projects.py` — About-me data

Holds only `ABOUT_ME`, the profile data rendered by the homepage and
retro mode (name, bio, profile photo, badges, highlights, tool groups),
plus `PROJECT_THUMBNAILS` (card thumbnails by repo name),
`RETRO_SHOWCASE` (the curated Top 8 list), `GLOSSARY` (one definition
per Tools & Tech pill), and `ROLE_DEFINITIONS` (the three role pills).
Every glossary/role definition here is the approved wording; changing
one changes the modal everywhere it appears.

Project data used to live here as a baked-in catalog, along with the
`/projects` page and the GSA MAS Checklist and Schedule Maker
blueprints. Those were removed: project listings now come from GitHub
— the homepage Projects tab loads `static/data/repos.json` (refreshed
by `fetch_repos.py` in CI) with a live GitHub API fallback, and retro's
Top 8 uses the same source.

## `models.py` — Profile models

`AboutMe`, `ToolGroup`, and `GlossaryEntry` dataclasses for the profile
data above.

## `blog.py` — Blog posts

`Post`, `load_posts`, `parse_post`, `slugify`, and
`build_post_source`. Posts are Markdown files in `content/posts/` with
a front-matter block; the loader validates strictly (required keys,
slug shape, real dates, non-empty bodies, duplicate slugs) and fails
loudly, so a bad post breaks the build instead of publishing
half-rendered. `content/drafts/` is never read. Bodies render with raw
HTML allowed and no sanitizer: posts are the author's own files, so do
not feed untrusted Markdown through this loader.

## `resume.py` — Curriculum Vitae data

Headline, summary, jobs, education, certifications, top skills, and
languages for the CV tab. Transcribed from the author's LinkedIn and
CV PDFs; the module docstring records exactly what was merged, what
was deliberately left out, and the two values (mobile phone, Gmail)
that must never render on the public site.

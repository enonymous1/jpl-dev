# config/

## `projects.py` — About-me data

Holds only `ABOUT_ME`, the profile data rendered by the homepage and retro
mode (name, title, bio, profile photo, badges, highlights, tool groups).

Project data used to live here as a baked-in catalog, along with
`data_access.py` and the `ProjectData` models. That catalog, the
`/projects` page, and the GSA MAS Checklist and Schedule Maker blueprints
were removed: project listings now come from GitHub — the homepage
Projects tab loads `static/data/repos.json` (refreshed by
`fetch_repos.py` in CI) with a live GitHub API fallback, and retro's
Top 8 uses the same source.

## `models.py` — Profile models

`AboutMe`, `ToolGroup`, and `Skill` dataclasses for the profile data above.

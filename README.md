# JPL-DEV — Justin P. Lyons Digital Portfolio

My portfolio site, live at [justinlyons.dev](https://justinlyons.dev). Flask for development ergonomics, frozen to static files for $0 GitHub Pages hosting — no live server, no database, no auth surface to maintain.

## 🚀 Live Site

Visit the live site at: [justinlyons.dev](https://justinlyons.dev)

## 🏗️ Architectural Philosophy: The Static Hybrid Model

This portfolio intentionally rejects heavy monolithic frameworks and database overhead in favor of a Thick Client / Static Backend architecture.

### Why this route?

- **Low infrastructure cost**: $0 hosting on GitHub Pages
- **Security-first delivery**: no live server runtime, no SQL injection surface
- **Performance at scale**: pre-rendered static pages and edge-friendly assets
- **Modular engineering**: Flask Blueprints and client-side state keep projects isolated and maintainable

### The Engineering Green Flags

- **Modular Flask Blueprint Architecture**: sub-projects like the GSA MAS Checklist are built as self-contained Flask Blueprints, so the repo scales like a real Python web application rather than a flat site.
- **Flask-Frozen compilation**: `freeze.py` crawls the Flask app at build time and produces static output in `docs/` (build output, not tracked in git), combining dynamic development ergonomics with static deployment simplicity. It also writes `404.html`, `robots.txt` and `sitemap.xml` for the static host.
- **Thick client state management**: statically generated pages rely on browser APIs such as `localStorage` and `IndexedDB` for persistence, enabling rich client-side experiences without a dynamic server.

## ⚖️ Alternative Architectural Routes & Trade-offs

As the platform grows, the next evolution depends on persistence and runtime requirements.

| Architectural Route | Infrastructure Change | What it Enables | Engineering Trade-off |
| --- | --- | --- | --- |
| **Current Static Route** (Flask + Frozen) | GitHub Pages static host | $0 hosting, maximum speed, edge caching, localized client state | No live Python runtime; state persistence limited to browser APIs |
| **Dynamic Monolith** (Flask + live DB) | Migrate to PaaS (Render, Railway, Fly.io) | Persistent database, user auth, live REST endpoints | Hosting cost, server latency, runtime security surface |
| **Cloud-Native Hybrid** (Jamstack) | Static host + serverless / BaaS | Cloud-synced user state via Supabase/Firebase with static shell | More client-side async plumbing; less Python runtime dependence |

## 🎨 Features

- **Modular CSS Architecture** — Logical styling modules for maintainability
- **Dark/Light Theme Toggle** — Client-side theme switching with system preference detection
- **Interactive GSA MAS Checklist** — Tool for GSA proposal preparation using JSON datasets and browser persistence
- **Schedule Maker** — Client-side schedule tool, saved in browser storage and exported as JSON
- **Component Library** — `/widget-demo/` showcases the cards, badges and repo cards used across the site
- **Retro Mode** — `/retro/` is an optional MySpace-style skin over the same About, Projects, and repo data as the clean homepage. The clean site is the default; retro mode is reached from the homepage sidebar and links back. No autoplay music, no fake friends, and it freezes like any other route. Retro mode has its own light/dark toggle, saved separately from the clean site's theme.
- **vCard Homepage** — The homepage is a sidebar + tabbed main card (About / Projects / Contact) in the style of a vCard portfolio, written for this site rather than copied from a template. Sections switch without a reload and deep-link via `#about`, `#projects`, `#contact`. No blog, testimonials, or resume sections: those would be filler without real content behind them.
- **Responsive Design** — Modern CSS layouts scaling across device sizes
- **Smart Tooltips** — Positioning algorithms to prevent off-screen clipping

## 🛠️ Development

### Prerequisites

- Python 3.11 or higher (uses PEP 585 built-in generic types — `tuple[...]`, `list[...]`)
- Node.js 24 for the Tailwind CSS build (only needed when template classes change)
- pip (Python package installer)

### Local Development

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install dev dependencies (tests + lint)
pip install -r requirements-dev.txt

# Run development server
python app.py
```

### Build Tailwind CSS

CI rebuilds both Tailwind bundles before freezing, so the committed CSS is only a local-dev convenience. Rebuild it after changing template classes:

```bash
# Site root
npx --yes tailwindcss@3.4.19 \
  -c tailwind.config.js \
  -i static/css/tailwind.input.css \
  -o static/css/tailwind.css \
  --minify

# Schedule Maker
npx --yes tailwindcss@3.4.19 \
  -c projects/schedule_maker/tailwind.config.js \
  -i projects/schedule_maker/tailwind.input.css \
  -o static/projects/schedule_maker/tailwind.css \
  --minify
```

### Refresh GitHub repo data

```bash
# Fetches public repos (paginated, forks/archived filtered out) into
# static/data/repos.json. On an API failure it keeps the cached file
# and warns instead of failing the build.
python fetch_repos.py
```

### Generate Static Site

```bash
# Generate static site in docs/ (ignored by git; CI builds it for Pages)
python freeze.py
```

### Checks

```bash
ruff check .
ruff format --check .
pytest
```

## 📦 Deployment

The site deploys to GitHub Pages when changes are pushed to `main` via GitHub Actions.

The automated workflow:

1. Runs lint (`ruff check`, `ruff format --check`) and tests (`pytest`) on Python 3.11 and 3.12 — deploys only if they pass
2. Builds both Tailwind CSS bundles
3. Refreshes GitHub repo metadata with `fetch_repos.py`
4. Runs Flask-Frozen to crawl and compile dynamic routes into flat static files in `docs/`, plus `404.html`, `robots.txt` and `sitemap.xml`
5. Injects the `CNAME` for `justinlyons.dev` and deploys the artifact to GitHub Pages

Pull requests run the same lint/test/build steps without deploying.

## 📁 Project Structure

```
├── app.py                 # Flask application entry point (create_app factory)
├── freeze.py              # Static site compiler + 404/robots/sitemap generation
├── fetch_repos.py         # GitHub repo metadata cache (static/data/repos.json)
├── templates/             # Core Jinja2 structural layouts
├── config/                # Data models and central data repositories
├── static/                # Global static assets
│   ├── css/               # Modular styling rules (+ Tailwind input/output)
│   ├── files/             # Downloadable resources
│   └── projects/          # Sub-project specific stylesheets and scripts
├── projects/              # Modular blueprint packages (sub-apps)
├── tests/                 # pytest smoke + unit tests
├── pyproject.toml         # ruff + pytest configuration (no installable package)
├── requirements.txt       # Runtime dependencies
├── requirements-dev.txt   # Dev dependencies (pytest, ruff)
├── .python-version        # 3.12 (CI also tests 3.11)
└── .github/workflows/     # CI + Pages deploy pipeline
```

`docs/` is generated by `freeze.py` and intentionally not tracked — do not commit it.

## 📄 License

MIT — see [LICENSE](LICENSE).

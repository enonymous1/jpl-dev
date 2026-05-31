# JPL-DEV - Justin P. Lyons Digital Portfolio

Hey there, welcome to my digital sandbox! Here, I experiment with code, share my musings, and build things that spark joy. Grab a seat, explore, and let's get acquainted.

## 🚀 Live Site
Visit the live site at: [justinlyons.dev](https://justinlyons.dev)

## 🏗️ Architectural Philosophy: The Static Hybrid Model
This portfolio intentionally rejects heavy monolithic frameworks and database overhead in favor of a Thick Client / Static Backend architecture.

### Why this route?
It delivers a clean engineering profile with:
- **Low infrastructure cost**: $0 hosting on GitHub Pages
- **Security-first delivery**: no live server runtime, no SQL injection surface
- **Performance at scale**: pre-rendered static pages and edge-friendly assets
- **Modular engineering**: Flask Blueprints and client-side state keep projects isolated and maintainable

### The Engineering Green Flags
- **Modular Flask Blueprint Architecture**: sub-projects like the GSA MAS Checklist are built as self-contained Flask Blueprints, so the repo scales like a real Python web application rather than a flat site.
- **Flask-Frozen compilation**: `freeze.py` crawls the Flask app at build time and produces optimized static output in `docs/`, combining dynamic development ergonomics with static deployment simplicity.
- **Thick client state management**: statically generated pages rely on browser APIs such as `localStorage` and `IndexedDB` for persistence, enabling rich client-side experiences without a dynamic server.

## ⚖️ Alternative Architectural Routes & Trade-offs
As the platform grows, the next evolution depends on persistence and runtime requirements.

| Architectural Route | Infrastructure Change | What it Enables | Engineering Trade-off |
| --- | --- | --- | --- |
| **Current Static Route** (Flask + Frozen) | GitHub Pages static host | $0 hosting, maximum speed, edge caching, localized client state | No live Python runtime; state persistence limited to browser APIs |
| **Dynamic Monolith** (Flask + live DB) | Migrate to PaaS (Render, Railway, Fly.io) | Persistent database, user auth, live REST endpoints | Hosting cost, server latency, runtime security surface |
| **Cloud-Native Hybrid** (Jamstack) | Static host + serverless / BaaS | Cloud-synced user state via Supabase/Firebase with static shell | More client-side async plumbing; less Python runtime dependence |

## 🎨 Features
- **Modular CSS Architecture** - Logical styling modules for maintainability
- **Dark/Light Theme Toggle** - Client-side theme switching with system preference detection
- **Interactive GSA MAS Checklist** - Heavy static tool for GSA proposal preparation using JSON datasets and browser persistence
- **Responsive Design** - Modern CSS layouts scaling across device sizes
- **Smart Tooltips** - Positioning algorithms to prevent off-screen clipping

## 🛠️ Development

### Prerequisites
- Python 3.9 or higher (uses PEP 585 built-in generic types — `tuple[...]`, `list[...]`)
- pip (Python package installer)

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Generate Static Site
```bash
# Generate static site in docs/ directory
python freeze.py
```

## 📦 Deployment
The site deploys to GitHub Pages when changes are pushed to `main` via GitHub Actions.

The automated workflow:
1. Installs Python dependencies
2. Runs Flask-Frozen to crawl and compile dynamic routes into flat static files
3. Outputs the build into `docs/`
4. Deploys the static site to GitHub Pages using the custom domain `justinlyons.dev`

## 📁 Project Structure

```
├── app.py                 # Flask application entry point
├── freeze.py              # Static site compiler configuration
├── templates/             # Core Jinja2 structural layouts
├── config/                # Data models and central data repositories
├── static/                # Global static assets
│   ├── css/               # Modular styling rules
│   ├── files/             # Downloadable resources
│   └── projects/          # Sub-project specific stylesheets and scripts
├── projects/              # Modular blueprint packages (sub-apps)
├── docs/                  # Statically compiled site target (GitHub Pages deployment)
└── .github/workflows/     # CI/CD automation pipeline configurations
```

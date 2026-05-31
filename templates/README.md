# templates/

Jinja2 templates for the core Flask application. All templates here are
rendered by routes defined in `app.py`.

Blueprint templates live alongside their blueprint — not here. Each blueprint
package registers its own `templates/` subfolder via `template_folder='templates'`
on the `Blueprint(...)` constructor.

## Structure

```
templates/
├── base.html          # Master layout — all other templates extend this
├── index.html         # Homepage  (route: /)
├── projects.html      # Projects listing  (route: /projects)
└── widget_demo.html   # Widget demo page  (route: /widget-demo)
```

Blueprint templates live alongside their blueprint:

```
projects/gsa_mas_checklist/templates/
└── gsa_mas_checklist.html   # GSA MAS Checklist  (route: /projects/gsa-mas-checklist)

projects/schedule_maker/templates/
└── schedule_maker.html      # Schedule Maker  (route: /projects/schedule-maker)
```

## base.html

The shared layout shell. Provides:

- `<head>` with Bootstrap 5.3.2 CDN (SRI), Bootstrap Icons, and all custom CSS
- Inline theme-init script (reads `jpl_dev_global_theme` from `localStorage`
  before first paint to prevent flash of unstyled content)
- `global-theme.js` deferred at end of `<body>`
- Bootstrap 5 JS bundle CDN (SRI) at end of `<body>`

### Blocks

| Block | Purpose |
|-------|---------|
| `title` | `<title>` text (appended with ` - JPL-DEV`) |
| `head` | Extra `<head>` content — used by pages that load GridStack CSS/JS |
| `content` | Main page body |
| `scripts` | Per-page JS loaded before `</body>` |

## Page Templates

| Template | Route | Rendered by | Notable context vars |
|----------|-------|-------------|----------------------|
| `index.html` | `/` | `app.py` | — |
| `projects.html` | `/projects` | `app.py` | `projects`, `ProjectStatus` |
| `widget_demo.html` | `/widget-demo` | `app.py` | — |

## GridStack

GridStack 9.2.0 CSS/JS is **page-scoped** — loaded only in `index.html` and
`widget_demo.html` via `{% block head %}`. It is not in `base.html`.

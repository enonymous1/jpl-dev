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
├── widget_demo.html   # Component library demo  (route: /widget-demo)
└── 404.html           # Not-found page (also written to docs/404.html by freeze.py)
```

Blueprint templates live alongside their blueprint:

```

```

## base.html

The shared layout shell. Provides:

- `<head>` with meta/OG description, Bootstrap Icons (icon font only — Bootstrap
  CSS and JS were removed in the Tailwind migration), Tailwind CSS built via
  the CLI, and all custom CSS
- Inline theme-init script (reads `jpl_dev_global_theme` from `localStorage`
  before first paint to prevent flash of unstyled content)
- `global-theme.js` deferred at end of `<body>`, plus `script.js`

### Blocks

| Block | Purpose |
|-------|---------|
| `title` | `<title>` text (appended with ` - JPL-DEV`) |
| `head` | Extra `<head>` content for a page |
| `content` | Main page body |
| `footer` | Page footer, where a page defines one |
| `scripts` | Per-page JS loaded before `</body>` |

## Page Templates

| Template | Route | Rendered by | Notable context vars |
|----------|-------|-------------|----------------------|
| `index.html` | `/` | `app.py` | `about` |
| `widget_demo.html` | `/widget-demo` | `app.py` | — |
| `404.html` | (error handler) | `app.py` | — |

## Component system

The site no longer uses Bootstrap or GridStack. Cards, badges and repo cards
are plain Tailwind utilities plus the component classes in
`static/css/tailwind.input.css` (`.widget-card`, `.badge-theme`, `.repo-card`).
The orphaned Bootstrap/GridStack CSS and JS (`bootstrap-theme.css`,
`widget-system.css`, `widgets.css`, `widget-manager.js`, `widget-utils.js`)
were deleted — they were not loaded by any template.

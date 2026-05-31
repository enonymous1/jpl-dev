# config/ — Data Layer

This directory is the **single source of truth** for all portfolio project metadata. It is a pure Python package with zero Flask dependencies — every module imports cleanly at build time so `freeze.py` can interrogate the catalog without starting a live server.

## Files

### `models.py` — Schema definitions

Defines all dataclasses and enums that describe a portfolio project.

| Symbol | Type | Purpose |
|---|---|---|
| `ProjectStatus` | `str+Enum` | Valid lifecycle states for a project |
| `ProjectCategory` | `str+Enum` | Category taxonomy for filtering/display |
| `ProjectImage` | `@dataclass` | Image metadata (filename, alt text, hero/thumbnail flags) |
| `ProjectLinks` | `@dataclass` | Optional external URLs (GitHub, demo, live site, docs) |
| `ProjectData` | `@dataclass` | Top-level project record; owns all of the above |

**`ProjectStatus` values**

```python
ProjectStatus.ACTIVE       # "active"      — live, maintained
ProjectStatus.DEVELOPMENT  # "development" — work in progress
ProjectStatus.COMPLETED    # "completed"   — finished, not actively maintained
ProjectStatus.ARCHIVED     # "archived"    — no longer relevant
ProjectStatus.FEATURED     # "featured"    — highlighted on the homepage
```

**`ProjectData.__post_init__`** performs construction-time validation:
- Validates `status` against `ProjectStatus`; raises `ValueError` on invalid values.
- Normalises `created_date` / `last_updated` so both are always populated if either is set.
- Initialises `links` to an empty `ProjectLinks()` if `None`, so templates can always access `project.links.*` without a `None` guard.

---

### `projects.py` — Project catalog

The **canonical list of portfolio projects**. Add, edit, or remove projects here.

```
_PROJECTS        list[ProjectData]   — mutable catalog (internal)
PROJECTS_SORTED  tuple[ProjectData]  — immutable, sorted for consumption
```

**Sort order**: `(priority DESC, last_updated DESC)` — highest-priority projects appear first; ties broken by most-recently-updated. `datetime.min` is used as a fallback so projects without dates always sort to the bottom rather than erroring.

**Adding a project**

```python
ProjectData(
    id="my_project",                      # unique snake_case ID
    title="My Project",
    description="One paragraph description.",
    status=ProjectStatus.DEVELOPMENT,
    category=ProjectCategory.WEB_APP,
    features=["Feature A", "Feature B"],
    tech_stack=["Flask", "JavaScript"],
    tags=["tag1", "tag2"],
    route="my_project.my_project",        # Blueprint endpoint name, or None
    links=ProjectLinks(
        github="https://github.com/...",
    ),
    created_date=datetime(2026, 1, 1),
    priority=5,                           # higher = appears first
)
```

The Blueprint is auto-discovered by `register_project_blueprints()` in `app.py` — **do not** manually call `app.register_blueprint()`.

---

### `data_access.py` — Query interface

Thin read-only access layer over `PROJECTS_SORTED`. Use these functions instead of importing `projects.py` directly so call sites get cache benefits and immutability guarantees.

| Function | Returns | Notes |
|---|---|---|
| `get_all_projects()` | `tuple[ProjectData, ...]` | All projects in sort order. `@lru_cache` — free on repeat calls. |
| `get_project_by_id(id)` | `ProjectData \| None` | O(1) dict lookup. Returns `None` for unknown IDs. `@lru_cache`. |

**Example usage in a Flask route**

```python
from config.data_access import get_all_projects, get_project_by_id

@app.route('/projects/')
def projects():
    return render_template('projects.html', projects=get_all_projects())
```

---

## Design constraints

- **No Flask imports.** This package must be importable before `app.py` runs so `freeze.py` can use it at build time without an application context.
- **Immutable public API.** `PROJECTS_SORTED` and `get_all_projects()` both return tuples. Never expose the internal `_PROJECTS` list to callers.
- **Validation at construction.** Bad status values raise `ValueError` immediately when a `ProjectData` is instantiated — not silently at render time.
- **Python 3.9+.** Uses PEP 585 built-in generic type hints (`tuple[...]`, `list[...]`, `Optional[...]`).

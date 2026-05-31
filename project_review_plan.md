SECTION A — Build Pipeline & CI
  Purpose: Deployment backbone. freeze.py compiles the live Flask app into flat static files.
           deploy.yml runs freeze.py on every push to main and ships docs/ to GitHub Pages.
  Key Files: app.py (L34-37), freeze.py, .github/workflows/deploy.yml

  A1. FREEZER_DESTINATION / FREEZER_RELATIVE_URLS (app.py L34-35)
    [x] A1a. FREEZER_DESTINATION passes an absolute path via os.path.join(app.root_path, 'docs').
             pathlib join discards the left side when the right is absolute — works by accident.
             Idiomatic value is the relative string 'docs'. Flag for cleanup.
    [x] A1b. FREEZER_RELATIVE_URLS=True is correct for GitHub Pages. Confirm still needed with
             apex custom domain justinlyons.dev (harmless but technically redundant).
    [x] A1c. FREEZER_REMOVE_EXTRA_FILES is never set — defaults to True. Any file manually placed
             in docs/ (including a local CNAME) will be silently deleted on the next local
             python freeze.py run. Fix: add FREEZER_DESTINATION_IGNORE = ['CNAME'] in app.py.

  A2. deploy.yml CNAME step ordering
    [x] A2a. CI step order is correct: freeze → inject CNAME → upload artifact → deploy.
             No bug, but the ordering has no explanatory comment — add one to prevent
             a future contributor from reordering steps.
    [x] A2b. CNAME value 'justinlyons.dev' is hardcoded in a shell echo command. Not tracked
             in version control. Better: keep a CNAME file in the repo root and cp it into docs/.
    [x] A2c. if: github.ref == 'refs/heads/main' gates deploy only, not the build. PRs run
             freeze.py for validation but do not deploy. Confirm this is intentional.
    [x] A2d. No on: workflow_dispatch trigger. No way to manually re-deploy without a commit.
             Low priority ops gap.

  A3. Dynamic route / @freezer.register_generator audit
    [x] A3a. All registered routes are currently parameter-free — verified. _warn_about_dynamic_routes()
             will log "No parameterized dynamic routes found." No generator needed today.
    [x] A3b. GSA Checklist blueprint defines its full path in the @route decorator
             ('/projects/gsa-mas-checklist/') instead of using url_prefix= on Blueprint().
             If blueprint registration ever applies a prefix, it will double-prefix. Latent bug.
             schedule_maker uses url_prefix correctly — GSA Checklist should match that pattern.
    [x] A3c. freeze.py imports freezer directly from app ('from app import freezer'). All freezer
             config lives in app.py. Any future @freezer.register_generator should go in freeze.py
             (as its docstring implies) to maintain build-time vs. runtime separation.
    [x] A3d. freeze.py uses sys.path.insert(0, BASE_DIR) as a path anchor. Verify this is necessary
             — 'app' should be importable when run from the project root. Defensive but fragile
             if the script is ever invoked from a different working directory.

SECTION B — Flask Core & Routing
  Purpose: Runtime skeleton of the site. app.py wires Blueprints, routes, and template filters.
           base.html is the single shared layout inherited by every page. Scripts and CDN assets
           loaded here execute on every route — highest-impact blast radius for bugs.
  Key Files: app.py, templates/base.html, static/global-theme.js,
             static/js/theme-manager.js, static/script.js

  B1. Blueprint auto-discovery (app.py L42-62)
    [x] B1a. pkgutil.iter_modules detects gsa_mas_checklist.py (flat module) and schedule_maker/
             (package). projects/gsa_mas_checklist/ data directory has no __init__.py — not
             iterated. No collision today, but verify this remains true as the project grows.
    [x] B1b. dir(module) iterates all attributes including Blueprint class itself when imported
             into module namespace. isinstance(Blueprint_class, Blueprint) correctly returns False
             (class is instance of type, not of itself). No false-positive registration.
    [x] B1c. Import failures are silently swallowed: except Exception → logger.warning → continue.
             A broken blueprint (syntax error, bad import) produces only a WARNING and drops the
             route entirely. freeze.py succeeds, CI passes, but the route is missing from docs/.
             Silent deployment failure. Fix: log at ERROR level; add a strict mode that re-raises.
    [x] B1d. register_project_blueprints(app) is called at module scope during import (line 63),
             before core routes are defined. Confirm no blueprint references a core app route
             during registration (would fail with BuildError at import time).

  B2. Core route context variables (app.py L100-148)
    [x] B2a. '/' passes no context to index.html. Confirm all project highlights/profile card
             content is hardcoded or client-rendered. If project cards render server-side,
             the route should pass get_featured_projects().
    [x] B2b. '/projects/' passes projects=get_all_projects() (returns tuple[ProjectData, ...]).
             Tuples are iterable in Jinja2 — fine. Confirm projects.html accesses only fields
             that exist on ProjectData and does not call .to_dict() unnecessarily.
    [x] B2c. '/widget-demo/' passes no context. Confirm widget_demo.html requires none
             (all GridStack state is client-managed via localStorage).
    [x] B2d. nl2br filter is registered globally but only needed by GSA Checklist template.
             Verify it is actually used in a template; if not, remove to reduce surface area.

  B3. base.html <head> — CDN & security
    [x] B3a. All three CDN links (Bootstrap CSS, Bootstrap Icons, GridStack CSS/JS) have NO
             integrity= SRI hashes and no crossorigin="anonymous". A compromised cdn.jsdelivr.net
             can inject arbitrary CSS/JS on every page. Add SRI hashes for all four CDN resources.
    [x] B3b. GridStack JS (gridstack-all.js) is loaded in base.html on EVERY page. Only needed
             on /widget-demo/. Heavy library loaded on homepage, projects page, and all blueprint
             routes unnecessarily. Move script tag to {% block scripts %} in widget_demo.html only.
    [x] B3c. GridStack CSS (gridstack.min.css) is loaded globally in <head> on every page. Same
             issue as B3b. Move to {% block head %} in widget_demo.html.
    [ ] B3d. checklist.css is loaded in base.html on every page, not just the GSA Checklist route.
             Evaluate moving to {% block head %} in the checklist template.
    [x] B3e. <html data-bs-theme="light"> hardcodes light mode. FOUC script sets data-theme only,
             never data-bs-theme. Bootstrap 5.3 dark mode is keyed exclusively on data-bs-theme,
             so Bootstrap always renders light on initial parse regardless of saved preference.
             Fix: FOUC script must also set document.documentElement.setAttribute('data-bs-theme', theme).
    [x] B3f. Stray </div> after </main> (~line 113) has no matching opening tag in the base
             template. Verify it is not closing a block injected by a child template; if not, remove.
    [x] B3g. Navbar toggler <button> is missing aria-expanded="false", aria-controls="navbarNav",
             and aria-label="Toggle navigation" — required per Bootstrap a11y docs and WCAG 2.1.

  B4. Theme system — three-way key/attribute conflict
    Three independent actors operate on the same DOM element with different keys and attributes:
      FOUC script (head):   key='jpl_dev_global_theme'  writes data-theme only       (sync, pre-parse)
      theme-manager.js:     key='jpl-dev-theme'         reads/writes data-bs-theme   (DOMContentLoaded)
      global-theme.js:      key='jpl_dev_global_theme'  reads/writes data-theme only (DOMContentLoaded)

    [x] B4a. On fresh session: ThemeManager defaults to 'light', sets data-bs-theme=light +
             data-theme=light. global-theme.js then reads jpl_dev_global_theme or system pref
             (may be 'dark') and sets data-theme=dark. Result: Bootstrap=light, custom CSS=dark.
             Permanently broken split-theme state on first visit.
    [x] B4b. Both theme-manager.js and global-theme.js attach independent click listeners to
             #theme-toggle. On click, ThemeManager inverts data-bs-theme; global-theme.js inverts
             data-theme (just set by ThemeManager). The two writes race and partially cancel.
             Theme toggle is effectively broken in most scenarios.
    [x] B4c. theme-manager.js is entirely redundant — global-theme.js covers all the same
             responsibilities with the correct storage key. Resolution: delete theme-manager.js,
             update global-theme.js to also write data-bs-theme on every theme set, update the
             FOUC script to also set data-bs-theme, and standardize on key='jpl_dev_global_theme'
             everywhere.

SECTION C — Data Layer
  Purpose: Build-time portfolio catalog. config/projects.py is the single source of truth.
           config/models.py defines the schema. config/data_access.py provides a cached query
           interface. The entire layer must be importable with zero side effects for freeze.py.
  Key Files: config/models.py, config/projects.py, config/data_access.py, requirements.txt

  C1. models.py — schema & type safety
    [x] C1a. ProjectStatus and ProjectCategory are plain classes with string attrs, not enum.Enum.
             Typos in status/category values (e.g., status="actve") produce no error at definition,
             import, or freeze time. Convert to class ProjectStatus(str, Enum) for free validation.
    [x] C1b. ProjectData.status: str carries no validation. Misspelled status silently excludes a
             project from all filtered queries (data_access.py compares against ProjectStatus
             constants). __post_init__ does not validate status against known constants.
    [ ] C1c. primary_link property returns f"route:{self.route}" — a raw prefixed string, not a URL.
             Templates receiving this must manually split on "route:" and call url_for(). Leaky
             abstraction. Rename to primary_endpoint or resolve inside the property with app context.
    [x] C1d. to_dict() calls asdict(self) (converts all nested dataclasses to plain dicts, so
             data['images'] is List[dict]) then overwrites hero_image and thumbnail_image with
             raw ProjectImage dataclass objects. Returned dict is a hybrid type — images is
             List[dict] but hero_image is ProjectImage. Fix: use asdict(self.hero_image) or
             avoid asdict() entirely.
    [ ] C1e. links: Optional[ProjectLinks] = None but primary_link accesses self.links.live_site
             without a None guard. Safe only because __post_init__ normalizes links to ProjectLinks().
             Type annotation contradicts the enforced invariant. Change to:
             links: ProjectLinks = field(default_factory=ProjectLinks).

  C2. data_access.py — lru_cache correctness & dead code
    [ ] C2a. _PROJECTS_BY_ID is a module-level dict (correct for static data). get_project_by_id
             is @lru_cache wrapping an O(1) dict lookup — the cache adds overhead for no gain.
             Remove @lru_cache from this function, or internalize the dict inside the function.
    [x] C2b. get_active_projects(), get_featured_projects(), get_projects_by_category(),
             get_projects_by_tech(), get_projects_by_tag(), get_project_stats(),
             get_all_technologies(), get_all_tags() — all 8 are defined but NEVER CALLED anywhere
             in the codebase. Only get_all_projects() is imported (app.py). Dead code — wire into
             templates/routes or remove entirely.
    [x] C2c. get_active_projects() and get_featured_projects() return mutable List[ProjectData].
             lru_cache stores and returns the SAME list object on every call. A caller mutating
             the returned list permanently corrupts the cached result. get_all_projects() correctly
             returns tuple. Fix: change all list-returning cached functions to return tuple.
    [ ] C2d. get_featured_projects() uses dual criteria: status==FEATURED OR priority>=8. Both
             current projects qualify by priority alone (10 and 8) regardless of status. The
             schedule_maker (status=DEVELOPMENT) appears as "featured". Verify this is intentional
             or add an explicit is_featured: bool field to ProjectData.
    [ ] C2e. tuple[ProjectData, ...] syntax (lowercase tuple) requires Python 3.9+. CI uses 3.11
             — safe today. Document minimum Python version in README or pyproject.toml to prevent
             a silent regression if the CI image is ever downgraded.

  C3. projects.py — sort key & mutability
    [x] C3a. Sort key: (p.priority, p.last_updated or p.created_date or datetime.min). After
             __post_init__ normalizes dates, datetime.min only triggers if both dates are None.
             No crash risk today, but a project with no dates silently sorts to the bottom with
             no warning. Add a logger.warning in __post_init__ when both dates are absent.
    [x] C3b. PROJECTS_SORTED is a module-level mutable list. Nothing prevents a caller from
             mutating it. Combined with C2c, this allows silent corruption of cached query
             results. Wrap in tuple() at definition site or prefix with underscore (_PROJECTS_SORTED)
             and expose only via data_access.py.
    [x] C3c. Both PROJECTS and PROJECTS_SORTED are exported at module level. Only PROJECTS_SORTED
             should be consumed downstream. Rename PROJECTS to _PROJECTS to remove it from the
             public namespace after sorting.

  C4. requirements.txt — orphaned dependencies
    [x] C4a. pandas==2.3.1, openpyxl==3.1.5, and PyPDF2==3.0.1 are listed in requirements.txt
             but NO Python source file in the project imports any of them (confirmed by full
             codebase search). GSA Checklist README mentions "Excel Export: openpyxl" but actual
             export is client-side JavaScript. These add ~25MB+ to the CI install step for zero
             functional benefit and unnecessarily expand the dependency attack surface. Remove all three.

SECTION D — Blueprint: GSA MAS Checklist
  Purpose: Heaviest application in the portfolio. Server-rendered checklist from checklist_data.json,
           enriched with server-side provision text. Client-side SINs browser (JSON fetch), Quill
           per-item notes, and full localStorage state persistence. Primary showcase project.
  Key Files: projects/gsa_mas_checklist.py, templates/projects/gsa_mas_checklist.html,
             static/projects/gsa_mas_checklist.js,
             static/projects/gsa_mas_checklist/data/checklist_data.json,
             static/projects/gsa_mas_checklist/data/sins_data.json

  D1. Blueprint structure & registration inconsistency
    [x] D1a. Blueprint registered with no url_prefix — route '/projects/gsa-mas-checklist/' is
             hardcoded in @route decorator. Same latent double-prefix bug as A3b. Refactor to
             url_prefix='/projects/gsa-mas-checklist', template_folder='templates', @bp.route('/').
    [x] D1b. Blueprint is a single flat .py file containing data, helpers, AND route handlers.
             140-line PROVISION_TEXT_MAP coexists with route logic. Evaluate converting to a package
             (gsa_mas_checklist/__init__.py, routes.py, data.py) matching schedule_maker/ pattern.

  D2. PROVISION_TEXT_MAP — hardcoded legal text
    [x] D2a. PROVISION_TEXT_MAP is a 37-entry dict of multi-line legal text (~300 lines) embedded
             inline in Python source. Legal text changes require Python edits and a redeploy. Fix:
             externalize to static/projects/gsa_mas_checklist/data/provision_text.json and load via
             @lru_cache + current_app.root_path + encoding='utf-8'.
    [ ] D2b. get_provision_text() strips "Provision SCP-FSS-001" and .strip() to produce a lookup
             key. checklist_data.json references are inconsistently formatted — some have a space
             before the paragraph ref, some do not. The strip produces different keys depending on
             the data entry. Lookup silently falls through to the error fallback. Normalize JSON.
    [ ] D2c. create_pdf_link() accepts a pdf_filename parameter but only 'SCP-FSS-001.pdf' is ever
             passed. The parameter is dead generalization. Simplify the function signature.

  D3. Server-side file I/O & helper patterns
    [ ] D3a. @lru_cache(maxsize=1) on load_checklist_data() — current_app.root_path anchor used
             correctly, encoding='utf-8' is explicit. HOWEVER: json.load(f) returns a mutable list.
             Cached object is the same instance on every call. Route handler iterates but does not
             mutate today — safe but fragile. Fix: return tuple(json.load(f)) to enforce immutability.
    [x] D3b. create_pdf_link() calls url_for('static', ...) inside the function body and is called
             once per checklist item per page render via Jinja2. url_for is invoked O(n_items) times.
             All calls produce the same PDF URL. Memoize or pre-compute the URL once per request.
    [ ] D3c. Template calls create_pdf_link() TWICE per item (card footer + modal) with identical
             arguments. Extract to a single {% set ref_data = create_pdf_link(...) %} at the top of
             the {% for item %} loop and reuse the variable in both locations.
    [ ] D3d. ref_data.content | nl2br | safe renders provision text without HTML escaping. Currently
             safe (plain legal text). If PROVISION_TEXT_MAP is ever externalized and a data entry
             introduces HTML tags, this is an XSS vector. Sanitize content on load or remove | safe.

  D4. gsa_mas_checklist.js — client state management
    [ ] D4a. STORAGE_KEY = 'gsa_mas_checklist_data' is well-isolated. Schema: { formData: {},
             checkboxes: {}, notes: {} }. No key collision with global theme or other projects.
    [x] D4b. importData() accepts any valid JSON and writes to localStorage without schema
             validation. Missing keys (checkboxes, notes) silently skip restoration on reload. Add
             schema validation before writing: verify top-level keys exist and have correct types.
    [x] D4c. URL.revokeObjectURL(url) is called synchronously immediately after link.click() in
             exportData(). Can race download initiation on some browsers → broken download file.
             Fix: revoke inside setTimeout(() => URL.revokeObjectURL(url), 100).
    [ ] D4d. Notes stored as Quill Delta objects ({ ops: [...] }). No version stamp on the
             localStorage schema. If Quill is upgraded and the Delta format changes, all saved notes
             are silently unreadable with no migration path. Add { version: 1, ... } to the schema.
    [x] D4e. loadSinsData() fetches from hardcoded absolute path '/static/projects/gsa_mas_checklist/
             data/sins_data.json'. Not generated via Jinja2/url_for. If the static path prefix
             changes (e.g., subdirectory deployment), this silently 404s. Fix: inject the URL as a
             data- attribute on the SINs modal element from the template using url_for().
    [x] D4f. renderSinsList() builds sinItem.innerHTML via template literal that directly interpolates
             sinNumber, sinTitle, sinDescription, etc. from JSON without sanitization. Developer-
             controlled data today — but an XSS vector if the source is ever replaced with external
             data. Escape all interpolated values via textContent assignments.
    [ ] D4g. Quill 2.0.3 loaded from CDN in {% block head %} with no SRI integrity hash. Same
             finding as B3a scoped to this template. Add integrity= attribute.

  D5. JSON data files — schema & data quality
    [ ] D5a. checklist_data.json field names ('Section', 'LINE Number', 'Required Documentation',
             etc.) are consumed by bare string literals in Python, Jinja2, and JS. No schema
             contract enforced — a key rename silently produces None or UndefinedError in template.
             Define a dataclass or JSON schema and validate at load_checklist_data() time.
    [x] D5b. sins_data.json has a persistent field name TYPO: "SIN Descripion" (missing 't').
             JS guards: sin['SIN Descripion'] || sin['SIN Description']. Typo is present in
             hundreds of records. Fix the source data and remove the defensive double-key lookup.
    [x] D5c. sins_data.json has a TRAILING SPACE field name: "Large Category Code " (space at end).
             JS guards: sin['Large Category Code '] || sin['Large Category Code']. Fix source data.
    [ ] D5d. sins_data.json is fully fetched and all items DOM-rendered on SINs modal open. No
             pagination or virtual scrolling. Verify total file size and item count — if the file
             grows, full fetch + DOM render will cause noticeable jank.

SECTION E — Blueprint: Schedule Maker
  Purpose: Employee shift scheduling tool. Weekly/monthly drag-and-drop schedule grid, employee
           roster management, shift editing. All state is volatile in-memory global variables —
           no persistence is implemented despite routes.py docstring claiming "client-side persistence".
           Blueprint is the CORRECT reference pattern that D1 should follow.
  Key Files: projects/schedule_maker/__init__.py, projects/schedule_maker/routes.py,
             projects/schedule_maker/templates/schedule_maker.html,
             static/projects/schedule_maker/script.js (ACTIVE),
             static/projects/schedule_maker/schedule_maker.js (DEAD — not loaded),
             static/projects/schedule_maker/style.css (ACTIVE),
             static/projects/schedule_maker/schedule_maker.css (DEAD — not loaded)

  E1. Blueprint registration (reference implementation)
    [ ] E1a. __init__.py correctly uses url_prefix='/projects/schedule-maker' and
             template_folder='templates'. routes.py uses @bp.route('/'). No bugs — document
             this as the correct pattern for D1a to follow when refactoring GSA Checklist.
    [ ] E1b. routes.py passes zero context to render_template. All data hardcoded in script.js.
             Correct for current state; document for when project metadata is ever displayed.

  E2. Two-file JS: dead prototype vs. active app
    [x] E2a. schedule_maker.js (~600 lines) implements a completely different application — a
             personal calendar (class ScheduleMaker) with timed events. It is NEVER LOADED by
             the template. The template loads only script.js. schedule_maker.js is dead code.
             Remove or archive it; its presence creates confusion about which file is canonical.
    [x] E2b. schedule_maker.css is the companion CSS to schedule_maker.js. Template loads
             style.css, not schedule_maker.css. Also dead code. Remove alongside schedule_maker.js.
    [ ] E2c. Template contains a 'force initialization' block (window.addEventListener('load', ...))
             checking for global functions renderSchedule, renderAvailableEmployees, updateDateDisplay.
             These are already called by script.js's DOMContentLoaded listener. Force-init block
             is redundant and causes double-render. Remove it.

  E3. Save / Export / Import buttons are dead
    [x] E3a. Header renders #save-schedule-btn, #export-schedule-btn, #import-schedule-btn, and
             #new-schedule-btn. Event listeners for these are only in schedule_maker.js (via
             this.setupEventListeners()) — which is NOT LOADED. script.js never attaches handlers
             to these buttons. All four buttons are non-functional. Either implement save/export/
             import in script.js or remove the buttons from the template header.
    [x] E3b. There is NO localStorage save or load anywhere in script.js. All state (employees,
             allSchedules, shiftInfo) lives in module-level let/const variables. Page refresh
             discards all user edits. The routes.py docstring says "client-side persistence" —
             this is documented intent that is not implemented. This is the core incomplete feature.
    [ ] E3c. #import-schedule-file (<input type="file">) is rendered in the header but its
             'change' listener is also only in schedule_maker.js. File import is non-functional.

  E4. Hardcoded seed data — always present, never cleared
    [x] E4a. employees object contains 10 hardcoded fake employees with phone/email rendered in
             DOM on every page load. No empty/first-run state. Intentional for DEVELOPMENT status —
             but document this explicitly so seed data is not confused with production data.
    [x] E4b. weekStartDate = new Date('2025-07-07T12:00:00Z') — past hardcoded date. allSchedules
             pre-populated through August 2025. Combined with E3b, every fresh page load resets
             to this demo state; no user edits ever survive a refresh.
    [ ] E4c. addEmployee() generates IDs via Math.max(...Object.keys(employees).map(Number)) + 1.
             ID arithmetic is correct. However, employees is keyed with string keys but values
             are accessed via parseInt(employeeId) in some paths and raw string in others (notably
             removeEmployee uses delete employees[employeeId] with raw string vs parseInt for
             allSchedules filtering). Verify no off-by-one or key-type mismatch exists.

  E5. Tailwind CDN — wrong build for production
    [x] E5a. <script src="https://cdn.tailwindcss.com"> loads the Tailwind Play CDN — a runtime
             build that scans the DOM and generates CSS on the fly. Tailwind explicitly marks this
             as NOT FOR PRODUCTION. Bundles the full PostCSS compiler (~3MB uncompressed) on every
             page load. For a static site, use the Tailwind CLI at build time to generate a purged,
             minified CSS file. Highest-weight CDN asset in the project.
    [x] E5b. Tailwind CDN <script> tag has no integrity= SRI hash and no version pin. Higher
             severity than other CDN findings (B3a) because a compromised CDN response executes
             arbitrary JavaScript — the Play CDN is a JS runtime, not just a stylesheet.
    [ ] E5c. Google Fonts (Inter) loaded without SRI (not possible for dynamic CSS). Font override
             uses body { font-family: 'Inter' !important; } — sledgehammer specificity acceptable
             for project isolation, but document rationale.

  E6. Tailwind + Bootstrap CSS framework collision
    [x] E6a. base.html loads Bootstrap 5.3.2 (with Reboot reset). This template additionally
             loads Tailwind (with Preflight reset). Both resets apply to the same elements, causing
             unpredictable base styling. The inline <style> block applies !important overrides as
             patches — symptoms of the collision. Long-term fix: eject this blueprint from base.html
             (standalone HTML) OR commit to one framework for the whole project.
    [ ] E6b. Dark mode CSS in {% block head %} uses [data-theme="dark"] selectors. This hooks into
             the broken half of the theme system (B4). Until B4 is fixed, dark mode on this page
             will only partially apply and inconsistently.

  E7. Navigation flyout — broken inline script
    [x] E7a. Template's inline nav wiring script does:
               document.querySelector('.sidenav .closebtn').parentElement...
             There is no .sidenav or .closebtn anywhere in this template or base.html. This selector
             returns null; .parentElement access throws TypeError on every page load. script.js's
             setupModalsAndFlyouts() correctly wires #nav-toggle. Remove the entire inline script block.
    [ ] E7b. setupModalsAndFlyouts() (script.js) attaches listeners to #nav-toggle. Verify this
             element exists in the rendered HTML (possibly from base.html's navbar block). If absent,
             setupModalsAndFlyouts() throws a second TypeError at init and aborts the setup —
             including modal overlay click-to-close wiring.

  E8. closeModal duplicate definition
    [ ] E8a. closeModal() is defined in script.js AND identically defined in an inline <script>
             block in {% block content %}. Inline version parsed last, shadows script.js version.
             Both are identical. Remove inline definition; rely on script.js global. Inline handlers
             (onclick="closeModal()") require a global function — script.js already provides one.

  E9. innerHTML interpolation in popover — XSS
    [x] E9a. showEmployeePopover() builds popover content via popover.innerHTML = `...` directly
             interpolating employee.name, .phone, .email, .notes without sanitization. Employee
             data comes from user input (addEmployee() reads form values). A crafted name value
             (e.g., <script>alert(1)</script>) triggers stored XSS on next hover. Fix: use
             textContent assignments for all interpolated values. Same class of issue as D4f.

SECTION F — Client-Side Core (JS)
  Purpose: Five JS files loaded globally on every page via base.html. Together they own the theme
           system, widget system, smart tooltip system, and legacy sidenav navigation. Load order:
           theme-manager.js → widget-manager.js → widget-utils.js → script.js → global-theme.js.
           Three of five contain bugs affecting every route.
  Key Files: static/js/theme-manager.js (global), static/global-theme.js (global),
             static/js/widget-manager.js (global, activates only on /widget-demo/),
             static/js/widget-utils.js (global, widget-demo only utilities),
             static/script.js (global, tooltips + dead sidenav)

  F1. Theme system: execution order confirms the B4 conflict
    [x] F1a. Load order: theme-manager.js first, global-theme.js last. Both register DOMContentLoaded
             listeners. ThemeManager fires first: reads 'jpl-dev-theme' (null → 'light'), writes
             data-bs-theme=light AND data-theme=light. Then global-theme.js fires: reads
             'jpl_dev_global_theme' (null → system pref), may write data-theme=dark but NEVER
             touches data-bs-theme. Result on every dark-mode fresh visit: Bootstrap=light,
             custom CSS=dark. Split-theme state is structurally guaranteed by load order.
    [x] F1b. ThemeManager uses key 'jpl-dev-theme'; global-theme.js uses 'jpl_dev_global_theme'.
             Two separate preferences in localStorage. On repeat visits each system restores its
             own saved value and overwrites the other's data-theme attribute. The two state machines
             permanently diverge; there is no code path where they can agree.
    [x] F1c. Both ThemeManager.setupThemeToggle() and global-theme.js attach independent click
             listeners to #theme-toggle. On a single click both fire: ThemeManager reads data-bs-theme,
             calls setTheme() (writes both attributes + dispatches themeChange). Then global-theme.js
             reads data-theme (just written by ThemeManager) and inverts it — undoing ThemeManager's
             data-theme write. Bootstrap ends up toggled correctly; custom CSS ends up wrong.
    [x] F1d. Resolution (implements B4c): Delete theme-manager.js. Update global-theme.js:
             (1) add data-bs-theme setAttribute to applyTheme(), (2) dispatch themeChange
             CustomEvent after applying, (3) add system preference mediaQuery listener.
             Update FOUC script in base.html to also set data-bs-theme. Preserve ThemeUtils
             (extract to global-theme.js or standalone file — see F2c).

  F2. themeChange custom event: partial wiring
    [ ] F2a. theme-manager.js dispatches CustomEvent('themeChange') on every setTheme() call.
             widget-manager.js and widget_demo.html listen for this event. Wiring is correct —
             but only when ThemeManager is the actor. Functional today only because ThemeManager
             always fires; the correct actor (global-theme.js) does not fire this event.
    [x] F2b. global-theme.js applyTheme() never dispatches themeChange. When global-theme.js
             handles a toggle click, WidgetManager.updateWidgetStyles() is never called and
             widget_demo.html's themeChange listener never fires. After F1d fix (delete
             theme-manager.js), dispatchThemeChangeEvent() MUST be added to global-theme.js
             or the widget-demo breaks silently on theme toggle.
    [ ] F2c. ThemeUtils (defined in theme-manager.js) provides onThemeChange(cb), offThemeChange(cb),
             isDarkTheme(), getCurrentTheme(), getCSSVariable(), getThemeColor(). Genuinely useful
             utilities. When theme-manager.js is deleted, ThemeUtils must be extracted into
             global-theme.js or a standalone theme-utils.js to preserve downstream consumers.

  F3. script.js: dead sidenav functions + functional tooltip utilities
    [x] F3a. openNav() and closeNav() target #mySidenav and #content-wrapper. These IDs exist only
             in build/projects/index.html — a stale artifact from a previous sidenav layout, not
             present in any current Jinja2 template. Never called by anything in the current
             codebase. Remove both functions from script.js.
    [ ] F3b. initializeSmartTooltips() is the legitimate purpose of script.js. Queries
             .info-icon[data-tooltip], adds tabindex="0" for keyboard a11y, attaches
             mouseenter/focus/mouseleave/blur handlers, debounces resize. No bugs. Keep as-is.
    [ ] F3c. initializeSmartTooltips() early-returns if no .info-icon[data-tooltip] elements are
             found — safe to run on every page. No performance concern.
    [ ] F3d. After removing openNav()/closeNav(), verify no inline onclick= handlers reference
             them. Confirmed: the only reference is build/projects/index.html (orphaned artifact,
             not a template). Removal is safe.

  F4. widget-manager.js: correct container guard, incomplete layout persistence
    [ ] F4a. WidgetManager is only instantiated if #grid-stack-container exists (DOMContentLoaded
             guard). GridStack global reference is inside class methods only — never evaluated at
             parse time. Moving GridStack CDN to widget_demo.html only (B3b fix) is safe and does
             not break widget-manager.js on other pages. Verify this invariant before applying B3b.
    [x] F4b. saveWidgetLayout() correctly serializes GridStack nodes to localStorage key
             'jpl-dev-widget-layout'. loadWidgetLayout() parses the saved JSON but does NOTHING
             with it — the restore block is a comment only. Widget layout saves but never restores.
             The save/load cycle is broken by design. Implement restoration logic or remove
             saveWidgetLayout() to avoid the false appearance of persistence.
    [ ] F4c. generateCalendarWidget() hardcodes "December 2024" as the calendar title. Over a year
             stale. Make dynamic (use new Date()) or remove the calendar widget type until it has
             a real implementation.
    [ ] F4d. WidgetManager listens for themeChange event to call updateWidgetStyles(). After F1d
             fix, this event must still be dispatched by global-theme.js (covered by F2b).

  F5. widget-manager.js / widget-utils.js: innerHTML interpolation — XSS patterns
    [x] F5a. generateProfileWidget(), generateSkillsWidget(), generateSocialWidget(),
             generateProjectsWidget() build HTML via template literals that interpolate config.*
             values directly into innerHTML. config.image → src="..." attribute (onerror injection).
             link.url → href="..." (javascript: XSS). Currently all values come from hardcoded
             defaults — low immediate risk. Pattern must be fixed before any config source
             is external. Use textContent or a sanitize helper for all interpolated values.
    [x] F5b. BootstrapUtils.createModal(id, title, content) and WidgetTemplates.createCard(title,
             content) in widget-utils.js interpolate title and content into innerHTML. These are
             utility functions designed for arbitrary caller input. Any caller passing unsanitized
             user data triggers XSS. Document input sanitization requirement or add a sanitizer.
    [x] F5c. widget-manager.js uses onclick="widgetManager.removeWidget('${id}')" in generated HTML.
             Widget IDs from Date.now() are numeric (safe). IDs from config.id are caller-supplied.
             A config.id containing a single quote breaks the attribute and can inject event handlers.
             Add alphanumeric-only validation for widget IDs before use in HTML attribute context.

  F6. widget-utils.js: dead weight on every page
    [ ] F6a. WidgetTemplates, WidgetAnimations, BootstrapUtils are defined as globals and loaded
             on every page. None are referenced outside widget-demo context. Move widget-utils.js
             to {% block scripts %} in widget_demo.html. Same fix category as B3b/B3c for GridStack.

SECTION G — CSS Architecture
  Purpose: Ten local CSS files loaded globally via base.html (lines 9-26), plus Bootstrap CDN and
           GridStack CDN. Load order: Bootstrap → GridStack → variables → bootstrap-theme → widgets
           → base → layout → components → profile-card → checklist → theme-toggle → projects →
           widget-system. Cascade conflicts, undefined custom properties, and misplaced page-specific
           files produce silent visual breakage on every route.
  Key Files: static/css/variables.css (L16), static/css/bootstrap-theme.css (L17),
             static/css/widgets.css (L18), static/css/base.css (L19), static/css/layout.css (L20),
             static/css/components.css (L21), static/css/profile-card.css (L22),
             static/css/checklist.css (L23), static/css/theme-toggle.css (L24),
             static/css/projects.css (L25), static/css/widget-system.css (L26),
             static/css/enhanced-widgets.css (not linked, empty)

  G1. CSS load order: variables.css is correctly first; two ordering issues remain
    [ ] G1a. variables.css at L16 is the first local file — all subsequent files can resolve
             var(--...) references. Load order is correct here. No bug.
    [ ] G1b. widgets.css (L18) is loaded before base.css (L19). base.css establishes body,
             .container, main — foundations that component files should build on. Swap: base.css
             should precede widgets.css. No functional bug today (no current conflict) but
             violates convention and creates future risk.
    [x] G1c. widget-system.css (L26) and widgets.css (L18) both define .widget and .widget-header
             with different property sets. widget-system.css is loaded last and wins for conflict
             properties. Specifically, widget-system.css adds contain: layout style paint to
             .widget — potentially interfering with widgets.css's display:flex/height:100% layout.
             Two files share the same selector set with no clear ownership. Consolidate: merge the
             two .widget / .widget-header definitions. widget-system.css should be the authority
             for widget-demo; remove duplicates from widgets.css.

  G2. Theme attribute split: CSS files disagree on which attribute drives dark mode
    [x] G2a. variables.css uses [data-theme="dark"] for custom property palette. This pairs with
             global-theme.js (the surviving actor after B4c). bootstrap-theme.css uses
             [data-bs-theme="dark"] for Bootstrap variable overrides (correct for Bootstrap 5.3).
             Until B4c is implemented (FOUC and global-theme.js write BOTH attributes in sync),
             every fresh dark-mode visit produces a mixed-theme render: custom components dark,
             Bootstrap components light (or vice versa).
    [ ] G2b. theme-toggle.css, projects.css, layout.css all use [data-theme="dark"]. Consistent
             with variables.css. No conflict within this group. These files continue to work
             after the B4c fix without change.
    [ ] G2c. After B4c is implemented, document the two-attribute contract in variables.css:
             [data-theme] drives custom property palette; [data-bs-theme] drives Bootstrap
             components. Both are always set in sync. Without this comment, future contributors
             will continue writing only one attribute inconsistently.

  G3. Undefined CSS custom properties: silent transparent/invisible rendering
    [x] G3a. widget-system.css references --accent-color in 14+ declarations: hover borders on
             .edit-mode .widget:hover, focus outlines (.widget:focus, .widget-action-btn:focus),
             drop-zone highlight gradient, resize-handle background, loading spinner. --accent-color
             is NOT defined in variables.css or anywhere else. All 14 declarations resolve to
             transparent/empty. On widget-demo: all widget hover borders, focus rings, drop-zone
             shimmer, and resize handle are invisible. Add --accent-color and dark-mode variant
             to variables.css (e.g., --accent-color: var(--primary-color)).
    [x] G3b. widget-system.css references --accent-color-alpha in drop-zone gradient (3 usages).
             Also not defined. The drop-zone highlight effect is completely invisible.
    [x] G3c. widget-system.css references --text-primary in .widget-header h3, widget-handle
             color, and activity text (3 usages). variables.css defines --text-color and
             --text-secondary but NOT --text-primary. Widget header titles and handle icons
             render with inherited/browser-default color instead of the intended value.
             Map --text-primary: var(--text-color) in variables.css.
    [x] G3d. profile-card.css L511 references --text-primary (1 usage). Same undefined-variable
             issue — homepage is affected. Fix via the same variables.css addition in G3c.
    [x] G3e. theme-toggle.css L75: [data-theme="dark"] .theme-toggle-switch { background:
             var(--bg-primary); }. --bg-primary is NOT defined. variables.css has --bg-color
             and --bg-secondary. In dark mode the toggle switch background is transparent — the
             visual toggle element disappears. Replace var(--bg-primary) with var(--bg-color) in
             theme-toggle.css, or add --bg-primary: var(--bg-color) to variables.css.

  G4. Invalid rgba() syntax in projects.css — invisible borders and icon backgrounds
    [x] G4a. projects.css L54: .project-meta-link { background: rgba(var(--text-color), 0.1); }
             and L77: .project-card-footer { border-top: 1px solid rgba(var(--text-color), 0.1); }
             --text-color is the hex string '#333'. rgba() requires three separate numeric channel
             values. Passing a hex string as the first argument is a CSS parse error — the browser
             ignores the entire declaration. Result: meta-link icon circles have no background;
             project card footer has no separator line. Fix: add --text-color-rgb: 51, 51, 51 to
             variables.css :root (and 224, 224, 224 for dark mode), then use
             rgba(var(--text-color-rgb), 0.1) — matching the existing --primary-color-rgb pattern.

  G5. Undefined spacing/layout variables in projects.css — broken project card layout
    [x] G5a. projects.css references --border-radius (L25), --spacing-md (L26 x4, L76), and
             --spacing-sm (L43, L44, L75). None are defined in variables.css. Affected rules:
             .project-card-image border-radius resolves to 0 (images overflow card corners),
             .project-card-image negative margin calc() resolves to 0 (image not flush to card
             edge), .project-links and .project-card-footer gap and padding collapse to 0.
             The entire enhanced project card image header and meta-links footer section is
             silently broken. Add --border-radius: 0.5rem, --spacing-md: 1rem,
             --spacing-sm: 0.5rem to variables.css, or replace with literal values in projects.css.

  G6. Duplicate selectors across bootstrap-theme.css and components.css
    [ ] G6a. Both files define .card, .btn, .btn:hover, .form-control:focus, .modal-content.
             bootstrap-theme.css uses border-radius: 0.5rem !important on .card (wins regardless
             of order). components.css uses border-radius: 5px — silently overridden by !important.
             The 5px is invisible, creating false intent in the source file. Establish ownership:
             bootstrap-theme.css owns Bootstrap component overrides; components.css owns custom
             non-Bootstrap components. Remove .card and .btn blocks from components.css.
    [ ] G6b. .btn-secondary and .btn-danger are defined in both files. components.css wins by
             cascade order. Remove the duplicate definitions from whichever file is not the
             designated owner (bootstrap-theme.css, since these are Bootstrap classes).

  G7. Dead CSS: .sidenav in layout.css
    [!] G7a. layout.css defines .sidenav, .sidenav a, .sidenav a:hover, .sidenav .closebtn.
             The sidenav element does not exist in any current Jinja2 template — only in
             build/projects/index.html (orphaned artifact). Dead CSS that pairs with the dead
             openNav()/closeNav() functions (F3a). Remove all sidenav rules from layout.css
             in the same commit that removes F3a.

  G8. Page-specific CSS loaded globally on every route
    [ ] G8a. widgets.css (L18) + widget-system.css (L26) — widget-demo page only. Move both to
             {% block head %} in widget_demo.html. Unblocks removal of GridStack CDN CSS (B3c)
             from base.html in the same cleanup.
    [ ] G8b. checklist.css (L23) — GSA Checklist route only. Move to {% block head %} in
             gsa_mas_checklist.html. This is the B3d finding. Verify {% block head %} exists
             in that template before moving.
    [ ] G8c. profile-card.css (L22) — homepage only. Move to {% block head %} in index.html.
    [ ] G8d. projects.css (L25) — /projects/ route only. Move to {% block head %} in projects.html.
    [ ] G8e. After moves: globally-loaded local files reduce to variables.css, bootstrap-theme.css,
             base.css, layout.css, components.css, theme-toggle.css. Confirm this reduced set
             is the correct global baseline.

  G9. enhanced-widgets.css: empty phantom file
    [ ] G9a. static/css/enhanced-widgets.css is completely empty and not linked from any template.
             A placeholder that was never populated. Remove the file — its presence implies
             widget enhancement styles exist somewhere, which they do not.

SECTION H — Templates
  Purpose: Four Jinja2 templates producing all user-facing HTML. base.html (Sections B/F/G) is the
           shared layout. These child templates own page-specific structure, inline scripts, and
           Jinja2 field access patterns. Two contain active JS bugs. One is an unrouted work-in-
           progress. One finding here (H1a) directly revises the B3b fix scope.
  Key Files: templates/index.html (route: /),
             templates/projects.html (route: /projects/),
             templates/widget_demo.html (route: /widget-demo/),
             templates/index_old.html (UNROUTED — no route renders this file)

  H1. index.html: homepage is a GridStack page — B3b fix direction is wrong
    [x] H1a. index.html's {% block scripts %} calls GridStack.init({...}, '#grid-stack-container')
             on DOMContentLoaded. The homepage renders a full GridStack widget dashboard. GridStack
             is therefore needed on BOTH homepage and widget-demo, not widget-demo only. The B3b
             fix ("move GridStack to widget_demo.html only") is incorrect as written — it would
             break the homepage. CORRECT FIX: remove GridStack CDN from base.html and add it to
             {% block head %} in BOTH index.html and widget_demo.html. Update B3b accordingly.
    [x] H1b. Double GridStack initialization on the homepage. widget-manager.js (loaded globally)
             guards on #grid-stack-container and calls GridStack.init() from WidgetManager
             constructor on DOMContentLoaded. The homepage inline script ALSO calls GridStack.init()
             on the same container with different options (cellHeight:120, margin:15). GridStack
             silently returns the existing instance on duplicate-init and ignores the new options.
             The homepage's intentional grid settings are discarded. Unify to one initialization:
             either remove the inline GridStack.init() and configure WidgetManager with the desired
             options, or rename the homepage container to prevent WidgetManager from activating.
    [x] H1c. Hardcoded Facebook CDN profile image URL in two places inside index.html (profile
             widget card ~L64; getWidgetConfig('profile').image ~L355). The URL contains a time-
             limited oe= expiry parameter — the image will silently fail to load when the token
             expires. The same expiring URL also appears twice in index_old.html (H4b) — four
             instances total across two templates, with onerror fallback present on only one.
             Move the image to static/images/ and reference via url_for('static', ...).
    [x] H1d. Project card links in "Featured Projects" and "Recent Projects" widgets use raw href
             strings: href="/projects/schedule-maker/" and href="/projects/gsa-mas-checklist/".
             Not generated via url_for(). If blueprint url_prefix changes (D1a refactor) or the
             site is deployed to a subpath, these silently 404. Replace with url_for() calls.
    [ ] H1e. All project content in homepage widgets is hardcoded in the template and in
             getWidgetConfig(): project names, descriptions, tech stacks, statuses. config/projects.py
             already owns this data authoritatively. The homepage and projects page can silently
             drift when projects are added or updated. Resolve B2a: pass get_featured_projects()
             from the '/' route and render homepage widget content from the data.
    [ ] H1f. window.dashboardGrid = grid — the homepage inline script stores the GridStack instance
             as a global but nothing reads window.dashboardGrid. Dead assignment.
    [x] H1g. addWidget(type) → getWidgetConfig('profile') → config.image = <Facebook CDN URL>.
             This flows into WidgetManager.generateProfileWidget() which interpolates config.image
             into src="${config.image}" via innerHTML — the F5a XSS pattern. Also: when the CDN
             URL expires (H1c), dynamically-added profile widgets will show broken images with no
             fallback. Two compounding bugs at the same call site.
    [ ] H1h. document.querySelector('.card:has(.progress-bar)') uses CSS :has() in a JS selector.
             Supported in Chrome 105+, Safari 15.4+, Firefox 121+. Acceptable for a personal
             portfolio but not universal. Document minimum browser target or use a fallback.

  H2. projects.html: field access patterns on ProjectData
    [ ] H2a. Route correctly passes projects=get_all_projects() (tuple). {% for project in projects %}
             iterates correctly. {% if project.route %} guards url_for(project.route) — no crash
             on None route. {% if project.thumbnail_image %} guards the image block. No bugs in
             field access logic.
    [x] H2b. Status badge color chosen by {% if project.status == 'active' %},
             {% elif project.status == 'development' %} etc. — hardcoded string literals that must
             stay in sync with ProjectStatus.ACTIVE = "active" in models.py. No freeze-time
             validation. If C1a is fixed (convert to enum.Enum) and values are renamed, badge
             colors silently show the wrong state for all projects. Pass ProjectStatus constants
             from the route context, or confirm string values are frozen before implementing C1a.
    [ ] H2c. project.links.github, project.links.documentation, project.links.live_site,
             project.links.demo accessed without a None guard on project.links. Safe today because
             __post_init__ normalizes links to ProjectLinks(). But type annotation is
             Optional[ProjectLinks] = None (C1e) — if C1e is ever fixed and normalization removed,
             this template raises AttributeError. The template relies on an undocumented invariant.
    [ ] H2d. projects.html has no {% block head %} override. Moving projects.css to this template
             (G8d) requires adding one. Verify base.html defines {% block head %} first.

  H3. widget_demo.html: GridStack init, broken toast signature, chart theme dependency
    [x] H3a. drawDemoChart() calls ThemeAwareUtils.getThemeColors() which reads data-bs-theme.
             Until B4c is fixed, data-bs-theme is unreliably set — always resolves to light or null.
             Chart always renders in light-theme colors regardless of user preference. COMPOUNDING:
             the themeChange listener that would redraw the chart never fires because global-theme.js
             doesn't dispatch themeChange (F2b). Two independent bugs lock chart to light colors.
    [x] H3b. showDemoToast() is defined with zero parameters but called with 3 args in two places:
             showDemoToast('Widget Added', ..., 'info') and showDemoToast('Animation Started', ...,
             'info'). All args are silently dropped. Every toast always shows "Widget Demo:
             This is a demonstration toast notification!" in green. Fix signature to
             (title, message, type) and pass through to BootstrapUtils.showToast().
    [ ] H3c. widget_demo.html uses #widget-demo-grid as the GridStack container ID. widget-manager.js
             guards on #grid-stack-container. IDs do not match — WidgetManager is NEVER instantiated
             on widget_demo.html. addRandomWidget() always takes the createDemoWidget() fallback
             path. The if (window.widgetManager) branch is dead code on this page. If unintentional:
             rename #widget-demo-grid to #grid-stack-container. If intentional: remove the dead
             window.widgetManager branch from addRandomWidget().
    [ ] H3d. resetWidgets() calls demoGrid.removeAll() immediately before location.reload().
             The removeAll() is redundant — reload discards all DOM. Remove it, or implement a
             proper in-place reset that avoids the disorienting full page reload.
    [ ] H3e. widget_demo.html has no {% block head %} override. Moving GridStack CSS, widgets.css,
             and widget-system.css to this template (B3c, G8a) requires adding the block.
    [ ] H3f. demoGrid declared with let at block scope but initialized inside DOMContentLoaded.
             removeDemoWidget() references demoGrid — safe via onclick (always post-load), but
             add if (!demoGrid) return guard for correctness.

  H4. index_old.html: unrouted work-in-progress
    [x] H4a. index_old.html still extends base.html — it is a structurally valid Jinja2 template.
             No route in app.py or any blueprint renders it; it is correctly absent from docs/.
             Its presence at the top-level templates/ path implies to any future contributor that
             it is an active template. Confirm it is unrouted, then delete it or move it to
             templates/archive/ with an explanatory comment. Do not leave it at templates/ root.
    [x] H4b. Contains the same expiring Facebook CDN image URL as index.html (×2). All four
             instances across both templates must be replaced in the same commit as H1c.
    [ ] H4c. References .sidebar-drop-zone class not defined in any CSS file. Confirms the file
             was abandoned mid-development. Moot if archived; must be authored if ever revived.

SECTION I — Static Output Drift
  Purpose: Two output directories co-exist: docs/ is the current Flask-Frozen production output
           deployed to GitHub Pages. build/ is a completely separate artifact from a pre-Flask
           version of the site. This section verifies docs/ currency against static/, identifies
           phantom empty directories from stale freeze runs, and clarifies the build/ risk.
  Key Files: docs/ (freeze output, deployed), docs/CNAME (CI-injected),
             docs/static/ (mirrors static/), build/ (pre-rewrite orphan, NOT a freeze output),
             deployment/ (empty)

  I1. build/ is a pre-rewrite orphan — NOT a freeze output
    [x] I1a. build/index.html contains bare HTML — <title>My Portfolio</title>,
             <h1>Welcome to my portfolio!</h1> — no Bootstrap, no Flask templating, no CSS
             framework. This predates the entire Flask/Bootstrap architecture. Flask-Frozen has
             never written to build/; it writes only to docs/ per FREEZER_DESTINATION.
    [x] I1b. build/projects/index.html is the CONFIRMED ORIGIN of multiple dead-code findings:
             it contains <div id="mySidenav" class="sidenav">, onclick="closeNav()",
             onclick="openNav()", href="/static/style.css". The dead sidenav functions in
             static/script.js (F3a) and the .sidenav CSS rules in layout.css (G7a) exist
             solely to support this file — which has never been rendered by the current Flask
             app. Deleting build/ closes the F3a and G7a ambiguity simultaneously and makes
             both removals unambiguously safe.
    [x] I1c. build/static/ contains only style.css and script.js — old flat files from the
             pre-rewrite layout. No css/, no js/, no projects/. Confirms build/ was written
             by hand, not generated by Flask-Frozen.
    [x] I1d. build/ sitting alongside docs/ in the repo creates a persistent readability hazard.
             A future contributor cannot immediately tell which directory is the production output.
             There is no README or comment explaining build/'s origin. Delete build/ entirely and
             document the docs/ role in the top-level README (Section J).

  I2. docs/ structure: correct routes, two phantom empty directories
    [ ] I2a. docs/ contains the correct set of freeze-generated routes:
             docs/index.html (/), docs/projects/index.html (/projects/),
             docs/widget-demo/index.html (/widget-demo/),
             docs/projects/gsa-mas-checklist/index.html, docs/projects/schedule-maker/index.html,
             docs/CNAME (CI-injected). All five production routes present. No missing routes.
    [x] I2b. docs/static/data/ is an EMPTY DIRECTORY with no counterpart in static/. static/data/
             does not exist. Created during a previous freeze run when static/data/ existed, then
             the source was deleted. FREEZER_REMOVE_EXTRA_FILES=True removes extra FILES but does
             NOT remove empty DIRECTORIES — the orphan persists across all subsequent freeze runs.
             No content impact today, but it pollutes the docs/static/ structure. Remove manually.
    [x] I2c. docs/projects/projects/ is an EMPTY DIRECTORY with no corresponding route. No
             Blueprint or core route generates /projects/projects/. Likely from a previous layout
             where the projects blueprint had a different URL prefix. Same root cause as I2b —
             empty directories are never cleaned by FREEZER_REMOVE_EXTRA_FILES. Remove manually.
    [ ] I2d. I2b and I2c are symptoms of the same Flask-Frozen limitation: FREEZER_REMOVE_EXTRA_FILES
             does not clean up empty directories after source directories are deleted. Document
             this limitation and consider a post-freeze cleanup step in freeze.py or deploy.yml
             that runs something like: find docs/ -type d -empty -delete.

  I3. docs/static/ mirrors static/ correctly for all file content
    [ ] I3a. docs/static/css/ contains all 12 files matching static/css/ exactly — including
             enhanced-widgets.css (the empty phantom from G9a). No additions or missing files.
    [ ] I3b. docs/static/js/ matches static/js/ exactly: theme-manager.js, widget-manager.js,
             widget-utils.js. docs/static/ top-level matches static/ top-level: global-theme.js,
             script.js, style.css. Full mirror is current.
    [ ] I3c. docs/static/projects/schedule_maker/ contains all four files including the two dead
             ones: schedule_maker.css and schedule_maker.js (E2a/E2b). Flask-Frozen copies all
             static files unconditionally regardless of whether they are referenced. Dead static
             files ship to production. Removing E2a/E2b from static/ is sufficient; the next
             freeze run drops them from docs/ automatically via FREEZER_REMOVE_EXTRA_FILES.
    [ ] I3d. docs/index.html contains the full Bootstrap/GridStack/widget-dashboard structure
             matching the current templates/index.html. Blueprint output pages are present and
             current. The freeze output appears current with the source templates.

  I4. docs/CNAME currency and the A1c local-freeze risk
    [ ] I4a. docs/CNAME contains 'justinlyons.dev' — correct. Injected by CI echo step (A2a/A2b)
             after the last successful deploy. Its presence confirms CI ran at least once after
             the current site was frozen.
    [x] I4b. Confirmed re: A1c: running python freeze.py locally RIGHT NOW deletes docs/CNAME
             because FREEZER_REMOVE_EXTRA_FILES=True and CNAME is not a Flask-generated route.
             A developer running a local freeze to preview changes silently destroys the custom
             domain file. The next git push deploys without CNAME, breaking justinlyons.dev
             until CI re-injects it on the following commit. This is a live operational risk.
             Fix: add FREEZER_DESTINATION_IGNORE = ['CNAME'] to app.py (implements A1c), or
             keep a CNAME file in the repo root and cp it in both freeze.py and deploy.yml.

  I5. Currency: docs/ reflects last CI run, not current source
    [ ] I5a. docs/ reflects the state of templates and static files at the time of the last
             freeze.py run (last push to main). Any source change since that deploy is not in
             docs/ until the next push triggers CI. For every fix implemented in this review,
             run python freeze.py locally and verify the docs/ diff before pushing to confirm
             the freeze output matches expectations.
    [ ] I5b. docs/ HTML files use relative static asset paths (href="static/css/variables.css")
             because FREEZER_RELATIVE_URLS=True. Verify subdirectory pages (docs/projects/index.html,
             docs/projects/gsa-mas-checklist/index.html) correctly resolve ../static/... paths
             when served from GitHub Pages. The FREEZER_RELATIVE_URLS=True setting is responsible
             for generating these — confirm they render correctly in the live site.

SECTION J — Dead Code & Hygiene
  Purpose: Tracked files, directories, and documentation that are unused, inaccurate, or
           misleading. Most findings here are low-effort deletions and README corrections — but
           the inaccurate READMEs directly mislead any contributor about which JS files are active
           and which framework features are implemented.
  Key Files: .gitignore, static/style.css, deployment/ (empty), build/ (pre-rewrite orphan),
             README.md, projects/README.md, projects/gsa_mas_checklist/README.md,
             projects/schedule_maker/README.md

  J1. deployment/ — empty tracked directory with no purpose
    [x] J1a. deployment/ is completely empty. It has no .gitignore entry, no README, no content,
             and is not referenced from app.py, freeze.py, deploy.yml, or any other file.
             Delete the directory. Add deployment/ to .gitignore to prevent accidental re-creation.

  J2. build/ — tracked pre-rewrite orphan not in .gitignore
    [x] J2a. build/ is committed and fully tracked in git. .gitignore contains 'docs/_build/'
             (a Sphinx convention) but NOT 'build/' — the project's own old-site directory is
             intentionally or accidentally tracked. It should be deleted (per I1d) AND added to
             .gitignore. Without the .gitignore entry, deleting the directory does not prevent
             a future `git checkout .` or branch switch from resurrecting it.
    [x] J2b. .gitignore currently has ZERO project-specific entries — only boilerplate from the
             standard Python .gitignore template. Add at minimum: build/, deployment/, and verify
             .venv/ is covered (it is: venv/ matches .venv/ only if using the venv/ name;
             .venv/ is NOT in .gitignore). Add .venv/ explicitly.

  J3. static/style.css — pre-rewrite monolithic stylesheet shipped to production unused
    [x] J3a. static/style.css is a complete CSS custom-property palette + dark theme block —
             the pre-modular predecessor to the current static/css/variables.css system. It is
             NOT loaded by base.html or any current Jinja2 template. The ONLY file referencing it
             is build/projects/index.html (the pre-rewrite orphan, I1b). It ships to production
             as docs/static/style.css (confirmed in freeze mirror, I3b) but is loaded by zero
             live pages. Delete it from static/. The next freeze run drops docs/static/style.css
             automatically via FREEZER_REMOVE_EXTRA_FILES.
    [ ] J3b. After deleting static/style.css and build/ in the same commit, confirm that
             docs/static/style.css is removed on the next freeze run. If FREEZER_REMOVE_EXTRA_FILES
             is already True (the default), the file is automatically cleaned. Verify after freeze.

  J4. .gitignore — __pycache__ covered; .venv/ and project-specific entries missing
    [ ] J4a. __pycache__/ is correctly in .gitignore (line 2). *.py[cod], .env, venv/,
             .pytest_cache/, instance/ — all covered by the boilerplate template. No gaps for
             standard Python artifacts.
    [x] J4b. .venv/ is NOT in .gitignore. The boilerplate covers 'venv/' but the project likely
             uses '.venv/' (the VSCode default for Python environments). If '.venv/' exists and
             is not ignored, it can be accidentally staged. Add '.venv/' explicitly.
    [x] J4c. build/, deployment/ are not in .gitignore (see J2a/J1a). After deleting both
             directories, add entries to prevent re-creation being accidentally tracked.

  J5. projects/README.md — missing schedule_maker; wrong Blueprint registration guidance
    [x] J5a. The Project Structure diagram in projects/README.md only shows gsa_mas_checklist/
             as a project. schedule_maker/ (a full Blueprint package with __init__.py, routes.py,
             templates/, and four static files) is absent from the diagram entirely. Any contributor
             following this README to understand the project layout gets an incomplete and
             misleading picture of the codebase.
    [x] J5b. The "Adding New Projects / Register in Main App" section instructs developers to
             manually call app.register_blueprint(new_project_bp) in app.py. THIS IS WRONG — and
             dangerous. The actual mechanism is Blueprint auto-discovery via pkgutil.iter_modules
             in register_project_blueprints() (app.py). Following the README guidance causes
             DOUBLE REGISTRATION: auto-discovery finds the new blueprint AND the manual call
             registers it again, silently discarding the first registration. Fix: remove the
             manual registration step from the README and describe the auto-discovery mechanism
             (create the package → Flask-Frozen picks it up automatically on next run).

  J6. projects/gsa_mas_checklist/README.md — false feature and dependency claims
    [x] J6a. "Excel Export: openpyxl library for spreadsheet generation" — FALSE. Export is
             client-side JSON download only (exportData() in gsa_mas_checklist.js). No openpyxl
             import exists anywhere in the codebase (see C4a). This claim is the direct reason
             openpyxl==3.1.5 was added to requirements.txt and is never used.
    [x] J6b. "Auto-save: Periodic automatic saving to prevent data loss" — NOT IMPLEMENTED.
             gsa_mas_checklist.js has no setInterval() auto-save timer anywhere. Save occurs only
             on explicit user action (checkboxes, notes via Quill 'text-change' event). The
             feature is described as working when it does not exist.
    [x] J6c. "Python 3.8+" badge on the README header. FALSE: the codebase uses lowercase
             tuple[ProjectData, ...] type hints (PEP 585, Python 3.9+). Running on 3.8 raises
             TypeError at import. The correct minimum is Python 3.9. Update badge and note in
             top-level README.
    [ ] J6d. "WCAG compliant with keyboard navigation support" — an unverified blanket claim.
             Not tested or audited. Downgrade to "keyboard navigation support" or remove the
             WCAG compliance claim until an audit is performed.
    [ ] J6e. README badge links to status shield [![Status: Active]] — accurate given the
             current ProjectStatus. No action needed unless J6a/J6b corrections change the
             feature set description.

  J7. projects/schedule_maker/README.md — documents the dead prototype, not the active codebase
    [x] J7a. Project Structure section:
               static/projects/schedule_maker/
               ├── schedule_maker.css     ← DEAD (E2b — not loaded by template)
               └── schedule_maker.js     ← DEAD (E2a — not loaded by template)
             The README lists the dead prototype files. The ACTIVE files (script.js and style.css)
             are not mentioned. This is the inverse of reality. Fix when E2a/E2b are deleted.
    [x] J7b. "RESTful API: Clean API endpoints for data operations" — routes.py has exactly one
             route that calls render_template(). There are zero API endpoints. Not accurate.
    [x] J7c. "💾 Data Persistence: Local storage for maintaining schedules between sessions" —
             script.js (the active file) has NO localStorage reads or writes anywhere (see E3b).
             This is a documented-but-not-implemented feature presented as if working.
    [x] J7d. "Drag-and-Drop Interface: Intuitive event creation and editing" — NOT implemented in
             script.js. Only present in the dead schedule_maker.js prototype class. Do not claim
             this as a current feature.
    [x] J7e. The README's feature list (Real-time Updates, Auto-save, Conflict Detection,
             Drag-and-Drop) is lifted from schedule_maker.js (the dead prototype) and describes
             that prototype's intended design — not the current working application in script.js.
             Rewrite README to accurately describe what script.js implements today: static employee
             roster, weekly schedule grid, shift assignment modals, and popover employee details.
             Mark drag-and-drop/export/localStorage as PLANNED.

  J8. Top-level README.md — architecture accurate; minor documentation gaps
    [ ] J8a. Architecture description (Static Hybrid Model, freeze.py → docs/ pipeline,
             Blueprint structure) is accurate and well-written. Project Structure diagram is
             correct. No major corrections needed here.
    [x] J8b. Minimum Python version not stated anywhere in README.md or requirements.txt.
             After J6c correction, document Python 3.9+ as the minimum. Add a comment to
             requirements.txt and a note to README's Prerequisites section.
    [ ] J8c. README.md does not mention the CNAME local-freeze risk (I4b): "Running python
             freeze.py locally will delete docs/CNAME, breaking the custom domain on the next
             push." Add a warning to the "Generate Static Site" section so future contributors
             don't silently break the domain by running a local freeze preview.
    [ ] J8d. build/ is not listed in the Project Structure diagram — correct, since it should
             be deleted. After I1d is done, verify the repo root is clean and the README structure
             matches actual directory contents.

  J9. Consolidated deletion manifest — all confirmed-dead files and directories
    [x] J9a. Files and directories to DELETE (all findings confirmed above or in earlier sections):
             DIRECTORIES: build/ (I1d), deployment/ (J1a), docs/static/data/ (I2b),
                          docs/projects/projects/ (I2c)
             STATIC FILES: static/style.css (J3a), static/css/enhanced-widgets.css (G9a),
                           static/projects/schedule_maker/schedule_maker.js (E2a),
                           static/projects/schedule_maker/schedule_maker.css (E2b)
             JS FILES: static/js/theme-manager.js (B4c/F1d)
             TEMPLATES: templates/index_old.html (H4a — archive or delete)
             Each deletion is safe to make individually. Deleting build/ must precede F3a/G7a
             removals in commit history to preserve the evidence trail for code review.
    [ ] J9b. After the deletion pass, run python freeze.py locally to verify the freeze output
             is clean and matches the expected docs/ structure before pushing to main.
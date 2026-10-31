// ── Homepage Projects grid ─────────────────────────────────────────────────
// Loads the repo inventory (via repo-loader.js), renders the grid with
// language filter chips, search, sort, and the expand control. The grid
// shows one list in API order (sorted by last push); the 'updated' sort
// key is therefore a no-op by design, not a missing feature. Filter,
// search, and sort combine, and any change collapses the grid back to
// the first PROJECTS_INITIAL_COUNT. Card thumbnails come from the
// server-injected window.JPL_CONFIG.projectThumbnails map; only mapped
// repos get a thumbnail, never a placeholder box.
let selectedLanguage = 'All';
let projectSearchQuery = '';
let projectSortKey = 'updated';
let projectsExpanded = false;
// How many projects show before the expand control appears. The
// threshold is a count, not a view: it applies to the full list and
// to any language-filtered list alike.
const PROJECTS_INITIAL_COUNT = 10;
let allRepos = [];

function renderRepoCard(repo) {
    const githubUser = window.JPL_CONFIG.githubUser;
    const name       = escHtml(repo.name);
    const desc       = escHtml(repo.description || 'No description provided.');
    const lang       = escHtml(repo.language || '');
    const stars      = repo.stargazers_count || 0;
    const forks      = repo.forks_count || 0;
    const topics     = (repo.topics || []).slice(0, 6).map(escHtml);
    const githubUrl  = escHtml(repo.html_url);

    const isFeatured  = (repo.topics || []).includes('featured');
    const statusBadge = isFeatured
        ? `<span class="badge-theme" style="background:#f59e0b;color:#000;border-color:#f59e0b;flex-shrink:0">&#9733; Featured</span>`
        : (lang ? `<span class="badge-theme" style="flex-shrink:0">${lang}</span>` : '');

    const langTag = lang
        ? `<span class="badge-theme"><span class="lang-dot" style="background:${langColor(repo.language)}" aria-hidden="true"></span>${lang}</span>`
        : '';
    const techTags  = [langTag, ...topics.map(t => `<span class="badge-theme">${t}</span>`)].filter(Boolean).slice(0, 7).join('');
    const statsHtml = (stars + forks) > 0
        ? `<small style="color:var(--text-secondary);font-size:0.7rem;margin-left:0.25rem;">${stars > 0 ? `<i class="bi bi-star"></i>&nbsp;${stars}` : ''}${forks > 0 ? `&nbsp;<i class="bi bi-diagram-2"></i>&nbsp;${forks}` : ''}</small>`
        : '';
    const btnGithub   = `<a href="${githubUrl}" class="repo-btn" target="_blank" rel="noopener noreferrer" aria-label="Open ${name} on GitHub"><i class="bi bi-github"></i>GitHub</a>`;
    const siteUrl = repoSiteUrl(repo, githubUser);
    const btnSite = siteUrl
        ? `<a href="${escHtml(siteUrl)}" class="repo-btn" target="_blank" rel="noopener noreferrer" aria-label="Open Pages site for ${name}"><i class="bi bi-globe"></i>Pages site</a>`
        : '';
    const thumbnails = window.JPL_CONFIG.projectThumbnails || {};
    const thumb = thumbnails[repo.name]
        ? `<img class="repo-card-thumb" src="/static/${escHtml(thumbnails[repo.name])}" alt="" loading="lazy">`
        : '';

    return `<div class="repo-card" data-repo-name="${name}" tabindex="0" role="button" aria-label="Preview ${name} repository" style="border-top-color:var(--primary-color)">${thumb}<div class="repo-card-body"><div class="repo-card-title"><span class="font-semibold text-sm">${name}${statsHtml}</span>${statusBadge}</div><p class="repo-card-desc">${desc}</p><div class="repo-card-footer"><div class="repo-card-tags flex flex-wrap gap-1">${techTags}</div><div class="repo-card-actions flex gap-1">${btnGithub}${btnSite}</div></div></div></div>`;
}

function renderLanguageFilters(repos) {
    const container = document.getElementById('language-filters');
    if (!container) return;
    // Chips are derived from the loaded repos, never hardcoded: a new
    // language in a future repo gets a chip automatically, and a language
    // with no repos gets none.
    const counts = new Map();
    repos.forEach(r => {
        const lang = r.language || 'Other';
        counts.set(lang, (counts.get(lang) || 0) + 1);
    });
    const langs = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    const chip = (lang, count, showDot) => {
        const active = lang === selectedLanguage;
        const dot = showDot ? `<span class="lang-dot" style="background:${langColor(lang)}" aria-hidden="true"></span>` : '';
        return `<button type="button" class="language-filter-btn${active ? ' active' : ''}" data-language-filter="${escHtml(lang)}" aria-pressed="${active}">${dot}${escHtml(lang)} <span class="lang-count">${count}</span></button>`;
    };
    // The All pill leads the row with the total count: the default load
    // shows every project in every language, so the default state
    // needs a pill that says so. Clicking it clears any language
    // filter; the toggle logic already makes that a no-op when All is
    // already selected.
    container.innerHTML = chip('All', repos.length, false) + langs.map(([lang, count]) => chip(lang, count, true)).join('');
    container.querySelectorAll('[data-language-filter]').forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.getAttribute('data-language-filter');
            selectedLanguage = (lang === selectedLanguage) ? 'All' : lang;
            projectsExpanded = false;
            container.querySelectorAll('[data-language-filter]').forEach(b => {
                const isActive = b.getAttribute('data-language-filter') === selectedLanguage;
                b.classList.toggle('active', isActive);
                b.setAttribute('aria-pressed', String(isActive));
            });
            renderProjects();
        });
    });
}

function renderProjects() {
    const gridEl = document.getElementById('projects-grid');
    const expandBtn = document.getElementById('projects-expand-btn');
    if (!gridEl || !expandBtn) return;
    const noRepos = (msg) => `<p class="col-span-full text-center py-4 text-sm" style="color:var(--text-secondary)">${msg}</p>`;
    let filtered = selectedLanguage === 'All'
        ? [...allRepos]
        : allRepos.filter(r => (r.language || 'Other') === selectedLanguage);
    const query = projectSearchQuery.trim().toLowerCase();
    if (query) {
        filtered = filtered.filter(r => {
            const haystack = [r.name, r.description, ...(r.topics || [])].filter(Boolean).join(' ').toLowerCase();
            return haystack.includes(query);
        });
    }
    if (projectSortKey === 'name') {
        filtered.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    } else if (projectSortKey === 'stars') {
        // Ties (most repos have 0 stars) fall back to name order so the
        // result is stable instead of looking shuffled.
        filtered.sort((a, b) => (b.stargazers_count || 0) - (a.stargazers_count || 0) || a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    }
    const shown = projectsExpanded ? filtered : filtered.slice(0, PROJECTS_INITIAL_COUNT);
    const empty = query
        ? `No projects match &ldquo;${escHtml(projectSearchQuery.trim())}&rdquo;. Try a different search or language.`
        : selectedLanguage === 'All'
            ? 'No repositories found.'
            : `No ${escHtml(selectedLanguage)} repositories. Try a different language.`;
    gridEl.innerHTML = shown.length ? shown.map(r => renderRepoCard(r)).join('') : noRepos(empty);
    if (filtered.length > PROJECTS_INITIAL_COUNT) {
        expandBtn.hidden = false;
        expandBtn.setAttribute('aria-expanded', String(projectsExpanded));
        expandBtn.innerHTML = projectsExpanded
            ? 'Show fewer <i class="bi bi-chevron-up"></i>'
            : `Show all ${filtered.length} projects <i class="bi bi-chevron-down"></i>`;
    } else {
        expandBtn.hidden = true;
    }
}

async function loadHomepageProjects() {
    const gridEl = document.getElementById('projects-grid');
    if (!gridEl) return;
    const repos = await loadRepos(window.JPL_CONFIG.githubUser);
    if (!repos) {
        gridEl.innerHTML = `<p class="col-span-full text-center py-4 text-sm" style="color:var(--text-secondary)"><i class="bi bi-exclamation-circle mr-1"></i>Could not load GitHub repositories.</p>`;
        return;
    }
    // One list, in API order (sorted by last push). The 'featured'
    // topic still earns a card its star badge in renderRepoCard.
    allRepos = filterActiveRepos(repos, window.JPL_CONFIG.githubUser);
    window.JPL.repos = allRepos;
    renderLanguageFilters(allRepos);
    renderProjects();
}

// Wiring: only on pages that carry the grid (the homepage). The
// document guard keeps this file requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.getElementById('projects-expand-btn')?.addEventListener('click', () => {
        projectsExpanded = !projectsExpanded;
        renderProjects();
    });
    document.getElementById('projects-search')?.addEventListener('input', (e) => {
        projectSearchQuery = e.target.value;
        projectsExpanded = false;
        renderProjects();
    });
    document.getElementById('projects-sort')?.addEventListener('change', (e) => {
        projectSortKey = e.target.value;
        projectsExpanded = false;
        renderProjects();
    });
    document.addEventListener('DOMContentLoaded', loadHomepageProjects);
}

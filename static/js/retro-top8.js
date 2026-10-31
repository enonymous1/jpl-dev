// ── Retro Top 8 grid ───────────────────────────────────────────────────────
// Retro's showcase grid over the same repo inventory the homepage loads
// (shared loader in repo-loader.js — no second copy of the cascade).
// Curated showcase, not "most recently updated": recency churned with
// every push and surfaced modernized old repos instead of the work the
// portfolio is meant to lead with. Fill from recent repos only if a
// showcase repo is missing, so the grid still reaches 8.
async function loadRetroTop8() {
    const el = document.getElementById('retro-top8');
    if (!el) return;
    const githubUser = window.JPL_CONFIG.githubUser;
    const repos = await loadRepos(githubUser);
    if (!repos) {
        el.innerHTML = '<p>Could not load GitHub repositories.</p>';
        return;
    }
    const active = filterActiveRepos(repos, githubUser);
    const showcase = window.JPL_CONFIG.retroShowcase || [];
    const top8 = showcase.map(name => active.find(r => r.name === name)).filter(Boolean);
    for (const repo of active) {
        if (top8.length >= 8) break;
        if (!top8.includes(repo)) top8.push(repo);
    }
    el.innerHTML = top8.map(r => {
        const initial = escHtml((r.name || '?').charAt(0).toUpperCase());
        const stars = r.stargazers_count ? ' &middot; &#9733; ' + r.stargazers_count : '';
        return '<div class="retro-top8-item"><div class="retro-top8-avatar">' + initial + '</div>'
            + '<p><a href="' + escHtml(r.html_url) + '" target="_blank" rel="noopener noreferrer">' + escHtml(r.name) + '</a></p>'
            + '<p>' + escHtml(r.language || '') + stars + '</p></div>';
    }).join('');
}

// Wiring: only on retro. The document guard keeps this file
// requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', loadRetroTop8);
}

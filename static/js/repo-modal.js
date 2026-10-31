// ── Project preview modal ────────────────────────────────────────────────────
// Clicking (or tapping, or Enter/Space on) a repo card opens a preview:
// the full description, metadata already in the loaded repo payload
// (language, topics, license, size, dates, stars/forks), action links,
// and the README rendered from GitHub. The README is fetched only when
// a modal opens, and cached in memory for the rest of the session.
// Focus stays inside the modal while it is open (Tab wraps), Escape
// closes it, and focus returns to the card that opened it.
let repoModalRequest = 0;
let repoModalReturnFocus = null;
const repoReadmeCache = new Map();

function formatRepoDate(iso) {
    try {
        return new Date(iso).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    } catch { return ''; }
}

function formatRepoSize(kb) {
    if (kb === undefined || kb === null) return '';
    return kb < 1024 ? `${kb} KB` : `${(kb / 1024).toFixed(1)} MB`;
}

async function loadRepoReadme(repo, branch) {
    const githubUser = window.JPL_CONFIG.githubUser;
    const bodyEl = document.getElementById('repo-modal-readme');
    if (!bodyEl) return;
    if (repoReadmeCache.has(repo.name)) {
        bodyEl.innerHTML = repoReadmeCache.get(repo.name);
        return;
    }
    const token = ++repoModalRequest;
    bodyEl.innerHTML = '<p class="repo-modal-loading">Loading README&hellip;</p>';
    const fallbackBranch = branch || repo.default_branch || 'main';
    let networkError = false;
    // 1. GitHub API README endpoint: filename- and branch-agnostic.
    try {
        const resp = await fetch(`https://api.github.com/repos/${githubUser}/${repo.name}/readme`, {
            headers: { 'Accept': 'application/vnd.github.raw' },
        });
        if (token !== repoModalRequest) return;
        if (resp.ok) {
            const rendered = renderMarkdown(await resp.text(), repo, fallbackBranch, githubUser);
            repoReadmeCache.set(repo.name, rendered);
            bodyEl.innerHTML = rendered;
            return;
        }
        if (resp.status !== 404 && resp.status !== 403) networkError = true;
    } catch { networkError = true; }
    // 2. Raw file fallback (covers API rate-limiting): default branch,
    //    then the other conventional branch name.
    if (!networkError) {
        for (const b of [...new Set([fallbackBranch, 'main', 'master'])]) {
            try {
                const resp = await fetch(`https://raw.githubusercontent.com/${githubUser}/${repo.name}/${b}/README.md`);
                if (token !== repoModalRequest) return;
                if (resp.ok) {
                    const rendered = renderMarkdown(await resp.text(), repo, b, githubUser);
                    repoReadmeCache.set(repo.name, rendered);
                    bodyEl.innerHTML = rendered;
                    return;
                }
                if (resp.status !== 404) { networkError = true; break; }
            } catch { networkError = true; break; }
        }
    }
    if (token !== repoModalRequest) return;
    bodyEl.innerHTML = networkError
        ? '<p class="repo-modal-empty">Couldn&rsquo;t load the README right now. The full project is on GitHub.</p>'
        : '<p class="repo-modal-empty">No README found for this repository. The full project is on GitHub.</p>';
}

function openRepoModal(name) {
    const githubUser = window.JPL_CONFIG.githubUser;
    const all = [...(window.JPL.repos || [])];
    const repo = all.find(r => r.name === name);
    if (!repo) return;
    repoModalReturnFocus = document.activeElement;
    const lang = repo.language || '';
    const license = repo.license && repo.license.name ? repo.license.name : '';
    const topics = (repo.topics || []).map(escHtml);
    const stats = [];
    if (repo.stargazers_count) stats.push(`<span><i class="bi bi-star"></i> ${repo.stargazers_count} star${repo.stargazers_count === 1 ? '' : 's'}</span>`);
    if (repo.forks_count) stats.push(`<span><i class="bi bi-diagram-2"></i> ${repo.forks_count} fork${repo.forks_count === 1 ? '' : 's'}</span>`);
    if (repo.open_issues_count) stats.push(`<span>${repo.open_issues_count} open issue${repo.open_issues_count === 1 ? '' : 's'}</span>`);
    if (repo.created_at) stats.push(`<span>Created ${formatRepoDate(repo.created_at)}</span>`);
    if (repo.pushed_at) stats.push(`<span>Last push ${formatRepoDate(repo.pushed_at)}</span>`);
    if (repo.size) stats.push(`<span>${formatRepoSize(repo.size)}</span>`);
    if (license) stats.push(`<span>${escHtml(license)}</span>`);
    const homepage = repoSiteUrl(repo, githubUser);
    document.getElementById('repo-modal-content').innerHTML = `
        <p class="repo-modal-kicker">${lang ? `<span class="badge-theme"><span class="lang-dot" style="background:${langColor(lang)}" aria-hidden="true"></span>${escHtml(lang)}</span>` : ''}<span>${escHtml(repo.full_name || repo.name)}</span></p>
        <h3 id="repo-modal-title" class="repo-modal-title">${escHtml(repo.name)}</h3>
        <p class="repo-modal-desc">${escHtml(repo.description || 'No description provided.')}</p>
        ${stats.length ? `<div class="repo-modal-meta">${stats.join('')}</div>` : ''}
        ${topics.length ? `<div class="repo-modal-topics">${topics.map(t => `<span class="badge-theme">${t}</span>`).join('')}</div>` : ''}
        <div class="repo-modal-actions">
            <a class="repo-modal-action repo-modal-action--primary" href="${escHtml(repo.html_url)}" target="_blank" rel="noopener noreferrer"><i class="bi bi-github"></i> View on GitHub</a>
            ${homepage ? `<a class="repo-modal-action" href="${escHtml(homepage)}" target="_blank" rel="noopener noreferrer">Visit site &rarr;</a>` : ''}
            <button type="button" class="repo-modal-action" data-clone-url="https://github.com/${githubUser}/${escHtml(repo.name)}.git">Copy clone URL</button>
        </div>
        <h4 class="repo-modal-readme-heading">README</h4>
        <div id="repo-modal-readme" class="repo-modal-readme"></div>`;
    // The copy button is wired here, not with an inline onclick: inline
    // handlers are the first thing a Content-Security-Policy breaks.
    document.querySelector('#repo-modal-content [data-clone-url]')?.addEventListener('click', (e) => {
        copyCloneUrl(e.currentTarget);
    });
    const modal = document.getElementById('repo-modal');
    modal.hidden = false;
    document.body.classList.add('repo-modal-open');
    document.getElementById('repo-modal-close').focus();
    loadRepoReadme(repo, repo.default_branch);
}

function closeRepoModal() {
    const modal = document.getElementById('repo-modal');
    if (!modal || modal.hidden) return;
    repoModalRequest++;
    modal.hidden = true;
    document.body.classList.remove('repo-modal-open');
    if (repoModalReturnFocus && document.contains(repoModalReturnFocus)) repoModalReturnFocus.focus();
}

async function copyCloneUrl(btn) {
    const url = btn.getAttribute('data-clone-url');
    try {
        await navigator.clipboard.writeText(url);
    } catch {
        const area = document.createElement('textarea');
        area.value = url;
        document.body.appendChild(area);
        area.select();
        try { document.execCommand('copy'); } catch {}
        area.remove();
    }
    const original = btn.textContent;
    btn.textContent = 'Copied \u2713';
    setTimeout(() => { btn.textContent = original; }, 1600);
}

// Wiring: card clicks open the preview, except on the real links inside a
// card (the GitHub button), which keep navigating. Backdrop and
// close-button clicks, and Escape, close it. Tab wraps inside the open
// modal instead of escaping to the page behind it. The document guard
// keeps this file requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.addEventListener('click', (e) => {
        if (e.target.closest('[data-modal-close]')) { closeRepoModal(); return; }
        const card = e.target.closest('.repo-card[data-repo-name]');
        if (card && !e.target.closest('a, button')) openRepoModal(card.getAttribute('data-repo-name'));
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') { closeRepoModal(); return; }
        const modal = document.getElementById('repo-modal');
        if (e.key === 'Tab' && modal && !modal.hidden) {
            const focusables = modal.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])');
            if (!focusables.length) return;
            const first = focusables[0];
            const last = focusables[focusables.length - 1];
            if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
            else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
            return;
        }
        if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('repo-card')) {
            e.preventDefault();
            openRepoModal(e.target.getAttribute('data-repo-name'));
        }
    });
}

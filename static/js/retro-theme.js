// ── Retro light/dark toggle ────────────────────────────────────────────────
// Independent of the clean site's theme, saved under its own key so
// flipping retro does not change the clean site.
function applyRetroTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const btn = document.getElementById('retro-theme-toggle');
    const label = document.getElementById('retro-theme-label');
    if (btn) btn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    if (label) label.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    try { window.localStorage.setItem('jpl_retro_theme', theme); } catch {}
}

// Wiring: only on retro. The document guard keeps this file
// requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.getElementById('retro-theme-toggle')?.addEventListener('click', function () {
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        applyRetroTheme(current === 'dark' ? 'light' : 'dark');
    });
    // Sync the button with the pre-paint choice (saved value or system)
    // without saving: a first visit should keep following the system until
    // the user explicitly toggles.
    (function () {
        const theme = document.documentElement.getAttribute('data-theme') || 'light';
        const btn = document.getElementById('retro-theme-toggle');
        const label = document.getElementById('retro-theme-label');
        if (btn) btn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
        if (label) label.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    })();
}

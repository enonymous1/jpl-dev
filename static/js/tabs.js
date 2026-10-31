// ── vCard section tabs ─────────────────────────────────────────────────────
// About / Projects / Curriculum Vitae / Blog / Contact, no reload.
// Deep-linkable via #about, #projects, #cv, #blog, #contact so a link
// can open a specific section on the frozen static site.
function activateVcardTab(name) {
    // Unknown names (e.g. #blog with no posts yet, so no Blog section
    // exists) leave the current tab alone instead of hiding everything.
    if (!document.querySelector('[data-vcard-section="' + name + '"]')) return;
    const sections = document.querySelectorAll('[data-vcard-section]');
    const tabs = document.querySelectorAll('[data-vcard-tab]');
    sections.forEach(s => {
        const show = s.getAttribute('data-vcard-section') === name;
        s.hidden = !show;
        if (show) {
            s.classList.remove('vcard-section-enter');
            void s.offsetWidth;
            s.classList.add('vcard-section-enter');
        }
    });
    tabs.forEach(b => { b.setAttribute('aria-selected', String(b.getAttribute('data-vcard-tab') === name)); });
    if (['about', 'projects', 'cv', 'contact', 'blog'].includes(name)) {
        history.replaceState(null, '', '#' + name);
    }
}

// Wiring: only on pages that carry the tab bar (the homepage). The
// document guard keeps this file requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.querySelectorAll('[data-vcard-tab]').forEach(b => {
        b.addEventListener('click', () => activateVcardTab(b.getAttribute('data-vcard-tab')));
    });
    // CV print button lives with the section code: it prints the whole
    // page, and the print stylesheet hides everything but the CV.
    document.getElementById('resume-print-btn')?.addEventListener('click', () => window.print());
    (function () {
        const hash = (window.location.hash || '').replace('#', '');
        if (['about', 'projects', 'cv', 'contact', 'blog'].includes(hash)) activateVcardTab(hash);
    })();
}

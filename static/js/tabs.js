// ── vCard section tabs ─────────────────────────────────────────────────────
// About / Projects / Websites / Curriculum Vitae / Blog / Videos / Contact,
// no reload. Deep-linkable via #about, #projects, #websites, #cv, #blog,
// #videos, #contact so a link can open a specific section on the frozen
// static site. One list drives both the history update and the hash
// handler, so they can't drift apart.
const VCARD_TABS = ['about', 'projects', 'websites', 'cv', 'contact', 'blog', 'videos'];

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
    if (VCARD_TABS.includes(name)) {
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
        if (VCARD_TABS.includes(hash)) activateVcardTab(hash);
    })();
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VCARD_TABS };
}

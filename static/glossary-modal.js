// Glossary and role definition modal, shared by the homepage and the
// blog post pages: both render the sidebar include, whose role pills
// and (on the homepage) Tools & Tech pills open this modal. Page data
// travels in window.GLOSSARY_DATA = {terms: {...}, roles: {...}}, set
// by an inline script before this file loads; the frozen site has no
// live Python runtime. Same interaction contract as the project
// preview: backdrop and close-button clicks and Escape close it, and
// focus returns to the pill that opened it. Entries without a URL
// (Team Building, Mentorship, and all three roles) show the definition
// with no link row.
(function () {
    function escHtml(s) {
        return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    let glossaryModalReturnFocus = null;

    function openGlossaryModal(term) {
        const data = window.GLOSSARY_DATA || {};
        const roles = data.roles || {};
        const terms = data.terms || {};
        const entry = roles[term] || terms[term];
        if (!entry) return;
        const modal = document.getElementById('glossary-modal');
        const content = document.getElementById('glossary-modal-content');
        if (!modal || !content) return;
        const kicker = roles[term] ? 'Role' : 'Tools &amp; Tech';
        const link = entry.url
            ? `<div class="repo-modal-actions"><a class="repo-modal-action repo-modal-action--primary" href="${escHtml(entry.url)}" target="_blank" rel="noopener noreferrer">Official site <i class="bi bi-box-arrow-up-right"></i></a></div>`
            : '';
        content.innerHTML = `<p class="repo-modal-kicker">${kicker}</p><h3 id="glossary-modal-title" class="repo-modal-title">${escHtml(term)}</h3><p class="repo-modal-desc">${escHtml(entry.definition)}</p>${link}`;
        glossaryModalReturnFocus = document.activeElement;
        modal.hidden = false;
        document.body.classList.add('repo-modal-open');
        document.getElementById('glossary-modal-close').focus();
    }

    function closeGlossaryModal() {
        const modal = document.getElementById('glossary-modal');
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        document.body.classList.remove('repo-modal-open');
        if (glossaryModalReturnFocus && document.contains(glossaryModalReturnFocus)) glossaryModalReturnFocus.focus();
    }

    document.addEventListener('click', (e) => {
        if (e.target.closest('[data-glossary-close]')) { closeGlossaryModal(); return; }
        const pill = e.target.closest('[data-glossary-term]');
        if (pill) openGlossaryModal(pill.getAttribute('data-glossary-term'));
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeGlossaryModal();
    });
})();

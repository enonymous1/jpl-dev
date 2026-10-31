// Location modal, shared by the homepage and the blog post pages:
// both render the sidebar include, whose Fredericksburg button opens
// this dialog. Content is rendered server-side in the partial, so this
// script only opens and closes it. Same interaction contract as the
// glossary modal: backdrop and close-button clicks and Escape close
// it, and focus returns to the button that opened it.
(function () {
    let locationModalReturnFocus = null;

    function openLocationModal() {
        const modal = document.getElementById('location-modal');
        if (!modal) return;
        locationModalReturnFocus = document.activeElement;
        modal.hidden = false;
        document.body.classList.add('repo-modal-open');
        document.getElementById('location-modal-close').focus();
    }

    function closeLocationModal() {
        const modal = document.getElementById('location-modal');
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        document.body.classList.remove('repo-modal-open');
        if (locationModalReturnFocus && document.contains(locationModalReturnFocus)) locationModalReturnFocus.focus();
    }

    document.addEventListener('click', (e) => {
        if (e.target.closest('[data-location-close]')) { closeLocationModal(); return; }
        if (e.target.closest('#location-modal-open')) openLocationModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLocationModal();
    });
})();

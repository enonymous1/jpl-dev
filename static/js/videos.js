// ── Videos tab search ────────────────────────────────────────────────────
// One search box filters every video card across all channel sections: a
// card matches when the query appears in its title, its shown
// description, or its channel name. A section with no visible cards
// hides, and a no-match message shows when nothing matches anywhere.
// No sort control: the list is newest-first by construction, per channel.
function videoMatches(title, description, channel, query) {
    const q = (query || '').trim().toLowerCase();
    if (!q) return true;
    return [title, description, channel].some(
        (text) => (text || '').toLowerCase().includes(q)
    );
}

function applyVideoSearch() {
    const input = document.getElementById('videos-search');
    const emptyEl = document.getElementById('videos-no-results');
    if (!input) return;
    const query = input.value;
    let visible = 0;
    document.querySelectorAll('#vcard-videos .video-section').forEach((section) => {
        let sectionVisible = 0;
        section.querySelectorAll('.video-card').forEach((card) => {
            const match = videoMatches(
                card.getAttribute('data-video-title'),
                card.getAttribute('data-video-description'),
                card.getAttribute('data-video-channel'),
                query
            );
            card.hidden = !match;
            if (match) sectionVisible++;
        });
        section.hidden = sectionVisible === 0;
        visible += sectionVisible;
    });
    if (emptyEl) {
        emptyEl.hidden = visible !== 0;
        emptyEl.textContent = visible === 0 && query.trim()
            ? `No videos match "${query.trim()}". Try a different search.`
            : '';
    }
}

// Wiring: only on pages that carry the list (the homepage). The
// document guard keeps this file requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.getElementById('videos-search')?.addEventListener('input', applyVideoSearch);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { videoMatches };
}

// Location modal, shared by the homepage and the blog post pages:
// both render the sidebar include, whose Fredericksburg button opens
// this dialog. Content is rendered server-side in the partial. Same
// interaction contract as the glossary modal: backdrop and
// close-button clicks and Escape close it, and focus returns to the
// button that opened it. The facts below the map are a carousel:
// prev/next arrows and left/right keys move one slide, the counter
// shows the position, and both ends wrap around. A wrap jump snaps
// instantly instead of sweeping back through every slide, and
// reopening the modal starts again at the first fact.

// Carousel index math, exported for Node tests (guarded: browsers
// never define module).
function nextFactIndex(index, total) {
    return (index + 1) % total;
}

function prevFactIndex(index, total) {
    return (index - 1 + total) % total;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { nextFactIndex, prevFactIndex };
}

(function () {
    if (typeof document === 'undefined') return;
    let locationModalReturnFocus = null;
    let resetCarousel = null;

    function openLocationModal() {
        const modal = document.getElementById('location-modal');
        if (!modal) return;
        locationModalReturnFocus = document.activeElement;
        modal.hidden = false;
        document.body.classList.add('repo-modal-open');
        if (resetCarousel) resetCarousel();
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

    const track = document.getElementById('location-track');
    if (track) {
        const counter = document.getElementById('location-fact-counter');
        const status = document.getElementById('location-fact-status');
        const prevBtn = document.getElementById('location-fact-prev');
        const nextBtn = document.getElementById('location-fact-next');
        const total = track.children.length;
        const titles = Array.from(track.children, (slide) => {
            const title = slide.querySelector('.location-fact-title');
            return title ? title.textContent : '';
        });
        let factIndex = 0;

        function showFact(index, instant) {
            factIndex = index;
            if (instant) track.classList.add('no-transition');
            track.style.transform = `translateX(${-factIndex * 100}%)`;
            if (instant) {
                void track.offsetWidth;
                track.classList.remove('no-transition');
            }
            if (counter) counter.textContent = `Fact ${factIndex + 1} of ${total}`;
            if (status) status.textContent = titles[factIndex] || '';
        }

        function goNext() {
            const next = nextFactIndex(factIndex, total);
            showFact(next, next === 0);
        }

        function goPrev() {
            const prev = prevFactIndex(factIndex, total);
            showFact(prev, prev === total - 1);
        }

        resetCarousel = () => showFact(0, true);
        if (prevBtn) prevBtn.addEventListener('click', goPrev);
        if (nextBtn) nextBtn.addEventListener('click', goNext);
        document.addEventListener('keydown', (e) => {
            const modal = document.getElementById('location-modal');
            if (!modal || modal.hidden) return;
            if (e.key === 'ArrowRight') goNext();
            else if (e.key === 'ArrowLeft') goPrev();
        });
    }
})();

// Avatar easter egg: the photo speaks in a speech bubble below it.
// Clicking cycles quips, escalating to a spin on the last one; idle
// for 5s and it resets. Hovering (or focusing) the photo shows a
// "Hello, World!" greeting bubble, but only while no clicked quip
// is pinned: a clicked quip always wins over the greeting, and
// leaving the photo never hides a pinned quip. Shared by the
// homepage and the blog post pages, whose sidebars are the same
// include. The script tag sits at the end of the body, after the
// sidebar markup it reads.
//
// Second egg on the same button: 10 clicks within 3 seconds opens
// a modal with a large copy of the photo that can be dragged to
// stretch, Mario 64 title-screen style; releasing springs it back.
// The burst also plays the normal quips (two full cycles); opening
// the modal resets the quip state so the bubble and spin do not
// linger behind it.

// Stretch math, exported for Node tests (guarded: browsers never
// define module). Dragging right/down stretches that axis; each
// 150px of drag is 1x of scale, clamped to half-to-double size.
function clampStretch(value) {
    return Math.min(2, Math.max(0.5, value));
}

function computeStretch(dx, dy) {
    return {
        scaleX: clampStretch(1 + dx / 150),
        scaleY: clampStretch(1 + dy / 150),
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { computeStretch };
}

(function () {
    if (typeof document === 'undefined') return;
    const btn = document.getElementById('avatar-easter-egg');
    const quip = document.getElementById('avatar-quip');
    if (!btn || !quip) return;
    const greeting = "Hello, World!";
    const lines = [
        "Hey. That's me.",
        "Yep, still me.",
        "The projects are in the next tab over.",
        "Okay, you found the clicky photo.",
        "Alright, you win. Go poke a repo instead."
    ];
    let count = 0;
    let timer = null;
    let pinned = false;
    function show(text) {
        quip.textContent = text;
        quip.classList.add('is-visible');
    }
    function hide() {
        quip.classList.remove('is-visible');
    }
    function resetQuipState() {
        count = 0;
        pinned = false;
        clearTimeout(timer);
        hide();
        btn.classList.remove('is-spinning');
    }

    // Face-stretch modal wiring. Elements live in the shared modal
    // partial; every lookup is guarded so pages without it simply
    // never open it.
    const RAPID_CLICKS = 10;
    const RAPID_WINDOW_MS = 3000;
    let clickTimes = [];
    let playReturnFocus = null;
    const playModal = document.getElementById('avatar-play-modal');
    const playPhoto = document.getElementById('avatar-play-photo');
    const playClose = document.getElementById('avatar-play-close');

    function openPlayModal() {
        if (!playModal || !playModal.hidden) return;
        resetQuipState();
        playReturnFocus = document.activeElement;
        playModal.hidden = false;
        document.body.classList.add('repo-modal-open');
        if (playClose) playClose.focus();
    }

    function closePlayModal() {
        if (!playModal || playModal.hidden) return;
        playModal.hidden = true;
        document.body.classList.remove('repo-modal-open');
        if (playReturnFocus && document.contains(playReturnFocus)) playReturnFocus.focus();
    }

    btn.addEventListener('click', () => {
        count = (count % lines.length) + 1;
        pinned = true;
        show(lines[count - 1]);
        if (count === lines.length) {
            btn.classList.remove('is-spinning');
            void btn.offsetWidth;
            btn.classList.add('is-spinning');
        }
        clearTimeout(timer);
        timer = setTimeout(() => {
            count = 0;
            pinned = false;
            hide();
        }, 5000);
        const now = Date.now();
        clickTimes = clickTimes.filter((t) => now - t < RAPID_WINDOW_MS);
        clickTimes.push(now);
        if (clickTimes.length >= RAPID_CLICKS) {
            clickTimes = [];
            openPlayModal();
        }
    });
    btn.addEventListener('mouseenter', () => {
        if (!pinned) show(greeting);
    });
    btn.addEventListener('mouseleave', () => {
        if (!pinned) hide();
    });
    btn.addEventListener('focus', () => {
        if (!pinned) show(greeting);
    });
    btn.addEventListener('blur', () => {
        if (!pinned) hide();
    });
    btn.addEventListener('animationend', () => {
        btn.classList.remove('is-spinning');
    });

    document.addEventListener('click', (e) => {
        if (e.target.closest('[data-avatar-play-close]')) closePlayModal();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closePlayModal();
    });

    if (playPhoto) {
        let dragging = false;
        let startX = 0;
        let startY = 0;
        playPhoto.addEventListener('pointerdown', (e) => {
            dragging = true;
            startX = e.clientX;
            startY = e.clientY;
            playPhoto.classList.remove('is-springing');
            try {
                playPhoto.setPointerCapture(e.pointerId);
            } catch (err) {
                // Synthetic events have no active pointer; real
                // pointer events always capture fine.
            }
        });
        playPhoto.addEventListener('pointermove', (e) => {
            if (!dragging) return;
            const { scaleX, scaleY } = computeStretch(e.clientX - startX, e.clientY - startY);
            playPhoto.style.transform = `scale(${scaleX}, ${scaleY})`;
        });
        const endDrag = () => {
            if (!dragging) return;
            dragging = false;
            playPhoto.classList.add('is-springing');
            playPhoto.style.transform = 'scale(1, 1)';
        };
        playPhoto.addEventListener('pointerup', endDrag);
        playPhoto.addEventListener('pointercancel', endDrag);
    }
})();

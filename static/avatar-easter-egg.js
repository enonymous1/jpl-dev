// Avatar easter egg: the photo speaks in a speech bubble below it.
// Clicking cycles quips, escalating to a spin on the last one; idle
// for 5s and it resets. Hovering (or focusing) the photo shows a
// "Hello, World!" greeting bubble, but only while no clicked quip
// is pinned: a clicked quip always wins over the greeting, and
// leaving the photo never hides a pinned quip. Shared by the
// homepage and the blog post pages, whose sidebars are the same
// include. The script tag sits at the end of the body, after the
// sidebar markup it reads.
(function () {
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
})();

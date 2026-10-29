// Avatar easter egg: clicking the photo cycles Warcraft-style quips,
// escalating to a spin on the last one. Idle for 5s and it resets.
// Shared by the homepage and the blog post pages, whose sidebars are
// the same include. The script tag sits at the end of the body, after
// the sidebar markup it reads.
(function () {
    const btn = document.getElementById('avatar-easter-egg');
    const quip = document.getElementById('avatar-quip');
    if (!btn || !quip) return;
    const lines = [
        "Hey. That's me.",
        "Yep, still me.",
        "The projects are in the next tab over.",
        "Okay, you found the clicky photo.",
        "Alright, you win. Go poke a repo instead."
    ];
    let count = 0;
    let timer = null;
    btn.addEventListener('click', () => {
        count = (count % lines.length) + 1;
        quip.textContent = lines[count - 1];
        quip.classList.add('is-visible');
        if (count === lines.length) {
            btn.classList.remove('is-spinning');
            void btn.offsetWidth;
            btn.classList.add('is-spinning');
        }
        clearTimeout(timer);
        timer = setTimeout(() => {
            count = 0;
            quip.classList.remove('is-visible');
        }, 5000);
    });
    btn.addEventListener('animationend', () => {
        btn.classList.remove('is-spinning');
    });
})();

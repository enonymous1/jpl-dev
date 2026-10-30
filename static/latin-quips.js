// Latin easter egg: clicking the CV subtitle cycles Latin developer
// quips, best first, then loops back to the definition. Idle for 5s
// and it resets. Same pattern as the avatar easter egg, but the text
// swaps with a quick fade-in instead of a spin. Homepage only: the
// blog post pages have no CV section, so the guard returns there.
// The definition itself lives in the HTML and is read on load, so it
// stays the single source for the starting text.
(function () {
    const btn = document.getElementById('latin-quip');
    if (!btn) return;
    const definition = btn.textContent;
    const quips = [
        'Ex memoria \u2014 \u201cout of memory.\u201d',
        'dum (verum) { spero; } \u2014 \u201cwhile (true) { I hope; }\u201d',
        'Condo, ergo sum \u2014 \u201cI build, therefore I am.\u201d',
        'Veni, vidi, vici (in localhost) \u2014 \u201cI came, I saw, I conquered... but it only works on my machine.\u201d',
        'Tabula rasa \u2014 \u201cBlank slate.\u201d',
        'Deus ex machina \u2014 \u201cGod from the machine.\u201d',
    ];
    let index = 0; // 0 = definition, 1..quips.length = quips
    let timer = null;
    btn.addEventListener('click', () => {
        index = (index + 1) % (quips.length + 1);
        btn.textContent = index === 0 ? definition : quips[index - 1];
        btn.classList.remove('latin-in');
        void btn.offsetWidth;
        btn.classList.add('latin-in');
        clearTimeout(timer);
        timer = setTimeout(() => {
            index = 0;
            btn.textContent = definition;
        }, 5000);
    });
})();

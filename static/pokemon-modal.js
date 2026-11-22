// Pokémon GO modal, shared by the homepage and the blog post pages:
// both render the sidebar include, whose Poké Ball button opens this
// dialog. Content is rendered server-side in the partial. Same
// interaction contract as the location modal: backdrop and
// close-button clicks and Escape close it, and focus returns to the
// button that opened it. The friend code is shown spaced for reading;
// Copy copies digits only, which is what Pokémon GO accepts in the
// app, and falls back to a temporary textarea when the clipboard API
// is unavailable.

// Pure helper, exported for Node tests (guarded: browsers never
// define module).
function friendCodeDigits(code) {
    return code.replace(/\D/g, '');
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { friendCodeDigits };
}

(function () {
    if (typeof document === 'undefined') return;
    let pokemonModalReturnFocus = null;

    function openPokemonModal() {
        const modal = document.getElementById('pokemon-modal');
        if (!modal) return;
        pokemonModalReturnFocus = document.activeElement;
        modal.hidden = false;
        document.body.classList.add('repo-modal-open');
        document.getElementById('pokemon-modal-close').focus();
    }

    function closePokemonModal() {
        const modal = document.getElementById('pokemon-modal');
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        document.body.classList.remove('repo-modal-open');
        if (pokemonModalReturnFocus && document.contains(pokemonModalReturnFocus)) pokemonModalReturnFocus.focus();
    }

    document.addEventListener('click', (e) => {
        if (e.target.closest('[data-pokemon-close]')) { closePokemonModal(); return; }
        if (e.target.closest('#pokemon-modal-open')) openPokemonModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closePokemonModal();
    });

    const copyBtn = document.getElementById('pokemon-copy-code');
    if (copyBtn) {
        const status = document.getElementById('pokemon-copy-status');
        const originalLabel = copyBtn.textContent;
        let resetTimer = null;
        copyBtn.addEventListener('click', async () => {
            const codeEl = document.getElementById('pokemon-friend-code');
            const digits = friendCodeDigits(codeEl ? codeEl.textContent : '');
            if (!digits) return;
            let copied = false;
            try {
                await navigator.clipboard.writeText(digits);
                copied = true;
            } catch (e) {
                const fallback = document.createElement('textarea');
                fallback.value = digits;
                document.body.appendChild(fallback);
                fallback.select();
                try { copied = document.execCommand('copy'); } catch (err) { copied = false; }
                document.body.removeChild(fallback);
            }
            if (!copied) return;
            copyBtn.textContent = 'Copied!';
            if (status) status.textContent = 'Friend code copied to clipboard.';
            if (resetTimer) clearTimeout(resetTimer);
            resetTimer = setTimeout(() => {
                copyBtn.textContent = originalLabel;
                if (status) status.textContent = '';
            }, 2000);
        });
    }
})();

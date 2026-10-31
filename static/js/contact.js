// ── Contact form ─────────────────────────────────────────────────────────────
// There is no server behind this static site, so the form does not
// pretend a message was sent. It builds a mailto link with the visitor's
// words and opens their own email app, addressed to the site owner's
// address, ready to send. buildContactMailto is kept separate so the
// encoding is testable without a mail client. The submit handler is
// wired here, not with an inline onsubmit: inline handlers are the
// first thing a Content-Security-Policy breaks.
function buildContactMailto(name, email, message, contactEmail) {
    const subject = `Portfolio contact from ${name}`;
    const body = `${message}\n\n\u2014 ${name} (${email})`;
    return `mailto:${contactEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

function sendContactEmail(event) {
    event.preventDefault();
    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const message = document.getElementById('contact-message').value.trim();
    if (!name || !email || !message) return false;
    window.location.href = buildContactMailto(name, email, message, window.JPL_CONFIG.contactEmail);
    return false;
}

// Wiring: only on pages that carry the form (the homepage). The
// document guard keeps this file requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.getElementById('contact-form')?.addEventListener('submit', sendContactEmail);
}

// Node-test exports (guarded: browsers never define module).
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { buildContactMailto };
}

// ── Project preview modal + dependency-free Markdown renderer ─────────────
// The renderer is intentionally small: it covers the shapes first-party
// READMEs use (headings, lists, tables, task lists, code, links) and
// silently drops the rest (strikethrough, footnotes, HTML blocks)
// rather than pulling in a Markdown dependency. README HTML is escaped
// BEFORE parsing, so a README can never inject markup into the page.

// Resolve a README-relative URL to something loadable: images to the
// raw file, links to the file view on GitHub. Absolute and anchor URLs
// keep their meaning; javascript:/vbscript:/data: URLs are refused
// outright (data:image/ is allowed for images: inert in an <img>).
function resolveReadmeUrl(src, repo, branch, isImage, githubUser) {
    const clean = src.trim().replace(/^["']|["']$/g, '');
    if (/^(https?:|data:image\/)/i.test(clean)) return clean;
    if (/^(javascript|vbscript|data):/i.test(clean)) return '';
    if (clean.startsWith('#')) return `${repo.html_url}${clean}`;
    const stripped = clean.replace(/^\.\//, '').replace(/^\//, '');
    if (!stripped) return '';
    return isImage
        ? `https://raw.githubusercontent.com/${githubUser}/${repo.name}/${branch}/${stripped}`
        : `${repo.html_url}/blob/${branch}/${stripped}`;
}

// Small, dependency-free Markdown renderer for READMEs, with the HTML
// escaped first so a README can never inject markup into the page.
// Covers the shapes these READMEs actually use: headings, lists
// (including task lists), tables, blockquotes, code fences and spans,
// bold/italic, images, and inline and reference-style links.
function mdInline(text, repo, branch, refs, githubUser) {
    const codes = [];
    let s = text.replace(/`([^`]+)`/g, (m, code) => {
        codes.push(`<code>${code}</code>`);
        return `\u0001CODE${codes.length - 1}\u0001`;
    });
    s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, (m, alt, src) => {
        const url = resolveReadmeUrl(src, repo, branch, true, githubUser);
        return url ? `<img src="${url}" alt="${alt}" loading="lazy">` : alt;
    });
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, (m, label, src) => {
        const url = resolveReadmeUrl(src, repo, branch, false, githubUser);
        return url ? `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>` : label;
    });
    s = s.replace(/\[([^\]]+)\]\[([^\]]*)\]/g, (m, label, ref) => {
        const url = refs[(ref || label).toLowerCase()];
        return url ? `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>` : label;
    });
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
         .replace(/__([^_]+)__/g, '<strong>$1</strong>')
         .replace(/\*([^*]+)\*/g, '<em>$1</em>')
         .replace(/_([^_]+)_/g, '<em>$1</em>');
    return s.replace(/\u0001CODE(\d+)\u0001/g, (m, i) => codes[+i]);
}

function renderMarkdown(md, repo, branch, githubUser) {
    const refs = {};
    let text = String(md || '').replace(/\r\n/g, '\n');
    // Reference definitions: [label]: url — collected, then dropped.
    text = text.replace(/^\[([^\]]+)\]:\s*(\S+)\s*$/gm, (m, label, url) => {
        refs[label.toLowerCase()] = resolveReadmeUrl(url, repo, branch, false, githubUser) || url;
        return '';
    });
    // Fenced code blocks: pulled out before escaping, restored verbatim.
    const codeBlocks = [];
    text = text.replace(/```(\w*)\n([\s\S]*?)(?:```|$)/g, (m, lang, code) => {
        codeBlocks.push(`<pre><code>${escHtml(code.replace(/\n$/, ''))}</code></pre>`);
        return `\u0000CODE${codeBlocks.length - 1}\u0000`;
    });
    text = escHtml(text);
    const lines = text.split('\n');
    const out = [];
    let para = [];
    let listTag = null;
    const flushPara = () => {
        if (para.length) out.push(`<p>${mdInline(para.join(' '), repo, branch, refs, githubUser)}</p>`);
        para = [];
    };
    const closeList = () => {
        if (listTag) { out.push(`</${listTag}>`); listTag = null; }
    };
    const isSeparatorRow = (line) => /^\s*\|?[\s:|-]+\|?\s*$/.test(line) && line.includes('-');
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();
        // Code fence placeholder, alone on its line.
        const codeMatch = trimmed.match(/^\u0000CODE(\d+)\u0000$/);
        if (codeMatch) { flushPara(); closeList(); out.push(codeBlocks[+codeMatch[1]]); continue; }
        if (!trimmed) { flushPara(); closeList(); continue; }
        // Table: header row followed by a separator row.
        if (trimmed.startsWith('|') && i + 1 < lines.length && isSeparatorRow(lines[i + 1])) {
            flushPara(); closeList();
            const cells = (row) => row.replace(/^\||\|$/g, '').split('|').map(c => mdInline(c.trim(), repo, branch, refs, githubUser));
            const header = cells(trimmed);
            const rows = [];
            i += 2;
            while (i < lines.length && lines[i].trim().startsWith('|')) { rows.push(cells(lines[i].trim())); i++; }
            i--;
            out.push(`<div class="repo-modal-table"><table><thead><tr>${header.map(c => `<th>${c}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`);
            continue;
        }
        const heading = trimmed.match(/^(#{1,6})\s+(.*)$/);
        if (heading) {
            flushPara(); closeList();
            const level = Math.min(heading[1].length + 2, 5);
            out.push(`<h${level}>${mdInline(heading[2], repo, branch, refs, githubUser)}</h${level}>`);
            continue;
        }
        if (/^(-{3,}|\*{3,}|_{3,})$/.test(trimmed)) { flushPara(); closeList(); out.push('<hr>'); continue; }
        // Blockquote: consecutive &gt; lines (escaped >) grouped.
        if (trimmed.startsWith('&gt;')) {
            flushPara(); closeList();
            const quote = [];
            while (i < lines.length && lines[i].trim().startsWith('&gt;')) {
                quote.push(lines[i].trim().replace(/^&gt;\s?/, ''));
                i++;
            }
            i--;
            out.push(`<blockquote>${mdInline(quote.join(' '), repo, branch, refs, githubUser)}</blockquote>`);
            continue;
        }
        const bullet = trimmed.match(/^[-*+]\s+(.*)$/);
        const ordered = trimmed.match(/^\d+[.)]\s+(.*)$/);
        if (bullet || ordered) {
            flushPara();
            const tag = bullet ? 'ul' : 'ol';
            if (listTag !== tag) { closeList(); out.push(`<${tag}>`); listTag = tag; }
            let item = (bullet || ordered)[1];
            item = item.replace(/^\[( |x|X)\]\s+/, (m, box) => box.trim() ? '&#9746; ' : '&#9744; ');
            out.push(`<li>${mdInline(item, repo, branch, refs, githubUser)}</li>`);
            continue;
        }
        closeList();
        para.push(trimmed);
    }
    flushPara();
    closeList();
    return out.join('\n').replace(/\u0000CODE(\d+)\u0000/g, (m, i) => codeBlocks[+i] || '');
}

// Node-test exports (guarded: browsers never define module).
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { resolveReadmeUrl, mdInline, renderMarkdown };
}

// ── Homepage Blog tab ────────────────────────────────────────────────────
// Client-side search, sort, and tag filter over the server-rendered
// post list. The list itself is rendered by Flask (see templates/
// index.html); this file only shows, hides, and reorders the <li>
// elements, so without JavaScript the full list still renders. Tag
// pills are server-rendered from the loaded posts (config/blog.py
// tag_counts), never hardcoded: a new tag gets a pill automatically.
// Filter, search, and sort combine, mirroring projects.js. Pinned
// posts stay first in every sort: pinning is a separate concept from
// sort order, and the pinned post is the blog's index.
let selectedBlogTag = 'All';
let blogSearchQuery = '';
let blogSortKey = 'newest';

// A post as the DOM layer reads it: title and summary from the item's
// text, tags/date/pinned from its data-blog-* attributes.
function readBlogItem(el) {
    const titleEl = el.querySelector('.blog-item-title');
    const summaryEl = el.querySelector('.blog-summary');
    return {
        el,
        title: titleEl ? titleEl.textContent.trim() : '',
        summary: summaryEl ? summaryEl.textContent.trim() : '',
        tags: (el.getAttribute('data-blog-tags') || '').split(' ').filter(Boolean),
        date: el.getAttribute('data-blog-date') || '',
        pinned: el.getAttribute('data-blog-pinned') === 'true',
    };
}

function blogItemMatches(item, tag, query) {
    if (tag !== 'All' && !item.tags.includes(tag)) return false;
    const q = query.trim().toLowerCase();
    if (!q) return true;
    const haystack = [item.title, item.summary, ...item.tags].join(' ').toLowerCase();
    return haystack.includes(q);
}

function sortBlogItems(items, sortKey) {
    // Pinned first in every sort; ties fall back to title so the
    // result is stable instead of looking shuffled.
    const byTitle = (a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase());
    return [...items].sort((a, b) => {
        if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
        if (sortKey === 'oldest') return a.date.localeCompare(b.date) || byTitle(a, b);
        if (sortKey === 'title') return byTitle(a, b);
        return b.date.localeCompare(a.date) || byTitle(a, b);
    });
}

function applyBlogFilters() {
    const listEl = document.getElementById('blog-list');
    const emptyEl = document.getElementById('blog-no-results');
    if (!listEl) return;
    const items = [...listEl.querySelectorAll('.blog-item')].map(readBlogItem);
    const visible = sortBlogItems(
        items.filter((item) => blogItemMatches(item, selectedBlogTag, blogSearchQuery)),
        blogSortKey,
    );
    const visibleSet = new Set(visible.map((item) => item.el));
    items.forEach((item) => {
        item.el.hidden = !visibleSet.has(item.el);
    });
    // Re-append in sorted order: appendChild moves an existing node,
    // so this reorders without rebuilding anything.
    visible.forEach((item) => listEl.appendChild(item.el));
    if (emptyEl) {
        if (visible.length) {
            emptyEl.hidden = true;
        } else {
            const query = blogSearchQuery.trim();
            emptyEl.textContent = query
                ? `No posts match "${query}". Try a different search or tag.`
                : selectedBlogTag === 'All'
                    ? 'No posts found.'
                    : `No ${selectedBlogTag} posts. Try a different tag.`;
            emptyEl.hidden = false;
        }
    }
}

// Wiring: only on pages that carry the list (the homepage). The
// document guard keeps this file requireable under Node for tests.
if (typeof document !== 'undefined') {
    document.getElementById('blog-search')?.addEventListener('input', (e) => {
        blogSearchQuery = e.target.value;
        applyBlogFilters();
    });
    document.getElementById('blog-sort')?.addEventListener('change', (e) => {
        blogSortKey = e.target.value;
        applyBlogFilters();
    });
    document.querySelectorAll('[data-blog-tag]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const tag = btn.getAttribute('data-blog-tag');
            selectedBlogTag = tag === selectedBlogTag ? 'All' : tag;
            document.querySelectorAll('[data-blog-tag]').forEach((b) => {
                const isActive = b.getAttribute('data-blog-tag') === selectedBlogTag;
                b.classList.toggle('active', isActive);
                b.setAttribute('aria-pressed', String(isActive));
            });
            applyBlogFilters();
        });
    });
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { blogItemMatches, sortBlogItems, readBlogItem };
}

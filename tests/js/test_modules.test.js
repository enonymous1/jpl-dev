// Node tests for the pure functions in the homepage JS modules.
// Run with: node --test tests/js/  (Node 20+; CI runs this too.)
// The modules are classic browser scripts, not ES modules: they expose
// their pure helpers through a guarded module.exports block, and the
// browser-only wiring is behind typeof-document guards.
const test = require('node:test');
const assert = require('node:assert/strict');

const loader = require('../../static/js/repo-loader.js');
global.escHtml = loader.escHtml;
const { renderMarkdown, resolveReadmeUrl } = require('../../static/js/readme-md.js');
const { buildContactMailto } = require('../../static/js/contact.js');
const { nextFactIndex, prevFactIndex } = require('../../static/location-modal.js');
const { friendCodeDigits } = require('../../static/pokemon-modal.js');

const repo = {
    name: 'demo',
    full_name: 'enonymous1/demo',
    html_url: 'https://github.com/enonymous1/demo',
    homepage: '',
    has_pages: false,
};

test('escHtml escapes markup and quotes, passes plain text through', () => {
    assert.equal(loader.escHtml('<a href="x">\'y\' & z</a>'),
        '&lt;a href=&quot;x&quot;&gt;&#39;y&#39; &amp; z&lt;/a&gt;');
    assert.equal(loader.escHtml('plain'), 'plain');
    assert.equal(loader.escHtml(null), '');
    assert.equal(loader.escHtml(undefined), '');
});

test('filterActiveRepos drops forks, archived, and hidden repos', () => {
    const repos = [
        { name: 'keep', fork: false, archived: false },
        { name: 'forked', fork: true, archived: false },
        { name: 'old', fork: false, archived: true },
        { name: 'jpl-dev', fork: false, archived: false },
        { name: 'enonymous1', fork: false, archived: false },
    ];
    assert.deepEqual(
        loader.filterActiveRepos(repos, 'enonymous1').map(r => r.name),
        ['keep'],
    );
});

test('repoSiteUrl prefers homepage, then Pages, then empty', () => {
    assert.equal(
        loader.repoSiteUrl({ ...repo, homepage: 'https://example.dev/' }, 'enonymous1'),
        'https://example.dev/',
    );
    assert.equal(
        loader.repoSiteUrl({ ...repo, has_pages: true }, 'enonymous1'),
        'https://enonymous1.github.io/demo/',
    );
    assert.equal(loader.repoSiteUrl(repo, 'enonymous1'), '');
    assert.equal(
        loader.repoSiteUrl({ ...repo, has_pages: true, name: 'a b' }, 'enonymous1'),
        'https://enonymous1.github.io/a%20b/',
    );
});

test('hasWebsite is true exactly when repoSiteUrl finds a site', () => {
    assert.equal(loader.hasWebsite({ ...repo, homepage: 'https://example.dev/' }, 'enonymous1'), true);
    assert.equal(loader.hasWebsite({ ...repo, has_pages: true }, 'enonymous1'), true);
    assert.equal(loader.hasWebsite(repo, 'enonymous1'), false);
    assert.equal(loader.hasWebsite({ ...repo, homepage: '   ' }, 'enonymous1'), false);
});

test('friendCodeDigits strips the display spacing, keeps digits only', () => {
    assert.equal(friendCodeDigits('8456 7104 2978'), '845671042978');
    assert.equal(friendCodeDigits('845671042978'), '845671042978');
    assert.equal(friendCodeDigits(''), '');
});

test('sortWebsites puts web languages first, keeps API order within groups', () => {
    assert.deepEqual(loader.WEBSITE_FIRST_LANGUAGES, ['HTML', 'JavaScript', 'TypeScript']);
    const mk = (name, language) => ({ ...repo, name, language });
    const input = [
        mk('py-tool', 'Python'),
        mk('web-game', 'JavaScript'),
        mk('docs-site', 'HTML'),
        mk('py-lib', 'Python'),
        mk('ts-app', 'TypeScript'),
        mk('no-lang', null),
        mk('ps-tool', 'PowerShell'),
        mk('web-page', 'HTML'),
    ];
    assert.deepEqual(
        loader.sortWebsites(input).map((r) => r.name),
        ['web-game', 'docs-site', 'ts-app', 'web-page', 'py-tool', 'py-lib', 'no-lang', 'ps-tool'],
    );
    // Input untouched: the sort returns a new list.
    assert.equal(input[0].name, 'py-tool');
});

test('langColor returns linguist colors and a fallback', () => {
    assert.equal(loader.langColor('Python'), '#3572a5');
    assert.equal(loader.langColor('Brainfuck'), '#888888');
    assert.equal(loader.langColor(undefined), '#888888');
});

test('resolveReadmeUrl handles absolute, relative, anchor, and refused URLs', () => {
    assert.equal(
        resolveReadmeUrl('https://example.dev/x.png', repo, 'main', true, 'enonymous1'),
        'https://example.dev/x.png',
    );
    assert.equal(
        resolveReadmeUrl('docs/shot.png', repo, 'main', true, 'enonymous1'),
        'https://raw.githubusercontent.com/enonymous1/demo/main/docs/shot.png',
    );
    assert.equal(
        resolveReadmeUrl('./guide.md', repo, 'main', false, 'enonymous1'),
        'https://github.com/enonymous1/demo/blob/main/guide.md',
    );
    assert.equal(
        resolveReadmeUrl('#setup', repo, 'main', false, 'enonymous1'),
        'https://github.com/enonymous1/demo#setup',
    );
    assert.equal(resolveReadmeUrl('javascript:alert(1)', repo, 'main', false, 'enonymous1'), '');
    assert.equal(resolveReadmeUrl('data:text/html,<b>x</b>', repo, 'main', false, 'enonymous1'), '');
    assert.equal(resolveReadmeUrl('', repo, 'main', false, 'enonymous1'), '');
});

test('renderMarkdown covers headings, emphasis, code, and escapes HTML', () => {
    const html = renderMarkdown('# Title\n\nHello **bold** and *italic* with `code`.\n\n<script>alert(1)</script>', repo, 'main', 'enonymous1');
    assert.match(html, /<h3>Title<\/h3>/);
    assert.match(html, /<strong>bold<\/strong>/);
    assert.match(html, /<em>italic<\/em>/);
    assert.match(html, /<code>code<\/code>/);
    assert.match(html, /&lt;script&gt;/);
    assert.doesNotMatch(html, /<script>alert/);
});

test('renderMarkdown covers tables, task lists, and code fences', () => {
    const md = '| A | B |\n|---|---|\n| 1 | 2 |\n\n- [ ] todo\n- [x] done\n\n```js\nconst x = 1;\n```';
    const html = renderMarkdown(md, repo, 'main', 'enonymous1');
    assert.match(html, /<table>/);
    assert.match(html, /<th>A<\/th>/);
    assert.match(html, /<td>2<\/td>/);
    assert.match(html, /&#9744; todo/);
    assert.match(html, /&#9746; done/);
    assert.match(html, /<pre><code>const x = 1;<\/code><\/pre>/);
});

test('renderMarkdown resolves reference links and relative images', () => {
    const md = 'See [the guide][g] and ![shot](docs/shot.png).\n\n[g]: guide.md';
    const html = renderMarkdown(md, repo, 'main', 'enonymous1');
    assert.match(html, /href="https:\/\/github\.com\/enonymous1\/demo\/blob\/main\/guide\.md"/);
    assert.match(html, /src="https:\/\/raw\.githubusercontent\.com\/enonymous1\/demo\/main\/docs\/shot\.png"/);
});

test('buildContactMailto encodes subject and body', () => {
    const url = buildContactMailto('Jane Doe', 'jane@example.dev', 'Hello & bye', 'justin@jpl-dev.com');
    assert.ok(url.startsWith('mailto:justin@jpl-dev.com?subject='));
    assert.match(url, /subject=Portfolio%20contact%20from%20Jane%20Doe/);
    assert.match(url, /Hello%20%26%20bye/);
    // encodeURIComponent leaves ( ) unescaped, so they appear literally.
    assert.match(url, /%E2%80%94%20Jane%20Doe%20\(jane%40example\.dev\)/);
});

test('carousel index math wraps at both ends', () => {
    assert.equal(nextFactIndex(10, 11), 0);
    assert.equal(nextFactIndex(0, 11), 1);
    assert.equal(prevFactIndex(0, 11), 10);
    assert.equal(prevFactIndex(5, 11), 4);
});

const { blogItemMatches, sortBlogItems } = require('../../static/js/blog.js');

test('blogItemMatches filters by tag and searches title, summary, and tags', () => {
    const item = { title: 'The FAR Overhaul, Explained', summary: 'Model deviations, proposed rules', tags: ['far', 'gsa'], date: '2026-11-25', pinned: false };
    assert.equal(blogItemMatches(item, 'All', ''), true);
    assert.equal(blogItemMatches(item, 'far', ''), true);
    assert.equal(blogItemMatches(item, 'gmail', ''), false);
    assert.equal(blogItemMatches(item, 'All', 'far overhaul'), true);
    assert.equal(blogItemMatches(item, 'All', 'deviations'), true);
    assert.equal(blogItemMatches(item, 'All', 'gsa'), true);
    assert.equal(blogItemMatches(item, 'All', 'password'), false);
    assert.equal(blogItemMatches(item, 'far', 'overhaul'), true);
    assert.equal(blogItemMatches(item, 'gmail', 'overhaul'), false);
});

test('sortBlogItems keeps pinned first in every sort', () => {
    const items = [
        { title: 'B Post', summary: '', tags: [], date: '2026-11-24', pinned: false },
        { title: 'A Post', summary: '', tags: [], date: '2026-11-25', pinned: false },
        { title: 'Pinned Post', summary: '', tags: [], date: '2026-10-28', pinned: true },
    ];
    assert.deepEqual(sortBlogItems(items, 'newest').map((i) => i.title), ['Pinned Post', 'A Post', 'B Post']);
    assert.deepEqual(sortBlogItems(items, 'oldest').map((i) => i.title), ['Pinned Post', 'B Post', 'A Post']);
    assert.deepEqual(sortBlogItems(items, 'title').map((i) => i.title), ['Pinned Post', 'A Post', 'B Post']);
});

global.sortWebsites = loader.sortWebsites;
const { websiteRepoMatches, sortWebsiteRepos } = require('../../static/js/projects.js');

test('websiteRepoMatches filters by language and searches name, description, and topics', () => {
    const repo = { name: 'whenwhere-drone-light-shows', description: 'Drone light shows in Charlottesville', language: 'JavaScript', topics: ['drone-light-show', 'canvas'] };
    assert.equal(websiteRepoMatches(repo, 'All', ''), true);
    assert.equal(websiteRepoMatches(repo, 'JavaScript', ''), true);
    assert.equal(websiteRepoMatches(repo, 'Python', ''), false);
    assert.equal(websiteRepoMatches(repo, 'All', 'drone'), true);
    assert.equal(websiteRepoMatches(repo, 'All', 'charlottesville'), true);
    assert.equal(websiteRepoMatches(repo, 'All', 'canvas'), true);
    assert.equal(websiteRepoMatches(repo, 'All', 'gmail'), false);
    assert.equal(websiteRepoMatches(repo, 'JavaScript', 'drone'), true);
    assert.equal(websiteRepoMatches(repo, 'Python', 'drone'), false);
    const untyped = { name: 'x', description: '', language: null, topics: [] };
    assert.equal(websiteRepoMatches(untyped, 'Other', ''), true);
    assert.equal(websiteRepoMatches(untyped, 'All', ''), true);
});

test('sortWebsiteRepos keeps web languages first by default, and sorts by recency or name', () => {
    const repos = [
        { name: 'py-tool', language: 'Python', pushed_at: '2026-11-25T00:00:00Z' },
        { name: 'js-site', language: 'JavaScript', pushed_at: '2026-11-20T00:00:00Z' },
        { name: 'html-site', language: 'HTML', pushed_at: '2026-11-24T00:00:00Z' },
        { name: 'ts-site', language: 'TypeScript', pushed_at: '2026-11-10T00:00:00Z' },
    ];
    assert.deepEqual(sortWebsiteRepos(repos, 'web').map((r) => r.name), ['js-site', 'html-site', 'ts-site', 'py-tool']);
    assert.deepEqual(sortWebsiteRepos(repos, 'recent').map((r) => r.name), ['py-tool', 'html-site', 'js-site', 'ts-site']);
    assert.deepEqual(sortWebsiteRepos(repos, 'name').map((r) => r.name), ['html-site', 'js-site', 'py-tool', 'ts-site']);
});

const { VCARD_TABS } = require('../../static/js/tabs.js');

test('vCard tabs include the Videos tab', () => {
    assert.deepEqual(VCARD_TABS, ['about', 'projects', 'websites', 'cv', 'contact', 'blog', 'videos']);
});

const { videoMatches } = require('../../static/js/videos.js');

test('videoMatches finds titles, descriptions, and channel names', () => {
    assert.equal(videoMatches('Lego Worlds 1 Billion studs method', '', 'Enonymous1 Gaming', 'lego'), true);
    assert.equal(videoMatches('Titanfall Assault', '', 'Enonymous1 Gaming', 'TITANFALL'), true);
    assert.equal(videoMatches('10HToCBoss2', 'Realm: Thrall', 'Justin Lyons', 'thrall'), true);
    assert.equal(videoMatches('10HToCBoss2', 'Realm: Thrall', 'Justin Lyons', 'gaming'), false);
    assert.equal(videoMatches('ANVIL Brone', '', 'Enonymous1 Gaming', 'gaming'), true);
    assert.equal(videoMatches('ANVIL Brone', '', 'Enonymous1 Gaming', ''), true);
    assert.equal(videoMatches('ANVIL Brone', '', 'Enonymous1 Gaming', 'zzz'), false);
});

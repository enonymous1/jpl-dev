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

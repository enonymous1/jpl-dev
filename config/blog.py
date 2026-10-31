#!/usr/bin/env python3
"""
Blog posts for the portfolio: Markdown files in ``content/posts/``.

Each post is one file with a ``---`` front-matter block and a Markdown
body::

    ---
    title: Interesting Links
    slug: interesting-links
    date: 2026-10-28
    summary: A running list of links and bookmarks worth sharing.
    tags: [bookmarks]
    pinned: true
    ---

    Body in Markdown.

``title``, ``slug``, ``date`` and ``summary`` are required; ``tags`` and
``pinned`` are optional. ``date`` is ``YYYY-MM-DD``. ``pinned`` posts
sort first in the list regardless of date. Unknown front-matter keys,
duplicate slugs, bad dates and empty bodies fail loudly (``ValueError``)
so a bad post breaks the build instead of publishing half-rendered.
``content/drafts/`` is never read, so unfinished posts cannot publish
by accident.

Posts are the author's own files in this repo, so bodies render with
raw HTML allowed (the ``extra`` extension) and no sanitizer: do not
feed untrusted Markdown through this loader.
"""

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import markdown

BASE_DIR = Path(__file__).resolve().parent.parent
POSTS_DIR = BASE_DIR / 'content' / 'posts'

FRONT_MATTER_KEYS = {'title', 'slug', 'date', 'summary', 'tags', 'pinned'}
REQUIRED_KEYS = {'title', 'slug', 'date', 'summary'}

_SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


@dataclass
class Post:
    """A single parsed blog post.

    Only ``html`` is rendered (templates use ``post.html``); the raw
    Markdown body is validated and then dropped, not kept on the object.
    """

    slug: str
    title: str
    date: date
    summary: str
    tags: list[str] = field(default_factory=list)
    pinned: bool = False
    html: str = ''

    @property
    def date_label(self) -> str:
        """Human date, e.g. ``October 28, 2026`` (platform-safe)."""
        return f'{self.date.strftime("%B")} {self.date.day}, {self.date.year}'

    @property
    def url_path(self) -> str:
        return f'/blog/{self.slug}/'


def slugify(title: str) -> str:
    """Turn a post title into a URL slug: lowercase, hyphens, no extras."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return slug or 'post'


def build_post_source(title: str, post_date: date, slug: str) -> str:
    """Front-matter scaffold for a new post (body left for the author)."""
    return (
        '---\n'
        f'title: {title}\n'
        f'slug: {slug}\n'
        f'date: {post_date.isoformat()}\n'
        'summary: \n'
        'tags: []\n'
        'pinned: false\n'
        '---\n'
        '\n'
        '<!-- Write the post in Markdown below. Delete this comment. -->\n'
    )


def _parse_front_matter(text: str, path: Path) -> tuple[dict[str, str], str]:
    if not text.startswith('---\n'):
        raise ValueError(f'{path}: post must start with a --- front-matter block')
    end = text.find('\n---', 4)
    if end == -1:
        raise ValueError(f'{path}: front-matter block is not closed with ---')
    raw = text[4:end]
    body = text[end + 4 :]
    if body.startswith('\n'):
        body = body[1:]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' not in line:
            raise ValueError(f'{path}: bad front-matter line: {line!r}')
        key, value = line.split(':', 1)
        fields[key.strip()] = value.strip()
    unknown = set(fields) - FRONT_MATTER_KEYS
    if unknown:
        raise ValueError(f'{path}: unknown front-matter keys: {sorted(unknown)}')
    missing = REQUIRED_KEYS - set(fields)
    if missing:
        raise ValueError(f'{path}: missing front-matter keys: {sorted(missing)}')
    return fields, body


def _parse_tags(value: str, path: Path) -> list[str]:
    value = value.strip()
    if value.startswith('[') and value.endswith(']'):
        value = value[1:-1]
    tags = [tag.strip().strip('\'"') for tag in value.split(',') if tag.strip()]
    if any(not tag for tag in tags):
        raise ValueError(f'{path}: empty tag in tags list')
    return tags


def _parse_bool(value: str, path: Path) -> bool:
    lowered = value.strip().lower()
    if lowered in {'true', 'yes', '1'}:
        return True
    if lowered in {'false', 'no', '0'}:
        return False
    raise ValueError(f'{path}: pinned must be true or false, got {value!r}')


def parse_post(path: Path) -> Post:
    """Parse one post file, validating its front matter and body."""
    text = path.read_text(encoding='utf-8')
    fields, body = _parse_front_matter(text, path)
    slug = fields['slug']
    if not _SLUG_RE.match(slug):
        raise ValueError(f'{path}: slug must be lowercase letters, digits and hyphens: {slug!r}')
    if not _DATE_RE.match(fields['date']):
        raise ValueError(f'{path}: date must be YYYY-MM-DD, got {fields["date"]!r}')
    try:
        parsed_date = date.fromisoformat(fields['date'])
    except ValueError as exc:
        raise ValueError(f'{path}: invalid date {fields["date"]!r}') from exc
    if not body.strip():
        raise ValueError(f'{path}: post body is empty')
    html = markdown.markdown(body, extensions=['extra', 'sane_lists'], output_format='html5')
    return Post(
        slug=slug,
        title=fields['title'],
        date=parsed_date,
        summary=fields['summary'],
        tags=_parse_tags(fields.get('tags', ''), path),
        pinned=_parse_bool(fields.get('pinned', 'false'), path),
        html=html,
    )


def load_posts(posts_dir: Path | None = None) -> list[Post]:
    """Load every post in ``posts_dir``, pinned first, then newest first.

    An empty or missing directory is a valid empty blog: the Blog tab
    only renders when this returns posts.
    """
    directory = Path(posts_dir) if posts_dir is not None else POSTS_DIR
    if not directory.is_dir():
        return []
    posts = [parse_post(path) for path in sorted(directory.glob('*.md'))]
    seen: set[str] = set()
    for post in posts:
        if post.slug in seen:
            raise ValueError(f'duplicate blog slug: {post.slug!r}')
        seen.add(post.slug)
    posts.sort(key=lambda p: (not p.pinned, -p.date.toordinal(), p.slug))
    return posts

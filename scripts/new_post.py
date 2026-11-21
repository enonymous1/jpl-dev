#!/usr/bin/env python3
"""Scaffold a new blog post: ``python scripts/new_post.py "My Post Title"``.

Writes ``content/posts/YYYY-MM-DD-<slug>.md`` with the front-matter
filled in and the body left for the author. Refuses to overwrite an
existing file. Drafts live in ``content/drafts/`` instead: create the
file there by hand (or move it there), since the loader never reads
that directory.
"""

import sys
from datetime import date
from pathlib import Path

# The scripts live in scripts/, one level below the repo root; the
# config package lives at the root, so that is what goes on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.blog import POSTS_DIR, build_post_source, slugify  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('Usage: python scripts/new_post.py "Post Title"', file=sys.stderr)
        return 2
    title = argv[1].strip()
    if not title:
        print('Post title must not be empty.', file=sys.stderr)
        return 2
    today = date.today()
    path = POSTS_DIR / f'{today.isoformat()}-{slugify(title)}.md'
    if path.exists():
        print(f'Refusing to overwrite existing post: {path}', file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_post_source(title, today, slugify(title)), encoding='utf-8')
    print(f'Created {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

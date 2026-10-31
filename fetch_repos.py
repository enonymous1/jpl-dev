#!/usr/bin/env python3
"""
Fetch public GitHub repository metadata and cache it to static/data/repos.json.

Run this script to refresh the cached repo data used by the Featured Projects
widget.  In CI (deploy.yml) this runs automatically before freeze.py so the
frozen site always ships up-to-date data.  Run it locally whenever you want to
pull fresh data into your dev environment:

    python fetch_repos.py

The JS in index.html loads from /static/data/repos.json first and falls back
to the live GitHub API if the file is absent or empty — so local dev still
works without running this script first.

Resilience notes: the API is paginated (100 per page), forks and archived
repos are filtered out (the homepage already hides the profile and jpl-dev
repos itself, so those are kept in the file), and on an API failure the
previously cached file is kept instead of failing the whole build — unless
there is no usable cache, in which case the build fails loudly.

Payload notes: the API returns ~80 keys per repo, but the homepage and
retro grid read about 16 of them. The snapshot is slimmed to those fields
before writing (see REPO_FIELDS), which cuts the file by roughly two
thirds — it ships to every visitor on every page load, so the keys nobody
reads should not travel with it.
"""

import json
import os
import sys
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from config.site import GITHUB_USER  # noqa: E402

PER_PAGE = 100
MAX_PAGES = 10
OUTPUT_PATH = os.path.join(BASE_DIR, 'static', 'data', 'repos.json')

API_BASE = f'https://api.github.com/users/{GITHUB_USER}/repos'

# The only repo fields the site reads (homepage cards + preview modal +
# retro Top 8). Everything else the API returns (every *_url, owner,
# node_id, visibility, ...) is dropped by _slim before writing.
REPO_FIELDS = {
    'name',
    'full_name',
    'description',
    'language',
    'topics',
    'stargazers_count',
    'forks_count',
    'html_url',
    'homepage',
    'has_pages',
    'default_branch',
    'created_at',
    'pushed_at',
    'size',
    'open_issues_count',
    'fork',
    'archived',
}


def _headers():
    headers = {
        'User-Agent': 'jpl-dev-build/1.0',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    # Use GITHUB_TOKEN if available (e.g. in CI) to raise rate limit from 60→5000/hr
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GITHUB_TOKEN_READ')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def parse_next_link(link_header):
    """Return the URL for rel="next" in a GitHub Link header, or None."""
    if not link_header:
        return None
    for part in link_header.split(','):
        part = part.strip()
        if 'rel="next"' in part:
            url = part.split(';')[0].strip()
            if url.startswith('<') and url.endswith('>'):
                return url[1:-1]
    return None


def filter_repos(repos):
    """Drop forks and archived repos; keep everything else in API order."""
    return [r for r in repos if not r.get('fork') and not r.get('archived')]


def _slim(repo):
    """Reduce one API repo payload to the fields the site reads.

    The license is flattened to its name: the modal renders
    ``repo.license.name`` and nothing else from the license object.
    """
    slim = {key: repo.get(key) for key in REPO_FIELDS}
    license_ = repo.get('license') or {}
    slim['license'] = {'name': license_.get('name')} if license_.get('name') else None
    return slim


def fetch_repos():
    """Fetch all public repos for GITHUB_USER, following pagination.

    Returns the filtered list (forks and archived repos dropped, API
    order preserved). Raises RuntimeError on any HTTP or network
    failure — callers decide whether to fall back to cache; this
    function never silently returns partial data, because a truncated
    snapshot would publish as if it were the whole inventory.
    """
    url = f'{API_BASE}?sort=updated&per_page={PER_PAGE}&type=public'
    all_repos = []
    for _ in range(MAX_PAGES):
        req = urllib.request.Request(url, headers=_headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                next_url = parse_next_link(resp.headers.get('Link'))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f'GitHub API returned HTTP {exc.code}: {exc.reason}') from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f'Could not reach GitHub API: {exc.reason}') from exc
        if not isinstance(data, list):
            raise RuntimeError(f'GitHub API returned unexpected payload: {data!r}'[:200])
        all_repos.extend(data)
        if not next_url:
            break
        url = next_url
    return filter_repos(all_repos)


def _cached_repos():
    """Previously cached repos, or None if the cache is missing/unusable."""
    try:
        with open(OUTPUT_PATH, encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, list) and data else None


def main():
    print(f'Fetching repos for {GITHUB_USER}...')
    try:
        repos = [_slim(repo) for repo in fetch_repos()]
    except RuntimeError as exc:
        cached = _cached_repos()
        if cached is not None:
            print(
                f'WARNING: {exc}; keeping cached {OUTPUT_PATH} ({len(cached)} repos)',
                file=sys.stderr,
            )
            return 0
        print(f'ERROR: {exc}; no usable cache at {OUTPUT_PATH}', file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)

    print(f'Wrote {len(repos)} repos → {os.path.relpath(OUTPUT_PATH)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

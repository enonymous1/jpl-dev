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
"""

import json
import os
import sys
import urllib.error
import urllib.request

GITHUB_USER = 'enonymous1'
PER_PAGE    = 30
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'static', 'data', 'repos.json')

API_URL = (
    f'https://api.github.com/users/{GITHUB_USER}/repos'
    f'?sort=updated&per_page={PER_PAGE}&type=public'
)


def fetch_repos() -> list:
    req = urllib.request.Request(
        API_URL,
        headers={
            'User-Agent':  'jpl-dev-build/1.0',
            'Accept':      'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        },
    )
    # Use GITHUB_TOKEN if available (e.g. in CI) to raise rate limit from 60→5000/hr
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GITHUB_TOKEN_READ')
    if token:
        req.add_header('Authorization', f'Bearer {token}')

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        print(f'ERROR: GitHub API returned HTTP {exc.code}: {exc.reason}', file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f'ERROR: Could not reach GitHub API: {exc.reason}', file=sys.stderr)
        sys.exit(1)

    return data


def main():
    print(f'Fetching repos for {GITHUB_USER}...')
    repos = fetch_repos()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)

    print(f'Wrote {len(repos)} repos → {os.path.relpath(OUTPUT_PATH)}')


if __name__ == '__main__':
    main()

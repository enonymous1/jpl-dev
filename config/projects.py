#!/usr/bin/env python3
"""
About-me metadata for the portfolio.

Project data no longer lives here: the GSA MAS Checklist and Schedule Maker
were removed from this repo (they may become standalone projects later),
the /projects page was removed with them, and project listings now come
from GitHub — the homepage Projects tab loads repos.json (refreshed by
fetch_repos.py in CI) with a live GitHub API fallback, and retro's Top 8
uses the same source. This module holds only the profile data both the
clean homepage and retro render.
"""

from config.models import AboutMe, ToolGroup

# ========================================================================
# ABOUT ME
# ========================================================================
ABOUT_ME = AboutMe(
    name='Justin P. Lyons',
    bio=(
        'IT Manager with AS & BS in Computer Science. I build tools that automate '
        'repetitive work — pricing and vendor data, message and photo archives, '
        'video and market-data pipelines — and the dashboards and infrastructure '
        'that run them. Mobile development is where I started; automation and '
        'full-stack tools are where most of my recent work lives.'
    ),
    # Local copy of the GitHub profile photo (avatars.githubusercontent.com,
    # enonymous1), downloaded 2026-10-26 and committed so the frozen site
    # does not hotlink an external avatar. If the GitHub avatar changes,
    # replace this file to match.
    profile_image='images/profile.jpg',
    badges=['IT Manager', 'Automation Engineer', 'Full-Stack Developer'],
    highlights=[
        'Builds automation for real operations: store, contracting, and personal archives',
        'Ships tested, documented tools with CI — not just demos',
        'Runs a homelab stack (Unraid, Docker) for media, backups, and automation',
        'Background in mobile development (Android, iOS) and full-stack web',
    ],
    # No percentage skill bars: they were never rendered, and a self-assigned
    # 90 vs 88 proves nothing. The tool groups are the evidence instead.
    tool_groups=[
        ToolGroup(
            'Languages',
            'bi-file-code',
            ['Python', 'JavaScript', 'TypeScript', 'Java', 'Kotlin', 'Swift'],
        ),
        ToolGroup(
            'Automation & Data',
            'bi-gear',
            ['Flask', 'GitHub Actions', 'Playwright', 'Pandas', 'SQLite', 'Parquet'],
        ),
        ToolGroup('Mobile', 'bi-phone', ['Android', 'iOS', 'Flutter', 'React Native']),
        ToolGroup(
            'Infrastructure',
            'bi-hdd-stack',
            ['Docker', 'Unraid', 'AWS', 'Firebase'],
        ),
        ToolGroup(
            'Leadership',
            'bi-people',
            ['Team Building', 'Agile', 'Project Management', 'Mentorship'],
        ),
        ToolGroup('Tools', 'bi-tools', ['Git', 'GitHub', 'Jira']),
    ],
)

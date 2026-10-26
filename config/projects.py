#!/usr/bin/env python3
"""
Project Repository

Static portfolio metadata used by the build pipeline and static portfolio
templates. This module defines the project catalog and a deterministic sort
order, so the site can render without any runtime backend dependencies.
"""

from datetime import datetime

from config.models import (
    AboutMe,
    ProjectCategory,
    ProjectData,
    ProjectImage,
    ProjectLinks,
    ProjectStatus,
    ToolGroup,
)

# ========================================================================
# STATIC PROJECT DEFINITIONS
# ========================================================================
# The canonical project catalog. Each ProjectData object should represent a
# static portfolio entry that can be rendered at build time.
_PROJECTS = [
    ProjectData(
        id='gsa_mas_checklist',
        title='Interactive GSA MAS New Offeror Checklist',
        description=(
            'A comprehensive interactive checklist for GSA Multiple Award '
            'Schedule (MAS) offer preparation. Streamlines the complex federal '
            'contracting process with an intuitive, step-by-step interface.'
        ),
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.WEB_APP,
        features=[
            'Step-by-step checklist validation with progress tracking',
            'SINs selection with advanced filtering and search',
            'Rich text notes management with Quill editor',
            'Complete data export/import capabilities (JSON/Excel)',
            'Dark/light theme support with system preference detection',
            'Local storage persistence for work-in-progress',
            'Responsive design for desktop and mobile use',
        ],
        tech_stack=[
            'Flask',
            'JavaScript',
            'Quill.js',
            'CSS Grid',
            'Local Storage',
            'JSON',
            'Excel Export',
        ],
        tags=['government', 'contracting', 'checklist', 'productivity', 'flask'],
        route='gsa_mas_checklist.gsa_mas_checklist',
        links=ProjectLinks(
            github='https://github.com/enonymous1/jpl-dev',
            documentation=(
                'https://github.com/enonymous1/jpl-dev/blob/main/projects/'
                'gsa_mas_checklist/README.md'
            ),
        ),
        images=[
            ProjectImage(
                filename='gsa_checklist_hero.svg',
                alt_text=('GSA MAS Checklist main interface showing checklist items and progress'),
                caption='Main checklist interface with progress tracking and theme toggle',
                is_hero=True,
                is_thumbnail=True,
            )
        ],
        created_date=datetime(2025, 6, 1),
        last_updated=datetime(2025, 7, 11),
        priority=10,
    ),
    ProjectData(
        id='schedule_maker',
        title='Interactive Schedule Maker',
        description=(
            'A comprehensive schedule creation and management tool with '
            'drag-and-drop functionality, multiple view modes, and export '
            'capabilities.'
        ),
        status=ProjectStatus.DEVELOPMENT,
        category=ProjectCategory.WEB_APP,
        features=[
            'Multiple view modes (Day, Week, Month)',
            'Drag-and-drop event creation and editing',
            'Color-coded event categorization',
            'Real-time schedule conflict detection',
            'Export to JSON and calendar formats',
            'Local storage for data persistence',
            'Responsive design for all devices',
        ],
        tech_stack=['Flask', 'JavaScript ES6+', 'CSS Grid', 'Local Storage', 'Canvas API'],
        tags=['productivity', 'scheduling', 'calendar', 'time-management', 'flask'],
        route='schedule_maker.schedule_maker',
        links=ProjectLinks(
            github='https://github.com/enonymous1/jpl-dev',
            documentation=(
                'https://github.com/enonymous1/jpl-dev/blob/main/projects/schedule_maker/README.md'
            ),
        ),
        images=[
            ProjectImage(
                filename='schedule_maker_hero.svg',
                alt_text=('Schedule Maker main interface with weekly view and event creation'),
                caption='Interactive schedule interface with multiple view modes',
                is_hero=True,
                is_thumbnail=True,
            )
        ],
        created_date=datetime(2025, 7, 11),
        last_updated=datetime(2025, 7, 11),
        priority=8,
    ),
    # Shipped tools, hosted in their own repos. No internal route: the card
    # links out to GitHub via external_url, and the template handles a
    # missing route. These are the projects the homepage repo cards point
    # to, so the /projects page and the homepage now tell the same story.
    ProjectData(
        id='repo_sync',
        title='repo-sync',
        description=(
            'You have dozens of repos on GitHub and dozens of folders on disk. '
            'repo-sync tells you which is which: it syncs GitHub repo metadata, '
            'reconciles it against local folders, and reports the mismatches.'
        ),
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.TOOL,
        features=[
            'GitHub REST sync of repo metadata',
            'Local scanner and remote-vs-local reconciliation',
            'Metadata reports and a .py-to-Markdown exporter',
        ],
        tech_stack=['Python', 'GitHub API', 'CSV', 'Markdown'],
        tags=['automation', 'github', 'cli', 'developer-tools'],
        external_url='https://github.com/enonymous1/repo-sync',
        links=ProjectLinks(github='https://github.com/enonymous1/repo-sync'),
        last_updated=datetime(2026, 10, 24),
        priority=9,
    ),
    ProjectData(
        id='gas_auditor',
        title='gas-auditor',
        description=(
            'Google hides some of your scripts from Drive. This finds them anyway: '
            'an inventory and audit tool for every Google Apps Script project '
            'across Drive, the Script API, and Apps Script-native dashboards.'
        ),
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.TOOL,
        features=[
            'Discovers scripts Drive search misses',
            'CLI plus a Flask dashboard plus bulk source export',
            'Anonymized sample output, no real account data in the repo',
        ],
        tech_stack=['Python', 'Flask', 'Google APIs', 'OAuth'],
        tags=['automation', 'audit', 'google-workspace', 'cli'],
        external_url='https://github.com/enonymous1/gas-auditor',
        links=ProjectLinks(github='https://github.com/enonymous1/gas-auditor'),
        last_updated=datetime(2026, 10, 24),
        priority=7,
    ),
    ProjectData(
        id='photo_stitcher',
        title='photo-stitcher',
        description=(
            'A review and stitch wizard for FastFoto-style scans: pick the best '
            'front, stitch the back, rotate losslessly, and organize finished '
            'groups — with pause and resume so a large archive survives interruptions.'
        ),
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.DESKTOP,
        features=[
            'Best-front pick and directional back-stitching',
            'Lossless rotation and pause/resume state',
            'Single-scan and reviewed-original organizing',
        ],
        tech_stack=['Python', 'PyQt6', 'Pillow'],
        tags=['desktop', 'image-processing', 'photo-scanning'],
        external_url='https://github.com/enonymous1/photo-stitcher',
        links=ProjectLinks(github='https://github.com/enonymous1/photo-stitcher'),
        last_updated=datetime(2026, 10, 24),
        priority=6,
    ),
    ProjectData(
        id='sms_toolkit',
        title='sms-toolkit',
        description=(
            'Your backup app copies everything, every day. This keeps only '
            "what's new: it deduplicates SMS and MMS backups into a clean, "
            'queryable archive.'
        ),
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.TOOL,
        features=[
            'Incremental backup: only new messages are kept',
            'Deduplication across repeated full backups',
            'Flask viewer over the cleaned archive',
        ],
        tech_stack=['Python', 'Flask', 'SQLite', 'OCR'],
        tags=['automation', 'data-cleaning', 'messaging', 'cli'],
        external_url='https://github.com/enonymous1/sms-toolkit',
        links=ProjectLinks(github='https://github.com/enonymous1/sms-toolkit'),
        last_updated=datetime(2026, 10, 24),
        priority=5,
    ),
    # Template entries are intentionally left commented out as a reference for
    # future additions. They should not affect build-time behavior.
]

# ========================================================================
# COMPUTED SORT ORDER
# ========================================================================
# Sort by priority descending, then by most-recent date descending. The date
# fallback to datetime.min keeps ordering deterministic when a project has no
# timestamp metadata.
# Wrapped in tuple() to prevent callers from mutating the canonical collection.
PROJECTS_SORTED = tuple(
    sorted(
        _PROJECTS,
        key=lambda p: (p.priority, p.last_updated or p.created_date or datetime.min),
        reverse=True,
    )
)


# ========================================================================
# ABOUT ME
# ========================================================================
ABOUT_ME = AboutMe(
    name='Justin P. Lyons',
    title='IT Manager | Automation & Full-Stack Builder',
    bio=(
        'IT Manager with AS & BS in Computer Science. I build tools that automate '
        'repetitive work — pricing and vendor data, message and photo archives, '
        'video and market-data pipelines — and the dashboards and infrastructure '
        'that run them. Mobile development is where I started; automation and '
        'full-stack tools are where most of my recent work lives.'
    ),
    profile_image='images/profile.svg',
    badges=['AS & BS in CS', 'Automation', 'Full-Stack'],
    highlights=[
        'Builds automation for real operations: store, contracting, and personal archives',
        'Ships tested, documented tools with CI — not just demos',
        'Runs a homelab stack (Unraid, Docker) for media, backups, and automation',
        'Background in mobile development (Android, iOS) and full-stack web',
    ],
    # No percentage skill bars: they were never rendered, and a self-assigned
    # 90 vs 88 proves nothing. The tool groups and the shipped projects below
    # are the evidence instead.
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

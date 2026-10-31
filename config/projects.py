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

from config.models import AboutMe, GlossaryEntry, ToolGroup

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

# ========================================================================
# PROJECT THUMBNAILS
# ========================================================================
# Card thumbnails, by repo name. Only mapped repos show a thumbnail;
# every other card renders exactly as before, with no placeholder box.
# The first four files are real screenshots from each repo's own README
# on main (verified 2026-10-30), copied into static/ so the card never
# hotlinks a README asset that could move. A fifth candidate,
# gas-auditor's docs/demo.gif, was dropped: the README references it,
# but the file is not on main (raw.githubusercontent returns 404), so
# it is not a verified image. The eight Pages entries are viewport
# screenshots of each repo's live Pages landing page, shot 2026-10-30
# with headless Chrome (intranet-dashboard in demo mode, godaddy with
# its sample data loaded, json-insight with a pasted sample analysed);
# re-shoot them if a landing page changes materially, since a
# screenshot freezes the page at shoot time. Add a repo here only
# with a verified screenshot.
PROJECT_THUMBNAILS = {
    'voxel-portfolio': 'images/project-thumbs/voxel-portfolio.png',
    'photo-stitcher': 'images/project-thumbs/photo-stitcher.gif',
    'sms-toolkit': 'images/project-thumbs/sms-toolkit.png',
    'floorplan-studio': 'images/project-thumbs/floorplan-studio.svg',
    'intranet-dashboard': 'images/project-thumbs/intranet-dashboard.png',
    'godaddy-billing-analyzer': 'images/project-thumbs/godaddy-billing-analyzer.png',
    'landscape-manager': 'images/project-thumbs/landscape-manager.png',
    'apps-script-samples': 'images/project-thumbs/apps-script-samples.png',
    'json-insight': 'images/project-thumbs/json-insight.png',
    'ngo-eval-webapp': 'images/project-thumbs/ngo-eval-webapp.png',
    'gsa-mas-offer-checklist': 'images/project-thumbs/gsa-mas-offer-checklist.png',
    'ss-space_marine_master_crafted': 'images/project-thumbs/ss-space_marine_master_crafted.png',
}

# ========================================================================
# RETRO TOP 8 SHOWCASE
# ========================================================================
# Curated showcase for retro's Top 8 grid, not "most recently updated":
# recency churned with every push and surfaced modernized old repos
# instead of the work the portfolio is meant to lead with. Retro fills
# from recent repos only if a showcase repo is missing, so the grid
# still reaches 8. Curation lives here (not inline in retro.html) so
# both the list and the rule for filling it change in one place.
RETRO_SHOWCASE = [
    'repo-sync',
    'gas-auditor',
    'photo-stitcher',
    'voxel-portfolio',
    'sms-toolkit',
    'gsa-vendor-toolkit',
    'kalshi-recorder',
    'gsa-fcp-toolkit',
]

# ========================================================================
# GLOSSARY
# ========================================================================
# One definition per Tools & Tech pill, exactly as drafted and approved
# 2026-10-28. Every pill in ABOUT_ME.tool_groups must have an entry here
# (a test enforces it), and every URL was verified to return 200 on
# 2026-10-28. Team Building and Mentorship have no official source, so
# their entries carry no URL and their modals show the definition only.
# Definitions describe the term itself; they make no claim about how
# the term is used in any project.
GLOSSARY: dict[str, GlossaryEntry] = {
    'Python': GlossaryEntry(
        'A general-purpose programming language known for readable syntax '
        'and a large ecosystem, widely used for automation, data work, and '
        'web backends.',
        'https://www.python.org/',
    ),
    'JavaScript': GlossaryEntry(
        'The programming language of the web browser, used to make web '
        'pages interactive and, with Node.js, to write server-side code.',
        'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
    ),
    'TypeScript': GlossaryEntry(
        'A typed superset of JavaScript that adds static type checking and '
        'compiles down to plain JavaScript.',
        'https://www.typescriptlang.org/',
    ),
    'Java': GlossaryEntry(
        'A general-purpose, object-oriented language designed to run on many '
        'platforms via the Java Virtual Machine; long used for enterprise '
        'and Android development.',
        'https://dev.java/',
    ),
    'Kotlin': GlossaryEntry(
        "A modern language for the Java Virtual Machine, and Google's "
        'preferred language for Android development, designed to be more '
        'concise and safer than Java.',
        'https://kotlinlang.org/',
    ),
    'Swift': GlossaryEntry(
        "Apple's programming language for iOS, macOS, and other Apple "
        'platforms, designed as a safer, faster successor to Objective-C.',
        'https://developer.apple.com/swift/',
    ),
    'Flask': GlossaryEntry(
        'A lightweight Python web framework for building web applications '
        'and APIs, providing the core tools and leaving the rest to '
        'extensions.',
        'https://flask.palletsprojects.com/',
    ),
    'GitHub Actions': GlossaryEntry(
        "GitHub's built-in automation service for running tests, builds, "
        'and deployments in response to events like pushes and pull '
        'requests.',
        'https://github.com/features/actions',
    ),
    'Playwright': GlossaryEntry(
        'A library for automating web browsers, used for end-to-end testing '
        'and for driving pages in a real browser.',
        'https://playwright.dev/',
    ),
    'Pandas': GlossaryEntry(
        'A Python library for working with tabular data: loading, cleaning, '
        'analyzing, and reshaping datasets.',
        'https://pandas.pydata.org/',
    ),
    'SQLite': GlossaryEntry(
        'A small, self-contained SQL database engine that stores an entire '
        'database in a single file, with no separate server process.',
        'https://www.sqlite.org/',
    ),
    'Parquet': GlossaryEntry(
        'A columnar file format for efficiently storing large datasets, '
        'widely used in data pipelines and analytics.',
        'https://parquet.apache.org/',
    ),
    'Android': GlossaryEntry(
        "Google's operating system for phones and tablets, with apps "
        'typically built in Kotlin or Java using Android Studio.',
        'https://developer.android.com/',
    ),
    'iOS': GlossaryEntry(
        "Apple's operating system for iPhone and iPad, with apps typically "
        'built in Swift using Xcode.',
        'https://developer.apple.com/ios/',
    ),
    'Flutter': GlossaryEntry(
        "Google's UI toolkit for building apps for mobile, web, and desktop "
        'from a single Dart codebase.',
        'https://flutter.dev/',
    ),
    'React Native': GlossaryEntry(
        "Meta's framework for building native mobile apps with JavaScript "
        'and React, sharing code between iOS and Android.',
        'https://reactnative.dev/',
    ),
    'Docker': GlossaryEntry(
        'A platform for packaging software and its dependencies into '
        'isolated containers that run consistently across machines.',
        'https://www.docker.com/',
    ),
    'Unraid': GlossaryEntry(
        'An operating system for home servers and network-attached storage, '
        'built around flexible drive pooling, Docker, and virtual machines.',
        'https://unraid.net/',
    ),
    'AWS': GlossaryEntry(
        "Amazon's cloud platform, providing on-demand computing, storage, "
        'databases, and other infrastructure services over the internet.',
        'https://aws.amazon.com/',
    ),
    'Firebase': GlossaryEntry(
        "Google's platform for building web and mobile apps, providing "
        'hosting, databases, authentication, and other backend services.',
        'https://firebase.google.com/',
    ),
    'Team Building': GlossaryEntry(
        'The practice of helping a group of people work well together, '
        'through shared goals, trust, and clear roles.'
    ),
    'Agile': GlossaryEntry(
        'An approach to software work built on short iterations, working '
        'software, and responding to change, as set out in the Agile '
        'Manifesto.',
        'https://agilemanifesto.org/',
    ),
    'Project Management': GlossaryEntry(
        'The planning, coordination, and tracking of work to deliver a '
        'defined outcome on time and within scope.',
        'https://www.pmi.org/',
    ),
    'Mentorship': GlossaryEntry(
        'Guiding a less experienced person by sharing knowledge, feedback, '
        'and perspective as they develop their skills.'
    ),
    'Git': GlossaryEntry(
        'A distributed version-control system for tracking changes to files '
        'and coordinating work across people and machines.',
        'https://git-scm.com/',
    ),
    'GitHub': GlossaryEntry(
        'A hosting platform for Git repositories, adding collaboration '
        'tools such as pull requests, issues, and Actions automation.',
        'https://github.com/',
    ),
    'Jira': GlossaryEntry(
        "Atlassian's issue- and project-tracking tool, commonly used to "
        'plan sprints, track work, and manage software delivery.',
        'https://www.atlassian.com/software/jira',
    ),
}


# ========================================================================
# ROLE DEFINITIONS
# ========================================================================
# Definitions for the three role pills under the name in the sidebar,
# exactly as drafted and approved 2026-10-29. Like Team Building and
# Mentorship, job titles have no official source, so these entries
# carry no URL and their modals show the definition only. Each entry
# states what the role is, then what it means in this portfolio's work.
ROLE_DEFINITIONS: dict[str, GlossaryEntry] = {
    'IT Manager': GlossaryEntry(
        "Directs an organization's IT infrastructure and technology "
        'solutions: support, onboarding, access, and the systems teams '
        'rely on day to day. At Millennium Partners, that means IT '
        'support for the headquarters and overseas field offices, '
        'onboarding and SharePoint access, and technical input on '
        'international projects and proposals.'
    ),
    'Automation Engineer': GlossaryEntry(
        'Builds software that replaces repetitive manual work: scripts '
        'and pipelines that collect, transform, and move data without '
        'someone doing it by hand. His tools automate GSA pricing and '
        'vendor data, message and photo archives, and video and '
        'market-data pipelines.'
    ),
    'Full-Stack Developer': GlossaryEntry(
        'Works across the whole of a web application: the user-facing '
        'interface, the server logic behind it, and the data it stores. '
        'His stack here is Flask and Jinja2 on the server with Tailwind '
        'on the front end, plus Android and iOS apps in Kotlin, Java, '
        'and Swift.'
    ),
}

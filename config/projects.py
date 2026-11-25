#!/usr/bin/env python3
"""
About-me metadata for the portfolio.

Project data no longer lives here: the GSA MAS Checklist and Schedule Maker
were removed from this repo (they may become standalone projects later),
the /projects page was removed with them, and project listings now come
from GitHub — the homepage Projects tab loads repos.json (refreshed by
scripts/fetch_repos.py in CI) with a live GitHub API fallback, and retro's Top 8
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
        'IT Manager with AS & BS in Computer Science, with weight in Mobile '
        'Application Development. I build tools that automate repetitive work — '
        'GSA schedule pricing and vendor data, message and photo archives, '
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
# with a verified screenshot. floorplan-studio's demo.svg re-copied
# 2026-11-08: the shipped copy was the Oct 28 portrait render, the
# repo's current file is the Nov 1 landscape (1100x850pt) render of
# the rebuilt sample plan. Note: the floorplan-studio README also
# references docs/assets/editor-hero.png and draw-export-render.gif,
# but both 404 on main as of 2026-11-08 — a floorplan-studio repo
# issue, not fixed here.
#
# Second batch, 2026-11-07 (19 more, 31 total): four more README shots,
# all verified 200 on raw.githubusercontent that day
# (achievement-trackers docs/screenshots/tracker-dark.png,
# profileforge assets/screenshots/portfolio-site.png,
# workspace-monitor docs/assets/home-dashboard.png,
# product-lookup-poc docs/assets/web-frontend.png — that last one is
# the top 1280x720 of a 1280x3400 full-page capture, cropped so the
# card shows the hero instead of a sliver); plus fifteen Pages shots,
# 1280x520 headless Chrome of each live landing page
# (face-stretch-playground, web-mtg-draft, web-conway-game-of-life,
# gas-auditor, dirt-bike-ghost-racer, number-chomper, snoodle-pop,
# fuzzle, android-automations, web-privacy-export-viewer, pdf-toolkit,
# tech6-cv-generator, video-optimizer-suite, walgreens-photo-prints,
# windows-sandbox-toolkit). Plus six more Pages shots, 1280x520, for
# the Websites tab (gmail-filter-builder, voice-generator, web-backtalk,
# web-typing-trainer, whenwhere-biz-main-site, whenwhere-drone-light-shows)
# — every repo with a live site now has a thumbnail. web-mtg-draft's shot shows the set list
# still loading from Scryfall — the sandbox capture caught the first
# paint; the list loads on a real browser. Still no thumbnail for the
# CLI/library repos (kalshi-recorder, repo-sync, gsa-vendor-toolkit,
# ...): nothing visual to show, and no image is faked.
PROJECT_THUMBNAILS = {
    'voxel-portfolio': 'images/project-thumbs/voxel-portfolio.png',
    'photo-stitcher': 'images/project-thumbs/photo-stitcher.gif',
    'sms-toolkit': 'images/project-thumbs/sms-toolkit.png',
    'floorplan-studio': 'images/project-thumbs/floorplan-studio.png',
    'intranet-dashboard': 'images/project-thumbs/intranet-dashboard.png',
    'godaddy-billing-analyzer': 'images/project-thumbs/godaddy-billing-analyzer.png',
    'landscape-manager': 'images/project-thumbs/landscape-manager.png',
    'apps-script-samples': 'images/project-thumbs/apps-script-samples.png',
    'json-insight': 'images/project-thumbs/json-insight.png',
    'ngo-eval-webapp': 'images/project-thumbs/ngo-eval-webapp.png',
    'gsa-mas-offer-checklist': 'images/project-thumbs/gsa-mas-offer-checklist.png',
    'ss-space_marine_master_crafted': 'images/project-thumbs/ss-space_marine_master_crafted.png',
    'achievement-trackers': 'images/project-thumbs/achievement-trackers.png',
    'profileforge': 'images/project-thumbs/profileforge.png',
    'workspace-monitor': 'images/project-thumbs/workspace-monitor.png',
    'product-lookup-poc': 'images/project-thumbs/product-lookup-poc.png',
    'face-stretch-playground': 'images/project-thumbs/face-stretch-playground.png',
    'web-mtg-draft': 'images/project-thumbs/web-mtg-draft.png',
    'web-conway-game-of-life': 'images/project-thumbs/web-conway-game-of-life.png',
    'gas-auditor': 'images/project-thumbs/gas-auditor.png',
    'dirt-bike-ghost-racer': 'images/project-thumbs/dirt-bike-ghost-racer.png',
    'number-chomper': 'images/project-thumbs/number-chomper.png',
    'snoodle-pop': 'images/project-thumbs/snoodle-pop.png',
    'fuzzle': 'images/project-thumbs/fuzzle.png',
    'android-automations': 'images/project-thumbs/android-automations.png',
    'web-privacy-export-viewer': 'images/project-thumbs/web-privacy-export-viewer.png',
    'pdf-toolkit': 'images/project-thumbs/pdf-toolkit.png',
    'tech6-cv-generator': 'images/project-thumbs/tech6-cv-generator.png',
    'video-optimizer-suite': 'images/project-thumbs/video-optimizer-suite.png',
    'walgreens-photo-prints': 'images/project-thumbs/walgreens-photo-prints.png',
    'windows-sandbox-toolkit': 'images/project-thumbs/windows-sandbox-toolkit.png',
    'gmail-filter-builder': 'images/project-thumbs/gmail-filter-builder.png',
    'voice-generator': 'images/project-thumbs/voice-generator.png',
    'web-backtalk': 'images/project-thumbs/web-backtalk.png',
    'web-typing-trainer': 'images/project-thumbs/web-typing-trainer.png',
    'whenwhere-biz-main-site': 'images/project-thumbs/whenwhere-biz-main-site.png',
    'whenwhere-drone-light-shows': 'images/project-thumbs/whenwhere-drone-light-shows.png',
    'whenwhere-biz-coming-soon': 'images/project-thumbs/whenwhere-biz-coming-soon.png',
}

# Wide thumbnails: repos whose card image is a desktop + mobile
# side-by-side composite (see below), rendered in the wider 9/4 thumb
# box instead of the standard 16:9 one. A repo lands here only with
# its composite file above and a mapping entry in PROJECT_THUMBNAILS.
# Captures are shot with prefers-color-scheme: dark, so a site with a
# dark variant shows dark and a light-only site renders its normal
# look — that is the convention, not a per-site choice. (Dark is the
# right default here: the site itself is dark-first and most of these
# pages have a dark variant; a light shot of a dark-capable page
# reads as the wrong theme.) Re-shoot a composite if its landing page
# changes materially, since a screenshot freezes the page at shoot time.
# 2026-11-25 pilot: whenwhere-biz-coming-soon — desktop 1920x1080 and
# mobile 390x844 viewport shots of the live page, composited at equal
# height with a 24px transparent gap (2443x1080 source, half-scaled
# to 1221x540 for the shipped file, ~2.26:1, no cropping). The page
# fits exactly one viewport at both sizes, so the shots are the whole
# page, not just the hero. First shot in light, corrected the same
# day to the dark variant (the page's Night & Gold theme has a real
# dark mode — verified by pixel-diff, mean delta ~219/255 — and the
# light shot showed the cream version). Rollout the same day: all 36
# Websites-tab cards are wide composites now, shot the same way (dark
# captures, same composite, half-scaled; ~10 MB total for the 36).
# floorplan-studio's mapping switched svg -> png with the rollout:
# the svg was the repo's own demo render, the png is the live editor.
# Still no thumbnail for
# enonymous1 and jpl-dev (both point at justinlyons.dev) — the
# "every repo with a live site has a thumbnail" line above is stale.
WIDE_THUMBNAILS = frozenset(
    {
        'achievement-trackers',
        'android-automations',
        'apps-script-samples',
        'dirt-bike-ghost-racer',
        'face-stretch-playground',
        'floorplan-studio',
        'fuzzle',
        'gas-auditor',
        'gmail-filter-builder',
        'godaddy-billing-analyzer',
        'gsa-mas-offer-checklist',
        'intranet-dashboard',
        'json-insight',
        'landscape-manager',
        'ngo-eval-webapp',
        'number-chomper',
        'pdf-toolkit',
        'product-lookup-poc',
        'profileforge',
        'sms-toolkit',
        'snoodle-pop',
        'ss-space_marine_master_crafted',
        'tech6-cv-generator',
        'video-optimizer-suite',
        'voice-generator',
        'walgreens-photo-prints',
        'web-backtalk',
        'web-conway-game-of-life',
        'web-mtg-draft',
        'web-privacy-export-viewer',
        'web-typing-trainer',
        'whenwhere-biz-coming-soon',
        'whenwhere-biz-main-site',
        'whenwhere-drone-light-shows',
        'windows-sandbox-toolkit',
        'workspace-monitor',
    }
)

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

# Pokémon GO trainer card: the sidebar's Poké Ball icon opens a modal
# with the trainer name and friend code (the About highlights used to
# carry this line; it moved to the icon on 2026-11-21). The code is
# shown spaced for reading; the modal's Copy button copies digits only,
# which is what the game accepts.
POKEMON_GO = {'trainer': 'enonymous1', 'friend_code': '8456 7104 2978'}


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

# ========================================================================
# LOCATION FACTS
# ========================================================================
# Facts about Fredericksburg, VA for the sidebar location modal, drafted
# 2026-10-31 and checked against public sources before shipping. Three
# of the supplied drafts were corrected in that check, and the
# corrections are the shipped wording, so do not "fix" them back:
# - The tunnels' purpose is unconfirmed (city tourism copy calls it
#   speculation), so the entry frames the goods-moving claim as local
#   lore instead of stating it as fact.
# - The Embrey Dam marker gives 1,070 feet overall with a 770-foot
#   spillway, so the entry carries no length at all rather than the
#   supplied 770-foot total.
# - Planet Novak Rewind opened in July 2026 (no longer "launching"),
#   with 25 cabinets per the opening coverage, not 24, and the cabinets
#   run the original games on modern hardware, not native hardware.
LOCATION_FACTS = [
    {
        'title': 'The birth of the power chord',
        'body': (
            'At a sock hop at the Fredericksburg Armory, Link Wray '
            "improvised 'Rumble', the power chords and distortion that "
            'became modern rock guitar.'
        ),
    },
    {
        'title': 'The blueprint for the First Amendment',
        'body': (
            'In January 1777, Thomas Jefferson met with his advisory '
            'committee here to draft the Bill for Establishing Religious '
            'Freedom, later the Virginia Statute for Religious Freedom '
            'and the model for the First Amendment.'
        ),
    },
    {
        'title': 'The first Civil Rights stop',
        'body': (
            'Fredericksburg was the first stop of the Freedom Rides on '
            'May 4, 1961, as the riders traveled south from Washington, '
            'D.C. to challenge segregated bus terminals.'
        ),
    },
    {
        'title': 'A massive crossing to freedom',
        'body': (
            'In 1862, an estimated 10,000 enslaved people freed '
            'themselves by crossing the Rappahannock River to Union lines.'
        ),
    },
    {
        'title': 'Royal street names',
        'body': (
            'Named in 1728 for Frederick, Prince of Wales, the town '
            'named its streets after members of the royal family.'
        ),
    },
    {
        'title': 'The true Washington home',
        'body': (
            'George Washington moved to Ferry Farm, across the '
            'Rappahannock from Fredericksburg, in 1738 at age six, and '
            'spent most of his boyhood there.'
        ),
    },
    {
        'title': '19th-century big data',
        'body': (
            'Matthew Fontaine Maury, born in Spotsylvania County just '
            "outside Fredericksburg, aggregated thousands of ships' logs "
            'to chart ocean currents and winds around the world, an early '
            "form of crowdsourced data. He was known as the 'Pathfinder "
            "of the Seas'."
        ),
    },
    {
        'title': 'The hydroelectric shift',
        'body': (
            'In 1909-10, the Fredericksburg Water Power Company built '
            'the Ambursen-type Embrey Dam across the Rappahannock to '
            'generate hydroelectric power. It powered the region into '
            'the 1960s and was removed in 2004.'
        ),
    },
    {
        'title': 'The mystery tunnels',
        'body': (
            'Brick-lined passages run beneath downtown near the old '
            'river docks, with torch smudges still visible on their '
            'walls. Their purpose is unconfirmed; local lore says they '
            'moved goods from the docks to shops out of sight.'
        ),
    },
    {
        'title': 'The local maker hub',
        'body': (
            "The Central Rappahannock Regional Library's IdeaSpace, on "
            'Princess Anne Street, is a community fabrication lab with '
            '3D printers, a laser cutter, and an AV booth for prototyping '
            'and digital design.'
        ),
    },
    {
        'title': 'The 2026 arcade expansion',
        'body': (
            'Planet Novak Rewind opened at Spotsylvania Towne Centre in '
            'summer 2026, with 25 retro cabinets, Pac-Man, Donkey Kong, '
            'Mortal Kombat, and more, running the original games on '
            'modern hardware.'
        ),
    },
]

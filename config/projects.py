#!/usr/bin/env python3
"""
Project Repository

Static portfolio metadata used by the build pipeline and static portfolio
templates. This module defines the project catalog and a deterministic sort
order, so the site can render without any runtime backend dependencies.
"""

from datetime import datetime
from config.models import ProjectCategory, ProjectData, ProjectLinks, ProjectImage, ProjectStatus


# ========================================================================
# STATIC PROJECT DEFINITIONS
# ========================================================================
# The canonical project catalog. Each ProjectData object should represent a
# static portfolio entry that can be rendered at build time.
PROJECTS = [
    ProjectData(
        id="gsa_mas_checklist",
        title="Interactive GSA MAS New Offeror Checklist",
        description=(
            "A comprehensive interactive checklist for GSA Multiple Award "
            "Schedule (MAS) offer preparation. Streamlines the complex federal "
            "contracting process with an intuitive, step-by-step interface."
        ),
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.WEB_APP,
        features=[
            "Step-by-step checklist validation with progress tracking",
            "SINs selection with advanced filtering and search",
            "Rich text notes management with Quill editor",
            "Complete data export/import capabilities (JSON/Excel)",
            "Dark/light theme support with system preference detection",
            "Local storage persistence for work-in-progress",
            "Responsive design for desktop and mobile use",
        ],
        tech_stack=[
            "Flask",
            "JavaScript",
            "Quill.js",
            "CSS Grid",
            "Local Storage",
            "JSON",
            "Excel Export",
        ],
        tags=["government", "contracting", "checklist", "productivity", "flask"],
        route="gsa_mas_checklist.gsa_mas_checklist",
        links=ProjectLinks(
            github="https://github.com/enonymous1/jpl-dev",
            documentation=(
                "https://github.com/enonymous1/jpl-dev/blob/main/projects/"
                "gsa_mas_checklist/README.md"
            ),
        ),
        images=[
            ProjectImage(
                filename="gsa_checklist_hero.svg",
                alt_text=(
                    "GSA MAS Checklist main interface showing checklist items "
                    "and progress"
                ),
                caption="Main checklist interface with progress tracking and theme toggle",
                is_hero=True,
                is_thumbnail=True,
            )
        ],
        created_date=datetime(2025, 6, 1),
        last_updated=datetime(2025, 7, 11),
        priority=10,
    ),
    ProjectData(
        id="schedule_maker",
        title="Interactive Schedule Maker",
        description=(
            "A comprehensive schedule creation and management tool with "
            "drag-and-drop functionality, multiple view modes, and export "
            "capabilities."
        ),
        status=ProjectStatus.DEVELOPMENT,
        category=ProjectCategory.WEB_APP,
        features=[
            "Multiple view modes (Day, Week, Month)",
            "Drag-and-drop event creation and editing",
            "Color-coded event categorization",
            "Real-time schedule conflict detection",
            "Export to JSON and calendar formats",
            "Local storage for data persistence",
            "Responsive design for all devices",
        ],
        tech_stack=["Flask", "JavaScript ES6+", "CSS Grid", "Local Storage", "Canvas API"],
        tags=["productivity", "scheduling", "calendar", "time-management", "flask"],
        route="schedule_maker.schedule_maker",
        links=ProjectLinks(
            github="https://github.com/enonymous1/jpl-dev",
            documentation=(
                "https://github.com/enonymous1/jpl-dev/blob/main/projects/"
                "schedule_maker/README.md"
            ),
        ),
        images=[
            ProjectImage(
                filename="schedule_maker_hero.svg",
                alt_text=(
                    "Schedule Maker main interface with weekly view and event creation"
                ),
                caption="Interactive schedule interface with multiple view modes",
                is_hero=True,
                is_thumbnail=True,
            )
        ],
        created_date=datetime(2025, 7, 11),
        last_updated=datetime(2025, 7, 11),
        priority=8,
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
PROJECTS_SORTED = sorted(
    PROJECTS,
    key=lambda p: (
        p.priority,
        p.last_updated or p.created_date or datetime.min
    ),
    reverse=True,
)
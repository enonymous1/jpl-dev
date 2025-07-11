#!/usr/bin/env python3
"""
Project Data Repository

Central repository containing all project definitions for the portfolio site.
This file contains the actual project data using the models defined in config/models.py.

Author: JPL Development  
Date: July 2025
"""

from datetime import datetime
from config.models import ProjectData, ProjectStatus, ProjectCategory, ProjectImage, ProjectLinks


# ============================================================================
# PROJECT DEFINITIONS
# ============================================================================

PROJECTS = [
    ProjectData(
        id="gsa_mas_checklist",
        title="Interactive GSA MAS New Offeror Checklist",
        description="A comprehensive interactive checklist for GSA Multiple Award Schedule (MAS) offer preparation. Streamlines the complex federal contracting process with an intuitive, step-by-step interface.",
        status=ProjectStatus.ACTIVE,
        category=ProjectCategory.WEB_APP,
        features=[
            "Step-by-step checklist validation with progress tracking",
            "SINs selection with advanced filtering and search",
            "Rich text notes management with Quill editor",
            "Complete data export/import capabilities (JSON/Excel)",
            "Dark/light theme support with system preference detection",
            "Local storage persistence for work-in-progress",
            "Responsive design for desktop and mobile use"
        ],
        tech_stack=["Flask", "JavaScript", "Quill.js", "CSS Grid", "Local Storage", "JSON", "Excel Export"],
        tags=["government", "contracting", "checklist", "productivity", "flask"],
        route="gsa_mas_checklist.gsa_mas_checklist",
        links=ProjectLinks(
            github="https://github.com/enonymous1/jpl-dev",
            documentation="https://github.com/enonymous1/jpl-dev/blob/main/projects/gsa_mas_checklist/README.md"
        ),
        images=[
            ProjectImage(
                filename="gsa_checklist_hero.svg",
                alt_text="GSA MAS Checklist main interface showing checklist items and progress",
                caption="Main checklist interface with progress tracking and theme toggle",
                is_hero=True,
                is_thumbnail=True
            ),
            # ProjectImage(
            #     filename="gsa_checklist_sins.png", 
            #     alt_text="SINs selection interface with filtering options",
            #     caption="Advanced SINs selection with real-time filtering"
            # ),
            # ProjectImage(
            #     filename="gsa_checklist_notes.png",
            #     alt_text="Rich text notes editor with formatting options",
            #     caption="Integrated notes management with Quill rich text editor"
            # ),
            # ProjectImage(
            #     filename="gsa_checklist_export.png",
            #     alt_text="Data export interface showing JSON and Excel options",
            #     caption="Flexible export options for data portability"
            # )
        ],
        created_date=datetime(2025, 6, 1),
        last_updated=datetime(2025, 7, 11),
        priority=10  # Highest priority for featured placement
    ),
    
    ProjectData(
        id="schedule_maker",
        title="Interactive Schedule Maker",
        description="A comprehensive schedule creation and management tool with drag-and-drop functionality, multiple view modes, and export capabilities.",
        status=ProjectStatus.DEVELOPMENT,
        category=ProjectCategory.WEB_APP,
        features=[
            "Multiple view modes (Day, Week, Month)",
            "Drag-and-drop event creation and editing",
            "Color-coded event categorization",
            "Real-time schedule conflict detection",
            "Export to JSON and calendar formats",
            "Local storage for data persistence",
            "Responsive design for all devices"
        ],
        tech_stack=["Flask", "JavaScript ES6+", "CSS Grid", "Local Storage", "Canvas API"],
        tags=["productivity", "scheduling", "calendar", "time-management", "flask"],
        route="schedule_maker.schedule_maker",
        links=ProjectLinks(
            github="https://github.com/enonymous1/jpl-dev",
            documentation="https://github.com/enonymous1/jpl-dev/blob/main/projects/schedule_maker/README.md"
        ),
        images=[
            ProjectImage(
                filename="schedule_maker_hero.svg",
                alt_text="Schedule Maker main interface with weekly view and event creation",
                caption="Interactive schedule interface with multiple view modes",
                is_hero=True,
                is_thumbnail=True
            )
        ],
        created_date=datetime(2025, 7, 11),
        last_updated=datetime(2025, 7, 11),
        priority=8  # High priority for featured placement
    ),
    
    # Template for future projects with all options:
    # ProjectData(
    #     id="example_project",
    #     title="Example Project Title",
    #     description="A comprehensive description of what this project does and why it's valuable...",
    #     status=ProjectStatus.DEVELOPMENT,
    #     category=ProjectCategory.WEB_APP,
    #     features=[
    #         "Feature 1 with detailed description",
    #         "Feature 2 explaining user benefits", 
    #         "Feature 3 highlighting technical innovation"
    #     ],
    #     tech_stack=["Technology 1", "Technology 2", "Framework 3"],
    #     tags=["tag1", "tag2", "category"],
    #     route="blueprint.route_name",  # For internal Flask routes
    #     external_url="https://example.com",  # For external projects
    #     links=ProjectLinks(
    #         github="https://github.com/user/repo",
    #         demo="https://demo.example.com",
    #         live_site="https://live.example.com",
    #         documentation="https://docs.example.com",
    #         download="https://releases.example.com"
    #     ),
    #     images=[
    #         ProjectImage(
    #             filename="project_hero.jpg",
    #             alt_text="Main project interface screenshot", 
    #             caption="Overview of the main application interface",
    #             is_hero=True,
    #             is_thumbnail=True,
    #             width=1200,
    #             height=800
    #         ),
    #         ProjectImage(
    #             filename="project_feature1.jpg",
    #             alt_text="Feature 1 in action",
    #             caption="Detailed view of the first major feature"
    #         )
    #     ],
    #     created_date=datetime(2025, 7, 15),
    #     last_updated=datetime(2025, 7, 15),
    #     priority=5
    # ),
]


# ============================================================================
# COMPUTED DATA
# ============================================================================

# Sort projects by priority (descending) then by last_updated (descending)
PROJECTS_SORTED = sorted(
    PROJECTS, 
    key=lambda p: (p.priority, p.last_updated), 
    reverse=True
)

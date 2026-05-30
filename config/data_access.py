#!/usr/bin/env python3
"""
Project Data Access Layer

Utilities for accessing and filtering static project metadata during build
and static runtime. This module operates on the in-memory project repository
and is intended for use in a static portfolio generation pipeline.
"""

from collections import Counter
from functools import lru_cache
from typing import Dict, List, Optional

from config.models import ProjectData, ProjectStatus
from config.projects import PROJECTS_SORTED


@lru_cache(maxsize=None)
def get_all_projects() -> tuple[ProjectData, ...]:
    """
    Return a fixed, immutable tuple of all projects.

    Returning a tuple prevents callers from mutating the canonical project
    collection that is cached for repeated lookups.
    """
    return tuple(PROJECTS_SORTED)


@lru_cache(maxsize=None)
def get_active_projects() -> List[ProjectData]:
    """
    Return all projects whose status is ProjectStatus.ACTIVE.

    This slice is commonly used in the UI and is cached because the underlying
    portfolio data is static during site generation.
    """
    return [project for project in PROJECTS_SORTED if project.status == ProjectStatus.ACTIVE]


@lru_cache(maxsize=None)
def get_featured_projects() -> List[ProjectData]:
    """
    Return projects that should be highlighted as featured.

    Featured projects are those explicitly marked FEATURED or those with a
    priority of 8 or higher, which supports both explicit and implicit
    promotion rules.
    """
    return [
        project for project in PROJECTS_SORTED
        if project.status == ProjectStatus.FEATURED or project.priority >= 8
    ]


_PROJECTS_BY_ID = {project.id: project for project in PROJECTS_SORTED}


@lru_cache(maxsize=None)
def get_project_by_id(project_id: str) -> Optional[ProjectData]:
    """
    Return a project by its unique identifier.

    Args:
        project_id: The unique project ID to look up.

    Returns:
        The matching ProjectData, or None if no project matches.
    """
    return _PROJECTS_BY_ID.get(project_id)


@lru_cache(maxsize=None)
def get_projects_by_category(category: str) -> List[ProjectData]:
    """
    Return projects that belong to a specific category.

    Args:
        category: The category identifier to filter by.

    Returns:
        A list of matching projects.
    """
    normalized_category = category.strip().lower()
    return [
        project for project in PROJECTS_SORTED
        if project.category and project.category.lower() == normalized_category
    ]


@lru_cache(maxsize=None)
def get_projects_by_tech(technology: str) -> List[ProjectData]:
    """
    Return projects that use a given technology.

    The match is case-insensitive, allowing UI filters to be tolerant of
    capitalization differences in metadata.
    """
    normalized_query = technology.strip().lower()
    return [
        project for project in PROJECTS_SORTED
        if normalized_query in {tech.strip().lower() for tech in project.tech_stack}
    ]


@lru_cache(maxsize=None)
def get_projects_by_tag(tag: str) -> List[ProjectData]:
    """
    Return projects that include the specified tag.

    Args:
        tag: The search tag to filter project tags.

    Returns:
        A list of matching projects.
    """
    normalized_tag = tag.lower()
    return [
        project for project in PROJECTS_SORTED
        if normalized_tag in [t.lower() for t in project.tags]
    ]


@lru_cache(maxsize=None)
def get_project_stats() -> Dict[str, int]:
    """
    Return aggregated portfolio statistics.

    This includes totals, active and featured counts, and breakdowns by
    project status and category.
    """
    stats = {
        'total_projects': len(PROJECTS_SORTED),
        'active_projects': len(get_active_projects()),
        'featured_projects': len(get_featured_projects()),
    }

    status_counts = Counter(project.status for project in PROJECTS_SORTED)
    category_counts = Counter(project.category for project in PROJECTS_SORTED if project.category)

    stats.update({f'status_{k}': v for k, v in status_counts.items()})
    stats.update({f'category_{k}': v for k, v in category_counts.items()})
    return stats


@lru_cache(maxsize=None)
def get_all_technologies() -> List[str]:
    """
    Return a sorted list of all unique technologies used by projects.

    Sorting keeps the output deterministic for UI rendering.
    """
    technologies = set()
    for project in PROJECTS_SORTED:
        technologies.update(project.tech_stack)
    return sorted(list(technologies))


@lru_cache(maxsize=None)
def get_all_tags() -> List[str]:
    """
    Return a sorted list of all unique tags used by projects.

    The resulting list is suitable for tag filter controls and navigation.
    """
    tags = set()
    for project in PROJECTS_SORTED:
        tags.update(project.tags)
    return sorted(list(tags))
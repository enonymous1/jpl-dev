#!/usr/bin/env python3
"""
Project Data Access Layer

Utilities for accessing and filtering static project metadata during build
and static runtime. This module operates on the in-memory project repository
and is intended for use in a static portfolio generation pipeline.
"""

from functools import lru_cache
from typing import Optional

from config.models import ProjectData
from config.projects import PROJECTS_SORTED


@lru_cache(maxsize=None)
def get_all_projects() -> tuple[ProjectData, ...]:
    """
    Return a fixed, immutable tuple of all projects.

    Returning a tuple prevents callers from mutating the canonical project
    collection that is cached for repeated lookups.
    """
    return tuple(PROJECTS_SORTED)


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
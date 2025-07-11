#!/usr/bin/env python3
"""
Project Data Access Layer

Provides utility functions for accessing and filtering project data.
This module serves as the interface between the data layer and the application.

Author: JPL Development
Date: July 2025
"""

from typing import List, Dict, Optional
from config.models import ProjectData, ProjectStatus, ProjectCategory
from config.projects import PROJECTS_SORTED


def get_all_projects() -> List[ProjectData]:
    """
    Get all projects sorted by priority and last updated date.
    
    Returns:
        List[ProjectData]: List of all project data objects, sorted
    """
    return PROJECTS_SORTED


def get_active_projects() -> List[ProjectData]:
    """
    Get only active projects.
    
    Returns:
        List[ProjectData]: List of active project data objects
    """
    return [project for project in PROJECTS_SORTED if project.status == ProjectStatus.ACTIVE]


def get_featured_projects() -> List[ProjectData]:
    """
    Get featured projects (status = featured or priority >= 8).
    
    Returns:
        List[ProjectData]: List of featured project data objects
    """
    return [
        project for project in PROJECTS_SORTED 
        if project.status == ProjectStatus.FEATURED or project.priority >= 8
    ]


def get_project_by_id(project_id: str) -> Optional[ProjectData]:
    """
    Get a specific project by its ID.
    
    Args:
        project_id (str): The unique identifier for the project
        
    Returns:
        Optional[ProjectData]: Project data object or None if not found
    """
    for project in PROJECTS_SORTED:
        if project.id == project_id:
            return project
    return None


def get_projects_by_category(category: str) -> List[ProjectData]:
    """
    Get projects by category.
    
    Args:
        category (str): The category to filter by
        
    Returns:
        List[ProjectData]: List of projects in the specified category
    """
    return [
        project for project in PROJECTS_SORTED 
        if project.category == category
    ]


def get_projects_by_tech(technology: str) -> List[ProjectData]:
    """
    Get projects that use a specific technology.
    
    Args:
        technology (str): The technology to filter by
        
    Returns:
        List[ProjectData]: List of projects using the specified technology
    """
    return [
        project for project in PROJECTS_SORTED 
        if technology.lower() in [tech.lower() for tech in project.tech_stack]
    ]


def get_projects_by_tag(tag: str) -> List[ProjectData]:
    """
    Get projects that have a specific tag.
    
    Args:
        tag (str): The tag to filter by
        
    Returns:
        List[ProjectData]: List of projects with the specified tag
    """
    return [
        project for project in PROJECTS_SORTED 
        if tag.lower() in [t.lower() for t in project.tags]
    ]


def get_project_stats() -> Dict[str, int]:
    """
    Get statistics about the project portfolio.
    
    Returns:
        Dict[str, int]: Statistics including counts by status, category, etc.
    """
    stats = {
        'total_projects': len(PROJECTS_SORTED),
        'active_projects': len(get_active_projects()),
        'featured_projects': len(get_featured_projects()),
    }
    
    # Count by status
    status_counts = {}
    for project in PROJECTS_SORTED:
        status_counts[project.status] = status_counts.get(project.status, 0) + 1
    stats.update({f'status_{k}': v for k, v in status_counts.items()})
    
    # Count by category  
    category_counts = {}
    for project in PROJECTS_SORTED:
        if project.category:
            category_counts[project.category] = category_counts.get(project.category, 0) + 1
    stats.update({f'category_{k}': v for k, v in category_counts.items()})
    
    return stats


def get_all_technologies() -> List[str]:
    """
    Get a list of all technologies used across projects.
    
    Returns:
        List[str]: Sorted list of unique technologies
    """
    technologies = set()
    for project in PROJECTS_SORTED:
        technologies.update(project.tech_stack)
    return sorted(list(technologies))


def get_all_tags() -> List[str]:
    """
    Get a list of all tags used across projects.
    
    Returns:
        List[str]: Sorted list of unique tags
    """
    tags = set()
    for project in PROJECTS_SORTED:
        tags.update(project.tags)
    return sorted(list(tags))

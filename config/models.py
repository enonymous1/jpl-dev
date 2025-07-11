#!/usr/bin/env python3
"""
Project Configuration Models

Defines the data structures and constants used for project management
throughout the portfolio application.

Author: JPL Development
Date: July 2025
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


class ProjectStatus:
    """Project status constants."""
    ACTIVE = "active"
    DEVELOPMENT = "development"  
    COMPLETED = "completed"
    ARCHIVED = "archived"
    FEATURED = "featured"  # For highlighting special projects


class ProjectCategory:
    """Project category constants."""
    WEB_APP = "web-app"
    TOOL = "tool"
    AUTOMATION = "automation"
    API = "api"
    LIBRARY = "library"
    GAME = "game"
    MOBILE = "mobile"
    DESKTOP = "desktop"


@dataclass
class ProjectImage:
    """
    Container for project image information.
    
    Supports multiple image types for different use cases.
    """
    filename: str
    alt_text: str
    caption: Optional[str] = None
    is_hero: bool = False  # Main project image
    is_thumbnail: bool = False  # For project cards
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class ProjectLinks:
    """Container for project-related links."""
    github: Optional[str] = None
    demo: Optional[str] = None
    live_site: Optional[str] = None
    documentation: Optional[str] = None
    download: Optional[str] = None


@dataclass 
class ProjectData:
    """
    Comprehensive container for project information.
    
    This dataclass provides a structured way to define project data with
    validation and easy access to project properties.
    """
    
    # Core information
    id: str
    title: str
    description: str
    status: str
    
    # Optional descriptive content
    features: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    # Routing and links
    route: Optional[str] = None
    external_url: Optional[str] = None
    links: Optional[ProjectLinks] = None
    
    # Media
    images: List[ProjectImage] = field(default_factory=list)
    
    # Metadata
    created_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    priority: int = 0  # For ordering (higher = more important)
    
    def __post_init__(self):
        """Set default dates if not provided."""
        if self.created_date is None:
            self.created_date = datetime.now()
        if self.last_updated is None:
            self.last_updated = datetime.now()
        if self.links is None:
            self.links = ProjectLinks()
    
    @property
    def hero_image(self) -> Optional[ProjectImage]:
        """Get the main hero image for the project."""
        for img in self.images:
            if img.is_hero:
                return img
        return self.images[0] if self.images else None
    
    @property
    def thumbnail_image(self) -> Optional[ProjectImage]:
        """Get the thumbnail image for project cards."""
        for img in self.images:
            if img.is_thumbnail:
                return img
        return self.hero_image
    
    @property
    def primary_link(self) -> Optional[str]:
        """Get the primary link for the project (route > live_site > demo > github)."""
        if self.route:
            return f"route:{self.route}"
        if self.external_url:
            return self.external_url
        if self.links.live_site:
            return self.links.live_site
        if self.links.demo:
            return self.links.demo
        if self.links.github:
            return self.links.github
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project data to dictionary for template rendering."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'features': self.features,
            'tech_stack': self.tech_stack,
            'status': self.status,
            'category': self.category,
            'tags': self.tags,
            'route': self.route,
            'external_url': self.external_url,
            'links': self.links,
            'images': self.images,
            'hero_image': self.hero_image,
            'thumbnail_image': self.thumbnail_image,
            'primary_link': self.primary_link,
            'created_date': self.created_date,
            'last_updated': self.last_updated,
            'priority': self.priority,
        }

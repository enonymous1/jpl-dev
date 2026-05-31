#!/usr/bin/env python3
"""
Project Configuration Models

Defines the data structures and constants used for project management
throughout the portfolio application.
"""

from datetime import datetime
from enum import Enum
import logging
from typing import Any
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


class ProjectStatus(str, Enum):
    """Project status constants used to classify portfolio items."""
    ACTIVE = "active"
    DEVELOPMENT = "development"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    FEATURED = "featured"


class ProjectCategory(str, Enum):
    """Project category constants for consistent filtering and display."""
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
    Container for project image metadata.

    The model supports multiple image roles so the frontend can choose the
    appropriate asset for hero display or thumbnails.
    """
    filename: str
    alt_text: str
    caption: str | None = None
    is_hero: bool = False
    is_thumbnail: bool = False
    width: int | None = None
    height: int | None = None


@dataclass
class ProjectLinks:
    """
    Container for a project's external links.

    Links are optional because some static portfolio entries may only need
    an internal route or a single destination.
    """
    github: str | None = None
    demo: str | None = None
    live_site: str | None = None
    documentation: str | None = None
    download: str | None = None


@dataclass
class ProjectData:
    """
    Comprehensive container for project information.

    This dataclass keeps the static portfolio schema consistent and provides
    convenience properties for derived display state.
    """
    id: str
    title: str
    description: str
    status: str

    features: list[str] = field(default_factory=list)
    tech_stack: list[str] = field(default_factory=list)
    category: str | None = None
    tags: list[str] = field(default_factory=list)

    route: str | None = None
    external_url: str | None = None
    links: ProjectLinks | None = None

    images: list[ProjectImage] = field(default_factory=list)

    created_date: datetime | None = None
    last_updated: datetime | None = None
    priority: int = 0

    def __post_init__(self):
        """
        Normalize related date fields without introducing runtime or build-time
        side effects.

        If one date is missing, the other date is reused so that downstream
        sorting and display logic always has a consistent datetime reference.
        """
        if self.created_date is None and self.last_updated is not None:
            self.created_date = self.last_updated
        if self.last_updated is None and self.created_date is not None:
            self.last_updated = self.created_date
        # C3a: warn when both dates are absent so the project silently sorts last
        if self.created_date is None and self.last_updated is None:
            logger.warning(
                "Project %r has no created_date or last_updated; "
                "it will sort to the bottom of all ordered listings.",
                self.id,
            )
        if self.links is None:
            self.links = ProjectLinks()
        # C1b: validate status against ProjectStatus enum at construction time
        try:
            self.status = ProjectStatus(self.status)
        except ValueError:
            valid = [s.value for s in ProjectStatus]
            raise ValueError(
                f"Invalid project status {self.status!r}. Must be one of: {valid}"
            ) from None

    @property
    def hero_image(self) -> ProjectImage | None:
        """
        Return the primary hero image for the project.

        This property is used by page templates that require a single prominent
        image asset.
        """
        for img in self.images:
            if img.is_hero:
                return img
        return self.images[0] if self.images else None

    @property
    def thumbnail_image(self) -> ProjectImage | None:
        """
        Return a thumbnail image for project cards.

        If no explicit thumbnail exists, fallback to the hero image to ensure
        the UI still displays a representative asset.
        """
        for img in self.images:
            if img.is_thumbnail:
                return img
        return self.hero_image

    @property
    def primary_link(self) -> str | None:
        """
        Return the most appropriate project link for navigation.

        The precedence is:
        1. internal route
        2. external URL
        3. live site
        4. demo
        5. GitHub repository
        """
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

    def to_dict(self) -> dict[str, Any]:
        """
        Convert project metadata into a plain dictionary for template rendering.

        The returned dictionary includes computed properties so templates can
        consume a uniform data shape without needing object access.
        """
        data = asdict(self)
        # C1d: asdict() already converts images list to List[dict]; use asdict() for
        # the computed properties too so the returned dict is a uniform plain-dict type.
        data["hero_image"] = asdict(self.hero_image) if self.hero_image else None
        data["thumbnail_image"] = asdict(self.thumbnail_image) if self.thumbnail_image else None
        data["primary_link"] = self.primary_link
        return data
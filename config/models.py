#!/usr/bin/env python3
"""
Profile models for the portfolio.

Only the AboutMe profile data remains: the baked-in project catalog
(ProjectData and friends) was removed with the GSA MAS Checklist,
Schedule Maker, and the /projects page. Project listings now come
from GitHub at runtime (homepage Projects tab, retro Top 8).
"""

from dataclasses import dataclass, field


@dataclass
class Skill:
    """A single skill entry for display in the Core Skills widget."""

    name: str
    level: int  # 0–100
    color: str = 'primary'  # Theme color name for the progress bar


@dataclass
class ToolGroup:
    """A labelled group of tool/technology tags for the Tools & Tech widget."""

    label: str
    icon: str  # Bootstrap Icons class, e.g. "bi-phone"
    tools: list[str]


@dataclass
class AboutMe:
    """Static profile data rendered on the homepage About Me widget."""

    name: str
    bio: str
    profile_image: str  # filename relative to static/images/
    badges: list[str] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    tool_groups: list[ToolGroup] = field(default_factory=list)

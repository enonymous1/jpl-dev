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
class ToolGroup:
    """A labelled group of tool/technology tags for the Tools & Tech widget."""

    label: str
    icon: str  # Bootstrap Icons class, e.g. "bi-phone"
    tools: list[str]


@dataclass
class GlossaryEntry:
    """A one-definition glossary entry for a Tools & Tech pill."""

    definition: str
    url: str | None = None  # Official source; None when there is none.


@dataclass
class AboutMe:
    """Static profile data rendered on the homepage About Me widget."""

    name: str
    bio: str
    profile_image: str  # filename relative to static/images/
    badges: list[str] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    # No percentage skill bars: they were never rendered, and a self-assigned
    # 90 vs 88 proves nothing. The tool groups are the evidence instead.
    tool_groups: list[ToolGroup] = field(default_factory=list)

#!/usr/bin/env python3
"""
Resume data for the homepage Curriculum Vitae tab.

Transcribed 2026-10-28 from the LinkedIn profile PDF the user uploaded
(Profile.pdf) — wording, titles, employers, and dates are the PDF's own;
nothing was added from project work or other sources. Merged
2026-10-30 from the user's own CV PDF (Justin-Lyons-CV.pdf): the
headline, the Mobile Application Developer description, the expanded
EM3 title and employer, and the education notes. Deliberately NOT
merged from the CV: its Selected Projects section (the Projects tab
already lists repos live from GitHub, and the CV's test counts are
dated 2026-10-29), its Technical Skills block (the About section's
Tools & Tech pills already cover most of it), its portfolio counts
(dated the moment they are printed), and its Homelab section (not
approved for the tab). Two things from the LinkedIn PDF are
deliberately NOT rendered on the public site: the mobile phone number
and the Gmail address. The site's contact address is justin@jpl-dev.com
(sidebar and Contact tab); add either value back only on the user's
explicit say-so.

The LinkedIn PDF lists only the Associate's degree. The bachelor's
degree (Full Sail University, April 2024) was supplied by the user in
conversation on 2026-10-28 and is listed alongside it.
"""

from dataclasses import dataclass, field


@dataclass
class ResumeJob:
    """One Experience entry: title, employer, dates, and optional detail."""

    title: str
    employer: str
    location: str
    start: str
    end: str  # "Present" for current roles
    description: str | None = None
    bullets: list[str] = field(default_factory=list)


@dataclass
class ResumeEducation:
    """One Education entry."""

    degree: str
    school: str
    date: str
    note: str | None = None  # e.g. Salutatorian; rendered under the entry


# Headline from the user's CV (2026-10-30), replacing the LinkedIn
# headline it carried before.
RESUME_HEADLINE = 'Systems Automation Specialist | IT Manager | Full-Stack and Mobile Developer'

RESUME_LOCATION = 'Spotsylvania, Virginia, United States'

RESUME_SUMMARY = [
    'As the Information Technology Manager at Millennium Partners, I am '
    'responsible for directing the IT infrastructure and technology '
    "solutions that support the company's global initiatives. I am "
    'passionate about creating user-focused, efficient technology '
    'environments that empower teams to meet their objectives.',
    'My core responsibilities in this role include: Providing '
    'comprehensive IT support to staff at the corporate headquarters and '
    'in various overseas field offices. Creating dynamic multimedia '
    'products, such as videos and infographics, to advance project goals '
    'and communication strategies. Managing the full IT onboarding process '
    'for new employees and consultants, including account setup and '
    'access to collaborative platforms like Microsoft SharePoint. '
    'Designing and implementing IT solutions for a range of international '
    'projects and contributing technical expertise to new proposals.',
    'This position builds upon my foundation as a highly motivated and '
    'results-oriented Mobile Application Developer, where I specialized '
    'in creating engaging and user-friendly applications. With a strong '
    'computer science background as a Salutatorian from Full Sail '
    'University, I have a proven track record of delivering high-quality '
    'apps using Java, Kotlin, and Swift. Furthermore, my prior '
    'experience in the mobile sales industry honed my ability to '
    'communicate effectively and understand end-user needs. I now '
    'leverage this unique combination of technical expertise and '
    'interpersonal skills to support my colleagues and contribute to '
    'innovative solutions at Millennium Partners.',
]

RESUME_JOBS = [
    ResumeJob(
        title='IT Manager',
        employer='Millennium Partners',
        location='',
        start='July 2024',
        end='Present',
        description=(
            'As the Information Technology Manager at Millennium Partners, '
            'I am responsible for directing the IT infrastructure and '
            "technology solutions that support our company's global "
            'initiatives. My role is central to ensuring that both our '
            'domestic and international teams have the technical '
            'capabilities required to meet their objectives effectively.'
        ),
        bullets=[
            'Providing comprehensive IT support to staff at the corporate '
            'headquarters and in various overseas field offices.',
            'Creating dynamic multimedia products, such as videos and '
            'infographics, to advance project goals and communication '
            'strategies.',
            'Managing the full IT onboarding process for new employees and '
            'consultants, which includes setting up email accounts and '
            'providing access to collaborative platforms like Microsoft '
            'SharePoint.',
            'Supporting talent acquisition by collaborating with IT '
            'consultants on the development and maintenance of an internal '
            'experts database.',
            'Designing and implementing IT solutions for a range of '
            'international projects and contributing technical expertise '
            'to proposals for new engagements.',
            'Functioning as a key technical resource for the home office '
            'and senior leadership, including the CEO.',
        ],
    ),
    ResumeJob(
        title='Mobile Application Developer',
        employer='Self-employed',
        location='',
        start='January 2021',
        end='Present',
        # Description from the user's CV: the LinkedIn PDF gave this
        # entry no detail at all, so the tab showed the title alone.
        description=(
            'Design and build engaging, user-friendly Android and iOS '
            'applications in Kotlin, Java, and Swift, with a focus on '
            'offline-first data, clear navigation, and tested releases. '
            'Ship Android apps with Jetpack Compose, Navigation, '
            'ViewModel/StateFlow, Room, and Retrofit, including a maps '
            'point-of-interest app, a Reddit browser with offline caching '
            'and installed-app OAuth, and contacts and employee-records '
            'apps backed by local databases. Build iOS apps in Swift and '
            'SwiftUI, including a card-matching game, a barcode scanner, '
            'and UIKit layout examples modernized for current toolchains.'
        ),
    ),
    ResumeJob(
        title='Freelancer',
        employer='Freelance',
        location='',
        start='January 2017',
        end='Present',
    ),
    ResumeJob(
        # Expanded title and employer from the user's CV; the duty list
        # below stays the fuller LinkedIn version, not the CV's summary.
        title="Electrician's Mate Third Class (EM3)",
        employer='United States Navy Reserve (USNR)',
        location='Richmond, VA',
        start='August 2015',
        end='September 2020',
        description=(
            'Installing power and lighting circuits; repairing distribution '
            'circuits; running wiring for lights and other equipment; '
            'maintaining operating efficiency of distribution panels, '
            'switches, switchboards, controllers, voltage regulators, '
            'current transformers and voltage transformers; maintaining '
            'operating efficiency of electric motors; repairing electrical '
            'equipment and appliances; installing and maintaining storage '
            'batteries; inspecting, maintaining, testing and repairing '
            'electric power equipment; maintenance and repair of shipboard '
            'elevator systems; interpreting electrical sketches, diagrams '
            'and blueprints; maintenance and repair of various propulsion '
            'and auxiliary control consoles; connecting electric power '
            'machinery and electric power equipment.'
        ),
    ),
]

RESUME_EDUCATION = [
    ResumeEducation(
        degree="Bachelor's degree, Computer Science",
        school='Full Sail University',
        date='April 2024',
    ),
    ResumeEducation(
        degree="Associate's degree, Computer Science",
        school='Full Sail University',
        date='November 2022',
        note='Salutatorian',
    ),
]

# From the user's CV: applies to both degrees above.
RESUME_EDUCATION_NOTE = 'Both degrees with weight in Mobile Application Development.'

# LinkedIn Learning courses, as listed in the PDF (no years shown there).
RESUME_CERTIFICATIONS = [
    'Android Studio Essential Training',
    'Learning MATLAB',
    'Android Development Essential Training: 1 Your First App',
    'Agile Foundations',
]

RESUME_LANGUAGES = ['English']

# Top Skills, as listed in the PDF.
RESUME_TOP_SKILLS = [
    'Information Technology',
    'Technology Management',
    'IT Infrastructure Management',
]

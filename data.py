# -*- coding: utf-8 -*-
"""
In-memory dummy data for LMS demo.
Each course has 8 weeks; resource types: tutorial, lecture, recording (video), assignment, project.
Lecture and recording: 1 per week. Tutorial: 1 per 2 weeks. Assignment: 1 per 2 weeks. Project: 1 per 4 weeks.
"""

# Course list: id, code, name, intro (dummy admin / course introduction)
COURSES = [
    {
        "id": "TCX2001",
        "code": "TCX2001",
        "name": "Data Structures and Algorithms",
        "intro": "This course covers fundamental data structures (arrays, linked lists, stacks, queues, trees, graphs, hash tables) and classic algorithms (sorting, searching). You will implement core structures and analyse time/space complexity. Assessment includes weekly lectures, bi-weekly tutorials and assignments, and a final project.",
    },
    {
        "id": "TCX3221",
        "code": "TCX3221",
        "name": "Software Engineering",
        "intro": "This course introduces software development lifecycle, requirements engineering, design, implementation, testing and maintenance. Topics include agile practices, UML, version control and quality assurance. Assessment includes lectures, tutorials, assignments and a team project.",
    },
]


def _lectures_8(code):
    """Build 8 lecture resources (Week 01..08). Title: course code dummyLecture."""
    return [
        {"type": "lecture", "title": f"Week {i:02d} - Lecture - {code} dummyLecture dummypdf.pdf", "week": i}
        for i in range(1, 9)
    ]


def _tutorials_4(code):
    """Build 4 tutorial resources (Week 01-02, 03-04, 05-06, 07-08). Title: tutorial title 1, 2, 3, 4."""
    weeks = [(1, 2), (3, 4), (5, 6), (7, 8)]
    titles = ["tutorial title 1", "tutorial title 2", "tutorial title 3", "tutorial title 4"]
    return [
        {"type": "tutorial", "title": f"Week {a:02d}-{b:02d} - Tutorial - {t} dummypdf.pdf", "week": a}
        for (a, b), t in zip(weeks, titles)
    ]


def _assignments_4(code):
    """Build 4 assignment resources (Week 02, 04, 06, 08). Title: assignment title 1, 2, 3, 4."""
    weeks = [2, 4, 6, 8]
    titles = ["assignment title 1", "assignment title 2", "assignment title 3", "assignment title 4"]
    return [
        {"type": "assignment", "title": f"Week {w:02d} - Assignment - {t} dummypdf.pdf", "week": w}
        for w, t in zip(weeks, titles)
    ]


def _projects_2(code, titles, exts=(".docx", ".pdf")):
    """Build 2 project resources (Week 04, Week 08). PDF project named with 'dummypdf'."""
    return [
        {"type": "project", "title": f"Week 04 - Project - {titles[0]}{exts[0]}", "week": 4},
        {"type": "project", "title": f"Week 08 - Project - {titles[1]} dummypdf{exts[1]}", "week": 8},
    ]


def _recordings_8(code, titles):
    """Build 8 recording/video resources (Week 01..08), one per week. Each has a YouTube URL."""
    # Dummy YouTube video ID per course+week (11-char style)
    base = "lms" + code.replace("X", "") + "w"
    return [
        {
            "type": "recording",
            "title": f"Week {i:02d} - Recording - {t}",
            "week": i,
            "url": f"https://www.youtube.com/watch?v={base}{i:02d}x",
        }
        for i, t in enumerate(titles, start=1)
    ]


# TCX2001 – Data Structures and Algorithms
TCX2001_LECTURES = _lectures_8("TCX2001")
TCX2001_TUTORIALS = _tutorials_4("TCX2001")
TCX2001_ASSIGNMENTS = _assignments_4("TCX2001")
TCX2001_PROJECTS = _projects_2("TCX2001", ["Data Structures Implementation", "Final Algorithms Report"], (".docx", ".pdf"))
TCX2001_RECORDINGS = _recordings_8("TCX2001", [
    "Array and Linked List",
    "Stack and Queue",
    "Trees and BST",
    "Graphs",
    "Sorting Algorithms",
    "Searching Algorithms",
    "Hash Tables",
    "Algorithm Analysis",
])

# TCX3221 – Software Engineering
TCX3221_LECTURES = _lectures_8("TCX3221")
TCX3221_TUTORIALS = _tutorials_4("TCX3221")
TCX3221_ASSIGNMENTS = _assignments_4("TCX3221")
TCX3221_PROJECTS = _projects_2("TCX3221", ["Mini Software Prototype Design", "Final Team Project Requirements"], (".docx", ".pdf"))
TCX3221_RECORDINGS = _recordings_8("TCX3221", [
    "Introduction to Software Engineering",
    "Software Development Life Cycle",
    "Requirements Engineering",
    "Software Design and Architecture",
    "Implementation and Coding Standards",
    "Software Quality and Metrics",
    "Software Maintenance",
    "Software Testing",
])

def get_courses():
    """Return list of course dicts (id, code, name)."""
    return list(COURSES)


def get_resources_by_course(course_id):
    """Return flat list of all resources for a course. Each item: type, title, week."""
    mapping = {
        "TCX2001": TCX2001_LECTURES + TCX2001_RECORDINGS + TCX2001_TUTORIALS + TCX2001_ASSIGNMENTS + TCX2001_PROJECTS,
        "TCX3221": TCX3221_LECTURES + TCX3221_RECORDINGS + TCX3221_TUTORIALS + TCX3221_ASSIGNMENTS + TCX3221_PROJECTS,
    }
    return mapping.get(course_id, [])

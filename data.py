# -*- coding: utf-8 -*-
"""
In-memory dummy data for LMS demo.
Each course has 8 weeks; resource types: tutorial, lecture, recording (video), assignment, project.
Lecture and recording: 1 per week. Tutorial: 1 per 2 weeks. Assignment: 1 per 2 weeks. Project: 1 per 4 weeks.
"""

# Course list: id, code, name
COURSES = [
    {"id": "TCX3211", "code": "TCX3211", "name": "Data Management and Visualisation"},
    {"id": "TCX3212", "code": "TCX3212", "name": "Predictive Analytics"},
    {"id": "TCX3213", "code": "TCX3213", "name": "Data Mining and Machine Learning in Business Analytics"},
    {"id": "TCX3214", "code": "TCX3214", "name": "Text Mining and NLP in Business Analytics"},
    {"id": "TCX3221", "code": "TCX3221", "name": "Software Engineering"},
    {"id": "TCX3222", "code": "TCX3222", "name": "Systems Programming"},
]


def _lectures_8(code, titles):
    """Build 8 lecture resources (Week 01..08). All PDFs named with 'dummypdf'."""
    return [
        {"type": "lecture", "title": f"Week {i:02d} - Lecture - {t} dummypdf.pdf", "week": i}
        for i, t in enumerate(titles, start=1)
    ]


def _tutorials_4(code, titles):
    """Build 4 tutorial resources (Week 01-02, 03-04, 05-06, 07-08). All tutorials are PDF (dummypdf)."""
    weeks = [(1, 2), (3, 4), (5, 6), (7, 8)]
    return [
        {"type": "tutorial", "title": f"Week {a:02d}-{b:02d} - Tutorial - {t} dummypdf.pdf", "week": a}
        for (a, b), t in zip(weeks, titles)
    ]


def _assignments_4(code, titles):
    """Build 4 assignment resources (Week 02, 04, 06, 08). All PDFs named with 'dummypdf'."""
    week_titles = list(zip([2, 4, 6, 8], titles))
    return [
        {"type": "assignment", "title": f"Week {w:02d} - Assignment - {t} dummypdf.pdf", "week": w}
        for w, t in week_titles
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


# TCX3211 – Data Management and Visualisation
TCX3211_LECTURES = _lectures_8("TCX3211", [
    "Introduction to Data Management",
    "Data Modelling and ER Diagrams",
    "SQL Basics and Queries",
    "Visualisation Principles",
    "Tableau Basics",
    "Dashboard Design",
    "Data Quality and Cleaning",
    "Capstone and Best Practices",
])
TCX3211_TUTORIALS = [
    {"type": "tutorial", "title": "Week 01-02 - Tutorial - Database Design Basics dummypdf.pdf", "week": 1},
    {"type": "tutorial", "title": "Week 03-04 - Tutorial - SQL Practice and Joins dummypdf.pdf", "week": 3},
    {"type": "tutorial", "title": "Week 05-06 - Tutorial - Chart Types and Encoding dummypdf.pdf", "week": 5},
    {"type": "tutorial", "title": "Week 07-08 - Tutorial - Dashboard Critique dummypdf.pdf", "week": 7},
]
TCX3211_ASSIGNMENTS = _assignments_4("TCX3211", [
    "ER Diagram Practice",
    "SQL Query Assignment",
    "Visualisation Report",
    "Final Portfolio",
])
TCX3211_PROJECTS = _projects_2("TCX3211", ["Dashboard Prototype Design", "Final Visualisation Report"], (".docx", ".pdf"))
TCX3211_RECORDINGS = _recordings_8("TCX3211", [
    "Introduction to Data Management",
    "Data Modelling and ER Diagrams",
    "SQL Basics and Queries",
    "Visualisation Principles",
    "Tableau Basics",
    "Dashboard Design",
    "Data Quality and Cleaning",
    "Capstone and Best Practices",
])

# TCX3212 – Predictive Analytics
TCX3212_LECTURES = _lectures_8("TCX3212", [
    "Introduction to Predictive Analytics",
    "Regression Fundamentals",
    "Classification Methods",
    "Time Series Basics",
    "Model Evaluation and Validation",
    "Feature Engineering",
    "Ensemble Methods",
    "Deployment and Ethics",
])
TCX3212_TUTORIALS = _tutorials_4("TCX3212", [
    "Linear Regression in Python",
    "Classification with sklearn",
    "Time Series Plotting",
    "Model Comparison and Reporting",
])
TCX3212_ASSIGNMENTS = _assignments_4("TCX3212", [
    "Regression Exercise",
    "Classification Report",
    "Time Series Forecast",
    "Capstone Predictive Report",
])
TCX3212_PROJECTS = _projects_2("TCX3212", ["Predictive Model Prototype", "Final Predictive Analytics Report"], (".docx", ".pdf"))
TCX3212_RECORDINGS = _recordings_8("TCX3212", [
    "Introduction to Predictive Analytics",
    "Regression Fundamentals",
    "Classification Methods",
    "Time Series Basics",
    "Model Evaluation and Validation",
    "Feature Engineering",
    "Ensemble Methods",
    "Deployment and Ethics",
])

# TCX3213 – Data Mining and Machine Learning in Business Analytics
TCX3213_LECTURES = _lectures_8("TCX3213", [
    "Introduction to Data Mining",
    "Clustering and Segmentation",
    "Decision Trees and Random Forest",
    "Association Rules",
    "Neural Networks Basics",
    "Model Tuning and Selection",
    "Business Applications of ML",
    "Ethics and Interpretability",
])
TCX3213_TUTORIALS = _tutorials_4("TCX3213", [
    "K-Means and Hierarchical Clustering",
    "Decision Tree Practice",
    "Association Rules in Python",
    "Model Comparison Report",
])
TCX3213_ASSIGNMENTS = _assignments_4("TCX3213", [
    "Clustering Assignment",
    "Classification with Trees",
    "Association Rules Report",
    "Final ML Report",
])
TCX3213_PROJECTS = _projects_2("TCX3213", ["ML Pipeline Design", "Final Business Analytics Project"], (".docx", ".pdf"))
TCX3213_RECORDINGS = _recordings_8("TCX3213", [
    "Introduction to Data Mining",
    "Clustering and Segmentation",
    "Decision Trees and Random Forest",
    "Association Rules",
    "Neural Networks Basics",
    "Model Tuning and Selection",
    "Business Applications of ML",
    "Ethics and Interpretability",
])

# TCX3214 – Text Mining and NLP in Business Analytics
TCX3214_LECTURES = _lectures_8("TCX3214", [
    "Introduction to Text Mining and NLP",
    "Tokenisation and Normalisation",
    "Vector Representations and TF-IDF",
    "Sentiment Analysis",
    "Topic Modelling",
    "Named Entity Recognition",
    "Transformers and LLMs Overview",
    "NLP in Business Context",
])
TCX3214_TUTORIALS = _tutorials_4("TCX3214", [
    "Text Preprocessing in Python",
    "Sentiment with NLTK",
    "Topic Modelling with LDA",
    "NER and Custom Pipelines",
])
TCX3214_ASSIGNMENTS = _assignments_4("TCX3214", [
    "Text Preprocessing Exercise",
    "Sentiment Analysis Report",
    "Topic Modelling Assignment",
    "NLP Application Report",
])
TCX3214_PROJECTS = _projects_2("TCX3214", ["NLP Pipeline Prototype", "Final NLP Project Report"], (".docx", ".pdf"))
TCX3214_RECORDINGS = _recordings_8("TCX3214", [
    "Introduction to Text Mining and NLP",
    "Tokenisation and Normalisation",
    "Vector Representations and TF-IDF",
    "Sentiment Analysis",
    "Topic Modelling",
    "Named Entity Recognition",
    "Transformers and LLMs Overview",
    "NLP in Business Context",
])

# TCX3221 – Software Engineering
TCX3221_LECTURES = _lectures_8("TCX3221", [
    "Introduction to Software Engineering",
    "Software Development Life Cycle",
    "Requirements Engineering",
    "Software Design and Architecture",
    "Implementation and Coding Standards",
    "Software Quality and Metrics",
    "Software Maintenance",
    "Software Testing",
])
TCX3221_TUTORIALS = _tutorials_4("TCX3221", [
    "Agile Development Basics",
    "UML Diagram Drawing",
    "Version Control with Git",
    "Testing Strategies",
])
TCX3221_ASSIGNMENTS = _assignments_4("TCX3221", [
    "Software Project Proposal",
    "UML Diagram Practice",
    "Code Review Exercise",
    "Test Case Design",
])
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

# TCX3222 – Systems Programming
TCX3222_LECTURES = _lectures_8("TCX3222", [
    "Introduction to Systems Programming",
    "Processes and Threads",
    "Memory Management",
    "File and I/O Systems",
    "Networking and Sockets",
    "Concurrency and Synchronisation",
    "System Security Basics",
    "Performance and Debugging",
])
TCX3222_TUTORIALS = _tutorials_4("TCX3222", [
    "C and Pointers Basics",
    "Multithreading Practice",
    "Socket Programming",
    "Debugging with GDB",
])
TCX3222_ASSIGNMENTS = _assignments_4("TCX3222", [
    "Process and Shell Exercise",
    "Memory and Allocation",
    "Network Client-Server",
    "Concurrency Assignment",
])
TCX3222_PROJECTS = _projects_2("TCX3222", ["Mini Shell or Scheduler", "Final Systems Project Report"], (".docx", ".pdf"))
TCX3222_RECORDINGS = _recordings_8("TCX3222", [
    "Introduction to Systems Programming",
    "Processes and Threads",
    "Memory Management",
    "File and I/O Systems",
    "Networking and Sockets",
    "Concurrency and Synchronisation",
    "System Security Basics",
    "Performance and Debugging",
])


def get_courses():
    """Return list of course dicts (id, code, name)."""
    return list(COURSES)


def get_resources_by_course(course_id):
    """Return flat list of all resources for a course. Each item: type, title, week."""
    mapping = {
        "TCX3211": TCX3211_LECTURES + TCX3211_RECORDINGS + TCX3211_TUTORIALS + TCX3211_ASSIGNMENTS + TCX3211_PROJECTS,
        "TCX3212": TCX3212_LECTURES + TCX3212_RECORDINGS + TCX3212_TUTORIALS + TCX3212_ASSIGNMENTS + TCX3212_PROJECTS,
        "TCX3213": TCX3213_LECTURES + TCX3213_RECORDINGS + TCX3213_TUTORIALS + TCX3213_ASSIGNMENTS + TCX3213_PROJECTS,
        "TCX3214": TCX3214_LECTURES + TCX3214_RECORDINGS + TCX3214_TUTORIALS + TCX3214_ASSIGNMENTS + TCX3214_PROJECTS,
        "TCX3221": TCX3221_LECTURES + TCX3221_RECORDINGS + TCX3221_TUTORIALS + TCX3221_ASSIGNMENTS + TCX3221_PROJECTS,
        "TCX3222": TCX3222_LECTURES + TCX3222_RECORDINGS + TCX3222_TUTORIALS + TCX3222_ASSIGNMENTS + TCX3222_PROJECTS,
    }
    return mapping.get(course_id, [])

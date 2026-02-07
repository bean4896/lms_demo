# LMS Resource Finder Demo

A simple student-centric LMS demo with a **global AJAX search bar**, fuzzy search, and resource recommendations. Built with Flask (Python) and plain HTML/CSS/JavaScript.

## Features

- **Dashboard**: List of 6 TCX courses; click a course to open its homepage.
- **Global search bar**: At the top of each course page; type to search without page reload.
- **Fuzzy search**: Tolerates typos, partial keywords, and case (e.g. `lec 01` or `lect 01` matches "Week 01 - Lecture - Introduction.pdf").
- **Recommendations**: After search, 2–3 related resources (e.g. same week tutorial/assignment) are shown below results.

## Dummy Data

- **Courses**: TCX3211, TCX3212, TCX3213, TCX3214, TCX3221, TCX3222 (with full names).
- **Per course**: 8 weeks; 5 resource types — **lecture** (1 per week, PDF), **recording** (1 per week, video e.g. .mp4), **tutorial** (1 per 2 weeks), **assignment** (1 per 2 weeks), **project** (1 per 4 weeks).
- All data is in-memory in `data.py`; no database required.

## Push to GitHub

From the `lms_demo` folder (as the repo root):

```bash
cd lms_demo
git init
git add .
git commit -m "Initial commit: LMS Resource Finder demo"
git remote add origin https://github.com/bean4896/lms_demo.git
git branch -M main
git push -u origin main
```

Repo: [https://github.com/bean4896/lms_demo](https://github.com/bean4896/lms_demo)

## Run the Demo

### 1. Install dependencies

```bash
cd lms_demo
pip install -r requirements.txt
```

### 2. Start the Flask server

```bash
python app.py
```

The app will run at **http://127.0.0.1:5000/** (debug mode).

### 3. Open in browser

- **Dashboard**: http://127.0.0.1:5000/
- Click any course (e.g. **TCX3221 – Software Engineering**) to open the course page.
- Use the **global search bar** at the top; try e.g. `lecture 01`, `week 02`, `assignment`, or `lec 01`.

## Project structure

```
lms_demo/
  app.py              # Flask app: routes, fuzzy search, recommendations
  data.py             # In-memory courses and resources (edit here to change dummy data)
  requirements.txt
  static/
    style.css         # Layout and search bar styling
    app.js            # AJAX search and result rendering
  templates/
    index.html        # Dashboard (course list)
    course.html       # Course page (global search + results)
  README.md
```

## Customisation

- **Dummy data**: Edit `data.py` to add courses or change resource titles/weeks.
- **Search logic**: See `search_resources()` and `fuzzy_score()` in `app.py`.
- **Recommendations**: See `get_recommendations()` in `app.py`.
- **UI**: Adjust `static/style.css` and `templates/course.html` as needed.

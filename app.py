# -*- coding: utf-8 -*-
"""
LMS Resource Finder Demo - Flask backend.
Serves dashboard, course page, and AJAX search API with fuzzy search and recommendations.
Internal manage page allows updating lecture/PDF/video links (stored in instance/resource_overrides.json).
"""
import re
from difflib import SequenceMatcher
from flask import Flask, render_template, request, jsonify

from data import get_courses, get_resources_by_course
from overrides import load_overrides, save_overrides, get_resources_for_course as get_overridable_resources

app = Flask(__name__)


def get_resources_for_course(course_id):
    """Resources for course: from overrides if saved, else default from data (with pdf_url set for PDFs)."""
    default = get_resources_by_course(course_id)
    return get_overridable_resources(app, course_id, default)


def normalize(s):
    """Lowercase and collapse spaces for case-insensitive, flexible matching."""
    return " ".join(re.split(r"\s+", (s or "").lower().strip()))


def fuzzy_score(query_norm, text_norm):
    """
    Score how well query matches text: exact substring, then all-token match.
    When not all query tokens appear in text (e.g. 'week 04' vs 'week 01'), return low score
    so that 'week 04' shows week 04 content first, not week 01.
    """
    if not query_norm:
        return 0.0
    if query_norm in text_norm:
        return 1.0
    q_tokens = query_norm.split()
    text_lower = text_norm
    token_ok = sum(1 for t in q_tokens if t in text_lower)
    if token_ok == len(q_tokens):
        return 0.9
    # Partial token match: don't rank highly (e.g. "week 04" must not rank "week 01" high)
    return 0.2 * SequenceMatcher(None, query_norm, text_norm).ratio()


def search_resources(course_id, query, limit=15):
    """
    Fuzzy search over course resources. Returns list of dicts with type, title, week, url/pdf_url.
    """
    resources = get_resources_for_course(course_id)
    if not query or not query.strip():
        return []
    q_norm = normalize(query.strip())
    scored = []
    for r in resources:
        title = r.get("title", "")
        # So "week xx video" / "week xx youtube" matches recordings (YouTube links)
        if r.get("type") == "recording":
            title = title + " video recording youtube"
        t_norm = normalize(title)
        score = fuzzy_score(q_norm, t_norm)
        if score > 0.3:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return [r for _, r in scored[:limit]]


def get_recommendations(course_id, matched_resources, max_count=3):
    """
    Suggest 2-3 related resources (e.g. same week: tutorial, assignment, project).
    Uses week and type: if user found a lecture, recommend tutorial/assignment for same week.
    """
    all_res = get_resources_for_course(course_id)
    if not matched_resources:
        # No search match: return first few by type diversity
        by_type = {}
        for r in all_res:
            t = r.get("type", "")
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(r)
        out = []
        for t in ("lecture", "recording", "tutorial", "assignment", "project"):
            if t in by_type and by_type[t]:
                out.append(by_type[t][0])
                if len(out) >= max_count:
                    break
        return out[:max_count]
    # Use weeks from matched results to find related (same week, different type)
    matched_titles = {r.get("title") for r in matched_resources}
    weeks = {r.get("week") for r in matched_resources}
    recommended = []
    for r in all_res:
        if r.get("title") in matched_titles:
            continue
        if r.get("week") in weeks:
            recommended.append(r)
    # Prefer different types from matches
    matched_types = {r.get("type") for r in matched_resources}
    recommended = [r for r in recommended if r.get("type") not in matched_types][:max_count]
    if len(recommended) < max_count:
        for r in all_res:
            if r.get("title") in matched_titles:
                continue
            if r not in recommended:
                recommended.append(r)
            if len(recommended) >= max_count:
                break
    return recommended[:max_count]


# ----- Routes -----

@app.route("/")
def index():
    """Dashboard: course list."""
    courses = get_courses()
    return render_template("index.html", courses=courses)


@app.route("/course/<course_id>")
def course_page(course_id):
    """Course homepage with global search bar."""
    courses = get_courses()
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        return "Course not found", 404
    return render_template("course.html", course=course)


@app.route("/api/courses")
def api_courses():
    """JSON: list of courses (for optional AJAX use)."""
    return jsonify(get_courses())


@app.route("/course/<course_id>/manage")
def manage_resources(course_id):
    """Internal page: edit lecture PDF, assignment PDF, video link, etc."""
    courses = get_courses()
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        return "Course not found", 404
    return render_template("manage.html", course=course)


@app.route("/api/course/<course_id>/resources", methods=["GET"])
def api_get_resources(course_id):
    """Return current resources for course (for manage page). Includes pdf_url, url."""
    resources = get_resources_for_course(course_id)
    return jsonify({"resources": resources})


@app.route("/api/course/<course_id>/resources", methods=["PUT"])
def api_put_resources(course_id):
    """Save resource overrides (titles, pdf_url, url) for the course."""
    data = request.get_json(force=True, silent=True) or {}
    resources = data.get("resources", [])
    if not isinstance(resources, list):
        return jsonify({"error": "resources must be a list"}), 400
    overrides = load_overrides(app)
    overrides[course_id] = resources
    save_overrides(app, overrides)
    return jsonify({"ok": True, "resources": resources})


@app.route("/api/course/<course_id>/search")
def api_search(course_id):
    """
    AJAX search: query param 'q' = search string.
    When q is empty, return all resources. Otherwise fuzzy search + recommendations.
    Returns { results: [...], recommendations: [...] }.
    """
    q = request.args.get("q", "").strip()
    if not q:
        results = get_resources_for_course(course_id)
        recommendations = []
    else:
        results = search_resources(course_id, q)
        recommendations = get_recommendations(course_id, results, max_count=3)
    return jsonify({
        "results": results,
        "recommendations": recommendations,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)

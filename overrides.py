# -*- coding: utf-8 -*-
"""
Persistent overrides for course resources (lecture PDF, assignment PDF, video link, etc.).
Stored in instance/resource_overrides.json so internal users can update links/titles.
"""
import json
import os
import copy

def _overrides_path(app):
    return os.path.join(app.instance_path, "resource_overrides.json")


def load_overrides(app):
    """Load { course_id: [ resources... ] } from JSON. Returns {} if file missing."""
    path = _overrides_path(app)
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_overrides(app, overrides):
    """Write full overrides dict to JSON."""
    path = _overrides_path(app)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(overrides, f, indent=2, ensure_ascii=False)


def get_resources_for_course(app, course_id, default_resources):
    """
    Return resources for course: overrides if present, else default.
    default_resources = list from data.get_resources_by_course(course_id).
    Each resource may have: type, title, week, url (recording), pdf_url (PDFs).
    """
    overrides = load_overrides(app)
    if course_id in overrides:
        return overrides[course_id]
    # Return copies so we can add pdf_url for API without mutating defaults
    out = []
    for r in default_resources:
        item = copy.deepcopy(r)
        if item.get("type") != "recording" and (item.get("title") or "").endswith(".pdf"):
            item.setdefault("pdf_url", "")
        out.append(item)
    return out

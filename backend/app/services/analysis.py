from __future__ import annotations

import re
from typing import Any


TASK_MARKERS = ("todo", "next step", "action item", "follow up", "need to")
PROJECT_KEYWORDS = {
    "hebrew": "Hebrew Learning",
    "guitar": "Guitar Mastery",
    "podcast": "Podcast",
    "book": "Book Writing",
    "iam": "IAM Engineering",
    "infra": "Infrastructure",
    "api": "API Integration",
}


def _extract_tasks(text: str) -> list[str]:
    tasks: list[str] = []
    lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]
    for line in lines:
        lowered = line.lower()
        if any(marker in lowered for marker in TASK_MARKERS):
            tasks.append(line[:240])
        elif lowered.startswith(("build ", "create ", "implement ", "ship ", "fix ")):
            tasks.append(line[:240])
    return tasks[:8]


def _extract_projects(text: str, fallback_title: str) -> list[str]:
    found: list[str] = []
    lowered = text.lower()
    for token, label in PROJECT_KEYWORDS.items():
        if token in lowered:
            found.append(label)
    if not found and fallback_title:
        found.append(fallback_title[:80])
    # Preserve order while removing duplicates
    seen = set()
    deduped = []
    for item in found:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped[:5]


def _condense(text: str, limit: int = 450) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return f"{compact[:limit].rstrip()}..."


def analyze_conversation(conversation: dict) -> dict:
    """Heuristic analysis fallback until LLM provider is configured."""
    title = conversation.get("title", "")
    messages = conversation.get("messages") or []
    text_blob = "\n".join(str(msg.get("content", "")) for msg in messages if isinstance(msg, dict))
    if not text_blob:
        text_blob = str(conversation.get("content", ""))

    task_titles = _extract_tasks(text_blob)
    project_names = _extract_projects(text_blob, title)

    open_questions = []
    for line in text_blob.splitlines():
        stripped = line.strip()
        if stripped.endswith("?"):
            open_questions.append(stripped[:240])
    open_questions = open_questions[:8]

    key_points = []
    for sentence in re.split(r"(?<=[.!?])\s+", _condense(text_blob, limit=1200)):
        clean = sentence.strip()
        if clean and len(clean) > 20:
            key_points.append(clean[:260])
        if len(key_points) >= 6:
            break

    return {
        "summary": _condense(text_blob),
        "key_points": key_points,
        "open_questions": open_questions,
        "projects": [{"name": name} for name in project_names],
        "tasks": [{"title": task, "status": "open"} for task in task_titles],
    }

"""
Importers for various chat-export formats.

Each importer accepts a file path and an open SQLite connection, then calls the
db helpers to persist sessions and messages.  The importers are intentionally
lenient – they skip records they cannot parse rather than aborting the whole
import.

Supported formats
-----------------
* ChatGPT  – the conversations.json produced by OpenAI's "Export data" feature.
* Claude   – the conversations.json produced by Anthropic's export feature.
* Generic  – a simple JSON array of sessions (documented in README).
* CSV      – a flat CSV where each row is one message (documented in README).
"""

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any

from .db import insert_message, upsert_session


# ---------------------------------------------------------------------------
# ChatGPT  (OpenAI export format)
# ---------------------------------------------------------------------------

def import_chatgpt(path: Path, conn: sqlite3.Connection) -> dict[str, int]:
    """
    Import a ChatGPT conversations.json export file.

    Expected top-level structure: a JSON array where each element is a
    conversation object with at minimum:
        {
          "id": "...",
          "title": "...",
          "create_time": 1700000000.0,
          "update_time": 1700001000.0,
          "mapping": {
            "<node-id>": {
              "message": {
                "author": {"role": "user"|"assistant"|"system"|"tool"},
                "create_time": 1700000001.0,
                "content": {"parts": ["text..."]}
              }
            }
          }
        }
    """
    raw: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    counts = {"sessions": 0, "messages": 0, "skipped": 0}

    for conv in raw:
        try:
            ext_id = conv.get("id")
            title = conv.get("title")
            started = _ts(conv.get("create_time"))
            ended = _ts(conv.get("update_time"))

            session_id = upsert_session(
                conn,
                source="chatgpt",
                external_id=ext_id,
                title=title,
                started_at=started,
                ended_at=ended,
            )
            counts["sessions"] += 1

            mapping = conv.get("mapping") or {}
            nodes = sorted(
                (v for v in mapping.values() if v.get("message")),
                key=lambda n: n["message"].get("create_time") or 0,
            )
            for node in nodes:
                msg = node["message"]
                role = (msg.get("author") or {}).get("role", "user")
                if role not in ("user", "assistant", "system", "tool"):
                    role = "user"
                content_obj = msg.get("content") or {}
                parts = content_obj.get("parts") or []
                content = "\n".join(str(p) for p in parts if p)
                if not content:
                    continue
                sent_at = _ts(msg.get("create_time"))
                insert_message(
                    conn,
                    session_id=session_id,
                    role=role,
                    content=content,
                    sent_at=sent_at,
                )
                counts["messages"] += 1
        except Exception:
            counts["skipped"] += 1
            continue

    return counts


# ---------------------------------------------------------------------------
# Claude  (Anthropic export format)
# ---------------------------------------------------------------------------

def import_claude(path: Path, conn: sqlite3.Connection) -> dict[str, int]:
    """
    Import a Claude conversations.json export file.

    Expected structure: a JSON array where each element looks like:
        {
          "uuid": "...",
          "name": "...",
          "created_at": "2024-01-01T00:00:00.000Z",
          "updated_at": "2024-01-01T01:00:00.000Z",
          "chat_messages": [
            {
              "uuid": "...",
              "sender": "human"|"assistant",
              "text": "...",
              "created_at": "2024-01-01T00:00:05.000Z"
            }
          ]
        }
    """
    raw: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    counts = {"sessions": 0, "messages": 0, "skipped": 0}

    _role_map = {"human": "user", "assistant": "assistant"}

    for conv in raw:
        try:
            ext_id = conv.get("uuid")
            title = conv.get("name")
            started = conv.get("created_at")
            ended = conv.get("updated_at")

            session_id = upsert_session(
                conn,
                source="claude",
                external_id=ext_id,
                title=title,
                started_at=started,
                ended_at=ended,
            )
            counts["sessions"] += 1

            for msg in conv.get("chat_messages") or []:
                sender = msg.get("sender", "human")
                role = _role_map.get(sender, "user")
                content = (msg.get("text") or "").strip()
                if not content:
                    continue
                insert_message(
                    conn,
                    session_id=session_id,
                    role=role,
                    content=content,
                    sent_at=msg.get("created_at"),
                )
                counts["messages"] += 1
        except Exception:
            counts["skipped"] += 1
            continue

    return counts


# ---------------------------------------------------------------------------
# Generic JSON  (werii-gather native format)
# ---------------------------------------------------------------------------

def import_generic_json(path: Path, conn: sqlite3.Connection) -> dict[str, int]:
    """
    Import a generic JSON array of sessions.

    Each session object may contain:
        {
          "id":         "<optional external id>",
          "source":     "<optional source label, defaults to 'generic'>",
          "title":      "<optional title>",
          "started_at": "<optional ISO-8601 timestamp>",
          "ended_at":   "<optional ISO-8601 timestamp>",
          "messages": [
            {
              "role":     "user"|"assistant"|"system",
              "content":  "<message text>",
              "sent_at":  "<optional ISO-8601 timestamp>"
            }
          ]
        }
    """
    raw: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    counts = {"sessions": 0, "messages": 0, "skipped": 0}

    for sess in raw:
        try:
            source = sess.get("source") or "generic"
            session_id = upsert_session(
                conn,
                source=source,
                external_id=sess.get("id"),
                title=sess.get("title"),
                started_at=sess.get("started_at"),
                ended_at=sess.get("ended_at"),
            )
            counts["sessions"] += 1

            for msg in sess.get("messages") or []:
                role = msg.get("role", "user")
                if role not in ("user", "assistant", "system", "tool"):
                    role = "user"
                content = (msg.get("content") or "").strip()
                if not content:
                    continue
                insert_message(
                    conn,
                    session_id=session_id,
                    role=role,
                    content=content,
                    sent_at=msg.get("sent_at"),
                )
                counts["messages"] += 1
        except Exception:
            counts["skipped"] += 1
            continue

    return counts


# ---------------------------------------------------------------------------
# CSV  (flat, one row per message)
# ---------------------------------------------------------------------------

# Expected columns (case-insensitive, order does not matter):
#   session_id  – groups messages into a session (required)
#   role        – user / assistant / system  (required)
#   content     – message text (required)
#   title       – session title (optional)
#   sent_at     – ISO-8601 or any parseable date string (optional)
#   source      – source label (optional, defaults to "csv")

def import_csv(path: Path, conn: sqlite3.Connection) -> dict[str, int]:
    counts = {"sessions": 0, "messages": 0, "skipped": 0}
    session_cache: dict[str, int] = {}  # external_id -> session rowid

    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        # Normalise header names to lowercase
        if reader.fieldnames is None:
            return counts
        reader.fieldnames = [f.strip().lower() for f in reader.fieldnames]

        for row in reader:
            try:
                ext_id = row.get("session_id", "").strip()
                if not ext_id:
                    counts["skipped"] += 1
                    continue

                if ext_id not in session_cache:
                    source = row.get("source", "").strip() or "csv"
                    sid = upsert_session(
                        conn,
                        source=source,
                        external_id=ext_id,
                        title=row.get("title", "").strip() or None,
                        started_at=None,
                        ended_at=None,
                    )
                    session_cache[ext_id] = sid
                    counts["sessions"] += 1

                role = row.get("role", "user").strip().lower()
                if role not in ("user", "assistant", "system", "tool"):
                    role = "user"
                content = row.get("content", "").strip()
                if not content:
                    counts["skipped"] += 1
                    continue

                insert_message(
                    conn,
                    session_id=session_cache[ext_id],
                    role=role,
                    content=content,
                    sent_at=row.get("sent_at", "").strip() or None,
                )
                counts["messages"] += 1
            except Exception:
                counts["skipped"] += 1
                continue

    return counts


# ---------------------------------------------------------------------------
# Dispatch helper
# ---------------------------------------------------------------------------

IMPORTERS = {
    "chatgpt": import_chatgpt,
    "claude": import_claude,
    "generic": import_generic_json,
    "csv": import_csv,
}


def detect_format(path: Path) -> str:
    """Heuristically detect the format of a file."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix in (".json", ".jsonl"):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(raw, list) and raw:
                first = raw[0]
                if "mapping" in first:
                    return "chatgpt"
                if "chat_messages" in first:
                    return "claude"
        except Exception:
            pass
        return "generic"
    return "generic"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _ts(unix_or_none) -> str | None:
    """Convert a UNIX float timestamp to ISO-8601, or return None."""
    if unix_or_none is None:
        return None
    try:
        from datetime import datetime, timezone
        return datetime.fromtimestamp(float(unix_or_none),
                                      tz=timezone.utc).isoformat()
    except Exception:
        return None

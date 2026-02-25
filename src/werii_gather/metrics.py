"""
Metrics and analytics: aggregate statistics across all gathered sessions.
"""

import sqlite3
from collections import Counter
import re


def summary(conn: sqlite3.Connection) -> dict:
    """Return a high-level summary dict of the entire database."""
    r = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    m = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    sources = {
        row["source"]: row["cnt"]
        for row in conn.execute(
            "SELECT source, COUNT(*) AS cnt FROM sessions GROUP BY source ORDER BY cnt DESC"
        ).fetchall()
    }
    return {"total_sessions": r, "total_messages": m, "by_source": sources}


def activity_by_date(conn: sqlite3.Connection) -> list[dict]:
    """Return per-day session-start counts (most recent first)."""
    rows = conn.execute(
        """
        SELECT substr(started_at, 1, 10) AS day, COUNT(*) AS sessions
        FROM   sessions
        WHERE  started_at IS NOT NULL
        GROUP  BY day
        ORDER  BY day DESC
        LIMIT  30
        """
    ).fetchall()
    return [dict(row) for row in rows]


def top_words(conn: sqlite3.Connection, n: int = 20) -> list[tuple[str, int]]:
    """Return the *n* most-frequent content words across all user messages."""
    _stopwords = {
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "is", "it", "i", "you", "that", "this",
        "was", "are", "be", "have", "has", "had", "do", "not", "as",
        "by", "from", "my", "we", "can", "will", "if", "so", "what",
        "how", "just", "me", "he", "she", "they", "all", "more", "when",
        "also", "there", "up", "out", "about", "like", "get", "use",
        "than", "no", "your", "its", "any", "which", "would", "could",
        "should", "been",
    }
    rows = conn.execute(
        "SELECT content FROM messages WHERE role='user'"
    ).fetchall()
    counter: Counter = Counter()
    for row in rows:
        words = re.findall(r"[a-z]{3,}", row[0].lower())
        for w in words:
            if w not in _stopwords:
                counter[w] += 1
    return counter.most_common(n)


def sessions_list(conn: sqlite3.Connection, *,
                  source: str | None = None,
                  limit: int = 50,
                  offset: int = 0) -> list[dict]:
    """Return a list of sessions with message-count annotation."""
    where = "WHERE s.source = ?" if source else ""
    params: list = [source] if source else []
    params += [limit, offset]
    rows = conn.execute(
        f"""
        SELECT s.id, s.source, s.title, s.started_at, s.ended_at,
               COUNT(m.id) AS message_count
        FROM   sessions s
        LEFT JOIN messages m ON m.session_id = s.id
        {where}
        GROUP  BY s.id
        ORDER  BY s.started_at DESC NULLS LAST
        LIMIT  ? OFFSET ?
        """,
        params,
    ).fetchall()
    return [dict(row) for row in rows]


def search_sessions(conn: sqlite3.Connection, query: str,
                    limit: int = 20) -> list[dict]:
    """Full-text search across message content and session titles."""
    pattern = f"%{query}%"
    rows = conn.execute(
        """
        SELECT DISTINCT s.id, s.source, s.title, s.started_at,
               COUNT(m2.id) AS message_count
        FROM   sessions s
        JOIN   messages m  ON m.session_id = s.id
        LEFT JOIN messages m2 ON m2.session_id = s.id
        WHERE  m.content LIKE ? OR s.title LIKE ?
        GROUP  BY s.id
        ORDER  BY s.started_at DESC NULLS LAST
        LIMIT  ?
        """,
        (pattern, pattern, limit),
    ).fetchall()
    return [dict(row) for row in rows]


def session_detail(conn: sqlite3.Connection, session_id: int) -> dict | None:
    """Return a session with all its messages."""
    s = conn.execute(
        "SELECT * FROM sessions WHERE id=?", (session_id,)
    ).fetchone()
    if not s:
        return None
    msgs = conn.execute(
        "SELECT role, content, sent_at FROM messages WHERE session_id=? ORDER BY sent_at, id",
        (session_id,),
    ).fetchall()
    tags = conn.execute(
        """
        SELECT t.name FROM tags t
        JOIN session_tags st ON st.tag_id = t.id
        WHERE st.session_id=?
        """,
        (session_id,),
    ).fetchall()
    return {
        **dict(s),
        "messages": [dict(m) for m in msgs],
        "tags": [t["name"] for t in tags],
    }

"""
Database layer: schema creation, migrations, and low-level CRUD helpers.

Schema
------
sessions   – one row per imported chat session
messages   – one row per message within a session
tags       – vocabulary of user-defined topic tags
session_tags – many-to-many link between sessions and tags
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Default database location (overridable via env / CLI flag)
DEFAULT_DB_PATH = Path.home() / ".werii-gather" / "gather.db"

DDL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT    NOT NULL,           -- e.g. "chatgpt", "claude", "csv", "generic"
    external_id TEXT,                       -- original id from the source, if available
    title       TEXT,
    started_at  TEXT,                       -- ISO-8601 timestamp of first message
    ended_at    TEXT,                       -- ISO-8601 timestamp of last message
    imported_at TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE(source, external_id)
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role       TEXT    NOT NULL CHECK(role IN ('user','assistant','system','tool')),
    content    TEXT    NOT NULL,
    sent_at    TEXT,                        -- ISO-8601 timestamp
    token_count INTEGER                    -- optional; populated if source provides it
);

CREATE TABLE IF NOT EXISTS tags (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS session_tags (
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    tag_id     INTEGER NOT NULL REFERENCES tags(id)     ON DELETE CASCADE,
    PRIMARY KEY (session_id, tag_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_role    ON messages(role);
CREATE INDEX IF NOT EXISTS idx_sessions_source  ON sessions(source);
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(DDL)
    return conn


@contextmanager
def get_connection(db_path: Path | None = None):
    """Context-manager that yields an open, WAL-mode SQLite connection."""
    path = db_path or DEFAULT_DB_PATH
    conn = _connect(path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def upsert_session(conn: sqlite3.Connection, *, source: str, external_id: str | None,
                   title: str | None, started_at: str | None,
                   ended_at: str | None) -> int:
    """Insert or update a session row and return its rowid."""
    cur = conn.execute(
        """
        INSERT INTO sessions (source, external_id, title, started_at, ended_at)
        VALUES (:source, :external_id, :title, :started_at, :ended_at)
        ON CONFLICT(source, external_id) DO UPDATE SET
            title      = excluded.title,
            started_at = excluded.started_at,
            ended_at   = excluded.ended_at
        RETURNING id
        """,
        dict(source=source, external_id=external_id, title=title,
             started_at=started_at, ended_at=ended_at),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    # ON CONFLICT path may not RETURN on all SQLite builds < 3.35 – fall back
    cur = conn.execute(
        "SELECT id FROM sessions WHERE source=? AND external_id=?",
        (source, external_id),
    )
    return cur.fetchone()[0]


def insert_message(conn: sqlite3.Connection, *, session_id: int, role: str,
                   content: str, sent_at: str | None,
                   token_count: int | None = None) -> int:
    cur = conn.execute(
        """
        INSERT INTO messages (session_id, role, content, sent_at, token_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        (session_id, role, content, sent_at, token_count),
    )
    return cur.lastrowid


def ensure_tag(conn: sqlite3.Connection, name: str) -> int:
    conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
    cur = conn.execute("SELECT id FROM tags WHERE name=?", (name,))
    return cur.fetchone()[0]


def tag_session(conn: sqlite3.Connection, session_id: int, tag_name: str) -> None:
    tag_id = ensure_tag(conn, tag_name.strip().lower())
    conn.execute(
        "INSERT OR IGNORE INTO session_tags (session_id, tag_id) VALUES (?,?)",
        (session_id, tag_id),
    )

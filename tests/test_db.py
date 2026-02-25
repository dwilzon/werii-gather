"""Tests for the database layer."""

import sqlite3
import pytest
from pathlib import Path

from werii_gather.db import (
    get_connection,
    upsert_session,
    insert_message,
    ensure_tag,
    tag_session,
)


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"


@pytest.fixture
def conn(db_path):
    with get_connection(db_path) as c:
        yield c


def test_upsert_session_creates_row(db_path):
    with get_connection(db_path) as conn:
        sid = upsert_session(
            conn,
            source="test",
            external_id="abc",
            title="Hello",
            started_at="2024-01-01T00:00:00+00:00",
            ended_at=None,
        )
    assert isinstance(sid, int)
    assert sid > 0


def test_upsert_session_is_idempotent(db_path):
    kwargs = dict(source="test", external_id="abc", title="A", started_at=None, ended_at=None)
    with get_connection(db_path) as conn:
        sid1 = upsert_session(conn, **kwargs)
        sid2 = upsert_session(conn, **kwargs)
    assert sid1 == sid2


def test_upsert_session_updates_title(db_path):
    with get_connection(db_path) as conn:
        upsert_session(conn, source="s", external_id="x", title="Old", started_at=None, ended_at=None)
        upsert_session(conn, source="s", external_id="x", title="New", started_at=None, ended_at=None)
        row = conn.execute("SELECT title FROM sessions WHERE source='s' AND external_id='x'").fetchone()
    assert row["title"] == "New"


def test_insert_message(db_path):
    with get_connection(db_path) as conn:
        sid = upsert_session(conn, source="t", external_id="1", title=None, started_at=None, ended_at=None)
        mid = insert_message(conn, session_id=sid, role="user", content="Hello", sent_at=None)
    assert isinstance(mid, int)


def test_ensure_tag_idempotent(db_path):
    with get_connection(db_path) as conn:
        t1 = ensure_tag(conn, "ai")
        t2 = ensure_tag(conn, "ai")
    assert t1 == t2


def test_tag_session(db_path):
    with get_connection(db_path) as conn:
        sid = upsert_session(conn, source="t", external_id="99", title=None, started_at=None, ended_at=None)
        tag_session(conn, sid, "creativity")
        tag_session(conn, sid, "creativity")  # idempotent
        rows = conn.execute(
            "SELECT t.name FROM tags t JOIN session_tags st ON st.tag_id=t.id WHERE st.session_id=?",
            (sid,),
        ).fetchall()
    assert len(rows) == 1
    assert rows[0]["name"] == "creativity"

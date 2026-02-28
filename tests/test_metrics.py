"""Tests for metrics / analytics helpers."""

import json
import pytest
from pathlib import Path

from werii_gather.db import get_connection, upsert_session, insert_message
from werii_gather.metrics import (
    summary,
    activity_by_date,
    top_words,
    sessions_list,
    search_sessions,
    session_detail,
)


@pytest.fixture
def populated_db(tmp_path):
    db_path = tmp_path / "metrics.db"
    with get_connection(db_path) as conn:
        sid1 = upsert_session(
            conn,
            source="chatgpt",
            external_id="s1",
            title="AI discussion",
            started_at="2024-01-10T09:00:00Z",
            ended_at="2024-01-10T10:00:00Z",
        )
        insert_message(conn, session_id=sid1, role="user",
                       content="Tell me about artificial intelligence and creativity",
                       sent_at="2024-01-10T09:00:01Z")
        insert_message(conn, session_id=sid1, role="assistant",
                       content="Sure! AI can be very creative.",
                       sent_at="2024-01-10T09:00:10Z")

        sid2 = upsert_session(
            conn,
            source="claude",
            external_id="s2",
            title="Project planning",
            started_at="2024-01-11T14:00:00Z",
            ended_at="2024-01-11T15:00:00Z",
        )
        insert_message(conn, session_id=sid2, role="user",
                       content="Let's plan our creative project about intelligence",
                       sent_at="2024-01-11T14:00:01Z")

    return db_path


def test_summary(populated_db):
    with get_connection(populated_db) as conn:
        s = summary(conn)
    assert s["total_sessions"] == 2
    assert s["total_messages"] == 3
    assert "chatgpt" in s["by_source"]
    assert "claude" in s["by_source"]


def test_sessions_list(populated_db):
    with get_connection(populated_db) as conn:
        rows = sessions_list(conn)
    assert len(rows) == 2
    # Most recent first
    assert rows[0]["title"] == "Project planning"


def test_sessions_list_filter_source(populated_db):
    with get_connection(populated_db) as conn:
        rows = sessions_list(conn, source="chatgpt")
    assert len(rows) == 1
    assert rows[0]["source"] == "chatgpt"


def test_search_sessions(populated_db):
    with get_connection(populated_db) as conn:
        results = search_sessions(conn, "creativity")
    assert any(r["title"] == "AI discussion" for r in results)


def test_search_sessions_by_title(populated_db):
    with get_connection(populated_db) as conn:
        results = search_sessions(conn, "Project")
    assert len(results) >= 1
    assert any("Project" in r["title"] for r in results)


def test_top_words(populated_db):
    with get_connection(populated_db) as conn:
        words = top_words(conn, n=10)
    word_names = [w for w, _ in words]
    # "creative"/"creativity" and "intelligence"/"intelligent" appear in user messages
    assert any(w in word_names for w in ("creative", "creativity", "intelligence", "artificial", "creative"))


def test_activity_by_date(populated_db):
    with get_connection(populated_db) as conn:
        rows = activity_by_date(conn)
    assert len(rows) >= 2
    dates = [r["day"] for r in rows]
    assert "2024-01-11" in dates
    assert "2024-01-10" in dates


def test_session_detail(populated_db):
    with get_connection(populated_db) as conn:
        rows = sessions_list(conn)
        sid = rows[-1]["id"]  # the chatgpt one (started earliest, listed last)
        detail = session_detail(conn, sid)

    assert detail is not None
    assert detail["source"] == "chatgpt"
    assert len(detail["messages"]) == 2
    assert detail["messages"][0]["role"] == "user"


def test_session_detail_not_found(populated_db):
    with get_connection(populated_db) as conn:
        detail = session_detail(conn, 9999)
    assert detail is None

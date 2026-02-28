"""Tests for chat-session importers."""

import json
import pytest
from pathlib import Path

from werii_gather.db import get_connection
from werii_gather.importers import (
    import_chatgpt,
    import_claude,
    import_generic_json,
    import_csv,
    detect_format,
)


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"


# ---------------------------------------------------------------------------
# detect_format
# ---------------------------------------------------------------------------

def test_detect_format_csv(tmp_path):
    f = tmp_path / "export.csv"
    f.write_text("session_id,role,content\n")
    assert detect_format(f) == "csv"


def test_detect_format_chatgpt(tmp_path):
    data = [{"id": "x", "mapping": {}}]
    f = tmp_path / "conversations.json"
    f.write_text(json.dumps(data))
    assert detect_format(f) == "chatgpt"


def test_detect_format_claude(tmp_path):
    data = [{"uuid": "y", "chat_messages": []}]
    f = tmp_path / "conversations.json"
    f.write_text(json.dumps(data))
    assert detect_format(f) == "claude"


def test_detect_format_generic(tmp_path):
    data = [{"title": "T", "messages": []}]
    f = tmp_path / "data.json"
    f.write_text(json.dumps(data))
    assert detect_format(f) == "generic"


# ---------------------------------------------------------------------------
# ChatGPT importer
# ---------------------------------------------------------------------------

def _chatgpt_fixture(tmp_path, convs):
    f = tmp_path / "conversations.json"
    f.write_text(json.dumps(convs))
    return f


def test_import_chatgpt_basic(tmp_path, db_path):
    conv = {
        "id": "cg-001",
        "title": "My first chat",
        "create_time": 1700000000.0,
        "update_time": 1700001000.0,
        "mapping": {
            "node1": {
                "message": {
                    "author": {"role": "user"},
                    "create_time": 1700000001.0,
                    "content": {"parts": ["Hello!"]},
                }
            },
            "node2": {
                "message": {
                    "author": {"role": "assistant"},
                    "create_time": 1700000002.0,
                    "content": {"parts": ["Hi there!"]},
                }
            },
        },
    }
    f = _chatgpt_fixture(tmp_path, [conv])
    with get_connection(db_path) as conn:
        counts = import_chatgpt(f, conn)
        sessions = conn.execute("SELECT * FROM sessions").fetchall()
        messages = conn.execute("SELECT * FROM messages ORDER BY id").fetchall()

    assert counts["sessions"] == 1
    assert counts["messages"] == 2
    assert sessions[0]["source"] == "chatgpt"
    assert sessions[0]["external_id"] == "cg-001"
    assert sessions[0]["title"] == "My first chat"
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello!"
    assert messages[1]["role"] == "assistant"


def test_import_chatgpt_skips_empty_content(tmp_path, db_path):
    conv = {
        "id": "cg-002",
        "title": "Empty content",
        "create_time": None,
        "update_time": None,
        "mapping": {
            "n1": {
                "message": {
                    "author": {"role": "user"},
                    "create_time": None,
                    "content": {"parts": [""]},
                }
            },
        },
    }
    f = _chatgpt_fixture(tmp_path, [conv])
    with get_connection(db_path) as conn:
        counts = import_chatgpt(f, conn)
    assert counts["sessions"] == 1
    assert counts["messages"] == 0


def test_import_chatgpt_idempotent(tmp_path, db_path):
    conv = {
        "id": "cg-003",
        "title": "Repeat",
        "create_time": 1700000000.0,
        "update_time": 1700001000.0,
        "mapping": {
            "n1": {
                "message": {
                    "author": {"role": "user"},
                    "create_time": 1700000001.0,
                    "content": {"parts": ["Hello"]},
                }
            }
        },
    }
    f = _chatgpt_fixture(tmp_path, [conv])
    with get_connection(db_path) as conn:
        import_chatgpt(f, conn)
        import_chatgpt(f, conn)
        count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    assert count == 1  # second import is a no-op (upsert)


# ---------------------------------------------------------------------------
# Claude importer
# ---------------------------------------------------------------------------

def test_import_claude_basic(tmp_path, db_path):
    conv = {
        "uuid": "cl-001",
        "name": "Claude chat",
        "created_at": "2024-01-01T00:00:00.000Z",
        "updated_at": "2024-01-01T01:00:00.000Z",
        "chat_messages": [
            {"uuid": "m1", "sender": "human", "text": "What is AI?", "created_at": "2024-01-01T00:00:05.000Z"},
            {"uuid": "m2", "sender": "assistant", "text": "AI stands for…", "created_at": "2024-01-01T00:00:10.000Z"},
        ],
    }
    f = tmp_path / "conversations.json"
    f.write_text(json.dumps([conv]))
    with get_connection(db_path) as conn:
        counts = import_claude(f, conn)
        msgs = conn.execute("SELECT role, content FROM messages ORDER BY id").fetchall()

    assert counts["sessions"] == 1
    assert counts["messages"] == 2
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "assistant"


# ---------------------------------------------------------------------------
# Generic JSON importer
# ---------------------------------------------------------------------------

def test_import_generic_json(tmp_path, db_path):
    data = [
        {
            "id": "g1",
            "source": "slack",
            "title": "Design brainstorm",
            "started_at": "2024-03-01T09:00:00Z",
            "messages": [
                {"role": "user", "content": "Let's brainstorm!"},
                {"role": "assistant", "content": "Great idea!"},
            ],
        }
    ]
    f = tmp_path / "export.json"
    f.write_text(json.dumps(data))
    with get_connection(db_path) as conn:
        counts = import_generic_json(f, conn)
        s = conn.execute("SELECT * FROM sessions").fetchone()

    assert counts["sessions"] == 1
    assert counts["messages"] == 2
    assert s["source"] == "slack"
    assert s["title"] == "Design brainstorm"


def test_import_generic_json_defaults_source(tmp_path, db_path):
    data = [{"messages": [{"role": "user", "content": "Hi"}]}]
    f = tmp_path / "export.json"
    f.write_text(json.dumps(data))
    with get_connection(db_path) as conn:
        import_generic_json(f, conn)
        s = conn.execute("SELECT source FROM sessions").fetchone()
    assert s["source"] == "generic"


# ---------------------------------------------------------------------------
# CSV importer
# ---------------------------------------------------------------------------

def test_import_csv_basic(tmp_path, db_path):
    csv_text = (
        "session_id,role,content,title,sent_at\n"
        "sess1,user,Hello world,My CSV session,2024-01-01T10:00:00Z\n"
        "sess1,assistant,Hi there,,2024-01-01T10:00:05Z\n"
        "sess2,user,Another session,,\n"
    )
    f = tmp_path / "export.csv"
    f.write_text(csv_text)
    with get_connection(db_path) as conn:
        counts = import_csv(f, conn)
        sessions = conn.execute("SELECT * FROM sessions ORDER BY id").fetchall()
        msgs = conn.execute("SELECT * FROM messages ORDER BY id").fetchall()

    assert counts["sessions"] == 2
    assert counts["messages"] == 3
    assert sessions[0]["title"] == "My CSV session"
    assert msgs[0]["role"] == "user"
    assert msgs[0]["content"] == "Hello world"


def test_import_csv_skips_missing_session_id(tmp_path, db_path):
    csv_text = "session_id,role,content\n,user,No session id here\n"
    f = tmp_path / "bad.csv"
    f.write_text(csv_text)
    with get_connection(db_path) as conn:
        counts = import_csv(f, conn)
    assert counts["sessions"] == 0
    assert counts["skipped"] == 1

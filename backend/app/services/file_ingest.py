from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from datetime import datetime, timezone
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - optional dependency
    BeautifulSoup = None


SUPPORTED_SOURCES = {"chatgpt", "claude", "grok", "copilot"}
SUPPORTED_FORMATS = {"json", "csv", "html"}


def _epoch_to_iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    return None


def _to_text(parts: Any) -> str:
    if isinstance(parts, str):
        return parts
    if isinstance(parts, list):
        return "\n".join(str(part) for part in parts if part is not None).strip()
    if isinstance(parts, dict):
        inner = parts.get("parts")
        if isinstance(inner, list):
            return "\n".join(str(part) for part in inner if part is not None).strip()
    return ""


def _normalize_chat_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for msg in messages:
        content = _to_text(msg.get("content"))
        if not content:
            content = _to_text(msg.get("parts"))
        if not content:
            continue

        role = msg.get("role") or msg.get("author") or "unknown"
        created_at = msg.get("created_at") or _epoch_to_iso(msg.get("create_time"))
        normalized.append(
            {
                "role": str(role),
                "content": content,
                "created_at": created_at,
                "metadata": msg.get("metadata") or {},
            }
        )
    return normalized


def parse_chatgpt_json(content: bytes) -> dict[str, Any]:
    data = json.loads(content.decode("utf-8"))
    conversations = data if isinstance(data, list) else data.get("conversations", [])
    normalized: list[dict[str, Any]] = []

    for convo in conversations:
        mapping = convo.get("mapping") or {}
        messages: list[dict[str, Any]] = []
        if isinstance(mapping, dict) and mapping:
            nodes = list(mapping.values())
            nodes.sort(
                key=lambda node: (
                    node.get("message", {}).get("create_time")
                    if isinstance(node.get("message"), dict)
                    else 0
                )
                or 0
            )
            for node in nodes:
                message = node.get("message")
                if not isinstance(message, dict):
                    continue
                author = message.get("author")
                role = author.get("role") if isinstance(author, dict) else message.get("role")
                content_obj = message.get("content")
                content = _to_text(content_obj)
                if not content:
                    continue
                messages.append(
                    {
                        "role": role or "unknown",
                        "content": content,
                        "created_at": _epoch_to_iso(message.get("create_time")),
                        "metadata": {},
                    }
                )
        else:
            raw_messages = convo.get("messages") if isinstance(convo, dict) else []
            if isinstance(raw_messages, list):
                messages = _normalize_chat_messages(raw_messages)

        external_id = str(convo.get("id") or convo.get("conversation_id") or "")
        if not external_id:
            material = f"{convo.get('title', '')}:{len(messages)}"
            external_id = hashlib.sha1(material.encode("utf-8")).hexdigest()

        normalized.append(
            {
                "external_id": external_id,
                "title": convo.get("title") or "Untitled conversation",
                "metadata": {"raw_source": "chatgpt_export"},
                "created_at": _epoch_to_iso(convo.get("create_time")),
                "messages": messages,
            }
        )

    return {"source": "chatgpt", "conversations": normalized}


def parse_csv_generic(source: str, content: bytes) -> dict[str, Any]:
    text = content.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    grouped: dict[str, dict[str, Any]] = {}

    for row_index, row in enumerate(reader, start=1):
        external_id = (
            row.get("external_id")
            or row.get("conversation_id")
            or row.get("thread_id")
            or f"{source}-{row_index}"
        )
        title = row.get("title") or row.get("conversation_title") or "Imported conversation"
        created_at = row.get("created_at") or row.get("conversation_created_at")

        convo = grouped.setdefault(
            external_id,
            {
                "external_id": str(external_id),
                "title": title,
                "metadata": {"raw_source": "csv_import"},
                "created_at": created_at,
                "messages": [],
            },
        )

        message = {
            "role": row.get("role") or row.get("author") or "unknown",
            "content": row.get("content") or row.get("message") or "",
            "created_at": row.get("message_created_at") or row.get("timestamp") or created_at,
            "metadata": {"row_index": row_index},
        }
        if message["content"]:
            convo["messages"].append(message)

    return {"source": source, "conversations": list(grouped.values())}


def parse_html_generic(source: str, content: bytes, filename: str) -> dict[str, Any]:
    text = content.decode("utf-8", errors="ignore")
    title = "Imported conversation"
    candidates: list[str] = []
    if BeautifulSoup is not None:
        soup = BeautifulSoup(text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else title
        for tag in soup.find_all(["p", "div", "li", "article"]):
            line = tag.get_text(" ", strip=True)
            if line:
                candidates.append(line)
    else:
        flattened = re.sub(r"<[^>]+>", " ", text)
        candidates = [line.strip() for line in flattened.splitlines() if line.strip()]
        if filename:
            title = filename

    messages: list[dict[str, Any]] = []
    for line in candidates:
        role = "unknown"
        content_line = line
        lowered = line.lower()
        if lowered.startswith("user:"):
            role = "user"
            content_line = line[5:].strip()
        elif lowered.startswith("assistant:"):
            role = "assistant"
            content_line = line[10:].strip()
        elif lowered.startswith("system:"):
            role = "system"
            content_line = line[7:].strip()

        if content_line:
            messages.append({"role": role, "content": content_line, "created_at": None, "metadata": {}})

    external_id = hashlib.sha1(f"{source}:{filename}:{len(messages)}".encode("utf-8")).hexdigest()
    return {
        "source": source,
        "conversations": [
            {
                "external_id": external_id,
                "title": title,
                "metadata": {"raw_source": "html_import", "filename": filename},
                "created_at": None,
                "messages": messages,
            }
        ],
    }


def normalize_file_payload(source: str, fmt: str, content: bytes, filename: str) -> dict[str, Any]:
    normalized_source = source.strip().lower()
    normalized_format = fmt.strip().lower()

    if normalized_source not in SUPPORTED_SOURCES:
        raise ValueError(f"Unsupported source '{source}'. Expected one of: {sorted(SUPPORTED_SOURCES)}")
    if normalized_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{fmt}'. Expected one of: {sorted(SUPPORTED_FORMATS)}")

    if normalized_source == "chatgpt" and normalized_format == "json":
        return parse_chatgpt_json(content)
    if normalized_format == "csv":
        return parse_csv_generic(normalized_source, content)
    if normalized_format == "html":
        return parse_html_generic(normalized_source, content, filename)

    # Fallback for non-ChatGPT JSON sources.
    if normalized_format == "json":
        payload = json.loads(content.decode("utf-8"))
        if isinstance(payload, dict) and "conversations" in payload and "source" in payload:
            return payload
        if isinstance(payload, list):
            return {"source": normalized_source, "conversations": payload}
        raise ValueError("JSON format is valid, but structure is not recognized.")

    raise ValueError("Unsupported source/format combination.")

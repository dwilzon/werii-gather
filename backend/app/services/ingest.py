from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from ..db import SessionLocal
from .. import models


EXPECTED_PAYLOAD = {
    "source": "chatgpt|grok|claude|copilot",
    "conversations": [
        {
            "external_id": "...",
            "title": "...",
            "metadata": {},
            "created_at": "2024-01-01T00:00:00Z",
            "messages": [
                {"role": "user|assistant|system", "content": "...", "created_at": "...", "metadata": {}}
            ],
        }
    ],
}


def _parse_dt(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()
    if isinstance(value, (int, float)):
        try:
            return datetime.utcfromtimestamp(value)
        except (ValueError, OSError):
            return datetime.utcnow()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return datetime.utcnow()


def ingest_payload(payload: dict) -> None:
    source_name = str(payload.get("source") or "unknown")
    conversations = payload.get("conversations", [])
    if not isinstance(conversations, list):
        return

    with SessionLocal() as session:
        source = session.scalar(select(models.Source).where(models.Source.name == source_name))
        if not source:
            source = models.Source(name=source_name)
            session.add(source)
            session.commit()
            session.refresh(source)

        for convo in conversations:
            if not isinstance(convo, dict):
                continue
            external_id = convo.get("external_id") or ""
            title = convo.get("title") or ""
            metadata = convo.get("metadata") or {}
            created_at = _parse_dt(convo.get("created_at"))

            existing = session.scalar(
                select(models.Conversation)
                .where(models.Conversation.source_id == source.id)
                .where(models.Conversation.external_id == external_id)
            )
            if existing:
                continue

            conversation = models.Conversation(
                source_id=source.id,
                external_id=external_id,
                title=title,
                meta=metadata,
                created_at=created_at,
                updated_at=datetime.utcnow(),
            )
            session.add(conversation)
            session.flush()

            raw_messages = convo.get("messages", [])
            if not isinstance(raw_messages, list):
                raw_messages = []
            for msg in raw_messages:
                if not isinstance(msg, dict):
                    continue
                message = models.Message(
                    conversation_id=conversation.id,
                    role=msg.get("role", "unknown"),
                    content=msg.get("content", ""),
                    created_at=_parse_dt(msg.get("created_at")),
                    meta=msg.get("metadata", {}),
                )
                session.add(message)

        session.commit()

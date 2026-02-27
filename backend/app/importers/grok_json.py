from typing import Any


def parse_grok_json(payload: Any) -> dict:
    """Normalize Grok JSON export to unified schema."""
    # TODO: implement mapping to the unified ingest payload
    return {"source": "grok", "conversations": []}

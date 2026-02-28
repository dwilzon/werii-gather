from typing import Any


def parse_chatgpt_json(payload: Any) -> dict:
    """Normalize ChatGPT JSON export to unified schema."""
    # TODO: implement mapping to the unified ingest payload
    return {"source": "chatgpt", "conversations": []}

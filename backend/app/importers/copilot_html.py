from typing import Any


def parse_copilot_html(payload: Any) -> dict:
    """Normalize Copilot HTML export to unified schema."""
    # TODO: implement mapping to the unified ingest payload
    return {"source": "copilot", "conversations": []}

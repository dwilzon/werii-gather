from typing import Any


def parse_claude_html(payload: Any) -> dict:
    """Normalize Claude HTML export to unified schema."""
    # TODO: implement mapping to the unified ingest payload
    return {"source": "claude", "conversations": []}

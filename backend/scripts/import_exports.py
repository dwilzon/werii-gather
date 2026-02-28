#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from app.services.file_ingest import normalize_file_payload
from app.services.ingest import ingest_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import a chat export file into the session database.")
    parser.add_argument("--source", required=True, choices=["chatgpt", "claude", "grok", "copilot"])
    parser.add_argument("--format", required=True, choices=["json", "csv", "html"])
    parser.add_argument("--path", required=True, help="Absolute path to export file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = Path(args.path).expanduser().resolve()
    payload = normalize_file_payload(
        source=args.source,
        fmt=args.format,
        content=file_path.read_bytes(),
        filename=file_path.name,
    )
    ingest_payload(payload)
    print(
        f"Imported source={payload.get('source')} conversations={len(payload.get('conversations', []))} "
        f"from={file_path}"
    )


if __name__ == "__main__":
    main()

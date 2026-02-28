from pathlib import Path
from typing import Iterable
import json
import subprocess
from ..config import settings


def ensure_repo() -> Path:
    repo_path = Path(settings.artifacts_repo_path).expanduser().resolve()
    repo_path.mkdir(parents=True, exist_ok=True)
    return repo_path


def write_markdown(filename: str, content: str) -> Path:
    repo = ensure_repo()
    path = repo / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def generate_pdf(markdown_path: Path) -> Path:
    # TODO: integrate markdown->pdf (e.g., pandoc) in later step
    return markdown_path.with_suffix(".pdf")


def sync_google_docs(title: str, content: str) -> str:
    if not settings.google_docs_enabled:
        return ""
    if not settings.google_credentials_json.strip():
        return ""

    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        service_account_info = json.loads(settings.google_credentials_json)
        scopes = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/drive.file",
        ]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        docs_service = build("docs", "v1", credentials=credentials, cache_discovery=False)
        doc = docs_service.documents().create(body={"title": title}).execute()
        document_id = doc["documentId"]
        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]},
        ).execute()
        return document_id
    except Exception:
        return ""


def build_reference_docs(chunks: Iterable[str]) -> list[Path]:
    paths = []
    for i, chunk in enumerate(chunks, start=1):
        filename = f"reference-{i}.md"
        paths.append(write_markdown(filename, chunk))
    return paths


def commit_and_push_artifacts(message: str) -> bool:
    repo = ensure_repo()
    if not settings.artifacts_git_auto_push:
        return False
    if not (repo / ".git").exists():
        return False
    try:
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "-C", str(repo), "commit", "-m", message],
            check=False,
            capture_output=True,
            text=True,
        )
        subprocess.run(["git", "-C", str(repo), "push"], check=True, capture_output=True, text=True)
        return True
    except Exception:
        return False

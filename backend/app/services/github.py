from typing import Any
import requests
from ..config import settings


def create_github_issue(title: str, body: str) -> dict:
    if not settings.github_repo or not settings.github_token:
        return {"skipped": True}
    url = f"https://api.github.com/repos/{settings.github_repo}/issues"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {settings.github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.post(url, headers=headers, json={"title": title, "body": body}, timeout=30)
    if response.status_code >= 300:
        return {"skipped": False, "ok": False, "status_code": response.status_code}
    payload = response.json()
    return {"ok": True, "number": payload.get("number"), "url": payload.get("html_url")}


def create_project_item(payload: Any) -> dict:
    # TODO: integrate GitHub Projects v2 API
    return {"skipped": True}

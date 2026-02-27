# Chat Session Hub

Collects chat sessions from ChatGPT, Grok, Claude, and Copilot, normalizes them, analyzes them, and produces artifacts (Markdown, PDFs, Google Docs) plus next actions synced to GitHub.

## Features (v0.1)
- Unified ingest endpoint (`/ingest`)
- File ingest endpoint (`/ingest/file`) supporting `json`, `csv`, and `html`
- Database schema for conversations, messages, analysis, projects, tasks, artifacts
- Daily job runner that creates projects and next-action tasks from chat content
- Artifact pipeline (Markdown + Google Docs; PDF placeholder)
- GitHub issues sync for generated next actions

## Local setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment variables
- `DATABASE_URL` (default: sqlite:///./data.db)
- `ARTIFACTS_REPO_PATH` (default: `~/local/code/werii-gather`)
- `ARTIFACTS_GIT_AUTO_PUSH` (`true|false`)
- `GITHUB_TOKEN`
- `GITHUB_REPO` (e.g. `dwilzon/werii-gather`)
- `LLM_PROVIDER` (openai|anthropic|local)
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_DOCS_ENABLED` (true/false)
- `GOOGLE_CREDENTIALS_JSON` (service account JSON)
- `DAILY_TIMEZONE` (default: `America/Chicago`)
- `DAILY_HOUR` (default: `2`)
- `DAILY_MINUTE` (default: `0`)

## Ingest examples
```bash
curl -X POST http://127.0.0.1:8000/ingest/file \
  -F "source=chatgpt" \
  -F "format=json" \
  -F "file=@/absolute/path/to/chatgpt-export.json"
```

```bash
curl -X POST http://127.0.0.1:8000/ingest/file \
  -F "source=claude" \
  -F "format=html" \
  -F "file=@/absolute/path/to/claude-export.html"
```

```bash
cd backend
python scripts/import_exports.py --source chatgpt --format json --path "/absolute/path/to/chatgpt-export.json"
```

## Render deploy
Use the `render.yaml` file at the repo root. It creates:
- `chat-session-hub-web` (FastAPI)
- `chat-session-hub-daily` (cron fixed to `2:00 AM CST` = `08:00 UTC`)

## Local 2:00 AM schedule on macOS
To run at 2:00 AM local time on your Mac:
```bash
cp "/Users/david/Library/Mobile Documents/com~apple~CloudDocs/Business/Projects/Cogi/deploy/launchd/com.werii.gather.daily.plist" ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.werii.gather.daily.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.werii.gather.daily.plist
launchctl start com.werii.gather.daily
```

## Next steps
- Add robust source-specific parsers for Claude/Grok/Copilot exports
- Replace heuristic analysis with LLM-based structured extraction
- Add GitHub Projects v2 sync
- Add knowledge-graph view for connected thoughts

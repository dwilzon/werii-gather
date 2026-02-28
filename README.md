# werii-gather

> **Aggregate all your chat sessions into one central database — your creative firestorm hub.**

`werii-gather` is a lightweight Python CLI tool that ingests chat-session exports from ChatGPT, Claude, and other sources into a local SQLite database. Once imported you can list, search, tag, and measure your sessions to find patterns, track your thinking over time, and get direction from your own creative output.

---

## Features

| Capability | Details |
|---|---|
| **Multi-source import** | ChatGPT (`conversations.json`), Claude (`conversations.json`), generic JSON, flat CSV |
| **Central database** | SQLite — no server required, lives at `~/.werii-gather/gather.db` by default |
| **Search** | Full-text search across message content and session titles |
| **Tagging** | Tag sessions with topics for manual curation |
| **Metrics** | Session/message counts, activity by day, top vocabulary from your own messages |
| **Pretty terminal UI** | Powered by [Rich](https://github.com/Textualize/rich) |

---

## Installation

```bash
pip install .          # standard install
pip install -e ".[dev]" # editable install with test dependencies
```

Requires **Python 3.10+**.

---

## Quick start

```bash
# 1. Import a ChatGPT export (auto-detected)
werii-gather import ~/Downloads/conversations.json

# 2. Import a Claude export and tag it
werii-gather import ~/Downloads/claude_conversations.json --tag ai --tag claude

# 3. List all gathered sessions
werii-gather list

# 4. Search your sessions
werii-gather search "creativity"

# 5. Show a full session (with messages)
werii-gather show 42

# 6. View aggregate metrics and top topics
werii-gather metrics
```

---

## Commands

### `import FILE`

Import a chat-export file into the database.

```
werii-gather import FILE [--format auto|chatgpt|claude|generic|csv]
                         [--tag TAG]...
                         [--db PATH]
```

`--format auto` (default) detects the format from the file extension and content.  
`--tag` applies one or more tags to every session imported from that file.

### `list`

```
werii-gather list [--source chatgpt|claude|csv|generic]
                  [--limit N] [--offset N]
                  [--db PATH]
```

### `search QUERY`

```
werii-gather search QUERY [--limit N] [--db PATH]
```

Searches message content and session titles (SQL `LIKE`).

### `show SESSION_ID`

```
werii-gather show SESSION_ID [--no-content] [--db PATH]
```

Prints the full session with all messages. `--no-content` shows only metadata.

### `tag SESSION_ID TAG...`

```
werii-gather tag SESSION_ID creativity inspiration project
```

Attaches one or more tags to a session.

### `metrics`

```
werii-gather metrics [--db PATH]
```

Prints:
- Total sessions & messages
- Breakdown by source
- Sessions-started-per-day (last 30 days)
- Top 20 words you use most in your own messages

---

## Import formats

### ChatGPT

Export your data from **ChatGPT → Settings → Data controls → Export data**.  
Use the `conversations.json` file from the zip.

### Claude

Export your data from **Claude → Settings → Privacy → Export data**.  
Use the `conversations.json` file from the zip.

### Generic JSON

A JSON array of sessions:

```json
[
  {
    "id": "optional-external-id",
    "source": "slack",
    "title": "Design brainstorm",
    "started_at": "2024-03-01T09:00:00Z",
    "ended_at":   "2024-03-01T10:00:00Z",
    "messages": [
      { "role": "user",      "content": "Let's brainstorm!", "sent_at": "2024-03-01T09:00:05Z" },
      { "role": "assistant", "content": "Great idea!",       "sent_at": "2024-03-01T09:00:10Z" }
    ]
  }
]
```

`role` must be one of `user`, `assistant`, `system`, or `tool`.

### CSV

A flat CSV where each row is a message:

```csv
session_id,role,content,title,sent_at,source
sess1,user,Hello world,My session,2024-01-01T10:00:00Z,slack
sess1,assistant,Hi there,,,
sess2,user,Another session,,,
```

Required columns: `session_id`, `role`, `content`.  
Optional columns: `title`, `sent_at`, `source` (defaults to `csv`).

---

## Database location

By default the database is stored at:

```
~/.werii-gather/gather.db
```

Override with `--db /path/to/custom.db` on any command.

---

## Running tests

```bash
pytest
```

All 27 tests cover the database layer, all importers, and the metrics helpers.

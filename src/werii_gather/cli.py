"""
CLI entry point for werii-gather.

Commands
--------
  import   – Import a chat-export file into the database
  list     – List gathered sessions
  search   – Search session content
  show     – Show a single session with all messages
  metrics  – Print aggregate metrics and top topics
  tag      – Tag a session
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich import box

from .db import get_connection, tag_session, DEFAULT_DB_PATH
from .importers import IMPORTERS, detect_format
from .metrics import (
    activity_by_date,
    search_sessions,
    session_detail,
    sessions_list,
    summary,
    top_words,
)

console = Console()
err_console = Console(stderr=True, style="bold red")


def _db_option():
    return click.option(
        "--db",
        default=None,
        type=click.Path(dir_okay=False),
        help=f"Path to the SQLite database (default: {DEFAULT_DB_PATH})",
    )


@click.group()
@click.version_option()
def main():
    """werii-gather – aggregate chat sessions into one creative hub."""


# ---------------------------------------------------------------------------
# import
# ---------------------------------------------------------------------------

@main.command("import")
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format", "fmt",
    type=click.Choice(list(IMPORTERS.keys()) + ["auto"]),
    default="auto",
    show_default=True,
    help="File format; 'auto' detects from filename and content.",
)
@click.option("--tag", "tags", multiple=True, help="Tag(s) to apply to every imported session.")
@_db_option()
def import_cmd(file: Path, fmt: str, tags: tuple, db: str | None):
    """Import a chat-export FILE into the database."""
    resolved_fmt = fmt if fmt != "auto" else detect_format(file)
    importer = IMPORTERS.get(resolved_fmt)
    if importer is None:
        err_console.print(f"Unknown format: {resolved_fmt}")
        sys.exit(1)

    db_path = Path(db) if db else None
    with get_connection(db_path) as conn:
        console.print(f"Importing [bold]{file}[/bold] as [cyan]{resolved_fmt}[/cyan]…")
        counts = importer(file, conn)

        if tags:
            # Apply tags to all sessions just imported
            cur = conn.execute("SELECT id FROM sessions ORDER BY id DESC LIMIT ?",
                               (counts["sessions"],))
            for row in cur.fetchall():
                for t in tags:
                    tag_session(conn, row[0], t)

    console.print(
        f"[green]✓[/green] Imported "
        f"[bold]{counts['sessions']}[/bold] sessions, "
        f"[bold]{counts['messages']}[/bold] messages"
        + (f" ([yellow]{counts['skipped']} skipped[/yellow])" if counts.get("skipped") else "")
    )


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

@main.command("list")
@click.option("--source", default=None, help="Filter by source (chatgpt, claude, …)")
@click.option("--limit", default=50, show_default=True, help="Max rows to show")
@click.option("--offset", default=0, show_default=True, help="Pagination offset")
@_db_option()
def list_cmd(source: str | None, limit: int, offset: int, db: str | None):
    """List gathered sessions."""
    db_path = Path(db) if db else None
    with get_connection(db_path) as conn:
        rows = sessions_list(conn, source=source, limit=limit, offset=offset)

    if not rows:
        console.print("[yellow]No sessions found.[/yellow]")
        return

    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Source", style="cyan", width=10)
    table.add_column("Title", width=45, no_wrap=True)
    table.add_column("Started", width=20)
    table.add_column("Msgs", justify="right", width=6)

    for r in rows:
        table.add_row(
            str(r["id"]),
            r["source"] or "",
            r["title"] or "(untitled)",
            (r["started_at"] or "")[:19],
            str(r["message_count"]),
        )

    console.print(table)
    console.print(f"[dim]Showing {len(rows)} session(s) (offset={offset})[/dim]")


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------

@main.command()
@click.argument("query")
@click.option("--limit", default=20, show_default=True)
@_db_option()
def search(query: str, limit: int, db: str | None):
    """Search session titles and message content for QUERY."""
    db_path = Path(db) if db else None
    with get_connection(db_path) as conn:
        rows = search_sessions(conn, query, limit=limit)

    if not rows:
        console.print(f"[yellow]No results for '{query}'.[/yellow]")
        return

    table = Table(box=box.SIMPLE_HEAVY)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Source", style="cyan", width=10)
    table.add_column("Title", width=50)
    table.add_column("Started", width=20)
    table.add_column("Msgs", justify="right")

    for r in rows:
        table.add_row(
            str(r["id"]),
            r["source"] or "",
            r["title"] or "(untitled)",
            (r["started_at"] or "")[:19],
            str(r["message_count"]),
        )

    console.print(table)


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------

@main.command()
@click.argument("session_id", type=int)
@click.option("--no-content", is_flag=True, help="Hide message bodies (show metadata only)")
@_db_option()
def show(session_id: int, no_content: bool, db: str | None):
    """Show a single session and its messages."""
    db_path = Path(db) if db else None
    with get_connection(db_path) as conn:
        detail = session_detail(conn, session_id)

    if not detail:
        err_console.print(f"Session {session_id} not found.")
        sys.exit(1)

    console.rule(f"[bold]Session {detail['id']}[/bold] – {detail['title'] or '(untitled)'}")
    console.print(f"  Source   : [cyan]{detail['source']}[/cyan]")
    console.print(f"  Started  : {detail['started_at'] or '—'}")
    console.print(f"  Ended    : {detail['ended_at'] or '—'}")
    console.print(f"  Tags     : {', '.join(detail['tags']) or '—'}")
    console.print(f"  Messages : {len(detail['messages'])}")
    console.rule()

    if not no_content:
        for msg in detail["messages"]:
            role_style = "bold green" if msg["role"] == "user" else "bold blue"
            console.print(f"\n[{role_style}]{msg['role'].upper()}[/{role_style}]"
                          + (f" [{msg['sent_at'][:19]}]" if msg.get("sent_at") else ""))
            console.print(msg["content"])


# ---------------------------------------------------------------------------
# metrics
# ---------------------------------------------------------------------------

@main.command()
@_db_option()
def metrics(db: str | None):
    """Print aggregate metrics and top topics across all sessions."""
    db_path = Path(db) if db else None
    with get_connection(db_path) as conn:
        s = summary(conn)
        activity = activity_by_date(conn)
        words = top_words(conn)

    console.rule("[bold]werii-gather metrics[/bold]")
    console.print(f"  Total sessions : [bold]{s['total_sessions']}[/bold]")
    console.print(f"  Total messages : [bold]{s['total_messages']}[/bold]")

    if s["by_source"]:
        console.print("\n[bold]By source:[/bold]")
        for src, cnt in s["by_source"].items():
            console.print(f"    {src:<15} {cnt}")

    if activity:
        console.print("\n[bold]Recent activity (sessions started per day):[/bold]")
        for row in activity[:10]:
            bar = "█" * min(row["sessions"], 40)
            console.print(f"    {row['day']}  {bar} {row['sessions']}")

    if words:
        console.print("\n[bold]Top topics (most frequent words in your messages):[/bold]")
        max_cnt = words[0][1]
        for word, cnt in words:
            bar = "▪" * max(1, int(cnt / max_cnt * 30))
            console.print(f"    {word:<20} {bar} {cnt}")


# ---------------------------------------------------------------------------
# tag
# ---------------------------------------------------------------------------

@main.command()
@click.argument("session_id", type=int)
@click.argument("tags", nargs=-1, required=True)
@_db_option()
def tag(session_id: int, tags: tuple, db: str | None):
    """Add TAG(s) to a session."""
    db_path = Path(db) if db else None
    with get_connection(db_path) as conn:
        for t in tags:
            tag_session(conn, session_id, t)
    console.print(f"[green]✓[/green] Tagged session {session_id} with: {', '.join(tags)}")

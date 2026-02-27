from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models
from ..services.analysis import analyze_conversation
from ..services.docs import write_markdown, generate_pdf, sync_google_docs, commit_and_push_artifacts
from ..services.github import create_github_issue


def _upsert_project(session: Session, name: str) -> models.Project:
    existing = session.scalar(select(models.Project).where(models.Project.name == name))
    if existing:
        return existing
    project = models.Project(name=name, description=f"Auto-created from conversation analysis: {name}")
    session.add(project)
    session.flush()
    return project


def _append_tasks(
    session: Session, project: models.Project, tasks: list[dict], conversation_id: int
) -> list[models.Task]:
    created: list[models.Task] = []
    for task_payload in tasks:
        title = (task_payload.get("title") or "").strip()
        if not title:
            continue
        duplicate = session.scalar(
            select(models.Task).where(models.Task.project_id == project.id).where(models.Task.title == title)
        )
        if duplicate:
            continue
        task = models.Task(
            project_id=project.id,
            title=title,
            status=task_payload.get("status", "open"),
            next_action=True,
            meta={"conversation_id": conversation_id},
        )
        session.add(task)
        created.append(task)
    return created


def _markdown_for_conversation(
    convo: models.Conversation, analysis: dict, projects: list[models.Project], tasks: list[models.Task]
) -> str:
    project_list = "\n".join(f"- {project.name}" for project in projects) or "- Unassigned"
    task_list = "\n".join(f"- [ ] {task.title}" for task in tasks) or "- [ ] Review conversation manually"
    key_points = "\n".join(f"- {point}" for point in analysis.get("key_points", [])) or "- None"
    questions = "\n".join(f"- {question}" for question in analysis.get("open_questions", [])) or "- None"
    return (
        f"# {convo.title}\n\n"
        f"## Summary\n{analysis.get('summary', '')}\n\n"
        f"## Projects\n{project_list}\n\n"
        f"## Next Actions\n{task_list}\n\n"
        f"## Key Points\n{key_points}\n\n"
        f"## Open Questions\n{questions}\n"
    )


def _safe_node_id(label: str) -> str:
    cleaned = "".join(ch for ch in label.lower() if ch.isalnum())
    return cleaned[:32] or "node"


def _build_graph_markdown(edges: list[tuple[str, str]]) -> str:
    lines = ["# Connected Thoughts Graph", "", "```mermaid", "graph TD"]
    seen = set()
    for left, right in edges:
        node_left = _safe_node_id(left)
        node_right = _safe_node_id(right)
        key = (node_left, node_right)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f'  {node_left}["{left}"] --> {node_right}["{right}"]')
    if len(lines) == 4:
        lines.append('  empty["No graph edges yet"]')
    lines.append("```")
    return "\n".join(lines) + "\n"


def run_daily() -> None:
    graph_edges: list[tuple[str, str]] = []
    with SessionLocal() as session:
        conversations = session.scalars(select(models.Conversation)).all()
        for convo in conversations:
            analysis_exists = session.scalar(
                select(models.Analysis).where(models.Analysis.conversation_id == convo.id)
            )
            if analysis_exists:
                continue

            messages = session.scalars(
                select(models.Message).where(models.Message.conversation_id == convo.id).order_by(models.Message.id.asc())
            ).all()
            analysis = analyze_conversation(
                {
                    "id": convo.id,
                    "title": convo.title,
                    "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                }
            )

            analysis_record = models.Analysis(
                conversation_id=convo.id,
                summary=analysis.get("summary", ""),
                key_points={"items": analysis.get("key_points", [])},
                open_questions={"items": analysis.get("open_questions", [])},
            )
            session.add(analysis_record)

            projects: list[models.Project] = []
            for project_payload in analysis.get("projects", []):
                name = (project_payload.get("name") or "").strip()
                if not name:
                    continue
                projects.append(_upsert_project(session, name))

            if not projects:
                projects.append(_upsert_project(session, "General Inbox"))

            created_tasks: list[models.Task] = []
            for project in projects:
                created_tasks.extend(_append_tasks(session, project, analysis.get("tasks", []), convo.id))
                graph_edges.append((convo.title or f"Conversation {convo.id}", project.name))
            for task in created_tasks:
                graph_edges.append((projects[0].name, task.title))

            md_content = _markdown_for_conversation(convo, analysis, projects, created_tasks)
            md_path = write_markdown(f"conversations/conversation-{convo.id}.md", md_content)
            generate_pdf(md_path)
            sync_google_docs(convo.title or f"Conversation {convo.id}", md_content)

            for task in created_tasks:
                create_github_issue(
                    title=f"[Next Action] {task.title}",
                    body=f"Generated from conversation `{convo.title}` (id={convo.id}).",
                )

        session.commit()
    if graph_edges:
        write_markdown("graphs/connected-thoughts.md", _build_graph_markdown(graph_edges))
    commit_and_push_artifacts(
        message=f"daily artifacts {datetime.utcnow().strftime('%Y-%m-%d')}"
    )


if __name__ == "__main__":
    run_daily()

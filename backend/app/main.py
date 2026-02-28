from typing import Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, HTTPException, Depends, Header, status
from fastapi.responses import JSONResponse
from .config import settings
from .db import init_db
from .services.ingest import ingest_payload
from .services.file_ingest import normalize_file_payload
from .jobs.daily import run_daily

app = FastAPI(title="Chat Session Hub", version="0.1.0")


class IngestMessage(BaseModel):
    role: str = "unknown"
    content: str = ""
    created_at: str | int | float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestConversation(BaseModel):
    external_id: str = ""
    title: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | int | float | None = None
    messages: list[IngestMessage] = Field(default_factory=list)


class IngestRequest(BaseModel):
    source: str = "unknown"
    conversations: list[IngestConversation] = Field(default_factory=list)


def require_write_token(x_api_key: str | None = Header(default=None)) -> None:
    if settings.write_api_token and x_api_key != settings.write_api_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token")


async def _read_upload_with_limit(file: UploadFile, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    chunk_size = 1024 * 1024
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Uploaded file exceeds limit of {max_bytes} bytes",
            )
        chunks.append(chunk)
    return b"".join(chunks)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "env": settings.environment}


@app.post("/ingest")
async def ingest(
    payload: IngestRequest,
    background: BackgroundTasks,
    _: None = Depends(require_write_token),
) -> JSONResponse:
    # Accepts unified payloads and queues processing
    background.add_task(ingest_payload, payload.model_dump())
    return JSONResponse({"queued": True})


@app.post("/ingest/file")
async def ingest_file(
    background: BackgroundTasks,
    source: str = Form(...),
    format: str = Form(...),
    file: UploadFile = File(...),
    _: None = Depends(require_write_token),
) -> JSONResponse:
    try:
        content = await _read_upload_with_limit(file, settings.max_upload_bytes)
        payload = normalize_file_payload(source=source, fmt=format, content=content, filename=file.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to parse uploaded file: {exc}") from exc

    background.add_task(ingest_payload, payload)
    return JSONResponse(
        {
            "queued": True,
            "source": payload.get("source"),
            "conversations": len(payload.get("conversations", [])),
            "filename": file.filename,
        }
    )


@app.post("/jobs/daily")
async def daily(background: BackgroundTasks, _: None = Depends(require_write_token)) -> JSONResponse:
    background.add_task(run_daily)
    return JSONResponse({"queued": True})

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from .config import settings
from .db import init_db
from .services.ingest import ingest_payload
from .services.file_ingest import normalize_file_payload
from .jobs.daily import run_daily

app = FastAPI(title="Chat Session Hub", version="0.1.0")


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "env": settings.environment}


@app.post("/ingest")
async def ingest(payload: dict, background: BackgroundTasks) -> JSONResponse:
    # Accepts unified payloads and queues processing
    background.add_task(ingest_payload, payload)
    return JSONResponse({"queued": True})


@app.post("/ingest/file")
async def ingest_file(
    background: BackgroundTasks,
    source: str = Form(...),
    format: str = Form(...),
    file: UploadFile = File(...),
) -> JSONResponse:
    try:
        content = await file.read()
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
async def daily(background: BackgroundTasks) -> JSONResponse:
    background.add_task(run_daily)
    return JSONResponse({"queued": True})

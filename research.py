import asyncio
import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse

import pipeline
from models.schemas import ResearchRequest
from services import store

router = APIRouter(prefix="/research", tags=["research"])


@router.post("")
async def start(req: ResearchRequest):
    q = req.question.strip()
    if len(q) < 8:
        raise HTTPException(400, "Question is too short")
    job_id = uuid.uuid4().hex[:12]
    store.create(job_id, q)
    asyncio.create_task(pipeline.run(job_id, q, req.depth))
    return {"id": job_id}


@router.get("")
def history():
    return store.list_all()


@router.get("/{job_id}")
def get_one(job_id: str):
    r = store.get(job_id)
    if not r:
        raise HTTPException(404, "Not found")
    return r


@router.get("/{job_id}/stream")
async def stream(job_id: str):
    async def gen():
        i = 0
        while True:
            evs = pipeline.EVENTS.get(job_id, [])
            while i < len(evs):
                yield f"data: {json.dumps(evs[i])}\n\n"
                if evs[i]["stage"] in ("complete", "error"):
                    return
                i += 1
            r = store.get(job_id)
            if r and r["status"] != "running" and not evs:
                yield f"data: {json.dumps({'stage': 'complete', 'status': 'done'})}\n\n"
                return
            await asyncio.sleep(0.5)

    return StreamingResponse(gen(), media_type="text/event-stream")


@router.get("/{job_id}/download", response_class=PlainTextResponse)
def download(job_id: str):
    r = store.get(job_id)
    if not r or "report" not in r:
        raise HTTPException(404, "Report not ready")
    return PlainTextResponse(
        r["report"], media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="research-{job_id}.md"'},
    )

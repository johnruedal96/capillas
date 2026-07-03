import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.database import get_db
from app.schemas.api import ChatRequest
from app.services.rag import ask

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    async def event_generator():
        async for event in ask(request.query, request.messages, db):
            yield {"event": event["type"], "data": json.dumps(event, ensure_ascii=False)}

    return EventSourceResponse(event_generator(), sep="\n")

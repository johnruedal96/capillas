import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import chat, documents

app = FastAPI(title="Capillas de la Fe - Prototipo Asistente Comercial", version="0.1.0")


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(chat.router)
app.include_router(documents.router)


frontend_paths = [
    Path("/frontend"),
    Path(__file__).resolve().parent.parent.parent / "frontend",
    Path(__file__).resolve().parent.parent / "frontend",
]
frontend_path = next((p for p in frontend_paths if p.exists()), None)
if frontend_path:
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    @app.get("/")
    async def root():
        return {"status": "ok", "message": "Capillas Prototipo API", "docs": "/docs"}

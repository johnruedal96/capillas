from fastapi import FastAPI

app = FastAPI(
    title="Capillas Knowledge Base",
    version="0.1.0",
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "knowledge-base"}

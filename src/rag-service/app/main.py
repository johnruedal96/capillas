from fastapi import FastAPI

app = FastAPI(
    title="Capillas RAG Service",
    version="0.1.0",
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "rag"}

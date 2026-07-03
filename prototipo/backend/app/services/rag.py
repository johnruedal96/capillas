import json

from openai import AsyncOpenAI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.services.embeddings import embed_text
from app.services.presidio_service import anonymize_text

SYSTEM_PROMPT = """Eres un asistente comercial de Capillas de la Fe, una empresa de servicios funerarios en Colombia.

REGLAS:
1. Responde SOLO con la información proporcionada en los documentos de contexto.
2. Si la información no está en los documentos, di: "No tengo esa información en mis documentos."
3. Usa lenguaje comercial claro y directo, como hablando con un asesor.
4. Cuando sea relevante, cita la fuente del documento entre paréntesis.
5. NUNCA inventes precios, coberturas, edades ni condiciones.
6. NUNCA des consejos legales.
7. Sé empático pero profesional.
8. Responde siempre en español."""


async def search_chunks(query: str, db: AsyncSession, top_k: int = 5) -> list[dict]:
    query_embedding = embed_text(query)
    embedding_str = json.dumps(query_embedding)

    sql = text(f"""
        SELECT dc.id, dc.content, dc.chunk_index, dc.metadata_json,
               d.original_filename AS source, d.category,
               1 - (dc.embedding <=> '{embedding_str}'::vector) AS similarity
        FROM document_chunks dc
        JOIN documents d ON d.id = dc.document_id
        WHERE dc.embedding IS NOT NULL
        ORDER BY dc.embedding <=> '{embedding_str}'::vector
        LIMIT :top_k
    """)

    result = await db.execute(sql, {"top_k": top_k})
    rows = result.fetchall()

    return [
        {
            "content": row[1],
            "chunk_index": row[2],
            "metadata": json.loads(row[3]) if row[3] else {},
            "source": row[4],
            "category": row[5],
            "similarity": float(row[6]) if row[6] else 0,
        }
        for row in rows
    ]


def build_context(chunks: list[dict]) -> str:
    sections = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk.get("metadata", {})
        meta_str = ""
        doc_meta = meta.get("doc_metadata") or {}
        if doc_meta:
            meta_str = " | Metadata: " + "; ".join(f"{k}={v}" for k, v in doc_meta.items())
        sections.append(f"[Fuente {i}] Documento: {chunk['source']} | Categoría: {chunk['category']}{meta_str}\n{chunk['content']}")
    return "\n\n---\n\n".join(sections)


async def ask(query: str, history: list[dict], db: AsyncSession):
    clean_query, presidio_info = anonymize_text(query)
    
    print(f'el texto limpio {clean_query}, la info de presiodio {presidio_info}', flush=1)

    chunks = await search_chunks(clean_query, db, top_k=settings.top_k)

    if not chunks:
        yield {"type": "error", "content": "No tengo información en mis documentos para responder esta consulta."}
        return

    if len(chunks) < 2:
        yield {"type": "error", "content": "No tengo información suficiente en mis documentos para responder esta consulta."}
        return

    context = build_context(chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Contexto de documentos:\n\n{context}"},
    ]

    last_user = None
    for msg in history:
        if msg.get("role") == "user":
            last_user = msg
        else:
            if last_user:
                messages.append({"role": "user", "content": last_user["content"]})
                messages.append({"role": "assistant", "content": msg.get("content", "")})
                last_user = None

    messages.append({"role": "user", "content": f"Pregunta del asesor:\n{clean_query}"})

    if not settings.openrouter_api_key:
        yield {"type": "error", "content": "OPENROUTER_API_KEY no configurada. Creá tu .env con tu key de https://openrouter.ai/keys"}
        return

    client = AsyncOpenAI(
        base_url=settings.openrouter_base_url,
        api_key=settings.openrouter_api_key,
    )

    response = await client.chat.completions.create(
        model=settings.openrouter_model,
        messages=messages,
        stream=True,
        temperature=0.1,
        max_tokens=1024,
    )

    async for chunk in response:
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and delta.content:
            yield {"type": "token", "content": delta.content}

    sources = [{"source": c["source"], "category": c["category"], "similarity": round(c["similarity"], 3)} for c in chunks]
    yield {"type": "sources", "content": sources}
    yield {"type": "presidio", "content": presidio_info}

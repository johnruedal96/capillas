import json
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.document import Document
from app.schemas.api import DeleteResponse, DocumentListResponse, DocumentResponse
from app.services.ingestion import delete_document_chunks, process_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

CATEGORIAS = {"planes", "clientes", "objeciones", "playbooks", "reglas", "general"}
TIPOS_PERMITIDOS = {
    "application/pdf",
    "application/octet-stream",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/markdown",
    "text/plain",
}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("general"),
    metadata: str = Form("{}"),
    db: AsyncSession = Depends(get_db),
):
    if category not in CATEGORIAS:
        raise HTTPException(status_code=400, detail=f"Categoría inválida. Opciones: {', '.join(CATEGORIAS)}")

    if file.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no soportado: {file.content_type}. Permitidos: PDF, DOCX, MD",
        )

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Archivo vacío")

    try:
        parsed_meta = json.loads(metadata) if isinstance(metadata, str) else metadata
    except json.JSONDecodeError:
        parsed_meta = {}

    doc = Document(
        id=uuid.uuid4(),
        filename=file.filename,
        original_filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        category=category,
        metadata_json=json.dumps(parsed_meta, ensure_ascii=False),
        status="processing",
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    try:
        await process_document(doc, content, db)
    except Exception as e:
        print(f"[upload] error processing {file.filename}: {e}", flush=True)
        return {"message": f"Error al procesar: {e}", "document_id": str(doc.id), "status": "error", "chunk_count": 0}

    return {"message": "Documento procesado", "document_id": str(doc.id), "status": doc.status, "chunk_count": doc.chunk_count}


@router.get("", response_model=DocumentListResponse)
async def list_documents(db: AsyncSession = Depends(get_db)):
    stmt = select(Document).order_by(Document.created_at.desc())
    result = await db.execute(stmt)
    docs = result.scalars().all()

    return DocumentListResponse(
        documents=[DocumentResponse.model_validate(d) for d in docs],
        total=len(docs),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return DocumentResponse.model_validate(doc)


@router.delete("/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Document).where(Document.id == document_id)
    result = await db.execute(stmt)
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    await delete_document_chunks(doc, db)
    await db.delete(doc)
    await db.commit()

    return DeleteResponse(message="Documento eliminado", document_id=document_id)

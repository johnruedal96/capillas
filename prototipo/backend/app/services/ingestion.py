import io
import json
import re
import tempfile

import markitdown
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.document import Document, DocumentChunk
from app.services.embeddings import embed_texts


def extract_markdown(content: bytes, content_type: str, filename: str) -> str:
    if content_type == "text/markdown" or filename.endswith(".md"):
        return content.decode("utf-8")

    converter = markitdown.MarkItDown()
    suffix = {"application/pdf": ".pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx"}

    with tempfile.NamedTemporaryFile(suffix=suffix.get(content_type, ".bin"), delete=True) as tmp:
        tmp.write(content)
        tmp.flush()
        result = converter.convert(tmp.name)

    return result.text_content


def chunk_markdown(markdown: str) -> list[str]:
    chunks = []
    lines = markdown.split("\n")
    current_section = ""
    current_chunk = []

    def flush():
        nonlocal current_chunk
        if current_chunk:
            text = "\n".join(current_chunk).strip()
            if text:
                text = f"{current_section}\n{text}" if current_section else text
                chunks.append(text)
            current_chunk = []

    for line in lines:
        is_heading = bool(re.match(r"^#{1,6}\s", line))
        if is_heading:
            flush()
            if line.startswith("## "):
                current_section = line
            else:
                current_chunk.append(line)
        else:
            current_chunk.append(line)

        text_so_far = "\n".join(current_chunk)
        if len(text_so_far) > settings.chunk_size:
            flush()

    flush()
    return chunks if chunks else [markdown]


async def process_document(doc: Document, file_content: bytes, db: AsyncSession):
    try:
        md_content = extract_markdown(file_content, doc.content_type, doc.filename)
        md_content = md_content.replace("\x00", "")
        doc.markdown_content = md_content

        raw_chunks = chunk_markdown(md_content)
        chunks = [c for c in raw_chunks if len(c.strip()) > 20]

        embeddings = embed_texts(chunks)

        doc_meta = json.loads(doc.metadata_json) if doc.metadata_json else {}
        for i, (text, emb) in enumerate(zip(chunks, embeddings)):
            chunk_meta = {
                "category": doc.category,
                "source": doc.original_filename,
                "chunk": i,
            }
            if doc_meta:
                chunk_meta["doc_metadata"] = doc_meta
            chunk = DocumentChunk(
                document_id=doc.id,
                content=text,
                chunk_index=i,
                embedding=emb,
                metadata_json=json.dumps(chunk_meta, ensure_ascii=False),
            )
            db.add(chunk)

        doc.chunk_count = len(chunks)
        doc.status = "ready"
        await db.commit()

    except Exception as e:
        await db.rollback()
        doc.status = "error"
        doc.error_message = str(e)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
        raise


async def delete_document_chunks(doc: Document, db: AsyncSession):
    stmt = select(DocumentChunk).where(DocumentChunk.document_id == doc.id)
    result = await db.execute(stmt)
    chunks = result.scalars().all()
    for chunk in chunks:
        await db.delete(chunk)
    await db.commit()

# Prototipo — Asistente Comercial Capillas de la Fe

Prototipo funcional del sistema de asesor comercial aumentado con IA usando RAG + OpenRouter.

## Stack

| Componente | Tecnología |
|---|---|
| API | FastAPI (Python 3.12) |
| Vector DB | PostgreSQL 16 + pgvector |
| Embeddings | sentence-transformers (local, gratis) |
| LLM | OpenRouter (configurable) |
| PII Filter | Microsoft Presidio |
| Frontend | HTML + JS vanilla |
| Contenedores | Docker Compose |

## Requisitos

- Docker + Docker Compose
- API key de [OpenRouter](https://openrouter.ai/keys)

## Configuración

```bash
cp backend/.env.example backend/.env
# Editar backend/.env y poner tu OPENROUTER_API_KEY
```

## Inicio

```bash
docker compose up --build
```

Abrir http://localhost:8000

## Uso

1. **Cargar documentos**: Ir a la pestaña Documentos, seleccionar archivo (PDF/DOCX/MD) y categoría. El sistema convierte a Markdown, divide en chunks, genera embeddings y los indexa en pgvector.

2. **Chat**: Ir a la pestaña Chat y preguntar sobre planes, coberturas, clientes, objeciones o reglas de negocio. Las respuestas se generan en tiempo real con fuentes citadas.

3. **Administrar**: Ver documentos cargados con su estado, categoría y número de chunks. Eliminar documentos cuando sea necesario.

## Estructura

```
prototipo/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init.sql
│   ├── .env.example
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models/document.py
│       ├── schemas/api.py
│       ├── routers/chat.py
│       ├── routers/documents.py
│       └── services/
│           ├── embeddings.py
│           ├── ingestion.py
│           ├── presidio_service.py
│           └── rag.py
├── frontend/
│   └── index.html
└── knowledge_base/
    ├── planes/
    ├── clientes/
    ├── objeciones/
    ├── playbooks/
    └── reglas/
```

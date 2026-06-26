# AGENTS.md — Instrucciones del Proyecto

## Proyecto: Asistente Comercial IA — Capillas de la Fe

### Stack Principal
- **Frontend**: Lit 3 (Web Components), Vite (IIFE build), Custom Elements
- **Backend**: FastAPI (Python 3.12), gRPC, SSE streaming
- **RAG**: LlamaIndex, pgvector, text-embedding-3-small (OpenAI), Claude (Bedrock)
- **Infra**: AWS (ECS Fargate, Aurora Serverless v2, Cognito, API Gateway, CloudFront, S3)
- **Cache**: Redis + Semantic Cache
- **Auth**: Amazon Cognito + OAuth 2.0 + OIDC + PKCE + BFF pattern
- **Presentaciones**: Marp CLI + tema personalizado (grises corporativos)
- **Documentación técnica**: ADRs (MADR 4.0), Especificaciones Técnicas

### Estructura del Proyecto
```
capillas/
├── opencode.json              # Configuración opencode
├── AGENTS.md                  # Estas instrucciones
├── .opencode/skills/template/ # Plantilla de skill personalizado
├── docs/
│   ├── propuesta_estrategica.md     # Propuesta de negocio
│   ├── propuesta_tecnologica.md     # Propuesta técnica (generada)
│   ├── contexto_base.md             # Contexto del mercado
│   ├── rag_base.md                  # Arquitectura RAG
│   ├── adr/                         # Architecture Decision Records (MADR)
│   │   ├── README.md                # Guía de uso
│   │   ├── CHANGELOG.md             # Registro de ADRs
│   │   ├── 0000-template.md         # Plantilla MADR
│   │   └── 0001-use-adrs.md         # ADR fundacional
│   ├── specs/                       # Especificaciones técnicas
│   │   └── TEMPLATE.md              # Plantilla de spec por servicio
│   ├── slides/                      # Presentaciones Marp
│   │   ├── README.md                # Cómo usar Marp
│   │   ├── theme-capillas.css       # Tema personalizado (grises corporativos)
│   │   ├── pitch-deck.md            # Deck técnico-comercial
│   │   ├── prompts-imagenes.md      # Prompts para diagramas técnicos
│   │   └── imagenes/                # Imágenes generadas externamente
│   └── tools/                       # Herramientas del proyecto
│       └── STACK.md                 # Testing, calidad, monitoreo
├── src/
│   ├── widget/            # Frontend Lit 3 (IIFE bundle)
│   │   ├── src/
│   │   │   ├── widget/index.ts
│   │   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── communication/
│   │   │   └── styles/
│   │   ├── package.json
│   │   └── vite.config.ts
│   ├── bff/               # Backend for Frontend (FastAPI)
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routers/
│   │   │   ├── services/
│   │   │   └── models/
│   │   └── Dockerfile
│   ├── rag-service/       # RAG Service (LlamaIndex)
│   │   ├── app/
│   │   │   ├── rag/
│   │   │   ├── embedding/
│   │   │   ├── retrieval/
│   │   │   └── generation/
│   │   └── Dockerfile
│   ├── knowledge-base/    # Knowledge Base Service
│   │   ├── app/
│   │   └── Dockerfile
│   └── analytics/         # Analytics Service
│       ├── app/
│       └── Dockerfile
├── infra/
│   └── terraform/         # IaC
│       ├── modules/
│       └── environments/
├── knowledge-base/        # Documentos fuente
│   ├── planes/
│   ├── objetos/
│   ├── playbooks/
│   ├── clientes/
│   └── reglas/
└── tests/
```

### Convenciones
- **Código**: TypeScript/Python, tipado fuerte, sin comentarios
- **Commits**: Prefijos convencionales (feat:, fix:, infra:, docs:)
- **Branch**: feat/, fix/, infra/ seguido del nombre

### Agentes Disponibles
- `widget-dev`: Desarrolla widget frontend Lit 3
- `bff-dev`: Desarrolla BFF FastAPI + SSE
- `rag-dev`: Desarrolla RAG Service con LlamaIndex
- `infra-dev`: Desarrolla infraestructura AWS Terraform

Skills proporcionan instrucciones especializadas y flujos de trabajo para tareas específicas.
Usar la herramienta `skill` para cargar un skill cuando una tarea coincida con su descripción.

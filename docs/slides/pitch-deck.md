<!--
theme: capillas
size: 16:9
headingDivider: false
-->

<!-- _class: lead -->
<!-- _paginate: false -->

# Asesor Comercial Aumentado con IA

### Propuesta de Arquitectura Técnica

**Capillas de la Fe** — Junio 2026

Clasificación: Confidencial

Tasa de cambio de referencia: $1 USD = $3,450 COP

<!--
note: Agradecer la atención. Esta presentación detalla la arquitectura, componentes,
costos de infraestructura y stack tecnológico del sistema de asesor comercial aumentado.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

## El Problema Técnico

---

## El Problema Técnico

### Fragmentación del conocimiento comercial

- Base de conocimiento distribuida en documentos Word, PDFs, presentaciones y experiencia individual
- Sin mecanismo de consulta en tiempo real durante la interacción con el cliente
- Sin control de versiones ni consistencia en las respuestas entre asesores

### Limitaciones de la infraestructura actual

- Sin API unificada para consumir información comercial
- Sin trazabilidad de consultas ni métricas de uso
- Sin capacidad de escalar horizontalmente

### Oportunidad

- Un widget embebible en cualquier app existente (sin migrar plataforma)
- Respuestas basadas en documentos oficiales — no en LLM genérico
- Tiempo real, streaming, multicanal

---

<!-- _class: section -->
<!-- _paginate: false -->

## Arquitectura General

---

## Arquitectura General

![Arquitectura General del Sistema width:900](./imagenes/arquitectura-general.png)

<!--
note: Este diagrama muestra la arquitectura completa. La explico componente por
componente en las siguientes slides.
-->

### Capas del sistema

| Capa | Componente | Tecnología |
|------|-----------|------------|
| **Presentación** | Widget embebible | Lit 3 + Custom Elements (IIFE bundle ~20KB gzip) |
| **Autenticación** | BFF + Cognito | OAuth 2.0 + OIDC + PKCE + httpOnly sessions |
| **API / BFF** | Backend for Frontend | FastAPI (Python 3.12) + SSE streaming |
| **RAG** | Retrieval-Augmented Generation | LlamaIndex + pgvector |
| **LLM** | Modelo de lenguaje | Claude Sonnet 4.6 (Bedrock) |
| **Caché** | Semantic cache | Redis |
| **Datos** | Base vectorial + documentos | Aurora PostgreSQL + S3 |
| **Infraestructura** | Cloud | AWS (ECS Fargate + CloudFront + API Gateway) |

---

<!-- _class: section -->
<!-- _paginate: false -->

## Componente 1: Widget Frontend

---

## Componente 1: Widget Frontend

### Lit 3 + Custom Elements + Vite IIFE

**Especificación técnica**

| Atributo | Valor |
|----------|-------|
| Framework | Lit 3 (Web Components estándar) |
| Bundle | IIFE — ~20KB gzip (~60KB sin comprimir) |
| Shadow DOM | Sí — aislado del CSS del host |
| Dependencias del host | Cero — no requiere React, Vue, jQuery ni ningún framework |
| Integración | Un `<script>` tag + un custom element `<asesor-ia>` |

**Modalidades de despliegue**

| Modalidad | Auth provista por | Ideal para |
|-----------|------------------|------------|
| Widget solo | Cliente (app existente) | WordPress, Shopify, React, HTML plano |
| App completa | Nosotros (Cognito) | Cuando no hay app existente |

**Configuración vía atributos HTML**

```html
<asesor-ia
  api-key="..."
  api-base="https://api.capillas.app"
  position="bottom-right"
  idioma="es"
></asesor-ia>
<script src="https://cdn.capillas.app/widget.js"></script>
```

<!--
note: El widget es el punto de entrada del usuario. Corre en el navegador del
asesor, embebido en cualquier aplicación existente. No requiere migración.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

## Componente 2: BFF (Backend for Frontend)

---

## Componente 2: BFF (Backend for Frontend)

### FastAPI + Cognito BFF Pattern + SSE Streaming

**Responsabilidades**

- Proxy de autenticación (Cognito BFF): maneja el flujo OAuth PKCE sin exponer tokens al navegador
- Gestión de sesiones persistentes vía Redis (httpOnly cookies)
- Endpoint `/chat` con streaming SSE (Server-Sent Events)
- Rate limiting por usuario y por IP
- Validación y sanitización de entradas
- Cliente gRPC para comunicación con RAG Service

**Stack**

| Componente | Tecnología |
|-----------|------------|
| Framework | FastAPI (Python 3.12) |
| Async runtime | Uvicorn + `asyncio` |
| Streaming | SSE via `StreamingResponse` |
| Sesiones | Redis (cookies `httpOnly` + `SameSite=Strict`) |
| Comunicación interna | gRPC (protobuf) |
| Rate limiting | Token bucket en Redis |
| Logs estructurados | Structlog + OpenTelemetry |

![Diagrama de componentes del BFF width:700](./imagenes/arquitectura-bff.png)

---

<!-- _class: section -->
<!-- _paginate: false -->

## Componente 3: RAG Service

---

## Componente 3: RAG Service

### LlamaIndex + pgvector + Claude (Bedrock)

**Pipeline de Retrieval-Augmented Generation**

| Etapa | Descripción | Tecnología |
|-------|------------|------------|
| **1. Ingestión** | Carga y chunking de documentos | LlamaIndex `SimpleDirectoryReader` |
| **2. Embedding** | Vectorización a 512 dimensiones | `text-embedding-3-small` (MRL) |
| **3. Indexación** | Almacenamiento vectorial | pgvector sobre Aurora PostgreSQL |
| **4. Retrieval** | Búsqueda híbrida (vectorial + keyword) | LlamaIndex `VectorIndexRetriever` |
| **5. Reranking** | Reordenamiento de resultados | Modelo de reranking local |
| **6. Generación** | Construcción de prompt + respuesta LLM | Claude Sonnet 4.6 (Bedrock) |
| **7. Cache** | Semantic cache de respuestas | Redis (hash de embedding + umbral coseno) |

**Costos de embedding**

| Modelo | Costo input | Costo output | Dims |
|--------|------------|-------------|------|
| text-embedding-3-small | ~$69 COP/1M tokens | N/A | 512 (MRL) |
| Claude Sonnet 4.6 | ~$10,350 COP/MTok | ~$51,750 COP/MTok | — |
| Claude Haiku 4.5 | ~$3,450 COP/MTok | ~$17,250 COP/MTok | — |

<!--
note: semantic cache puede reducir costos de LLM hasta 68%.
Cada consulta primero verifica cache, si hay match semántico (similitud coseno > umbral),
devuelve respuesta cachead sin llamar a Bedrock.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

## Componente 4: Knowledge Base

---

## Componente 4: Knowledge Base

### Pipeline de ingestión y versionado de documentos

**Fuentes de datos**

| Fuente | Formato | Volumen estimado | Frecuencia de actualización |
|--------|---------|------------------|---------------------------|
| Planes funerarios | PDF, DOCX | ~200 páginas | Trimestral |
| Objetos y coberturas | MD, PDF | ~100 páginas | Trimestral |
| Playbooks de venta | MD | ~50 páginas | Mensual |
| FAQ y objeciones | MD | ~30 páginas | Quincenal |
| Reglas de negocio | MD | ~20 páginas | Mensual |

**Pipeline**

1. **Subida** — Documento subido vía API o interfaz admin
2. **Validación** — Verificación de formato, permisos, duplicados
3. **Chunking** — División en fragmentos de ~512 tokens con overlap de 64
4. **Embedding** — Vectorización con text-embedding-3-small
5. **Indexación** — Inserción en pgvector con metadatos (fuente, versión, fecha)
6. **Versionado** — Cada cambio crea una nueva versión; el retrieval siempre usa la activa

**Almacenamiento**

| Tipo | Almacenamiento | Costo estimado |
|------|---------------|---------------|
| Documentos fuente | S3 Standard | ~$800 COP/GB/mes |
| Vectores + metadatos | Aurora PostgreSQL + pgvector | Incluido en ACU |
| Caché de respuestas | Redis | Incluido en instancia |

---

<!-- _class: section -->
<!-- _paginate: false -->

## Infraestructura AWS

---

## Infraestructura AWS

![Infraestructura AWS width:900](./imagenes/infraestructura-aws.png)

### Servicios utilizados

| Servicio | Propósito | Tipo |
|----------|-----------|------|
| **ECS Fargate** | Orquestación de contenedores (BFF, RAG, KB) | Serverless (sin EC2) |
| **Aurora Serverless v2** | Base de datos PostgreSQL + pgvector | Serverless (escala a 0) |
| **S3** | Almacenamiento de documentos fuente | Object storage |
| **CloudFront** | CDN + distribución del widget + assets | Edge caching |
| **API Gateway HTTP** | Endpoint público del widget | Serverless |
| **Cognito** | Autenticación y autorización | Managed service |
| **Bedrock** | LLM (Claude) vía API | Managed service |
| **Redis / MemoryDB** | Caché de sesiones + semantic cache | In-memory |
| **KMS** | Cifrado de llaves y secretos | HSM-managed |
| **ELB (ALB)** | Load balancing interno | Application LB |

---

<!-- _class: section -->
<!-- _paginate: false -->

## Seguridad

---

## Seguridad

### Autenticación y cifrado

![Flujo de autenticación y seguridad width:900](./imagenes/seguridad-auth.png)

<!--
note: El flujo OAuth PKCE garantiza que el widget nunca tenga acceso directo
a tokens. El BFF actúa como proxy, manteniendo las sesiones en cookies httpOnly.
-->

| Capa | Mecanismo |
|------|-----------|
| **Autenticación** | Amazon Cognito + OAuth 2.0 + OIDC + PKCE |
| **Autorización** | Roles IAM + políticas de acceso por servicio |
| **Transporte** | TLS 1.3 + mTLS entre servicios internos |
| **Payload** | AES-256-GCM cifrado extremo a extremo |
| **Secretos** | AWS KMS con rotación automática |
| **Headers** | Headers personalizados cifrados + validación |
| **Rate limiting** | Token bucket (Redis) por usuario + IP |
| **Input validation** | Pydantic v2 (schemas estrictos) |

---

<!-- _class: section -->
<!-- _paginate: false -->

## Costos de Infraestructura AWS

---

## Costos de Infraestructura AWS

> Costos de servicios en la nube AWS. No incluye desarrollo, soporte ni margen de servicio.

### Por servicio — Escenario Producción (100 asesores)

| Servicio | Configuración | Costo/mes (USD) | Costo/mes (COP) |
|----------|--------------|-----------------|-----------------|
| ECS Fargate (BFF + RAG) | 2 servicios × 0.5 vCPU + 1 GB | ~$80 | ~$276,000 |
| Aurora Serverless v2 | 2 ACU promedio + 20 GB storage | ~$90 | ~$310,500 |
| S3 + CloudFront | 5 GB storage + 50 GB transfer | ~$10 | ~$34,500 |
| API Gateway HTTP | ~500K requests/mes | ~$5 | ~$17,250 |
| Cognito | 100 MAU (dentro del tier gratis) | $0 | $0 |
| Bedrock Claude | ~500K tokens input + ~100K output | ~$30 | ~$103,500 |
| Redis / MemoryDB | t4g.small (1.5 GB) | ~$25 | ~$86,250 |
| KMS | 2 keys + API calls | ~$3 | ~$10,350 |
| ALB + Data transfer | 1 ALB + NAT Gateway | ~$35 | ~$120,750 |

### Consolidado por escenario

| Escenario | Usuarios | Costo/mes (USD) | Costo/mes (COP) |
|-----------|----------|-----------------|-----------------|
| **MVP / Desarrollo** | < 10 asesores | ~$90–170 | ~$314,000–586,000 |
| **Producción** | 100 asesores | ~$525 | ~$1,804,000 |
| **Escalado** | 500+ asesores | ~$1,306 | ~$4,506,000 |

---

<!-- _class: section -->
<!-- _paginate: false -->

## Stack Tecnológico Completo

---

## Stack Tecnológico Completo

| Capa | Tecnología | Versión | Licencia |
|------|-----------|---------|----------|
| **Frontend** | Lit 3 + Custom Elements | 3.x | BSD-3 |
| **BFF** | FastAPI (Python) | 3.12 + FastAPI 0.115 | MIT |
| **RAG** | LlamaIndex | 0.12.x | MIT |
| **Vector DB** | pgvector (Aurora PostgreSQL) | 0.8+ | PostgreSQL |
| **Embeddings** | text-embedding-3-small | API OpenAI | Pago por uso |
| **LLM** | Claude Sonnet 4.6 / Haiku 4.5 | Bedrock | Pago por uso |
| **Cache** | Redis / MemoryDB | 7.x | BSD-3 |
| **Auth** | Cognito + OAuth 2.0 + OIDC + PKCE | — | AWS managed |
| **Infra** | ECS Fargate + API Gateway + S3 + CloudFront | — | AWS |
| **Observabilidad** | OpenTelemetry + Grafana + Sentry | — | Open source |
| **CI/CD** | GitHub Actions + ECR + ECS | — | Gratuito |

---

<!-- _class: lead -->
<!-- _paginate: false -->

## Siguientes pasos

### Discutamos los detalles

<!--
note: La solución está diseñada para integrarse sin fricción con la
infraestructura existente de Capillas de la Fe. Podemos ajustar cada
componente según sus necesidades específicas.
-->

**Contacto:**

[Correo electrónico] · [Teléfono]

---

Esta presentación se generó con Marp. Tema personalizado disponible en `theme-capillas.css`.
Para ver en vivo: `marp --theme theme-capillas.css --watch pitch-deck.md`

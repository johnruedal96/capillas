# PROPUESTA TECNOLÓGICA
## Sistema de Asesor Comercial Aumentado con IA — Capillas de la Fe

**Versión:** 1.0  
**Fecha:** Junio 2026  
**Clasificación:** Confidencial — Capillas de la Fe

---

## Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Stack Tecnológico Detallado](#3-stack-tecnológico-detallado)
4. [Comparativa Cloud Provider](#4-comparativa-cloud-provider)
5. [Seguridad](#5-seguridad)
6. [Plan de Implementación](#6-plan-de-implementación)
7. [Estimación de Costos](#7-estimación-de-costos)
8. [Referencias y Fuentes](#8-referencias-y-fuentes)

---

## 1. Resumen Ejecutivo

### 1.1 Objetivo del Sistema

Implementar un **Asistente Comercial Inteligente** basado en arquitectura RAG (Retrieval-Augmented Generation) que potencie a la fuerza de ventas de Capillas de la Fe con inteligencia artificial en tiempo real. El sistema permite a cada asesor acceder a información confiable, recomendaciones de planes, argumentos de venta personalizados y manejo de objeciones, todo desde un widget embebible en cualquier aplicación.

### 1.2 Stack Tecnológico Recomendado

| Capa | Tecnología | Especificación |
|------|-----------|----------------|
| **Frontend (Widget)** | Lit 3 + Custom Elements + Vite IIFE | Bundle ~20KB gzip, Shadow DOM nativo, 0 dependencias del host |
| **Autenticación** | Amazon Cognito + OAuth 2.0 + OIDC + PKCE | 10K MAU gratis, MFA, SSO SAML/OIDC |
| **Backend** | FastAPI (Python 3.12) + gRPC | Async nativo, SSE streaming, tipado fuerte |
| **RAG Orchestration** | LlamaIndex (retrieval) + LangChain (agentes) | Mejor RAG out-of-box + agentes complejos |
| **Vector Database** | Aurora PostgreSQL Serverless v2 + pgvector | Escala a 0 ACU (~$43/mes idle), SQL + vectores |
| **Embeddings** | text-embedding-3-small (512d MRL) | $0.02/1M tokens, 1,536 dims configurables |
| **LLM Principal** | Claude Sonnet 4.6 (Bedrock) | $3/$15 por MTok, 200K contexto |
| **LLM Económico** | Claude Haiku 4.5 (Bedrock) | $1/$5 por MTok, tareas simples de alto volumen |
| **Caché** | Redis + Semantic Cache | Reduce costos LLM hasta 68%, latencia <10ms en cache hit |
| **Infraestructura** | ECS Fargate + S3 + CloudFront + API Gateway HTTP | Serverless-first, sin Kubernetes |
| **Cifrado** | AWS KMS + ACM (TLS 1.3) + mTLS | ACM gratuito, KMS ~$1/key/mes |
| **Observabilidad** | OpenTelemetry + LangFuse (self-hosted) + Grafana | Datos soberanos, trazabilidad completa |
| **CI/CD** | GitHub Actions + ECR + ECS | Despliegue automatizado blue/green |

### 1.3 Costo Mensual Estimado

| Etapa | Costo/mes | Usuarios | Descripción |
|-------|-----------|----------|-------------|
| **MVP / Desarrollo** | ~$200-400/mes | < 10 asesores | 1-2 microservicios, instancias pequeñas |
| **Producción inicial** | ~$400-800/mes | 100 asesores | 3-5 servicios, HA parcial |
| **Escalado** | ~$800-1,500/mes | 500+ asesores | HA completa, múltiples AZ |

---

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Componentes (Nivel 1)

```
                           ┌──────────────────────┐
                           │     HOST APP          │
                           │  (WordPress, PHP,     │
                           │   React, jQuery...)   │
                           └──────────┬───────────┘
                                      │ <script src="cdn/widget.js">
                                      │ <mi-widget api-key="xxx">
                                      ▼
                           ┌──────────────────────┐
                           │   WIDGET (Lit 3)     │
                           │   Custom Element     │
                           │   Shadow DOM         │
                           │   ~20KB gzip         │
                           └──────────┬───────────┘
                                      │ HTTPS · TLS 1.3
                                      │ Authorization: Bearer <JWT>
                                      ▼
                    ┌──────────────────────────────────┐
                    │       CLOUDFRONT CDN              │
                    │   (Widget estático: index.html,   │
                    │    bundle.js, estilos)            │
                    └──────────────────────────────────┘
                                      │
                    ┌──────────────────────────────────┐
                    │      API GATEWAY HTTP             │
                    │  • Rate limiting (100 req/min)    │
                    │  • JWT validation (Cognito)       │
                    │  • Request routing                │
                    │  • TLS termination                │
                    └────────────────┬─────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │  BFF SERVICE    │   │  AUTH SERVICE   │   │ ANALYTICS SVC   │
    │  (ECS Fargate)  │   │  (Cognito)      │   │  (ECS Fargate)  │
    │  • FastAPI       │   │  • OAuth 2.0    │   │  • Métricas     │
    │  • SSE Streaming │   │  • User pools   │   │  • Feedback     │
    │  • Session mgmt  │   │  • MFA          │   │  • Logs         │
    └────────┬─────────┘   └─────────────────┘   └─────────────────┘
             │
             │ gRPC + mTLS
             ▼
    ┌──────────────────────────────────────────────────────────┐
    │                    RAG SERVICE (ECS Fargate)              │
    │                                                          │
    │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
    │   │  Query   │  │  Hybrid  │  │  Cross-  │  │  LLM   │ │
    │   │  Rewrite │─▶│  Search  │─▶│ encoder  │─▶│  Call  │ │
    │   │          │  │  (RRF)   │  │ Reranker │  │ Claude │ │
    │   └──────────┘  └────┬─────┘  └──────────┘  └───┬────┘ │
    │                      │                           │      │
    └──────────────────────┼───────────────────────────┼──────┘
                           │                           │
              ┌────────────┘                           └──────────┐
              ▼                                                    
    ┌──────────────────┐                                 ┌──────────────┐
    │  Aurora Serverless│                                 │  Amazon      │
    │  v2 + pgvector    │                                 │  Bedrock     │
    │  • Vectores       │                                 │  • Claude    │
    │  • Conversaciones │                                 │  • Titan Emb │
    │  • Usuarios       │                                 │  • Guardrails│
    │  • Metadata       │                                 └──────────────┘
    └──────────────────┘

    ┌──────────────────┐
    │  Redis           │
    │  • Semantic Cache│
    │  • Rate limiting │
    │  • Sesiones      │
    └──────────────────┘

    ┌──────────────────┐
    │  AWS KMS         │
    │  • Cifrado datos │
    │  • Secrets       │
    └──────────────────┘
```

### 2.2 Flujo de Consulta (Asesor → Respuesta)

```
ASESOR                    WIDGET                  BFF                  RAG SERVICE           pgvector        Bedrock
  │                         │                     │                      │                     │               │
  │  "¿Qué plan para        │                     │                      │                     │               │
  │   familia de 4          │                     │                      │                     │               │
  │   con $50/mes?"         │                     │                      │                     │               │
  │────────────────────────▶│                     │                      │                     │               │
  │                         │  POST /api/chat     │                      │                     │               │
  │                         │  {query, context}   │                      │                     │               │
  │                         │────────────────────▶│                      │                     │               │
  │                         │                     │  │ Validar token     │                     │               │
  │                         │                     │  │ Enriquecer ctx    │                     │               │
  │                         │                     │  gRPC Query(query)  │                     │               │
  │                         │                     │────────────────────▶│                     │               │
  │                         │                     │                      │  │ Query Rewrite   │               │
  │                         │                     │                      │  │                 │               │
  │                         │                     │                      │  │ Cache Lookup    │               │
  │                         │                     │                      │  │──── Cache ──────│               │
  │                         │                     │                      │  │    MISS         │               │
  │                         │                     │                      │  │                 │               │
  │                         │                     │                      │  │ Hybrid Search   │               │
  │                         │                     │                      │  │ (BM25+vector)   │               │
  │                         │                     │                      │  │────────────────▶│               │
  │                         │                     │                      │  │ Top 20 chunks   │               │
  │                         │                     │                      │  │◀────────────────│               │
  │                         │                     │                      │  │                 │               │
  │                         │                     │                      │  │ Reranker        │               │
  │                         │                     │                      │  │ Parent-child    │               │
  │                         │                     │                      │  │                 │               │
  │                         │                     │                      │  │ Invoke Claude   │               │
  │                         │                     │                      │  │────────────────────────────────▶│
  │                         │                     │                      │  │                 │               │
  │                         │                     │                      │  │◀────────────────────────────────│
  │                         │                     │                      │  │ Respuesta       │               │
  │                         │                     │                      │  │                 │               │
  │                         │                     │  ◀───────────────────│  │                 │               │
  │                         │                     │  Response + sources  │  │                 │               │
  │                         │  SSE Stream         │                     │                     │               │
  │                         │◀────────────────────│                     │                     │               │
  │                         │  data: {"type":     │                     │                     │               │
  │                         │  "token","content": │                     │                     │               │
  │                         │  "Te recomiendo..."}│                     │                     │               │
  │  "Te recomiendo         │                     │                     │                     │               │
  │   Plan Familiar         │                     │                     │                     │               │
  │   Premium..."           │                     │                     │                     │               │
  │◀────────────────────────│                     │                     │                     │               │
```

### 2.3 Flujo de Autenticación OAuth 2.0 + PKCE + BFF

```
HOST APP         WIDGET            POPUP           COGNITO           BFF              API
   │                │                │                │                │                │
   │  Carga widget  │                │                │                │                │
   │───────────────▶│                │                │                │                │
   │                │  Detectar no   │                │                │                │
   │                │  autenticado   │                │                │                │
   │                │  Mostrar login │                │                │                │
   │                │                │                │                │                │
   │                │  Click "Login" │                │                │                │
   │                │────────────────│               │                │                │
   │                │  window.open() │                │                │                │
   │                │  con PKCE      │                │                │                │
   │                │                │  Auth Request  │                │                │
   │                │                │───────────────▶│                │                │
   │                │                │                │  Login form    │                │
   │                │                │◀───────────────│                │                │
   │                │                │  Credenciales  │                │                │
   │                │                │───────────────▶│                │                │
   │                │                │                │  Auth Code     │                │
   │                │                │◀───────────────│                │                │
   │                │                │                │                │                │
   │                │                │  POST /auth/   │                │                │
   │                │                │  token {code,  │                │                │
   │                │                │  verifier}     │                │                │
   │                │                │────────────────────────────────▶│                │
   │                │                │                │                │  Validate code  │
   │                │                │                │  Token Request │                │
   │                │                │                │◀───────────────│                │
   │                │                │                │  Tokens        │                │
   │                │                │                │───────────────▶│                │
   │                │                │                │                │  Set HttpOnly  │
   │                │                │                │                │  cookie RT      │
   │                │                │                │                │                │
   │                │                │  postMessage   │                │                │
   │                │                │  (access_token)│                │                │
   │                │◀───────────────│                │                │                │
   │                │                │                │                │                │
   │                │  Almacenar AT  │                │                │                │
   │                │  in-memory     │                │                │                │
   │                │  Render UI     │                │                │                │
   │                │  autenticada   │                │                │                │
   │                │                │                │                │                │
   │                │  API Call      │                │                │                │
   │                │  Authorization:│                │                │                │
   │                │  Bearer <AT>   │                │                │                │
   │                │───────────────────────────────────────────────────────────────▶│
```

### 2.4 Flujo de Seguridad (Anti-MITM, Cifrado)

```
                          CAPA EXTERNA (Internet)              CAPA INTERNA (AWS VPC)
┌─────────────┐    TLS 1.3    ┌──────────────────┐   mTLS     ┌──────────────────┐
│  ASESOR     │──────────────▶│  API Gateway     │───────────▶│  BFF Service     │
│  (Widget)   │  HSTS         │  (Edge)          │  Cert      │  (Internal)      │
│             │  PFS          │  • ACM cert      │  Cliente   │                  │
│  JWT in-    │  Cert Pin     │  • Rate limit    │  Server    │  • Access token  │
│  memory     │               │  • WAF (Armor)   │            │  • Refresh via   │
│             │               │  • DDoS protect  │            │    HttpOnly      │
└─────────────┘               └──────────────────┘            │    cookie        │
                                                               └────────┬─────────┘
                                                                        │ mTLS
                                                                        ▼
                                                               ┌──────────────────┐
                                                               │  RAG Service     │
                                                               │                  │
                                                               │  • KMS cifrado   │
                                                               │    datos sensibles│
                                                               │  • PII stripping  │
                                                               │    antes de LLM  │
                                                               └────────┬─────────┘
                                                                        │
                                                          ┌─────────────┴─────────────┐
                                                          │                           │
                                                    TLS 1.3                    TLS 1.3
                                                          │                           │
                                                          ▼                           ▼
                                               ┌──────────────────┐       ┌──────────────────┐
                                               │  Aurora pgvector  │       │  Bedrock (Claude)│
                                               │  • Cifrado at     │       │  • API Key via   │
                                               │    rest (KMS)     │       │    Secrets Mgr    │
                                               │  • Audit logs     │       │  • Audit trail   │
                                               └──────────────────┘       └──────────────────┘
```

---

## 3. Stack Tecnológico Detallado

### 3.1 Frontend — Widget Embebible

#### 3.1.1 Arquitectura del Widget

El widget se construye con **Lit 3** como Web Component nativo, empaquetado como **IIFE** (Immediately Invoked Function Expression) mediante **Vite**. Esto permite instalarlo en cualquier aplicación web agregando un simple `<script>` tag, sin importar el framework del host.

**Requisito clave:** No depende de Module Federation, Webpack, ni ningún bundler del host. Funciona en WordPress, PHP, React, Angular, Vue, jQuery, HTML plano.

#### 3.1.2 Instalación

```html
<!-- Único requisito: agregar script y custom element -->
<script src="https://cdn.capillas.ai/widget/v1/widget.js" defer></script>
<mi-widget 
  api-key="live_abc123_def456" 
  theme="light" 
  position="bottom-right"
  lang="es">
</mi-widget>
```

#### 3.1.3 Stack del Widget

| Componente | Tecnología | Versión | Tamaño |
|------------|-----------|---------|--------|
| Framework | Lit | 3.x | ~5 KB gzip |
| Build | Vite | 6.x | — |
| Formato output | IIFE | — | ~20 KB gzip total |
| Shadow DOM | Nativo | — | CSS aislado automático |
| Testing | Web Test Runner | — | — |

#### 3.1.4 Flujo de Comunicación con el Host

```
Host App → Widget:
  widgetElement.config = { theme: 'dark', user: { id: '123' } }
  window.postMessage({ type: '@capillas:config', payload: {...} }, '*')

Widget → Host App:
  window.parent.postMessage({ type: '@capillas:event', 
    payload: { event: 'login', user: 'asesor_456' } }, parentOrigin)
```

#### 3.1.5 Manejo de Tokens en el Widget

| Token | Duración | Almacenamiento | Propósito |
|-------|----------|----------------|-----------|
| Access Token (JWT) | 15 minutos | Variable in-memory (JS) | API calls |
| Refresh Token | 30 días | HttpOnly + Secure + SameSite=Strict cookie | Refrescar AT |
| ID Token (JWT) | 1 hora | Variable in-memory | Perfil de usuario |

### 3.2 Backend — Microservicios

#### 3.2.1 Servicios y Tecnologías

| Servicio | Lenguaje | Framework | Protocolo | Puerto | Réplicas |
|----------|----------|-----------|-----------|--------|----------|
| **BFF** | Python 3.12 | FastAPI | HTTP/SSE | 8080 | 2-3 |
| **RAG Service** | Python 3.12 | FastAPI + LlamaIndex | gRPC | 50051 | 2-3 |
| **Knowledge Base** | Python 3.12 | FastAPI + LangChain | gRPC | 50052 | 1-2 |
| **Analytics** | Python 3.12 | FastAPI | HTTP | 8083 | 1-2 |

#### 3.2.2 Comunicación entre Servicios

| De | A | Protocolo | Autenticación | Propósito |
|----|---|-----------|---------------|-----------|
| API Gateway | BFF | HTTP/1.1 | JWT + OAuth | Solicitudes widget |
| BFF | RAG | gRPC + mTLS | Certificado cliente | Consultas RAG |
| BFF | Analytics | SQS | IAM Role | Eventos async |
| RAG | Bedrock | AWS SDK | IAM Role | InvokeModel |
| RAG | Aurora | PostgreSQL (TLS) | IAM Auth | Queries pgvector |
| RAG | Redis | Redis (TLS) | IAM Auth | Cache |

#### 3.2.3 Pipeline RAG (Detalle)

```
INGESTA (Offline / Batch)
  Documentos (PDF, DOCX, MD) 
    → S3 Bucket 
    → S3 Event Notification 
    → Step Functions 
    → Lambda (parse + chunk + metadata extraction)
    → Titan Embeddings V2 (512d) 
    → Aurora pgvector (HNSW index)

QUERY (Online / Tiempo Real)
  Query asesor 
    → Query Rewrite (corrección ortográfica, expansión)
    → Semantic Cache (Redis, umbral 0.92)
      → [HIT] → Respuesta cacheada
      → [MISS] → 
    → Hybrid Search (BM25 + vector + metadata filters)
    → Cross-encoder Reranker (top 50 → top 5)
    → Parent-child expansion (chunks pequeños → contexto padre)
    → Context Assembly (< 4K tokens)
    → Prompt Engineering (system + context + query)
    → Claude Sonnet 4.6 (Bedrock)
    → Streaming response (SSE)
    → Store in semantic cache
    → Log to Analytics
```

### 3.3 Infraestructura AWS

#### 3.3.1 Servicios AWS Utilizados

| Servicio | Uso | Justificación |
|----------|-----|---------------|
| **Cognito** | Autenticación y autorización | 10K MAU gratis, OAuth 2.0/OIDC, MFA, SSO |
| **API Gateway HTTP** | API entry point | $1/1M requests (vs $3.50 REST), JWT auth nativo |
| **ECS Fargate** | Orquestación de microservicios | Sin Kubernetes, ~$50-300/mes, auto-escalado |
| **Aurora Serverless v2** | Base de datos principal + vectores | pgvector gratis, datos relacionales + vectores en una DB |
| **Bedrock** | LLM (Claude) + Embeddings (Titan) | Sin mínimo, pago por token, Guardrails |
| **ElastiCache (Redis)** | Semantic cache, sesiones | Reduce costos LLM hasta 68% |
| **S3 + CloudFront** | Hosting widget estático | Transferencia S3→CF gratis, free tier 1TB/mes |
| **KMS** | Cifrado de datos en reposo | $1/key/mes, integración nativa |
| **ACM** | Certificados TLS/SSL | GRATIS, renovación automática |
| **CloudWatch + X-Ray** | Monitoreo y tracing | Incluido con AWS |
| **Step Functions** | Orquestación de ingesta de documentos | Flujos async con retry/error handling |
| **ECR** | Registro de imágenes Docker | Sin costo de almacenamiento |

#### 3.3.2 Recursos y Dimensionamiento

| Microservicio | CPU | RAM | Réplicas | Storage | Costo/mes (prod) |
|--------------|-----|-----|----------|---------|------------------|
| BFF | 0.5 vCPU | 1 GB | 2 | — | ~$50 |
| RAG Service | 1 vCPU | 2 GB | 2 | — | ~$80 |
| Knowledge Base | 0.5 vCPU | 1 GB | 1 | — | ~$25 |
| Analytics | 0.5 vCPU | 1 GB | 1 | — | ~$25 |
| Aurora Serverless v2 | 2 ACU | — | 1 | 50 GB | ~$60 |
| Redis | 1 GB | — | 1 | — | ~$20 |
| **Total** | | | | | **~$260** |

---

## 4. Comparativa Cloud Provider

### 4.1 Comparativa por Componente

#### 4.1.1 Autenticación (Auth)

| Aspecto | AWS Cognito | Azure Entra External ID | GCP Firebase Auth |
|---------|------------|------------------------|-------------------|
| **Nombre exacto** | Amazon Cognito (User Pool) | Microsoft Entra External ID | Firebase Authentication |
| **Free Tier** | 10,000 MAU gratis | 50,000 MAU gratis | 50,000 MAU gratis |
| **Precio extra** | $0.0055/MAU (Lite), $0.015 (Essentials) | ~$0.033/MAU (P1) | $0.0055/MAU (50k-100k) |
| **OAuth 2.0/OIDC** | Sí | Sí | Sí (Blaze/Identity) |
| **MFA** | SMS, TOTP, Biometric | SMS, Voice | Solo SMS |
| **SSO (SAML/OIDC)** | Sí (Enterprise SSO $0.015/MAU) | Sí (nativo) | Sí (Identity Platform) |
| **Custom UI** | Sí (Hosted UI personalizable) | Sí | Limitado |
| **Presencia LATAM** | sa-east-1 (Sao Paulo) | Brazil South | Firebase global |
| **Valoración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recomendación: Amazon Cognito** — Mejor balance costo/features, 10K MAU gratis, integración nativa con API Gateway.

#### 4.1.2 API Gateway

| Aspecto | AWS API Gateway | Azure API Management | GCP Apigee / LB |
|---------|----------------|---------------------|-----------------|
| **Opción económica** | HTTP API: $1/1M requests | Consumption: ~$3.50/1M | LB + Armor: ~$30/mes |
| **Opción completa** | REST API: $3.50/1M | Basic v2: ~$150/mes | Apigee: desde $500/mes |
| **WAF** | AWS WAF ($5/mo + $0.60/GB) | Azure WAF (incluido en Front Door) | Cloud Armor ($3-5/mo) |
| **JWT Auth nativo** | Sí (HTTP API) | Sí | No nativo |
| **Rate limiting** | Sí | Sí (políticas) | Sí (Armor) |
| **Free Tier** | 1M calls/mes x 12 meses | Consumption: 1M gratis | No |
| **Valoración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

**Recomendación: AWS API Gateway HTTP** — 71% más barato que REST API, JWT auth nativo, suficiente para este caso.

#### 4.1.3 Contenedores / Compute

| Aspecto | AWS ECS Fargate | Azure Container Apps | GCP Cloud Run |
|---------|----------------|---------------------|---------------|
| **Costo base** | $0 (solo pago por uso) | $0 (consumption plan) | $0 (free tier 2M req) |
| **vCPU-hora** | $0.04048/vCPU-hr | $0.0864/vCPU-hr | $0.000024/seg (~$0.086/hr) |
| **Escala a 0** | Sí | Sí | Sí |
| **Cold start** | ~100-300ms | ~200-500ms | ~100-500ms |
| **Cluster fee** | $0 | $0 | $0 |
| **Complexidad ops** | Baja | Baja | Muy baja |
| **GPU support** | No (ECS) / Sí (EKS) | Limitado | Limitado |
| **Costo típico/mes** | ~$50-300 | ~$100-300 | ~$150-300 |
| **Valoración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recomendación: AWS ECS Fargate** — Control plane gratis, operación zero-ops, más barato que AKS, no requiere DevOps dedicado.

#### 4.1.4 Vector Database

| Aspecto | Aurora pgvector | Azure AI Search | GCP AlloyDB pgvector |
|---------|----------------|-----------------|----------------------|
| **Costo mínimo** | ~$43/mes (0.5 ACU Serverless) | $73/mes (Basic) | ~$200-400/mes |
| **Precio 10M vectores** | ~$60/mes (Aurora Svrls v2) | $245/mes (S1) | ~$300-600/mes |
| **Escala a 0** | Sí (Serverless v2) | No | No (instance-based) |
| **Hybrid search** | Manual (tsvector + pgvector) | Nativo (AI Search) | Manual |
| **SQL + vectores** | Sí (misma DB) | No | Sí (misma DB) |
| **Performance HNSW** | Muy buena | Excelente (GPU) | Muy buena |
| **Costo idle** | ~$43/mes | $73/mes | ~$200/mes (AlloyDB min) |
| **Valoración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

**Recomendación: Aurora Serverless v2 + pgvector** — 90% más barato que OpenSearch Classic y Azure AI Search, escala a 0, misma DB para datos operacionales y vectores.

#### 4.1.5 LLM / Modelos

| Aspecto | AWS Bedrock (Claude) | Azure OpenAI (GPT-4o) | GCP Vertex AI (Gemini) |
|---------|---------------------|----------------------|----------------------|
| **Modelo principal** | Claude Sonnet 4.6 | GPT-4o | Gemini 2.5 Flash |
| **Precio input/1M tok** | $3.00 | $2.50 | $0.30 |
| **Precio output/1M tok** | $15.00 | $10.00 | $2.50 |
| **Modelo económico** | Claude Haiku 4.5 ($1/$5) | GPT-4o-mini ($0.15/$0.60) | Gemini 2.0 Flash ($0.10/$0.40) |
| **Contexto máximo** | 200K tokens | 128K tokens | 1M tokens |
| **Batch (50% off)** | Sí | No | Sí |
| **Prompt caching** | No nativo | Sí (hasta 50% ahorro) | Sí (hasta 90% contexto repetido) |
| **Disponibilidad LATAM** | sa-east-1 (SP) | Brazil South | us-central1 |
| **Calidad español** | Excelente | Excelente | Muy buena |
| **Valoración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recomendación: Claude en Bedrock** — Mejor calidad conversacional para español, 200K contexto, sin mínimo, integración nativa AWS, Guardrails, Knowledge Bases.

#### 4.1.6 Hosting Widget (CDN + Estáticos)

| Aspecto | AWS S3 + CloudFront | Azure Blob + Front Door | GCP GCS + CDN |
|---------|--------------------|------------------------|---------------|
| **Free Tier** | 1TB/mes transfer + 10M requests | Siempre | Sí |
| **Egress LATAM** | $0.110/GB | ~$0.082/GB | ~$0.08-0.12/GB |
| **S3 → CDN transfer** | **Gratis** (desde late 2024) | Gratis (origen Azure) | Gratis (origen GCP) |
| **Costo típico/mes** | $0-15 | ~$25 | $10-30 |
| **Valoración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recomendación: S3 + CloudFront** — Transferencia S3→CF gratis, free tier de 1TB/mes, flat-rate plans desde $15/mes (50TB).

#### 4.1.7 Resumen Comparativo de Costos

| Componente | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Auth | $0 (10K MAU) | $0 (50K MAU) | $0 (50K MAU) |
| API Gateway | $1-5 | $0-5 | $30-50 |
| Compute | $50-300 | $100-300 | $150-300 |
| Vector DB | $43-70 | $73-245 | $200-400 |
| LLM | $35-200 | $200-500 | $50-200 |
| Hosting Widget | $0-15 | ~$25 | $10-30 |
| Embeddings | $0-2 | $5-10 | $5-20 |
| Storage convs | $50-150 | $25-50 | $10-30 |
| Cache | ~$20 | ~$30 | ~$20 |
| Cifrado | $1-5 | ~$10 | $2-5 |
| **TOTAL/mes** | **~$200-800** | **~$800-1,400** | **~$400-1,000** |

### 4.2 Justificación de AWS como Proveedor Recomendado

#### 4.2.1 Razones Principales

1. **Costo más bajo en todos los componentes críticos:**
   - Aurora Serverless v2 + pgvector: ~$43-70/mes vs $73-245 de Azure AI Search vs $200-400 de GCP AlloyDB
   - ECS Fargate sin cluster fee ($0) vs AKS ($73/mes) vs GKE ($73/mes)
   - API Gateway HTTP a $1/1M requests vs competencia
   - CloudFront con free tier de 1TB/mes

2. **Mejor ecosistema para RAG en producción:**
   - Bedrock con Claude (mejor LLM conversacional) + Titan Embeddings (más baratos) integrados
   - Bedrock Knowledge Bases para RAG gestionado
   - Guardrails para seguridad de outputs
   - Step Functions para orquestación de ingesta

3. **Presencia LATAM madura:**
   - Región sa-east-1 (Sao Paulo) con todos los servicios principales
   - Bedrock disponible en Sao Paulo con Claude, Titan, Llama, Mistral
   - Baja latencia desde Colombia (~20-40ms a Sao Paulo)

4. **Operación sin equipo DevOps dedicado:**
   - ECS Fargate no requiere expertise en Kubernetes
   - Aurora Serverless v2 escala a 0 sin gestión
   - Cognito es gestionado
   - Bedrock es serverless

5. **Portabilidad futura:**
   - El stack (FastAPI + pgvector + Lit widget) es portable a cualquier cloud
   - Sin vendor lock-in fuerte (a diferencia de Azure OpenAI Service)

#### 4.2.2 Referencias de Precios (2025-2026)

| Servicio | Precio | Fuente |
|----------|--------|--------|
| Cognito Essentials | $0 (10K MAU gratis) | aws.amazon.com/cognito/pricing |
| API Gateway HTTP | $1.00/1M requests | aws.amazon.com/api-gateway/pricing |
| ECS Fargate | $0.04048/vCPU-hr + $0.004445/GB-hr | aws.amazon.com/ecs/pricing |
| Aurora Serverless v2 | $0.12/ACU-hr, storage $0.10/GB-mes | aws.amazon.com/rds/aurora/pricing |
| Bedrock Claude Sonnet 4.6 | $3.00/MTok input, $15.00/MTok output | aws.amazon.com/bedrock/pricing |
| Bedrock Claude Haiku 4.5 | $1.00/MTok input, $5.00/MTok output | aws.amazon.com/bedrock/pricing |
| Titan Embeddings V2 | $0.00002/1K tokens (~$0.02/1M tokens) | aws.amazon.com/bedrock/pricing |
| CloudFront | $0.085/GB (Norteamérica), 1TB free tier | aws.amazon.com/cloudfront/pricing |
| S3 Standard | $0.023/GB-mes | aws.amazon.com/s3/pricing |
| KMS | $1/key/mes + $0.03/10,000 requests | aws.amazon.com/kms/pricing |
| ACM | GRATIS (certificados públicos) | aws.amazon.com/acm/pricing |
| ElastiCache (Redis) | ~$0.034/GB-hr (serverless) | aws.amazon.com/elasticache/pricing |

---

## 5. Seguridad

### 5.1 Matriz de Amenazas y Mitigaciones

| Amenaza | Mitigación | Implementación |
|---------|-----------|----------------|
| **MITM** | TLS 1.3 con PFS obligatorio (ECDHE) + HSTS | ACM gratis, HSTS header, Certificate Transparency |
| **Inter-sevicio** | mTLS con certificados de cliente | Istio service mesh o API Gateway mTLS |
| **XSS** | Shadow DOM + CSP + sanitización de inputs | Shadow DOM (open) por defecto, CSP headers |
| **Token theft** | Access token in-memory (15 min), Refresh token HttpOnly | Variable JS + Secure cookie |
| **CSRF** | SameSite=Strict + Origin validation | Cookies configuradas con SameSite |
| **Data leakage (LLM)** | PII stripping antes de llamar a Bedrock | Filtro automático en RAG Service |
| **API abuse** | Rate limiting + JWT validation + WAF | API Gateway (100 req/min/asesor) |
| **Injection (prompt)** | Separación system/user prompt + input sanitization | Prompt engineering estructurado |
| **Key compromise** | AWS KMS + Secrets Manager + rotación automática | Rotación cada 30 días |
| **Data at rest** | KMS encryption en todos los servicios | Aurora, S3, Redis con KMS |

### 5.2 Comunicación Cifrada

```
Browser (Widget)                        API Gateway                     Microservicios Internos
      │                                      │                                 │
      │  ● TLS 1.3 (PFS)                     │  ● TLS 1.3                     │
      │  ● HSTS: max-age=31536000            │  ● mTLS (cert cliente)         │
      │  ● Certificate Transparency          │  ● Certificados ACM Private CA │
      │  ● JWT in-memory                     │  ● IAM Roles (no keys)         │
      │                                      │                                 │
      └──────────────────────────────────────┴─────────────────────────────────┘
```

### 5.3 Privacidad de Datos — Ley 1581 de 2012 (Colombia)

| Requisito Legal | Implementación |
|----------------|---------------|
| **Consentimiento** | El asesor informa al cliente del uso de IA. Consentimiento explícito antes de guardar datos personales |
| **Finalidad** | Datos solo para mejorar asesoría comercial. No para entrenar modelos externos |
| **Circulación restringida** | Datos no salen del entorno AWS. Anonimización PII antes de Bedrock |
| **Derechos ARCO** | Endpoints para exportar/eliminar datos de un cliente |
| **Notificación brechas** | Sistema de alertas + procedimiento para reportar a SIC (15 días hábiles) |
| **Minimización** | Solo recolectar datos necesarios para la asesoría |

**Pipeline de anonimización antes del LLM:**

```
Datos crudos del cliente (nombre, documento, teléfono, dirección)
    │
    ▼
┌─────────────────────────────────────┐
│  1. Detección de PII (regex + NER)  │
│  2. Reemplazo con tokens anónimos   │
│     ("Cliente-001", 60 años,        │
│      "Familia 4 personas")          │
│  3. Verificación de fuga de PII     │
│  4. Envío a Bedrock (sin PII)       │
└─────────────────────────────────────┘
    │
    ▼
Bedrock (Claude) — NUNCA recibe datos personales
```

### 5.4 Secret Management

| Secreto | Almacenamiento | Rotación |
|---------|---------------|----------|
| API Keys Bedrock | AWS Secrets Manager + KMS | Cada 30 días |
| DB Credentials | AWS Secrets Manager + RDS IAM Auth | Automática (IAM) |
| JWT Signing Keys | Cognito (gestionado) | Automática |
| KMS Keys | AWS KMS | Anual (rotación automática) |
| SSL/TLS Certs | AWS ACM | Automática (gratis) |

---

## 6. Plan de Implementación

### 6.1 Timeline General

| Fase | Duración | Semanas | Hitos |
|------|----------|---------|-------|
| **Fase 1: Fundación** | 5 semanas | 1-5 | Infraestructura AWS, Auth, Widget base |
| **Fase 2: RAG Pipeline** | 5 semanas | 6-10 | Knowledge Base, RAG Service, Embeddings |
| **Fase 3: Asistente Completo** | 5 semanas | 11-15 | Asistente integrado, Piloto con asesores |
| **Fase 4: Optimización** | 5 semanas | 16-20 | WhatsApp, Analytics, Escalamiento |

### 6.2 Fase 1: Fundación (Semanas 1-5)

| Semana | Actividades | Entregables |
|--------|------------|-------------|
| **1** | Setup cuenta AWS, IAM, redes VPC, Security Groups | Infraestructura base Terraform |
| **2** | Cognito User Pool, OAuth config, Hosted UI | Auth service funcional |
| **3** | Widget base (Lit 3), Custom Element, Shadow DOM | Widget con login flow |
| **4** | API Gateway, BFF service (FastAPI), CI/CD | BFF desplegado, widget conectado |
| **5** | Integración widget → BFF → Auth → API → tests | End-to-end login flow funcional |

### 6.3 Fase 2: RAG Pipeline (Semanas 6-10)

| Semana | Actividades | Entregables |
|--------|------------|-------------|
| **6** | Aurora Serverless v2 + pgvector setup, schema | Vector DB operativa |
| **7** | Pipeline de ingesta: S3 → Step Functions → Embeddings → pgvector | Ingesta de documentos funcional |
| **8** | RAG Service (LlamaIndex): chunking, embedding, indexación | RAG service v1 |
| **9** | Hybrid search, metadata filters, cross-encoder reranker | Retrieval optimizado |
| **10** | Claude en Bedrock, prompt engineering, Guardrails | RAG pipeline completo |

### 6.4 Fase 3: Asistente Completo (Semanas 11-15)

| Semana | Actividades | Entregables |
|--------|------------|-------------|
| **11** | Integración RAG → BFF → Widget (SSE streaming) | Asistente funcional end-to-end |
| **12** | Semantic cache (Redis), optimización de latencia | Cache operativo |
| **13** | Knowledge Base Service, administración de documentos | KB admin UI |
| **14** | Piloto con 5-10 asesores, feedback, ajustes | Piloto funcionando |
| **15** | Ajustes según feedback, refinamiento prompts | Piloto validado |

### 6.5 Fase 4: Optimización y Expansión (Semanas 16-20)

| Semana | Actividades | Entregables |
|--------|------------|-------------|
| **16** | Analytics Service, dashboard de métricas | Dashboard operativo |
| **17** | Monitoreo (LangFuse, Grafana), alertas | Observabilidad completa |
| **18** | Expansión a más asesores (50-100) | Producción escalada |
| **19** | Integración WhatsApp (Twilio + canal) | Fase 2 del roadmap |
| **20** | Documentación, hardening seguridad, optimización costos | Sistema listo para producción |

---

## 7. Estimación de Costos

### 7.1 Costos Mensuales Detallados — AWS

#### MVP / Desarrollo (primeros 3 meses)

| Servicio | Configuración | Costo/mes |
|----------|--------------|-----------|
| Cognito | Essentials, < 10 MAU | $0.00 |
| API Gateway HTTP | 10K requests/mes | $0.01 |
| ECS Fargate | 1 servicio, 0.5 vCPU, 1 GB | ~$30 |
| Aurora Serverless v2 | 0.5 ACU, 10 GB | ~$43 |
| Bedrock (Claude Haiku) | 1K conversaciones/mes | ~$5 |
| Titan Embeddings | 1K documentos | ~$0.02 |
| ElastiCache (Redis) | Serverless, 0.5 GB | ~$10 |
| S3 + CloudFront | 1 GB, 1K requests | ~$1 |
| KMS + ACM | 2 keys | ~$2 |
| **Total MVP** | | **~$91/mes** |

#### Producción (100 asesores)

| Servicio | Configuración | Costo/mes |
|----------|--------------|-----------|
| Cognito | Essentials, 100 MAU | $0.00 |
| API Gateway HTTP | 500K requests/mes | $0.50 |
| ECS Fargate | 3 servicios, 2-4 réplicas | ~$260 |
| Aurora Serverless v2 | 2 ACU, 50 GB | ~$60 |
| Bedrock (Claude Sonnet + Haiku) | 10K conversaciones/mes | ~$150 |
| Titan Embeddings | 10K documentos/mes | ~$0.20 |
| ElastiCache (Redis) | Serverless, 1 GB | ~$20 |
| S3 + CloudFront | 10 GB, 50K requests | ~$5 |
| Step Functions | Ingesta documentos | ~$5 |
| CloudWatch + X-Ray | Logs + trazas | ~$20 |
| KMS + ACM | 3 keys | ~$3 |
| **Total Producción** | | **~$523/mes** |

#### Escalado (500+ asesores)

| Servicio | Configuración | Costo/mes |
|----------|--------------|-----------|
| Cognito | Essentials, 500-1000 MAU | ~$3 |
| API Gateway HTTP | 2.5M requests/mes | $2.50 |
| ECS Fargate | 4 servicios, 3-5 réplicas + Spot | ~$400 |
| Aurora Serverless v2 | 4 ACU, 100 GB HA | ~$150 |
| Bedrock (Sonnet + Haiku routing) | 50K conversaciones/mes | ~$600 |
| Titan Embeddings | 50K documentos/mes | ~$1 |
| ElastiCache (Redis) | Serverless, 5 GB | ~$50 |
| S3 + CloudFront | 50 GB, 250K requests | ~$15 |
| Step Functions | Ingesta + workflows | ~$20 |
| CloudWatch + X-Ray | Logs + trazas | ~$60 |
| KMS + ACM | 5 keys | ~$5 |
| **Total Escalado** | | **~$1,306/mes** |

### 7.2 Proyección Anual

| Mes | Fase | Costo/mes | Acumulado |
|-----|------|-----------|-----------|
| 1-2 | Desarrollo + Fundación | ~$100 | $200 |
| 3 | MVP | ~$200 | $600 |
| 4-5 | Piloto (10 asesores) | ~$300 | $1,200 |
| 6 | Piloto expandido (50) | ~$400 | $2,400 |
| 7-8 | Producción (100) | ~$500 | $3,400 |
| 9-12 | Escalamiento (200-500) | ~$800-1,300 | $7,700 |
| **Total Año 1** | | | **~$12,000-15,000/año** |

### 7.3 Estrategias de Optimización de Costos

| Estrategia | Ahorro | Implementación |
|-----------|--------|---------------|
| **Semantic Cache** (Redis) | Hasta 68% en costos LLM | Umbral similitud 0.92 |
| **Routing inteligente** (Sonnet ↔ Haiku) | Hasta 30% | Tareas simples → Haiku, complejas → Sonnet |
| **Fargate Spot** | Hasta 70% en compute | Dev/QA y servicios no críticos |
| **Savings Plans** (1 año) | Hasta 50% en compute | Comprometerse a $50/mes |
| **Batch Bedrock** | 50% en inferencia | Procesamiento nocturno de documentos |
| **CloudFront free tier** | 1TB/mes gratis | Aprovechar los primeros meses |
| **S3 Intelligent Tiering** | Hasta 40% en storage | Datos de conversaciones con acceso variable |

---

## 8. Referencias y Fuentes

### 8.1 Precios Oficiales AWS

- Amazon Cognito Pricing: https://aws.amazon.com/cognito/pricing/
- API Gateway Pricing: https://aws.amazon.com/api-gateway/pricing/
- Amazon ECS Pricing: https://aws.amazon.com/ecs/pricing/
- Amazon Aurora Pricing: https://aws.amazon.com/rds/aurora/pricing/
- Amazon Bedrock Pricing: https://aws.amazon.com/bedrock/pricing/
- Amazon CloudFront Pricing: https://aws.amazon.com/cloudfront/pricing/
- Amazon S3 Pricing: https://aws.amazon.com/s3/pricing/
- AWS KMS Pricing: https://aws.amazon.com/kms/pricing/
- AWS ACM Pricing: https://aws.amazon.com/acm/pricing/
- ElastiCache Pricing: https://aws.amazon.com/elasticache/pricing/

### 8.2 Precios Oficiales Azure

- Entra External ID Pricing: https://azure.microsoft.com/pricing/details/active-directory/external-identities/
- API Management Pricing: https://azure.microsoft.com/pricing/details/api-management/
- Container Apps Pricing: https://azure.microsoft.com/pricing/details/container-apps/
- AI Search Pricing: https://azure.microsoft.com/pricing/details/search/
- OpenAI Service Pricing: https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/

### 8.3 Precios Oficiales GCP

- Firebase Pricing: https://firebase.google.com/pricing
- Cloud Run Pricing: https://cloud.google.com/run/pricing
- AlloyDB Pricing: https://cloud.google.com/alloydb/pricing
- Vertex AI Pricing: https://cloud.google.com/vertex-ai/pricing
- Cloud Storage Pricing: https://cloud.google.com/storage/pricing

### 8.4 Tecnologías y Frameworks

- Lit 3 Documentation: https://lit.dev/docs/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- LlamaIndex Documentation: https://docs.llamaindex.ai/
- LangChain Documentation: https://python.langchain.com/docs/
- pgvector GitHub: https://github.com/pgvector/pgvector
- OAuth 2.0 RFC 6749: https://datatracker.ietf.org/doc/html/rfc6749
- OAuth 2.1 BCP (RFC 9700): https://datatracker.ietf.org/doc/rfc9700/
- OpenTelemetry Documentation: https://opentelemetry.io/docs/

### 8.5 Seguridad y Cumplimiento

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Ley 1581 de 2012 (Colombia): https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981
- SIC — Protección de Datos: https://www.sic.gov.co/proteccion-de-datos-personales
- RFC 9700 — OAuth Security BCP: https://www.rfc-editor.org/rfc/rfc9700

### 8.6 Benchmarks y Estándares

- MTEB Leaderboard (Embeddings): https://huggingface.co/spaces/mteb/leaderboard
- RAGAS Evaluation: https://docs.ragas.io/
- LangFuse (Observabilidad): https://langfuse.com/
- Bedrock Knowledge Bases: https://aws.amazon.com/bedrock/knowledge-bases/
- Claude Prompt Engineering: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering

---

*Documento generado con asistencia de IA agentic. Versión 1.0 — Junio 2026.*

*Para preguntas o ajustes: equipo de desarrollo.*

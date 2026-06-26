# Prompts para generación de imágenes técnicas

Usar con [nanobanana2](https://nanobanana2.com) u otra herramienta de generación.
Las imágenes deben guardarse en `docs/slides/imagenes/` con los nombres indicados.

---

## 1. `arquitectura-general.png` — Diagrama de Arquitectura General

```
Diagrama de arquitectura de microservicios en 2D, estilo draw.io profesional.
Fondo blanco, líneas grises (#94A3B8) y azules (#2563EB).
Cajas rectangulares con bordes redondeados (4px) organizadas en 3 capas horizontales:
- Capa superior: "Widget (Lit 3)" conectado via HTTPS a "BFF (FastAPI)"
- Capa media: "BFF" conectado a "RAG Service (LlamaIndex)", "Auth (Cognito)", "API Gateway"
- Capa inferior: "Aurora PostgreSQL + pgvector", "Redis Cache", "S3 Knowledge Base", "Bedrock (Claude)"
Flechas de un solo sentido con etiquetas: "SSE Stream", "gRPC", "REST", "SQL queries".
Sin personas, sin logos de empresas, sin sombras. Estilo corporativo sobrio.
Esquema de colores: slate (#1E293B, #475569, #CBD5E1) con acentos azul acero (#2563EB).
Proporción 16:9, 1920x1080px, PNG.
```

## 2. `flujo-widget.png` — Flujo de consulta del widget

```
Diagrama de secuencia vertical con 4 columnas: "Usuario", "Widget (Lit 3)",
"BFF (FastAPI)", "RAG Service".
De arriba abajo con flechas:
1. Usuario -> Widget: "Escribe pregunta" (flecha negra)
2. Widget -> BFF: "POST /chat" con token JWT (flecha azul #2563EB)
3. BFF -> RAG Service: "gRPC query + contexto" (flecha slate #475569)
4. RAG -> BFF: "Streaming response vía SSE" (flecha verde #059669)
5. BFF -> Widget: "SSE event stream" (flecha azul)
6. Widget -> Usuario: "Renderiza respuesta markdown" (flecha negra)
Estilo diagrama de secuencia UML limpio, sin personas, monocromático con acentos
de color mínimos. Fondo blanco, tipografía sans-serif. 1920x1080px, PNG.
```

## 3. `arquitectura-bff.png` — Componentes del BFF

```
Diagrama de cajas estilo draw.io mostrando la arquitectura interna del BFF
(FastAPI Python 3.12).
Caja principal "BFF (Backend for Frontend)" con submódulos internos conectados:
- "Auth Middleware (Cognito BFF)" en la entrada
- "Session Manager (Redis)"
- "Chat Router (SSE)" conectado a "RAG Client (gRPC)"
- "Cache Layer (Redis Semantic Cache)"
Conexiones internas con flechas. Input: "HTTPS / OAuth PKCE".
Output: "SSE Stream" -> "Widget".
Estilo técnico limpio, solo líneas negras y grises (#334155, #CBD5E1),
detalles en azul acero (#2563EB). Sin logos. 1920x1080px, PNG.
```

## 4. `infraestructura-aws.png` — Infraestructura AWS

```
Diagrama de arquitectura en la nube AWS, estilo diagrama de infraestructura técnica.
5-6 servicios AWS representados como cajas rectangulares con iconos minimalistas
(no logos oficiales):
- "ECS Fargate" (contiene BFF + RAG Service)
- "Aurora Serverless v2 + pgvector" (base de datos)
- "S3 + CloudFront" (knowledge base + distribución)
- "API Gateway HTTP" (entrada)
- "Cognito" (auth)
- "Redis / MemoryDB" (cache)
- "Bedrock" (Claude LLM)
Conexiones con flechas entre servicios. Dos Availability Zones.
Fondo blanco (#FFFFFF), cajas slate (#1E293B) con bordes slate (#CBD5E1).
Etiquetas en español. Proporción 16:9, 1920x1080px, PNG.
```

## 5. `flujo-rag.png` — Pipeline RAG

```
Diagrama de flujo horizontal de 5 etapas (izquierda a derecha):
1. "Ingestión" -> documentos -> chunking -> embedding (text-embedding-3-small 512d)
2. "Indexación" -> vectores -> pgvector (Aurora PostgreSQL)
3. "Query" -> pregunta -> embedding -> búsqueda vectorial + búsqueda semántica
4. "Generación" -> contexto + prompt -> Claude Sonnet 4.6 (Bedrock)
5. "Respuesta" -> respuesta estructurada -> cache Redis -> SSE
Cada etapa es una caja rectangular slate (#475569) con borde, conectadas por flechas.
Etapas 1-2 en gris claro "Offline", etapas 3-5 en azul acero "Online".
Fondo blanco, sin personas. 1920x1080px, PNG.
```

## 6. `seguridad-auth.png` — Flujo de autenticación y seguridad

```
Diagrama de flujo de autenticación OAuth 2.0 + OIDC + PKCE.
4 actores en columnas: "Usuario" -> "Widget (SPA)" -> "BFF" -> "Cognito".
Flechas numeradas 1-8 mostrando:
1. Widget redirige a Cognito (con code_challenge)
2. Cognito muestra login
3. Usuario ingresa credenciales
4. Cognito redirige con authorization code
5. BFF intercambia code por tokens (PKCE)
6. BFF establece session cookie httpOnly
7. BFF retorna session al widget
8. Widget usa session para requests
Bajo el diagrama, 3 cajas de iconos: "AES-256-GCM E2E", "TLS 1.3 + mTLS",
"KMS Key Rotation".
Estilo técnico limpio, slate + azul acero. 1920x1080px, PNG.
```

## 7. `costos-nube.png` — Gráfico de costos

```
Gráfico de barras horizontales simple, estilo corporativo sobrio.
3 barras correspondientes a 3 escenarios:
- "MVP / Desarrollo: ~$314K COP/mes" (barra slate #475569, más corta)
- "Producción 100 users: ~$1.8M COP/mes" (barra slate #334155, mediana)
- "Escalado 500+ users: ~$4.5M COP/mes" (barra slate #1E293B, más larga)
Eje X: "Costo mensual (COP)", eje Y: "Escenario".
Sin adornos, sin 3D, sin iconos. Fondo blanco, etiquetas en fuente sans-serif negra.
1920x1080px, PNG.
```

---

## Instrucciones de uso

1. Copiar el prompt deseado
2. Pegar en nanobanana2
3. Ajustar parámetros de generación (estilo: diagrama técnico, fotorealismo: bajo)
4. Guardar imagen generada en `docs/slides/imagenes/<nombre-archivo>`
5. La imagen se cargará automáticamente en la presentación

# Especificación Técnica: [Nombre del Componente/Servicio]

- **Estado:** [Borrador | Revisión | Aprobado]
- **Versión:** 0.1.0
- **Última actualización:** [YYYY-MM-DD]
- **Responsable:** [Nombre]

---

## 1. Objetivo

<!--
¿Qué problema resuelve este componente?
¿Cuál es su responsabilidad dentro del sistema?
-->

## 2. Contrato / API

### 2.1 Interfaz pública

```
[Descripción de la interfaz: REST, gRPC, WebSocket, SSE, etc.]
```

| Método | Path | Request | Response | Códigos |
|--------|------|---------|----------|---------|
| GET | `/resource` | ... | ... | 200, 400, 500 |

### 2.2 Eventos (si aplica)

| Evento | Producer | Consumer | Payload |
|--------|----------|----------|---------|
| ... | ... | ... | ... |

## 3. Flujo

### 3.1 Diagrama de secuencia

<!--
```
Usuario     Widget      BFF        RAG Service
  |           |          |            |
  |--pregunta-->|         |            |
  |           |--request-->|           |
  |           |          |--query----->|
  |           |          |<--respuesta-|
  |           |<--stream--|            |
  |<--respuesta-|         |            |
```
-->

### 3.2 Estados

| Estado | Descripción | Transición a |
|--------|-------------|--------------|
| ... | ... | ... |

## 4. Modelo de Datos

### 4.1 Esquema

```typescript
// o Python, o SQL
interface Ejemplo {
  id: string;
  campo: string;
}
```

### 4.2 Almacenamiento

| Dato | Storage | Índices | TTL |
|------|---------|---------|-----|
| ... | PostgreSQL / Redis / S3 | ... | ... |

## 5. Dependencias

| Dependencia | Versión | Propósito |
|-------------|---------|-----------|
| ... | ... | ... |

## 6. Configuración

| Variable | Default | Descripción |
|----------|---------|-------------|
| `ENV_VAR` | `valor` | ... |

## 7. Seguridad

<!--
- Autenticación y autorización
- Cifrado
- Rate limiting
- Validación de entrada
-->

## 8. Tests

### 8.1 Unitarios

- ...
- ...

### 8.2 Integración

- ...
- ...

### 8.3 Carga / Estrés

- ...
- ...

## 9. Criterios de Aceptación

- [ ] ...
- [ ] ...
- [ ] ...

## 10. Abiertos / Preguntas

- ¿...?
- ¿...?

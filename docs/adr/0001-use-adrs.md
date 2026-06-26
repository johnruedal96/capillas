# Usar Architecture Decision Records (MADR)

- **Estado:** Aceptado
- **Fecha:** 2026-06-26
- **Autores:** Equipo de desarrollo

---

## Contexto

El proyecto Capillas de la Fe involucra múltiples componentes (widget frontend, BFF, RAG service, knowledge base, infraestructura AWS) y decisiones técnicas que impactan la arquitectura general. Sin un registro estructurado, las decisiones se pierden en conversaciones, PRs o documentación dispersa.

Necesitamos un mecanismo ligero que:
- Capture el contexto y la justificación de cada decisión arquitectónica
- Sea fácil de mantener en el repositorio junto al código
- Permita a nuevos miembros del equipo entender por qué se tomaron ciertas decisiones
- No agregue fricción al flujo de trabajo

## Decisión

Adoptamos **Architecture Decision Records (ADRs)** usando el formato **MADR 4.0** (Markdown Any Decision Records).

Los ADRs se almacenan en `docs/adr/` como archivos Markdown numerados secuencialmente (`NNNN-titulo-breve.md`).

### Formato MADR

Cada ADR incluye:
- **Título** descriptivo
- **Estado**: Propuesto / Aceptado / Rechazado / Deprecado / Superseded
- **Contexto**: problema, fuerzas, restricciones
- **Decisión**: qué se decidió con detalle técnico
- **Consecuencias**: pros, contras, trade-offs
- **Alternativas consideradas**: otras opciones evaluadas con su descarte

### Proceso

1. Detectar una decisión arquitectónica significativa
2. Crear archivo usando `0000-template.md`
3. Asignar siguiente número secuencial
4. Abrir PR para discusión
5. Mergear → ADR aceptado
6. Registrar en `CHANGELOG.md`

## Consecuencias

### Positivas

- Decisiones documentadas con contexto completo
- Nuevos miembros pueden ponerse al día rápido
- Historial de evolución arquitectónica rastreable en git
- Formato estándar (MADR) ampliamente adoptado en la industria

### Negativas / Trade-offs

- Esfuerzo adicional al tomar decisiones (redactar el ADR)
- Riesgo de burocracia si se documenta todo sin criterio
- Los ADRs requieren mantenimiento si una decisión cambia

### Migración

No aplica — es el primer ADR del proyecto.

## Alternativas consideradas

### Y-Statements

- **Pros:** Formato ultra-ligero (3 líneas)
- **Contras:** Demasiado breve para decisiones complejas; no captura alternativas
- **Razón de descarte:** MADR ofrece mejor equilibrio entre detalle y simplicidad

### No documentar / Confiar en git commits

- **Pros:** Cero overhead
- **Contras:** Los mensajes de commit no capturan contexto ni alternativas; la información se pierde
- **Razón de descarte:** Para un proyecto multi-servicio, el costo de no documentar es mayor

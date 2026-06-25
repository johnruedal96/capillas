# **Arquitectura RAG**

- [**CAPA 1: INGESTA (qué información entra)**](#capa-1-ingesta-de-información)
- [**CAPA 2: MODELADO (cómo se estructura)**](#capa-2-modelado-del-conocimiento)
- [**CAPA 3: RECUPERACIÓN (cómo busca)**](#capa-3-recuperación-cómo-busca-la-ia)
- [**CAPA 4: GENERACIÓN (cómo responde)**](#capa-4-generación-cómo-responde)
- [**CAPA 5: ORQUESTACIÓN (lógica de negocio)**](#capa-5-orquestación-el-diferencial-real)

---
## **CAPA 1: Ingesta de información**

- **Fuentes clave**

    - **Producto (CRÍTICO)**

        - Planes exequiales
        - Coberturas
        - Exclusiones
        - Precios / rangos

    - **Comercial (MUY CRÍTICO)**

        - Scripts actuales
        - Objeciones reales (call center, asesores)
        - Casos de cierre exitoso
        - Argumentos diferenciales

    - **Operación**

        - Qué pasa después de la venta
        - Tiempos
        - Logística

    - **Cliente**

        - Segmentos (edad, nivel socioeconómico)
        - Motivaciones
        - Miedos

    - **Legal / reputacional**

        - Qué NO se puede prometer
        - Condiciones críticas

**Regla de oro:**

No meteremos PDFs sin procesar → **Metadata**

## **CAPA 2: Modelado del conocimiento**

**Tipo 1: "Fichas de producto"**

- **Task: Conocer arquetipos**

Ejemplo:

Plan: Familiar Premium

Segmento: Edad - Contexto económico  
<br/>Incluye:  
\- Velación  
\- Cremación  
\- Traslado nacional  
<br/>No incluye:  
\- Repatriación  
<br/>Perfil ideal:  
\- Familias 3-5 personas  
\- Nivel medio  
<br/>Argumento clave:  
"Te permite cubrir a toda tu familia sin preocuparte por costos inesperados"  
<br/>Objeción típica:  
"Está caro"  
<br/>Respuesta sugerida:  
"Más que un gasto, es evitar que tu familia asuma un costo mayor en un momento difícil"

**Tipo 2: "Fichas de cliente"**

- **Task: Conocer arquetipos**

Segmento: Adulto 55+  
<br/>Necesidades:  
\- Tranquilidad  
\- No ser carga para la familia  
<br/>Sensibilidad:  
\- Alta emocionalidad  
<br/>Discurso recomendado:  
\- Protección  
\- Legado  
<br/>Errores a evitar:  
\- Lenguaje técnico

**Tipo 3: "Fichas de objeciones"**

Objeción: "Lo voy a pensar"  
<br/>Significado real:  
\- Duda  
\- Falta de urgencia  
<br/>Respuesta sugerida:  
\- Generar urgencia emocional  
\- Ejemplo real

**Tipo 4: "Playbooks comerciales"**

Canal: Sala de velación  
<br/>Contexto:  
\- Alta emocionalidad  
<br/>Objetivo:  
\- Contención + asesoría  
<br/>Tono:  
\- Empático  
<br/>No hacer:  
\- Venta agresiva

**Tipo 5: "Reglas de negocio"**

Si:  
\- Cliente > 60 años  
\- Bajo presupuesto  
<br/>Entonces:  
\- No recomendar plan premium

## **CAPA 3: Recuperación (cómo busca la IA)**

Aquí defines **qué trae la IA antes de responder**.

- Búsqueda semántica (vector)
- Filtros por metadata

**Metadata clave (IMPORTANTÍSIMO)**

Cada documento debe tener:

- Tipo (producto, objeción, cliente, etc.)
- Segmento (edad, perfil)
- Canal (call, presencial, etc.)
- Nivel emocional (alto/medio/bajo)
- Etapa (descubrimiento, cierre)

## **CAPA 4: Generación (cómo responde)**

Aquí defines el comportamiento del asistente.

**Prompt base**

Debe obligar a la IA a:

- Responder claro y corto
- Usar lenguaje comercial
- Adaptarse al cliente
- Sugerir acción

**Ejemplo de output ideal**

No:  
❌ "El plan incluye…"

Sí:  
✅ "Para este cliente te recomiendo el Plan X porque cubre a su familia y evita costos altos. Puedes decirle: 'Esto te da tranquilidad…'"

## **CAPA 5: Orquestación (el diferencial real)**

**Ejemplo:**

- **_Usuario pregunta:_** <br>
"¿Qué le vendo a alguien de 60 años con bajo presupuesto?"

- **_Sistema hace_**_:_
    - Busca fichas de cliente
    - Filtra planes adecuados
    - Consulta objeciones
    - Aplica reglas de negocio
    
- **_Responde:_**
    - Plan recomendado
    - Argumento
    - Objeción + respuesta

**DATA**

**Necesitamos medir todo**

- Qué preguntas hacen
- Qué respuestas funcionan

**Evolución futura**

Después puedes agregar:

- "Next Best Offer" automático
- Predicción de conversión
- Análisis de llamadas
- Fine-tuning con datos propios

Tasks:

- Que bases de conocimiento tienen?
- Que indicadores miden actualmente para performance interno?
- Que indicadores miden actualmente para performance externo: CSAT/CES/Percepción?
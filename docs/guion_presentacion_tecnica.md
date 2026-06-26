# Guion — Presentación Técnica (Versión Negocio)

**Para ti (el desarrollador)** — pero con palabras que entienda negocio.  
**Duración:** ~20-25 min · **Audiencia:** Dirección, dueños de negocio (no técnicos)

---

## Slide 1 — Portada (30s)

> *"Buenos días. Vamos a ver la parte técnica: cómo funciona el sistema por dentro, cuánto cuesta la nube, cómo protegemos los datos, y por qué tomamos cada decisión. La idea es que se vayan con la confianza de que esto es serio, seguro y que los números dan."*

---

## Slide 2 — ¿Qué es el Sistema? (1 min)

> *"Empecemos con lo básico. El sistema tiene dos partes que se ven y una que no se ve.*

> *"Lo que se ve: un chat flotante que los asesores usan para hacer preguntas. Y un panel de administración donde el equipo de Capillas sube los documentos. No hay que instalar nada —solo se agrega una línea al sistema actual y el widget aparece en la pantalla.*

> *"Lo que no se ve es la inteligencia: corre en la nube de Amazon en Sao Paulo, todo viaja cifrado como un banco, y el sistema mejora solo con el uso."*

---

## Slide 3 — Arquitectura (3 min)

> *"Acá está el diagrama de cómo se conecta todo. No se asusten por los cuadros — es más simple de lo que parece.*

> *"Del lado izquierdo están los dos widgets —el de chat y el de administración— que se cargan desde la red de distribución de Amazon [señalar CloudFront]. Esto asegura que el widget cargue rápido desde cualquier parte de Colombia.*

> *"Cuando el asesor hace una pregunta, el dato viaja cifrado hasta CloudFront, donde una función en el borde de la red [Lambda@Edge] lo descifra y lo pasa a la puerta de entrada del sistema [API Gateway].*

> *"De ahí va al orquestador [BFF], que es el que coordina todo: valida que el asesor tenga sesión, decide qué servicio debe responder.*

> *"El orquestador habla con tres servicios internos: el cerebro que busca la información [RAG Service], el que gestiona los documentos [KB Service], y el que mide todo [Analytics].*

> *"Entre estos servicios internos la comunicación es aún más segura —usan certificados digitales mutuos— y todo dentro de una red privada que no está expuesta a internet.*

> *"Al final están: la base de datos que entiende significados [pgvector], el caché que guarda respuestas repetidas [Redis], y la inteligencia artificial [Claude en Bedrock].*

> *"Cada capa tiene una razón de existir: seguridad, velocidad, escalabilidad. No es complejidad por complejidad."*

---

## Slide 4 — Flujo de Consulta (2 min)

> *"Veamos qué pasa segundo a segundo cuando un asesor pregunta algo. Miren el diagrama de arriba abajo:*

> *"El asesor escribe '¿Qué plan para familia de 4 con $50 mil?' en el widget.*

> *"El widget cifra esa pregunta con el mismo estándar que usan los bancos y la envía.*

> *"CloudFront recibe el dato cifrado, lo descifra en el borde, y lo pasa al sistema.*

> *"El orquestador [BFF] valida la sesión y envía la consulta al cerebro [RAG Service].*

> *"El cerebro primero revisa si ya respondió esto antes [cache]. Si la respuesta está guardada, la devuelve en menos de medio segundo sin gastar en IA.*

> *"Si no está en cache, busca en la base de datos que entiende significados [pgvector] los documentos más relevantes para esa pregunta, arma el contexto, y se lo envía a Claude [Bedrock].*

> *"Claude genera la respuesta y la devuelve. El sistema la guarda en cache por si otro asesor pregunta lo mismo.*

> *"La respuesta viaja de vuelta cifrada, el widget la descifra, y el asesor la ve: 'Plan Familiar Premium, $48/mes, cubre a toda la familia'.*

> *"Todo esto en aproximadamente 2 segundos. Si ya se había preguntado antes, en menos de medio segundo."*

---

## Slide 5 — Ingesta de Datos (2 min)

> *"¿Cómo sabe la IA los planes, las coberturas, las reglas? Veamos cómo entran los datos.*

> *"El administrador abre el panel, arrastra un archivo —puede ser PDF, Word o Markdown— y lo suelta. Eso es todo lo que tiene que hacer.*

> *"Detrás, ocurre esto en automático, sin que nadie tenga que hacer nada más:*

> *"El archivo se guarda en Amazon S3. Eso dispara un flujo automático [Step Functions] que ejecuta varios pasos en secuencia.*

> *"Primero: extrae el texto del documento. Segundo: lo divide en fragmentos pequeños para que la IA pueda manejarlos bien. Tercero: le pone etiquetas —¿esto es un plan? ¿una objeción? ¿un playbook? ¿para qué canal?—*

> *"Cuarto: genera una huella digital del significado del texto [embedding]. Es como convertir el significado en un código matemático que la base de datos puede buscar. Y quinto: guarda todo en la base de datos que entiende significados [pgvector].*

> *"El administrador ve en su panel: 'Documento indexado correctamente'. Desde ese momento, la IA ya puede responder preguntas sobre ese documento.*

> *"¿Cada cuánto se actualiza? En el momento. Si un plan cambia, se sube el nuevo y el sistema lo reemplaza al instante. No más 'ese plan ya no existe' o 'la tarifa cambió la semana pasada'."*

---

## Slide 6 — Estructura del Conocimiento (2 min)

> *"Para que la IA no invente ni se equivoque, la información se organiza en 5 tipos de fichas. Cada ficha es como una tarjeta que la IA sabe combinar.*

> *"Primero: fichas de producto. Cada plan tiene su ficha con precio, coberturas, exclusiones, para quién es, el argumento de venta, y la objeción típica con su respuesta.*

> *"Segundo: fichas de cliente. Los segmentos —adulto mayor, familia joven— con sus necesidades, cómo se sienten, cómo hablarles, qué errores evitar.*

> *"Tercero: fichas de objeciones. Cada 'lo voy a pensar' o 'está caro' con su significado real y la mejor respuesta, basada en lo que realmente funciona.*

> *"Cuarto: playbooks comerciales. ¿Qué hacer en sala de velación? Tono empático, sin venta agresiva. ¿En call center? Rápido y concreto. Cada canal tiene su receta.*

> *"Quinto: reglas de negocio. Condiciones firmes. Por ejemplo: si el cliente tiene más de 60 años y bajo presupuesto, no recomendar el plan premium. La IA no puede violar estas reglas.*

> *"Cuando el asesor pregunta, el sistema combina automáticamente estas fichas. No es un chatbot con respuestas pre-escritas. Es un sistema que orquesta conocimiento en tiempo real para dar una respuesta única para ese cliente, en ese momento, en ese canal."*

---

## Slide 7 — Control de la IA (1.5 min)

> *"¿Cómo nos aseguramos de que la IA no se desvíe? Con tres mecanismos:*

> *"Primero: el instructivo [system prompt]. Antes de cada respuesta, le decimos a Claude: responde claro, corto, en español, usa lenguaje comercial, nunca inventes, si no sabes, di que no sabes.*

> *"Segundo: las reglas de fábrica [guardrails]. Claude tiene prohibido: dar consejos legales, prometer lo que el plan no cubre, discriminar, inventar precios, recomendar fuera del portafolio.*

> *"Tercero: el filtro de datos personales [PII stripping]. Antes de que la pregunta llegue a Claude, se eliminan nombres, documentos, teléfonos, direcciones. Claude nunca recibe datos personales de los clientes. Esto es clave para cumplir la Ley 1581 de Protección de Datos."*

---

## Slide 8 — Comparativa Cloud (4 min)

> *"Esta es la diapositiva más importante para tomar la decisión. Comparamos AWS, Azure y GCP —los tres grandes— componente por componente, con costos en pesos colombianos a la tasa de $3,450 por dólar.*

> *[IR COMPONENTE POR COMPONENTE]*

> *"Autenticación: los tres son gratis para el volumen que necesitamos. AWS: 10 mil usuarios gratis. Azure y GCP: 50 mil. Para 100 asesores, los tres cuestan cero.*

> *"Puerta de entrada [API Gateway]: AWS cobra $3,450 por cada millón de llamadas. Azure: $12,075. GCP: $103,500 fijos al mes. AWS gana por mucho.*

> *"Servidores: los tres se cobran por uso, sin costo fijo mensual. Pero AWS es más barato por hora. Para 3 servicios, AWS: ~$897K. Azure y GCP: ~$1M.*

> *"Base de datos vectorial [la que entiende significados]: aquí la diferencia es enorme. AWS: ~$207K al mes con Aurora pgvector. Azure AI Search: ~$345K. GCP AlloyDB: ~$1M. AWS es 80% más barato que GCP en este componente.*

> *"IA: por 10 mil consultas al mes: AWS con Claude Sonnet: ~$517K. Azure con GPT-4o: ~$690K. GCP con Gemini: ~$172K.*

> *"Almacenamiento + CDN [S3 + CloudFront]: AWS: ~$17K. Azure: ~$86K. GCP: ~$35K. AWS es el más barato.*

> *"Cache: AWS: ~$69K. Azure: ~$103K. GCP: ~$69K.*

> *"Monitoreo [CloudWatch]: AWS: ~$69K. Azure: ~$86K. GCP: ~$69K.*

> *"Servicios auxiliares [notificaciones + workflows + eventos]: AWS: ~$17K. Azure: ~$35K. GCP: ~$17K.*

> *"Seguridad y cifrado [KMS + ACM + Lambda@Edge]: AWS: ~$12K. Azure: ~$35K. GCP: ~$7K.*

> *"Total: AWS: ~$1.8M. Azure: ~$2.4M. GCP: ~$2.5M. AWS es entre 25% y 30% más barato.*

> *"Y esto se mantiene consistente a cualquier escala. Miren la tabla de proyección: desde 10 asesores hasta 500, AWS es consistentemente 20% a 30% más barato que Azure y GCP. No importa el tamaño del proyecto.*"

---

## Slide 9 — Por qué AWS (2 min)

> *"Más allá del precio, hay tres razones de negocio:*

> *"Uno: AWS tiene presencia en Sudamérica. La región Sao Paulo tiene todos los servicios que necesitamos, con latencia de 20 a 40 milisegundos desde Colombia. Azure y GCP también tienen Brasil, pero AWS tiene más servicios disponibles allá.*

> *"Dos: no necesitamos un equipo de tecnología dedicado. Los servidores se administran solos, la base de datos escala automáticamente—si no se usa, no se paga—, la IA se paga por uso. Esto es clave para una empresa que no tiene un departamento de TI grande.*

> *"Tres: podemos cambiarnos después. Usamos PostgreSQL, Python, tecnologías abiertas. Si en el futuro Azure o GCP ofrecen mejor precio, podemos migrar sin tener que rehacer todo. No estamos atados a AWS para siempre."*

---

## Slide 10 — Costos AWS Detallados (3 min)

> *"Aquí está el detalle mensual de AWS para producción con 100 asesores. Léanlo así: cada fila es un servicio, dice para qué sirve, cómo se cobra, cuánto usamos, y cuánto cuesta.*

> *"Los rubros más grandes son:*

> *"Servidores: ~$897K. Son 3 servicios con 2 a 4 copias cada uno para garantizar disponibilidad.*

> *"IA: ~$517K para 10 mil conversaciones al mes. Eso son aproximadamente 330 conversaciones al día entre 100 asesores. Son 3 o 4 consultas por asesor por día.*

> *"Base de datos: ~$207K. Incluye datos de vectores y datos operacionales en una sola base de datos.*

> *"Total producción: ~$1.8M. Más ambiente de pruebas: ~$255K. Total: ~$2.1M.*

> *PERO: este número se reduce aplicando estrategias de optimización:*

> *"El caché de respuestas repetidas evita hasta el 68% de las llamadas a la IA. Si dos asesores preguntan lo mismo, la segunda respuesta se sirve del caché y no paga IA.*

> *"Podemos usar un modelo económico para preguntas simples —como saludos u horarios— que cuesta la tercera parte del modelo completo.*

> *"Y AWS da descuentos por compromiso anual.*

> *"Costo real estimado después de optimización: entre 1.2 y 1.8 millones de pesos al mes.*"

> *"Ahora, lo interesante: ¿cómo escala esto si crecemos? Miren la tabla de proyección.*

> *"Con 10 asesores en piloto, el costo base es de ~$636 mil al mes. Pero el costo por asesor es de ~$50 mil —porque los costos fijos de servidores y base de datos se reparten entre pocos.*

> *"Con 100 asesores —que es el escenario que hemos estado viendo— el costo por asesor baja a ~$15 mil. Es decir, cada asesor cuesta la tercera parte del piloto.*

> *"Con 500 asesores, el costo por asesor es de ~$7.500. La mitad que con 100.*

> *"¿Por qué? Por tres razones: los costos fijos se reparten entre más gente, el cache es más efectivo porque hay más preguntas repetidas, y AWS da mejores precios por volumen.*

> *"Moraleja: el sistema es más eficiente entre más asesores lo usen. Duele menos tener 500 asesores que tener 10, en términos de costo por asesor.*"

---

## Slide 11 — Comparativa de Modelos de IA (2.5 min)

> *"Comparamos los 5 modelos principales. La tabla tiene 5 filas: quién lo hizo, dónde se accede, cuánto cuesta recibir palabras, cuánto cuesta generarlas, capacidad, calidad en español, velocidad, y costo para 10 mil consultas.*

> *[SEÑALAR CADA FILA]*

> *"Claude Sonnet de Anthropic: lo recomendamos para el 80% de las consultas. Excelente calidad en español, 200 mil tokens de contexto, ~$517K para 10 mil consultas.*

> *"Claude Haiku: mismo creador, más barato, más rápido. Para consultas simples.*

> *"GPT-4o de OpenAI: excelente calidad, pero cuesta ~$690K para el mismo volumen —33% más caro que Sonnet.*

> *"GPT-4o-mini: baratísimo, pero calidad en español limitada para conversaciones emocionales como las funerarias.*

> *"Gemini 2.5 Flash de Google: el más barato y con la mayor capacidad de contexto. Pero la calidad conversacional en español es inferior a Claude y GPT. Para procesar documentos es excelente, para chatear con un asesor no es la mejor opción.*

> *"Nuestra estrategia: Haiku para consultas simples, Sonnet para las complejas, y el caché para repetidas. El costo efectivo por conversación es de aproximadamente 50 a 80 pesos.*"

---

## Slide 12 — Seguridad (2.5 min)

> *"Hablemos de seguridad, que sé que es una prioridad.*

> *"Todo el mensaje que el asesor escribe viaja cifrado con AES-256-GCM. Es el mismo estándar que usan los bancos para las transferencias y las aplicaciones de mensajería.*

> *"El cifrado funciona así: el widget y el sistema comparten una clave secreta que solo ellos conocen. El widget cifra el mensaje antes de enviarlo. Viaja por internet cifrado —nadie puede leerlo aunque lo intercepte. En CloudFront, una función descifra el mensaje y lo pasa a los servicios internos. La respuesta viaja de vuelta cifrada. El widget la descifra y el asesor la ve.*

> *"Además, los tokens de sesión expiran cada 15 minutos. Si un asesor deja la sesión abierta, el sistema la cierra automáticamente.*

> *"En cuanto a la Ley 1581 de Protección de Datos de Colombia: cumplimos en todos los frentes. El asesor informa al cliente que usa IA. Los datos no salen de AWS. Claude nunca recibe datos personales. Los clientes pueden pedir que les muestren o eliminen sus datos. Tenemos sistema de alertas por si ocurre una brecha. Y todo está cifrado durante el tránsito y en reposo.*

> *"Resumen: su información está segura. No solo por la tecnología, sino porque está diseñado para cumplir la ley colombiana."*

---

## Slide 13 — Cierre (30s)

> *"En resumen:*

> *"Un chat que los asesores usan desde su pantalla actual. Respuestas en ~2 segundos. Tecnología de Amazon Web Services. Cifrado bancario. Cumplimiento Ley 1581. Costos de nube de ~1.2 a 1.8 millones al mes. Inteligencia artificial de primera calidad con Claude Sonnet.*

> *"¿Preguntas?"*

---

## Preguntas Técnicas Frecuentes (Preparadas)

**¿Qué pasa si internet falla?**
> El widget requiere internet, pero pesa menos que una foto. Funciona con datos móviles sin problema.

**¿Los datos de Capillas de la Fe se usan para entrenar la IA de otros?**
> No. Claude se usa solo para responder preguntas. No se entrena con los datos de Capillas. Los datos nunca salen de la cuenta de AWS.

**¿Qué tan seguro es este cifrado?**
> AES-256-GCM es el estándar que usa el gobierno de Estados Unidos para información clasificada. Además, la clave se renueva cada 15 minutos.

**¿Podemos probar el sistema antes de comprometernos?**
> Sí. Parte del proceso es un piloto con 5-10 asesores reales para validar que funciona.

**¿Qué tamaño de equipo técnico necesitamos para mantener esto?**
> Con el Modelo de servicio, ninguno. Nosotros operamos todo. Solo necesitan una persona que sepa subir documentos al panel de administración.

**¿Cuánto tiempo toma ver los primeros resultados?**
> Técnicamente, desde el mes 2 el chat ya responde preguntas. El piloto con asesores reales empieza en el mes 3.

**¿Podemos escalar a más asesores después?**
> Sí. La arquitectura está diseñada para escalar. Se ajusta la capacidad según el número de asesores.

**¿Qué pasa si queremos cambiar de proveedor de nube después?**
> Es posible. Usamos tecnologías abiertas. PostgreSQL, Python y FastAPI corren en cualquier nube. Lit 3 se sirve desde cualquier CDN. No hay vendor lock-in.

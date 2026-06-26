# Guion — Presentación Técnica (Versión Negocio)

**Para ti (el desarrollador)** — pero con palabras que entienda negocio.  
**Duración:** ~20-25 min · **Audiencia:** Dirección, dueños de negocio (no técnicos)

---

## Slide 1 — Portada (30s)

*"Buenos días. Vamos a ver la parte técnica: cómo funciona el sistema por dentro, cuánto cuesta la nube, cómo protegemos los datos, y por qué tomamos cada decisión. La idea es que se vayan con la confianza de que esto es serio, seguro y que los números dan."*

---

## Slide 2 — ¿Qué es el Sistema? (1 min)

*"Empecemos con lo básico. El sistema tiene dos partes que se ven y una que no se ve.*

*"Lo que se ve: un chat flotante que los asesores usan para hacer preguntas. Y un panel de administración donde el equipo de Capillas sube los documentos. No hay que instalar nada —solo se agrega una línea al sistema actual y el widget aparece en la pantalla.*

*"Lo que no se ve es la inteligencia: corre en la nube de Amazon en Sao Paulo, todo viaja cifrado como un banco, y el sistema mejora solo con el uso."*

---

## Slide 3 — Opciones de Despliegue (1 min)

*"Antes de ver la arquitectura, hablemos de cómo se instala. Tenemos dos caminos.*

*"Opción 1 — Widget solo: si Capillas ya tiene su aplicación web con su propio login —un WordPress, un sistema de gestión, lo que sea— nosotros les damos un script que importan en su página. Ese script toma los datos del usuario —su ID, su nombre— los cifra con una llave que solo nuestro sistema conoce, los envía a nuestro servidor, y recibe un token. Ese token se lo pasa al widget. Todo el proceso es automático —el cliente solo importa el script y listo.*

*"Opción 2 — App completa: si Capillas no tiene una aplicación donde instalar el widget, o prefiere que nosotros manejemos también el inicio de sesión, construimos una aplicación completa con login incluido. Ustedes no tienen que preocuparse por nada.*

*"Las dos opciones usan el mismo motor por dentro —la misma inteligencia, la misma base de datos, el mismo cifrado— la única diferencia es quién pone la pantalla y el login."*

---

## Slide 4 — Arquitectura (3 min)

*"Acá está el diagrama de cómo se conecta todo.*

*"Del lado izquierdo está la aplicación anfitriona. En la Opción 1, es la aplicación que ya tiene Capillas. En la Opción 2, es una aplicación que nosotros construimos.*

*"Luego están los dos widgets —el de chat y el de administración— que se cargan desde una red de distribución de Amazon [señalar CloudFront]. Esto asegura que carguen rápido desde cualquier parte de Colombia.*

*"Cuando el asesor hace una pregunta, el dato viaja cifrado hasta CloudFront. Ahí una función lo descifra y lo pasa a la puerta de entrada del sistema.*

*"De ahí va al orquestador, que es el que coordina todo: verifica que el asesor tenga permiso, decide qué servicio debe responder.*

*"El orquestador habla con tres servicios internos: el que busca la información, el que gestiona los documentos, y el que mide todo.*

*"Entre estos servicios internos la comunicación es más segura aún —usan certificados digitales— y todo dentro de una red privada que no está expuesta a internet.*

*"Al final están: la base de datos que entiende significados, el caché que guarda respuestas repetidas, y la inteligencia artificial.*

*"Dato clave: el login solo aparece si elegimos la Opción 2. En la Opción 1, el login lo maneja Capillas y el widget obtiene el token mediante un intercambio seguro sin que el usuario tenga que hacer nada."*

---

## Slide 5 — Flujo de Consulta (2 min)

*"Veamos qué pasa segundo a segundo cuando un asesor pregunta algo.*

*"El asesor escribe '¿Qué plan para familia de 4 con $50 mil?' en el widget.*

*"El widget cifra esa pregunta con un estándar que usan los bancos y la envía.*

*"CloudFront recibe el dato cifrado, lo descifra, y lo pasa al sistema.*

*"El orquestador verifica la sesión y envía la consulta al servicio que busca información.*

*"Ese servicio primero revisa si ya respondió esto antes [caché]. Si la respuesta está guardada, la devuelve en menos de medio segundo. No gasta en inteligencia artificial.*

*"Si no está guardada, busca en la base de datos que entiende significados los documentos más relevantes, arma el contexto, y se lo envía a la inteligencia artificial [Claude].*

*"Claude genera la respuesta y la devuelve. El sistema la guarda en caché por si otro asesor pregunta lo mismo.*

*"La respuesta viaja de vuelta cifrada, el widget la descifra, y el asesor la ve: 'Plan Familiar Premium, $48/mes, cubre a toda la familia'.*

*"Todo esto en aproximadamente 2 segundos. Si ya se había preguntado antes, en menos de medio segundo."*

---

## Slide 6 — Ingesta de Datos (2 min)

*"¿Cómo sabe la inteligencia artificial los planes, las coberturas, las reglas? Veamos cómo entran los datos.*

*"El administrador abre el panel, arrastra un archivo —puede ser PDF, Word o texto— y lo suelta. Eso es todo lo que tiene que hacer.*

*"Detrás, ocurre esto en automático:*

*"El archivo se guarda en Amazon S3. Eso dispara un flujo automático que ejecuta varios pasos en secuencia.*

*"Primero: extrae el texto del documento. Segundo: lo divide en fragmentos pequeños para que la inteligencia artificial pueda manejarlos bien. Tercero: le pone etiquetas como 'esto es un plan, esto es una objeción, esto es para tal canal'.*

*"Cuarto: genera un código matemático del significado del texto. Y quinto: guarda todo en la base de datos que entiende significados.*

*"El administrador ve en su panel: 'Documento procesado correctamente'. Desde ese momento, la inteligencia artificial ya puede responder preguntas sobre ese documento.*

*"¿Cada cuánto se actualiza? En el momento. Si un plan cambia, se sube el nuevo y el sistema lo reemplaza al instante. No más 'ese plan ya no existe' o 'la tarifa cambió la semana pasada'."*

---

## Slide 7 — Estructura del Conocimiento (2 min)

*"Para que la inteligencia artificial no invente ni se equivoque, la información se organiza en 5 tipos de fichas.*

*"Primero: fichas de producto. Cada plan tiene su ficha con precio, coberturas, exclusiones, para quién es, el argumento de venta, y la objeción típica con su respuesta.*

*"Segundo: fichas de cliente. Los segmentos —adulto mayor, familia joven— con sus necesidades, cómo se sienten, cómo hablarles, qué errores evitar.*

*"Tercero: fichas de objeciones. Cada 'lo voy a pensar' o 'está caro' con su significado real y la mejor respuesta.*

*"Cuarto: guías de atención. Qué hacer en sala de velación —tono respetuoso, sin venta agresiva. En call center —rápido y concreto. Cada canal tiene su receta.*

*"Quinto: reglas de negocio. Condiciones firmes. Por ejemplo: si el cliente tiene más de 60 años y poco presupuesto, no recomendar el plan premium. La inteligencia artificial no puede violar estas reglas.*

*"Cuando el asesor pregunta, el sistema combina automáticamente estas fichas. No es un chatbot con respuestas fijas. Es un sistema que arma conocimiento en tiempo real para dar una respuesta única para ese cliente, en ese momento, en ese canal."*

---

## Slide 8 — Control de la IA (1.5 min)

*"¿Cómo nos aseguramos de que la inteligencia artificial no se desvíe? Con tres mecanismos:*

*"Primero: las instrucciones. Antes de cada respuesta, le decimos a Claude: responde claro, corto, en español, usa lenguaje comercial, nunca inventes, si no sabes, di que no sabes.*

*"Segundo: las reglas de fábrica. Claude tiene prohibido: dar consejos legales, prometer lo que el plan no cubre, discriminar, inventar precios, recomendar algo que no vendan.*

*"Tercero: el filtro de datos personales. Antes de que la pregunta llegue a Claude, se eliminan nombres, documentos, teléfonos, direcciones. Claude nunca recibe datos personales de los clientes. Esto es clave para cumplir la ley de protección de datos."*

---

## Slide 9 — Comparativa Cloud (4 min)

*"Esta es la diapositiva más importante para tomar la decisión. Comparamos AWS, Azure y GCP —los tres grandes— componente por componente, con costos en pesos colombianos.*

*[IR COMPONENTE POR COMPONENTE]*

*"Autenticación: los tres son gratis para el volumen que necesitamos. Para 100 asesores, los tres cuestan cero.*

*"Puerta de entrada: AWS cobra $3,450 por cada millón de llamadas. Azure: $12,075. GCP: $103,500 fijos al mes.*

*"Servidores: los tres se cobran por uso. Para 3 servicios, AWS: ~$897K. Azure y GCP: ~$1M.*

*"Base de datos: aquí la diferencia es enorme. AWS: ~$207K al mes. Azure: ~$345K. GCP: ~$1M. AWS es 80% más barato que GCP en este componente.*

*"IA: por 10 mil consultas al mes: AWS con Claude: ~$517K. Azure con GPT: ~$690K. GCP con Gemini: ~$172K.*

*"Almacenamiento: AWS: ~$17K. Azure: ~$86K. GCP: ~$35K.*

*"Caché: AWS: ~$69K. Azure: ~$103K. GCP: ~$69K.*

*"Monitoreo: AWS: ~$69K. Azure: ~$86K. GCP: ~$69K.*

*"Servicios auxiliares: AWS: ~$17K. Azure: ~$35K. GCP: ~$17K.*

*"Seguridad: AWS: ~$12K. Azure: ~$35K. GCP: ~$7K.*

*"Total: AWS: ~$1.8M. Azure: ~$2.4M. GCP: ~$2.5M. AWS es entre 25% y 30% más barato.*

*"Y esto se mantiene a cualquier escala. AWS es consistentemente más barato que Azure y GCP, sin importar el tamaño del proyecto."*

---

## Slide 10 — Por qué AWS (2 min)

*"Más allá del precio, hay tres razones de negocio:*

*"Uno: AWS tiene presencia en Sudamérica. La región de Sao Paulo está a 20-40 milisegundos de Colombia. Azure y GCP también tienen Brasil, pero AWS tiene más servicios disponibles allá.*

*"Dos: no necesitamos un equipo de tecnología dedicado. Los servidores se administran solos, la base de datos escala automáticamente —si no se usa, no se paga—, la inteligencia artificial se paga por uso. Esto es clave para una empresa que no tiene un departamento de TI grande.*

*"Tres: podemos cambiarnos después. Usamos tecnologías abiertas que corren en cualquier nube. Si en el futuro Azure o GCP ofrecen mejor precio, podemos migrar sin tener que rehacer todo. No estamos atados a AWS para siempre."*

---

## Slide 11 — Costos AWS Detallados (3 min)

*"Aquí está el detalle mensual de AWS para producción con 100 asesores. Cada fila es un servicio, dice para qué sirve, cómo se cobra y cuánto cuesta.*

*"Los rubros más grandes son:*

*"Servidores: ~$897K. Son 3 servicios con 2 a 4 copias cada uno para garantizar disponibilidad.*

*"IA: ~$517K para 10 mil consultas al mes. Eso son aproximadamente 3 o 4 consultas por asesor por día.*

*"Base de datos: ~$207K. Incluye datos de vectores y datos operacionales en una sola base.*

*"Total producción: ~$1.8M. Más ambiente de pruebas: ~$255K. Total: ~$2.1M.*

*"PERO: este número se reduce con optimizaciones:*

*"El caché de respuestas repetidas evita hasta el 68% de las llamadas a la IA. Si dos asesores preguntan lo mismo, la segunda respuesta se sirve del caché y no paga IA.*

*"Podemos usar un modelo económico para preguntas simples —como saludos u horarios— que cuesta la tercera parte del modelo completo.*

*"Costo real estimado después de optimización: entre 1.2 y 1.8 millones de pesos al mes.*

*"Ahora, lo interesante: ¿cómo escala esto si crecemos?*

*"Con 10 asesores en piloto, el costo base es de ~$636 mil al mes. Pero el costo por asesor es de ~$50 mil —porque los costos fijos de servidores y base de datos se reparten entre pocos.*

*"Con 100 asesores, el costo por asesor baja a ~$15 mil. Cada asesor cuesta la tercera parte del piloto.*

*"Con 500 asesores, el costo por asesor es de ~$7.500. La mitad que con 100.*

*"¿Por qué? Los costos fijos se reparten entre más gente, el caché es más efectivo porque hay más preguntas repetidas, y AWS da mejores precios por volumen.*

*"Moraleja: el sistema es más eficiente entre más asesores lo usen."*

---

## Slide 12 — Comparativa de Modelos de IA (2.5 min)

*"Comparamos los 5 modelos principales. La tabla muestra: quién lo hizo, cuánto cuesta, calidad en español, velocidad, y costo para 10 mil consultas.*

*[SEÑALAR CADA FILA]*

*"Claude Sonnet: lo recomendamos para la mayoría de las consultas. Excelente calidad en español. ~$517K para 10 mil consultas.*

*"Claude Haiku: mismo creador, más barato, más rápido. Para consultas simples.*

*"GPT-4o de OpenAI: excelente calidad, pero cuesta ~$690K —33% más caro que Sonnet.*

*"GPT-4o-mini: baratísimo, pero calidad en español limitada para conversaciones emocionales como las funerarias.*

*"Gemini de Google: el más barato y con mayor capacidad. Pero la calidad conversacional en español es inferior a Claude y GPT.*

*"Nuestra estrategia: modelo barato para consultas simples, modelo caro para las complejas, y caché para repetidas. El costo efectivo por conversación es de aproximadamente 50 a 80 pesos."*

---

## Slide 13 — Seguridad (2.5 min)

*"Hablemos de seguridad.*

*"Todo el mensaje que el asesor escribe viaja cifrado. Es el mismo estándar que usan los bancos.*

*"El cifrado funciona así: el widget y el sistema comparten una clave secreta que solo ellos conocen. El widget cifra el mensaje antes de enviarlo. Viaja por internet cifrado —nadie puede leerlo aunque lo intercepte. En CloudFront, una función descifra el mensaje y lo pasa a los servicios internos. La respuesta viaja de vuelta cifrada. El widget la descifra y el asesor la ve.*

*"Además, las sesiones expiran cada 15 minutos. Si un asesor deja la sesión abierta, el sistema la cierra automáticamente.*

*"En cuanto a la ley de protección de datos de Colombia: cumplimos en todos los frentes. El asesor informa al cliente que usa inteligencia artificial. Los datos no salen de AWS. Claude nunca recibe datos personales. Los clientes pueden pedir que les muestren o eliminen sus datos. Y todo está cifrado.*

*"Resumen: su información está segura. No solo por la tecnología, sino porque está diseñado para cumplir la ley colombiana."*

---

## Slide 14 — Cierre (30s)

*"En resumen:*

*"Un chat que los asesores usan desde su pantalla actual. Respuestas en ~2 segundos. Tecnología de Amazon. Cifrado bancario. Cumplimiento de ley de protección de datos. Costos de nube de ~1.2 a 1.8 millones al mes. Inteligencia artificial de primera calidad con Claude.*

*"Y lo importante: no necesitan tener una aplicación para empezar. Si ya tienen plataforma, es la Opción 1 —solo importan un script y listo. Si no, la Opción 2 —hacemos todo, incluido el login. Las dos opciones usan el mismo motor de inteligencia artificial.*

*"¿Preguntas?"*

---

## Preguntas Técnicas Frecuentes (Preparadas)

**¿Qué pasa si internet falla?**
> El widget requiere internet, pero pesa menos que una foto. Funciona con datos móviles sin problema.

**¿Los datos de Capillas se usan para entrenar la inteligencia artificial de otros?**
> No. Claude se usa solo para responder preguntas. No se entrena con los datos de Capillas. Los datos nunca salen de la cuenta de AWS.

**¿Qué tan seguro es este cifrado?**
> Es el mismo estándar que usa el gobierno de Estados Unidos para información clasificada. Además, la clave se renueva cada 15 minutos.

**¿Podemos probar el sistema antes de comprometernos?**
> Sí. Parte del proceso es un piloto con 5-10 asesores reales para validar que funciona.

**¿Qué tamaño de equipo técnico necesitamos para mantener esto?**
> Con el modelo de servicio, ninguno. Nosotros operamos todo. Solo necesitan una persona que sepa subir documentos al panel de administración.

**¿Cuánto tiempo toma ver los primeros resultados?**
> Desde el mes 2 el chat ya responde preguntas. El piloto con asesores reales empieza en el mes 3.

**¿Podemos escalar a más asesores después?**
> Sí. La arquitectura está diseñada para escalar. Se ajusta la capacidad según el número de asesores.

**¿Qué pasa si queremos cambiar de proveedor de nube después?**
> Es posible. Usamos tecnologías abiertas que corren en cualquier nube. No hay vendor lock-in.

**¿Qué necesitamos de nuestra parte para la Opción 1?**
> Una aplicación web donde puedan importar un script —WordPress, sistema de gestión, lo que sea— y que tenga los datos del usuario disponibles (ID, nombre, email) después de que el usuario inicia sesión. El script se encarga de todo el proceso de seguridad y obtiene el token automáticamente. Ustedes no hacen nada más.

**Si elegimos Opción 2, ¿nos quedamos sin control del login?**
> No. Nosotros configuramos el sistema de login con su dominio, sus reglas de contraseña, su recuperación de cuenta. Ustedes administran los usuarios desde una consola. Y si después quieren pasar su propio login, se puede —solo cambia la forma en que el widget recibe el token.

**¿Podemos empezar con Opción 1 y después pasar a Opción 2?**
> Sí. Si empiezan con su propio login y después deciden que nosotros administremos la aplicación, migramos los usuarios y el widget sigue funcionando igual. El motor es el mismo.

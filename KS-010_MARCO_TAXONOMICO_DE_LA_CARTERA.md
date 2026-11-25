# KS-010 · Marco taxonómico de la cartera tecnológica

**Edición** · 1.0, 25 de noviembre de 2026  
**Ámbito** · Clasificación y trazabilidad de la cartera de I+D  
**Autoridad** · Convenciones de la cartera subordinadas a la Especificación Estratégica y a RDL-PB-001 v0.1. La aprobación del trabajo documental y la adopción institucional de una convención tienen actos distintos.

[Mapa de la cartera](KS-011_MAPA_DE_DOMINIOS_ESPECIALIDADES_Y_CAPACIDADES.md) · [Expediente de especializaciones](KS-012_ESPECIALIZACIONES_DE_SIGUIENTE_GENERACION.md)

## 1. Vocabulario

| Término | Definición de uso en la cartera | Ejemplo |
| --- | --- | --- |
| Dominio de actividad de I+D | Clase de actividad institucional según la Especificación, §8. | Desarrollo tecnológico, investigación tecnológica, desarrollo de capacidades de investigación o desarrollo de conocimiento. |
| Dominio tecnológico | Campo de problemas en el que se desarrolla o explora competencia, con restricciones y criterios propios. | Finanzas cuantitativas. |
| Dominio de validez | Condiciones bajo las que se sostiene una propiedad, una evidencia o una afirmación. Aplica RDL-PB-001 §12. | Un consumidor temporal, un escritor, entregas válidas y recepción simulada. |
| Especialidad | Familia delimitada de problemas que comparte preguntas, métodos o criterios de aceptación. Puede figurar en un dominio principal y tener vínculos transversales. | Evaluación temporal de pronósticos. |
| Capacidad | Aptitud para ejecutar una acción y producir un resultado bajo condiciones explícitas. Puede ser tecnológica, de investigación u operacional. | Reconstruir el insumo y el resultado de una decisión histórica ante una revisión tardía. |
| Objeto de investigación | Entidad concreta interrogada conforme al Playbook. Registrar revisión y contexto cuando la afirmación dependa de ellos. | El selector GEI de TN en una revisión fijada. |
| Instrumento | Medio utilizado para producir o examinar resultados según el Playbook. | Una perturbación del sufijo, un oráculo manual, un evaluador por origen. |
| Laboratorio | Conjunto organizado de instrumentos, protocolos y medios de ejecución para una clase de preguntas. Puede ser instrumento de una investigación u objeto de otra. | Un laboratorio cuantitativo para pronósticos o WORLD-LAB para interacción dinámica. |
| Activo reutilizable | Activo de ingeniería o metodológico identificable y con un uso candidato. La transferencia requiere un contexto receptor y revalidación cuando cambien sus supuestos. | Registro SQLite, arnés de replay, criterio de descenso para recurrencias. |
| Infraestructura operativa | Conjunto identificable de componentes y procedimientos que sostiene un uso dentro de un perfil operativo respaldado por evidencia. | Motor, protocolos y registro de WORLD-LAB en su perfil congelado. |
| Proyecto, repositorio y versión | Un proyecto organiza trabajo. El repositorio conserva fuentes y evidencia. La versión fija una identidad técnica o documental. | Computational-Lab conserva un entorno y una copia del núcleo TN que también se estudia en tn-ea. |

«Espacio de competencia» puede nombrar una **hipótesis estratégica** sobre un dominio. Para acreditar competencia hay que identificar la capacidad, su perfil de uso y la referencia frente a la que se evalúa. Un campo explorado conserva su lugar en el mapa con ese alcance.

## 2. Reglas de clasificación

1. **Identificar desde la pregunta.** Usar el campo de problemas para ubicar el dominio, la familia de preguntas para delimitar la especialidad y el objeto concreto para adjudicar la evidencia.
2. **Registrar capacidades por resultado.** Usar la forma «realizar acción, producir resultado, bajo condiciones». Vincular instrumento, activo, consumidor, fuente, revisión, control y límite. Una sola capacidad puede servir a varios dominios.
3. **Resolver identidades antes de sumar.** Contar una identidad tecnológica una vez. Vincular copias, variantes, derivados, ejecuciones y expedientes. Una variante con comportamiento propio requiere identificación y evidencia propias. Una copia exacta no aumenta el número de tecnologías ni la independencia de una réplica.
4. **Conservar la dirección de las relaciones.** Una especialidad requiere capacidades. Un instrumento ejerce o examina una capacidad. Un activo puede sostener varios instrumentos. La evidencia respalda una afirmación delimitada. Un fallo demuestra el límite del candidato bajo el contraste registrado y puede dejar un control transferible.
5. **Indicar cómo se sostiene cada afirmación.** Usar los términos del Playbook y su alcance. Describir si procede de especificación, deducción, ejecución observada, contraste verificado o validación en contexto. La mera presencia de código acredita implementación identificable. Una construcción propuesta conserva su estado de diseño hasta tener evidencia de ejecución.
6. **Registrar madurez por uso.** Expresar el alcance con hechos como exploración documentada, piloto acotado, operación verificada en un perfil o uso de campo reportado. Una misma tecnología puede tener perfiles con madurez diferente. Si falta evidencia, registrar qué afirmación queda abierta y qué prueba resolvería la incertidumbre.
7. **Transferir con condiciones.** Identificar qué se conserva, qué se adapta, qué debe volver a verificarse y cuánto trabajo exige. Distinguir un contrato general demostrado bajo supuestos, una transferencia observada y una hipótesis sobre aplicaciones futuras.

## 3. Casos de calibración

| Caso | Clasificación aplicada | Consecuencia para el inventario |
| --- | --- | --- |
| TN | Modelo y núcleo de decisión bajo estudio. Pronóstico y adaptación son preguntas de finanzas y modelado. TN-LAB es instrumento. El observador LAB2 es un sistema distinto. | Un núcleo con relaciones de procedencia y variantes. Evidencia de laboratorio, modelo y observador vinculada por separado. |
| F001 | Objeto de derivación algorítmica, con formulación matemática e implementación histórica. | El contraejemplo y la prueba de dominio y descenso se catalogan como evidencia y método para diseños futuros. |
| WORLD-LAB y TITAN | WORLD-LAB es instrumento de entornos dinámicos y sistema con un perfil operativo. TITAN es objeto de investigación. D4 es una integración ensayada. | El replay del motor, la equivalencia acotada del adaptador y la reanudación del agente sustentan afirmaciones distintas. |
| Laboratorio cuantitativo | Familia de instrumentos especializados. Puede ejercer evaluación por origen, validación de señales o simulación de ejecución. | Las capacidades se acreditan por contrato y propósito experimental. Pronóstico, rendimiento simulado y utilidad de mercado requieren evidencia diferente. |
| Laboratorio de datos | Instrumentos para estudiar ingesta, calidad, revisiones, lineage o reconciliación. Un pipeline puede ser objeto de prueba o componente operativo. | El mismo registro puede apoyar datos y finanzas. La admisión de cada fuente se verifica en su contexto. |
| CYBERsec | Prototipo histórico y exploración documentada. | La presencia en la cartera registra experiencia exploratoria. Una capacidad defensiva futura requerirá sistema, requisito y evidencia propios. |

## 4. Aplicación y revisión

La Especificación Estratégica, §§8 y 11–12, gobierna la actividad, la arquitectura experimental y la selección proporcional del instrumento. El Playbook, §§3, 5, 11–14 y 20, gobierna los objetos de investigación, la evidencia, el alcance y las decisiones. Este marco aporta las convenciones de inventario necesarias para relacionarlos.

Una revisión multidisciplinaria registra **afirmación, supuesto, evidencia, objeción y decisión afectada**. Se invita a cada disciplina cuando su objeción puede cambiar una clasificación, requisito, prueba o inversión. Los casos frontera se resuelven por evidencia y propósito de uso. Se conserva el desacuerdo cuando la decisión queda abierta.

[Especificación Estratégica](https://chatgpt.com/library?file_id=libfile_e0932365a6ac8191a15982b0355879e0&account_id=personal) · [RDL-PB-001 v0.1](docs/program/RDL-PB-001_v0.1_original_propuesta.md) · [Evaluación de la cartera](KS-001_EVALUACION_CARTERA.md)

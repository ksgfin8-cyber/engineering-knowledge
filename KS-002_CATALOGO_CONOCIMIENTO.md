# KS-002 · Catálogo de conocimiento de ingeniería

**Corte documental:** 24 de noviembre de 2026. **Etapa:** consolidación, primera extracción de los 14 repositorios tecnológicos evaluados en [KS-001](KS-001_EVALUACION_CARTERA.md). **Marco:** Especificación Estratégica de I+D v1.0, §§18–25. RDL-PB-001 v0.1, §§7, 9–14 y 19–23. [Playbook y acta de adopción](https://github.com/ksgfin8-cyber/yellow/tree/5d40f08/docs/program)

## Uso del catálogo

Para diseñar una prueba o construcción, localizar la capacidad que requiere la pregunta, consultar el registro y confirmar que sus precondiciones se cumplen en el nuevo objeto. Los expedientes vinculados fijan las revisiones y el alcance de las pruebas originales. Los usos en proyectos futuros se registran como propuestas. La evidencia obtenida en un nuevo receptor debe conservar su propia configuración, comparación y decisión.

| Pregunta de ingeniería | Registros |
| --- | --- |
| ¿La formulación y el código usan unidades y contratos coherentes? | [F001](#kc-01), [unidades de TN](#kc-02), [semántica de AURORA](#kc-12) |
| ¿El modelo usa solo la información disponible y se puede reconstruir lo ocurrido? | [cortes de TN](#kc-03), [escenarios](#kc-04), [admisión de LAB2](#kc-05), [instantáneas](#kc-06) |
| ¿Se puede confiar en los datos, la contabilidad o el comparador? | [datos XAUUSD](#kc-09), [contabilidad](#kc-10), [detección de divergencia](#kc-11) |
| ¿Es necesario estudiar interacción, decisión o equivalencia de un controlador? | [WORLD-LAB](#kc-07), [TITAN D4](#kc-08), [consenso de Viper](#kc-13) |
| ¿Cómo verifico la compatibilidad, la entrega o la adopción de un componente? | [pedidos](#kc-14), [extensión InHouse](#kc-15), [admisión de prototipos](#kc-16) |

## A. Formulación, algoritmos y evaluación temporal

<a id="kc-01"></a>
### KC-01 · Partición y descenso en una recurrencia

**Evidencia.** En F001, el caso `[2,1]` produce una llamada inválida al sustituir valores en la recurrencia escrita. El código histórico modifica el arreglo y termina con una excepción.  
**Uso propuesto.** Algoritmos recursivos que dividen, rotan o fusionan segmentos. Especificar cobertura, pertenencia al dominio, progreso y tratamiento de vacíos antes de implementar la recurrencia completa.  
**Condición de uso.** La geometría alternativa del expediente es una hipótesis para la implementación. La corrección funcional y el coste de una variante *in-place* requieren evidencia propia. [F001-R01](https://github.com/ksgfin8-cyber/f001/blob/2b60f32/docs/research/F001_RDL_PB_001_EVALUATION.md)

<a id="kc-02"></a>
### KC-02 · Consistencia dimensional entre representación, pronóstico y error

**Evidencia.** T1 de TN usa la media de log-retornos como nivel de reversión. La réplica encontró −27,08 en una serie cercana a 102. Un centro expresado en precios redujo el MAE en el control, y esa variante fija perdió frente a Random Walk en las nueve trayectorias.  
**Uso propuesto.** Modelos que convierten características en pronósticos o acciones. Registrar la unidad de entrada, salida, objetivo y pérdida. Forzar un caso de nivel y cambio conocido para verificar el contrato.  
**Condición de uso.** El control corregía un comparador fijo. El efecto de incorporar la variante a GEI queda NO EVALUADO. [Réplica TN-R01](https://github.com/ksgfin8-cyber/tn-ea/blob/ee49ac7/docs/research/TN_R01_REPLICATION.md)

<a id="kc-03"></a>
### KC-03 · Cortes internos y externos de información

**Evidencia.** En el caso probado, añadir un sufijo conservó las 70 filas comunes proyectadas. Al recalcular los descriptores para cada origen interno, en vez de usar la ventana envolvente, cambiaron los errores de cinco teorías en la ventana ensayada.  
**Uso propuesto.** Pronósticos, selección adaptativa y cualquier evaluación que reconstruya decisiones pasadas. Probar invariancia de prefijo para las salidas externas y controlar por separado qué datos consulta cada cálculo interno.  
**Condición de uso.** Fijar origen, horizonte, información disponible y medida de error. El cambio de selección al sustituir todos los insumos internos queda NO EVALUADO. [Réplica TN-R01](https://github.com/ksgfin8-cyber/tn-ea/blob/ee49ac7/docs/research/TN_R01_REPLICATION.md)

<a id="kc-04"></a>
### KC-04 · Comparación emparejada y perturbación de escenarios

**Evidencia.** Computational-Lab localizó un desplazamiento de etiquetas en Exp. 20 y una cola global en Exp. 21. Tras alinear objetivos por origen, el resultado de GEI varió por escenario. La persistencia del selector quedó expuesta por un cambio sintético conocido.  
**Uso propuesto.** Comparar un selector con una política fija y una referencia simple usando los mismos objetivos, y calcular el error antes y después de un cambio controlado.  
**Condición de uso.** Conservar generador, semillas, ventanas y comparadores. Los resultados son del banco declarado. La generalización de mercado requiere datos y una evaluación propios. [Computational-Lab-R01](https://github.com/ksgfin8-cyber/Computational-Lab/blob/55b43dd/docs/research/COMPUTATIONAL_LAB_RDL_PB_001_EVALUATION.md)

## B. Estado, observación y entornos dinámicos

<a id="kc-05"></a>
### KC-05 · Admisión antes de mutar el estado

**Evidencia.** En LAB2, un duplicado cambió la memoria aunque la persistencia descartó su fila. Una vela parcial y su revisión final tampoco quedaron representadas fielmente. El control con acumulador reprodujo el defecto.  
**Uso propuesto.** Observadores, pipelines de telemetría, simuladores y servicios que reciben eventos repetidos o revisables. Probar un evento nuevo, una repetición, una revisión y un reinicio con estados esperados.  
**Condición de uso.** Definir identidad, orden, política de revisiones y momento de *commit*. La transferencia de un contrato corregido a otro receptor queda por demostrar. [LAB2-R01](https://github.com/ksgfin8-cyber/LAB2/blob/0c21d18/docs/research/LAB2_RDL_PB_001_EVALUATION.md)

<a id="kc-06"></a>
### KC-06 · Instantánea y reconstrucción fiel

**Evidencia.** En la réplica de TN, la primera fila contenía una transición al registrarse y 22 al releerse al final por colecciones compartidas. BOX1 mostró una mutación equivalente del valor retenido después de la captura. Su ensayo HTTP usó un doble de almacenamiento.  
**Uso propuesto.** Sistemas de auditoría, captura y evolución de estado. Observar un registro al emitirlo y otra vez después de modificar el estado de origen. Si hay persistencia, comprobar el recorrido de escritura y lectura con el almacenamiento real.  
**Condición de uso.** Fijar qué se conserva por valor, en qué representación y cómo se identifica el instante. Un doble HTTP permite probar la ruta ejercitada. La fidelidad de almacenamiento requiere una comprobación propia. [TN](https://github.com/ksgfin8-cyber/tn-ea/blob/ee49ac7/docs/research/TN_R01_REPLICATION.md) · [BOX1-R01](https://github.com/ksgfin8-cyber/box1-runtime/blob/69e5c88/docs/research/BOX1_RDL_PB_001_EVALUATION.md)

<a id="kc-07"></a>
### KC-07 · Entorno reproducible de interacción agente–mundo

**Evidencia.** WORLD-LAB tiene un perfil congelado y P01 documenta 256 replays sobre 32 semillas con el mismo motor. La evidencia abarca una configuración identificada del mundo y sus interfaces.  
**Uso disponible.** Investigar políticas con efectos acumulados, observaciones parciales y acciones discretas dentro del perfil aprobado. Una pregunta de interacción dinámica debe justificar su uso.  
**Condición de uso.** Verificar compatibilidad del agente, configuración y criterio de comparación. La interoperabilidad externa, RC1 y TITAN G2 tienen estados y decisiones propios. [Acta operacional](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/audits/WORLD_LAB_OPERATIONAL_FREEZE.md)

<a id="kc-08"></a>
### KC-08 · Control directo para decidir si un mecanismo añade conducta

**Evidencia.** Para TITAN-MVP-01 en D4, un controlador directo de prioridades coincidió en las 2.401 combinaciones y las 7.903 comparaciones documentadas.  
**Uso propuesto.** Comparar una política elaborada con una regla más simple en un dominio enumerable. Incluir decisiones, memoria y primera divergencia.  
**Condición de uso.** El resultado de D4 permanece limitado al adaptador y a sus condiciones. Una investigación nueva requiere un caso donde la propiedad estudiada pueda producir una diferencia relevante. [Equivalencia D4](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/research/titan-mvp-01/EQUIVALENCE_VERIFICATION.md)

## C. Datos, contabilidad y conformidad

<a id="kc-09"></a>
### KC-09 · Dato preparado, procedencia y corte de ajuste

**Evidencia.** Filtrado y FASES1234 comparten el mismo CSV XAUUSD y su reporte. La auditoría del archivo es repetible y el generador candidato permite identificar ajustes globales. Ajustar la imputación solo en entrenamiento cambió 78 valores imputados de validación y prueba. El bruto autenticado sigue pendiente.  
**Uso propuesto.** Preparación de series temporales y revisión de datasets con imputación. Fijar fuente, versión, ventana de ajuste e instante de disponibilidad por variable.  
**Condición de uso.** El dataset publicado permite descripción acotada. La regeneración y el significado económico de los ceros de spread requieren insumos adicionales. [FASES1234-R01](https://github.com/ksgfin8-cyber/FASES1234/blob/dc42400/docs/research/FASES1234_RDL_PB_001_EVALUATION.md) · [Filtrado-R01](https://github.com/ksgfin8-cyber/Filtrado/blob/e93a6bb/docs/research/FILTRADO_RDL_PB_001_EVALUATION.md)

<a id="kc-10"></a>
### KC-10 · Oráculo contable con precio constante

**Evidencia.** En Indicadores, a precio constante el registro histórico dio −0,20 % y la curva −0,3996 %. La prueba permite aislar costes y tratamiento de entradas, salidas y liquidación.  
**Uso propuesto.** Backtesters y simuladores con inventario, capital y costes. Construir secuencias mínimas de transición y reconciliar eventos, posiciones y capital con una cuenta manual.  
**Condición de uso.** Definir modelo de ejecución y denominadores antes de comparar. El fallo del motor actual delimita la evidencia de rendimiento obtenida con él. [Indicadores-R01](https://github.com/ksgfin8-cyber/Indicadores/blob/184f41a/docs/research/INDICADORES_RDL_PB_001_EVALUATION.md)

<a id="kc-11"></a>
### KC-11 · Sensibilidad del comparador e independencia de referencia

**Evidencia.** En Filtrado, una perturbación unilateral localizó la primera divergencia en `ema_fast`. La misma implementación alimentaba las rutas principales y el arnés omitía `close_window`. QV-R01 documentó que el núcleo mínimo tiene un contrato distinto de Quantum Viper v1.5c.  
**Uso propuesto.** Comparación entre runtimes, implementaciones, versiones o serializadores. Inyectar un desacuerdo conocido para probar la sensibilidad del instrumento y verificar qué campos cubre.  
**Condición de uso.** La equivalencia exige una referencia pertinente e independiente para la afirmación estudiada, configuración y calentamiento alineados. La concordancia con Pine permanece NO EVALUADA en los expedientes citados. [Filtrado-R01](https://github.com/ksgfin8-cyber/Filtrado/blob/e93a6bb/docs/research/FILTRADO_RDL_PB_001_EVALUATION.md) · [QV-R01](https://github.com/ksgfin8-cyber/quantum-viper/blob/f55fc60/docs/research/QUANTUM_VIPER_RDL_PB_001_EVALUATION.md)

## D. Indicadores y contratos de producto

<a id="kc-12"></a>
### KC-12 · Coherencia semántica entre fórmula, clasificación y presentación

**Evidencia.** En AURORA, el caso de rango y volatilidad conjunta separa panel e histograma. Una serie plana produjo φ=1 y Ω=0,5 en el oráculo local. La fórmula histórica de volatilidad con signo difiere del valor absoluto que usa el Pine examinado.  
**Uso propuesto.** Indicadores, clasificadores y paneles con varios consumidores de un mismo estado. Construir tabla de estados y precedencias y probar simetrías, reposo y calentamiento.  
**Condición de uso.** La elección de semántica y la autoridad del documento histórico sobre el candidato actual requieren decisión propia. Utilidad externa y concordancia Pine quedan NO EVALUADAS. [AURORA-R01](https://github.com/ksgfin8-cyber/aurora/blob/e6792fd/docs/research/AURORA_RDL_PB_001_EVALUATION.md) · [Contrato histórico](https://github.com/ksgfin8-cyber/Indicadores/blob/184f41a/archive/dead_strategies/AURORA_SYSTEM_FREEZE_v1.4.md) · [Pine examinado](https://github.com/ksgfin8-cyber/aurora/blob/37a05cc/codigo)

<a id="kc-13"></a>
### KC-13 · Cotas, abstención, memoria y expiración

**Evidencia.** Por la cota del peso de P2 y el mínimo de apoyos, P2 puede bloquear la dirección que respalda con el umbral por defecto de Viper. La memoria usa el signo del resultado neto. El contador NRT puede llegar a cero con el nivel todavía visible.  
**Uso propuesto.** Sistemas de decisión con agregación, memoria o estados con vigencia. Deducir qué salidas admite el diseño y aislar un mecanismo por prueba. En el límite de expiración, comprobar visibilidad y estado persistente por separado.  
**Condición de uso.** La finalidad de cada mecanismo requiere un contrato de producto. Los resultados algebraicos y locales conservan su alcance. [QV-R01](https://github.com/ksgfin8-cyber/quantum-viper/blob/f55fc60/docs/research/QUANTUM_VIPER_RDL_PB_001_EVALUATION.md)

## E. Aplicaciones, extensibilidad y evaluación de prototipos

<a id="kc-14"></a>
### KC-14 · Confirmación en una frontera externa

**Evidencia.** Almuerzos Ecuador produjo el estado interno `ENVIADO` en el caso donde la apertura del canal devolvió `null`. El expediente permite reconstruir el flujo de pedido y la frontera con la entrega.  
**Uso propuesto.** Pedidos, notificaciones y aplicaciones que delegan una operación a otro servicio. Definir qué evidencia corresponde a preparación, intento y recepción confirmada.  
**Condición de uso.** La confirmación externa necesita señal del sistema receptor o un procedimiento operacional verificable. [AE-R01](https://github.com/ksgfin8-cyber/almuerzos-ecuador/blob/af7cf32/docs/research/almuerzos-ecuador-rdl-pb-001.md)

<a id="kc-15"></a>
### KC-15 · Extensión conservadora bajo contexto compartido

**Evidencia.** EscanningQR conservó el modo normal de Almuerzos Ecuador en 10.080 minutos para dos pedidos bajo condiciones emparejadas. La introducción de InHouse reveló una combinación incoherente entre etiqueta y despacho cuando los componentes interpretan contextos distintos.  
**Uso propuesto.** Extender un sistema con una modalidad, canal o configuración. Comparar la ruta preexistente y comprobar la propagación del contexto en la ruta nueva.  
**Condición de uso.** Fijar catálogo, reloj y contrato de cada componente. Escaneo y entrega de campo requieren su propia evaluación. [EQ-R01](https://github.com/ksgfin8-cyber/escanningqr/blob/55b999f/docs/research/ESCANNINGQR_RDL_PB_001_EVALUATION.md)

<a id="kc-16"></a>
### KC-16 · Admisión de un prototipo como biblioteca

**Evidencia.** CYBERsec-R01 documentó un fallo de importación y límites en el dominio y la evidencia de las métricas. La relación con TITAN formal permanece abierta.  
**Uso propuesto.** Revisión de admisión de prototipos de cualquier dominio. Verificar una importación por la interfaz declarada, un contrato mínimo y la correspondencia entre afirmaciones y mediciones antes de recomendar integración.  
**Condición de uso.** El fallo histórico concierne a la revisión evaluada. Su reapertura requiere una revisión candidata y evidencia pertinente a la propiedad reclamada. [CYBERsec-R01](https://github.com/ksgfin8-cyber/CYBERsec/blob/944297f/docs/research/CYBERSEC_RDL_PB_001_EVALUATION.md)

## Primera selección para el siguiente ciclo

| Receptor candidato o clase de proyectos | Activos a recuperar | Primera decisión que pueden informar |
| --- | --- | --- |
| **Variante experimental de TN** | KC-02, KC-03 y KC-04 | Si hay una hipótesis sobre selección adaptativa que justifique construir una variante, y qué unidades, orígenes y comparadores se fijarán antes de hacerlo. |
| **Nueva variante de ordenamiento recursivo** | KC-01 y KC-08 | Si la partición propuesta respeta sus obligaciones de dominio y descenso, y cuál es la referencia que permitiría evaluar su diferencial. |
| **Procesamiento de eventos revisables** | KC-05 y KC-06 | Si un registro ofrece garantías suficientes de admisión, persistencia y recuperación para el uso previsto. LAB2 es un receptor candidato. Un sistema de telemetría representa una clase de uso adicional. |
| **Conformidad de un indicador o aplicación** | KC-11, KC-12, KC-13 y KC-15 | Qué contrato debe comprobarse y qué referencia puede distinguir el primer incumplimiento. |

Los antecedentes del propietario sobre campañas cuantitativas sin registros conservados se utilizan para priorizar revisión de fórmulas y casos mínimos antes de presupuestar una campaña. Los resultados de esas campañas permanecen sin verificar. Este corte conserva los contrastes ya documentados y no añade resultados experimentales. La selección de posibles receptores orienta el siguiente ciclo. La transferencia y el efecto sobre coste o productividad requieren ejecución y registro propios.

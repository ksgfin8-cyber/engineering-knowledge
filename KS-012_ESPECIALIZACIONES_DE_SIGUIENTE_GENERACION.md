# KS-012 · Especializaciones de siguiente generación

**Cierre de investigación** · 25 de noviembre de 2026  
**Decisión solicitada en la fase siguiente** · Seleccionar un consumidor y una construcción inicial conforme a la secuencia de este expediente. Las disposiciones son recomendaciones de inversión y especificación.

[Marco taxonómico](KS-010_MARCO_TAXONOMICO_DE_LA_CARTERA.md) · [Mapa de capacidades](KS-011_MAPA_DE_DOMINIOS_ESPECIALIDADES_Y_CAPACIDADES.md) · [Cuatro planos v0.1](disenos/siguiente-generacion/README.md)

## 1. Evaluación temporal de pronósticos

**Usuario y problema.** Un investigador cuantitativo que necesita comparar pronósticos sobre orígenes y horizontes idénticos y reconstruir la información vista por cada candidato. La ventana global en TN-LAB y la perturbación del sufijo de KS-004 mostraron por qué especificar el origen modifica el diseño del evaluador. La cadena VIX demostró evaluación histórica sobre 444 orígenes con reloj simulado.

**Resultado R01.** El archivo por anexado y SQLite satisficieron las nueve comprobaciones de resultado por motor para un productor local, un escritor y cuatro entregas. La decisión histórica H conservó D1 y 10 puntos. La retrospectiva incorporó D2 y 14. P conservó 14 tras cargar D4, que sí produjo 99 cuando fue admisible. El control que consulta la última revisión asignó 14 a H y falló por cuatro puntos. En la ruta de revisión, el archivo necesitó una lectura y un anexado, frente a dos consultas de identidad y tres escrituras en una transacción de SQLite. Ambos se operaron con una invocación. Los recuentos describen esta ejecución y el coste total recurrente quedó abierto.

**Construcción candidata.** Un consumidor, una fuente identificada, archivo versionado de solo anexado y script. Conservar bruto, identidad de observación y entrega, instante del dato, publicación cuando exista, recepción observada, regla ejecutable, corte y frontera de la decisión. Registrar objetivo, pronóstico y referencia en unidades comparables. Mantener el historial y los puntos de control juntos.

**Contrato y aceptación.** Con configuración y prefijo admisible iguales, el pronóstico determinista para el mismo origen y horizonte debe permanecer igual al cambiar el sufijo. El ensayo de aceptación debe poder cambiar una revisión retrospectiva conservando la decisión original. Comparar con un oráculo independiente y una referencia simple sobre los mismos orígenes. Acreditar recepción real y repetición del flujo con el consumidor antes de declararlo operativo. La comparación de desempeño predictivo exige una muestra y un criterio propios.

**Decisión.** Empezar con archivo y script para el perfil de un escritor. Reabrir SQLite si la aceptación exige confirmación atómica de varias entidades y recuperación verificable, o si se identifica una necesidad de consulta indexada que cambie el coste operativo. Probar fallos de escritura y concurrencia cuando el uso los requiera.

[KS-004](KS-004_CONSTRUCCION_TECNOLOGICA.md) · [KS-007](KS-007_CADENA_TEMPORAL_Y_VALOR_DEL_LABORATORIO.md) · [Temporal R01](https://github.com/ksgfin8-cyber/engineering-knowledge/blob/14a814b8de4d062b89581ec23a142e1ba89c66a5/docs/research/ESPECIALIZACION_TEMPORAL_R01.md)

## 2. Ingeniería de datos, observación y reconciliación

**Usuario y problema.** Un consumidor interno que debe explicar una decisión ante datos revisados o un receptor que necesita conciliar dos extractos. FASES1234 y Filtrado permiten auditar el preparado y muestran lo que pierde un pipeline sin bruto recuperable. BOX1 y LAB2 muestran límites distintos en serialización, admisión y reconstrucción de estado.

**Capacidad y transferencia.** KS-008 reconstruyó cinco cortes de cuatro publicaciones oficiales y obtuvo paridad Python/SQL en logística sintética. KS-009 conservó las vistas retrospectiva e histórica en un mismo registro local y verificó el reintento tras interrupción de un proceso antes y después de confirmar. Temporal R01 respalda un camino inicial de menor alcance para el consumidor de pronósticos. El observatorio puede empezar registrando decisiones de ese consumidor. La interfaz visual se justifica si hay una pregunta recurrente que el informe de ejecución no cubre.

**Aceptación para el observatorio.** Bruto recuperable, recepción observada, regla ejecutable identificada, admisión trazable y reconstrucción completa de una decisión. Registrar por separado disponibilidad, admisión y confirmación. El fallo parcial y el reintento se prueban a nivel del soporte que vaya a operarse.

**Aceptación para reconciliación externa.** Dos extractos autorizados, periodo y reglas acordados. Entregar pares, excepciones y comprobación reproducible. Repetir con una corrección y un cambio de tolerancia. Comparar discrepancias, tiempo activo y trabajo del receptor frente a su procedimiento habitual. La prueba de campo queda condicionada a un receptor.

[KS-006](KS-006_DIMENSIONES_Y_RECUPERACION.md) · [KS-008](KS-008_SIGUIENTE_GENERACION_Y_TRANSFERENCIA.md) · [KS-009](KS-009_REGISTRO_TEMPORAL_Y_EVIDENCIA_DE_DISENO.md) · [Observatorio](disenos/siguiente-generacion/OBSERVATORIO_DE_DECISIONES.md) · [Reconciliación](disenos/siguiente-generacion/PILOTO_DE_RECONCILIACION.md)

## 3. Modelado, algoritmos y validación de señales

**Usuario y problema.** Un diseñador que debe escoger un mecanismo antes de acometer su implementación completa. F001 proporciona el patrón de dominio, partición y descenso. TN aporta control de unidades y fronteras de información. AURORA y Quantum Viper aportan obligaciones específicas de coherencia de estados, abstención, memoria y vigencia.

**Resultado Banco R01.** Se transfirió desde LAB2 el patrón de observar estado y decisión después de descartar una entrega, sin reusar su implementación. Las dos alternativas aprobaban la secuencia limpia A → B. En A → A, deduplicar antes de mutar mantuvo memoria 1 y abstención. Mutar al recibir dejó memoria 2 y activó la acción pese al descarte. El criterio discriminativo acertó en el paso, el valor y la decisión del control negativo.

**Construcción candidata.** Ejercer el banco en una decisión prospectiva con una propiedad y un oráculo independientes del candidato. Para una recurrencia sobre dominio finito, los subproblemas deben quedar dentro del dominio y reducir una medida de progreso. Para una señal con memoria, declarar estado, entradas admisibles, condiciones de abstención y expiración. Formular la relación matemática únicamente donde resuelva un requisito verificable.

**Aceptación y decisión.** Un caso válido y un control defectuoso deben producir el contraste previsto. Registrar qué opción se conserva, qué parte del instrumento se transfirió y qué esfuerzo añadió. Adoptar la mutación al admitir para el contrato de Banco R01. Ejercer el protocolo en nuevos diseños según su propia propiedad. La mejora de productividad y la eficacia de una señal en mercado siguen abiertas.

[KS-002](KS-002_CATALOGO_CONOCIMIENTO.md) · [Banco R01](https://github.com/ksgfin8-cyber/engineering-knowledge/blob/9e5e8bf1b97312ec9e815f7b368cd66fa1da50e0/docs/research/ESPECIALIZACION_BANCO_R01.md) · [Plano del banco](disenos/siguiente-generacion/BANCO_DE_EVIDENCIA.md)

## 4. Simulación financiera de ejecución y rendimiento

**Usuario y problema.** Un investigador que necesita explicar patrimonio y exposición tras órdenes y ejecuciones. En Indicadores, a precio constante el registro dio −0,20 % y la curva −0,3996 %. El caso fija una obligación de reconciliación. Los contratos de admisión, estado y continuidad de LAB2 son precedentes para la trayectoria de un simulador.

**Construcción candidata y aceptación.** Si existe un consumidor de rendimiento, empezar por un motor mínimo con eventos de señal, orden, ejecución y cargo diferenciados. Bajo un modelo simple sin otros activos ni pasivos, el patrimonio marcado debe coincidir con efectivo más posición por precio de valoración. Usar un oráculo manual por transición a precio constante y con cambio de precio. Reconciliar inventario, movimientos de efectivo, costes y curva. Probar información elegible, sesiones, disponibilidad, supuestos de ejecución y reglas de cargo antes de interpretar cualquier métrica de estrategia.

**Decisión.** Conservar el oráculo y los casos históricos. Abrir la construcción cuando una pregunta concreta de simulación avance más allá de la evaluación de pronósticos o señales. Los casos disponibles delimitan el contrato inicial y el criterio de parada ante diferencias.

[Indicadores-R01](https://github.com/ksgfin8-cyber/Indicadores/blob/6e2f0239d59aba2a05a9a82a9479fed141b552f1/docs/research/INDICADORES_RDL_PB_001_EVALUATION.md)

## 5. Simulación dinámica y laboratorios de agentes

**Usuario y problema.** Un investigador de fenómenos con trayectoria que debe interrumpir y continuar una corrida preservando decisiones y contexto. WORLD-LAB aporta ejecución, replay y registro operativo acotado. En el caso FrontierMemory, restaurar o reconstruir memoria conservó el resultado completo.

**Resultado Continuidad R01.** Con RandomAgent y un corte posconfirmación en tick 8, instantánea e historial produjeron cada uno 16 decisiones nuevas y el resultado completo de la corrida continua. Reiniciar solo el agente divergió en el tick 9 aunque el RNG del mundo y el motivo terminal coincidieran. El replay con acciones guardadas reprodujo la trayectoria física con cero decisiones nuevas y perdió el contexto completo del recorder. El expediente conserva la corrección posterior del analizador y documenta cero reintentos experimentales. Son dos formas de memoria y dos ensayos del mismo motor mediante arnés.

**Especificación candidata.** Separar estado privado versionado del agente, mundo y su RNG, coordinación del punto de corte, último resultado de acción y contexto del registro. Definir exportación e importación con identidad, compatibilidad y rechazo explícito de estados inválidos. Tratar la reconstrucción como opción condicionada al estado inicial y al historial necesario de llamadas y entradas. Definir una representación portable del recorder.

**Aceptación y decisión.** Hay base para especificar la interfaz. Para adoptarla, comprobar conformidad de dos adaptadores a la misma interfaz, rechazo de una versión incompatible, consistencia del punto de corte e igualdad de sufijo regenerado. Usar una sonda simple cuando la propiedad sea local y una trayectoria completa cuando intervenga la memoria acumulada. Una interfaz pública, persistencia durante caída y compatibilidad entre motores siguen pendientes.

[FrontierMemory](https://github.com/ksgfin8-cyber/yellow/blob/c807730ada1cc1ec830c2ead8c5836a469349471/docs/research/world-lab-resume-viability/REPORT.md) · [Continuidad R01](https://github.com/ksgfin8-cyber/yellow/blob/38f2dbe1408cebe81792ca5dbf8cc78926e9c59d/docs/research/WORLD_LAB_CONTINUIDAD_SEGUNDO_AGENTE_R01.md) · [Laboratorio componible](disenos/siguiente-generacion/LABORATORIO_COMPONIBLE.md)

## 6. Sistemas web y flujos de atención

**Usuario y problema.** Un comercio que necesita recibir un pedido completo y atenderlo bajo sus reglas de despacho. Almuerzos Ecuador y EscanningQR sustentan preparación local, traducción de reglas y extensión del modo de uso. Una apertura de canal y una etiqueta interna de enviado no establecen recepción.

**Construcción y aceptación condicionadas.** Con un comercio participante, contrastar el mismo catálogo, horario y regla de despacho con su flujo habitual. Verificar acuse, contenido, pedidos fallidos, trabajo del personal y comportamiento bajo un pico representativo. Registrar también esfuerzo y errores de un cambio ordinario de configuración. La elección de arquitectura depende de la autoridad necesaria para reglas, confirmación e información compartida.

[KS-001](KS-001_EVALUACION_CARTERA.md) · [KS-007](KS-007_CADENA_TEMPORAL_Y_VALOR_DEL_LABORATORIO.md)

## 7. Ciberseguridad defensiva

**Situación.** CYBERsec preserva experiencia exploratoria, límites metodológicos y fallos observados. La cartera carece de evidencia suficiente para declarar una especialidad defensiva estable.

**Condición de entrada.** Elegir un sistema de la organización, un responsable y una propiedad defensiva que afecte su uso. Un caso candidato es comprobar que una operación que exige autorización solo produce efecto tras una decisión autorizada y que un rechazo deja evidencia auditable. La revisión de arquitectura fija la autoridad. La verificación comprueba el comportamiento declarado y el registro. Escalar a un laboratorio cuando estas preguntas sean recurrentes y requieran aislamiento u observación sistemática.

[Evaluación del prototipo histórico](https://github.com/ksgfin8-cyber/CYBERsec/blob/944297f/docs/research/CYBERSEC_RDL_PB_001_EVALUATION.md)

## 8. Secuencia de inversión y revisión

| Orden propuesto | Trabajo y primer resultado útil | Cuándo ampliar o detener |
| --- | --- | --- |
| 1 | Elegir un consumidor interno de pronósticos, conectar una fuente recurrente al archivo y script y entregar una evaluación por origen reconstruible. | Ampliar a un registro transaccional cuando aparezca un requisito verificable que el archivo no cubra con coste defendible. Si la fuente carece de recepción identificable, limitar el resultado a replay o cambiar de fuente. |
| En paralelo | Aplicar el banco a una decisión nueva de modelado y conservar la alternativa y el contraejemplo. | Ampliar fichas cuando cambien decisiones reales. Si la prueba es indistinguible, revisar su sensibilidad antes de añadir instrumentación. |
| Siguiente especificación | Precisar el contrato del checkpoint y del recorder sobre un consumidor de trayectorias. | Implementar cuando una necesidad de continuidad justifique el coste. Diferir persistencia distribuida hasta contar con requisitos propios. |
| Condicionado a demanda | Abrir simulación de ejecución, web o reconciliación con su consumidor y referencia. Delimitar una propiedad defensiva con un sistema concreto. | Admitir cada trabajo cuando el resultado pueda cambiar una decisión de usuario, operación o inversión. Cerrar como condicionado si la entrada externa falta. |

| Disciplina | Objeción que puede cambiar la decisión | Evidencia que resuelve |
| --- | --- | --- |
| Semántica temporal y estadística | La información del origen no estaba disponible o los candidatos no comparten horizonte e insumos. | Bitácora de recepción, oráculo de elegibilidad y puntuación emparejada. |
| Verificación y modelado | El control defectuoso pasa o una propiedad depende de un supuesto omitido. | Contraejemplo discriminativo, argumento de dominio y trazas intermedias. |
| Sistemas y software | Reiniciar una parte mantiene el resumen final aunque cambie la conducta. | Primera divergencia de decisiones, estado privado y registro tras restauración. |
| Operaciones y economía | La solución consume más trabajo que el flujo que reemplaza. | Medición del mismo trabajo con un receptor y referencia acordados. |

## 9. Verificación de este cierre

Los expedientes temporal y de banco, incorporados a engineering-knowledge, se reprodujeron con Python 3.12.14. Las dos salidas coincidieron byte por byte con sus JSONL publicados. Para WORLD-LAB se revisaron el protocolo, el expediente, la verificación publicada y el diff frente al motor congelado. No se repitió la campaña de episodios. El cierre preserva los límites de productividad, escala, generalización empírica y valor externo de cada prueba.

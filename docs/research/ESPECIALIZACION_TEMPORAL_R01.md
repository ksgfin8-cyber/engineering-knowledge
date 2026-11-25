# Especialización temporal R01

## Protocolo previo · RDL-PB-001 v0.1

**Pregunta y decisión previa.** ¿Un archivo de entregas versionado y un script bastan para reconstruir un pronóstico y revisar retrospectivamente su insumo? Empezar con archivo para un consumidor y un escritor si cumple el oráculo con una operación sencilla. Compararlo con el registro SQLite intacto.

**Revisiones.** Base `736bbd01e7cd211ca4ac9b46d45ddbde20194484`. Se reutiliza directamente `instrumentos/registro-versionado/registro.py` de esa base. Se reutilizan como método, sin ejecutar sus candidatos, la perturbación causal de KS-004 (`instrumentos/tn-causal/probar.mjs`), el corte y la persistencia del último valor de KS-007 (`instrumentos/evaluacion-temporal/ejecutar.py`), y las dos vistas de KS-009. Los documentos y el plano `disenos/siguiente-generacion/OBSERVATORIO_DE_DECISIONES.md` están fijados en la misma base. [Playbook v0.1](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08fbb36c5bbe075628a5b9a9078ce9c017c/docs/program/RDL-PB-001_v0.1_original_propuesta.md)

**Consumidor.** Pronostica en puntos el valor de la serie a un día calendario, al mediodía UTC. Origen histórico H: 2 de enero a las 12:00 UTC, objetivo 3 de enero a las 12:00. Intervención P: origen 4 de enero a las 12:00, objetivo 5 de enero a las 12:00. Todos los tiempos son de enero de 2026. Regla de persistencia P1: repetir el último valor observado elegible. Referencia fija predeclarada: pronosticar 10 puntos siempre. La retrospectiva recalcula P1 con el corte de información del 3 de enero a las 12:00 para el mismo objetivo de H, sin llamarlo pronóstico prospectivo. Una única observación ocurrió el 2 a las 09:00. Elegibilidad inclusiva por admisión, con mayor revisión elegible. En este ensayo admisión coincide con recepción. Cada decisión conserva regla, corte, frontera, insumo y resultado.

**Entregas controladas.** El productor local proporciona sobres brutos y un reloj declarado. Las marcas de publicación y recepción son simuladas. El proceso lee los bytes localmente. La recepción recurrente desde una fuente externa queda abierta. D3 retransmite la misma observación revisada con nuevo identificador de entrega y hora de recepción. D4 altera el valor mucho después del origen P.

| Entrega | Revisión | Puntos | Dato UTC | Publicación UTC | Recepción UTC |
| --- | ---: | ---: | --- | --- | --- |
| D1 | 1 | 10 | 02 09:00 | 02 09:10 | 02 09:11 |
| D2 | 2 | 14 | 02 09:00 | 02 11:50 | 02 12:10 |
| D3 | 2 | 14 | 02 09:00 | 02 11:50 | 03 13:00 |
| D4 | 3 | 99 | 02 09:00 | 04 12:05 | 04 12:06 |

**Oráculo manual previo.** D2 ya fue publicada en H, pero su recepción ocurre diez minutos después. D3 no crea versión. D4 llega seis minutos después de P. De ahí se obtiene la siguiente tabla independientemente de los ejecutores.

| Caso | Consulta | Revisión y entrega admisibles | P1 | Referencia |
| --- | --- | --- | ---: | ---: |
| Revisión | H reconstruida tras D2 | 1, D1 | 10 | 10 |
| Revisión | Retrospectiva del 03 12:00 | 2, D2 | 14 | 10 |
| Retransmisión | Retrospectiva repetida tras D3 | 2, D2 | 14 | 10 |
| Perturbación | P antes de D4 y tras D4 | 2, D2 | 14 | 10 |
| Perturbación | Consulta del 04 12:06 | 3, D4 | 99 | 10 |

**Comparación y cierre.** Los dos motores reciben los mismos bytes en el mismo orden. El archivo crece por anexado y cada decisión fija la longitud del prefijo de entregas. Se reabre cada almacén para reconstruir la decisión y verificar su insumo y resultado. El comparador negativo usa la revisión mayor del archivo ignorando el corte y debe dar 14 para H tras D2. Aceptar si ambos motores coinciden en todas las filas y el negativo falla en H; conservar toda discrepancia. Medir por separado acciones del operador y operaciones lógicas de persistencia/lectura, sin usar la latencia de una sola corrida como coste recurrente. Cerrar tras un consumidor, una fuente y esos tres casos. Alcance local, sin evaluar ventaja predictiva ni escala.

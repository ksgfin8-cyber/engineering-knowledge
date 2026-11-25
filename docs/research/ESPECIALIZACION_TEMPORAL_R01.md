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

## Resultado y decisión

**Deducido antes de la corrida.** El conocimiento cambia entre H y la retrospectiva. La publicación anticipada de D2 no la hace elegible en H. La perturbación D4 debe ser visible a partir de su admisión para que la prueba de invariancia en P sea sensible.

**Observado.** Python 3.12.14 y SQLite 3.53.1 leyeron la secuencia local versionada. Ambos almacenes devolvieron `admitted, admitted, duplicate, admitted`. El archivo conservó los bytes por anexado y SQLite por entrega. Se reabrieron los almacenes para reconstruir H y P. El comparador sin corte obtuvo D2 y 14 en H, una divergencia de +4 puntos respecto al oráculo. [Salida inicial](temporal-r01/resultado.jsonl) · [Sobres brutos](temporal-r01/entregas.jsonl)

**Verificado.** Las nueve comprobaciones de resultado de cada motor coincidieron con el oráculo, incluidos identidad del insumo y pronóstico. H conservó D1 y 10, mientras que la retrospectiva incorporó D2 y 14. P conservó D2 y 14 incluso al recalcular su corte con D4 ya cargada. A las 12:06 del día 4 se recuperó D4 y 99. Se comprobó igualdad de bytes de las cuatro entregas en ambos almacenes. El control negativo falló como estaba previsto. El protocolo y los diseños se mantuvieron tras observar la salida.

### Trabajo por operación

El arnés recorrió ambos almacenes en una invocación, sin ediciones manuales de datos, reglas o esquema. Por operación se contó una llamada explícita del arnés por alternativa y cero intervenciones adicionales. Los recuentos de persistencia describen las rutas ejecutadas y excluyen la apertura del almacén, sus comprobaciones de arranque y la configuración inicial.

| Operación | Archivo versionado | SQLite KS-009 |
| --- | --- | --- |
| Incorporar D2 | Una lectura del historial para clasificar y un anexado de los bytes. Se añade una línea. | Dos consultas de identidad y tres escrituras (entrega, versión, vínculo) en una transacción. |
| Reconstruir H | Dos lecturas (punto de control y prefijo del historial), una comprobación SHA-256 y un recorrido del prefijo para recalcular. | Tres consultas (decisión, selección por corte y frontera, referencias de insumos), cotejo de referencias y recálculo. |
| Cambios para D2 | Cero cambios de código o formato. | Cero cambios de código o esquema. |
| Dependencias operativas | Python, sistema de archivos, un escritor, conservar historial y puntos de control juntos. La fixture se versiona en Git. Si se usa Git para respaldar lotes de operación, hay que incluir también los puntos de control. Ese paso no se cronometró. | Python con SQLite, archivo de base, transacciones y respaldo consistente. El núcleo encapsula admisión y trazabilidad. |

**Arquitectura inicial.** Usar archivo append-only y script para este primer consumidor con escritor único. Ambos mecanismos cubren el trabajo comprobado. El archivo requiere menos escrituras lógicas para D2 y menos piezas de persistencia. El coste total y la latencia recurrente quedan sin medir. Adoptar KS-009 cuando sea requisito confirmar atómicamente entregas, versiones y referencias de decisión con recuperación verificable ante interrupciones, o cuando la auditoría inversa de muchas decisiones requiera consultas indexadas. Esas necesidades exceden el caso probado.

**Pendientes.** Observar recepción real de una fuente identificada, medir trabajo de captura, verificación, respaldo, recuperación y mantenimiento con lotes recurrentes, y repetir el contraste si aparecen escritores concurrentes. Ventaja predictiva y escala requieren ensayos propios. El archivo de referencia presupone sobres válidos y escritura secuencial, y el ensayo no probó fallos de escritura, correcciones conflictivas ni tiempos de servicio.

### Reproducción desde la raíz

```sh
set -eu
salida=$(mktemp)
trap 'rm -f -- "$salida"' EXIT
python3 -B docs/research/temporal-r01/probar.py > "$salida"
cmp docs/research/temporal-r01/resultado.jsonl "$salida"
```

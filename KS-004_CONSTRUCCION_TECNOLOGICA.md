# KS-004 · Construcción observada y escalamiento del evaluador TN

**Corte:** 24 de noviembre de 2026. **Etapa:** estudio del proceso de construcción tecnológica. **Objeto:** evaluador experimental por origen sobre [TN 4217f70](https://github.com/ksgfin8-cyber/tn-ea/tree/4217f70e2a140d03746873183dad5328a65e1fba). **Procedencia:** [KS-002](KS-002_CATALOGO_CONOCIMIENTO.md), controles KC-02 a KC-04, y [KS-003](KS-003_PLAN_INFRAESTRUCTURA.md). **Marco:** [RDL-PB-001 v0.1](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/program/RDL-PB-001_v0.1_original_propuesta.md), §§6–12, 17 y 19–23.

## Dictamen

**Descartar el descriptor de ventana completa para puntuar orígenes internos.** En la prueba previa a la implementación, una perturbación futura cambió los pronósticos de las doce posiciones comunes examinadas en T1, con el mismo origen, historial permitido y objetivo en la primera discrepancia. Se construyó un evaluador con una ventana por origen y se compartió Γ entre teorías del mismo origen. En la carga mayor, produjo exactamente las mismas 8.024 filas que la referencia causal con 1.003 llamadas a Γ frente a 8.024.

La fase 3 deja un precedente prospectivo de selección de diseño. La medición institucional de retrabajo, la operación a escala del ejecutor común de KS-003 y la evaluación global de TN tienen alcances pendientes propios.

## 1. Reconstrucción con evidencia disponible

| Caso | Mecanismo documentado | Consecuencia para el proceso |
| --- | --- | --- |
| **TN** | La puntuación histórica recorta el vector de precios del predictor por origen. Las estadísticas de la ventana envolvente se reutilizan dentro de la evaluación 70/30. La réplica encontró divergencias al recalcular por origen. | Hacer explícito qué información puede recibir cada argumento. Comparar orígenes y objetivos idénticos antes de integrar un cambio en el selector. La motivación original de compartir esos descriptores permanece sin verificar. [Réplica TN-R01](https://github.com/ksgfin8-cyber/tn-ea/blob/ee49ac7/docs/research/TN_R01_REPLICATION.md) |
| **F001** | La partición pierde el dominio incluso en dos elementos. La excepción ocurre después de modificar el arreglo. | Verificar dominio, división y descenso en la recurrencia antes de ampliar la implementación. Medir secuencia de desarrollo y retrabajo exigiría registros contemporáneos. [F001-R01](https://github.com/ksgfin8-cyber/f001/blob/2b60f32/docs/research/F001_RDL_PB_001_EVALUATION.md) |
| **LAB2** | La persistencia puede descartar una consulta después de que el modelo ya cambió la memoria. | Examinar el orden de admisión, transición y registro en la frontera entre componentes. Recuperar los casos como controles de diseño. [LAB2-R01](https://github.com/ksgfin8-cyber/LAB2/blob/0c21d18/docs/research/LAB2_RDL_PB_001_EVALUATION.md) |

Los expedientes permiten identificar causas técnicas en revisiones concretas. La atribución de burocracia o de demoras a procedimientos históricos queda **NO EVALUADA** con los registros disponibles.

## 2. Construcción prospectiva

Se fijó antes de ejecutar el bloque de protocolo que sigue, SHA-256 `54eb88e1088c837a2073be6f3d031b84bf30c61ba54ff66724db471e75d293c3`.

## Protocolo previo · TN, evaluador por origen v0.1

Pregunta. ¿Podemos conservar el descriptor calculado una vez para toda la ventana o debe calcularse por origen? Tras fijar el corte, ¿se puede compartir Γ entre teorías del mismo origen sin cambiar resultados?

Candidato. Motor TN en 4217f70e2a140d03746873183dad5328a65e1fba. El piloto construirá un evaluador aislado, sin modificar TN ni sustituir sus predictores. Comparará un descriptor de ventana completa con un descriptor de origen, sobre la misma subventana y el mismo objetivo. El contrato del evaluador usa los últimos 21 precios hasta t y separa el pronóstico de nivel en t del precio objetivo en t+1. Un descriptor para toda la ventana es un control deliberadamente no causal, no una réplica integral de GEI.

Criterios previos.
1. Variar solo precios posteriores a un prefijo de 32 valores. Entre los orígenes comunes 20–31, los pronósticos causales deben coincidir exactamente. Los objetivos y errores deben coincidir en 20–30. En 31 solo se exige igualdad del pronóstico. Random Walk sin ruido es el control positivo y debe devolver el último precio. El descriptor de toda la ventana debe producir al menos una divergencia en T1.
2. Comparar dos realizaciones causales: descriptor calculado por teoría y descriptor calculado una vez por origen. Exigir igualdad exacta de todas las parejas origen–teoría, pronósticos, objetivos y errores. Si coincide, preferir compartir el cálculo en el piloto. El descriptor se comparte solo en el mismo contexto de entradas, configuración y origen.
3. Medir llamadas a Γ y tiempo de pared en series de 64, 256 y 1.024 precios para 2, 4 y 8 teorías. El recuento esperado es orígenes × teorías para la referencia y orígenes para la implementación compartida. Comparar dos ejecuciones de los resultados sin tiempos.
4. Delimitar el piloto a series sintéticas positivas, horizonte uno y estado construido a partir de precios. La utilización posterior de un descriptor variable, con efecto lateral o dependiente de la teoría requiere otro contrato. El desempeño de GEI, la mezcla de unidades de T1, la utilidad en mercado y el ahorro de retrabajo del programa quedan fuera.

### Decisión antes de construir

El contraste en modo `decision` se completó antes de escribir el evaluador. El primer origen divergente fue 20. El objetivo permaneció en 105,52 y el pronóstico pasó de −67,461133 a −11,604514 al modificar exclusivamente valores posteriores al prefijo común. El resultado se limita al control construido con descriptor de ventana completa. Su registro tiene SHA-256 `144b077b64c4103632a6146dff1cdf76b57de8b095451cea90f5b6c2c3ed0a07`.

A partir del resultado se fijó la frontera del [evaluador](instrumentos/tn-causal/evaluar.mjs). El descriptor y los predictores reciben únicamente los 21 precios terminados en t. El precio en t+1 solo entra como objetivo de medición. Cada fila conserva origen, índice del objetivo, teoría, pronóstico, objetivo y error. Se reutiliza Γ entre teorías de ese mismo origen. El módulo rechaza entradas fuera del dominio previsto y salidas no finitas. Su contrato presupone que los predictores no mutan el descriptor ni la ventana durante la evaluación.

### Verificación

- **Corte externo del evaluador.** Los 48 pronósticos de cuatro teorías sobre 12 orígenes comunes fueron idénticos después de perturbar el futuro. Coincidieron 44 filas completas hasta el origen 30. En el origen 31 se alteró el objetivo posterior y se comprobó solo la invariancia del pronóstico.
- **Control y límites.** Random Walk devolvió el último precio en los orígenes comprobados. La sonda detectó cuatro casos inválidos, incluidos un pronóstico infinito y una entrada no finita.
- **Reutilización local de Γ.** La referencia recomputó Γ por teoría. El evaluador calculó Γ una sola vez por origen. Coincidieron exactamente todas las filas en las tres cargas. El contraste comparte las primitivas del motor y usa bucles separados para comprobar la transformación del procedimiento.
- **Repetibilidad.** Dos corridas finales produjeron JSON idéntico, SHA-256 `da9b266aedb8cdcd6097449ada4172354eb246fb0adfb8a1fd63940270928c86`. Se preservó ese resultado al reemplazar dos conteos informativos fijos por conteos de las filas verificadas.

| Precios | Teorías | Filas idénticas | Γ por teoría | Γ por origen |
| ---: | ---: | ---: | ---: | ---: |
| 64 | 2 | 86 | 86 | 43 |
| 256 | 4 | 940 | 940 | 235 |
| 1.024 | 8 | 8.024 | 8.024 | 1.003 |

La reducción exacta de llamadas se refiere a la comparación con una referencia que **ya es causal**. Compartir Γ no reduce el número de pronósticos ni el volumen de filas. Para la carga mayor, la referencia tomó aproximadamente 103–104 ms y el evaluador 29–48 ms en las dos corridas finales. El orden de ejecución fue fijo y los tamaños y el número de teorías variaron conjuntamente. Los tiempos tienen alcance descriptivo y no estiman un factor general de aceleración.

## 3. Implicaciones y límites por disciplina

| Perspectiva | Decisión informada | Evidencia pendiente |
| --- | --- | --- |
| **Matemática y experimentación** | El horizonte y la ventana tienen cortes distintos. La perturbación establece una dependencia de información futura en el control envolvente. | La incoherencia dimensional de T1 sigue abierta. El desempeño frente a referencias en una muestra reservada no pertenece al piloto. |
| **Ingeniería** | Compartir un descriptor por origen dentro del mismo contexto conserva los resultados registrados de esas teorías. La salida permite relacionar pronóstico, objetivo y error. | El uso con datos faltantes, versiones distintas de Γ, predictores mutables o procesamiento reanudable necesita su propio contrato. La integración con GEI permanece abierta. |
| **Escalamiento** | Se conoce la reducción del recuento de Γ y el crecimiento de filas con orígenes y teorías. El evaluador acumula las filas en memoria. | Cargas representativas, memoria, fallos, recuperación y mantenimiento recurrente. Una eventual emisión incremental se justifica cuando el volumen la exija. |
| **Economía y proceso** | La prueba de diseño tomó aproximadamente 30 s de reloj desde la fijación local del protocolo hasta la primera corrida. Entre esa decisión y la primera doble corrida del evaluador transcurrieron aproximadamente 14 s. | Los intervalos incluyen escritura y ejecución asistidas. El retrabajo evitado y la productividad requieren una línea base o ciclos comparables. |

**Lección operacional comprobada en este caso.** Un contraste ejecutado antes de construir permitió abandonar una opción incompatible con el requisito y definir la frontera de información de la implementación. El paquete final contiene el evaluador y su sonda. El motor de TN conserva su revisión de origen.

**Siguiente uso propuesto.** Aplicar el mismo tipo de decisión previa en otro objeto con una pregunta real y registrar esfuerzo activo, iteraciones y cambios de decisión. Evaluar el escalamiento de la fase 2 por separado si aparece una carga representativa o un nuevo receptor que justifique medir lotes, errores y operación recurrente.

## Reproducción

Node 24.22.3. Los nueve archivos del motor utilizados coinciden con los blobs de `4217f70e2a140d03746873183dad5328a65e1fba`. La sonda reutiliza el cargador de KS-003 para los imports TypeScript del candidato. Con un checkout de `engineering-knowledge` y otro de `tn-ea` como directorios hermanos:

```sh
set -eu
tmp=$(mktemp -d)
git -C ../tn-ea archive 4217f70e2a140d03746873183dad5328a65e1fba src/engine | tar -x -C "$tmp"
node --disable-warning=ExperimentalWarning instrumentos/tn-causal/probar.mjs "$tmp/src/engine" decision > "$tmp/decision.json"
for run in 1 2; do
  node --disable-warning=ExperimentalWarning instrumentos/tn-causal/probar.mjs "$tmp/src/engine" > "$tmp/run-$run.json" 2> "$tmp/time-$run.jsonl"
done
cmp "$tmp/run-1.json" "$tmp/run-2.json"
sha256sum "$tmp/decision.json" "$tmp/run-1.json"
```

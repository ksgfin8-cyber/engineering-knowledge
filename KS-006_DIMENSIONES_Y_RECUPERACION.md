# KS-006 · Fronteras de información, decisiones de diseño y recuperación de estado

**Corte** · 24 de noviembre de 2026, Ecuador  
**Alcance** · Profundización transversal de las cuatro fases y piloto local.  
**Procedencia** · [Cartera](KS-001_EVALUACION_CARTERA.md) · [Catálogo](KS-002_CATALOGO_CONOCIMIENTO.md) · [Infraestructura](KS-003_PLAN_INFRAESTRUCTURA.md) · [Construcción](KS-004_CONSTRUCCION_TECNOLOGICA.md) · [Posicionamiento](KS-005_POSICIONAMIENTO_Y_DECISIONES.md)

## Dictamen

El cruce de la cartera revela tres obligaciones separadas en los sistemas que transforman observaciones en decisiones: establecer **cuándo la información está disponible**, determinar **qué entradas pueden cambiar el estado** y definir **qué evidencia confirma una transición o un efecto externo**. Las tres pueden requerir instrumentos diferentes. Una puntuación temporalmente válida puede coexistir con una trayectoria irrecuperable. Una trayectoria fiel puede reproducir un cálculo internamente inválido.

El piloto verificó que **un adaptador real de LAB2, con la admisión y el registro del arnés, pudo recuperar las seis observaciones y el estado expuesto de TN después de una interrupción de proceso**. Replay e instantánea pasaron los dos cortes ensayados. La decisión recomendada es conservar el replay como referencia experimental inicial y evaluar la instantánea cuando el coste de recomputación observado lo justifique. La integración en un servicio con almacenamiento duradero y la operación a escala requieren evidencia de otro alcance.

## 1. Objeto, entornos y procedencia

**Tortuga Ninja cuenta como un solo objeto tecnológico.** La revisión `tn-ea@4217f70` permite estudiar modelo, especificación e implementación. `Computational-Lab@55b43dd` aporta experimentos, protocolos y contexto de laboratorio. Los nueve módulos de `src/engine` y la especificación matemática raíz son idénticos byte por byte entre ambas revisiones. `LAB2@0c21d18` comparte ocho de esos módulos y la especificación raíz, con un `types.ts` distinto y un adaptador observador propio. La comprobación de identidad se hizo por blob Git. Los resultados se atribuyen al núcleo, al protocolo o al adaptador según el punto donde se establece la propiedad. Una réplica que comparte núcleo puede aportar independencia de ejecución o de método de contraste en la medida documentada por el expediente. [TN](https://github.com/ksgfin8-cyber/tn-ea/tree/4217f70) · [Computational-Lab](https://github.com/ksgfin8-cyber/Computational-Lab/tree/55b43dd) · [LAB2](https://github.com/ksgfin8-cyber/LAB2/tree/0c21d18)

Se usan cuatro dimensiones de análisis según la pregunta. Para cada conclusión se conserva el hecho observado o deducido, su alcance y la decisión que podría cambiar. La transferencia se acredita en el receptor ejercitado. [RDL-PB-001 v0.1, §§6–12, 17, 19 y 23](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/program/RDL-PB-001_v0.1_original_propuesta.md) · [Especificación Estratégica, §§9, 21–26, 29–30 y 43–48](https://chatgpt.com/library?file_id=libfile_e0932365a6ac8191a15982b0355879e0&account_id=personal)

## 2. Flujo de información y autoridad

| Frontera | Condición que habilita el paso | Evidencia histórica | Control aprovechable |
| --- | --- | --- | --- |
| **Disponibilidad → pronóstico o puntuación** | Cada cálculo recibe información disponible en su propio origen. El objetivo posterior entra al medir el error. | El corte externo de TN pasó en la proyección de la réplica mientras el descriptor de la ventana envolvente contaminaba cortes internos. En Computational-Lab, el Exp. 20 desplazó el objetivo 48 barras y el Exp. 21 utilizó la cola global. Estas son obligaciones en usos distintos del mismo núcleo. | Perturbar solo el futuro y comprobar por separado entradas de cada cálculo, pronóstico y objetivo. Una proyección externa invariante puede coexistir con un evaluador interno inválido. |
| **Observación → admisión → mutación** | La entrada tiene identidad y orden definidos y satisface la política de cierre. La admisión precede a la llamada con memoria. | LAB2 tomó la apertura de la vela como marca, perdió el cierre programado al convertir la entrada y computó antes de que la persistencia descartara el duplicado. El contador y la teoría podían cambiar sin fila propia. | Duplicado y provisional con valores distintos, seguidos de una entrada válida. Observar la memoria además de las filas. |
| **Transición → registro → recuperación** | La evidencia persistida permite fundamentar qué ocurrió y continuar desde el mismo estado. | El reinicio histórico de LAB2 recuperó el contador del observador y perdió la memoria de TN. En una fixture coincidieron las filas pese a divergir la memoria. La réplica TN también documentó que una colección de una fila cambió al releerla por referencias compartidas. | Comparar instantáneas por valor, trayectoria y estado posterior a la reanudación. Probar tanto antes como después de confirmar el registro. |
| **Intento → efecto externo confirmado** | El receptor o una comprobación independiente acredita el efecto. | Almuerzos registró `ENVIADO` después de que la apertura simulada devolviera `null`. Eso aporta evidencia sobre la transición local. La entrega real sigue abierta. | Separar preparación, intento y acuse. Un replay del estado local, aunque sea fiel, deja pendiente el acuse externo. |

**Conexión que cambia el diseño.** Una observación tiene más de una frontera temporal y de autoridad. Para este tipo de sistema, conviene registrar qué entrada exacta se aceptó, contra qué versión y orden se calculó, qué salida produjo y cómo se vincula con el estado confirmado. Si además se afirma un efecto externo, su evidencia debe provenir de esa frontera. Una marca única de tiempo o un indicador único de éxito puede resultar insuficiente. [TN-R01](https://github.com/ksgfin8-cyber/tn-ea/blob/ee49ac7/docs/research/TN_R01_REPLICATION.md) · [Computational-Lab-R01](https://github.com/ksgfin8-cyber/Computational-Lab/blob/55b43dd/docs/research/COMPUTATIONAL_LAB_RDL_PB_001_EVALUATION.md) · [LAB2-R01](https://github.com/ksgfin8-cyber/LAB2/blob/0c21d18/docs/research/LAB2_RDL_PB_001_EVALUATION.md) · [Almuerzos R01](https://github.com/ksgfin8-cyber/almuerzos-ecuador/blob/af7cf32/docs/research/almuerzos-ecuador-rdl-pb-001.md)

## 3. Evolución del diseño

| Caso | Decisión bajo estudio | Momento viable de intervención | Calidad de la reconstrucción |
| --- | --- | --- | --- |
| **F001** | Límites y descenso de la partición después de rotar segmentos. | En la recurrencia escrita, sustituir una entrada de dos elementos y verificar dominio, cobertura y descenso de cada llamada. El código añade la observación de que la excepción puede dejar un arreglo modificado. | El defecto se puede localizar en la especificación antes de leer el código. La secuencia histórica de decisiones y el ahorro de retrabajo permanecen sin medir. |
| **TN, fase 3** | Calcular Γ sobre la ventana envolvente o por origen. | Antes de implementar, fijar origen y objetivo. Cambiar solo el sufijo y observar si se conserva el pronóstico que ya estaba determinado. | El protocolo y la ejecución precedieron al prototipo. El contraste sí cambió la elección registrada. El ahorro de tiempo organizacional permanece sin medir. |
| **LAB2** | Ordenar admisión, cálculo y confirmación del registro. | Al especificar la interacción entre ingesta, adaptador y almacenamiento. Introducir una entrada cuyo registro se descartaría y medir si cambió el estado. | El expediente atribuye el comportamiento a la secuencia del código. El piloto nuevo verifica una alternativa acotada. Las motivaciones originales y las demoras históricas permanecen abiertas. |

**Aplicación propuesta.** Cuando una decisión cruza interfaces o puede invalidar muchas pruebas posteriores, fijar el requisito y buscar un caso que separe las opciones antes de ampliar el prototipo. En otro ciclo comparable, registrar esfuerzo activo, iteraciones y cambios de decisión para evaluar la economía del método. [F001-R01](https://github.com/ksgfin8-cyber/f001/blob/2b60f32/docs/research/F001_RDL_PB_001_EVALUATION.md) · [KS-004](KS-004_CONSTRUCCION_TECNOLOGICA.md) · [LAB2-R01](https://github.com/ksgfin8-cyber/LAB2/blob/0c21d18/docs/research/LAB2_RDL_PB_001_EVALUATION.md)

## 4. Sensibilidad de la evidencia

| Instrumento | Defecto que puede distinguir | Cómo podría dar seguridad excesiva |
| --- | --- | --- |
| **Sonda de escala TN** | Con media de log-retornos no nula, exhibe la mezcla de unidades en el requisito de escala del piloto. | La primera serie casi anulaba el término defectuoso. Un resultado favorable describía el caso, con capacidad insuficiente para refutar la fórmula. |
| **Comparador de Filtrado** | Detectó y localizó un cambio inyectado en `ema_fast`. | Las rutas principales compartían código y el comparador de estado omitía `close_window`. Detectar esa perturbación acredita sensibilidad local, dejando abierta la equivalencia completa e independiente. |
| **Sonda nueva de recuperación** | Detecta mutación antes de admitir, memoria omitida al reiniciar y una entrada eliminada del registro con instantánea intacta. | Los ensayos usan un escritor y un archivo local. Las huellas del registro permiten comprobar igualdad en la representación probada. La corrupción coordinada, la concurrencia y la verificación independiente del cálculo necesitan sus propios controles. |

Una prueba de recuperación debe incluir al menos un control que cambie memoria dejando intactas las reglas de comparación y otro que degrade el registro persistido. Así se puede distinguir la sensibilidad de la sonda de la mera repetibilidad de la corrida. [KS-003](KS-003_PLAN_INFRAESTRUCTURA.md) · [Filtrado-R01](https://github.com/ksgfin8-cyber/Filtrado/blob/e93a6bb/docs/research/FILTRADO_RDL_PB_001_EVALUATION.md)

## 5. Composición y piloto ejecutado

Los expedientes separaban corte temporal y fidelidad de la memoria. Dejaban abierta una decisión concreta: recuperar desde entradas confirmadas o restaurar una instantánea. Se probó primero un acumulador con resultado manual y luego el adaptador local original de LAB2, que llama a GEI. El instrumento usa el ejecutor de fase 2 sin cambios. Toma de la fase 3 el control de perturbación del sufijo y usa su propio adaptador de eventos para ejercer memoria. WORLD-LAB proporciona la referencia conceptual de replay bajo identidad de entorno. Su motor no interviene en esta ejecución. [Acta de WORLD-LAB](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/audits/WORLD_LAB_OPERATIONAL_FREEZE.md) · [Sonda](instrumentos/recuperacion/probar.mjs)

### Protocolo previo

Pregunta. Comparar replay de entradas admitidas con restauración de instantánea para reanudar un cálculo con memoria y reconciliar sus observaciones. Primer receptor real, adaptador local de TN en LAB2 0c21d18, sin ejecutar su aplicación ni alterar el núcleo. Comenzar por un acumulador con resultado manual 101+102+103+104+105+106=621. La entrada trae una ventana de 21 cierres y una marca de confirmación sintética explícita. Un solo símbolo, identificadores estrictamente crecientes en cierres confirmados, un proceso escritor. Rechazar provisional y duplicado antes de llamar al modelo. Duplicado tardío con la misma clave no concede autoridad para revisar un cierre. Comparar corrida limpia de seis cierres con una que incluye provisionales y duplicados. La referencia de recuperación es la corrida limpia sin interrupción.

Contrastes previos. (1) En procesos separados, interrumpir el proceso en el tercer cierre entre cálculo y reemplazo del registro, y justo después del reemplazo, antes de que el controlador reciba confirmación. Reentregar todo el flujo. Ejecutar los dos cortes con replay y con instantánea. Exigir igualdad de filas confirmadas y del estado final íntegro para el acumulador y el estado expuesto por el adaptador LAB2, más el mismo comportamiento en el resto de la secuencia. Exigir 2 y 3 entradas presentes al reiniciar, respectivamente. Exigir que las corridas limpias y con ruido concuerden sin interrupción. (2) Controles negativos de omitir recuperación de memoria, perder una entrada del registro mientras se conserva la instantánea, y efectuar la admisión después de mutar. Deben fallar o ser detectados por el instrumento. (3) Verificar que cambiar precios de los tres cierres finales no afecta las primeras tres observaciones. Esto prueba el corte de entrada externo del piloto, no los cortes internos de GEI.

Contar reevaluaciones necesarias para recuperar, tamaños de representación para el mismo historial y campos de estado que la ruta de instantánea debe restaurar. No inferir ahorro medido de tiempo, validez predictiva, concurrencia ni durabilidad ante corte del sistema. Usar archivo temporal y reemplazo dentro del mismo directorio para inyectar los dos cortes en un proceso escritor local. Se preservan las ventanas exactas para el replay. Usar resultados deterministas en el ejecutor de fase 2. Evaluador de fase 3 como referencia del corte externo. La integración de sus puntuaciones con GEI no es necesaria para contestar esta pregunta.

El protocolo se registró localmente a las 17:38:21 UTC antes de escribir y ejecutar la sonda, con SHA-256 `04868ddcd09bcebb59214426023d3d1f66a9f4c842e96e02d7800ee2146d66ed`. El corte anterior interrumpe el proceso después de calcular y antes de iniciar el reemplazo del registro. El posterior lo interrumpe después del reemplazo, antes de responder. Cada reinicio se ejecuta en otro proceso y reentrega el flujo completo. La instantánea usa los cinco campos de memoria expuestos por el adaptador, incluidos el historial de teorías, la teoría activa, el historial de transiciones, los recuentos de uso y el tick. El arnés restaura vía el mapa que devuelve ese adaptador.

### Resultados y alcance

| Estrategia | Entradas presentes al reiniciar antes / después | Cálculos de recuperación antes / después | Tamaño final del registro de LAB2 | Resultado |
| --- | ---: | ---: | ---: | --- |
| Replay desde entradas confirmadas | 2 / 3 | 2 / 3 | 3.296 bytes | Misma trayectoria y mismo estado para ambos cortes. |
| Instantánea y registro coordinados | 2 / 3 | 0 / 0 | 3.922 bytes | Misma trayectoria y mismo estado para ambos cortes. |

- El **acumulador** terminó en tick 6 y suma 621. Sus seis sumas parciales coincidieron con la cuenta manual. Ambas estrategias recuperaron estado y filas en los dos cortes.
- El **adaptador de LAB2** terminó en tick 6. Las teorías seleccionadas fueron 8, 0, 1, 2, 3 y 4. Las seis filas y las huellas de estado de cada transición coincidieron con la corrida limpia bajo las dos estrategias y los dos cortes. El estado final íntegro dentro de la representación expuesta coincidió también. Se ejerció memoria con seis cambios de teoría.
- El control de admisión posterior a mutar divergió en la segunda transición registrada en ambos modelos. El reinicio sin recuperar la memoria divergió en la cuarta. Eliminar la última entrada mientras se conservaba la instantánea activó el rechazo por desacuerdo entre ambos.
- Alterar los tres cierres finales conservó las tres primeras filas. Esto respalda el corte externo de las entradas sintéticas. Sigue abierta la incoherencia temporal interna de GEI documentada en el expediente correspondiente.
- La instantánea añadió 626 bytes en esta representación y evitó ejecutar las transiciones previas al reinicio. Ambas estrategias conservaron el registro, incluidas las ventanas de entrada necesarias para reproducir. Se midieron cálculos y bytes. El efecto sobre latencia, mantenimiento y coste a escala queda abierto. El archivo se reemplaza completo por transición en este prototipo. La combinación de proceso controlado y reemplazo local no acredita durabilidad ante corte eléctrico, acceso concurrente ni persistencia de LAB2 en producción.

## 6. Decisiones para el siguiente uso

| Decisión | Evidencia y condición de reapertura |
| --- | --- |
| **Conservar replay como referencia experimental.** | Permite recalcular el prefijo y contrastarlo con las observaciones y huellas de estado registradas. Encaja en ejecuciones cortas con entradas reproducibles y modelo determinista en el alcance correspondiente. |
| **Considerar instantáneas al observar un problema de recuperación.** | La instantánea evitó recalcular el prefijo en el piloto. Su adopción añade un contrato de estado, vínculo con el registro y compatibilidad de representación. Reabrir con una carga representativa, un presupuesto de latencia y una necesidad real de recuperación. |
| **Aplicar las comprobaciones de admisión en un receptor concreto.** | El adaptador original quedó ejercitado bajo un arnés. Antes de promover un observador operativo, el siguiente contraste debe usar su almacenamiento real y una política de identidad, confirmación y revisión acorde a la fuente. |
| **Mantener el escalamiento de fase 2 como evaluación propia.** | Este trabajo reutilizó el ejecutor en otra sonda y exploró recuperación en un caso pequeño. La fiabilidad de lotes, el coste operativo y la adaptación a otro dominio siguen pendientes. Un consumidor de telemetría con eventos revisables o un simulador con memoria son posibles receptores. |

El conocimiento verificable nuevo es la recuperación de ambas representaciones en el adaptador y el poder discriminativo de los controles. La hipótesis de infraestructura es una combinación reutilizable de admisión, registro y recuperación. Su promoción depende de un segundo receptor con la misma necesidad, evidencia de transferencia y coste de adaptación.

### Reproducción

Node 24.22.3 y Python 3.12.14. Desde el repositorio `engineering-knowledge`, con un checkout de LAB2 en el directorio hermano. Se verificaron los blobs de los nueve módulos de núcleo requeridos y del adaptador original por separado. El blob del adaptador `src/lib/tn-engine/client.ts` es `c184f4e8eb03b693329a1f50f2e5d5b94daa3255`.

```sh
set -eu
tmp=$(mktemp -d)
lab2=0c21d1853006214b8fda16d18c1cb6693aa601c6
git -C ../LAB2 archive "$lab2" src/core/tn-engine src/lib/tn-engine/client.ts | tar -x -C "$tmp"
node --disable-warning=ExperimentalWarning instrumentos/recuperacion/probar.mjs "$tmp" accumulator > "$tmp/accumulator.json"
for run in 1 2; do
  python3 instrumentos/caracterizacion/ejecutar.py --candidate LAB2-adaptador --revision "$lab2" \
    --protocol admision-recuperacion-v1 -- node --disable-warning=ExperimentalWarning \
    instrumentos/recuperacion/probar.mjs "$tmp" > "$tmp/run-$run.json"
done
cmp "$tmp/run-1.json" "$tmp/run-2.json"
sha256sum "$tmp/accumulator.json" "$tmp/run-1.json"
```

Las dos corridas integradas fueron idénticas byte por byte, SHA-256 `1a5ce7818d2fd054d0a964de234a64aafa37a163236a4d79ea6c70787317e2f8`. La salida aislada del acumulador tiene SHA-256 `cac033cc84683237ee45add74cf1b14284ce49237ee0ef5f3a228545fbf64d64`. Los tiempos de pared se dejan fuera de la salida determinista.

# KS-005 · Posicionamiento tecnológico y decisiones de inversión

**Corte** · 24 de noviembre de 2026, Ecuador  
**Estado** · Fase 4 ejecutada. Dictamen para decisión de cartera.  
**Unidad de comparación** · Capacidad demostrada para un uso, una versión y unas condiciones determinadas.

## 1. Dictamen

El programa puede **operar un entorno experimental especializado**, **investigar mecanismos propios** y **convertir fallos en controles reutilizables**. La capacidad mejor establecida es WORLD-LAB dentro de su perfil congelado. La mayor brecha para escalar la cartera es demostrar que la cadena de datos, ejecución y evidencia funciona de forma repetida y recuperable, con un coste conocido. En modelos cuantitativos, la ventaja predictiva permanece sin demostrar. [Evaluación de cartera](KS-001_EVALUACION_CARTERA.md) · [Catálogo](KS-002_CATALOGO_CONOCIMIENTO.md) · [Piloto de infraestructura](KS-003_PLAN_INFRAESTRUCTURA.md) · [Piloto de construcción](KS-004_CONSTRUCCION_TECNOLOGICA.md)

**Recomendación estratégica.** Mantener WORLD-LAB operativo y financiar un ciclo acotado para convertir la evaluación causal, el registro fiel y los controles discriminativos en capacidades que sirvan a receptores concretos. Dar a TN una pregunta científica propia, con una puerta temprana que pueda detener la variante. Conservar los indicadores, el backtester y F001 según el uso que su evidencia respalda. Asignar presupuesto de ampliación únicamente cuando la siguiente prueba pueda cambiar una decisión.

**Alcance de la conclusión.** La revisión externa establece referencias funcionales y organizativas. El control de F001 fue ejecutado localmente. Las demás comparaciones externas se documentaron y sus ensayos emparejados quedan pendientes. El corte usa los candidatos y expedientes identificados en KS-001 a KS-004. El dictamen recomienda asignaciones y puertas para el próximo ciclo.

## 2. Autoridad y criterio de inversión

La Especificación Estratégica v1.0 distingue dirección, diseño del programa y ejecución en §9. §§21–26 vinculan aprendizaje, desarrollo de capacidades y transferencia a decisiones. §§29–30 y 43–48 exigen valorar coste, alternativas y capacidad institucional resultante. RDL-PB-001 v0.1 §§5–11 exige formular preguntas y elegir pruebas discriminativas. §§12–14, 17–20 y 23 gobiernan el alcance de las afirmaciones, la transferencia, la economía, la decisión y el cierre. [Especificación Estratégica](https://chatgpt.com/library?file_id=libfile_e0932365a6ac8191a15982b0355879e0&account_id=personal) · [Playbook](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/program/RDL-PB-001_v0.1_original_propuesta.md)

Una propuesta entra al ciclo si tiene un receptor actual o un tipo de proyecto receptor descrito, una incertidumbre que cambia una decisión y una prueba capaz de resolverla a coste razonable. Se considera primero el requisito que puede invalidar el uso. Cuando existe una alternativa que ya cumple ese requisito, se compara antes de construir. El valor de una exploración matemática también puede justificar un ciclo propio si se define qué conocimiento dejaría una refutación. El coste de oportunidad se expresa como trabajo explícitamente desplazado.

Para el contraste externo se eligieron referentes con fuentes primarias y un mecanismo pertinente. La distinción entre **demostrado internamente**, **documentado externamente** y **comparado en ejecución** determina qué afirmaciones habilita cada fila.

## 3. Posición por dominio y referencias externas

| Dominio y evidencia interna | Qué ofrece la referencia y en qué es más completa | Disposición y contraste pendiente |
| --- | --- | --- |
| **Entornos dinámicos y agentes.** WORLD-LAB reprodujo 256 trayectorias en su motor. TITAN-MVP-01 reutilizó el entorno. D4 encontró equivalencia con el control directo en el dominio ensayado. | Gymnasium documenta una interfaz de entorno con semillas y distingue terminación de truncamiento. Su comprobador proporciona una referencia de conformidad de API. OpenSpiel aporta juegos y métricas para preguntas de decisión donde existe una formulación compatible. NASA Trick aporta un ejemplo de infraestructura de simulación reutilizable en otro dominio. | **Operar** el perfil actual. Probar un adaptador de Gymnasium solo con un receptor que requiera integrar otro agente o herramienta. El contrato mínimo compara observación, acción, terminación y replay bajo un subconjunto equivalente. Abrir un nuevo TITAN únicamente con una propiedad capaz de separarlo de D4 o de otro control directo. [Gymnasium](https://gymnasium.farama.org/api/env/) · [Comprobador](https://gymnasium.farama.org/_modules/gymnasium/utils/env_checker/) · [OpenSpiel](https://openspiel.readthedocs.io/en/latest/intro.html) · [NASA Trick](https://github.com/nasa/trick) |
| **Modelado temporal.** TN conserva mecanismos propios y un evaluador causal experimental. La réplica histórica de GEI perdió ante Random Walk en 9 de 9 trayectorias sintéticas. La fase 3 verificó causalidad local y redujo cálculos repetidos para las teorías probadas. | sktime documenta cortes con horizonte explícito y un pronosticador ingenuo de último valor. StatsForecast documenta Naive y AutoARIMA como alternativas de evaluación. Son referencias más completas para organizar una comparación temporal. Su error relativo frente a una variante corregida de TN queda pendiente. | **Financiar** un protocolo reservado tras validar unidades y cortes. Comparar Random Walk, teoría fija y selector sobre los mismos orígenes. Evaluar AutoARIMA si el primer contraste deja una razón concreta para añadirlo. [sktime, ventanas](https://www.sktime.org/en/latest/api_reference/auto_generated/sktime.forecasting.model_selection.expandingwindowsplitter.html) · [sktime, Naive](https://www.sktime.net/docs/api-reference/sktimeforecastingnaivenaiveforecaster/) · [StatsForecast](https://nixtla.github.io/statsforecast/docs/getting-started/getting_started_complete.html) |
| **Datos y simulación financiera.** FASES1234 y Filtrado permiten auditar un CSV compartido. El bruto falta. Indicadores dejó un oráculo de costes y un motor rechazado para decisiones de rendimiento. | OpenLineage ofrece un modelo explícito de ejecución, trabajo y dataset. LEAN documenta frontera temporal y extensiones para fills, comisiones y deslizamiento. Estas capacidades tienen cobertura documentada frente a brechas internas. La conformidad de un adaptador con nuestras convenciones queda pendiente. | **Reconstruir una cadena para una fuente concreta** cuando haya consumidor y procedencia. Ante una pregunta que requiera ejecutar órdenes, probar LEAN primero con el oráculo a precio constante, el momento de disponibilidad y la reconciliación de posiciones y capital. El XAUUSD histórico permanece apto para descripción acotada. [OpenLineage](https://openlineage.io/docs/spec/object-model/) · [LEAN](https://github.com/QuantConnect/Lean) · [Frontera temporal](https://www.quantconnect.com/docs/v1/key-concepts/understanding-time) · [Órdenes y costes](https://www.quantconnect.com/docs/v2/writing-algorithms/live-trading/trading-and-orders) |
| **Estado, persistencia y trazas.** LAB2 exhibió mutaciones no registradas y recuperación parcial. BOX1 aporta casos de referencias mutables y fallos de serialización. | XState documenta instantáneas de actores y el patrón de registro de eventos. MLflow ofrece registro de ejecuciones, parámetros y artefactos. Sirven para evaluar dos necesidades diferentes, la recuperación del estado y la trazabilidad de las corridas. | **Probar** en un consumidor con estado real. Inyectar un duplicado, una actualización provisional y un reinicio. Exigir el mismo estado que una corrida limpia y reconciliar entradas admitidas con eventos registrados. Adoptar almacenamiento de experimentos solo si el modo local pierde trazabilidad o introduce coste recurrente medido. [XState](https://stately.ai/docs/xstate/v6/persistence) · [MLflow](https://mlflow.org/docs/latest/ml/tracking/) |
| **Indicadores AURORA y Quantum Viper.** Sus auditorías de fórmulas y estados descubrieron contradicciones, pero carecen de trazas Pine independientes. | La documentación oficial de Pine fija la semántica de barras abiertas y confirmadas. La alternativa funcional depende del problema. Un clasificador explícito de regímenes o la abstención constante pueden servir de control una vez definidos objetivo, horizonte y pérdida. | **Pausar** la validación externa costosa. AURORA requiere contrato común de estados y significado de Ω. Viper requiere contrato del voto P2, la memoria, la abstención y la vigencia del NRT. Reabrir con definición verificable y datos alineables. [Pine](https://www.tradingview.com/pine-script-docs/concepts/bar-states/) · [AURORA-R01](https://github.com/ksgfin8-cyber/aurora/blob/e6792fd/docs/research/AURORA_RDL_PB_001_EVALUATION.md) · [QV-R01](https://github.com/ksgfin8-cyber/quantum-viper/blob/f55fc60/docs/research/QUANTUM_VIPER_RDL_PB_001_EVALUATION.md) |
| **Derivación de algoritmos.** F001 tiene un contraejemplo histórico y una geometría alternativa modelada. | Python proporciona ordenamiento estable y un oráculo funcional disponible. Hypothesis permite generar y reducir contraejemplos cuando haya una variante. En el contraste finito de §4 la referencia supera inequívocamente al candidato histórico en cumplimiento funcional. | **Archivar la revisión histórica como candidato de ordenamiento** y preservar el estudio de derivación. Reabrir si se formula una propiedad diferencial medible, como memoria auxiliar bajo un contrato comparable. Validar descenso, permutación, orden, estabilidad y subrangos antes de costes. [Python](https://docs.python.org/3.12/howto/sorting.html) · [Hypothesis](https://hypothesis.works/) |
| **Aplicaciones y confirmación externa.** Almuerzos conserva transiciones útiles. InHouse preservó el modo normal dentro del contraste descrito en KS-001. El estado local de envío excedió la evidencia observada. | Playwright permite esperar resultados y comprobar efectos observables en el navegador. La confirmación de entrega exige evidencia del sistema receptor. | **Conservar** el patrón de extensión y de transición. Si vuelve a existir un proyecto receptor, validar modo, destino y acuse por separado. Reabrir inversión de producto con un usuario y un criterio de aceptación de campo. [Playwright](https://playwright.dev/docs/actionability) · [KS-001](KS-001_EVALUACION_CARTERA.md) |
| **Prototipo histórico CYBERsec.** El corte registra limitaciones de importación, alcance y métricas, con equivalencia con TITAN abierta. | Las referencias para el próximo candidato dependen de una propiedad formal y un dominio definidos. La literatura de madurez tecnológica de sistemas de ML ofrece criterios de transición aplicables si existe un receptor concreto. | **Mantener en archivo histórico** con sus límites. Exigir una interfaz funcional y un objetivo medible antes de asignar recursos a otro contraste. [Marco de madurez de ML](https://doi.org/10.1038/s41467-022-33128-9) · [KS-001](KS-001_EVALUACION_CARTERA.md) |

### Referencias para dirigir el programa

**DARPA** hace explícitas la alternativa actual, la novedad, el riesgo, el coste y las pruebas intermedia y final. Aplicación propuesta: usar esas preguntas cuando se solicita ampliar inversión, dejando los controles menores en el expediente técnico. **MLCommons** publica escenarios y reglas de medición para interpretar resultados de un benchmark. Aplicación propuesta: fijar escenario, entradas, métricas y elegibilidad antes de comparar, con una referencia sencilla y una ruta para reproducir la medición. Ambos ejemplos aportan prácticas documentadas. El impacto de adoptarlas en esta organización se debe medir. [DARPA](https://www.darpa.mil/about/heilmeier-catechism) · [MLCommons](https://mlcommons.org/benchmarks/inference-datacenter/)

## 4. Comparación ejecutada · F001 frente al ordenamiento de Python

**Criterio fijado antes del contraste.** Para cada vector de enteros, el candidato cumple si retorna normalmente y su secuencia coincide con la de `sorted`. Se enumeró el producto cartesiano de los valores −1, 0 y 1 para longitudes de 1 a 5 y rangos completos. Como control de referencia, `list.sort` coincidió con `sorted`; ambos pertenecen a la biblioteca de Python. Se registró la mutación visible cuando el candidato lanzó una excepción.

| Longitud | Entradas | Retorno normal y resultado igual | Excepciones | Excepciones con arreglo modificado |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 3 | 3 | 0 | 0 |
| 2 | 9 | 6 | 3 | 3 |
| 3 | 27 | 10 | 17 | 17 |
| 4 | 81 | 20 | 61 | 61 |
| 5 | 243 | 21 | 222 | 210 |
| **Total** | **363** | **60** | **303** | **291** |

La revisión histórica lanzó `AssertionError` en los 303 fallos. Python devolvió una secuencia ordenada en 363 de 363 casos. El resultado extiende el contraejemplo conocido dentro de un universo finito. El contraste carece de etiquetas de identidad para discernir estabilidad, cubre rangos completos y deja abiertos memoria, subrangos y rendimiento. La frecuencia observada corresponde a esta enumeración y carece de interpretación como tasa en producción.

**Reproducción.** Python 3.12.14, con aserciones habilitadas. Usar `f001_code` de [f001@23e4027](https://github.com/ksgfin8-cyber/f001/blob/23e4027/f001_code), blob `bd694ded1a4fbd96d6581c5457039d58dbd58726`. Guardar el bloque como `f001-control.py` y ejecutar `python f001-control.py f001_code`. Dos ejecuciones produjeron la misma salida con SHA-256 `ebd91c44f1c3e8db1b9678dcbf75976f744da95295e743d68428350ed7d02890`. [Auditoría original](https://github.com/ksgfin8-cyber/f001/blob/2b60f32/docs/research/F001_RDL_PB_001_EVALUATION.md)

```python
"""Functional comparison fixed before running the finite grid."""
from collections import Counter
from itertools import product
from pathlib import Path
from runpy import run_path
import json
import sys

assert __debug__, "Run with contract assertions enabled"
sort_candidate = run_path(str(Path(sys.argv[1])))["mergesort"]
results = {}
for n in range(1, 6):
    counts = Counter()
    for values in product((-1, 0, 1), repeat=n):
        expected = sorted(values)
        control = list(values)
        control.sort()
        assert control == expected
        counts["control_pass"] += 1
        candidate = list(values)
        try:
            sort_candidate(candidate, 1, n)
        except (AssertionError, IndexError, RecursionError) as error:
            counts[type(error).__name__] += 1
            counts["mutated_on_error"] += int(candidate != list(values))
            continue
        counts["normal_equal" if candidate == expected else "normal_different"] += 1
    results[n] = dict(counts)
print(json.dumps(results, sort_keys=True))
```

## 5. Decisiones propuestas para el siguiente ciclo

| Nivel | Decisión y responsable funcional propuesto | Entregable y puerta |
| --- | --- | --- |
| **Estratégico** | Dirección de I+D. Mantener WORLD-LAB como capacidad operativa especializada. Asignar tiempo de nueva construcción a evaluación causal y evidencia reproducible con un receptor. Mantener una vía de exploración matemática con presupuesto explícito. | Aprobar un encargo principal y una alternativa que se difiere. El criterio de ampliación es una capacidad adicional demostrada a un coste defendible. |
| **Táctico** | Responsable del ciclo. Priorizar un evaluador temporal con TN como primer consumidor. Fijar versiones, unidades, disponibilidad, objetivo, métrica, referencias y una muestra de evaluación reservada. Separar las decisiones de idoneidad del instrumento y continuidad del modelo. | Pasar primero consistencia dimensional, invariancia del pronóstico ante cambios de sufijo y fidelidad de la traza. Luego abrir la muestra una vez y evaluar con una diferencia mínima relevante y tratamiento de la incertidumbre fijados de antemano. Si falla un prerrequisito, detener el gasto predictivo y registrar la causa. Si el selector no aporta una ventaja práctica frente a las referencias elegibles, cerrar el candidato evaluado y conservar el instrumento. |
| **Operativo** | Responsable de ejecución y función de revisión técnica. Reproducir el piloto, añadir controles de fallo y registrar el resultado junto al candidato y la decisión. Para la escala del ejecutor de fase 2, fijar carga representativa, tiempo, memoria, integridad y recuperación antes de lanzar un lote. | Una corrida limpia, un fallo inducido y una reanudación, con el mismo conjunto final de resultados trazables que una corrida limpia. Comparar coste de adaptación, tiempo activo, fallos y trabajo manual contra una línea base predefinida. Ampliar únicamente con evidencia de demanda y operación. |

**Secuencia de inversión.** Primero, controles contractuales y un comparador sencillo. Después, un receptor real o un prototipo acotado con criterio de descarte. La integración de un segundo runtime, una nueva ingesta o un almacén central compite por presupuesto cuando hay una pregunta que requiere esa capacidad. Dar prioridad al instrumento de evaluación desplaza temporalmente la reescritura del backtester, la ampliación de WORLD-LAB y otra investigación predictiva de indicadores. Una pregunta con receptor confirmado y coste menor puede cambiar el orden.

**Transferencia a proyectos aún no iniciados.** Un simulador de colas o recursos puede usar el patrón de observación, acción y replay de WORLD-LAB si necesita dinámica controlada. Un sensor o motor de reglas que consume eventos puede usar los controles de duplicados, provisionalidad y recuperación de LAB2 y BOX1. Un sistema de pronóstico de demanda puede usar la perturbación del sufijo y el contrato de disponibilidad sin adoptar las teorías de TN. En cada caso, la transferencia se acredita en el receptor cuando mantiene la capacidad que motivó su adopción y se conoce el esfuerzo de adaptación. [Catálogo](KS-002_CATALOGO_CONOCIMIENTO.md)

## 6. Revisión multidisciplinar y medición

| Disciplina | Pregunta que debe poder cambiar la decisión | Sesgo que debe controlarse |
| --- | --- | --- |
| Matemática y modelado | ¿Las unidades, el dominio y la propiedad afirmada sobreviven a un caso límite? | Confundir elegancia formal con utilidad observable. |
| Estadística y dominio | ¿El objetivo, la información disponible y la diferencia mínima representan el uso? | Favorecer al modelo con selección de escenarios, métricas o ventanas posterior al resultado. |
| Ingeniería y operación | ¿Se puede repetir, recuperar y auditar la ejecución al coste previsto? | Confundir un prototipo exitoso con una plataforma operativa o una interfaz con un contrato íntegro. |
| Economía y dirección de I+D | ¿La siguiente prueba cambia una decisión valiosa y qué trabajo desplazará? | Favorecer el volumen de pruebas o el éxito inmediato a costa de capacidad futura. |

Cada revisión conserva la afirmación, la evidencia, el alcance y el caso que la refutaría. El responsable del mecanismo registra su interpretación y una revisión distingue capacidad real, defecto del instrumento y discrepancia de objetivos. Cuando una persona cubre varios roles, se registran las conclusiones por separado y se busca una comprobación independiente para afirmaciones de alto impacto. Se preservan los desacuerdos junto con la prueba que podría resolverlos. Una contradicción demostrada del requisito bloquea la promoción prevista hasta resolverse. Los criterios y el presupuesto se fijan antes de observar la evidencia reservada.

**Medición de dirección.** Registrar coste y tiempo activo por decisión, incidencias que requirieron intervención, reproducibilidad de ejecuciones elegibles, receptores con transferencia efectiva y trabajo recurrente desplazado. Para escala, conservar además volumen, memoria máxima, pérdida o duplicación de resultados y recuperación. Para ciencia, conservar preguntas cerradas y qué decisión cambió. Comparar ciclos comparables antes de afirmar una mejora de productividad. El piloto de fase 3 establece ahorro de llamadas a Γ para el caso medido. El piloto de fase 2 establece uso del mismo ejecutor en F001 y TN. La operación a escala se mantiene abierta. [KS-003](KS-003_PLAN_INFRAESTRUCTURA.md) · [KS-004](KS-004_CONSTRUCCION_TECNOLOGICA.md)

**Cierre de fase 4.** El posicionamiento, la oportunidad de inversión, los referentes y las puertas quedan registrados. La primera decisión de cartera propuesta es financiar un ciclo pequeño de evaluabilidad temporal y mantener WORLD-LAB en operación. La primera prueba de transferencia debe tener un receptor definido. Los ensayos de mercado, la equivalencia con runtimes independientes y la evaluación a escala tienen puertas propias.

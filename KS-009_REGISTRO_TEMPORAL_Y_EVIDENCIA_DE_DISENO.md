# KS-009 · Registro temporal y evidencia de diseño en dos dominios

**Corte** · 25 de noviembre de 2026, Ecuador.  
**Estado** · Piloto local ejecutado.  
**Objeto** · Registro experimental SQLite con entregas, versiones, decisiones y referencias de entrada.  
**Antecedentes** · [KS-002](KS-002_CATALOGO_CONOCIMIENTO.md) · [KS-006](KS-006_DIMENSIONES_Y_RECUPERACION.md) · [KS-007](KS-007_CADENA_TEMPORAL_Y_VALOR_DEL_LABORATORIO.md) · [KS-008](KS-008_SIGUIENTE_GENERACION_Y_TRANSFERENCIA.md)

## Dictamen

**Continuar con un registro local compartido para un uso interno acotado.** El mismo núcleo conservó la consulta temporal y la trazabilidad de decisiones en un caso económico y uno logístico. Estos usos justifican conservar el componente como instrumento de investigación. La operación recurrente, la economía comparativa y la validación con un receptor real quedan abiertas.

**Preservar dos vistas del pasado.** Una consulta retrospectiva puede incorporar una corrección que se cargó después. Una decisión ya registrada conserva el corte, la versión de regla y la frontera de entradas que realmente tenía el registro cuando se ejecutó. Una fixture que rompía la equivalencia entre ambas consultas justificó conservar esa frontera.

**Conservar dos casos mínimos de diseño.** El orden de escritura no determina cuál es la revisión que corresponde al corte. Un despacho preparado no confirma recepción. Ambos casos dejan un requisito comprobable para un diseño posterior.

## 1. Contrato y protocolo previo

El Playbook exige una alternativa falsable y evidencia proporcional a la decisión. La Especificación Estratégica distingue transferencia, economía de investigación y madurez. El piloto usa el oráculo manual y una referencia por dominio para decidir sobre el registro local. Las revisiones históricas de productos y los documentos normativos permanecen como fuentes de referencia. [Especificación Estratégica, §§12, 15–16, 25, 29 y 45](https://chatgpt.com/library?file_id=libfile_e0932365a6ac8191a15982b0355879e0&account_id=personal) · [RDL-PB-001, §§6–9, 11–14, 17 y 23](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/program/RDL-PB-001_v0.1_original_propuesta.md)

El piloto usa SQLite local con un escritor, fuentes identificadas y marcas UTC proporcionadas por las fixtures. Se mantiene en solo lectura la cartera histórica. El criterio de parada es una reproducción fiel del caso BEA y una transferencia logística con el mismo núcleo. Se presupuestan dos recorridos y dos decisiones de diseño, con casos pequeños antes de extensiones de plataforma. El valor comercial y el coste institucional comparativo permanecen sujetos a receptor y línea de base.

- Identidad de la entrega distingue reintentos de contenido. Identidad de la observación es fuente, entidad y revisión positiva. Un duplicado exacto con otra entrega no vuelve a crear una versión. Un contenido incompatible en la misma identidad queda registrado como conflicto, sin reemplazar la versión admitida.
- Se conserva el bruto y su huella, la identidad de fuente y regla, y marcas de ocurrencia, publicación si consta, recepción y admisión. Una observación es elegible si fue admitida hasta el corte inclusive. Entre elegibles gana la revisión mayor. Cada decisión fija el corte y la frontera de versiones registradas, de modo que un alta posterior con admisión anterior no reescribe su conocimiento. Se conservan las referencias de entrada y versión de regla. Cualquier efecto externo exige un comprobante identificado.
- Oráculo económico (décimas de punto): antes del 25 de abril 12:30Z, ninguno; 30 de mayo 12:29:59Z, 16; 30 de mayo 12:30:00Z, 16; 30 de mayo 12:30:02Z, 13; 28 de junio, 14; 26 de septiembre, 16. Para la primera revisión de mayo se modela recepción un segundo y admisión dos segundos después de publicación. En otros casos BEA se simula admisión inmediata. Estos tiempos no acreditan recepción histórica. El consumidor usa umbral 15 y el comparador negativo usa siempre la revisión final.
- Oráculo logístico: G1 concuerda (2/2), G2 difiere (4/5), G3 carece de recepción, G4 carece de despacho. Con tolerancia 1 cambia solo G2. Una revisión de la recepción a 4 hace concordar G2 incluso con tolerancia 0 en el corte nuevo; el histórico anterior conserva su diferencia. Cambiar la regla conserva la identidad y el resultado de decisiones ya registradas.
- Verificar duplicados, conflicto, fuera de orden, revisión tardía, alta retroactiva, cambio de regla y una interrupción de proceso justo antes y justo después de confirmar una entrega, seguida del mismo reintento. Comparar con una trayectoria local limpia.
- Diseño: contrastar el criterio que toma la última entrega con un oráculo de revisión fuera de orden. En operación comparar estado local preparado con evidencia de una recepción auténtica dentro de la fixture y exigir comprobante. Usar un mapa simple y un caso de valores concretos para observar qué decisión revela cada uno. Se mide coste descriptivo de la ejecución, cambios estructurales y pasos manuales. La operación con un receptor real y una campaña dinámica quedan condicionadas a su necesidad y disponibilidad.

El protocolo se registró localmente antes de escribir las sondas, el 25 de noviembre a las 18:49:33 UTC. SHA-256 del archivo original `3835821ddf3d9667aaade4c780eab31662e8815047edb2a05c2a154cfbff74bf`. El presupuesto se fijó por alcance experimental. El reloj de ejecución y el esfuerzo de construcción tienen métricas distintas.

| Transición | Registro y condición demostrada |
| --- | --- |
| **Entrega → admisión** | El sobre recibido se conserva por bytes cuando se registra como admitido, duplicado o conflicto. Se separa identidad de entrega de identidad y revisión de la observación. Una entrega reintentada retorna su resultado anterior. La cronología inválida se rechaza antes de persistir. |
| **Admisión → consulta** | El corte es inclusivo. Entre las versiones elegibles de una identidad se selecciona la revisión mayor. Las marcas se normalizan a UTC con precisión de segundo. |
| **Consulta → decisión** | En una transacción se fijan corte, frontera de versiones, claves buscadas, regla, resultado e insumos seleccionados. El identificador de regla debe corresponder a la función suministrada por el consumidor. Este piloto conserva identidad y referencias. El despliegue de un registro de código ejecutable de cada regla queda abierto. |
| **Decisión → rastreo** | Se reconstruye la selección con su frontera original y se cotejan las referencias guardadas. La consulta de impactos lista las decisiones que efectivamente usaron una revisión. Un recálculo hipotético tendría identidad propia. |
| **Acción → efecto externo** | El consumidor logístico exige un registro del lado receptor antes de considerar completo el par. La fixture ilustra el contrato y no sustituye un comprobante de un receptor de campo. |

## 2. Primer uso · Publicaciones revisadas

El oráculo usa las cuatro publicaciones oficiales del PIB de BEA transcritas y vinculadas en [KS-008](KS-008_SIGUIENTE_GENERACION_Y_TRANSFERENCIA.md) y en [bea.json](instrumentos/siguiente-generacion/bea.json). La fuente BEA acredita la hora de publicación. Los sobres normalizados de este piloto fijan marcas **simuladas de recepción y admisión**, separadas de la hora de publicación. En mayo se simularon demoras de uno y dos segundos, respectivamente. No se ejercitó un conector BEA en vivo.

| Corte UTC | Versión admisible | Resultado del umbral 1,5 % |
| --- | ---: | --- |
| 25 de abril, 12:29:59 | Sin dato | Sin decisión |
| 30 de mayo, 12:29:59 | 1,6 % | Sí |
| 30 de mayo, 12:30:00 | 1,6 % | Sí |
| 30 de mayo, 12:30:02 | 1,3 % | No |
| 28 de junio, 00:00:00 | 1,4 % | No |
| 26 de septiembre, 12:30:00 | 1,6 % | Sí |

La consulta y la referencia independiente por recorrido del archivo coincidieron con el oráculo. La revisión final aplicada indiscriminadamente dio **tres respuestas de datos incorrectas**, entre ellas **dos decisiones cambiadas** y un dato antes de su publicación. Seleccionar por orden físico de llegada daba 1,3 % en el corte de junio, donde se esperaba 1,4 %. Se verificaron las **24 permutaciones** de las cuatro entregas para los mismos seis cortes. Este barrido es exhaustivo para la fixture y sus marcas.

Una carga retroactiva sintética posterior hizo que la consulta retrospectiva de junio pasara de 1,4 % a 1,7 %. La decisión ya registrada conservó 1,4 %, su resultado, las referencias y la regla original. La consulta de impactos de la revisión 3 identificó `gdp/4`. El duplicado con otro identificador de entrega se clasificó como duplicado. El contenido discrepante con la misma identidad de observación quedó registrado como conflicto y la revisión elegible se preservó.

## 3. Segundo uso · Reconciliación logística

La fixture usa documentos sintéticos de despacho y recepción. El núcleo compartido se mantuvo idéntico. El adaptador de prueba define los nombres de las fuentes, las entidades consultadas, la referencia de cada documento y la función de tolerancia.

| Guía | Tolerancia cero | Tolerancia uno | Tolerancia cero tras la corrección |
| --- | --- | --- | --- |
| G1 | Coincide | Coincide | Coincide |
| G2 | Diferencia 4/5 | Coincide | Coincide, recepción corregida a 4 |
| G3 | Pendiente de recepción | Pendiente de recepción | Pendiente de recepción |
| G4 | Falta despacho | Falta despacho | Falta despacho |

Las dos primeras columnas se cotejaron con el oráculo manual y con [las referencias Python y SQL de KS-008](instrumentos/siguiente-generacion/probar.py), mediante una correspondencia explícita de etiquetas. Se añadió **un consumidor logístico** sobre el mismo archivo de núcleo y **cero cambios de esquema o consultas del registro**. Pasar de tolerancia cero a uno cambió un parámetro de la función del consumidor y se registró con otra identidad de regla. Cargar la corrección cambió la vista posterior de G2. Las dos decisiones que habían usado la recepción original quedaron listadas y la anterior se pudo reconstruir. El caso acredita transferencia del registro **entre estos dos usos locales**, con continua dependencia de los adaptadores y las reglas específicas. El soporte, la utilidad económica y la recepción efectiva de un negocio requieren campo.

## 4. Interrupciones y decisiones de diseño

Se interrumpió un proceso escritor antes de confirmar una entrega y otro justo después de confirmarla, antes de responder. Al reabrir SQLite se observaron respectivamente **cero y una entrega persistidas**. En ambos casos, reintentar la misma entrega produjo el mismo resultado que la corrida limpia y dejó una sola entrega. Se ejercitó la frontera de confirmación observable de un proceso local. Los cortes eléctricos, varios escritores, restauración remota y fallos de almacenamiento exigen pruebas propias.

| Decisión | Evidencia que la cambió | Regla para un candidato posterior |
| --- | --- | --- |
| **Algoritmo de selección por corte** | El mapa `entrega → admisión → selección → decisión` localizó la frontera. La tabla con una revisión fuera de orden refutó seleccionar por último registro físico. La alta retroactiva refutó reconstruir una decisión solo con su fecha. | Resolver elegibilidad y precedencia por separado. Guardar la frontera de conocimiento de cada decisión. |
| **Regla operativa para pedidos o recepciones** | El mapa `despacho → posible recepción → conciliación` expuso la fuente de evidencia que faltaba. El caso G3 mantuvo `AWAITING_RECEIPT`, mientras G1 pudo conciliarse con ambos documentos de prueba. Cambiar tolerancia conservó esa diferencia de estado. | Exigir un comprobante receptor para cambiar un estado que afirma un efecto externo. Hacer un control donde el despacho existe y la recepción falta. |

El mapa mostró la dependencia entre componentes. La tabla produjo contraejemplos y oráculos concretos. Esta comparación descriptiva documenta qué aportó cada representación en dos decisiones del piloto. La productividad de una práctica general requiere ciclos comparables. WORLD-LAB se conserva como opción para preguntas donde la secuencia dinámica del entorno sea la causa a estudiar. En este piloto, las pruebas locales fueron suficientes para las decisiones de corte y confirmación.

## 5. Economía y decisión de ampliación

- **Operación local.** Un comando ejecuta los dos dominios, el barrido y la recuperación, e imprime el resultado. Las dos corridas finales se verifican por comparación byte por byte. El tiempo de proceso fue del orden de décimas de segundo. Incluye los subprocesos y las bases de prueba.
- **Adaptación.** El coste observado es estructural. La misma clase, tablas y consultas soportaron los dos usos. El segundo caso incorpora una fixture, una función de conciliación y su oráculo. Cambiar tolerancia queda en el consumidor. La referencia de archivo es adecuada y más directa para responder un corte aislado. El valor adicional del registro aparece al preservar decisiones, inspeccionar impactos y reintentar transacciones.
- **Economía pendiente.** El ciclo carece de medición de esfuerzo humano activo y de una comparación de mantenimiento con un receptor operativo. La reutilización observada permite ensayar esa comparación. El tiempo de proceso no acredita productividad organizacional.

| Línea | Disposición |
| --- | --- |
| Registro temporal | **Continuar** en alcance local. Probar recepción observada y un uso interno recurrente antes de una interfaz de servicio. |
| Reconciliación | **Validar** con un receptor cuando haya datos autorizados y un procedimiento de referencia. Medir adaptación, excepciones y soporte. |
| Diseño y verificación | **Transferir** los dos casos mínimos como controles de diseño. Revalidar el contrato y las transiciones en cada receptor. |
| Plataforma o servicio a terceros | Mantener abierta la decisión de inversión hasta que exista un receptor y podamos estimar coste, utilidad y responsabilidad sobre el dato. |

## Reproducción

Python 3.12.14 y SQLite 3.53.1 en la ejecución. Desde la raíz de `engineering-knowledge`:

```sh
set -eu
tmp=$(mktemp -d)
for run in 1 2; do
  PYTHONDONTWRITEBYTECODE=1 python3 -B instrumentos/registro-versionado/probar.py > "$tmp/registro-$run.json"
done
cmp "$tmp/registro-1.json" "$tmp/registro-2.json"
sha256sum "$tmp/registro-1.json"
python3 -B instrumentos/siguiente-generacion/probar.py
```

SHA-256 de la salida del registro `dc551278656fdd57eb37e757cde0047b246fff916d17d830436734972f63f8ab`. SHA-256 de la referencia KS-008 `2ae07714969e0d38f7d89a4a4c6a35311d8d8b7a13efa5e34368428ddcfa7335`. El desarrollo local usó una copia exacta de bea.json, blob `ef7af95ff5051f2cfe8aceba586220df7b662b2f`. El repositorio conserva una sola copia versionada de la fuente de prueba.

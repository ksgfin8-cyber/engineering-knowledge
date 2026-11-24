# KS-003 · Plan de infraestructura y piloto de caracterización

**Corte:** 24 de noviembre de 2026. **Etapa:** diseño y primera verificación de infraestructura. **Registro de partida:** [KS-001](KS-001_EVALUACION_CARTERA.md) y [KS-002](KS-002_CATALOGO_CONOCIMIENTO.md). **Marco operacional:** [RDL-PB-001 v0.1](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/program/RDL-PB-001_v0.1_original_propuesta.md), §§7–9, 11–12, 17 y 21–23.

## Decisión de alcance

**Incorporar un procedimiento mínimo de caracterización como candidato a infraestructura compartida.** El piloto ejecutó la misma capa de registro y validación en F001 y TN, con sondas y comparadores propios. El resultado respalda reutilización del procedimiento en los dos casos ensayados. Productividad, mantenimiento recurrente y operación a escala permanecen **NO EVALUADOS**.

El uso del catálogo y la construcción inicial se solapan. Para este ciclo bastó una decisión acotada y reversible sobre qué control incorporar. La expansión de cada línea sigue sus propias dependencias.

## Cartera y coste de oportunidad

Los costes son cualitativos y comparan la preparación del **primer caso útil**, bajo los insumos conocidos. Las inversiones futuras requieren estimación y medición propias.

| Línea | Opción recomendada y primer producto | Coste relativo y alternativa postergada | Evidencia para ampliar |
| --- | --- | --- | --- |
| Caracterización computacional | **Adaptar ahora.** Un ejecutor neutral para sondas, identidad, controles y registro. Oráculos por dominio. | Bajo con candidatos y toolchains ya identificados. Se posterga una plataforma central de campañas y resultados. | Nueva investigación de diseño con criterio fijado antes de ver los resultados. Medir adaptación, verificación y decisión en una ejecución limpia. |
| Estado, información y recuperación | **Prototipar tras delimitar la interfaz.** Reutilizar los casos de admisión de LAB2 y los controles de instantáneas de TN y BOX1. | Medio en memoria. El coste sube al incluir persistencia y recuperación reales. Se posterga un almacén común hasta que un receptor defina su frontera. | En un receptor, repetir eventos y reiniciar conservando el estado que corresponde al conjunto de entradas admitidas. |
| Datos temporales | **Adaptar para una fuente concreta.** Conservar reglas de procedencia, disponibilidad y ajuste por corte. | Medio con una fuente disponible. El histórico XAUUSD sigue condicionado por su fuente bruta. Se posterga la reconstrucción general de ingesta. | Reproducir una cadena fuente–transformación–salida y un caso que refute un ajuste temporal inválido. |
| Simulación y contabilidad | **Conservar los oráculos.** Probar una transición a precio constante antes de seleccionar o construir un motor. | Medio o alto para un motor completo, según ejecuciones, costes y datos. Se posterga el backtester general hasta que una pregunta requiera su uso. | Acuerdo exacto de eventos, posiciones y capital bajo un modelo explícito. Evaluar después discrepancias bajo fallos y cambios de estado. |
| Entornos dinámicos | **Operar WORLD-LAB dentro del perfil congelado.** | Bajo para reaprovechar el perfil. Mayor si la pregunta requiere otro motor o perfil. Se posterga la ampliación sin una propiedad que la exija. | Pregunta dinámica identificada y evidencia que justifique una ampliación. RC1 y TITAN G2 conservan los estados de sus expedientes. |
| Conformidad entre entornos | **Reutilizar el control de divergencias.** Conectar un comparador a dos trazas alineadas. | Bajo con ambas trazas. Depende de acceso a Pine u otro runtime para demostrar concordancia externa. Se posterga la integración hasta obtener una referencia independiente. | Caso limpio, perturbación detectada y primera divergencia localizable en los campos requeridos. |

Adoptar una herramienta externa es una alternativa cuando un requisito concreto excede el piloto. Su comparación formal y la posición externa de la cartera corresponden a la etapa 4. La arquitectura inicial comparte identificación, resultados y evidencia. El significado de cada prueba pertenece a su sonda.

## Diseño, precedencia y ejecución

Se registró el protocolo inicial antes de implementar y ejecutar sus casos. SHA-256 del bloque de protocolo, desde el título hasta su salto final: `877630fc82fbf3470867514a50675677df110d7d4d769a4fee0f2dd62bf3b04a`.

## Protocolo previo · Piloto de caracterización v0.1

Pregunta. ¿Puede un procedimiento común registrar un contraste verificable en dos familias tecnológicas conservando el criterio propio de cada dominio?

Orden de incorporación. F001 primero, TN segundo. El procedimiento común invoca un proceso, registra identidad, protocolo, entradas, evidencia observada y estado, y valida la estructura de la respuesta. Se conserva el mismo ejecutor para el segundo objeto. Cada sonda implementa su criterio de dominio.

- F001. Contrato: ordenar `[2,1]` sin excepción. Control positivo: ordenamiento de referencia de Python. Control negativo deliberado: preservar la secuencia de entrada. Candidato: implementación histórica. Registrar resultado o excepción y estado tras la llamada.
- TN. Contrato elegido para el piloto: una predicción de nivel de precio debe duplicarse si se duplica el precio de toda la entrada y las características son equivalentes. Probar T1; control positivo: fórmula de reversión con centro en media de precios, usando el alfa del candidato. Control negativo: sumar una constante de una unidad a la predicción del control positivo. Serie fija de precios: 100, 103, 99, 104, 100, 103, 99, 104, 100, 103, 99, 104, 100, 103, 99, 104, 100, 103, 99, 104, 100. Comparar las medias de log-retornos y la autocorrelación inicial, comprobar alfa positivo y usar tolerancia absoluta 1e-10 y relativa 1e-9.
- Aceptación del instrumento. En los dos candidatos, debe aceptar el positivo, detectar el negativo y registrar el caso histórico como cumple, refuta o error de sondeo. Repetir una vez. Comparar el resultado determinista y reportar tiempos de pared por separado. Los controles fallidos o una sonda inválida marcan el procedimiento como insuficiente para tomar una decisión.
- Alcance. Un caso por candidato, sin cambios a los motores. El resultado solo califica la capacidad de producir evidencia focalizada. El contrato de escala de TN es un criterio explícito del piloto, cuya aplicación como requisito general requiere una decisión de diseño.

El control suplementario de TN se fijó después de observar v1 y antes de ejecutarlo. SHA-256 del bloque suplementario: `fe98f4f0fa28ab2e6d6e7f02488be7c081ce22b20e93468fda80c7f2229ed6ca`.

### Contraste suplementario · TN-escala-v2

Motivo. El caso v1 conservó la escala con un retorno medio prácticamente nulo, aun cuando T1 produjo un nivel negativo. Para comprobar sensibilidad al término sospechoso se conserva v1 y se cambia únicamente el último dato base de 100 a 102 en v2. Se mantienen factor, controles y tolerancias. Se exige media de log-retornos distinta de cero, alfa positivo, positivo aceptado y negativo detectado. Por inspección de T1, si μ es invariante a escala y no nulo, la diferencia entre la predicción con precios duplicados y el doble de la predicción original es −(1+α)μ. Un desacuerdo fuera de tolerancia refuta la equivarianza en ese caso. Esta intervención se decide tras observar v1 y precede a la nueva corrida.

### Resultados

| Caso | Observación | Decisión técnica |
| --- | --- | --- |
| **F001-partición-v1** | Positivo aceptado y negativo detectado. La revisión histórica transforma `[2,1]` en `[1,2]` y lanza `AssertionError` por índices inválidos. Registro `refuta`. | Conservar la excepción y el estado resultante. Comprobar solo la secuencia final habría dejado pasar este fallo. |
| **TN-escala-v1** | Positivo aceptado y negativo detectado. T1 devuelve −93,3490714872 y −186,6981429745, en proporción 1:2. La media de log-retornos es aproximadamente cero. Registro `cumple` para la propiedad de escala en el caso. | La primera prueba es insuficiente para detectar la mezcla de unidades conocida. El término de centro queda prácticamente anulado. |
| **TN-escala-v2** | Positivo aceptado y negativo detectado. T1 devuelve −95,6673423820 y −191,3366035733. El doble esperado es −191,3346847641. La diferencia es aproximadamente −0,0019188092. Registro `refuta`. | El control con media no nula discrimina la mezcla de unidades bajo el requisito de escala del piloto. No se acepta v1 como prueba suficiente por sí sola. |
| **Instrumentación inválida** | Una respuesta vacía en estructura devuelve `error_de_sondeo` y código 1. Un import duplicado durante la incorporación de TN también se registró como error de sondeo. | Mantener separados un fallo del instrumento y un contraejemplo del candidato. |

La fórmula de T1 es `(1+α)μ−αP`. Si la escala cambia de P a 2P y Γ conserva μ y α, la diferencia es `−(1+α)μ`. Esto explica tanto el cumplimiento de v1 como el incumplimiento de v2. La prueba local contrasta la sonda con la deducción. El control de centro en unidades de precio solo sirve como referencia dimensional en este piloto. Su desempeño predictivo queda **NO EVALUADO**.

Se verificó el blob del Python histórico y el de los nueve módulos del motor TN contra sus revisiones de GitHub. Se usó el mismo ejecutor Python en ambos candidatos, con el mismo SHA-256 `d09832a5d11053b8338ffbcc3bd926d1614781df344fcb2ed50253971c19c005`. El adaptador de TN reutiliza el cargador del [arnés de TN-R01](https://github.com/ksgfin8-cyber/tn-ea/blob/ceaf934/docs/research/tn_r01.mjs). Registra evidencia bajo esa ruta de carga de Node, cuyo alcance es distinto de una compilación independiente.

### Coste observado del piloto

| Medición | Observación |
| --- | --- |
| Sonda F001 | 38 líneas. Dos ejecuciones entre 0,048 y 0,067 s. |
| Sonda TN | 74 líneas finales, incluido el cargador reutilizado. Las dos ejecuciones v2 tomaron 0,194–0,206 s. |
| Incorporación y refinamiento de TN | 49 s de reloj entre la primera doble corrida válida de F001 y el cierre de v2. El intervalo incluye lectura, adaptación, un fallo de sondeo, ajuste del caso y ejecución. No representa tiempo humano activo ni beneficio frente a un proceso de referencia. |
| Ejecutor compartido | 65 líneas, mismo contenido en ambas incorporaciones. |

## Reproducción

Usar Python 3.12.14 y Node 24.22.3. Preparar los objetos de origen mediante dos checkouts. Los comandos presuponen los repositorios fuente en directorios hermanos del checkout de `engineering-knowledge` y generan registros temporales.

```sh
cd engineering-knowledge
set -eu
tmp=$(mktemp -d)
f001_ref=23e40279d05774d147995a620678cdc62976dda3
tn_ref=4217f70e2a140d03746873183dad5328a65e1fba
git -C ../f001 show "${f001_ref}:f001_code" > "$tmp/f001_code"
git -C ../tn-ea archive "$tn_ref" src/engine | tar -x -C "$tmp"
for run in 1 2; do
  python3 instrumentos/caracterizacion/ejecutar.py --candidate F001 --revision "$f001_ref" --protocol F001-particion-v1 -- python3 -B instrumentos/caracterizacion/f001.py "$tmp/f001_code" > "$tmp/f001-$run.json"
  python3 instrumentos/caracterizacion/ejecutar.py --candidate TN-T1 --revision "$tn_ref" --protocol TN-escala-v1 -- node --disable-warning=ExperimentalWarning instrumentos/caracterizacion/tn.mjs "$tmp/src/engine" > "$tmp/tn-v1-$run.json"
  python3 instrumentos/caracterizacion/ejecutar.py --candidate TN-T1 --revision "$tn_ref" --protocol TN-escala-v2 -- node --disable-warning=ExperimentalWarning instrumentos/caracterizacion/tn.mjs "$tmp/src/engine" shifted > "$tmp/tn-v2-$run.json"
done
for case in f001 tn-v1 tn-v2; do
  cmp "$tmp/$case-1.json" "$tmp/$case-2.json"
  sha256sum "$tmp/$case-1.json"
done
```

Los registros repetidos durante el piloto coincidieron byte a byte. SHA-256 de F001: `0a9f033894f1326dacadc640d2c884dc0c493ad124774dfba91f31bd161c8091`. TN v1: `e0e389811fd02995f1a53f160d07076c7ff020814a89ccfd3bc80e4b55f7fc1d`. TN v2: `f5b1e71c2bda5d9a2c6f64680a4bb71f80eefafcdb66b0d9d58aae0b816a2119`.

## Cierre de esta etapa

Se recomienda conservar el ejecutor como **instrumento experimental inicial**. El piloto ejercitó el uso del catálogo, respondió una pregunta sobre infraestructura y expuso una prueba que tenía controles correctos y aun así era insuficiente para su objetivo. El siguiente uso de mayor valor es una decisión prospectiva en una construcción tecnológica, con criterio discriminativo fijado antes de ampliar el prototipo. Ampliar infraestructura después de medir el coste y la calidad de ese uso.

Fuentes de referencia: [F001-R01](https://github.com/ksgfin8-cyber/f001/blob/2b60f32/docs/research/F001_RDL_PB_001_EVALUATION.md) · [Réplica TN-R01](https://github.com/ksgfin8-cyber/tn-ea/blob/ee49ac7/docs/research/TN_R01_REPLICATION.md) · [LAB2-R01](https://github.com/ksgfin8-cyber/LAB2/blob/0c21d18/docs/research/LAB2_RDL_PB_001_EVALUATION.md) · [Acta operacional de WORLD-LAB](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08/docs/audits/WORLD_LAB_OPERATIONAL_FREEZE.md).

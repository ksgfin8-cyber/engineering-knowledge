# Especialización del banco de evidencia R01

## Ficha previa · RDL-PB-001 v0.1

**Identidad y procedencia.** R01, consumidor nuevo de confirmaciones para abrir una revisión interna de un lote documental. Responsable del ensayo y la ficha: Codex. Base `736bbd01e7cd211ca4ac9b46d45ddbde20194484`. Se recupera la ficha de memoria y abstención de `disenos/siguiente-generacion/BANCO_DE_EVIDENCIA.md` en esa base, sin reutilizar código histórico. LAB2 observó que una consulta duplicada descartada por persistencia ya había cambiado el tick, la frecuencia y el historial de memoria. Se reutiliza el orden causal de ese contraejemplo, con otro dominio y otro estado. [Plano del banco](../../disenos/siguiente-generacion/BANCO_DE_EVIDENCIA.md) · [LAB2-R01, revisión congelada](https://github.com/ksgfin8-cyber/LAB2/blob/2bd75e13c6f72a2909d5fd0a6d8aa61d0b869ae8/docs/research/LAB2_RDL_PB_001_EVALUATION.md) · [Playbook v0.1](https://github.com/ksgfin8-cyber/yellow/blob/5d40f08fbb36c5bbe075628a5b9a9078ce9c017c/docs/program/RDL-PB-001_v0.1_original_propuesta.md)

**Pregunta y decisión previa.** ¿Permite la ficha elegir en qué frontera cambia la memoria antes de desarrollar el componente? El procedimiento inicial de comparación habría ejercitado solo la salida final con dos confirmaciones distintas. La elección habría quedado sin evidencia discriminativa.

**Propiedad y dominio.** Un lote, una fuente controlada, confirmaciones válidas e identidad estable del evento subyacente dentro de ese lote y fuente. A y B son confirmaciones distintas. La segunda A es una entrega separada del mismo evento; la identidad de transporte no define una confirmación nueva. Estado inicial: contador cero y conjunto de identidades admitidas vacío. Unidad: confirmaciones únicas. Solo cuentan las identidades vistas hasta el paso, sin datos futuros. Al alcanzar dos confirmaciones se dispara la decisión lógica de abrir revisión. La decisión permanece en acción desde ese umbral. No se emiten efectos externos. Repetir una confirmación debe conservar memoria y decisión. Igualdad exacta en cada paso.

**Alternativas antes de programar.** A: deduplicar por identidad y cambiar la memoria al admitir. B: incrementar al recibir, deduplicar después y conservar el incremento aun si se descarta la entrega. En ambas el observador registra memoria y decisión después de cada paso. B es el control del defecto de transición adelantada.

**Oráculo manual independiente.** El conjunto tras A es {A}; tras repetir A sigue siendo {A}; tras B es {A,B}. Por tanto:

| Secuencia | Paso 1, memoria y decisión | Paso 2, memoria y decisión |
| --- | --- | --- |
| Una confirmación, A | 1, abstenerse | — |
| Retransmisión, A → A | 1, abstenerse | 1, abstenerse |
| Dos confirmaciones, A → B | 1, abstenerse | 2, actuar |

**Controles, aceptación y cierre.** La salida final limpia A → B debe ser actuar en ambas alternativas. El criterio discriminativo exige cotejar memoria y decisión en los cinco pasos por alternativa. A debe coincidir en todos. B debe divergir exactamente en el segundo paso de la retransmisión con 2 y actuar, aunque la admisión de esa entrega se haya descartado. Si ambas pasan el criterio discriminativo, revisar la prueba antes de concluir y preservar la corrida inicial y el cambio. Presupuesto: una propiedad, dos alternativas y tres secuencias; sin aleatoriedad ni persistencia. Cerrar después de registrar la primera divergencia, la comparación limpia y el esfuerzo de adaptación. No inferir productividad ni efectos en producción.

## Ejecución y dictamen

**Deducido.** Contar identidades admitidas conserva el estado al repetir A. La mutación al recibir aumenta el contador aunque se rechace la entrega, por lo que cruza el umbral en A → A.

**Observado.** Con Python 3.12.14, ambas alternativas terminaron A → B en «actuar». En A → A el segundo paso quedó marcado como descartado en ambas. A conservó 1 y «abstenerse». B reportó 2 y «actuar». [Traza inicial y divergencia](banco-r01/resultado.jsonl)

**Verificado.** A coincidió con los cinco pasos del oráculo. B coincidió en cuatro y divergió exactamente en el segundo paso de A → A con el estado y la decisión previstos. El arnés exige esa divergencia para que el control negativo sea válido. La prueba de salida final limpia aprobó ambas opciones. La segunda corrida reprodujo la primera byte por byte. Se mantuvieron el diseño y el oráculo registrados antes de programar.

**Decisión.** Adoptar la transición al admitir. La ficha permitió elegir la frontera de mutación antes de construir el componente. Del antecedente LAB2 se transfirió la obligación de observar la memoria después de un descarte y el orden de operaciones que sirve para inyectar el defecto. La identidad de confirmación, el contador y el umbral pertenecen al consumidor nuevo.

**Esfuerzo y aporte del oráculo.** Se adaptaron el dominio y la identidad de una ficha, se derivaron manualmente cinco pares estado/decisión repartidos en tres secuencias y se implementó un arnés sin dependencias externas. Se reutilizaron el formato y el patrón del contraejemplo, con cero cambios al plano o a LAB2 y cero iteraciones de reparación de la prueba. El oráculo fijó el paso donde debía conservarse el estado, el valor residual y la decisión esperada. La prueba limpia de salida final dejó la elección abierta. El esfuerzo se registra por artefactos y casos. La productividad, la integración y la transferencia a otro consumidor requieren una comparación de trabajo más amplia.

### Reproducción desde la raíz

```sh
set -eu
salida=$(mktemp)
trap 'rm -f -- "$salida"' EXIT
python3 -B docs/research/banco-r01/probar.py > "$salida"
cmp docs/research/banco-r01/resultado.jsonl "$salida"
```

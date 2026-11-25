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

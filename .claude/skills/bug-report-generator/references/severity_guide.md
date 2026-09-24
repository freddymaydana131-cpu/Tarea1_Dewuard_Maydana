# Guía de severidad y prioridad

La **severidad** mide el impacto técnico del defecto en el sistema.
La **prioridad** mide la urgencia con la que debe corregirse.
Son independientes: un error de ortografía en el logo de la página principal puede ser severidad Baja pero prioridad P1.

## Severidad

| Severidad | Cuándo usarla | Ejemplos |
|---|---|---|
| **Crítica** | El sistema o una función principal no se puede usar, hay pérdida o exposición de datos, o hay impacto económico directo. No existe alternativa. | La app se cierra (crash) al abrir el carrito; la tienda se congela y deja de responder; pantalla en blanco al iniciar; error 500 al pagar; cobro duplicado; se borran los datos del usuario. |
| **Alta** | Una función importante falla o da resultados incorrectos, pero el resto del sistema funciona o existe una alternativa incómoda. | El total del carrito es incorrecto; al eliminar un producto se eliminan otros; el formulario no se guarda; un botón no responde. |
| **Media** | Falla una función secundaria o el comportamiento es inconsistente, con alternativa razonable. Es el valor por defecto si no hay evidencia para otra. | El filtro por categoría ignora mayúsculas; el contador del carrito tarda en actualizarse; mensaje de error poco claro. |
| **Baja** | Problema cosmético o de texto que no afecta la funcionalidad. | Error de ortografía; texto cortado; botón desalineado; color incorrecto; tooltip faltante. |

## Prioridad

| Prioridad | Significado | Relación por defecto |
|---|---|---|
| **P1** | Corregir de inmediato, bloquea la entrega. | Crítica |
| **P2** | Corregir en el sprint actual. | Alta |
| **P3** | Planificar para un próximo sprint. | Media |
| **P4** | Corregir cuando haya tiempo. | Baja |

Quien reporta puede cambiar la prioridad si el contexto de negocio lo justifica (por ejemplo, una demo al cliente mañana).

## Cómo sugiere la severidad el script

Si el JSON **no** trae `severity`, `scripts/generate_report.py` usa `assets/severity_rules.json`:

1. Une `title + summary + actual`, lo pasa a minúsculas y le quita las tildes.
2. Revisa las reglas **en orden** (Crítica → Alta → Baja) y se queda con la primera cuyas palabras clave aparezcan.
3. Si ninguna coincide, usa la severidad por defecto (`Media`).
4. La prioridad se deriva con `priority_by_severity` si no viene en el JSON.

El reporte marca la severidad como **"(sugerida)"** y lista las palabras clave que la dispararon, para que una persona la confirme.

## Qué debe hacer el agente

- Si el usuario dice explícitamente la severidad o prioridad, ponerla en el JSON (debe ser uno de los valores permitidos).
- Si el usuario no la dice, **no inventarla**: dejar el campo fuera y que el script la sugiera.
- Si la sugerencia contradice claramente esta guía (p. ej. "crash" en un texto que habla de otro sistema), avisar al usuario en el resumen final.

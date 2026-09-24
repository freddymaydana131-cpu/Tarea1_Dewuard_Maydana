# Solucionario — Mini Tienda (solo para el presentador)

La página `demo-app/` tiene **5 errores intencionales**, uno por cada nivel de severidad, para demostrar la skill `bug-report-generator` con bugs reales.

Abrir la página:
```powershell
npm install   # solo la primera vez
npm run dev
```
→ http://localhost:5173

| # | Bug | Severidad que sugiere la skill | Causa en el código |
|---|---|---|---|
| 1 | "Vaciar carrito" congela la tienda | **Crítica / P1** | `clearCart()` asigna `cart = null` (`app.js`) |
| 2 | El total ignora la cantidad | **Alta / P2** | `reduce` suma `item.price` sin `* item.qty` |
| 3 | "Quitar" elimina otro artículo | **Alta / P2** | `cart.splice(index + 1, 1)` |
| 4 | La búsqueda distingue mayúsculas | **Media / P3** (por defecto) | `p.name.includes(query)` sin `toLowerCase()` |
| 5 | Typo "carrrito" y precio desalineado | **Baja / P4** | texto del botón + `.card.featured .price { margin-left: 60px }` |

El cupón `DESC10` (10 %) **funciona bien**: sirve para mostrar algo que no es un bug.

---

## Cómo reproducir cada bug y qué escribirle a Claude

Las frases de abajo son ejemplos de descripción informal para pegar después de `/bug-report-generator`. Contienen las palabras clave con las que la skill sugiere la severidad de la tabla.

### Bug 1 — Vaciar carrito congela la tienda (Crítica)
1. Agregar cualquier artículo.
2. Pulsar **Vaciar carrito**.
3. Resultado: la lista del carrito queda en blanco pero el total no cambia; después ningún botón "Agregar" funciona. En la consola (F12): `Cannot read properties of null`.

> en la mini tienda agregué un mouse y le di a vaciar carrito, el carrito queda en blanco pero el total sigue igual y la tienda se congela, ningún botón responde, queda sin responder hasta recargar. debería vaciarse y seguir funcionando. windows 11, chrome, http://localhost:5173. en consola sale Cannot read properties of null (reading 'length'). pasa siempre

### Bug 2 — Total incorrecto con varias unidades (Alta)
1. Pulsar 3 veces **Agregar** en "Mouse inalámbrico" (Bs 85).
2. El carrito muestra `x3 Bs 255.00` pero el subtotal/total dice **Bs 85.00**.

> agregué 3 mouses de 85 bs, la línea dice 255 pero el total dice 85, total incorrecto. debería ser 255. windows 11 chrome localhost:5173, siempre

### Bug 3 — Quitar elimina otro artículo (Alta)
1. Agregar "Mouse inalámbrico" y luego "Monitor 24"".
2. Pulsar **Quitar** en el Mouse → se elimina el Monitor.
3. Si se pulsa Quitar en el último artículo, no pasa nada.

> puse un mouse y un monitor, le di quitar al mouse y se borró el monitor, elimina otros artículos en vez del que elegí. windows 11, chrome, localhost:5173

### Bug 4 — Búsqueda sensible a mayúsculas (Media)
1. Escribir `mouse` en el buscador → "No se encontraron artículos".
2. Escribir `Mouse` → sí aparece.

> si busco mouse en minúsculas no sale nada, pero con Mouse en mayúscula sí aparece. debería encontrarlo igual. windows 11 chrome

### Bug 5 — Ortografía y desalineación (Baja)
1. Ver el catálogo: todos los botones dicen "Agregar al carrrito" (tres r).
2. En "Teclado mecánico" y "Parlante portátil" el precio está desalineado a la derecha.

> los botones dicen "agregar al carrrito" con tres r, error de ortografía. también el precio del teclado y del parlante está desalineado. windows 11 chrome

---

## Casos para probar errores de la skill
- **Falta dato obligatorio:** describir el bug 2 **sin** mencionar el sistema operativo → Claude debe preguntarlo antes de generar.
- **Dos bugs en un mensaje:** pegar las descripciones del bug 4 y el 5 juntas → Claude debe generar dos reportes.
- **Severidad indicada:** agregar "severidad media" al bug 3 → el reporte usa Media sin "(sugerida)".

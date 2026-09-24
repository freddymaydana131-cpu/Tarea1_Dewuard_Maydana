# BUG-001: [Carrito] Eliminar un producto borra también los de la misma categoría

| Campo | Valor |
|---|---|
| **ID** | BUG-001 |
| **Fecha** | 2026-09-24 |
| **Componente** | Carrito |
| **Severidad** | Alta (sugerida) |
| **Prioridad** | P2 |
| **Frecuencia** | Siempre |
| **Reportado por** | Dewuard Maydana |

## Resumen

Al quitar un producto del carrito se eliminan todos los productos que comparten su categoría, por lo que el usuario pierde artículos que sí quería comprar.

## Entorno

- **Sistema operativo:** Windows 11
- **Navegador:** Chrome 128
- **URL:** http://localhost:5173/

## Pasos para reproducir

1. Abrir la tienda en http://localhost:5173/
2. Agregar al carrito el producto "iPhone 9" (categoría smartphones)
3. Agregar al carrito el producto "Samsung Universe 9" (categoría smartphones)
4. En el panel del carrito, hacer clic en "Quitar" del producto "iPhone 9"

## Resultado esperado

Solo se elimina "iPhone 9"; "Samsung Universe 9" permanece en el carrito.

## Resultado actual

Se eliminan los dos productos y el carrito queda vacío.

## Evidencia

- capturas/carrito_vacio.png

## Clasificación

Severidad **sugerida** automáticamente por las palabras clave: 'se eliminan'. Revisar antes de enviar. Prioridad P2 derivada de la severidad.

---
_Generado con la skill `bug-report-generator`._

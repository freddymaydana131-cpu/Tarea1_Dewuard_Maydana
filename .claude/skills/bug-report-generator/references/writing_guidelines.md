# Guía de redacción de bug reports

Úsala para transformar la descripción cruda del usuario en los campos del JSON (`assets/input_schema.json`).

## title (10–120 caracteres)
- Formato: `[Componente] Qué falla + cuándo/dónde`.
- Específico y buscable. Sin opiniones ni mayúsculas gritadas.
- ✅ `[Carrito] Eliminar un producto borra todos los de la misma categoría`
- ❌ `No funciona el carrito!!!`, `Bug`, `Error urgente`

## summary (mínimo 20 caracteres)
- 1 a 3 oraciones: qué pasa, a quién afecta y por qué importa.
- No repetir los pasos.

## component
- Pantalla o módulo afectado (`Carrito`, `Login`, `Checkout`). Omitir si no se sabe.

## environment
- `os` es obligatorio. Añadir `browser`, `app_version` (versión o commit) y `url` si el usuario los menciona.
- Si el usuario no dio el sistema operativo, **preguntar** antes de generar.

## steps (mínimo 2)
- Un paso por elemento, en orden, empezando por un verbo en imperativo: "Abrir…", "Hacer clic en…", "Escribir…".
- Incluir datos concretos usados (producto, usuario de prueba, valores).
- No incluir el resultado en los pasos; va en `actual`.

## expected vs. actual
- `expected`: lo que debería pasar según el requisito o el sentido común.
- `actual`: lo que pasa realmente, con mensajes de error **textuales** entre comillas.
- Deben ser distintos; si son iguales no hay bug.

## frequency
- `Siempre`, `A veces`, `Rara vez` o `Una vez`. Omitir si no se sabe.

## evidence
- Rutas de capturas, fragmentos cortos de log, enlaces. Un elemento por evidencia.

## Qué evitar
- Inventar datos que el usuario no dio (versiones, navegador, severidad).
- Mezclar varios defectos en un solo reporte: si el usuario describe dos problemas, generar dos reportes.
- Lenguaje culpabilizador ("el dev rompió…").

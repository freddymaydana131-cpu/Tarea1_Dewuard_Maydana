---
name: bug-report-generator
description: Convierte una descripción cruda o informal de un defecto (texto suelto, pasos desordenados, logs, mensajes de error) en un bug report profesional en Markdown, validado y con severidad/prioridad sugeridas. Úsala cuando el usuario pida "redactar/armar un bug report", "documentar un defecto", "crear un ticket de bug", "pasar esto a un reporte de bug" o pegue la descripción de un problema para reportarlo a desarrollo.
---

# Bug Report Generator

Transforma la descripción de un defecto en un archivo `reports/BUG-<id>-<slug>.md` con formato estándar (resumen, entorno, pasos, esperado vs. actual, evidencia, severidad y prioridad).

Rutas (relativas a la raíz del proyecto):
- Skill: `.claude/skills/bug-report-generator/`
- Scripts: `.claude/skills/bug-report-generator/scripts/`
- Salida: `reports/`

## Flujo

### 1. Leer las referencias
Antes de estructurar nada, lee:
- `references/writing_guidelines.md` — cómo redactar cada campo.
- `references/severity_guide.md` — cuándo poner (o no) severidad y prioridad.

### 2. Estructurar el defecto en JSON
Con la descripción del usuario, crea `reports/tmp_input.json` siguiendo `assets/input_schema.json`.

Campos obligatorios: `title`, `summary`, `environment.os`, `steps` (≥ 2), `expected`, `actual`.
Opcionales: `component`, `environment.browser`, `environment.app_version`, `environment.url`, `severity`, `priority`, `frequency`, `evidence`, `reporter`.

Reglas:
- **No inventes datos.** Si falta un campo obligatorio (p. ej. el sistema operativo o el resultado esperado) y no se puede deducir con seguridad del texto, pregunta al usuario antes de seguir.
- Si el usuario no da severidad/prioridad, **omítelas**; el script las sugiere.
- Si la descripción contiene varios defectos, crea un JSON y un reporte por cada uno.

Ejemplo de JSON válido: `examples/bug_input.json` en la raíz del repositorio.

### 3. Validar
```bash
python .claude/skills/bug-report-generator/scripts/validate_input.py reports/tmp_input.json
```
- Exit `0` → continuar.
- Exit `1` → lee los mensajes `[ERROR]`, corrige el JSON (o pregunta al usuario lo que falte) y valida otra vez.
- Exit `2` → el archivo no existe o el JSON está mal formado; revisa la ruta/sintaxis.

### 4. Generar el reporte
```bash
python .claude/skills/bug-report-generator/scripts/generate_report.py reports/tmp_input.json --out reports
```
Opciones: `--id 007` (número fijo), `--date 2026-09-24`, `--force` (sobrescribir).
- Exit `0` → reporte creado; el script imprime la ruta.
- Exit `3` → ya existe un reporte con ese id; usa otro `--id` o `--force` solo si el usuario lo pide.

### 5. Responder al usuario
- Ruta del reporte generado.
- Severidad y prioridad, indicando si fueron **sugeridas** y por qué palabras clave.
- Campos opcionales que quedaron sin especificar y que convendría completar.
- Borra `reports/tmp_input.json` si el usuario no necesita conservarlo.

## Archivos de la skill
| Archivo | Uso |
|---|---|
| `scripts/validate_input.py` | Valida el JSON contra el schema. |
| `scripts/generate_report.py` | Valida, sugiere severidad, rellena la plantilla y guarda el `.md`. |
| `assets/input_schema.json` | Campos, tipos, obligatorios y valores permitidos. |
| `assets/severity_rules.json` | Palabras clave → severidad; severidad → prioridad. |
| `assets/report_template.md` | Plantilla Markdown del reporte. |
| `references/writing_guidelines.md` | Guía de redacción de cada campo. |
| `references/severity_guide.md` | Criterios de severidad y prioridad. |

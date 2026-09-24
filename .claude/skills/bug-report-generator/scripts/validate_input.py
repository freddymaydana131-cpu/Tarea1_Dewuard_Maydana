"""Valida el JSON de entrada de un bug report contra assets/input_schema.json.

Uso:
    python validate_input.py <archivo.json>

Codigos de salida:
    0  JSON valido
    1  JSON con errores de contenido (campos faltantes, tipos, valores no permitidos)
    2  Problema con el archivo (no existe, no es JSON valido) o con el schema
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_DIR / "assets" / "input_schema.json"

TYPE_NAMES = {"string": str, "list": list, "object": dict}


class InputFileError(Exception):
    """Error al leer el archivo (no existe, JSON roto). Corresponde al exit code 2."""


def configure_output():
    # La consola de Windows no siempre usa UTF-8; evita errores con tildes.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def load_json(path):
    path = Path(path)
    if not path.is_file():
        raise InputFileError(f"No se encontró el archivo: {path}")
    try:
        # utf-8-sig tolera el BOM que agrega PowerShell al guardar archivos.
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise InputFileError(f"El archivo no está en UTF-8: {path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise InputFileError(
            f"JSON mal formado en {path.name} (línea {exc.lineno}, columna {exc.colno}): {exc.msg}"
        )


def load_schema():
    return load_json(SCHEMA_PATH)


def _check_field(name, value, rules, errors):
    expected_type = TYPE_NAMES[rules["type"]]
    if not isinstance(value, expected_type):
        errors.append(f"'{name}' debe ser de tipo {rules['type']}, se recibió {type(value).__name__}.")
        return

    if rules["type"] == "string":
        stripped = value.strip()
        if rules.get("required") and not stripped:
            errors.append(f"'{name}' no puede estar vacío.")
            return
        if "min_length" in rules and len(stripped) < rules["min_length"]:
            errors.append(f"'{name}' es muy corto (mínimo {rules['min_length']} caracteres).")
        if "max_length" in rules and len(stripped) > rules["max_length"]:
            errors.append(f"'{name}' es muy largo (máximo {rules['max_length']} caracteres).")
        if "enum" in rules and value not in rules["enum"]:
            errors.append(f"'{name}' tiene un valor no permitido: '{value}'. Opciones: {', '.join(rules['enum'])}.")

    elif rules["type"] == "list":
        if "min_items" in rules and len(value) < rules["min_items"]:
            errors.append(f"'{name}' necesita al menos {rules['min_items']} elementos (tiene {len(value)}).")
        item_type = TYPE_NAMES.get(rules.get("item_type", ""), None)
        for i, item in enumerate(value, start=1):
            if item_type and not isinstance(item, item_type):
                errors.append(f"'{name}[{i}]' debe ser de tipo {rules['item_type']}.")
            elif isinstance(item, str) and not item.strip():
                errors.append(f"'{name}[{i}]' está vacío.")

    elif rules["type"] == "object":
        _check_object(value, rules.get("fields", {}), errors, [], prefix=f"{name}.")


def _check_object(data, fields, errors, warnings, prefix=""):
    for name, rules in fields.items():
        full_name = prefix + name
        if name not in data or data[name] is None:
            if rules.get("required"):
                errors.append(f"Falta el campo obligatorio '{full_name}'. {rules.get('help', '')}".strip())
            continue
        _check_field(full_name, data[name], rules, errors)

    for name in data:
        if name not in fields:
            warnings.append(f"Campo desconocido '{prefix + name}': se ignorará.")


def validate(data, schema):
    """Devuelve (errores, advertencias)."""
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["El JSON debe ser un objeto { ... } con los campos del bug."], warnings
    _check_object(data, schema["fields"], errors, warnings)
    return errors, warnings


def main(argv):
    configure_output()
    if len(argv) != 2:
        print("Uso: python validate_input.py <archivo.json>", file=sys.stderr)
        return 2
    try:
        schema = load_schema()
        data = load_json(argv[1])
    except InputFileError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data, schema)
    for warning in warnings:
        print(f"[AVISO] {warning}")
    if errors:
        print(f"[ERROR] El archivo tiene {len(errors)} problema(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"[OK] {Path(argv[1]).name} es válido.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

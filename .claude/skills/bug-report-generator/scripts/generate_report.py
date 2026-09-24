"""Genera un bug report en Markdown a partir de un JSON validado.

Uso:
    python generate_report.py <archivo.json> [--out reports] [--id 001] [--date AAAA-MM-DD] [--force]

Flujo:
    1. Valida el JSON con validate_input.py (mismo schema).
    2. Si no trae severidad, la sugiere con assets/severity_rules.json.
    3. Rellena assets/report_template.md y guarda <out>/BUG-<id>-<slug>.md

Codigos de salida:
    0  Reporte generado
    1  JSON con errores de contenido
    2  Problema con archivos (entrada, plantilla, reglas) o argumentos
    3  El reporte ya existe y no se uso --force
"""
import argparse
import datetime
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_input import (  # noqa: E402
    SKILL_DIR,
    InputFileError,
    configure_output,
    load_json,
    load_schema,
    validate,
)

TEMPLATE_PATH = SKILL_DIR / "assets" / "report_template.md"
RULES_PATH = SKILL_DIR / "assets" / "severity_rules.json"
NOT_SPECIFIED = "_No especificado_"


def normalize(text):
    """Minusculas y sin tildes, para comparar palabras clave."""
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def slugify(text, max_len=40):
    slug = re.sub(r"[^a-z0-9]+", "-", normalize(text)).strip("-")
    if len(slug) > max_len:
        # Corta en el ultimo guion para no dejar palabras a medias.
        slug = slug[:max_len + 1].rsplit("-", 1)[0]
    return slug or "bug"


def classify(data, rules):
    """Devuelve (severidad, prioridad, explicacion)."""
    if data.get("severity"):
        severity = data["severity"]
        reason = "Severidad indicada por quien reporta."
    else:
        haystack = normalize(" ".join([data["title"], data["summary"], data["actual"]]))
        severity, matched = rules["default"], []
        for rule in rules["rules"]:
            matched = [kw for kw in rule["keywords"] if normalize(kw) in haystack]
            if matched:
                severity = rule["severity"]
                break
        if matched:
            reason = (
                f"Severidad **sugerida** automáticamente por las palabras clave: "
                f"{', '.join(repr(m) for m in matched)}. Revisar antes de enviar."
            )
        else:
            reason = (
                f"Severidad **sugerida** por defecto ({severity}): no se encontraron palabras clave. "
                "Revisar antes de enviar."
            )

    if data.get("priority"):
        priority = data["priority"]
    else:
        priority = rules["priority_by_severity"][severity]
        reason += f" Prioridad {priority} derivada de la severidad."
    return severity, priority, reason


def next_id(out_dir):
    numbers = [
        int(m.group(1))
        for f in out_dir.glob("BUG-*.md")
        if (m := re.match(r"BUG-(\d+)-", f.name))
    ]
    return f"{max(numbers, default=0) + 1:03d}"


def format_environment(env):
    labels = [("os", "Sistema operativo"), ("browser", "Navegador"),
              ("app_version", "Versión de la app"), ("url", "URL")]
    return "\n".join(f"- **{label}:** {env[key]}" for key, label in labels if env.get(key))


def build_values(data, report_id, date, severity, priority, reason):
    suggested = not data.get("severity")
    return {
        "id": report_id,
        "title": data["title"].strip(),
        "date": date,
        "component": data.get("component") or NOT_SPECIFIED,
        "severity": f"{severity} (sugerida)" if suggested else severity,
        "priority": priority,
        "frequency": data.get("frequency") or NOT_SPECIFIED,
        "reporter": data.get("reporter") or NOT_SPECIFIED,
        "summary": data["summary"].strip(),
        "environment": format_environment(data["environment"]),
        "steps": "\n".join(f"{i}. {step.strip()}" for i, step in enumerate(data["steps"], start=1)),
        "expected": data["expected"].strip(),
        "actual": data["actual"].strip(),
        "evidence": "\n".join(f"- {e}" for e in data.get("evidence") or []) or "_Sin evidencia adjunta._",
        "classification": reason,
    }


def render(template, values):
    unknown = set(re.findall(r"\{\{(\w+)\}\}", template)) - set(values)
    if unknown:
        raise InputFileError(f"La plantilla tiene marcadores sin valor: {', '.join(sorted(unknown))}")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Genera un bug report en Markdown desde un JSON.")
    parser.add_argument("input", help="Archivo JSON con los datos del bug")
    parser.add_argument("--out", default="reports", help="Carpeta de salida (por defecto: reports)")
    parser.add_argument("--id", help="Número del bug, ej. 001 (por defecto: siguiente disponible)")
    parser.add_argument("--date", help="Fecha AAAA-MM-DD (por defecto: hoy)")
    parser.add_argument("--force", action="store_true", help="Sobrescribe el reporte si ya existe")
    return parser.parse_args(argv)


def main(argv):
    configure_output()
    args = parse_args(argv)

    if args.id and not re.fullmatch(r"\d{1,6}", args.id):
        print(f"[ERROR] --id debe ser numérico (ej. 001), se recibió '{args.id}'.", file=sys.stderr)
        return 2
    date = args.date or datetime.date.today().isoformat()
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        print(f"[ERROR] --date debe tener formato AAAA-MM-DD, se recibió '{date}'.", file=sys.stderr)
        return 2

    try:
        schema = load_schema()
        rules = load_json(RULES_PATH)
        data = load_json(args.input)
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    except InputFileError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print(f"[ERROR] No se encontró la plantilla: {TEMPLATE_PATH}", file=sys.stderr)
        return 2

    errors, warnings = validate(data, schema)
    for warning in warnings:
        print(f"[AVISO] {warning}")
    if errors:
        print(f"[ERROR] No se generó el reporte, el JSON tiene {len(errors)} problema(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_id = args.id.zfill(3) if args.id else next_id(out_dir)
    out_file = out_dir / f"BUG-{report_id}-{slugify(data['title'])}.md"
    if out_file.exists() and not args.force:
        print(f"[ERROR] Ya existe {out_file}. Usa --force para sobrescribirlo u otro --id.", file=sys.stderr)
        return 3

    severity, priority, reason = classify(data, rules)
    values = build_values(data, report_id, date, severity, priority, reason)
    try:
        report = render(template, values)
    except InputFileError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    out_file.write_text(report, encoding="utf-8")
    print(f"[OK] Reporte generado: {out_file}")
    print(f"     Severidad: {values['severity']} | Prioridad: {priority} | Pasos: {len(data['steps'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

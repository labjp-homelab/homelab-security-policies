"""Genera los lineamientos de seguridad (TechDocs + catálogo de Backstage) desde las políticas.

Las ValidatingPolicy de policies/kubernetes/ son la fuente única: este script no inventa nada,
solo traduce sus anotaciones a lo que leen las personas (páginas de TechDocs) y los
agentes (una entidad del catálogo por regla, que leen por el MCP de Backstage).

    uv run --with pyyaml tools/generate_guidelines.py           # escribe en la raíz del repo
    uv run --with pyyaml tools/generate_guidelines.py --check   # falla si no está al día

Salida (raíz del repo, convención de Backstage):
    catalog-info.yaml   Resource `security-guidelines` (con TechDocs) + un Resource por regla
    mkdocs.yml          sitio TechDocs
    docs/index.md       resumen de todas las reglas
    docs/<id>.md        una página por regla
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICIES = ROOT / "policies" / "kubernetes"
OWNER = "plataforma"
REPO_URL = "https://github.com/labjp-homelab/homelab-security-policies"
SYSTEM = "platform"
GUIDELINES = "security-guidelines"
HEADER = "# GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano.\n"


@dataclass(frozen=True)
class Rule:
    rule_id: str
    policy: str
    title: str
    category: str
    severity: str
    description: str
    remediation: str
    mode: str
    condition: str
    source: str

    @property
    def slug(self) -> str:
        return self.rule_id.lower()


def load_rules() -> list[Rule]:
    rules = []
    for path in sorted(POLICIES.glob("validatingpolicy-*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        meta, spec = doc["metadata"], doc["spec"]
        notes = meta.get("annotations", {})
        rules.append(
            Rule(
                rule_id=notes["security.labjp.xyz/rule-id"],
                policy=meta["name"],
                title=notes["policies.kyverno.io/title"],
                category=notes["policies.kyverno.io/category"],
                severity=notes["policies.kyverno.io/severity"],
                description=" ".join(notes["policies.kyverno.io/description"].split()),
                remediation=notes["security.labjp.xyz/remediation"].rstrip(),
                mode=", ".join(spec.get("validationActions", [])),
                condition=" ".join(spec["validations"][0]["expression"].split()),
                source=path.name,
            )
        )
    ids = [r.rule_id for r in rules]
    if len(ids) != len(set(ids)):
        sys.exit(f"IDs de regla repetidos: {ids}")
    return rules


def rule_page(rule: Rule) -> str:
    return f"""<!-- {HEADER.strip("# ").strip()} -->
# {rule.rule_id} · {rule.title}

| | |
|---|---|
| **Severidad** | {rule.severity} |
| **Categoría** | {rule.category} |
| **Modo actual** | {rule.mode} |
| **Política** | `{rule.policy}` ([`policies/kubernetes/{rule.source}`]({REPO_URL}/blob/main/policies/kubernetes/{rule.source})) |

## Por qué

{rule.description}

## Cómo cumplirla

```yaml
{rule.remediation}
```

## Qué comprueba exactamente

Expresión CEL que evalúa Kyverno sobre cada contenedor del pod:

```
{rule.condition}
```
"""


def index_page(rules: list[Rule]) -> str:
    rows = "\n".join(
        f"| [{r.rule_id}]({r.slug}.md) | {r.title} | {r.severity} | {r.mode} |" for r in rules
    )
    return f"""<!-- {HEADER.strip("# ").strip()} -->
# Lineamientos de seguridad del homelab

Cada regla es una `ValidatingPolicy` de Kyverno en [`policies/kubernetes/`]({REPO_URL}/tree/main/policies/kubernetes).
Lo que se lee aquí y lo que aplica el clúster salen del mismo archivo: si cambia la
política, cambia esta página.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
{rows}

`Audit` informa en los PolicyReports sin bloquear; `Deny` rechaza en la admisión.
"""


def mkdocs(rules: list[Rule]) -> str:
    doc = {
        "site_name": "Lineamientos de seguridad del homelab",
        "nav": [{"Resumen": "index.md"}] + [{f"{r.rule_id} · {r.title}": f"{r.slug}.md"} for r in rules],
        "plugins": ["techdocs-core"],
    }
    return HEADER + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False)


def catalog(rules: list[Rule]) -> str:
    entities = [
        {
            "apiVersion": "backstage.io/v1alpha1",
            "kind": "Resource",
            "metadata": {
                "name": GUIDELINES,
                "title": "Lineamientos de seguridad",
                "description": "Estándar de seguridad del homelab, generado desde las políticas de Kyverno.",
                "annotations": {"backstage.io/techdocs-ref": "dir:."},
                "tags": ["security", "kyverno", "guidelines"],
            },
            "spec": {"type": "security-guidelines", "owner": OWNER, "system": SYSTEM},
        }
    ]
    for r in rules:
        entities.append(
            {
                "apiVersion": "backstage.io/v1alpha1",
                "kind": "Resource",
                "metadata": {
                    "name": f"{r.slug}-{r.policy}",
                    "title": f"{r.rule_id} · {r.title}",
                    "description": r.description,
                    "annotations": {
                        "security.labjp.xyz/rule-id": r.rule_id,
                        "security.labjp.xyz/severity": r.severity,
                        "security.labjp.xyz/category": r.category,
                        "security.labjp.xyz/mode": r.mode,
                        "security.labjp.xyz/kyverno-policy": r.policy,
                        "security.labjp.xyz/condition": r.condition,
                        "security.labjp.xyz/remediation": r.remediation,
                    },
                    "tags": ["security-policy", r.severity],
                    "links": [{"url": f"/docs/default/resource/{GUIDELINES}/{r.slug}/", "title": "Lineamiento"}],
                },
                "spec": {
                    "type": "security-policy",
                    "owner": OWNER,
                    "system": SYSTEM,
                    "dependencyOf": [f"resource:{GUIDELINES}"],
                },
            }
        )
    return HEADER + "---\n".join(yaml.safe_dump(e, allow_unicode=True, sort_keys=False) for e in entities)


def render(rules: list[Rule]) -> dict[str, str]:
    files = {
        "catalog-info.yaml": catalog(rules),
        "mkdocs.yml": mkdocs(rules),
        "docs/index.md": index_page(rules),
    }
    files.update({f"docs/{r.slug}.md": rule_page(r) for r in rules})
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=ROOT, type=Path, help="por defecto, la raíz del repo")
    parser.add_argument("--check", action="store_true", help="falla si la salida no está al día")
    args = parser.parse_args()

    files = render(load_rules())
    stale = sorted(
        name
        for name, content in files.items()
        if not (args.out / name).is_file() or (args.out / name).read_text(encoding="utf-8") != content
    )
    orphans = sorted(
        str(p.relative_to(args.out)) for p in (args.out / "docs").glob("*.md") if str(p.relative_to(args.out)) not in files
    ) if (args.out / "docs").is_dir() else []

    if args.check:
        if stale or orphans:
            print("Lineamientos desactualizados; regenera con generate_guidelines.py:", *stale, *orphans, sep="\n  ")
            return 1
        print(f"Lineamientos al día ({len(files)} archivos).")
        return 0

    for name in orphans:
        (args.out / name).unlink()
    for name, content in files.items():
        target = args.out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    print(f"Escritos {len(files)} archivos en {args.out}; retirados {len(orphans)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

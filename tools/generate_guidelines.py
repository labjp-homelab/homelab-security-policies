"""Genera los lineamientos (TechDocs + catálogo de Backstage) desde las políticas.

Lee las ValidatingPolicy de policies/ (que genera vendor_policies.py desde curation.yaml) y
traduce sus anotaciones a lo que leen las personas (páginas de TechDocs, ordenadas por
categoría) y los agentes (una entidad del catálogo por regla, que leen por el MCP de
Backstage). No inventa nada: todo sale de las políticas.

    uv run --with pyyaml tools/generate_guidelines.py           # escribe en la raíz del repo
    uv run --with pyyaml tools/generate_guidelines.py --check   # falla si no está al día

Salida (raíz del repo, convención de Backstage):
    catalog-info.yaml          Resource `security-guidelines` (con TechDocs) + un Resource por regla
    mkdocs.yml                 sitio TechDocs, con el menú por categoría
    docs/index.md              resumen de todas las reglas
    docs/source-of-truth.md    de dónde sale cada cosa y quién lee qué
    docs/<categoría>/<id>.md   una página por regla
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICIES = ROOT / "policies"
OWNER = "plataforma"
SYSTEM = "platform"
GUIDELINES = "security-guidelines"
REPO_URL = "https://github.com/labjp-homelab/homelab-security-policies"
# Backstage exige URLs absolutas en metadata.links.
BACKSTAGE_URL = "https://backstage.labjp.xyz"
LABEL = "security.labjp.xyz"
HEADER = "GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano."


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    summary: str


@dataclass(frozen=True)
class Rule:
    rule_id: str
    policy: str
    category: str
    title: str
    severity: str
    rationale: str
    remediation: str
    mode: str
    resources: str
    conditions: tuple[str, ...]
    upstream: str
    source: str

    @property
    def slug(self) -> str:
        return self.rule_id.lower()

    @property
    def page(self) -> str:
        return f"{self.category}/{self.slug}.md"


def load_categories() -> list[Category]:
    curation = yaml.safe_load((ROOT / "curation.yaml").read_text(encoding="utf-8"))
    return [Category(c["id"], c["title"], " ".join(c["summary"].split())) for c in curation["categories"]]


def load_rules() -> list[Rule]:
    rules = []
    for path in sorted(POLICIES.rglob("validatingpolicy-*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        meta, spec = doc["metadata"], doc["spec"]
        notes = meta["annotations"]
        kinds = sorted({r for rule in spec["matchConstraints"]["resourceRules"] for r in rule["resources"]})
        rules.append(
            Rule(
                rule_id=notes[f"{LABEL}/rule-id"],
                policy=meta["name"],
                category=meta["labels"][f"{LABEL}/category"],
                title=notes[f"{LABEL}/title"],
                severity=notes["policies.kyverno.io/severity"],
                rationale=notes[f"{LABEL}/rationale"],
                remediation=notes[f"{LABEL}/remediation"].rstrip(),
                mode=", ".join(spec.get("validationActions", [])),
                resources=", ".join(kinds),
                conditions=tuple(" ".join(v["expression"].split()) for v in spec["validations"]),
                upstream=notes[f"{LABEL}/upstream"],
                source=str(path.relative_to(ROOT)),
            )
        )
    return rules


def rule_page(rule: Rule, category: Category) -> str:
    checks = "\n\n".join(f"```\n{c}\n```" for c in rule.conditions)
    return f"""<!-- {HEADER} -->
# {rule.rule_id} · {rule.title}

| | |
|---|---|
| **Categoría** | {category.title} |
| **Severidad** | {rule.severity} |
| **Modo actual** | {rule.mode} |
| **Se evalúa sobre** | {rule.resources} |
| **Política** | [`{rule.source}`]({REPO_URL}/blob/main/{rule.source}) |
| **Origen** | [biblioteca oficial de Kyverno]({rule.upstream}) |

## Por qué

{rule.rationale}

## Cómo cumplirla

```yaml
{rule.remediation}
```

## Qué comprueba exactamente

Expresiones CEL que evalúa Kyverno (deben cumplirse todas):

{checks}
"""


def index_page(rules: list[Rule], categories: list[Category]) -> str:
    sections = []
    for cat in categories:
        own = [r for r in rules if r.category == cat.id]
        if not own:
            continue
        rows = "\n".join(f"| [{r.rule_id}]({r.page}) | {r.title} | {r.severity} | {r.mode} |" for r in own)
        sections.append(f"## {cat.title}\n\n{cat.summary}\n\n| ID | Regla | Severidad | Modo |\n|----|-------|-----------|------|\n{rows}")
    body = "\n\n".join(sections)
    return f"""<!-- {HEADER} -->
# Lineamientos de seguridad del homelab

{len(rules)} reglas, cada una una `ValidatingPolicy` de Kyverno en
[`policies/`]({REPO_URL}/tree/main/policies), basada en la biblioteca oficial de Kyverno. Lo
que se lee aquí y lo que aplica el clúster salen del mismo archivo (ver
[Fuente de verdad](source-of-truth.md)).

`Audit` informa en los PolicyReports sin bloquear; `Deny` rechaza en la admisión.

{body}
"""


def source_of_truth_page() -> str:
    return f"""<!-- {HEADER} -->
# Fuente de verdad

**La fuente de verdad son las políticas de Kyverno de [`homelab-security-policies`]({REPO_URL})**,
en `policies/`. Todo lo demás se deriva de ellas; nada se escribe aparte.

```
biblioteca oficial de Kyverno (github.com/kyverno/policies, commit fijado)
        │  curation.yaml: qué reglas adoptamos + ID, categoría, textos, casos de prueba
        ▼  tools/vendor_policies.py
policies/<categoría>/validatingpolicy-<id>-<nombre>.yaml   ◀── FUENTE DE VERDAD
        │
        ├──▶ Argo CD del homelab: las aplica en el clúster (tag fijado, modo Audit)
        ├──▶ tests/kubernetes: kyverno test (cada regla con su caso que cumple y el que no)
        ├──▶ pipelines: kyverno apply antes del build (shift-left)
        └──▶ tools/generate_guidelines.py
                ├─ docs/ + mkdocs.yml   ──▶ TechDocs en Backstage (personas)
                └─ catalog-info.yaml    ──▶ catálogo de Backstage, una entidad por regla
                                              └──▶ agentes A2A, por el MCP de Backstage
```

| Quién | Lee | Por qué así |
|-------|-----|-------------|
| Kyverno (clúster) | las políticas, por Argo CD | es lo que de verdad se aplica |
| Personas | estas páginas (TechDocs) | explicación, remedio y la expresión exacta |
| Agentes A2A | la entidad de la regla, por el MCP de Backstage | leen la regla y su condición, no la prosa: un texto alterado no cambia lo que recomiendan |

## Cambiar una regla

1. Editar `curation.yaml` (adoptar o retirar una regla, sus textos o sus casos de prueba).
2. `tools/vendor_policies.py` regenera `policies/` y el test; `kyverno test tests/kubernetes`.
3. `tools/generate_guidelines.py` regenera estas páginas y el catálogo.
4. Publicar un tag; el homelab lo adopta cambiando `targetRevision` de su Application.
"""


def mkdocs(rules: list[Rule], categories: list[Category]) -> str:
    nav: list[dict] = [{"Resumen": "index.md"}, {"Fuente de verdad": "source-of-truth.md"}]
    for cat in categories:
        own = [r for r in rules if r.category == cat.id]
        if own:
            nav.append({cat.title: [{f"{r.rule_id} · {r.title}": r.page} for r in own]})
    doc = {"site_name": "Lineamientos de seguridad del homelab", "nav": nav, "plugins": ["techdocs-core"]}
    return f"# {HEADER}\n" + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False)


def catalog(rules: list[Rule], categories: list[Category]) -> str:
    titles = {c.id: c.title for c in categories}
    entities = [
        {
            "apiVersion": "backstage.io/v1alpha1",
            "kind": "Resource",
            "metadata": {
                "name": GUIDELINES,
                "title": "Lineamientos de seguridad",
                "description": "Estándar de seguridad del homelab: políticas de Kyverno, fuente única de los lineamientos.",
                "annotations": {"backstage.io/techdocs-ref": "dir:."},
                "tags": ["security", "kyverno", "guidelines"],
                "links": [{"url": REPO_URL, "title": "Repo (fuente de verdad)"}],
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
                    "description": r.rationale,
                    "annotations": {
                        f"{LABEL}/rule-id": r.rule_id,
                        f"{LABEL}/category": r.category,
                        f"{LABEL}/severity": r.severity,
                        f"{LABEL}/mode": r.mode,
                        f"{LABEL}/kyverno-policy": r.policy,
                        f"{LABEL}/applies-to": r.resources,
                        f"{LABEL}/conditions": "\n".join(r.conditions),
                        f"{LABEL}/remediation": r.remediation,
                        f"{LABEL}/source": f"{REPO_URL}/blob/main/{r.source}",
                    },
                    "tags": ["security-policy", r.category, r.severity],
                    "links": [
                        {
                            "url": f"{BACKSTAGE_URL}/docs/default/resource/{GUIDELINES}/{r.category}/{r.slug}/",
                            "title": "Lineamiento",
                        },
                        {"url": f"{REPO_URL}/blob/main/{r.source}", "title": f"Política ({titles[r.category]})"},
                    ],
                },
                "spec": {
                    "type": "security-policy",
                    "owner": OWNER,
                    "system": SYSTEM,
                    "dependencyOf": [f"resource:{GUIDELINES}"],
                },
            }
        )
    return f"# {HEADER}\n" + "---\n".join(yaml.safe_dump(e, allow_unicode=True, sort_keys=False) for e in entities)


def render() -> dict[str, str]:
    categories, rules = load_categories(), load_rules()
    ids = [r.rule_id for r in rules]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"IDs de regla repetidos: {ids}")
    by_id = {c.id: c for c in categories}
    files = {
        "catalog-info.yaml": catalog(rules, categories),
        "mkdocs.yml": mkdocs(rules, categories),
        "docs/index.md": index_page(rules, categories),
        "docs/source-of-truth.md": source_of_truth_page(),
    }
    files.update({f"docs/{r.page}": rule_page(r, by_id[r.category]) for r in rules})
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="falla si los lineamientos no están al día")
    args = parser.parse_args()

    files = render()
    docs = ROOT / "docs"
    existing = {str(p.relative_to(ROOT)) for p in docs.rglob("*.md")} if docs.is_dir() else set()
    orphans = sorted(existing - files.keys())
    stale = sorted(n for n, c in files.items() if not (ROOT / n).is_file() or (ROOT / n).read_text(encoding="utf-8") != c)

    if args.check:
        if stale or orphans:
            print("Lineamientos desactualizados; regenera con tools/generate_guidelines.py:", *stale, *orphans, sep="\n  ")
            return 1
        print(f"Lineamientos al día ({len(files)} archivos).")
        return 0

    for name in orphans:
        (ROOT / name).unlink()
    for name, content in files.items():
        (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / name).write_text(content, encoding="utf-8")
    for directory in sorted(docs.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    print(f"Escritos {len(files)} archivos; retirados {len(orphans)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Genera los lineamientos (TechDocs + catálogo de Backstage) desde las políticas.

Lee las ValidatingPolicy de policies/ (que genera vendor_policies.py desde curation.yaml) y
traduce sus anotaciones a lo que leen las personas (páginas de TechDocs, ordenadas por
categoría) y los agentes (una entidad del catálogo por regla, que leen por el MCP de
Backstage). No inventa nada: todo sale de las políticas.

    uv run --with pyyaml tools/generate_guidelines.py           # escribe en la raíz del repo
    uv run --with pyyaml tools/generate_guidelines.py --check   # falla si no está al día

Los marcos de referencia (OWASP Kubernetes, LLM y MCP Top 10, PCI DSS) se definen a mano en
frameworks/: sus puntos, su estado y lo que los cubre fuera de Kyverno. Qué reglas cubren
cada punto sale de las anotaciones de las políticas.

Salida (raíz del repo, convención de Backstage):
    catalog-info.yaml          Resource `security-guidelines` (con TechDocs), uno por marco y uno por regla
    mkdocs.yml                 sitio TechDocs, con el menú por categoría
    docs/index.md              resumen de todas las reglas
    docs/source-of-truth.md    de dónde sale cada cosa y quién lee qué
    docs/<categoría>/<id>.md   una página por regla
    docs/frameworks/<marco>.md una página por marco, con su matriz de cobertura
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICIES = ROOT / "policies"
FRAMEWORKS = ROOT / "frameworks"
OWNER = "plataforma"
SYSTEM = "seguridad"  # System del catálogo del homelab (domain platform), junto a kyverno
GUIDELINES = "security-guidelines"
REPO_URL = "https://github.com/labjp-homelab/homelab-security-policies"
# Backstage exige URLs absolutas en metadata.links.
BACKSTAGE_URL = "https://backstage.labjp.xyz"
LABEL = "security.labjp.xyz"
HEADER = "GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano."
STATUS = {"cubierto": "Cubierto", "parcial": "Parcial", "pendiente": "Pendiente", "no-aplica": "No aplica"}


@dataclass(frozen=True)
class FrameworkItem:
    id: str
    title: str
    status: str
    homelab: tuple[str, ...]


@dataclass(frozen=True)
class Framework:
    id: str
    title: str
    edition: str
    url: str
    items: tuple[FrameworkItem, ...]

    @property
    def page(self) -> str:
        return f"frameworks/{self.id}.md"

    @property
    def entity(self) -> str:
        return f"framework-{self.id}"

    @property
    def name(self) -> str:
        return f"{self.title} {self.edition}"


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
    frameworks: tuple[tuple[str, tuple[str, ...]], ...] = ()

    @property
    def slug(self) -> str:
        return self.rule_id.lower()

    @property
    def page(self) -> str:
        return f"{self.category}/{self.slug}.md"


def load_categories() -> list[Category]:
    curation = yaml.safe_load((ROOT / "curation.yaml").read_text(encoding="utf-8"))
    return [Category(c["id"], c["title"], " ".join(c["summary"].split())) for c in curation["categories"]]


def load_frameworks() -> list[Framework]:
    frameworks = []
    for path in sorted(FRAMEWORKS.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        items = []
        for item in doc["items"]:
            if item["status"] not in STATUS:
                raise SystemExit(f"{doc['id']} {item['id']}: estado {item['status']!r} no es {', '.join(STATUS)}")
            items.append(FrameworkItem(str(item["id"]), item["title"], item["status"], tuple(item.get("homelab") or ())))
        frameworks.append(Framework(doc["id"], doc["title"], str(doc["edition"]), doc["url"], tuple(items)))
    return frameworks


def load_rules(frameworks: list[Framework]) -> list[Rule]:
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
                frameworks=tuple(
                    (fw.id, tuple(i.strip() for i in notes[f"{LABEL}/{fw.id}"].split(",")))
                    for fw in frameworks
                    if f"{LABEL}/{fw.id}" in notes
                ),
            )
        )
    return rules


def covering(rules: list[Rule], framework: Framework, item: FrameworkItem) -> list[Rule]:
    return [r for r in rules if item.id in dict(r.frameworks).get(framework.id, ())]


def check_coverage(rules: list[Rule], frameworks: list[Framework]) -> None:
    """El estado declarado a mano no puede contradecir lo que dicen las políticas."""
    for fw in frameworks:
        for item in fw.items:
            own = covering(rules, fw, item)
            if item.status == "pendiente" and own:
                raise SystemExit(f"{fw.id} {item.id}: 'pendiente' pero lo cubren {', '.join(r.rule_id for r in own)}")
            if item.status in ("cubierto", "parcial") and not own and not item.homelab:
                raise SystemExit(f"{fw.id} {item.id}: '{item.status}' sin reglas ni controles del homelab")


def rule_page(rule: Rule, category: Category, frameworks: list[Framework]) -> str:
    checks = "\n\n".join(f"```\n{c}\n```" for c in rule.conditions)
    by_id = {fw.id: fw for fw in frameworks}
    marcos = "<br>".join(
        f"[{by_id[fid].name}](../{by_id[fid].page}): {', '.join(ids)}" for fid, ids in rule.frameworks
    ) or "—"
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
| **Marcos de referencia** | {marcos} |

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


def framework_page(framework: Framework, rules: list[Rule]) -> str:
    rows = []
    for item in framework.items:
        own = covering(rules, framework, item)
        kyverno = ", ".join(f"[{r.rule_id}](../{r.page})" for r in own) or "—"
        homelab = "<br>".join(item.homelab) or "—"
        rows.append(f"| **{item.id}** | {item.title} | {STATUS[item.status]} | {kyverno} | {homelab} |")
    counts = ", ".join(
        f"{sum(i.status == s for i in framework.items)} {label.lower()}" for s, label in STATUS.items()
    )
    return f"""<!-- {HEADER} -->
# {framework.name}

Referencia oficial: <{framework.url}>

Cobertura en el homelab: {counts}.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `{LABEL}/{framework.id}`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`frameworks/{framework.id}.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno | Otros controles del homelab |
|----|--------|--------|-------------------|-----------------------------|
{chr(10).join(rows)}
"""


def index_page(rules: list[Rule], categories: list[Category], frameworks: list[Framework]) -> str:
    sections = []
    for cat in categories:
        own = [r for r in rules if r.category == cat.id]
        if not own:
            continue
        rows = "\n".join(f"| [{r.rule_id}]({r.page}) | {r.title} | {r.severity} | {r.mode} |" for r in own)
        sections.append(f"## {cat.title}\n\n{cat.summary}\n\n| ID | Regla | Severidad | Modo |\n|----|-------|-----------|------|\n{rows}")
    body = "\n\n".join(sections)
    marcos = "\n".join(
        f"| [{fw.name}]({fw.page}) | "
        + " | ".join(str(sum(i.status == s for i in fw.items)) for s in STATUS)
        + " |"
        for fw in frameworks
    )
    return f"""<!-- {HEADER} -->
# Lineamientos de seguridad del homelab

{len(rules)} reglas, cada una una `ValidatingPolicy` de Kyverno en
[`policies/`]({REPO_URL}/tree/main/policies), basada en la biblioteca oficial de Kyverno. Lo
que se lee aquí y lo que aplica el clúster salen del mismo archivo (ver
[Fuente de verdad](source-of-truth.md)).

`Audit` informa en los PolicyReports sin bloquear; `Deny` rechaza en la admisión.

## Marcos de referencia

Qué cubre el homelab de cada marco, con estas reglas y con otros controles (Keycloak,
OpenBao, Kuadrant, agentgateway...). El detalle de cada punto, en su página.

| Marco | Cubierto | Parcial | Pendiente | No aplica |
|-------|----------|---------|-----------|-----------|
{marcos}

{body}
"""


def source_of_truth_page() -> str:
    return f"""<!-- {HEADER} -->
# Fuente de verdad

**La fuente de verdad son las políticas de Kyverno de [`homelab-security-policies`]({REPO_URL})**,
en `policies/`. Todo lo demás se deriva de ellas; nada se escribe aparte.

```
biblioteca oficial de Kyverno (github.com/kyverno/policies, commit fijado)
        │  curation.yaml: qué reglas adoptamos + ID, categoría, textos, marcos, casos de prueba
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

frameworks/<marco>.yaml (a mano): puntos de OWASP Kubernetes, LLM y MCP Top 10 y PCI DSS,
su estado y lo que los cubre fuera de Kyverno ──▶ una página y una entidad por marco
```

| Quién | Lee | Por qué así |
|-------|-----|-------------|
| Kyverno (clúster) | las políticas, por Argo CD | es lo que de verdad se aplica |
| Personas | estas páginas (TechDocs) | explicación, remedio y la expresión exacta |
| Agentes A2A | la entidad de la regla, por el MCP de Backstage | leen la regla y su condición, no la prosa: un texto alterado no cambia lo que recomiendan |

## Cambiar una regla

1. Editar `curation.yaml` (adoptar o retirar una regla, sus textos, sus marcos o sus casos
   de prueba) o `frameworks/` (estado de un punto y lo que lo cubre fuera de Kyverno).
2. `tools/vendor_policies.py` regenera `policies/` y el test; `kyverno test tests/kubernetes`.
3. `tools/generate_guidelines.py` regenera estas páginas y el catálogo.
4. Publicar un tag; el homelab lo adopta cambiando `targetRevision` de su Application.
"""


def mkdocs(rules: list[Rule], categories: list[Category], frameworks: list[Framework]) -> str:
    nav: list[dict] = [
        {"Resumen": "index.md"},
        {"Fuente de verdad": "source-of-truth.md"},
        {"Marcos de referencia": [{fw.name: fw.page} for fw in frameworks]},
    ]
    for cat in categories:
        own = [r for r in rules if r.category == cat.id]
        if own:
            nav.append({cat.title: [{f"{r.rule_id} · {r.title}": r.page} for r in own]})
    doc = {"site_name": "Lineamientos de seguridad del homelab", "nav": nav, "plugins": ["techdocs-core"]}
    return f"# {HEADER}\n" + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False)


def catalog(rules: list[Rule], categories: list[Category], frameworks: list[Framework]) -> str:
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
    for fw in frameworks:
        entities.append(
            {
                "apiVersion": "backstage.io/v1alpha1",
                "kind": "Resource",
                "metadata": {
                    "name": fw.entity,
                    "title": fw.name,
                    "description": f"Cobertura del homelab frente a {fw.name}: reglas de Kyverno y otros controles.",
                    "annotations": {
                        f"{LABEL}/framework": fw.id,
                        **{
                            f"{LABEL}/{s}": ", ".join(i.id for i in fw.items if i.status == s) or "-"
                            for s in STATUS
                        },
                    },
                    "tags": ["security", "framework"],
                    "links": [
                        {
                            "url": f"{BACKSTAGE_URL}/docs/default/resource/{GUIDELINES}/frameworks/{fw.id}/",
                            "title": "Cobertura",
                        },
                        {"url": fw.url, "title": "Referencia oficial"},
                    ],
                },
                "spec": {
                    "type": "security-framework",
                    "owner": OWNER,
                    "system": SYSTEM,
                    "dependencyOf": [f"resource:{GUIDELINES}"],
                },
            }
        )
    by_id = {fw.id: fw for fw in frameworks}
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
                        **{f"{LABEL}/{fid}": ", ".join(ids) for fid, ids in r.frameworks},
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
                    "dependencyOf": [f"resource:{GUIDELINES}"]
                    + [f"resource:{by_id[fid].entity}" for fid, _ in r.frameworks],
                },
            }
        )
    return f"# {HEADER}\n" + "---\n".join(yaml.safe_dump(e, allow_unicode=True, sort_keys=False) for e in entities)


def render() -> dict[str, str]:
    categories, frameworks = load_categories(), load_frameworks()
    rules = load_rules(frameworks)
    check_coverage(rules, frameworks)
    ids = [r.rule_id for r in rules]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"IDs de regla repetidos: {ids}")
    by_id = {c.id: c for c in categories}
    files = {
        "catalog-info.yaml": catalog(rules, categories, frameworks),
        "mkdocs.yml": mkdocs(rules, categories, frameworks),
        "docs/index.md": index_page(rules, categories, frameworks),
        "docs/source-of-truth.md": source_of_truth_page(),
    }
    files.update({f"docs/{r.page}": rule_page(r, by_id[r.category], frameworks) for r in rules})
    files.update({f"docs/{fw.page}": framework_page(fw, rules) for fw in frameworks})
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

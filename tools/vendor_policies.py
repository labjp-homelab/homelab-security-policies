"""Genera policies/ y tests/kubernetes/kyverno-test.yaml desde curation.yaml.

Toma cada política de la biblioteca oficial de Kyverno (fijada a un commit en
curation.yaml), conserva su lógica y le añade nuestra capa: ID, categoría, título, por qué y
remedio en español, modo Audit y el ID delante de cada mensaje. Así seguimos alineados con
Kyverno: actualizar es cambiar `upstream.ref` y volver a generar.

    uv run --with pyyaml tools/vendor_policies.py           # escribe
    uv run --with pyyaml tools/vendor_policies.py --check   # falla si no está al día
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICIES = ROOT / "policies"
TESTS = ROOT / "tests" / "kubernetes"
CACHE = ROOT / ".cache" / "upstream"
GENERATED = "# GENERADO por tools/vendor_policies.py desde curation.yaml. No editar a mano.\n"
STANDARD = "homelab-baseline"
LABEL = "security.labjp.xyz"


class _Dumper(yaml.SafeDumper):
    """YAML legible: textos de varias líneas como bloque `|`."""


def _str(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(str, _str)


def dump(doc: Any) -> str:
    return yaml.dump(doc, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=100)


def fetch(repo: str, ref: str, path: str) -> dict[str, Any]:
    cached = CACHE / ref / path
    if not cached.is_file():
        raw = repo.replace("https://github.com/", "https://raw.githubusercontent.com/")
        with urllib.request.urlopen(f"{raw}/{ref}/{path}", timeout=30) as response:  # noqa: S310 - URL fija de curation.yaml
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(response.read())
    return yaml.safe_load(cached.read_text(encoding="utf-8"))


def build_policy(rule: dict[str, Any], category: dict[str, Any], upstream: dict[str, Any]) -> dict[str, Any]:
    doc = fetch(upstream["repo"], upstream["ref"], rule["upstream"])
    meta, spec = doc["metadata"], doc["spec"]
    meta["labels"] = {**meta.get("labels", {}), f"{LABEL}/standard": STANDARD, f"{LABEL}/category": category["id"]}
    meta["annotations"] = {
        **meta.get("annotations", {}),
        "policies.kyverno.io/severity": rule["severity"],
        f"{LABEL}/rule-id": rule["id"],
        f"{LABEL}/title": rule["title"],
        f"{LABEL}/rationale": " ".join(rule["rationale"].split()),
        f"{LABEL}/remediation": rule["remediation"].rstrip() + "\n",
        f"{LABEL}/upstream": f"{upstream['repo']}/blob/{upstream['ref']}/{rule['upstream']}",
    }
    for key, value in rule.get("override", {}).items():
        spec[key] = value
    if "override" in rule:
        # La descripción original describe el ejemplo de la biblioteca, no nuestra versión.
        meta["annotations"]["policies.kyverno.io/description"] = (
            "Customized from the Kyverno library policy (see security.labjp.xyz/upstream): "
            + " ".join(rule["rationale"].split())
        )
    # Nada bloquea todavía: todo informa en los PolicyReport (decisión del 3 oct 2026).
    spec["validationActions"] = ["Audit"]
    spec["evaluation"] = {"background": {"enabled": True}}
    for validation in spec["validations"]:
        if "message" in validation:
            validation["message"] = f"[{rule['id']}] " + " ".join(validation["message"].split())
        if "messageExpression" in validation:
            validation["messageExpression"] = f"'[{rule['id']}] ' + " + validation["messageExpression"]
    return doc


def policy_file(rule: dict[str, Any], category: dict[str, Any], name: str) -> str:
    return f"{category['dir']}/validatingpolicy-{rule['id'].lower()}-{name}.yaml"


def render(curation: dict[str, Any]) -> dict[str, str]:
    upstream = curation["upstream"]
    categories = {c["id"]: c for c in curation["categories"]}
    files: dict[str, str] = {}
    by_dir: dict[str, list[str]] = {}
    seen: set[str] = set()
    for rule in curation["rules"]:
        if rule["id"] in seen:
            sys.exit(f"ID repetido: {rule['id']}")
        seen.add(rule["id"])
        category = categories[rule["category"]]
        doc = build_policy(rule, category, upstream)
        path = policy_file(rule, category, doc["metadata"]["name"])
        header = (
            f"# {rule['id']} · {rule['title']}\n"
            f"# Origen: kyverno/policies@{upstream['ref'][:12]} {rule['upstream']} (Apache-2.0).\n"
            f"# Lógica de Kyverno{' con override (ver curation.yaml)' if 'override' in rule else ' sin cambios'};"
            " añadidos: ID, categoría, textos, modo Audit.\n"
        )
        files[f"policies/{path}"] = GENERATED + header + dump(doc)
        by_dir.setdefault(category["dir"], []).append(Path(path).name)
    for directory, names in by_dir.items():
        files[f"policies/{directory}/kustomization.yaml"] = GENERATED + dump(
            {"apiVersion": "kustomize.config.k8s.io/v1beta1", "kind": "Kustomization", "resources": sorted(names)}
        )
    files["policies/kustomization.yaml"] = GENERATED + (
        "# Todo el estándar. Lo aplica Argo CD (Application homelab-security-policies).\n"
    ) + dump(
        {
            "apiVersion": "kustomize.config.k8s.io/v1beta1",
            "kind": "Kustomization",
            "resources": [c["dir"] for c in curation["categories"] if c["dir"] in by_dir],
        }
    )
    files["tests/kubernetes/kyverno-test.yaml"] = GENERATED + render_test(curation, files)
    return files


def render_test(curation: dict[str, Any], files: dict[str, str]) -> str:
    resources = {
        doc["metadata"]["name"]: doc
        for doc in yaml.safe_load_all((TESTS / "resources.yaml").read_text(encoding="utf-8"))
        if doc and doc["kind"] != "Namespace"
    }
    policy_paths = sorted(p for p in files if p.startswith("policies/") and "/validatingpolicy-" in p)
    names = {yaml.safe_load(files[p].split("\n", 3)[-1])["metadata"]["annotations"][f"{LABEL}/rule-id"]: p for p in policy_paths}
    results = []
    for rule in curation["rules"]:
        policy = yaml.safe_load(files[names[rule["id"]]].split("\n", 3)[-1])["metadata"]["name"]
        for outcome in ("pass", "fail"):
            for name in rule["tests"][outcome]:
                res = resources[name]
                ns = res["metadata"].get("namespace")
                results.append(
                    {
                        "policy": policy,
                        "kind": res["kind"],
                        "resources": [f"{ns}/{name}" if ns else name],
                        "result": outcome,
                    }
                )
    test = {
        "apiVersion": "cli.kyverno.io/v1alpha1",
        "kind": "Test",
        "metadata": {"name": STANDARD},
        "policies": [f"../../{p}" for p in policy_paths],
        "resources": ["resources.yaml"],
        # namespaceObject (WKL-003): namespaces simulados.
        "variables": "values.yaml",
        "results": results,
    }
    return "# kyverno test tests/kubernetes: cada regla con su caso que cumple y el que no.\n" + dump(test)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="falla si policies/ o el test no están al día")
    args = parser.parse_args()

    curation = yaml.safe_load((ROOT / "curation.yaml").read_text(encoding="utf-8"))
    files = render(curation)
    existing = {
        str(p.relative_to(ROOT)) for p in POLICIES.rglob("*.yaml") if GENERATED in p.read_text(encoding="utf-8")
    } if POLICIES.is_dir() else set()
    orphans = sorted(existing - files.keys())
    # Restos anteriores al generador (sin la marca GENERADO) también sobran.
    unmanaged = sorted(str(p.relative_to(ROOT)) for p in POLICIES.rglob("*.yaml") if str(p.relative_to(ROOT)) not in files) if POLICIES.is_dir() else []
    stale = sorted(n for n, c in files.items() if not (ROOT / n).is_file() or (ROOT / n).read_text(encoding="utf-8") != c)

    if args.check:
        problems = stale + orphans + unmanaged
        if problems:
            print("policies/ desactualizado; regenera con tools/vendor_policies.py:", *problems, sep="\n  ")
            return 1
        print(f"policies/ al día ({len(files)} archivos).")
        return 0

    for name in sorted(set(orphans) | set(unmanaged)):
        (ROOT / name).unlink()
    for name, content in files.items():
        (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / name).write_text(content, encoding="utf-8")
    for directory in sorted(POLICIES.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    print(f"Escritos {len(files)} archivos; retirados {len(set(orphans) | set(unmanaged))}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

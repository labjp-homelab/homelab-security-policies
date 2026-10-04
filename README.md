# homelab-security-policies

Estándar de seguridad del homelab **labjp.xyz** como código: 32 políticas de
[Kyverno](https://kyverno.io) (API CEL `policies.kyverno.io/v1`, Kyverno 1.19), tomadas de la
[biblioteca oficial de Kyverno](https://github.com/kyverno/policies) y ordenadas por
categoría, cada una con un ID estable.

**Fuente de verdad: las políticas de `policies/`.** Lo que aplica el clúster, lo que
comprueba el pipeline y lo que leen las personas (TechDocs) y los agentes (MCP de
Backstage) sale de esos archivos; nada se escribe aparte.

```
biblioteca oficial de Kyverno (commit fijado)
   │  curation.yaml: qué reglas adoptamos + ID, categoría, textos en español, casos de prueba
   ▼  tools/vendor_policies.py
policies/<categoría>/validatingpolicy-<id>-<nombre>.yaml   ◀── FUENTE DE VERDAD
   ├──▶ Argo CD del homelab (Application homelab-security-policies, tag fijado, Audit)
   ├──▶ tests/kubernetes: kyverno test
   └──▶ tools/generate_guidelines.py
          ├─ docs/ + mkdocs.yml  ──▶ TechDocs en Backstage (personas)
          └─ catalog-info.yaml   ──▶ una entidad por regla en Backstage ──▶ agentes A2A (MCP)
```

## Estructura

```
homelab-security-policies/
├── curation.yaml               qué adoptamos de Kyverno y lo que le añadimos (a mano)
├── policies/                   GENERADO: la fuente de verdad que aplica el clúster
│   ├── pod-security/baseline/      POD-001…010  Pod Security Standards · Baseline
│   ├── pod-security/restricted/    POD-101…106  Pod Security Standards · Restricted
│   ├── workloads/                  WKL-001…004  recursos, raíz de solo lectura, namespace, socket del runtime
│   ├── images/                     IMG-001…003  sin latest, por digest, registries permitidos
│   ├── network/                    NET-001…003  NodePort, externalIPs, ExternalName a localhost
│   ├── rbac/                       RBAC-001…004 cluster-admin, grupos del sistema, verbos de escalada, nodes/proxy
│   └── secrets/                    SEC-001…002  secretos en variables, tokens de larga vida
├── tests/kubernetes/           resources.yaml + values.yaml (a mano), kyverno-test.yaml (GENERADO)
├── tools/                      vendor_policies.py, generate_guidelines.py
├── docs/, mkdocs.yml           GENERADO: TechDocs, una página por regla y categoría
└── catalog-info.yaml           GENERADO: entidades de Backstage
```

Todas las reglas están en **`Audit`**: informan en los `PolicyReport` sin bloquear. Se
pasarán a `Deny` namespace a namespace cuando su informe esté limpio.

## Qué añadimos a cada política de Kyverno

La lógica (CEL) no se toca, salvo `IMG-003`, cuya lista de registries la biblioteca deja
para personalizar (`override` en `curation.yaml`). Encima se añade:

| Añadido | Dónde |
|---------|-------|
| ID estable (`POD-001`…) | `security.labjp.xyz/rule-id`, y delante de cada mensaje (`[POD-001] ...`) |
| Categoría | etiqueta `security.labjp.xyz/category` |
| Título, por qué y cómo cumplirla, en español | `security.labjp.xyz/title`, `rationale`, `remediation` |
| Severidad del homelab | `policies.kyverno.io/severity` |
| Origen exacto | `security.labjp.xyz/upstream` (URL al commit de la biblioteca) |
| Modo | `validationActions: [Audit]` |

## Cambiar el estándar

```bash
# 1. Editar curation.yaml (adoptar/retirar reglas, textos, casos en tests/kubernetes/resources.yaml)
# 2. Regenerar las políticas y su test, y probar
uv run --with pyyaml tools/vendor_policies.py
docker run --rm -v "$PWD":/p:ro -w /p ghcr.io/kyverno/kyverno-cli:v1.19.1 test tests/kubernetes
# 3. Regenerar los lineamientos
uv run --with pyyaml tools/generate_guidelines.py
# 4. Comprobar que todo está al día
uv run --with pyyaml tools/vendor_policies.py --check
uv run --with pyyaml tools/generate_guidelines.py --check
# 5. Publicar una versión; el homelab la adopta cambiando targetRevision en
#    homelab-gitops/bootstrap/applications/platform/homelab-security-policies.yaml
git tag -a vX.Y.Z -m "..." && git push origin vX.Y.Z
```

Para actualizar la biblioteca de Kyverno: cambiar `upstream.ref` en `curation.yaml` y
repetir los pasos 2 a 5.

## Ver el estado en el clúster

```bash
kubectl get validatingpolicies -l security.labjp.xyz/standard=homelab-baseline
kubectl get policyreports -A
```

## Licencia

Apache-2.0 (ver `LICENSE`). Las políticas derivan de
[kyverno/policies](https://github.com/kyverno/policies), también Apache-2.0.

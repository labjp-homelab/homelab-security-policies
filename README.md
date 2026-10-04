# homelab-security-policies

Estándar de seguridad del homelab **labjp.xyz** como código: 39 políticas de
[Kyverno](https://kyverno.io) (API CEL `policies.kyverno.io/v1`, Kyverno 1.19), ordenadas por
categoría y cada una con un ID estable. 34 vienen de la
[biblioteca oficial de Kyverno](https://github.com/kyverno/policies); las otras 5 son
propias del homelab (`custom/`), para lo que la biblioteca no cubre: NetworkPolicy en cada
namespace, LoadBalancer solo para el Gateway, login en las rutas externas, secretos fuera
de los ConfigMaps y servidores MCP solo por la pasarela de agentes. Cada regla indica qué puntos cubre de los marcos de
referencia: **OWASP Kubernetes Top 10 (2025)**, **OWASP Top 10 for LLM Applications
(2025)**, **OWASP MCP Top 10 (2025, beta)** y **PCI DSS 4.0.1** (como referencia).

Los marcos no se cubren solo con Kyverno: cada punto también dice qué otro control del
homelab lo cubre (Keycloak, OpenBao, Kuadrant, agentgateway, Tekton Chains...) o qué falta.
Esos controles se gestionan en su repo (homelab-gitops, homelab-ansible); aquí solo se
documenta su cobertura.

**Fuente de verdad: las políticas de `policies/`.** Lo que aplica el clúster, lo que
comprueba el pipeline y lo que leen las personas (TechDocs) y los agentes (MCP de
Backstage) sale de esos archivos; nada se escribe aparte.

```
biblioteca oficial de Kyverno (commit fijado)  +  custom/ (reglas propias)
   │  curation.yaml: qué reglas adoptamos + ID, categoría, textos en español, marcos, casos de prueba
   ▼  tools/vendor_policies.py
policies/<categoría>/validatingpolicy-<id>-<nombre>.yaml   ◀── FUENTE DE VERDAD
   ├──▶ Argo CD del homelab (Application homelab-security-policies, tag fijado, Audit)
   ├──▶ tests/kubernetes: kyverno test
   └──▶ tools/generate_guidelines.py
          ├─ docs/ + mkdocs.yml  ──▶ TechDocs en Backstage (personas)
          └─ catalog-info.yaml   ──▶ una entidad por regla en Backstage ──▶ agentes A2A (MCP)

frameworks/<marco>.yaml (a mano): puntos del marco, su estado y lo que los cubre fuera de
Kyverno ──▶ tools/generate_guidelines.py ──▶ una página y una entidad por marco
```

## Estructura

```
homelab-security-policies/
├── curation.yaml               qué adoptamos de Kyverno y lo que le añadimos (a mano)
├── custom/                     reglas propias del homelab: ValidatingPolicy con la lógica CEL (a mano)
├── frameworks/                 marcos de referencia: OWASP K8s, LLM y MCP, PCI DSS (a mano)
├── policies/                   GENERADO: la fuente de verdad que aplica el clúster
│   ├── pod-security/baseline/      POD-001…010  Pod Security Standards · Baseline
│   ├── pod-security/restricted/    POD-101…106  Pod Security Standards · Restricted
│   ├── workloads/                  WKL-001…004  recursos, raíz de solo lectura, namespace, socket del runtime
│   ├── images/                     IMG-001…003  sin latest, por digest, registries permitidos
│   ├── network/                    NET-001…006  NodePort, externalIPs, ExternalName a localhost, NetworkPolicy, LoadBalancer, login en rutas externas
│   ├── rbac/                       RBAC-001…005 cluster-admin, grupos del sistema, verbos de escalada, nodes/proxy, comodines
│   ├── secrets/                    SEC-001…004  secretos en variables, tokens de larga vida, montaje del token, secretos en ConfigMaps
│   └── ai/                         AI-001       servidores MCP solo por la pasarela de agentes
├── tests/kubernetes/           resources.yaml, values.yaml, context.yaml (a mano), kyverno-test.yaml (GENERADO)
├── tools/                      vendor_policies.py, generate_guidelines.py
├── docs/, mkdocs.yml           GENERADO: TechDocs, una página por regla y por marco
└── catalog-info.yaml           GENERADO: entidades de Backstage
```

Las reglas que consultan otros objetos (`resource.List`) necesitan que Kyverno pueda
leerlos: NET-006 lee SecurityPolicy y AuthPolicy, y AI-001 RemoteMCPServer. Ese permiso se
da en homelab-gitops (`bootstrap/applications/platform/kyverno.yaml`). La rama de NET-006 que
consulta esas CRD no se puede simular en `kyverno test` y se comprueba en el clúster.

Todas las reglas están en **`Audit`**: informan en los `PolicyReport` sin bloquear. Se
pasarán a `Deny` namespace a namespace cuando su informe esté limpio.

## Qué añadimos a cada política de Kyverno

En las de la biblioteca la lógica (CEL) no se toca, salvo `IMG-003`, cuya lista de
registries la biblioteca deja para personalizar (`override` en `curation.yaml`). Las propias
(`custom/`) se escriben en CEL igual que las de la biblioteca. A todas se les añade:

| Añadido | Dónde |
|---------|-------|
| ID estable (`POD-001`…) | `security.labjp.xyz/rule-id`, y delante de cada mensaje (`[POD-001] ...`) |
| Categoría | etiqueta `security.labjp.xyz/category` |
| Título, por qué y cómo cumplirla, en español | `security.labjp.xyz/title`, `rationale`, `remediation` |
| Severidad del homelab | `policies.kyverno.io/severity` |
| Origen | `security.labjp.xyz/origin` (`kyverno-library` o `homelab`) y `upstream` (URL a la fuente) |
| Puntos de los marcos que cubre | `security.labjp.xyz/<marco>` (p. ej. `owasp-k8s-2025: K02`) |
| Modo | `validationActions: [Audit]` |

## Cambiar el estándar

```bash
# 1. Editar curation.yaml (adoptar/retirar reglas, textos, marcos, casos en tests/kubernetes/resources.yaml)
#    o frameworks/ (estado de un punto y lo que lo cubre fuera de Kyverno)
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

## CI

Cada push (rama o tag) dispara el Pipeline `security-policies-verify` del CI del homelab
(Tekton, repo `homelab-pipelines`): comprueba que `policies/` y los lineamientos están al
día con su fuente y pasa `kyverno test`. Si falla, no se publica la versión.

## Ver el estado en el clúster

```bash
kubectl get validatingpolicies -l security.labjp.xyz/standard=homelab-baseline
kubectl get policyreports -A
```

## Licencia

Apache-2.0 (ver `LICENSE`). Las políticas derivan de
[kyverno/policies](https://github.com/kyverno/policies), también Apache-2.0.

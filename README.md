# homelab-security-policies

Estándar de seguridad del homelab **labjp.xyz** como código: 41 políticas de
[Kyverno](https://kyverno.io) (API CEL `policies.kyverno.io/v1`, Kyverno 1.19), cada una con
un ID estable y ordenadas por categoría.

- **34 de la [biblioteca oficial de Kyverno](https://github.com/kyverno/policies)**, copiadas
  de un commit fijo sin tocar su lógica.
- **7 propias del homelab** (`curation/custom/`), para lo que la biblioteca no cubre:
  NetworkPolicy en cada namespace, LoadBalancer solo para el Gateway, login en las rutas
  externas, sin secretos en ConfigMaps, servidores MCP solo por la pasarela de agentes, un
  revisor de IA no aprueba solo, y sin descargar y ejecutar scripts en CI.

Cada regla indica qué puntos cubre de los marcos de referencia: **OWASP Kubernetes Top 10
(2025)**, **OWASP Top 10 for LLM Applications (2025)**, **OWASP MCP Top 10 (2025, beta)** y
**PCI DSS 4.0.1** (como referencia). Kyverno no cubre todos los puntos: los que dependen de
Keycloak, OpenBao, Kuadrant, agentgateway, Tekton Chains o la configuración de k3s se
documentan en cada marco con el control que los cubre o lo que falta. Esos controles se
gestionan en su repo (homelab-gitops, homelab-ansible); aquí solo se documenta su cobertura.

## Estructura

Lo que se escribe a mano está en `curation/` y `tests/`; el resto lo generan `tools/`.

```
homelab-security-policies/
├── curation/                 A MANO: el estándar
│   ├── rules.yaml                qué reglas se adoptan y lo que se les añade (ID, textos, marcos, tests)
│   ├── custom/                   reglas propias: ValidatingPolicy con su lógica CEL
│   └── frameworks/               marcos de referencia: puntos, estado y controles fuera de Kyverno
├── policies/                 GENERADO: lo que aplica el clúster (Argo CD lee esta carpeta)
│   ├── pod-security/baseline/    POD-001…010  Pod Security Standards · Baseline
│   ├── pod-security/restricted/  POD-101…106  Pod Security Standards · Restricted
│   ├── workloads/                WKL-001…004  recursos, raíz de solo lectura, namespace, socket del runtime
│   ├── images/                   IMG-001…003  sin latest, por digest, registries permitidos
│   ├── network/                  NET-001…006  NodePort, externalIPs, localhost, NetworkPolicy, LoadBalancer, login en rutas externas
│   ├── rbac/                     RBAC-001…005 cluster-admin, grupos del sistema, escalada, nodes/proxy, comodines
│   ├── secrets/                  SEC-001…004  variables de entorno, tokens de larga vida, montaje del token, ConfigMaps
│   ├── ai/                       AI-001…002   servidores MCP por la pasarela; un revisor de IA no aprueba solo
│   └── ci/                       CI-001       sin descargar y ejecutar scripts en los pipelines
├── tests/                    casos de prueba (a mano) y kyverno-test.yaml (GENERADO)
├── backstage/                GENERADO: lo que lee Backstage
│   ├── catalog-info.yaml         una entidad por regla y por marco
│   └── mkdocs.yml, docs/         TechDocs: una página por regla y por marco
├── tools/                    vendor_policies.py, generate_guidelines.py
└── README.md, LICENSE
```

```
biblioteca de Kyverno (commit fijado) + curation/custom/
   │  curation/rules.yaml
   ▼  tools/vendor_policies.py
policies/   ◀── FUENTE DE VERDAD: lo que aplica el clúster
   ├──▶ Argo CD del homelab (Application homelab-security-policies, tag fijado)
   ├──▶ tests/: kyverno test
   └──▶ tools/generate_guidelines.py  (+ curation/frameworks/)
          └─▶ backstage/: TechDocs (personas) y catálogo (agentes, por el MCP de Backstage)
```

Todas las reglas están en **`Audit`**: informan en los `PolicyReport` sin bloquear. Se
pasarán a `Deny` namespace a namespace cuando su informe esté limpio.

Las reglas que consultan otros objetos (`resource.List`) necesitan que Kyverno pueda
leerlos: NET-006 lee SecurityPolicy y AuthPolicy, y AI-001 RemoteMCPServer. Para el
escaneo de fondo, CI-001 necesita leer los Task y Pipeline de Tekton. Ese permiso se
da en homelab-gitops (`bootstrap/applications/platform/kyverno.yaml`). La rama de NET-006
que consulta esas CRD no se puede simular en `kyverno test` y se comprueba en el clúster.

## Qué se añade a cada política

En las de la biblioteca la lógica no se toca, salvo `IMG-003`, cuya lista de registries la
biblioteca deja para personalizar (`override` en `curation/rules.yaml`). A todas se les
añade:

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
# 1. Editar curation/ (reglas, textos, marcos) y tests/resources.yaml (casos de prueba)
# 2. Regenerar las políticas y su test, y probar
uv run --with pyyaml tools/vendor_policies.py
docker run --rm -v "$PWD":/p:ro -w /p ghcr.io/kyverno/kyverno-cli:v1.19.1 test tests
# 3. Regenerar lo que lee Backstage
uv run --with pyyaml tools/generate_guidelines.py
# 4. Comprobar que todo está al día (lo mismo que hace el CI)
uv run --with pyyaml tools/vendor_policies.py --check
uv run --with pyyaml tools/generate_guidelines.py --check
# 5. Publicar una versión; el homelab la adopta cambiando targetRevision en
#    homelab-gitops/bootstrap/applications/platform/homelab-security-policies.yaml
git tag -a vX.Y.Z -m "..." && git push origin vX.Y.Z
```

Para actualizar la biblioteca de Kyverno: cambiar `upstream.ref` en `curation/rules.yaml` y
repetir los pasos 2 a 5.

## CI

Cada push (rama o tag) dispara el Pipeline `security-policies-verify` del CI del homelab
(Tekton, repo `homelab-pipelines`): comprueba que `policies/` y `backstage/` están al día con
su fuente y pasa `kyverno test`. Si falla, no se publica la versión.

## Ver el estado en el clúster

```bash
kubectl get validatingpolicies -l security.labjp.xyz/standard=homelab-baseline
kubectl get policyreports -A
```

## Licencia

Apache-2.0 (ver `LICENSE`). Las políticas derivan de
[kyverno/policies](https://github.com/kyverno/policies), también Apache-2.0.

# homelab-security-policies

Estándar de seguridad del homelab **labjp.xyz** como código: políticas de
[Kyverno](https://kyverno.io) (API CEL `policies.kyverno.io/v1`, Kyverno 1.19), una por
regla, con un ID estable. Es la **fuente única** de los lineamientos: lo que aplica el
clúster, lo que comprueba el pipeline y lo que leen las personas y los agentes salen de
estos archivos.

```
homelab-security-policies (este repo)
 ├─ policies/kubernetes/   ──▶ Argo CD del homelab (Application homelab-security-policies, tag fijado)
 ├─ tests/kubernetes/      ──▶ kyverno test
 ├─ tools/                 generate_guidelines.py
 └─ catalog-info.yaml, mkdocs.yml, docs/   (GENERADOS)
        ──▶ Backstage: una entidad Resource por regla + TechDocs
              ──▶ agentes, por el MCP de Backstage (leen la regla, no la prosa)
```

## Reglas

| ID | Política | Severidad | Exige |
|----|----------|-----------|-------|
| K8S-001 | `run-as-non-root` | high | `runAsNonRoot: true` (pod o contenedor) |
| K8S-002 | `disallow-privilege-escalation` | high | `allowPrivilegeEscalation: false` |
| K8S-003 | `drop-all-capabilities` | medium | `capabilities.drop: [ALL]` |
| K8S-004 | `seccomp-runtime-default` | medium | `seccompProfile` `RuntimeDefault` o `Localhost` |
| K8S-005 | `read-only-root-filesystem` | medium | `readOnlyRootFilesystem: true` |
| K8S-006 | `require-memory-limits` | medium | `resources.limits.memory` |
| K8S-007 | `pin-image-reference` | high | imagen por digest o tag de versión, nunca `latest` |

Todas en **`Audit`**: informan en los `PolicyReport` de cada namespace sin bloquear. Se
pasarán a `Deny` namespace a namespace cuando su informe esté limpio.

## Anotaciones (el contrato con Backstage y los agentes)

| Anotación | Para qué |
|-----------|----------|
| `security.labjp.xyz/rule-id` | ID estable; no cambia aunque cambie el nombre de la política |
| `policies.kyverno.io/title`, `category`, `severity` | título, categoría y severidad |
| `policies.kyverno.io/description` | por qué existe la regla |
| `security.labjp.xyz/remediation` | cómo cumplirla (fragmento YAML) |

Cada mensaje de incumplimiento empieza por el ID (`[K8S-001] ...`) y nombra los
contenedores afectados.

## Cambiar o añadir una regla

1. Edita o crea `policies/kubernetes/validatingpolicy-<id>-<nombre>.yaml` (con todas las
   anotaciones) y añádela a `policies/kubernetes/kustomization.yaml`.
2. Añade sus casos a `tests/kubernetes/kyverno-test.yaml` y pásalos:

   ```bash
   docker run --rm -v "$PWD":/p:ro -w /p ghcr.io/kyverno/kyverno-cli:v1.19.1 test tests/kubernetes
   ```

3. Regenera los lineamientos (nunca se editan a mano) y comprueba que están al día:

   ```bash
   uv run --with pyyaml tools/generate_guidelines.py
   uv run --with pyyaml tools/generate_guidelines.py --check
   ```

4. Publica una versión: `git tag -a vX.Y.Z` y súbela. El homelab la adopta al cambiar
   `targetRevision` en su Application (`homelab-gitops`,
   `bootstrap/applications/platform/homelab-security-policies.yaml`).

## Ver el estado en el clúster

```bash
kubectl get validatingpolicies -l security.labjp.xyz/standard=homelab-baseline
kubectl get policyreports -A
```

## Licencia

Apache-2.0 (ver `LICENSE`).

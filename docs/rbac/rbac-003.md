<!-- GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano. -->
# RBAC-003 · Sin verbos de escalada en roles

| | |
|---|---|
| **Categoría** | Permisos (RBAC) |
| **Severidad** | high |
| **Modo actual** | Audit |
| **Se evalúa sobre** | clusterroles, roles |
| **Política** | [`policies/rbac/validatingpolicy-rbac-003-restrict-escalation-verbs-roles.yaml`](https://github.com/labjp-homelab/homelab-security-policies/blob/main/policies/rbac/validatingpolicy-rbac-003-restrict-escalation-verbs-roles.yaml) |
| **Origen** | [biblioteca oficial de Kyverno](https://github.com/kyverno/policies/blob/ec478cb5996376c0d2f09520675805a8e33297c9/other-vpol/restrict-escalation-verbs-roles/restrict-escalation-verbs-roles.yaml) |

## Por qué

bind, escalate e impersonate sobre roles permiten darse a uno mismo cualquier permiso.

## Cómo cumplirla

```yaml
rules:
  - apiGroups: [""]
    resources: [pods]
    verbs: [get, list, watch]   # nada de bind / escalate / impersonate / *
```

## Qué comprueba exactamente

Expresiones CEL que evalúa Kyverno (deben cumplirse todas):

```
object.rules == null || !object.rules.exists(rule, rule.apiGroups.exists(apiGroup, apiGroup in variables.apiGroups) && rule.resources.exists(resource, resource in variables.resources) && rule.verbs.exists(verb, verb in variables.verbs))
```

<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# RBAC-005 · Sin verbos comodín en roles

| | |
|---|---|
| **Categoría** | Permisos (RBAC) |
| **Severidad** | medium |
| **Modo actual** | Audit |
| **Se evalúa sobre** | clusterroles, roles |
| **Política** | [`policies/rbac/validatingpolicy-rbac-005-restrict-wildcard-verbs.yaml`](https://github.com/labjp-homelab/homelab-security-policies/blob/main/policies/rbac/validatingpolicy-rbac-005-restrict-wildcard-verbs.yaml) |
| **Origen** | [biblioteca oficial de Kyverno](https://github.com/kyverno/policies/blob/ec478cb5996376c0d2f09520675805a8e33297c9/other-vpol/restrict-wildcard-verbs/restrict-wildcard-verbs.yaml) |
| **Marcos de referencia** | [OWASP Kubernetes Top 10 2025](../frameworks/owasp-k8s-2025.md): K02<br>[OWASP MCP Top 10 2025 (v0.1, beta)](../frameworks/owasp-mcp-2025.md): MCP02<br>[PCI DSS 4.0.1 (referencia)](../frameworks/pci-dss-4.0.1.md): 7 |

## Por qué

Un verbo '*' concede hoy todo lo que la API permite y mañana lo que añada: el rol deja de describir lo que de verdad necesita quien lo usa.

## Cómo cumplirla

```yaml
rules:
  - apiGroups: [""]
    resources: [pods]
    verbs: [get, list, watch]   # los verbos concretos, nunca "*"
```

## Qué comprueba exactamente

Expresiones CEL que evalúa Kyverno (deben cumplirse todas):

```
object.rules == null || !object.rules.exists(rule, '*' in rule.verbs)
```

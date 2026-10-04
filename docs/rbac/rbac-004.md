<!-- GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano. -->
# RBAC-004 · Sin acceso a nodes/proxy

| | |
|---|---|
| **Categoría** | Permisos (RBAC) |
| **Severidad** | high |
| **Modo actual** | Audit |
| **Se evalúa sobre** | clusterroles |
| **Política** | [`policies/rbac/validatingpolicy-rbac-004-restrict-clusterrole-nodesproxy.yaml`](https://github.com/labjp-homelab/homelab-security-policies/blob/main/policies/rbac/validatingpolicy-rbac-004-restrict-clusterrole-nodesproxy.yaml) |
| **Origen** | [biblioteca oficial de Kyverno](https://github.com/kyverno/policies/blob/ec478cb5996376c0d2f09520675805a8e33297c9/other-vpol/restrict-clusterrole-nodesproxy/restrict-clusterrole-nodesproxy.yaml) |

## Por qué

nodes/proxy da acceso directo a la API del kubelet: ejecutar comandos en cualquier pod del nodo saltándose la auditoría del API server.

## Cómo cumplirla

```yaml
# Quitar "nodes/proxy" de los resources del ClusterRole
```

## Qué comprueba exactamente

Expresiones CEL que evalúa Kyverno (deben cumplirse todas):

```
object.rules == null || !object.rules.exists(rule, rule.resources.exists(resource, resource == 'nodes/proxy') && rule.apiGroups.exists(apiGroup, apiGroup == ''))
```

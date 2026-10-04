<!-- GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano. -->
# RBAC-001 · Sin enlaces a cluster-admin

| | |
|---|---|
| **Categoría** | Permisos (RBAC) |
| **Severidad** | high |
| **Modo actual** | Audit |
| **Se evalúa sobre** | clusterrolebindings, rolebindings |
| **Política** | [`policies/rbac/validatingpolicy-rbac-001-restrict-binding-clusteradmin.yaml`](https://github.com/labjp-homelab/homelab-security-policies/blob/main/policies/rbac/validatingpolicy-rbac-001-restrict-binding-clusteradmin.yaml) |
| **Origen** | [biblioteca oficial de Kyverno](https://github.com/kyverno/policies/blob/ec478cb5996376c0d2f09520675805a8e33297c9/other-vpol/restrict-binding-clusteradmin/restrict-binding-clusteradmin.yaml) |

## Por qué

cluster-admin permite cualquier acción sobre cualquier recurso. Ninguna aplicación ni agente debe tenerlo; cada uno, su Role mínimo.

## Cómo cumplirla

```yaml
roleRef:
  kind: ClusterRole
  name: <rol mínimo propio>   # nunca cluster-admin
```

## Qué comprueba exactamente

Expresiones CEL que evalúa Kyverno (deben cumplirse todas):

```
object.roleRef.name != 'cluster-admin'
```

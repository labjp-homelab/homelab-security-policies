<!-- GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano. -->
# RBAC-002 · Sin enlaces a grupos del sistema

| | |
|---|---|
| **Categoría** | Permisos (RBAC) |
| **Severidad** | high |
| **Modo actual** | Audit |
| **Se evalúa sobre** | clusterrolebindings, rolebindings |
| **Política** | [`policies/rbac/validatingpolicy-rbac-002-restrict-binding-system-groups.yaml`](https://github.com/labjp-homelab/homelab-security-policies/blob/main/policies/rbac/validatingpolicy-rbac-002-restrict-binding-system-groups.yaml) |
| **Origen** | [biblioteca oficial de Kyverno](https://github.com/kyverno/policies/blob/ec478cb5996376c0d2f09520675805a8e33297c9/other-vpol/restrict-binding-system-groups/restrict-binding-system-groups.yaml) |

## Por qué

Enlazar system:anonymous, system:unauthenticated o system:masters da permisos a cualquiera o el control total.

## Cómo cumplirla

```yaml
subjects:
  - kind: ServiceAccount   # o un grupo propio de Keycloak
    name: <identidad concreta>
```

## Qué comprueba exactamente

Expresiones CEL que evalúa Kyverno (deben cumplirse todas):

```
object.subjects.all(subject, subject.name != 'system:anonymous')
```

```
object.subjects.all(subject, subject.name != 'system:unauthenticated')
```

```
object.subjects.all(subject, subject.name != 'system:masters')
```

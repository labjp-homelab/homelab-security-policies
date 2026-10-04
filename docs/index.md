<!-- GENERADO por tools/generate_guidelines.py desde policies/. No editar a mano. -->
# Lineamientos de seguridad del homelab

Cada regla es una `ValidatingPolicy` de Kyverno en [`policies/kubernetes/`](https://github.com/labjp-homelab/homelab-security-policies/tree/main/policies/kubernetes).
Lo que se lee aquí y lo que aplica el clúster salen del mismo archivo: si cambia la
política, cambia esta página.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [K8S-001](k8s-001.md) | Los contenedores no corren como root | high | Audit |
| [K8S-002](k8s-002.md) | Sin escalada de privilegios | high | Audit |
| [K8S-003](k8s-003.md) | Sin capabilities de Linux | medium | Audit |
| [K8S-004](k8s-004.md) | Perfil seccomp del runtime | medium | Audit |
| [K8S-005](k8s-005.md) | Sistema de archivos raíz de solo lectura | medium | Audit |
| [K8S-006](k8s-006.md) | Límite de memoria declarado | medium | Audit |
| [K8S-007](k8s-007.md) | Imagen fijada, sin latest | high | Audit |

`Audit` informa en los PolicyReports sin bloquear; `Deny` rechaza en la admisión.

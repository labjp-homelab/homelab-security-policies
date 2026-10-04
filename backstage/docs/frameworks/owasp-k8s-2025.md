<!-- GENERADO por tools/generate_guidelines.py desde policies/ y curation/. No editar a mano. -->
# OWASP Kubernetes Top 10 2025

Referencia oficial: <https://kubernetes-top10.owasp.org/>

Cobertura en el homelab: 0 cubierto, 9 parcial, 0 pendiente, 1 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/owasp-k8s-2025`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`curation/frameworks/owasp-k8s-2025.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno |
|----|--------|--------|-------------------|
| [K01](#k01) | Insecure Workload Configurations | Parcial | [POD-001](../pod-security-baseline/pod-001.md), [POD-002](../pod-security-baseline/pod-002.md), [POD-003](../pod-security-baseline/pod-003.md), [POD-004](../pod-security-baseline/pod-004.md), [POD-005](../pod-security-baseline/pod-005.md), [POD-006](../pod-security-baseline/pod-006.md), [POD-007](../pod-security-baseline/pod-007.md), [POD-008](../pod-security-baseline/pod-008.md), [POD-009](../pod-security-baseline/pod-009.md), [POD-010](../pod-security-baseline/pod-010.md), [POD-101](../pod-security-restricted/pod-101.md), [POD-102](../pod-security-restricted/pod-102.md), [POD-103](../pod-security-restricted/pod-103.md), [POD-104](../pod-security-restricted/pod-104.md), [POD-105](../pod-security-restricted/pod-105.md), [POD-106](../pod-security-restricted/pod-106.md), [WKL-001](../workloads/wkl-001.md), [WKL-002](../workloads/wkl-002.md), [WKL-003](../workloads/wkl-003.md), [WKL-004](../workloads/wkl-004.md) |
| [K02](#k02) | Overly Permissive Authorization Configurations | Parcial | [RBAC-001](../rbac/rbac-001.md), [RBAC-002](../rbac/rbac-002.md), [RBAC-003](../rbac/rbac-003.md), [RBAC-004](../rbac/rbac-004.md), [RBAC-005](../rbac/rbac-005.md), [SEC-003](../secrets/sec-003.md) |
| [K03](#k03) | Secrets Management Failures | Parcial | [SEC-001](../secrets/sec-001.md), [SEC-002](../secrets/sec-002.md), [SEC-003](../secrets/sec-003.md), [SEC-004](../secrets/sec-004.md) |
| [K04](#k04) | Lack Of Cluster Level Policy Enforcement | Parcial | — |
| [K05](#k05) | Missing Network Segmentation Controls | Parcial | [NET-001](../network/net-001.md), [NET-002](../network/net-002.md), [NET-003](../network/net-003.md), [NET-004](../network/net-004.md) |
| [K06](#k06) | Overly Exposed Kubernetes Components | Parcial | [NET-005](../network/net-005.md) |
| [K07](#k07) | Misconfigured And Vulnerable Cluster Components | Parcial | — |
| [K08](#k08) | Cluster To Cloud Lateral Movement | No aplica | — |
| [K09](#k09) | Broken Authentication Mechanisms | Parcial | [NET-006](../network/net-006.md) |
| [K10](#k10) | Inadequate Logging And Monitoring | Parcial | — |

## K01

**Insecure Workload Configurations** · Parcial

**Reglas de Kyverno**

- [POD-001 · Sin contenedores privilegiados](../pod-security-baseline/pod-001.md)
- [POD-002 · Sin namespaces del nodo](../pod-security-baseline/pod-002.md)
- [POD-003 · Sin volúmenes hostPath](../pod-security-baseline/pod-003.md)
- [POD-004 · Sin puertos del nodo](../pod-security-baseline/pod-004.md)
- [POD-005 · Sin HostProcess de Windows](../pod-security-baseline/pod-005.md)
- [POD-006 · Solo capabilities del conjunto Baseline](../pod-security-baseline/pod-006.md)
- [POD-007 · /proc con máscara por defecto](../pod-security-baseline/pod-007.md)
- [POD-008 · Sin opciones SELinux personalizadas](../pod-security-baseline/pod-008.md)
- [POD-009 · Perfil seccomp no deshabilitado](../pod-security-baseline/pod-009.md)
- [POD-010 · Solo sysctls seguros](../pod-security-baseline/pod-010.md)
- [POD-101 · Los contenedores no corren como root](../pod-security-restricted/pod-101.md)
- [POD-102 · Ningún uid 0 explícito](../pod-security-restricted/pod-102.md)
- [POD-103 · Sin escalada de privilegios](../pod-security-restricted/pod-103.md)
- [POD-104 · Sin capabilities (salvo NET_BIND_SERVICE)](../pod-security-restricted/pod-104.md)
- [POD-105 · seccomp RuntimeDefault o Localhost](../pod-security-restricted/pod-105.md)
- [POD-106 · Solo tipos de volumen seguros](../pod-security-restricted/pod-106.md)
- [WKL-001 · Raíz de solo lectura](../workloads/wkl-001.md)
- [WKL-002 · Requests y límite de memoria](../workloads/wkl-002.md)
- [WKL-003 · Nada en el namespace default](../workloads/wkl-003.md)
- [WKL-004 · Sin el socket del runtime](../workloads/wkl-004.md)

**Otros controles del homelab**

- Pod Security Admission por namespace (homelab-gitops, components/governance/values)

## K02

**Overly Permissive Authorization Configurations** · Parcial

**Reglas de Kyverno**

- [RBAC-001 · Sin enlaces a cluster-admin](../rbac/rbac-001.md)
- [RBAC-002 · Sin enlaces a grupos del sistema](../rbac/rbac-002.md)
- [RBAC-003 · Sin verbos de escalada en roles](../rbac/rbac-003.md)
- [RBAC-004 · Sin acceso a nodes/proxy](../rbac/rbac-004.md)
- [RBAC-005 · Sin verbos comodín en roles](../rbac/rbac-005.md)
- [SEC-003 · Sin montar el token de la ServiceAccount por defecto](../secrets/sec-003.md)

**Otros controles del homelab**

- Argo CD con un rol por AppProject y sin acceso por defecto (homelab-gitops, components/platform/argocd/patch-argocd-rbac-cm.yaml)

## K03

**Secrets Management Failures** · Parcial

**Reglas de Kyverno**

- [SEC-001 · Secretos montados, no en variables de entorno](../secrets/sec-001.md)
- [SEC-002 · Sin tokens de ServiceAccount de larga vida](../secrets/sec-002.md)
- [SEC-003 · Sin montar el token de la ServiceAccount por defecto](../secrets/sec-003.md)
- [SEC-004 · Sin secretos en ConfigMaps](../secrets/sec-004.md)

**Otros controles del homelab**

- Secretos en OpenBao, fuera del clúster, materializados por External Secrets; nunca en Git

## K04

**Lack Of Cluster Level Policy Enforcement** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Kyverno aplica este estándar en todo el clúster; todas las reglas en Audit hasta pasar a Deny namespace a namespace

## K05

**Missing Network Segmentation Controls** · Parcial

**Reglas de Kyverno**

- [NET-001 · Sin Services NodePort](../network/net-001.md)
- [NET-002 · Sin externalIPs en Services](../network/net-002.md)
- [NET-003 · Sin Services ExternalName a localhost](../network/net-003.md)
- [NET-004 · Cada namespace con NetworkPolicy](../network/net-004.md)

**Otros controles del homelab**

- NetworkPolicies de homelab-hardening (homelab-gitops, components/platform/homelab-hardening); la salida sigue abierta fuera de homelab

## K06

**Overly Exposed Kubernetes Components** · Parcial

**Reglas de Kyverno**

- [NET-005 · LoadBalancer solo para el Gateway](../network/net-005.md)

**Otros controles del homelab**

- Argo CD, Grafana, Backstage y la interfaz de n8n solo por el Gateway interno (LAN); la única entrada desde Internet es el túnel de Cloudflare

## K07

**Misconfigured And Vulnerable Cluster Components** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- k3s al día con system-upgrade-controller (homelab-gitops, components/platform/system-upgrade-plans)
- kube-bench revisa cada semana el control plane, etcd y el kubelet de cada nodo contra el CIS Benchmark de k3s (homelab-gitops, components/platform/kube-bench); sus FAIL siguen abiertos

## K08

**Cluster To Cloud Lateral Movement** · No aplica

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- El clúster corre en VMs propias, sin proveedor de nube ni metadatos de instancia; las credenciales de R2 viven fuera del clúster

## K09

**Broken Authentication Mechanisms** · Parcial

**Reglas de Kyverno**

- [NET-006 · Rutas externas con login o públicas a propósito](../network/net-006.md)

**Otros controles del homelab**

- SSO con Keycloak (OIDC con PKCE) en todas las interfaces (homelab-ansible, rol keycloak_identity)
- Pendiente exigir segundo factor

## K10

**Inadequate Logging And Monitoring** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Prometheus, Alertmanager y Grafana; PolicyReports de Kyverno
- Pendiente centralizar los registros de auditoría del API server

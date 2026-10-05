<!-- GENERADO por tools/generate_guidelines.py desde policies/ y curation/. No editar a mano. -->
# PCI DSS 4.0.1 (referencia)

Referencia oficial: <https://www.pcisecuritystandards.org/document_library/>

Cobertura en el homelab: 0 cubierto, 9 parcial, 1 pendiente, 2 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/pci-dss-4.0.1`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`curation/frameworks/pci-dss-4.0.1.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno |
|----|--------|--------|-------------------|
| [1](#1) | Install and maintain network security controls | Parcial | [NET-001](../network/net-001.md), [NET-002](../network/net-002.md), [NET-003](../network/net-003.md), [NET-004](../network/net-004.md), [NET-005](../network/net-005.md) |
| [2](#2) | Apply secure configurations to all system components | Parcial | [POD-001](../pod-security-baseline/pod-001.md), [POD-002](../pod-security-baseline/pod-002.md), [POD-003](../pod-security-baseline/pod-003.md), [POD-004](../pod-security-baseline/pod-004.md), [POD-005](../pod-security-baseline/pod-005.md), [POD-006](../pod-security-baseline/pod-006.md), [POD-007](../pod-security-baseline/pod-007.md), [POD-008](../pod-security-baseline/pod-008.md), [POD-009](../pod-security-baseline/pod-009.md), [POD-010](../pod-security-baseline/pod-010.md), [POD-101](../pod-security-restricted/pod-101.md), [POD-102](../pod-security-restricted/pod-102.md), [POD-103](../pod-security-restricted/pod-103.md), [POD-104](../pod-security-restricted/pod-104.md), [POD-105](../pod-security-restricted/pod-105.md), [POD-106](../pod-security-restricted/pod-106.md), [WKL-001](../workloads/wkl-001.md), [WKL-004](../workloads/wkl-004.md) |
| [3](#3) | Protect stored account data | Parcial | [SEC-001](../secrets/sec-001.md), [SEC-004](../secrets/sec-004.md) |
| [4](#4) | Protect cardholder data with strong cryptography during transmission | Parcial | — |
| [5](#5) | Protect all systems and networks from malicious software | Pendiente | — |
| [6](#6) | Develop and maintain secure systems and software | Parcial | [CI-001](../ci/ci-001.md), [IMG-001](../images/img-001.md), [IMG-002](../images/img-002.md), [IMG-003](../images/img-003.md) |
| [7](#7) | Restrict access to system components and cardholder data by business need to know | Parcial | [RBAC-001](../rbac/rbac-001.md), [RBAC-002](../rbac/rbac-002.md), [RBAC-003](../rbac/rbac-003.md), [RBAC-004](../rbac/rbac-004.md), [RBAC-005](../rbac/rbac-005.md), [SEC-003](../secrets/sec-003.md) |
| [8](#8) | Identify users and authenticate access to system components | Parcial | [NET-006](../network/net-006.md), [SEC-002](../secrets/sec-002.md) |
| [9](#9) | Restrict physical access to cardholder data | No aplica | — |
| [10](#10) | Log and monitor all access to system components and cardholder data | Parcial | — |
| [11](#11) | Test security of systems and networks regularly | Parcial | — |
| [12](#12) | Support information security with organizational policies and programs | No aplica | — |

## 1

**Install and maintain network security controls** · Parcial

**Reglas de Kyverno**

- [NET-001 · Sin Services NodePort](../network/net-001.md)
- [NET-002 · Sin externalIPs en Services](../network/net-002.md)
- [NET-003 · Sin Services ExternalName a localhost](../network/net-003.md)
- [NET-004 · Cada namespace con NetworkPolicy](../network/net-004.md)
- [NET-005 · LoadBalancer solo para el Gateway](../network/net-005.md)

**Otros controles del homelab**

- pfSense en el perímetro y NetworkPolicies de homelab-hardening

## 2

**Apply secure configurations to all system components** · Parcial

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
- [WKL-004 · Sin el socket del runtime](../workloads/wkl-004.md)

**Otros controles del homelab**

- Pod Security Admission por namespace; hosts endurecidos con homelab-ansible (rol common)

## 3

**Protect stored account data** · Parcial

**Reglas de Kyverno**

- [SEC-001 · Secretos montados, no en variables de entorno](../secrets/sec-001.md)
- [SEC-004 · Sin secretos en ConfigMaps](../secrets/sec-004.md)

**Otros controles del homelab**

- Secretos en OpenBao con la clave de apertura sellada en el TPM

## 4

**Protect cardholder data with strong cryptography during transmission** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- TLS de Let's Encrypt (cert-manager) en los gateways y redirección de HTTP a HTTPS
- El tráfico entre pods no va cifrado

## 5

**Protect all systems and networks from malicious software** · Pendiente

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

Ninguno.

## 6

**Develop and maintain secure systems and software** · Parcial

**Reglas de Kyverno**

- [CI-001 · Sin descargar y ejecutar scripts en CI](../ci/ci-001.md)
- [IMG-001 · Sin el tag latest](../images/img-001.md)
- [IMG-002 · Imagen fijada por digest](../images/img-002.md)
- [IMG-003 · Solo registries conocidos](../images/img-003.md)

**Otros controles del homelab**

- Imágenes firmadas con Tekton Chains y k3s al día con system-upgrade-controller

## 7

**Restrict access to system components and cardholder data by business need to know** · Parcial

**Reglas de Kyverno**

- [RBAC-001 · Sin enlaces a cluster-admin](../rbac/rbac-001.md)
- [RBAC-002 · Sin enlaces a grupos del sistema](../rbac/rbac-002.md)
- [RBAC-003 · Sin verbos de escalada en roles](../rbac/rbac-003.md)
- [RBAC-004 · Sin acceso a nodes/proxy](../rbac/rbac-004.md)
- [RBAC-005 · Sin verbos comodín en roles](../rbac/rbac-005.md)
- [SEC-003 · Sin montar el token de la ServiceAccount por defecto](../secrets/sec-003.md)

**Otros controles del homelab**

- Roles app-* de Keycloak por aplicación y un rol de Argo CD por AppProject

## 8

**Identify users and authenticate access to system components** · Parcial

**Reglas de Kyverno**

- [NET-006 · Rutas externas con login o públicas a propósito](../network/net-006.md)
- [SEC-002 · Sin tokens de ServiceAccount de larga vida](../secrets/sec-002.md)

**Otros controles del homelab**

- SSO con Keycloak; pendiente exigir segundo factor

## 9

**Restrict physical access to cardholder data** · No aplica

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Fuera del alcance de Kubernetes

## 10

**Log and monitor all access to system components and cardholder data** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Prometheus, Alertmanager y Grafana; pendiente centralizar la auditoría del API server

## 11

**Test security of systems and networks regularly** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- kube-bench semanal contra el CIS Benchmark de k3s y PolicyReports continuos de Kyverno
- Pendiente el escaneo de vulnerabilidades de las imágenes en ejecución

## 12

**Support information security with organizational policies and programs** · No aplica

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Programa organizativo; fuera del alcance técnico

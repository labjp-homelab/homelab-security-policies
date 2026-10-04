<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# PCI DSS 4.0.1 (referencia)

Referencia oficial: <https://www.pcisecuritystandards.org/document_library/>

Cobertura en el homelab: 0 cubierto, 8 parcial, 2 pendiente, 2 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/pci-dss-4.0.1`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`frameworks/pci-dss-4.0.1.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno | Otros controles del homelab |
|----|--------|--------|-------------------|-----------------------------|
| **1** | Install and maintain network security controls | Parcial | [NET-001](../network/net-001.md), [NET-002](../network/net-002.md), [NET-003](../network/net-003.md), [NET-004](../network/net-004.md), [NET-005](../network/net-005.md) | pfSense en el perímetro y NetworkPolicies de homelab-hardening |
| **2** | Apply secure configurations to all system components | Parcial | [POD-001](../pod-security-baseline/pod-001.md), [POD-002](../pod-security-baseline/pod-002.md), [POD-003](../pod-security-baseline/pod-003.md), [POD-004](../pod-security-baseline/pod-004.md), [POD-005](../pod-security-baseline/pod-005.md), [POD-006](../pod-security-baseline/pod-006.md), [POD-007](../pod-security-baseline/pod-007.md), [POD-008](../pod-security-baseline/pod-008.md), [POD-009](../pod-security-baseline/pod-009.md), [POD-010](../pod-security-baseline/pod-010.md), [POD-101](../pod-security-restricted/pod-101.md), [POD-102](../pod-security-restricted/pod-102.md), [POD-103](../pod-security-restricted/pod-103.md), [POD-104](../pod-security-restricted/pod-104.md), [POD-105](../pod-security-restricted/pod-105.md), [POD-106](../pod-security-restricted/pod-106.md), [WKL-001](../workloads/wkl-001.md), [WKL-004](../workloads/wkl-004.md) | Pod Security Admission por namespace; hosts endurecidos con homelab-ansible (rol common) |
| **3** | Protect stored account data | Parcial | [SEC-001](../secrets/sec-001.md), [SEC-004](../secrets/sec-004.md) | Secretos en OpenBao con la clave de apertura sellada en el TPM |
| **4** | Protect cardholder data with strong cryptography during transmission | Parcial | — | TLS de Let's Encrypt (cert-manager) en los gateways y redirección de HTTP a HTTPS<br>El tráfico entre pods no va cifrado |
| **5** | Protect all systems and networks from malicious software | Pendiente | — | — |
| **6** | Develop and maintain secure systems and software | Parcial | [IMG-001](../images/img-001.md), [IMG-002](../images/img-002.md), [IMG-003](../images/img-003.md) | Imágenes firmadas con Tekton Chains y k3s al día con system-upgrade-controller |
| **7** | Restrict access to system components and cardholder data by business need to know | Parcial | [RBAC-001](../rbac/rbac-001.md), [RBAC-002](../rbac/rbac-002.md), [RBAC-003](../rbac/rbac-003.md), [RBAC-004](../rbac/rbac-004.md), [RBAC-005](../rbac/rbac-005.md), [SEC-003](../secrets/sec-003.md) | Roles app-* de Keycloak por aplicación y un rol de Argo CD por AppProject |
| **8** | Identify users and authenticate access to system components | Parcial | [NET-006](../network/net-006.md), [SEC-002](../secrets/sec-002.md) | SSO con Keycloak; pendiente exigir segundo factor |
| **9** | Restrict physical access to cardholder data | No aplica | — | Fuera del alcance de Kubernetes |
| **10** | Log and monitor all access to system components and cardholder data | Parcial | — | Prometheus, Alertmanager y Grafana; pendiente centralizar la auditoría del API server |
| **11** | Test security of systems and networks regularly | Pendiente | — | — |
| **12** | Support information security with organizational policies and programs | No aplica | — | Programa organizativo; fuera del alcance técnico |

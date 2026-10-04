<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# OWASP Kubernetes Top 10 2025

Referencia oficial: <https://kubernetes-top10.owasp.org/>

Cobertura en el homelab: 0 cubierto, 9 parcial, 0 pendiente, 1 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/owasp-k8s-2025`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`frameworks/owasp-k8s-2025.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno | Otros controles del homelab |
|----|--------|--------|-------------------|-----------------------------|
| **K01** | Insecure Workload Configurations | Parcial | [POD-001](../pod-security-baseline/pod-001.md), [POD-002](../pod-security-baseline/pod-002.md), [POD-003](../pod-security-baseline/pod-003.md), [POD-004](../pod-security-baseline/pod-004.md), [POD-005](../pod-security-baseline/pod-005.md), [POD-006](../pod-security-baseline/pod-006.md), [POD-007](../pod-security-baseline/pod-007.md), [POD-008](../pod-security-baseline/pod-008.md), [POD-009](../pod-security-baseline/pod-009.md), [POD-010](../pod-security-baseline/pod-010.md), [POD-101](../pod-security-restricted/pod-101.md), [POD-102](../pod-security-restricted/pod-102.md), [POD-103](../pod-security-restricted/pod-103.md), [POD-104](../pod-security-restricted/pod-104.md), [POD-105](../pod-security-restricted/pod-105.md), [POD-106](../pod-security-restricted/pod-106.md), [WKL-001](../workloads/wkl-001.md), [WKL-002](../workloads/wkl-002.md), [WKL-003](../workloads/wkl-003.md), [WKL-004](../workloads/wkl-004.md) | Pod Security Admission por namespace (homelab-gitops, components/governance/values) |
| **K02** | Overly Permissive Authorization Configurations | Parcial | [RBAC-001](../rbac/rbac-001.md), [RBAC-002](../rbac/rbac-002.md), [RBAC-003](../rbac/rbac-003.md), [RBAC-004](../rbac/rbac-004.md), [RBAC-005](../rbac/rbac-005.md), [SEC-003](../secrets/sec-003.md) | Argo CD con un rol por AppProject y sin acceso por defecto (homelab-gitops, components/platform/argocd/patch-argocd-rbac-cm.yaml) |
| **K03** | Secrets Management Failures | Parcial | [SEC-001](../secrets/sec-001.md), [SEC-002](../secrets/sec-002.md), [SEC-003](../secrets/sec-003.md) | Secretos en OpenBao, fuera del clúster, materializados por External Secrets; nunca en Git |
| **K04** | Lack Of Cluster Level Policy Enforcement | Parcial | — | Kyverno aplica este estándar en todo el clúster; todas las reglas en Audit hasta pasar a Deny namespace a namespace |
| **K05** | Missing Network Segmentation Controls | Parcial | [NET-001](../network/net-001.md), [NET-002](../network/net-002.md), [NET-003](../network/net-003.md) | NetworkPolicies de homelab-hardening (homelab-gitops, components/platform/homelab-hardening); la salida sigue abierta fuera de homelab<br>Pendiente una regla que exija NetworkPolicy en cada namespace (no hay ValidatingPolicy oficial) |
| **K06** | Overly Exposed Kubernetes Components | Parcial | — | Argo CD, Grafana, Backstage y la interfaz de n8n solo por el Gateway interno (LAN); la única entrada desde Internet es el túnel de Cloudflare |
| **K07** | Misconfigured And Vulnerable Cluster Components | Parcial | — | k3s al día con system-upgrade-controller (homelab-gitops, components/platform/system-upgrade-plans)<br>Pendiente revisar la configuración del clúster contra CIS (kube-bench) |
| **K08** | Cluster To Cloud Lateral Movement | No aplica | — | El clúster corre en VMs propias, sin proveedor de nube ni metadatos de instancia; las credenciales de R2 viven fuera del clúster |
| **K09** | Broken Authentication Mechanisms | Parcial | — | SSO con Keycloak (OIDC con PKCE) en todas las interfaces (homelab-ansible, rol keycloak_identity)<br>Pendiente exigir segundo factor |
| **K10** | Inadequate Logging And Monitoring | Parcial | — | Prometheus, Alertmanager y Grafana; PolicyReports de Kyverno<br>Pendiente centralizar los registros de auditoría del API server |

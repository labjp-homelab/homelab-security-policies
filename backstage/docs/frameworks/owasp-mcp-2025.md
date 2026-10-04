<!-- GENERADO por tools/generate_guidelines.py desde policies/ y curation/. No editar a mano. -->
# OWASP MCP Top 10 2025 (v0.1, beta)

Referencia oficial: <https://owasp.github.io/www-project-mcp-top-10/>

Cobertura en el homelab: 0 cubierto, 7 parcial, 3 pendiente, 0 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/owasp-mcp-2025`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`curation/frameworks/owasp-mcp-2025.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno |
|----|--------|--------|-------------------|
| [MCP01](#mcp01) | Token Mismanagement & Secret Exposure | Parcial | [SEC-001](../secrets/sec-001.md), [SEC-002](../secrets/sec-002.md), [SEC-003](../secrets/sec-003.md), [SEC-004](../secrets/sec-004.md) |
| [MCP02](#mcp02) | Privilege Escalation via Scope Creep | Parcial | [RBAC-001](../rbac/rbac-001.md), [RBAC-003](../rbac/rbac-003.md), [RBAC-005](../rbac/rbac-005.md) |
| [MCP03](#mcp03) | Tool Poisoning | Pendiente | — |
| [MCP04](#mcp04) | Software Supply Chain Attacks & Dependency Tampering | Parcial | [IMG-001](../images/img-001.md), [IMG-002](../images/img-002.md), [IMG-003](../images/img-003.md) |
| [MCP05](#mcp05) | Command Injection & Execution | Pendiente | — |
| [MCP06](#mcp06) | Intent Flow Subversion | Parcial | — |
| [MCP07](#mcp07) | Insufficient Authentication & Authorization | Parcial | [AI-001](../ai/ai-001.md), [NET-006](../network/net-006.md) |
| [MCP08](#mcp08) | Lack of Audit and Telemetry | Parcial | — |
| [MCP09](#mcp09) | Shadow MCP Servers | Parcial | [AI-001](../ai/ai-001.md) |
| [MCP10](#mcp10) | Context Injection & Over-Sharing | Pendiente | — |

## MCP01

**Token Mismanagement & Secret Exposure** · Parcial

**Reglas de Kyverno**

- [SEC-001 · Secretos montados, no en variables de entorno](../secrets/sec-001.md)
- [SEC-002 · Sin tokens de ServiceAccount de larga vida](../secrets/sec-002.md)
- [SEC-003 · Sin montar el token de la ServiceAccount por defecto](../secrets/sec-003.md)
- [SEC-004 · Sin secretos en ConfigMaps](../secrets/sec-004.md)

**Otros controles del homelab**

- Tokens de corta duración emitidos por Keycloak; secretos en OpenBao vía External Secrets

## MCP02

**Privilege Escalation via Scope Creep** · Parcial

**Reglas de Kyverno**

- [RBAC-001 · Sin enlaces a cluster-admin](../rbac/rbac-001.md)
- [RBAC-003 · Sin verbos de escalada en roles](../rbac/rbac-003.md)
- [RBAC-005 · Sin verbos comodín en roles](../rbac/rbac-005.md)

**Otros controles del homelab**

- Un rol mcp:tool:<destino>_<herramienta> por herramienta en Keycloak, que agentgateway exige en cada tools/call (homelab-gitops, components/platform/agentgateway-config/policy-mcp-backend.yaml)

## MCP03

**Tool Poisoning** · Pendiente

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- La demo de Black Alpaca lo muestra; no hay control en el homelab

## MCP04

**Software Supply Chain Attacks & Dependency Tampering** · Parcial

**Reglas de Kyverno**

- [IMG-001 · Sin el tag latest](../images/img-001.md)
- [IMG-002 · Imagen fijada por digest](../images/img-002.md)
- [IMG-003 · Solo registries conocidos](../images/img-003.md)

**Otros controles del homelab**

- Imágenes firmadas con Tekton Chains y servidas desde Zot

## MCP05

**Command Injection & Execution** · Pendiente

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Pendiente validar la entrada en cada servidor MCP; las reglas de pods solo acotan el daño

## MCP06

**Intent Flow Subversion** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Solo en la demo de Black Alpaca, sesión 2 (aprobación humana antes de actuar)

## MCP07

**Insufficient Authentication & Authorization** · Parcial

**Reglas de Kyverno**

- [AI-001 · Servidores MCP solo por la pasarela de agentes](../ai/ai-001.md)
- [NET-006 · Rutas externas con login o públicas a propósito](../network/net-006.md)

**Otros controles del homelab**

- JWT de Keycloak en la entrada de agentgateway y autorización por herramienta (policy-jwt.yaml, policy-mcp-backend.yaml)
- Pendiente validar el flujo de punta a punta agente → agentgateway → servidor MCP

## MCP08

**Lack of Audit and Telemetry** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Métricas en Prometheus; pendiente la traza de punta a punta de cada llamada a herramienta

## MCP09

**Shadow MCP Servers** · Parcial

**Reglas de Kyverno**

- [AI-001 · Servidores MCP solo por la pasarela de agentes](../ai/ai-001.md)

**Otros controles del homelab**

- Los servidores solo se federan en agentgateway (homelab-gitops, components/platform/agentgateway-config/backend-mcp.yaml)

## MCP10

**Context Injection & Over-Sharing** · Pendiente

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

Ninguno.

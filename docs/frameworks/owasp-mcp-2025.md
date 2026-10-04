<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# OWASP MCP Top 10 2025 (v0.1, beta)

Referencia oficial: <https://owasp.github.io/www-project-mcp-top-10/>

Cobertura en el homelab: 0 cubierto, 7 parcial, 3 pendiente, 0 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/owasp-mcp-2025`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`frameworks/owasp-mcp-2025.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno | Otros controles del homelab |
|----|--------|--------|-------------------|-----------------------------|
| **MCP01** | Token Mismanagement & Secret Exposure | Parcial | [SEC-001](../secrets/sec-001.md), [SEC-002](../secrets/sec-002.md), [SEC-003](../secrets/sec-003.md) | Tokens de corta duración emitidos por Keycloak; secretos en OpenBao vía External Secrets |
| **MCP02** | Privilege Escalation via Scope Creep | Parcial | [RBAC-001](../rbac/rbac-001.md), [RBAC-003](../rbac/rbac-003.md), [RBAC-005](../rbac/rbac-005.md) | Scopes mcp:* por herramienta en Keycloak (homelab-ansible, keycloak_service_accounts) |
| **MCP03** | Tool Poisoning | Pendiente | — | La demo de Black Alpaca lo muestra; no hay control en el homelab |
| **MCP04** | Software Supply Chain Attacks & Dependency Tampering | Parcial | [IMG-001](../images/img-001.md), [IMG-002](../images/img-002.md), [IMG-003](../images/img-003.md) | Imágenes firmadas con Tekton Chains y servidas desde Zot |
| **MCP05** | Command Injection & Execution | Pendiente | — | Pendiente validar la entrada en cada servidor MCP; las reglas de pods solo acotan el daño |
| **MCP06** | Intent Flow Subversion | Parcial | — | Solo en la demo de Black Alpaca, sesión 2 (aprobación humana antes de actuar) |
| **MCP07** | Insufficient Authentication & Authorization | Parcial | — | AuthPolicy de Kuadrant en el MCP Gateway y JWT en agentgateway<br>Pendiente cerrar el flujo agente → agentgateway → MCP Gateway (tools/call aún no se reenvía) |
| **MCP08** | Lack of Audit and Telemetry | Parcial | — | Métricas en Prometheus; pendiente la traza de punta a punta de cada llamada a herramienta |
| **MCP09** | Shadow MCP Servers | Parcial | — | Los servidores se registran en el MCP Gateway (homelab-gitops, components/platform/mcp-gateway)<br>Pendiente una regla que impida servidores MCP fuera del registro |
| **MCP10** | Context Injection & Over-Sharing | Pendiente | — | — |

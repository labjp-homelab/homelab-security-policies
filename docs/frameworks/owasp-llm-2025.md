<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# OWASP Top 10 for LLM Applications 2025

Referencia oficial: <https://genai.owasp.org/llm-top-10/>

Cobertura en el homelab: 0 cubierto, 6 parcial, 2 pendiente, 2 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/owasp-llm-2025`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`frameworks/owasp-llm-2025.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno | Otros controles del homelab |
|----|--------|--------|-------------------|-----------------------------|
| **LLM01** | Prompt Injection | Parcial | — | Solo en la demo de Black Alpaca, sesión 2 (revisor azul y aprobación humana antes de desplegar) |
| **LLM02** | Sensitive Information Disclosure | Parcial | — | Los agentes reciben tokens acotados por scopes mcp:* de Keycloak, no credenciales de las aplicaciones |
| **LLM03** | Supply Chain | Parcial | [IMG-001](../images/img-001.md), [IMG-002](../images/img-002.md), [IMG-003](../images/img-003.md) | Imágenes firmadas con Tekton Chains y servidas desde Zot<br>Pendiente verificar los pesos del modelo descargado |
| **LLM04** | Data and Model Poisoning | No aplica | — | No se entrena ni se ajusta ningún modelo; se sirve el publicado |
| **LLM05** | Improper Output Handling | Parcial | — | Solo en la demo de Black Alpaca, sesión 2 (la salida del agente no se aplica sin aprobación humana en Git) |
| **LLM06** | Excessive Agency | Parcial | — | Cada agente de kagent declara sus herramientas; el de diagnóstico de Kubernetes es de solo lectura<br>Scopes mcp:* por herramienta en Keycloak (p. ej. mcp:ocr:read) |
| **LLM07** | System Prompt Leakage | Pendiente | — | — |
| **LLM08** | Vector and Embedding Weaknesses | No aplica | — | No hay base de datos vectorial ni RAG |
| **LLM09** | Misinformation | Pendiente | — | — |
| **LLM10** | Unbounded Consumption | Parcial | [WKL-002](../workloads/wkl-002.md) | RateLimitPolicy de Kuadrant en agents.labjp.xyz y en el MCP Gateway (homelab-gitops, components/platform/agentgateway-config y mcp-gateway) |

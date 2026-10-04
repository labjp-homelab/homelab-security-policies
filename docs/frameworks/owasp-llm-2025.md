<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# OWASP Top 10 for LLM Applications 2025

Referencia oficial: <https://genai.owasp.org/llm-top-10/>

Cobertura en el homelab: 0 cubierto, 6 parcial, 2 pendiente, 2 no aplica.

- **Reglas de Kyverno**: las políticas de este estándar que cubren el punto (sale de sus
  anotaciones `security.labjp.xyz/owasp-llm-2025`). Mientras estén en `Audit`, informan sin impedir.
- **Otros controles del homelab**: lo que lo cubre fuera de Kyverno y dónde se gestiona, o
  lo que falta (`frameworks/owasp-llm-2025.yaml`).

| ID | Riesgo | Estado | Reglas de Kyverno |
|----|--------|--------|-------------------|
| [LLM01](#llm01) | Prompt Injection | Parcial | — |
| [LLM02](#llm02) | Sensitive Information Disclosure | Parcial | — |
| [LLM03](#llm03) | Supply Chain | Parcial | [IMG-001](../images/img-001.md), [IMG-002](../images/img-002.md), [IMG-003](../images/img-003.md) |
| [LLM04](#llm04) | Data and Model Poisoning | No aplica | — |
| [LLM05](#llm05) | Improper Output Handling | Parcial | — |
| [LLM06](#llm06) | Excessive Agency | Parcial | [AI-001](../ai/ai-001.md) |
| [LLM07](#llm07) | System Prompt Leakage | Pendiente | — |
| [LLM08](#llm08) | Vector and Embedding Weaknesses | No aplica | — |
| [LLM09](#llm09) | Misinformation | Pendiente | — |
| [LLM10](#llm10) | Unbounded Consumption | Parcial | [WKL-002](../workloads/wkl-002.md) |

## LLM01

**Prompt Injection** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Solo en la demo de Black Alpaca, sesión 2 (revisor azul y aprobación humana antes de desplegar)

## LLM02

**Sensitive Information Disclosure** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Los agentes reciben tokens de Keycloak acotados a sus roles mcp:tool:*, no credenciales de las aplicaciones

## LLM03

**Supply Chain** · Parcial

**Reglas de Kyverno**

- [IMG-001 · Sin el tag latest](../images/img-001.md)
- [IMG-002 · Imagen fijada por digest](../images/img-002.md)
- [IMG-003 · Solo registries conocidos](../images/img-003.md)

**Otros controles del homelab**

- Imágenes firmadas con Tekton Chains y servidas desde Zot
- Pendiente verificar los pesos del modelo descargado

## LLM04

**Data and Model Poisoning** · No aplica

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- No se entrena ni se ajusta ningún modelo; se sirve el publicado

## LLM05

**Improper Output Handling** · Parcial

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- Solo en la demo de Black Alpaca, sesión 2 (la salida del agente no se aplica sin aprobación humana en Git)

## LLM06

**Excessive Agency** · Parcial

**Reglas de Kyverno**

- [AI-001 · Servidores MCP solo por la pasarela de agentes](../ai/ai-001.md)

**Otros controles del homelab**

- Cada agente de kagent declara sus herramientas; el de diagnóstico de Kubernetes es de solo lectura
- Un rol mcp:tool:* por herramienta, exigido por agentgateway en cada tools/call

## LLM07

**System Prompt Leakage** · Pendiente

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

Ninguno.

## LLM08

**Vector and Embedding Weaknesses** · No aplica

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

- No hay base de datos vectorial ni RAG

## LLM09

**Misinformation** · Pendiente

**Reglas de Kyverno**

Ninguna: Kyverno solo ve los objetos de la API de Kubernetes y este punto se cubre fuera de ella.

**Otros controles del homelab**

Ninguno.

## LLM10

**Unbounded Consumption** · Parcial

**Reglas de Kyverno**

- [WKL-002 · Requests y límite de memoria](../workloads/wkl-002.md)

**Otros controles del homelab**

- RateLimitPolicy de Kuadrant en agents.labjp.xyz y cupo por usuario en /mcp de agentgateway (homelab-gitops, components/platform/agentgateway-config)

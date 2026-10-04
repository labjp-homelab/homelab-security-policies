<!-- GENERADO por tools/generate_guidelines.py desde policies/ y curation/. No editar a mano. -->
# Lineamientos de seguridad del homelab

39 reglas, cada una una `ValidatingPolicy` de Kyverno en
[`policies/`](https://github.com/labjp-homelab/homelab-security-policies/tree/main/policies): 34 de la biblioteca oficial de
Kyverno y 5 propias del homelab (`curation/custom/`), para lo que la biblioteca no cubre. Lo
que se lee aquí y lo que aplica el clúster salen del mismo archivo (ver
[Fuente de verdad](source-of-truth.md)).

`Audit` informa en los PolicyReports sin bloquear; `Deny` rechaza en la admisión.

## Marcos de referencia

Qué cubre el homelab de cada marco, con estas reglas y con otros controles (Keycloak,
OpenBao, Kuadrant, agentgateway...). El detalle de cada punto, en su página.

| Marco | Cubierto | Parcial | Pendiente | No aplica |
|-------|----------|---------|-----------|-----------|
| [OWASP Kubernetes Top 10 2025](frameworks/owasp-k8s-2025.md) | 0 | 9 | 0 | 1 |
| [OWASP Top 10 for LLM Applications 2025](frameworks/owasp-llm-2025.md) | 0 | 6 | 2 | 2 |
| [OWASP MCP Top 10 2025 (v0.1, beta)](frameworks/owasp-mcp-2025.md) | 0 | 7 | 3 | 0 |
| [PCI DSS 4.0.1 (referencia)](frameworks/pci-dss-4.0.1.md) | 0 | 9 | 1 | 2 |

## Seguridad de pods · Baseline

Pod Security Standards nivel Baseline: impide las escaladas de privilegios conocidas (contenedores privilegiados, namespaces y rutas del nodo).

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [POD-001](pod-security-baseline/pod-001.md) | Sin contenedores privilegiados | high | Audit |
| [POD-002](pod-security-baseline/pod-002.md) | Sin namespaces del nodo | high | Audit |
| [POD-003](pod-security-baseline/pod-003.md) | Sin volúmenes hostPath | high | Audit |
| [POD-004](pod-security-baseline/pod-004.md) | Sin puertos del nodo | medium | Audit |
| [POD-005](pod-security-baseline/pod-005.md) | Sin HostProcess de Windows | high | Audit |
| [POD-006](pod-security-baseline/pod-006.md) | Solo capabilities del conjunto Baseline | high | Audit |
| [POD-007](pod-security-baseline/pod-007.md) | /proc con máscara por defecto | medium | Audit |
| [POD-008](pod-security-baseline/pod-008.md) | Sin opciones SELinux personalizadas | medium | Audit |
| [POD-009](pod-security-baseline/pod-009.md) | Perfil seccomp no deshabilitado | medium | Audit |
| [POD-010](pod-security-baseline/pod-010.md) | Solo sysctls seguros | medium | Audit |

## Seguridad de pods · Restricted

Pod Security Standards nivel Restricted: endurecimiento de pods según las buenas prácticas actuales (sin root, sin capabilities, seccomp, volúmenes acotados).

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [POD-101](pod-security-restricted/pod-101.md) | Los contenedores no corren como root | high | Audit |
| [POD-102](pod-security-restricted/pod-102.md) | Ningún uid 0 explícito | high | Audit |
| [POD-103](pod-security-restricted/pod-103.md) | Sin escalada de privilegios | high | Audit |
| [POD-104](pod-security-restricted/pod-104.md) | Sin capabilities (salvo NET_BIND_SERVICE) | medium | Audit |
| [POD-105](pod-security-restricted/pod-105.md) | seccomp RuntimeDefault o Localhost | medium | Audit |
| [POD-106](pod-security-restricted/pod-106.md) | Solo tipos de volumen seguros | medium | Audit |

## Cargas de trabajo

Recursos, sistema de archivos y ubicación de las cargas.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [WKL-001](workloads/wkl-001.md) | Raíz de solo lectura | medium | Audit |
| [WKL-002](workloads/wkl-002.md) | Requests y límite de memoria | medium | Audit |
| [WKL-003](workloads/wkl-003.md) | Nada en el namespace default | low | Audit |
| [WKL-004](workloads/wkl-004.md) | Sin el socket del runtime | high | Audit |

## Imágenes y cadena de suministro

De dónde vienen las imágenes y cómo se fijan.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [IMG-001](images/img-001.md) | Sin el tag latest | high | Audit |
| [IMG-002](images/img-002.md) | Imagen fijada por digest | medium | Audit |
| [IMG-003](images/img-003.md) | Solo registries conocidos | medium | Audit |

## Red y exposición de servicios

Cómo se exponen los servicios fuera del clúster.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [NET-001](network/net-001.md) | Sin Services NodePort | medium | Audit |
| [NET-002](network/net-002.md) | Sin externalIPs en Services | high | Audit |
| [NET-003](network/net-003.md) | Sin Services ExternalName a localhost | medium | Audit |
| [NET-004](network/net-004.md) | Cada namespace con NetworkPolicy | high | Audit |
| [NET-005](network/net-005.md) | LoadBalancer solo para el Gateway | medium | Audit |
| [NET-006](network/net-006.md) | Rutas externas con login o públicas a propósito | high | Audit |

## Permisos (RBAC)

Quién puede hacer qué en el clúster.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [RBAC-001](rbac/rbac-001.md) | Sin enlaces a cluster-admin | high | Audit |
| [RBAC-002](rbac/rbac-002.md) | Sin enlaces a grupos del sistema | high | Audit |
| [RBAC-003](rbac/rbac-003.md) | Sin verbos de escalada en roles | high | Audit |
| [RBAC-004](rbac/rbac-004.md) | Sin acceso a nodes/proxy | high | Audit |
| [RBAC-005](rbac/rbac-005.md) | Sin verbos comodín en roles | medium | Audit |

## Secretos

Cómo llegan los secretos a las cargas.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [SEC-001](secrets/sec-001.md) | Secretos montados, no en variables de entorno | medium | Audit |
| [SEC-002](secrets/sec-002.md) | Sin tokens de ServiceAccount de larga vida | medium | Audit |
| [SEC-003](secrets/sec-003.md) | Sin montar el token de la ServiceAccount por defecto | medium | Audit |
| [SEC-004](secrets/sec-004.md) | Sin secretos en ConfigMaps | high | Audit |

## IA y MCP

Con qué servidores MCP pueden hablar los agentes.

| ID | Regla | Severidad | Modo |
|----|-------|-----------|------|
| [AI-001](ai/ai-001.md) | Servidores MCP solo por la pasarela de agentes | high | Audit |

<!-- GENERADO por tools/generate_guidelines.py desde policies/ y frameworks/. No editar a mano. -->
# Fuente de verdad

**La fuente de verdad son las políticas de Kyverno de [`homelab-security-policies`](https://github.com/labjp-homelab/homelab-security-policies)**,
en `policies/`. Todo lo demás se deriva de ellas; nada se escribe aparte.

```
biblioteca oficial de Kyverno (github.com/kyverno/policies, commit fijado)
        │  curation.yaml: qué reglas adoptamos + ID, categoría, textos, marcos, casos de prueba
        ▼  tools/vendor_policies.py
policies/<categoría>/validatingpolicy-<id>-<nombre>.yaml   ◀── FUENTE DE VERDAD
        │
        ├──▶ Argo CD del homelab: las aplica en el clúster (tag fijado, modo Audit)
        ├──▶ tests/kubernetes: kyverno test (cada regla con su caso que cumple y el que no)
        ├──▶ pipelines: kyverno apply antes del build (shift-left)
        └──▶ tools/generate_guidelines.py
                ├─ docs/ + mkdocs.yml   ──▶ TechDocs en Backstage (personas)
                └─ catalog-info.yaml    ──▶ catálogo de Backstage, una entidad por regla
                                              └──▶ agentes A2A, por el MCP de Backstage

frameworks/<marco>.yaml (a mano): puntos de OWASP Kubernetes, LLM y MCP Top 10 y PCI DSS,
su estado y lo que los cubre fuera de Kyverno ──▶ una página y una entidad por marco
```

| Quién | Lee | Por qué así |
|-------|-----|-------------|
| Kyverno (clúster) | las políticas, por Argo CD | es lo que de verdad se aplica |
| Personas | estas páginas (TechDocs) | explicación, remedio y la expresión exacta |
| Agentes A2A | la entidad de la regla, por el MCP de Backstage | leen la regla y su condición, no la prosa: un texto alterado no cambia lo que recomiendan |

## Cambiar una regla

1. Editar `curation.yaml` (adoptar o retirar una regla, sus textos, sus marcos o sus casos
   de prueba) o `frameworks/` (estado de un punto y lo que lo cubre fuera de Kyverno).
2. `tools/vendor_policies.py` regenera `policies/` y el test; `kyverno test tests/kubernetes`.
3. `tools/generate_guidelines.py` regenera estas páginas y el catálogo.
4. Publicar un tag; el homelab lo adopta cambiando `targetRevision` de su Application.

---
name: find-component
description: Busca en el vault componentes/recursos que cubran una necesidad y devuelve candidatos con source_url.
---

Necesidad del usuario: **$ARGUMENTS**

Encuentra los mejores recursos del UI Components Vault para esta necesidad.

1. Usa el agente `component-discovery` (o, si trabajas directo, la skill `vault-navigator`) para consultar `data/consolidated.json` por categoría y por keyword, ampliando a `sites/<slug>/raw/*.json` si hace falta.
2. Rankea por: ajuste semántico → framework objetivo (si el usuario lo indicó) → especificidad → trazabilidad.
3. Descarta cualquier candidato sin `source_url`.

Devuelve una tabla con los 5–8 mejores:

| # | Componente | Sitio | Framework | Install | Categoría | source_url |
|---|---|---|---|---|---|---|

Cierra con una recomendación breve y, si aplica, qué especialista debería implementarlo (`animation-motion-specialist`, `webgl-3d-specialist`, `creative-effects-specialist`). Si no hay coincidencias, dilo y sugiere la categoría/sitio más cercano sin inventar.

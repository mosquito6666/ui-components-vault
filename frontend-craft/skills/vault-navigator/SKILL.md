---
name: vault-navigator
description: >
  Mapa maestro del UI Components Vault: cómo está organizado y cómo consultarlo. Úsala siempre que
  necesites ENCONTRAR un recurso de UI/animación/3D, entender el esquema de data/consolidated.json,
  filtrar por categoría/sitio/framework/tags, o leer los scrapes en sites/*/raw. Es la skill de
  entrada para cualquier trabajo con el vault.
---

# Vault Navigator

El **UI Components Vault** cura 10 librerías de UI/animación/3D. Esta skill explica su modelo de
datos y cómo consultarlo eficientemente.

## Estructura del repo

```
data/consolidated.json     # fuente de verdad filtrable (esquema v2)
categories/NN_*.md          # vista por tema (esquema canónico 00..08)
sites/<slug>/_index.md      # vista por librería: framework + install + catálogo
sites/<slug>/raw/*.json     # scrape original (campo markdown, con snippets cuando existen)
sites/<slug>/_meta.json     # metadata del scrape
_index.md / _meta.json      # índices maestros
scripts/build_vault.py      # regenera todo OFFLINE desde raw/ (idempotente)
```

## Esquema de `data/consolidated.json` (v2)

```jsonc
{
  "metadata": { "total_sites", "total_components", "generated_at", "schema_version": 2, "categories": [...] },
  "components": [
    {
      "name", "slug", "site",
      "framework",        // React+Tailwind | Svelte+Three.js | Vanilla/React | Web components ...
      "install_cmd",      // comando concreto o null
      "install_pattern",  // copy-paste | registry | npm | embed
      "snippet",          // código del origen o null (solo donde se scrapeó la página interna)
      "source_url",       // trazabilidad OBLIGATORIA
      "preview_url",
      "primary_category", // buttons|backgrounds|animations|colors|typography|interactions|3d_canvas|layout_cards|other
      "tags": [...],
      "confidence"
    }
  ],
  "by_category": { "<cat>": ["slug", ...] },
  "by_site":     { "<site>": <count> }
}
```

## Recetas de consulta (no cargues el JSON entero a contexto)

```bash
# Listar por categoría
python -c "import json;d=json.load(open('data/consolidated.json',encoding='utf-8'));[print(c['site'],'|',c['name'],'|',c['framework'],'|',c['source_url']) for c in d['components'] if c['primary_category']=='animations']"

# Buscar por keyword (nombre + tags)
python -c "import json;q='reveal';d=json.load(open('data/consolidated.json',encoding='utf-8'));[print(c['site'],c['name'],c['source_url']) for c in d['components'] if q in (c['name']+' '+' '.join(c['tags'])).lower()]"

# Filtrar por framework
python -c "import json;d=json.load(open('data/consolidated.json',encoding='utf-8'));[print(c['name'],c['site']) for c in d['components'] if 'Svelte' in c['framework']]"

# Conteos
python -c "import json;d=json.load(open('data/consolidated.json',encoding='utf-8'));print(d['by_site']);print({k:len(v) for k,v in d['by_category'].items()})"
```

Para snippets/install que no estén en el JSON, usa Grep sobre `sites/<slug>/raw/*.json`.

## Mapa rápido sitio → especialidad

| Sitio | Framework | Fuerte en |
|---|---|---|
| cult-ui | React+Tailwind | componentes animados (shadcn) |
| skiper-ui | React+Tailwind | **animaciones / scroll / hover / preloaders** |
| watermelon-ui | React | base + **100+ animados** |
| aliimam | React+Tailwind | **shaders / efectos creativos** |
| theatrejs | agnóstico | **motion design / animación JSON** |
| threlte | Svelte+Three.js | **3D / WebGL / física** |
| spline | Web/3D | **3D editor / embeds** |
| styleui | React/Svelte | templates / landing |
| 21st-community | React | **registro masivo (200+)** |
| peachweb | Web components | (scrape parcial) |

## Reglas

- **Sin `source_url`, no entra.** Nunca recomiendes algo sin trazabilidad.
- Snippet `null` = la página interna no fue scrapeada; ve al `source_url` para el código real.
- Para profundizar por dominio, salta a las skills: `animations-catalog`, `webgl-3d-catalog`, `creative-effects-catalog`, `component-registries`, `design-tokens`.
- Tras re-scrapear, corre `/vault-enrich`; valida con `/vault-sync`.

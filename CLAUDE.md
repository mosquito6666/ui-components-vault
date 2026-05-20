# UI Components Vault — Guía de desarrollo web

Repositorio curado de 10 librerías/directorios de UI components, agrupados por categoría con snippets, previews, configuraciones y animaciones.

## Navegación

- **`_index.md`** — entrada maestra. Métricas globales + cómo usar agentes/skills.
- **`categories/NN_<cat>.md`** — vista cruzada por tema. Esquema canónico (9 archivos): `00_overview`, `01_buttons`, `02_backgrounds`, `03_animations`, `04_colors`, `05_typography`, `06_interactions`, `07_3d_canvas`, `08_layout_cards`.
- **`sites/<slug>/`** — vista por librería original. `_index.md` (framework + install + catálogo), `_meta.json`, `raw/*.json` (Firecrawl).
- **`data/consolidated.json`** — fuente de verdad estructurada (esquema v2). Filtrable por `primary_category`/`framework`/`site`/`tags`; incluye `by_category` y `by_site`.

> Los archivos generados (`categories/*.md`, `sites/*/_index.md`, `_index.md`, `_meta.json`, `data/consolidated.json`) **no se editan a mano**: se regeneran con `scripts/build_vault.py` (ver _Actualización_). Llevan el aviso correspondiente.

## Plugin `frontend-craft` (super-skill de diseño frontend)

El vault expone un plugin instalable (`/plugin marketplace add .` → `/plugin install frontend-craft`) con:

- **Agentes** (`frontend-craft/agents/`): builders — `frontend-architect` (orquestador), `animation-motion-specialist`, `webgl-3d-specialist`, `creative-effects-specialist`, `component-discovery`, `design-system-tokens`; reviewers — `frontend-quality-reviewer`, `accessibility-motion-reviewer`. Flujo: builders construyen → reviewers validan.
- **Skills** (`frontend-craft/skills/`): `vault-navigator`, `animations-catalog`, `webgl-3d-catalog`, `creative-effects-catalog`, `component-registries`, `design-tokens`, `frontend-quality-standards`.
- **Comandos** (`frontend-craft/commands/`): `/find-component`, `/build-ui`, `/animate`, `/vault-enrich`, `/vault-sync`.

## Cómo elegir componente

1. `/find-component "<necesidad>"` o consulta `data/consolidated.json` / `categories/` por tema.
2. Cada registro: `name · site · framework · install_cmd · snippet · source_url · preview_url · primary_category · tags`.
3. Verificar framework (React/Svelte/Vanilla/Web components) contra tu stack.
4. Abrir `source_url` para el código/demo oficial (snippet `null` = página interna no scrapeada).

## Frameworks por sitio

| Sitio | Framework | Patrón | Instalar |
|-------|-----------|--------|----------|
| cult-ui | React + Tailwind | copy-paste registry | `npx shadcn add` |
| threlte | Svelte | npm packages | `npm i @threlte/*` |
| theatrejs | Vanilla/React | npm library | `npm i @theatre/*` |
| 21st | React | components + hooks | copy-paste |
| styleui | React/Svelte | registry | various |
| spline | Web/3D | cloud canvas | embed iframes |
| watermelon | React | registry | copy-paste |
| skiper-ui | React | Tailwind | copy-paste |
| aliimam | React | Tailwind + Storybook | copy-paste |
| peachweb | Web components | HTML5 | `npm i peachweb` |

## Estructura de secciones

Cada categoría contiene:

- **Descripción** — qué entra en esta categoría.
- **Tabla de componentes** — sitio, nombre, framework, install, snippet, preview, link a source.
- **Alternativas equivalentes** — mismo patrón en N sitios.
- **Config global** — colores recurrentes, animaciones frecuentes, tipografía recomendada.

## Convenciones

- **Snippets**: tal cual del origen. Sin ediciones; si la sintaxis difiere, anotado.
- **Colores**: preservados en oklch/hsl/hex originales. Incluir CSS custom properties.
- **Sin source_url, no entra**: trazabilidad obligatoria.
- **Animaciones**: nombradas (spring, scroll-reveal, marquee, fade-in). Incluir parámetros.
- **3D/Canvas**: threlte, theatre, spline. Incluir links a playgrounds + embed.

## Para el desarrollo

1. **Busca por categoría** → encuentra N alternativas.
2. **Verifica el framework** → ¿React? ¿Svelte? ¿vanilla JS?
3. **Copia el snippet** → instala dependencias listadas.
4. **Ajusta a tu design system** → colores/tipografía en `04_colors.md` y `05_typography.md`.
5. **Valida en preview_url** → antes de integrar.

## Actualización

El contenido derivado se regenera **offline** desde `sites/*/raw/*.json` con un único motor idempotente:

```bash
python scripts/build_vault.py --all          # regenera todo (default)
python scripts/build_vault.py --site threlte # un sitio (+ índices globales)
python scripts/build_vault.py --category 3   # una categoría (+ índices)
python scripts/build_vault.py --check         # dry-run: reporta discrepancias (exit!=0)
```

O vía comandos del plugin: `/vault-enrich [args]` y `/vault-sync`.

**Re-scrapear** un sitio (traer nuevo `raw/*.json`) requiere red: usa la skill `firecrawl-web` y guarda el resultado en `sites/<slug>/raw/`; luego corre `build_vault.py`. El script de scraping de red no está versionado aquí; el enriquecimiento/consolidación es 100% offline.

### Esquema de `data/consolidated.json` (v2)

```jsonc
{
  "metadata": { "total_sites", "total_components", "generated_at", "schema_version": 2, "categories": [...] },
  "components": [ { "name","slug","site","framework","install_cmd","install_pattern",
                    "snippet","source_url","preview_url","primary_category","tags","confidence" } ],
  "by_category": { "<cat>": ["slug", ...] },
  "by_site":     { "<site>": <count> }
}
```

## Créditos y licencias

Cada componente lleva su `source_url` e información de licencia en el JSON. Respetar términos de uso de cada librería.

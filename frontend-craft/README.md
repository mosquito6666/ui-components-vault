# frontend-craft

Super-skill de **diseño frontend de máximo detalle** construida sobre el **UI Components Vault** (10 librerías de UI / animación / 3D curadas y enriquecidas en `data/consolidated.json` + `categories/` + `sites/`).

El plugin convierte el vault en un equipo de agentes y un cuerpo de conocimiento que **encuentra, ensambla y revisa** interfaces de alta calidad — animaciones (JSON/Theatre.js, scroll, hover), 3D/WebGL (Threlte, Spline), efectos/shaders, registries de componentes y design tokens.

## Qué incluye

### 🤖 8 agentes (mega-prompts) — builders + reviewers que se complementan

**Builders**
- `frontend-architect` — orquestador maestro: elige stack, descompone la UI, delega en especialistas, ensambla y coordina el loop build→review.
- `animation-motion-specialist` — Skiper UI · Watermelon · Theatre.js: scroll-reveal, hover/gooey, spring, marquee, preloaders, text/number animation, timelines.
- `webgl-3d-specialist` — Threlte (Svelte+Three.js+Rapier+GLTF) · Spline (embeds) · R3F: composición de escena y performance WebGL.
- `creative-effects-specialist` — Aliimam shaders/canvas: swirl, liquid, ripple, pixel-grid, patterns, typewriter.
- `component-discovery` — retrieval: busca en el vault y devuelve candidatos rankeados con `source_url` + install.
- `design-system-tokens` — colores (oklch/hsl/hex), tipografía, spacing, CSS custom properties, theming.

**Reviewers**
- `frontend-quality-reviewer` — correctitud, idiomática del framework, responsive, performance, integridad del snippet vs `source_url`.
- `accessibility-motion-reviewer` — WCAG 2.1 AA + `prefers-reduced-motion`, jank, 60fps.

### 📚 7 skills de conocimiento (auto-cargadas por contexto)
`vault-navigator` · `animations-catalog` · `webgl-3d-catalog` · `creative-effects-catalog` · `component-registries` · `design-tokens` · `frontend-quality-standards`.

### ⚡ 5 comandos de workflow
`/find-component` · `/build-ui` · `/animate` · `/vault-enrich` · `/vault-sync`.

> 📖 **Instructivo detallado de comandos, agentes y skills:** ver [USAGE.md](./USAGE.md).

## Instalación

Desde la raíz del vault (este repositorio):

```
/plugin marketplace add .
/plugin install frontend-craft
```

(O apunta a la ruta absoluta del repo: `/plugin marketplace add <ruta-a>/ui-components-vault`.)

Verifica con `/help` (comandos) y `/agents` (agentes).

## Flujo recomendado

1. `/find-component "scroll reveal de texto"` → candidatos con `source_url`.
2. `/build-ui "hero con escena 3D y texto en scroll-reveal"` → arquitecto + especialistas ensamblan.
3. Revisión automática (`frontend-quality-reviewer`, `accessibility-motion-reviewer`).
4. `/vault-enrich` tras re-scrapear; `/vault-sync` para verificar consistencia.

## Datos que consume

- `data/consolidated.json` — fuente de verdad filtrable (`by_category`, `by_site`, `tags`, `framework`, `install_cmd`, `source_url`).
- `categories/NN_*.md` — vista por tema (esquema canónico 00..08).
- `sites/<slug>/_index.md` + `sites/<slug>/raw/*.json` — catálogo y scrape original por librería.

> Convención del vault: **sin `source_url`, no entra** (trazabilidad obligatoria). Los snippets se preservan tal cual del origen.

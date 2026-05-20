---
name: animations-catalog
description: >
  Catálogo y guía de animaciones web del vault: Skiper UI, Watermelon UI y Theatre.js. Úsala cuando
  necesites elegir y parametrizar MOTION — scroll-reveal, parallax, hover/gooey, spring, marquee,
  preloaders, texto/números animados o timelines/secuencias JSON. Incluye taxonomía, parámetros
  recomendados y reglas de accesibilidad/performance.
---

# Animations Catalog

Conocimiento de animación web sobre tres fuentes del vault.

## Fuentes

- **Skiper UI** — React+Tailwind, copy-paste. `sites/skiper-ui/`. Scroll effects (parallax, card stack, text/image reveal, timeline), crazy hover, preloaders, minimal interactions (rolling text, números, toggles).
- **Watermelon UI** — React. `sites/watermelon-ui/`. 100+ animated por categoría: action, cards, carousel, micro-interaction, lists, marketing, media, navigation, sliders, toggles, tooltip, widgets.
- **Theatre.js** — agnóstico (R3F/Three.js/HTML-SVG). `sites/theatrejs/`. Motion design profesional; **secuencias guardables/exportables como JSON**; sincronización con audio; scrubbing en el studio.

Filtra candidatos con la skill `vault-navigator` (categoría `animations`).

## Taxonomía → parámetros recomendados

| Patrón | Uso | Parámetros | Defaults sensatos |
|---|---|---|---|
| spring | drag, toggle, modal | stiffness, damping, mass | stiffness 170, damping 26 |
| scroll-reveal | entrada de secciones | threshold, offset, stagger, once | threshold 0.2, stagger 60ms, once true |
| parallax | profundidad | speed por capa | 0.1–0.4 |
| hover | affordance | duración, ease | 150–220ms, ease-out |
| gooey | identidad/marca | blur+contrast filter, duración | 200ms |
| marquee | tickers/logos | velocidad, gap, pausa-hover | 40–80 px/s, pausa on hover |
| preloader | carga inicial | duración máx, salida | ≤1.5s, fade-out 300ms |
| text reveal | titulares | stagger por carácter/palabra, ease | 30–50ms char, ease-out |
| number/counter | métricas | duración, ease, formato | 1–2s, ease-out |
| timeline (Theatre.js) | secuencias | sheet, objetos, keyframes, JSON | export JSON al repo |

## Theatre.js — patrón de animación por datos (JSON)

```
npm i @theatre/core @theatre/studio
```
1. Crea un `project` y un `sheet`.
2. Declara objetos con props animables (position, opacity, color…).
3. Define keyframes en el studio; exporta el **state JSON**.
4. En producción, carga el JSON y reproduce sin el studio. Ideal para hero sincronizado con scroll/audio y reutilizable entre frameworks.

## Reglas (siempre)

- **`prefers-reduced-motion: reduce`** con variante atenuada/instant. No negociable.
- Anima solo **`transform` y `opacity`**; evita `width/height/top/left`.
- 60fps; `will-change` con criterio; stagger ≤6 elementos visibles.
- Easing intencional (entradas ease-out, salidas ease-in; `linear` solo en loops).
- Conserva el `source_url`; preserva el snippet del origen y anota adaptaciones.

Para implementar, delega en el agente `animation-motion-specialist`. Para revisar, `accessibility-motion-reviewer`.

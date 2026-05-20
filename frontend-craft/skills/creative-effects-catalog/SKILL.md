---
name: creative-effects-catalog
description: >
  Catálogo de efectos visuales creativos 2D del vault: shaders de canvas/fragment, fondos
  generativos, patterns y micro-efectos de marca (Aliimam + categoría backgrounds). Úsala para
  dithered swirl, liquid wave, ripple, pixel-grid, dot/grid patterns, render canvas, shine border,
  gradient bars, glow/spotlight. Incluye reglas de coste GPU, fallback y contraste.
---

# Creative Effects & Shaders Catalog

## Fuentes

- **Aliimam** — React+Tailwind. `sites/aliimam/`.
  - Shaders: **Dithered Swirl, Liquid Wave, PixelGrid, Ripple**.
  - Creativos: **Render Canvas, Dot Pattern, Grid Pattern, Gradient Bars, Shine Border, Border Glow, Marquee, Typewriter, Counter Number, Gauge**.
- Categoría `backgrounds` del vault (`categories/02_backgrounds.md`) para fondos complementarios.

Filtra: `sites/aliimam/` o `vault-navigator` con `site == 'aliimam'`.

## Catálogo de efectos → rol y coste

| Efecto | Rol típico | Coste | Notas |
|---|---|---|---|
| Dithered Swirl | fondo de hero | alto (shader full-screen) | limitar área/resolución |
| Liquid Wave | separador / fondo | alto | pausar fuera de viewport |
| Ripple | interacción puntual | medio | trigger por evento |
| PixelGrid | fondo retro | medio | densidad parametrizable |
| Dot/Grid Pattern | textura sutil | bajo (CSS/SVG) | preferir cuando baste |
| Shine Border / Border Glow | énfasis de card/CTA | bajo-medio | respetar contraste |
| Gradient Bars | data-viz / acento | bajo | — |
| Render Canvas | base genérica canvas | variable | controla rAF |

## Reglas

1. **Coste GPU controlado**: un fragment shader a pantalla completa consume continuamente. Limita área, baja resolución del buffer, pausa fuera de viewport y en `prefers-reduced-motion`.
2. **Fallback estático**: sin WebGL o en dispositivos débiles → gradiente/imagen equivalente.
3. **Detrás del contenido**: z-index/opacidad; el texto encima mantiene contraste **AA** (verifícalo).
4. **Parámetros expuestos**: velocidad, escala, color, densidad — con defaults documentados.
5. **Origen preservado**: snippet/shader tal cual del `source_url`; anota uniforms/adaptaciones.

Prefiere CSS/SVG (dot/grid pattern, gradients) cuando logren el efecto sin shader. Implementa con `creative-effects-specialist`; revisa contraste/motion con `accessibility-motion-reviewer`.

---
name: frontend-quality-standards
description: >
  La barra de calidad frontend del plugin: responsive, accesibilidad (WCAG 2.1 AA), performance,
  semántica, motion seguro e idiomática por framework. Úsala como referencia compartida al construir
  o revisar UI, para saber qué "de calidad" significa concretamente y qué verificar antes de dar
  algo por terminado. La consumen los builders y, sobre todo, los reviewers.
---

# Frontend Quality Standards

Definición operativa de "UI de calidad". Cada ítem es verificable.

## 1. Estructura & semántica
- Landmarks (`header/nav/main/footer/aside`), un solo `h1`, jerarquía de headings sin saltos.
- HTML semántico antes que `div` genéricos; ARIA solo cuando el HTML no alcanza.
- Componentes reutilizables, nombres claros, sin duplicación; tokens centralizados (no colores mágicos).

## 2. Responsive
- Breakpoints reales probados; sin overflow horizontal.
- Tipografía fluida (`clamp`) donde aporte; targets táctiles ≥44×44px.
- Imágenes responsivas (`srcset`/`sizes`), aspect-ratio reservado (sin CLS).

## 3. Accesibilidad (WCAG 2.1 AA)
- Contraste: texto ≥4.5:1, grande/UI ≥3:1 (incluye texto sobre fondos animados/3D/imágenes).
- Teclado completo; foco visible (`:focus-visible`); sin trampas de foco.
- Formularios con labels asociadas y errores anunciados.
- Información no dependiente solo de color.

## 4. Motion seguro
- `prefers-reduced-motion: reduce` con variante atenuada — **obligatorio**.
- Anima solo `transform/opacity`; 60fps; sin layout thrash.
- Auto-play >5s o loops: pausables (WCAG 2.2.2). Nada parpadea >3×/seg.

## 5. Performance
- LCP/CLS/INP sanos; 3D/animación no comprometen el LCP.
- Lazy-load de 3D/medios pesados; `dynamic import` para bundles grandes; tree-shaking.
- WebGL: pausa fuera de viewport, DPR ≤2, GLTF comprimido, `dispose()`.

## 6. Idiomática por framework
- **React**: keys estables, deps de efectos correctas, cleanup de listeners/observers, SSR/hydration seguras, evitar estado derivado.
- **Svelte**: reactividad correcta, stores apropiados, `onDestroy` limpia.
- **Vanilla**: sin fugas de listeners; idempotente al re-montar.

## 7. Trazabilidad (convención del vault)
- Cada componente externo conserva su `source_url`.
- Snippets **tal cual del origen**; toda adaptación queda anotada.

## Definition of Done
- [ ] Semántica + headings correctos
- [ ] Responsive sin overflow, targets ≥44px
- [ ] Contraste AA verificado (incl. sobre fondos animados)
- [ ] Teclado + foco visible
- [ ] `prefers-reduced-motion` presente
- [ ] Solo `transform/opacity` animados; 60fps
- [ ] LCP/CLS no comprometidos; 3D/medios lazy
- [ ] Idiomática del framework
- [ ] `source_url` conservado; adaptaciones anotadas

---
name: design-tokens
description: >
  Guía de design tokens del vault: color (oklch/hsl/hex), tipografía, spacing, radios, sombras y
  theming claro/oscuro como CSS custom properties. Úsala cuando definas o normalices el lenguaje
  visual de un proyecto, conviertas colores entre espacios, o crees una fuente única de verdad de
  tokens que los componentes consuman. Enlaza categories/04_colors.md y 05_typography.md.
---

# Design Tokens

Convierte intención de marca en tokens coherentes y accesibles. Fuente única de verdad que los
componentes consumen — nunca valores crudos sueltos.

## Fuentes del vault

- `categories/04_colors.md` — paletas/temas/tokens detectados (preservados en su espacio original).
- `categories/05_typography.md` — escalas y familias (21st, styleui).

## Estructura recomendada

**Primitivos** (paleta cruda) → **Semánticos** (rol) → **Componentes** (consumen semánticos).

```css
:root {
  /* primitivos (oklch preferido; hsl/hex de origen como referencia) */
  --blue-500: oklch(0.62 0.19 255);
  --gray-50:  oklch(0.98 0.005 255);
  --gray-900: oklch(0.21 0.02 255);

  /* semánticos */
  --color-bg:      var(--gray-50);
  --color-fg:      var(--gray-900);
  --color-accent:  var(--blue-500);
  --color-border:  oklch(0.9 0.01 255);
  --color-muted:   oklch(0.55 0.02 255);

  /* tipografía */
  --font-sans: "Inter", system-ui, sans-serif;
  --step-0: 1rem;            /* base */
  --step-1: 1.25rem;         /* ratio 1.25 */
  --step-2: 1.563rem;
  --step-3: 1.953rem;
  --leading-tight: 1.15; --leading-normal: 1.5;

  /* spacing / forma */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-4: 1rem; --space-8: 2rem;
  --radius-sm: 0.375rem; --radius-md: 0.5rem; --radius-lg: 1rem;
  --shadow-md: 0 4px 12px oklch(0 0 0 / 0.1);
}

[data-theme="dark"] {
  --color-bg: var(--gray-900);
  --color-fg: var(--gray-50);
  --color-border: oklch(0.32 0.02 255);
}
```

## Principios

1. **oklch primero** (uniformidad perceptual; estados hover/active más predecibles). Conserva hex/hsl de origen como comentario.
2. **Escala tipográfica modular** (ratio 1.2–1.333) con line-height/tracking por nivel.
3. **Spacing en escala 4/8**; radios/sombras tokenizados.
4. **Solo tokens semánticos en componentes**; los primitivos no se referencian directo.
5. **Contraste AA** en cada par fg/bg semántico (texto ≥4.5:1). Verifícalo y ajusta.

## Conversión de espacios de color

- Mantén el valor original (trazabilidad) + emite oklch para uso. Documenta el par.
- Para Tailwind, mapea los semánticos a `theme.extend.colors` apuntando a las CSS vars.

Implementa/normaliza con el agente `design-system-tokens`. Verifica contraste con `accessibility-motion-reviewer`.

---
name: animate
description: Añade o mejora una animación/micro-interacción en un elemento o sección, con prefers-reduced-motion.
---

Elemento o sección a animar: **$ARGUMENTS**

Aplica motion de calidad usando el catálogo del vault.

1. Carga la skill `animations-catalog` e identifica el **patrón** adecuado (scroll-reveal, hover, spring, marquee, parallax, text/number, timeline Theatre.js).
2. Con `component-discovery` localiza el componente equivalente (Skiper / Watermelon / Theatre.js) y trae su `source_url`.
3. Delega en `animation-motion-specialist` para implementar:
   - Snippet adaptado al stack (preservando el origen, anotando cambios).
   - **Tabla de parámetros** (duración, easing, stagger, threshold…).
   - Variante **`@media (prefers-reduced-motion: reduce)`** (obligatoria).
   - Solo animar `transform/opacity`; objetivo 60fps.
4. Pasa el resultado a `accessibility-motion-reviewer` para validar reduced-motion, pausabilidad y ausencia de jank.

Entrega: patrón elegido + justificación, snippet con source_url, tabla de parámetros, bloque reduced-motion y notas de performance.

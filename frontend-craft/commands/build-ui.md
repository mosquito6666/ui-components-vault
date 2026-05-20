---
name: build-ui
description: Ensambla una página/sección de calidad usando recursos del vault, orquestando especialistas y revisores.
---

Encargo de UI: **$ARGUMENTS**

Construye esto con calidad de portfolio usando el plugin frontend-craft.

1. **Arranca con `frontend-architect`** como orquestador. Si falta contexto crítico (stack, design system, claro/oscuro, breakpoints, marca), pregunta antes de construir.
2. **Descompón** la UI en bloques y mapea cada bloque a recursos del vault (vía `component-discovery` / `vault-navigator`). Verifica framework.
3. **Delega** por bloque:
   - motion / micro-interacciones → `animation-motion-specialist`
   - 3D / WebGL / Spline → `webgl-3d-specialist`
   - shaders / canvas / efectos → `creative-effects-specialist`
   - color / tipografía / tokens → `design-system-tokens`
4. **Ensambla** en código idiomático del framework, con tokens centralizados y snippets preservados del origen (anota adaptaciones).
5. **Revisión obligatoria** antes de entregar:
   - `frontend-quality-reviewer` (correctitud, responsive, performance, integridad de snippet vs source_url)
   - `accessibility-motion-reviewer` (WCAG AA + prefers-reduced-motion)
   Itera sobre los hallazgos (máx. 2 ciclos por bloque).
6. **Entrega**: plan de bloques, tabla de recursos (con source_url), código por archivo, notas de adaptación y una sección de **verificación** (cómo correr/ver y qué comprobar).

Aplica la skill `frontend-quality-standards` como Definition of Done.

# frontend-craft — Instructivo de uso

Manual de los **comandos**, **agentes** y **skills** del plugin. Para la visión general e instalación, ver el [README](./README.md).

---

## 1. Instalación

Desde la raíz del repositorio del vault:

```
/plugin marketplace add .
/plugin install frontend-craft
```

> Si el repo está en otra ruta: `/plugin marketplace add C:\ruta\a\ui-components-vault`.

Verifica:
- `/help` → deberían aparecer `/find-component`, `/build-ui`, `/animate`, `/vault-enrich`, `/vault-sync`.
- `/agents` → los 8 agentes del plugin.

Las **skills** no se invocan a mano: Claude las carga automáticamente cuando el contexto coincide con su `description`.

---

## 2. Comandos (workflow)

### `/find-component <necesidad>`
Busca recursos del vault que cubran una necesidad y devuelve candidatos rankeados **con `source_url`**.

```
/find-component scroll reveal de texto
/find-component toggle animado para React
/find-component fondo shader para un hero
```
**Devuelve:** tabla `# · Componente · Sitio · Framework · Install · Categoría · source_url` + recomendación. No escribe código.

---

### `/build-ui <descripción>`
Ensambla una página/sección de calidad orquestando arquitecto → especialistas → revisores.

```
/build-ui hero con escena 3D Threlte y titular en scroll-reveal, modo oscuro, React/Next
/build-ui pricing section con 3 planes, cards con shine border y entrada animada
```
**Flujo:** `frontend-architect` clarifica stack → descompone en bloques → delega en especialistas → ensambla → revisión obligatoria (`frontend-quality-reviewer` + `accessibility-motion-reviewer`).
**Devuelve:** plan de bloques, tabla de recursos (con source_url), código por archivo, notas de adaptación y verificación.
**Tip:** indica stack, design system, claro/oscuro y breakpoints para evitar preguntas.

---

### `/animate <elemento|sección>`
Añade o mejora una animación con `prefers-reduced-motion` incluido.

```
/animate el contador de métricas del dashboard
/animate las cards de features con entrada escalonada al hacer scroll
```
**Devuelve:** patrón elegido + justificación, snippet (con source_url), tabla de parámetros (duración/easing/stagger/threshold), bloque `@media (prefers-reduced-motion: reduce)` y notas de performance.

---

### `/vault-enrich [--all | --site <slug> | --category <n>]`
Regenera el contenido derivado del vault desde `sites/*/raw/*.json` (offline, idempotente).

```
/vault-enrich
/vault-enrich --site threlte
/vault-enrich --category 3
```
**Regenera:** `data/consolidated.json`, `categories/NN_*.md`, `sites/*/_index.md`, `_index.md`, `_meta.json`.
**Cuándo:** tras re-scrapear un sitio o cambiar la lógica de `scripts/build_vault.py`.

---

### `/vault-sync`
Verifica consistencia sin escribir nada (dry-run de `build_vault.py --check`).

```
/vault-sync
```
**Devuelve:** `0 discrepancias` (OK) o líneas `DIFF`/`FALTA`/`LEGACY`. Si hay deriva, corre `/vault-enrich`.
**Cuándo:** antes de commitear, tras un re-scrape, o tras editar el script.

---

## 3. Agentes

Se invocan solos cuando el trabajo encaja, o explícitamente: *"usa el agente `<name>` para…"*. Los comandos ya los orquestan.

### Builders
| Agente | Para qué | Fuentes del vault |
|---|---|---|
| `frontend-architect` | **Orquestador**: ensamblar páginas/secciones completas | todo el vault |
| `animation-motion-specialist` | motion, micro-interacciones, scroll, hover, timelines | skiper-ui, watermelon-ui, theatrejs |
| `webgl-3d-specialist` | escenas 3D, WebGL, física, embeds | threlte, spline, R3F |
| `creative-effects-specialist` | shaders, canvas, patterns, bordes vivos | aliimam, backgrounds |
| `component-discovery` | **buscar** componentes (retrieval rankeado) | consolidated.json, raw/ |
| `design-system-tokens` | color, tipografía, spacing, theming, CSS vars | 04_colors, 05_typography |

### Reviewers (validan lo que producen los builders)
| Agente | Revisa |
|---|---|
| `frontend-quality-reviewer` | correctitud, idiomática del framework, responsive, performance, **integridad del snippet vs source_url** |
| `accessibility-motion-reviewer` | WCAG 2.1 AA (contraste/teclado/foco/ARIA) + **prefers-reduced-motion**, jank, 60fps |

**Flujo típico:** un builder construye → entrega a los dos reviewers → itera sobre los hallazgos (máx. 2 ciclos).

Ejemplos:
```
Usa component-discovery para listar carouseles disponibles en React.
Pide a webgl-3d-specialist una escena con un modelo GLTF y cámara orbital.
Que frontend-quality-reviewer y accessibility-motion-reviewer revisen esta sección.
```

---

## 4. Skills (conocimiento bajo demanda)

Se cargan automáticamente; no se invocan a mano. Útil saber qué cubren:

| Skill | Cubre |
|---|---|
| `vault-navigator` | mapa del vault + esquema de `consolidated.json` + recetas de consulta |
| `animations-catalog` | taxonomía de animación + parámetros (Skiper/Watermelon/Theatre.js) |
| `webgl-3d-catalog` | setup 3D, escena, física, embeds, presupuesto de performance |
| `creative-effects-catalog` | shaders/canvas/patterns + coste GPU y fallbacks |
| `component-registries` | cómo instalar (shadcn/copy-paste/npm/templates) |
| `design-tokens` | tokens color/tipo/spacing + theming claro/oscuro |
| `frontend-quality-standards` | la barra de calidad / Definition of Done |

---

## 5. Flujo recomendado de principio a fin

```
1. /find-component "lo que necesito"      → veo candidatos con source_url
2. /build-ui "la sección que quiero"      → arquitecto + especialistas ensamblan
3. (revisión automática)                  → quality + a11y/motion validan
4. /animate "ajuste de motion"            → refino interacciones puntuales
5. /vault-sync                            → confirmo que el vault sigue coherente
```

## 6. Mantenimiento del vault

```
# tras traer nuevos sites/<slug>/raw/*.json (vía skill firecrawl-web):
/vault-enrich --site <slug>
/vault-sync
```
Nunca edites a mano los archivos generados (llevan el aviso "No editar a mano"): cambia `scripts/build_vault.py` y vuelve a correr `/vault-enrich`.

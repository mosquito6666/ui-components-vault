---
name: webgl-3d-catalog
description: >
  Guía de 3D/WebGL para la web sobre el vault: Threlte (Svelte+Three.js+Rapier+GLTF), Spline
  (editor 3D + embeds) y R3F (React Three Fiber) como puente. Úsala cuando el trabajo incluya
  escenas 3D, modelos, física, cámaras, materiales/luces o decidir entre 3D real vs embed vs video.
  Incluye setup, composición de escena, física y presupuesto de performance.
---

# WebGL / 3D Catalog

## Fuentes y cuándo usar cada una

| Fuente | Stack | Cuándo |
|---|---|---|
| **Threlte** | Svelte + Three.js | escena 3D real con interacción/estado en Svelte |
| **R3F** | React + Three.js | equivalente para stacks React/Next |
| **Spline** | embed/iframe | 3D decorativo o creado por artista, sin lógica custom |

Threlte: `npm i @threlte/core @threlte/extras three` (+ `@threlte/rapier` para física). El raw de Threlte (`sites/threlte/raw/`) trae snippets reales (`<T.Mesh>…`).

## Decisión: 3D real vs embed vs video

1. ¿Hay interacción/estado/datos? → **escena real** (Threlte/R3F).
2. ¿Es decorativo y viene de diseño? → **Spline embed** (o video con poster si solo es ambiente).
3. ¿Es crítico para LCP? → nunca bloquees con WebGL: poster + lazy.

## Composición de escena (checklist)

- **Cámara**: perspectiva vs ortográfica; FOV; posición; controles (orbit/limitados).
- **Luces**: mínimas dinámicas; combina ambient + directional; baked cuando sea posible.
- **Materiales**: PBR con texturas comprimidas; reutiliza materiales.
- **Modelos GLTF**: Draco/meshopt; instancing para repetición; LOD si aplica.
- **Animación/física**: clips GLTF, o Rapier (colliders mínimos, timestep fijo, dormir cuerpos).
- **Integración Theatre.js** para cinemática de cámara/objetos sincronizada.

## Presupuesto de performance (aplicar y declarar)

- `frameloop="demand"` si no hay animación continua; render on-demand.
- Pausar el canvas fuera de viewport (IntersectionObserver).
- Limitar `devicePixelRatio` ≤ 2; bajar calidad en móvil.
- Lazy-load del bundle 3D; `Suspense`/fallback; poster mientras carga.
- Vigilar memoria de texturas; `dispose()` al desmontar.

## Accesibilidad

- El 3D no es la única vía de información; provee texto/alt.
- `prefers-reduced-motion`: desactiva auto-rotación/cámara animada.
- Controles operables por teclado cuando hay interacción.

Implementa con el agente `webgl-3d-specialist`; revisa con `frontend-quality-reviewer` (perf/SSR) y `accessibility-motion-reviewer`.

---
name: component-registries
description: >
  Cómo instalar e integrar componentes de las librerías-registro del vault: cult-ui (shadcn
  registry), watermelon-ui (registry React), 21st-community (registro masivo) y styleui (templates).
  Úsala cuando tengas que TRAER un componente a un proyecto y necesites el patrón correcto de
  instalación (copy-paste vs npx shadcn add vs npm vs template) y su integración con Tailwind.
---

# Component Registries — instalación e integración

Patrones de adopción por librería. Verifica siempre el `framework` contra tu stack.

## Patrones de instalación

| Librería | Framework | Patrón | Comando / método |
|---|---|---|---|
| **cult-ui** | React+Tailwind | shadcn registry | `npx shadcn@latest add <url-o-slug>` |
| **watermelon-ui** | React | registry / copy-paste | `npx shadcn@latest add <slug>` o copiar del docs |
| **21st-community** | React | copy-paste comunitario | copiar snippet del componente (cada uno con su autor) |
| **styleui** | React/Svelte | templates | clonar/adaptar template completo |
| **skiper-ui** | React+Tailwind | copy-paste | copiar componente + deps |
| **aliimam** | React+Tailwind | copy-paste / registry | copiar componente/shader |

## Flujo shadcn (cult-ui, watermelon)

1. Proyecto con Tailwind + shadcn inicializado (`npx shadcn@latest init`).
2. `npx shadcn@latest add <componente>` (o la URL del registry).
3. Ajusta tokens a tu design system (ver skill `design-tokens`).
4. Verifica dependencias peer (Radix, framer-motion, etc.) y que el componente respeta tu theming.

## Flujo copy-paste (skiper, aliimam, 21st)

1. Localiza el componente con `vault-navigator` y abre su `source_url`.
2. Copia el snippet **tal cual del origen** (convención del vault) a tu árbol de componentes.
3. Instala dependencias que el snippet importe (anímalas: framer-motion, gsap, three, etc.).
4. Sustituye colores/tipografía crudos por tus tokens semánticos.
5. Anota cualquier adaptación respecto al origen.

## Templates (styleui)

- No son componentes atómicos sino páginas/landing completas; úsalos como punto de partida y desmóntalos en bloques que mapeen a tu sistema.

## Checklist de integración

- [ ] Framework del componente == stack del proyecto (si no, busca equivalente o adapta).
- [ ] Dependencias instaladas y versionadas.
- [ ] Colores/tipografía → tokens del proyecto (no valores mágicos).
- [ ] `source_url` conservado en un comentario para trazabilidad.
- [ ] Revisión con `frontend-quality-reviewer` (integridad de snippet) antes de dar por hecho.

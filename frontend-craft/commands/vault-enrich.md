---
name: vault-enrich
description: Regenera el contenido del vault (categorías, índices, consolidated.json) desde sites/*/raw OFFLINE.
---

Argumentos opcionales: **$ARGUMENTS** (ej. `--site threlte`, `--category 3`, vacío = `--all`).

Regenera el contenido derivado del vault a partir de los scrapes existentes. Es offline, determinista e idempotente.

1. Sitúate en la raíz del repo del vault (donde está `scripts/build_vault.py`). Si el plugin está instalado fuera del vault, usa la ruta `${CLAUDE_PLUGIN_ROOT}/../scripts/build_vault.py` o pide al usuario la ruta del vault.
2. Ejecuta:
   ```bash
   python scripts/build_vault.py $ARGUMENTS
   ```
   (sin argumentos equivale a `--all`).
3. Reporta el resumen: nº de archivos generados y nº de componentes consolidados. Regenera:
   - `data/consolidated.json` (esquema v2 + by_category/by_site)
   - `categories/NN_*.md` (00..08) + `00_overview.md` (matriz)
   - `sites/<slug>/_index.md`
   - `_index.md` y `_meta.json`
4. Verifica con `/vault-sync` que quede en 0 discrepancias.

No edites a mano los archivos generados (llevan el aviso "No editar a mano"): cambia la lógica en `scripts/build_vault.py` y vuelve a correr. Para añadir/re-scrapear sitios nuevos, primero actualiza `sites/<slug>/raw/*.json` (Firecrawl) y luego corre este comando.

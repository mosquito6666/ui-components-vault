---
name: vault-sync
description: Verifica consistencia del vault (dry-run) entre raw, consolidated.json, categorías e índices.
---

Reconcilia el estado del vault sin escribir nada.

1. Sitúate en la raíz del repo del vault (donde está `scripts/build_vault.py`).
2. Ejecuta el dry-run:
   ```bash
   python scripts/build_vault.py --check
   ```
3. Interpreta la salida:
   - `Vault sincronizado: 0 discrepancias.` → todo coherente (exit 0).
   - Líneas `DIFF`/`FALTA`/`LEGACY` → hay deriva (exit 1). Cada línea indica el archivo afectado.
4. Si hay discrepancias, propón correr `/vault-enrich` para regenerar y vuelve a verificar.

El `--check` ignora líneas de timestamp (`generated_at`/`scraped_at`/`Last updated`) para no marcar falsas diferencias. Úsalo tras editar el script, tras un re-scrape, o antes de commitear cambios en el vault.

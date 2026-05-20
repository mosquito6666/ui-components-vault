#!/usr/bin/env python3
"""build_vault.py — Motor de consolidación/enriquecimiento OFFLINE del UI Components Vault.

Lee los scrapes existentes en ``sites/<slug>/raw/*.json`` (campo ``markdown``) y los
``sites/<slug>/_meta.json``, extrae los componentes (links markdown), los clasifica por
categoría canónica, infiere framework + comando de instalación, y regenera de forma
DETERMINISTA e IDEMPOTENTE:

  - data/consolidated.json   (esquema extendido + by_category + by_site)
  - categories/NN_*.md       (esquema canónico 00..08, con tablas pobladas)
  - sites/<slug>/_index.md    (resumen real: framework, install, catálogo, links)
  - categories/00_overview.md (matriz cruzada sitio × categoría con counts reales)
  - _index.md / _meta.json    (reconciliados con el esquema canónico)

NO requiere red. NO inventa contenido: si una página interna no fue scrapeada, el snippet
queda en null / "—" y solo se conserva el ``source_url`` (trazabilidad obligatoria).

Uso:
    python scripts/build_vault.py --all          # regenera todo (default)
    python scripts/build_vault.py --site threlte # solo un sitio (+ índices globales)
    python scripts/build_vault.py --category 3   # solo una categoría (+ índices)
    python scripts/build_vault.py --check         # dry-run: reporta discrepancias, exit!=0 si las hay
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES_DIR = ROOT / "sites"
CATEGORIES_DIR = ROOT / "categories"
DATA_DIR = ROOT / "data"

# --------------------------------------------------------------------------------------
# Esquema canónico de categorías (alineado con _index.md). índice -> (clave, título es)
# --------------------------------------------------------------------------------------
CATEGORIES: list[tuple[int, str, str]] = [
    (0, "overview", "Matriz Cruzada"),
    (1, "buttons", "Botones"),
    (2, "backgrounds", "Backgrounds"),
    (3, "animations", "Animaciones"),
    (4, "colors", "Colores"),
    (5, "typography", "Tipografía"),
    (6, "interactions", "Interacciones"),
    (7, "3d_canvas", "3D / Canvas"),
    (8, "layout_cards", "Layout & Cards"),
]
CAT_KEY_BY_INDEX = {i: k for i, k, _ in CATEGORIES}
CAT_INDEX_BY_KEY = {k: i for i, k, _ in CATEGORIES}
CAT_TITLE_BY_KEY = {k: t for _, k, t in CATEGORIES}
CONTENT_CATEGORY_KEYS = [k for i, k, _ in CATEGORIES if k != "overview"] + ["other"]

# --------------------------------------------------------------------------------------
# Metadatos por sitio: framework, patrón/comando de instalación, descripción corta.
# Fuente: tabla "Frameworks por sitio" del CLAUDE.md. install_cmd_tpl admite {slug}.
# --------------------------------------------------------------------------------------
SITE_INFO: dict[str, dict] = {
    "cult-ui": {
        "framework": "React + Tailwind",
        "install_pattern": "copy-paste registry (shadcn)",
        "install_cmd_tpl": "npx shadcn@latest add {slug}",
        "desc": "Componentes animados niche que extienden el ecosistema shadcn/ui.",
    },
    "skiper-ui": {
        "framework": "React + Tailwind",
        "install_pattern": "copy-paste",
        "install_cmd_tpl": None,
        "desc": "Colección profesional de animaciones y micro-interacciones (scroll, hover, preloaders).",
    },
    "watermelon-ui": {
        "framework": "React",
        "install_pattern": "registry (copy-paste)",
        "install_cmd_tpl": "npx shadcn@latest add {slug}",
        "desc": "Librería React: componentes base + amplia colección de componentes animados.",
    },
    "aliimam": {
        "framework": "React + Tailwind",
        "install_pattern": "copy-paste / registry",
        "install_cmd_tpl": None,
        "desc": "Shaders y efectos visuales creativos (swirl, liquid, ripple, patterns).",
    },
    "theatrejs": {
        "framework": "Vanilla / React (agnóstico)",
        "install_pattern": "npm library",
        "install_cmd_tpl": "npm i @theatre/core @theatre/studio",
        "desc": "Motor de motion design y sincronización temporal de animaciones.",
    },
    "threlte": {
        "framework": "Svelte + Three.js",
        "install_pattern": "npm packages",
        "install_cmd_tpl": "npm i @threlte/core @threlte/extras three",
        "desc": "Framework declarativo 3D/WebGL para Svelte (física Rapier, GLTF, Theatre.js).",
    },
    "peachweb": {
        "framework": "Web components (HTML5)",
        "install_pattern": "npm package",
        "install_cmd_tpl": "npm i peachweb",
        "desc": "Web components HTML5.",
    },
    "styleui": {
        "framework": "React / Svelte",
        "install_pattern": "templates / registry",
        "install_cmd_tpl": None,
        "desc": "Templates SaaS y landing pages pre-construidas.",
    },
    "21st-community": {
        "framework": "React",
        "install_pattern": "community registry (copy-paste)",
        "install_cmd_tpl": None,
        "desc": "Registro comunitario masivo de componentes (200+) filtrable por categoría.",
    },
    "spline": {
        "framework": "Web / 3D (SaaS)",
        "install_pattern": "embed iframe",
        "install_cmd_tpl": None,
        "desc": "Editor 3D visual con generación por lenguaje natural; se integra vía embeds.",
    },
}

# --------------------------------------------------------------------------------------
# Clasificación por palabras clave. Orden = prioridad (primer match gana).
# --------------------------------------------------------------------------------------
CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("3d_canvas", ["3d", "webgl", "three", "threlte", "spline", "scene", "canvas", "gltf", "mesh", "render canvas"]),
    ("animations", ["animat", "motion", "scroll", "reveal", "marquee", "hover", "spring",
                     "transition", "parallax", "fade", "preloader", "loader", "shader",
                     "ripple", "wave", "swirl", "gooey", "typewriter", "counter", "number",
                     "rolling", "stagger", "timeline", "kinetic"]),
    ("buttons", ["button", "btn", "cta", "call to action"]),
    ("backgrounds", ["background", "gradient", "pattern", "dot pattern", "grid pattern",
                     "aurora", "noise", "mesh gradient", "beams", "glow", "spotlight"]),
    ("interactions", ["modal", "dialog", "dropdown", "popover", "tooltip", "menu", "accordion",
                      "tabs", "toggle", "select", "combobox", "command", "sheet", "drawer",
                      "carousel", "slider", "navbar", "navigation", "input", "form", "checkbox",
                      "switch", "calendar", "date picker", "pagination", "breadcrumb"]),
    ("typography", ["typograph", "text", "font", "words", "heading", "title", "type "]),
    ("colors", ["color", "palette", "theme", "swatch", "token"]),
    ("layout_cards", ["card", "grid", "layout", "bento", "masonry", "flex", "section", "hero",
                      "footer", "header", "sidebar", "pricing", "feature", "testimonial",
                      "dock", "comparison", "client"]),
]

# Pistas por segmento de ruta en el source_url (refuerzan la clasificación).
PATH_HINTS: list[tuple[str, str]] = [
    ("/shaders/", "animations"),
    ("/3d", "3d_canvas"),
    ("/backgrounds", "backgrounds"),
    ("/buttons", "buttons"),
    ("/typography", "typography"),
]

# Texto de links que NO son componentes (navegación / legal / social / assets).
NOISE_NAMES = {
    "home", "components", "component", "registry", "installation", "framework support",
    "changelog", "introduction", "documentation", "docs", "read more", "dismiss",
    "privacy policy", "terms of service", "github", "twitter", "x", "discord", "blog",
    "pricing", "login", "sign in", "sign up", "get started", "start building", "contact",
    "about", "faq", "support", "community", "templates", "showcase", "examples", "guides",
    "api reference", "manual", "concepts", "magic chat", "private registry",
    "publish your agents", "agent templates", "mcp", "featured", "newest", "all",
    "copyright", "privacy", "terms", "sitemap", "cookies", "license", "careers",
    "best of the week", "top authors", "themes",
}
ASSET_RE = re.compile(r"\.(webp|png|svg|jpg|jpeg|gif|mp4|webm|ico|css|js)(\?|$)", re.I)
LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")
CODEBLOCK_RE = re.compile(r"```[a-zA-Z0-9]*\n(.*?)```", re.S)
SLUG_RE = re.compile(r"[^a-z0-9]+")
TRAILING_COUNT_RE = re.compile(r"\s*\d+$")        # "Buttons130" -> "Buttons"
INITIALS_RE = re.compile(r"^[A-Z]{1,3}\d*$")       # "SC", "AU", "B" (avatares de autor)


def slugify(text: str) -> str:
    return SLUG_RE.sub("-", text.lower()).strip("-")


def clean_name(raw_name: str) -> str:
    name = raw_name.replace("\n", " ").strip().lstrip("!").strip()
    name = TRAILING_COUNT_RE.sub("", name).strip()  # quita conteos de 21st
    return name


def classify(name: str, url: str) -> tuple[str, list[str]]:
    """Devuelve (categoría_canónica, tags)."""
    hay = f"{name} {url}".lower()
    tags: list[str] = []
    chosen = None
    # Pistas de ruta primero
    for frag, cat in PATH_HINTS:
        if frag in url.lower():
            chosen = cat
            break
    for cat, kws in CATEGORY_RULES:
        for kw in kws:
            if kw in hay:
                tags.append(kw.strip())
                if chosen is None:
                    chosen = cat
    if chosen is None:
        chosen = "other"
    # tags únicos preservando orden
    seen: set[str] = set()
    tags = [t for t in tags if not (t in seen or seen.add(t))]
    return chosen, tags[:6]


def is_component_link(name: str, url: str, site_url: str) -> bool:
    if not name or name == "[":
        return False
    if name.lower() in NOISE_NAMES:
        return False
    if INITIALS_RE.match(name):       # iniciales de autor (SC, AU, B…)
        return False
    if len(name) < 3:
        return False
    if ASSET_RE.search(url):
        return False
    if len(name) > 60:                # frases largas de marketing
        return False
    return True


def extract_components(site: str, raw_md: str, site_url: str) -> list[dict]:
    """Extrae componentes (links) deduplicados de un markdown scrapeado."""
    info = SITE_INFO.get(site, {})
    framework = info.get("framework", "—")
    install_tpl = info.get("install_cmd_tpl")
    install_pattern = info.get("install_pattern", "")
    snippets = [s.strip() for s in CODEBLOCK_RE.findall(raw_md) if s.strip()]
    site_snippet = snippets[0] if snippets else None

    out: dict[str, dict] = {}
    for raw_name, url in LINK_RE.findall(raw_md):
        name = clean_name(raw_name)
        if not is_component_link(name, url, site_url):
            continue
        slug = slugify(url.rstrip("/").split("/")[-1]) or slugify(name)
        if not slug or slug in out:
            continue
        category, tags = classify(name, url)
        install_cmd = install_tpl.format(slug=slug) if install_tpl else None
        out[slug] = {
            "name": name,
            "slug": slug,
            "site": site,
            "framework": framework,
            "install_cmd": install_cmd,
            "install_pattern": install_pattern,
            "snippet": site_snippet if (site == "threlte" and category == "3d_canvas") else None,
            "source_url": url,
            "preview_url": url,
            "primary_category": category,
            "tags": tags,
            "evidence_text": name,
            "confidence": 0.6,
        }
    return sorted(out.values(), key=lambda c: (c["primary_category"], c["name"].lower()))


def load_site(site_dir: Path) -> tuple[dict, list[dict]]:
    """Devuelve (meta, components) para un directorio de sitio."""
    site = site_dir.name
    meta_path = site_dir / "_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"site": site}
    components: list[dict] = []
    raw_dir = site_dir / "raw"
    if raw_dir.exists():
        for raw_file in sorted(raw_dir.glob("*.json")):
            try:
                d = json.loads(raw_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            md = d.get("markdown") or ""
            if len(md.strip()) < 200:  # raw vacío / error de scraping
                meta["scrape_status"] = "partial" if md.strip() else "error"
                continue
            components.extend(extract_components(site, md, d.get("url", "")))
    return meta, components


# --------------------------------------------------------------------------------------
# Renderizado de archivos
# --------------------------------------------------------------------------------------
NOTE = "> Generado por `scripts/build_vault.py` desde `sites/*/raw/`. No editar a mano — usa `/vault-enrich`."


def fm(d: dict) -> str:
    """Frontmatter YAML simple y determinista."""
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def md_cell(v) -> str:
    if v is None or v == "":
        return "—"
    return str(v).replace("|", "\\|").replace("\n", " ")


def render_category(idx: int, key: str, title: str, comps: list[dict], scraped_at: str) -> str:
    rows = [c for c in comps if c["primary_category"] == key]
    rows.sort(key=lambda c: (c["site"], c["name"].lower()))
    source_urls = sorted({c["source_url"] for c in rows})
    frameworks = sorted({c["framework"] for c in rows})
    front = fm({
        "section": key,
        "canonical_index": idx,
        "source_urls": source_urls,
        "scraped_at": scraped_at,
        "items_count": len(rows),
        "frameworks": frameworks,
    })
    parts = [front, "", f"# {title}", "", NOTE, ""]
    if not rows:
        parts += ["_Sin componentes detectados en los scrapes actuales. "
                  "Re-scrapear las páginas internas para poblar esta categoría._", ""]
        return "\n".join(parts)

    parts += ["## Componentes", "",
              "| Sitio | Componente | Framework | Install | Snippet | Preview | Tags |",
              "|---|---|---|---|---|---|---|"]
    for c in rows:
        install = md_cell(c["install_cmd"]) if c["install_cmd"] else md_cell(c["install_pattern"])
        snippet = "ver source" if c["snippet"] else "—"
        preview = f"[demo]({c['preview_url']})" if c["preview_url"] else "—"
        tags = ", ".join(c["tags"]) if c["tags"] else "—"
        parts.append(f"| {c['site']} | {md_cell(c['name'])} | {md_cell(c['framework'])} | "
                     f"`{install}` | {snippet} | {preview} | {md_cell(tags)} |")
    parts.append("")

    # Alternativas equivalentes: agrupar por sitios que cubren esta categoría
    by_site: dict[str, int] = {}
    for c in rows:
        by_site[c["site"]] = by_site.get(c["site"], 0) + 1
    parts += ["## Alternativas equivalentes", "",
              "Sitios que cubren esta categoría (nº de componentes):", ""]
    for site, n in sorted(by_site.items(), key=lambda x: (-x[1], x[0])):
        parts.append(f"- **{site}** — {n}")
    parts.append("")
    return "\n".join(parts)


def render_overview(comps: list[dict], scraped_at: str) -> str:
    sites = sorted({c["site"] for c in comps})
    cats = [k for k in CONTENT_CATEGORY_KEYS]
    # matriz counts
    counts: dict[tuple[str, str], int] = {}
    for c in comps:
        counts[(c["site"], c["primary_category"])] = counts.get((c["site"], c["primary_category"]), 0) + 1
    front = fm({
        "section": "overview",
        "canonical_index": 0,
        "scraped_at": scraped_at,
        "items_count": len(comps),
    })
    header = "| Sitio | " + " | ".join(cats) + " | **Total** |"
    sep = "|" + "---|" * (len(cats) + 2)
    parts = [front, "", "# Categorías — Matriz Cruzada", "", NOTE, "",
             "Número de componentes por sitio × categoría.", "", header, sep]
    for site in sites:
        total = sum(counts.get((site, k), 0) for k in cats)
        cells = [str(counts.get((site, k), 0) or "—") for k in cats]
        parts.append(f"| {site} | " + " | ".join(cells) + f" | **{total}** |")
    totals = [str(sum(counts.get((s, k), 0) for s in sites) or "—") for k in cats]
    parts.append(f"| **Total** | " + " | ".join(f"**{t}**" for t in totals) + f" | **{len(comps)}** |")
    parts += ["", "## Qué entra en cada categoría", "",
              "- **buttons** — botones, estados, variantes (solid/outline/ghost/loading).",
              "- **backgrounds** — gradientes, patterns, glows, beams, shaders de fondo.",
              "- **animations** — spring, scroll-reveal, hover, marquee, preloaders, motion.",
              "- **colors** — paletas, temas, tokens CSS (oklch/hsl/hex).",
              "- **typography** — escalas, familias, texto animado.",
              "- **interactions** — modales, dropdowns, popovers, tooltips, forms, carousels.",
              "- **3d_canvas** — 3D, WebGL, canvas (Threlte, Spline, Three.js).",
              "- **layout_cards** — grids, cards, heroes, secciones de marketing.", ""]
    return "\n".join(parts)


def render_site_index(site: str, meta: dict, comps: list[dict]) -> str:
    info = SITE_INFO.get(site, {})
    site_comps = [c for c in comps if c["site"] == site]
    by_cat: dict[str, list[dict]] = {}
    for c in site_comps:
        by_cat.setdefault(c["primary_category"], []).append(c)
    status = meta.get("scrape_status")
    front = fm({
        "site": site,
        "url": meta.get("url", ""),
        "phase": meta.get("phase", ""),
        "framework": info.get("framework", "—"),
        "scraped_at": meta.get("scraped_at", ""),
        "items_count": len(site_comps),
    })
    parts = [front, "", f"# {site}", "", NOTE, "",
             f"**URL**: {meta.get('url','')}",
             f"**Framework**: {info.get('framework','—')}",
             f"**Instalación**: {info.get('install_pattern','—')}",
             f"**Descripción**: {info.get('desc','—')}", ""]
    if status:
        parts += [f"> ⚠️ Estado de scraping: **{status}** — sin contenido suficiente en `raw/`. "
                  "No se inventan componentes.", ""]
    if not site_comps:
        return "\n".join(parts)
    parts += ["## Catálogo por categoría", ""]
    for key in CONTENT_CATEGORY_KEYS:
        rows = by_cat.get(key)
        if not rows:
            continue
        parts.append(f"### {CAT_TITLE_BY_KEY.get(key, key)} ({len(rows)})")
        for c in sorted(rows, key=lambda x: x["name"].lower()):
            parts.append(f"- [{c['name']}]({c['source_url']})")
        parts.append("")
    return "\n".join(parts)


def render_root_index(comps: list[dict], by_site: dict, scraped_at: str) -> str:
    front = fm({"section": "index", "generated_at": scraped_at})
    total = len(comps)
    nav = []
    for i, k, t in CATEGORIES:
        if k == "overview":
            nav.append(f"- **[00_overview](categories/00_overview.md)** — Matriz cruzada sitio × categoría")
        else:
            nav.append(f"- **[{i:02d}_{k}](categories/{i:02d}_{k}.md)** — {t}")
    parts = [front, "", "# UI Components Vault — Índice Maestro", "",
             f"Repositorio curado de **{len(SITE_INFO)} librerías UI**, "
             f"**{total} componentes** categorizados y enriquecidos.", "",
             "## Navegación rápida", "", *nav, "",
             "## Cómo trabajar con agentes y skills (plugin `frontend-craft`)", "",
             "1. **Descubrir** — `/find-component \"<necesidad>\"` busca candidatos en el vault con su `source_url`.",
             "2. **Construir** — `/build-ui \"<descripción>\"` orquesta `frontend-architect` → especialistas.",
             "3. **Animar** — `/animate \"<elemento>\"` aplica el catálogo de animaciones con `prefers-reduced-motion`.",
             "4. **Revisar** — los reviewers (`frontend-quality-reviewer`, `accessibility-motion-reviewer`) validan.",
             "5. **Mantener** — `/vault-enrich` regenera el contenido; `/vault-sync` reconcilia.", "",
             "## Estadísticas globales", "",
             "| Métrica | Valor |", "|---|---|",
             f"| **Sitios totales** | {len(SITE_INFO)} |",
             f"| **Componentes** | {total} |"]
    for site in sorted(by_site):
        parts.append(f"| {site} | {by_site[site]} |")
    parts += ["", f"*Generado con `scripts/build_vault.py`. Last updated: {scraped_at}*", ""]
    return "\n".join(parts)


# --------------------------------------------------------------------------------------
# Orquestación
# --------------------------------------------------------------------------------------
def build_all() -> dict[str, str]:
    """Construye el contenido en memoria. Devuelve {ruta_relativa: contenido}."""
    now = datetime.now(timezone.utc).isoformat()
    metas: dict[str, dict] = {}
    comps: list[dict] = []
    for site_dir in sorted(p for p in SITES_DIR.iterdir() if p.is_dir()):
        meta, site_comps = load_site(site_dir)
        metas[site_dir.name] = meta
        comps.extend(site_comps)

    by_category: dict[str, list[dict]] = {}
    by_site: dict[str, int] = {}
    for c in comps:
        by_category.setdefault(c["primary_category"], []).append(c)
        by_site[c["site"]] = by_site.get(c["site"], 0) + 1

    files: dict[str, str] = {}

    # consolidated.json
    consolidated = {
        "metadata": {
            "total_sites": len(SITE_INFO),
            "total_components": len(comps),
            "generated_at": now,
            "schema_version": 2,
            "categories": CONTENT_CATEGORY_KEYS,
        },
        "components": comps,
        "by_category": {k: sorted([c["slug"] for c in v]) for k, v in sorted(by_category.items())},
        "by_site": {s: by_site[s] for s in sorted(by_site)},
    }
    files["data/consolidated.json"] = json.dumps(consolidated, ensure_ascii=False, indent=2) + "\n"

    # categorías
    for i, k, t in CATEGORIES:
        fname = f"categories/{i:02d}_{k}.md"
        if k == "overview":
            files[fname] = render_overview(comps, now)
        else:
            files[fname] = render_category(i, k, t, comps, now)

    # sites/<slug>/_index.md
    for site, meta in metas.items():
        files[f"sites/{site}/_index.md"] = render_site_index(site, meta, comps)

    # índices raíz
    files["_index.md"] = render_root_index(comps, by_site, now)
    meta_master = {
        "status": "enriched",
        "schema_version": 2,
        "total_sites": len(SITE_INFO),
        "total_components": len(comps),
        "generated_at": now,
        "categories": CONTENT_CATEGORY_KEYS,
        "by_site": {s: by_site[s] for s in sorted(by_site)},
    }
    files["_meta.json"] = json.dumps(meta_master, ensure_ascii=False, indent=2) + "\n"
    return files


TS_LINE_RE = re.compile(r'(generated_at|scraped_at|Last updated)["\']?\s*[:=].*', re.I)


def normalize(text: str) -> str:
    """Quita líneas con timestamps para comparar idempotencia en --check."""
    return "\n".join(l for l in text.splitlines() if not TS_LINE_RE.search(l))


def cleanup_legacy() -> list[Path]:
    """Elimina archivos de categorías con numeración antigua/duplicada."""
    legacy = {
        "00_buttons.md", "01_backgrounds.md", "02_animations.md", "03_colors.md",
        "04_typography.md", "05_interactions.md", "06_3d_canvas.md", "07_layout_cards.md",
    }
    removed = []
    for name in legacy:
        p = CATEGORIES_DIR / name
        if p.exists():
            removed.append(p)
    return removed


def main() -> int:
    ap = argparse.ArgumentParser(description="Enriquecedor offline del UI Components Vault")
    ap.add_argument("--all", action="store_true", help="Regenerar todo (default)")
    ap.add_argument("--site", help="Limitar la salida a un sitio (los índices globales se regeneran igual)")
    ap.add_argument("--category", type=int, help="Limitar la salida a una categoría por índice (0..8)")
    ap.add_argument("--check", action="store_true", help="Dry-run: reportar discrepancias sin escribir")
    args = ap.parse_args()

    files = build_all()
    legacy = cleanup_legacy()

    # Filtro opcional de salida (los índices y consolidated siempre se incluyen)
    def keep(path: str) -> bool:
        if args.site and path.startswith("sites/") and f"/{args.site}/" not in path:
            return False
        if args.category is not None and path.startswith("categories/") and "overview" not in path:
            want = f"categories/{args.category:02d}_"
            if not path.startswith(want):
                return False
        return True

    targets = {p: c for p, c in files.items() if keep(p)}

    if args.check:
        discrepancies = 0
        for rel, content in targets.items():
            fp = ROOT / rel
            if not fp.exists():
                print(f"  FALTA  {rel}")
                discrepancies += 1
            elif normalize(fp.read_text(encoding="utf-8")) != normalize(content):
                print(f"  DIFF   {rel}")
                discrepancies += 1
        for p in legacy:
            print(f"  LEGACY {p.relative_to(ROOT)} (debería eliminarse)")
            discrepancies += 1
        if discrepancies:
            print(f"\n{discrepancies} discrepancia(s). Ejecuta sin --check para regenerar.")
            return 1
        print("Vault sincronizado: 0 discrepancias.")
        return 0

    # Escritura
    for p in legacy:
        p.unlink()
        print(f"  eliminado  {p.relative_to(ROOT)}")
    written = 0
    for rel, content in targets.items():
        fp = ROOT / rel
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        written += 1
    total_comps = json.loads(files["data/consolidated.json"])["metadata"]["total_components"]
    print(f"OK: {written} archivos generados · {total_comps} componentes consolidados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

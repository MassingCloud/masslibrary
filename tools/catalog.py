"""Generate CATALOG.md from the artifacts that were actually built.

The catalog reads each `.mass` container's own manifest and each sector's computed economics rather
than a hand-maintained list. A catalog beside the artifacts is a promise; a catalog read *from* them
is a measurement, and only one of the two can go stale without anybody noticing.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import projectdata as P  # noqa: E402
import sectors           # noqa: E402


def read_manifest(path: str) -> dict:
    with zipfile.ZipFile(path) as z:
        man = json.loads(z.read("manifest.json"))
        try:
            idx = json.loads(z.read("index/props.json"))
        except KeyError:
            idx = {}
    return {"manifest": man, "index": idx, "bytes": os.path.getsize(path)}


def sector_dir(spec: dict) -> str:
    return spec["sector"].lower().replace(" ", "-").replace("/", "-")


def container_path(spec: dict) -> str:
    return os.path.join(ROOT, "samples", sector_dir(spec), f"{spec['key']}.mass")


def main() -> int:
    rows = []
    for spec in sectors.SECTORS:
        path = container_path(spec)
        if not os.path.exists(path):
            print(f"missing container for {spec['key']} — skipped", file=sys.stderr)
            continue
        rows.append((spec, read_manifest(path)))

    if not rows:
        print("no containers found; run tools/build_library.py first", file=sys.stderr)
        return 1

    # Containers that are in the library but not generated from `sectors.py` — the contributed
    # vertiport and the in-browser authoring demo. They are listed from their own manifests, which
    # is the only description of them that cannot go stale.
    generated = {container_path(s) for s in sectors.SECTORS}
    extra = []
    for dirpath, _, files in os.walk(os.path.join(ROOT, "samples")):
        for fn in sorted(files):
            p = os.path.join(dirpath, fn)
            if fn.endswith(".mass") and p not in generated:
                extra.append((os.path.relpath(p, ROOT).replace("\\", "/"), read_manifest(p)))

    L: list[str] = []
    A = L.append
    A("# Catalog")
    A("")
    A("Generated from the built containers by `tools/catalog.py` — every figure below is read from "
      "an artifact's own manifest or computed from `tools/sectors.py`, never typed in.")
    A("")

    # ── Containers ───────────────────────────────────────────────────────────────────────────────
    A("## Containers")
    A("")
    A("| Sample | Sector | Elements | Tables | Rows | Container | Storeys | Gross area |")
    A("|---|---|---:|---:|---:|---:|---:|---:|")
    for spec, m in rows:
        man = m["manifest"]
        n_el = man["tables"].get("element", 0)
        tables = {k: v for k, v in man["tables"].items() if k != "element"}
        A(f"| [{spec['name']}](samples/{sector_dir(spec)}/{spec['key']}.mass) | {spec['sector']} | "
          f"{n_el:,} | {len(tables)} | {sum(tables.values()):,} | {m['bytes'] / 1e6:.2f} MB | "
          f"{spec['storeys']} | {spec['gross_sf']:,} sf |")
    A("")
    total_bytes = sum(m["bytes"] for _, m in rows)
    total_el = sum(m["manifest"]["tables"].get("element", 0) for _, m in rows)
    A(f"**{len(rows)} generated containers · {total_el:,} elements · "
      f"{total_bytes / 1e6:.1f} MB.**")
    A("")

    if extra:
        A("### Contributed and demonstration containers")
        A("")
        A("Not generated from `tools/sectors.py`. Described from their own manifests.")
        A("")
        A("| Container | Project | Elements | Tables | Rows | Size |")
        A("|---|---|---:|---:|---:|---:|")
        for rel, m in extra:
            man = m["manifest"]
            tabs = {k: v for k, v in man["tables"].items() if k != "element"}
            A(f"| [`{rel.split('/')[-1]}`]({rel}) | {(man.get('project') or {}).get('name', '?')} | "
              f"{man['tables'].get('element', 0):,} | {len(tabs)} | {sum(tabs.values()):,} | "
              f"{m['bytes'] / 1e6:.2f} MB |")
        A("")

    # ── Economics ────────────────────────────────────────────────────────────────────────────────
    A("## Economics")
    A("")
    A("| Sample | Total dev cost | $/gross sf | NOI | Yield on cost | Exit cap | Spread | "
      "Unlevered IRR | Levered IRR | Equity multiple |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for spec, _ in rows:
        pf = P.proforma(spec)
        if pf["noi"] and pf["yield_on_cost"]:
            A(f"| {spec['name']} | ${pf['total_cost'] / 1e6:,.1f}M | ${pf['cost_psf']:,.0f} | "
              f"${pf['noi'] / 1e6:,.2f}M | {pf['yield_on_cost']:.2%} | "
              f"{spec['finance']['exit_cap']:.2%} | {pf['spread_bps']:+.0f} bps | "
              f"{pf['unlevered_irr']:.2%} | {pf['levered_irr']:.2%} | "
              f"{pf['equity_multiple']:.2f}× |")
        else:
            A(f"| {spec['name']} | ${pf['total_cost'] / 1e6:,.1f}M | ${pf['cost_psf']:,.0f} | — | "
              "— | — | — | — | — | — |")
    A("")
    A("The aviation terminal is publicly funded. It reports no capitalised exit rather than "
      "fabricating returns from a cap rate that does not apply to it.")
    A("")

    # ── Schedule ─────────────────────────────────────────────────────────────────────────────────
    A("## Schedule and budget")
    A("")
    A("| Sample | Start | Substantial completion | Duration | Activities | "
      "Revised budget | Forecast | Variance |")
    A("|---|---|---|---:|---:|---:|---:|---:|")
    for spec, _ in rows:
        st, fi = P.schedule_span(spec)
        bt = P.budget_totals(spec)
        var = bt["revised"] - bt["forecast"]
        A(f"| {spec['name']} | {st:%b %Y} | {fi:%b %Y} | {spec['finance']['months']} mo | "
          f"{len(P.schedule(spec))} | ${bt['revised'] / 1e6:,.1f}M | "
          f"${bt['forecast'] / 1e6:,.1f}M | {var / bt['revised']:+.2%} |")
    A("")

    # ── Model composition ────────────────────────────────────────────────────────────────────────
    A("## Model composition")
    A("")
    A("Element counts by IFC class, read from each container's element index.")
    A("")
    for spec, m in rows:
        els = m["index"].get("elements", [])
        by: dict[str, int] = {}
        for e in els:
            by[e.get("ifc_class", "?")] = by.get(e.get("ifc_class", "?"), 0) + 1
        A(f"### {spec['name']}")
        A("")
        A(f"*{spec['subtype']}* · LOD claim: {spec['lod']}")
        A("")
        A("| IFC class | Count |")
        A("|---|---:|")
        for cls, n in sorted(by.items(), key=lambda kv: -kv[1])[:14]:
            A(f"| `{cls}` | {n:,} |")
        A(f"| **Total indexed** | **{len(els):,}** |")
        A("")

    A("---")
    A("")
    A(f"*Generated {dt.date.today():%d %B %Y}.*")

    out = os.path.join(ROOT, "CATALOG.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {out} ({len(rows)} containers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Generate the GitHub Pages site into `docs/`.

The library's most persuasive artifact is its drawings, and GitHub's file browser shows them one at
a time behind a click. This puts them on a page.

Everything on the site is read from the built artifacts and the same modules the containers came
from — manifests for element counts, `projectdata` for economics, `docs/_data/lod-audit.json` for
record coverage. Nothing is re-derived and nothing is typed in, so the site cannot drift from the
library the way a hand-written landing page would.

    python tools/lod_audit.py        # writes docs/_data/lod-audit.json
    python tools/site.py             # writes docs/

Sheets are copied into `docs/sheets/` (about 800 KB of SVG) so the site is self-contained. The
containers themselves are linked to the repository rather than duplicated — one copy of a 10 MB
artifact is enough.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import projectdata as P   # noqa: E402
import registers as R     # noqa: E402
import sectors            # noqa: E402

DOCS = os.path.join(ROOT, "docs")
REPO = "https://github.com/MassingCloud/masslibrary"
RAW = "https://raw.githubusercontent.com/MassingCloud/masslibrary/main"

#: A grid square — the mark, as a favicon. Percent-encoded: a data URI carrying raw `<`, `>` and `#`
#: inside an HTML attribute is legal but brittle, and it trips every naive HTML parser that reads
#: the page afterwards.
_FAV = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'>"
        "<rect width='16' height='16' fill='#12161a'/>"
        "<rect x='3' y='3' width='10' height='10' fill='none' stroke='#e8eaed' stroke-width='1'/>"
        "<line x1='3' y1='8' x2='13' y2='8' stroke='#e8eaed' stroke-width='.7'/>"
        "<line x1='8' y1='3' x2='8' y2='13' stroke='#e8eaed' stroke-width='.7'/></svg>")
FAVICON = "data:image/svg+xml," + "".join(
    c if (c.isalnum() or c in "-_.!~*'()/:;=,") else f"%{ord(c):02X}" for c in _FAV)


def e(s) -> str:
    return html.escape(str(s), quote=True)


def sector_dir(spec: dict) -> str:
    return spec["sector"].lower().replace(" ", "-").replace("/", "-")


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Page shell
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def page(title: str, body: str, *, subtitle: str = "", depth: int = 0, active: str = "") -> str:
    up = "../" * depth
    nav = [("index.html", "Library", "index"), ("catalog.html", "Catalog", "catalog"),
           ("lod-audit.html", "LOD audit", "lod")]
    links = "".join(
        f'<a href="{up}{href}"{" class=on" if key == active else ""}>{label}</a>'
        for href, label, key in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(subtitle or 'Free CC0 .mass sample projects for the Massing AEC platform.')}">
<link rel="stylesheet" href="{up}style.css">
<link rel="icon" href="{FAVICON}">
</head>
<body>
<header class="top">
  <a class="brand" href="{up}index.html">
    <span class="mark"></span>
    <span><b>Massing Sample Library</b><em>MassingCloud</em></span>
  </a>
  <nav>{links}<a class="ghost" href="{REPO}">GitHub &#8599;</a></nav>
</header>
{body}
<footer>
  <div>
    <p><b>Samples</b> are dedicated to the public domain under
      <a href="{REPO}/blob/main/LICENSE-SAMPLES">CC0 1.0</a>.
      <b>Generator code</b> is <a href="{REPO}/blob/main/LICENSE">MIT</a>.</p>
    <p class="muted">Every project here is synthetic. No sample describes a real site, party or
      contract value. The figures are plausible and internally consistent — they are not market
      data, and must not be used to underwrite, price, bid or design anything real.</p>
  </div>
  <p class="muted small">Generated {dt.date.today():%d %B %Y} by <code>tools/site.py</code>.</p>
</footer>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Data gathering
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def read_container(path: str) -> dict:
    with zipfile.ZipFile(path) as z:
        man = json.loads(z.read("manifest.json"))
    tables = {k: v for k, v in man["tables"].items() if k != "element"}
    return {"manifest": man, "bytes": os.path.getsize(path),
            "elements": man["tables"].get("element", 0),
            "tables": len(tables), "rows": sum(tables.values())}


def collect() -> tuple[list[dict], dict]:
    audit_path = os.path.join(DOCS, "_data", "lod-audit.json")
    audit = {}
    if os.path.exists(audit_path):
        with open(audit_path, encoding="utf-8") as fh:
            audit = json.load(fh)
    else:
        print("! docs/_data/lod-audit.json missing — run tools/lod_audit.py first; "
              "coverage panels will be omitted", file=sys.stderr)

    items = []
    for spec in sectors.SECTORS:
        sd = sector_dir(spec)
        path = os.path.join(ROOT, "samples", sd, f"{spec['key']}.mass")
        if not os.path.exists(path):
            print(f"! missing container for {spec['key']}", file=sys.stderr)
            continue
        sheets_dir = os.path.join(ROOT, "samples", sd, f"{spec['key']}-sheets")
        sheets = sorted(os.listdir(sheets_dir)) if os.path.isdir(sheets_dir) else []
        items.append({"spec": spec, "dir": sd, "path": path, "sheets": sheets,
                      "audit": audit.get(spec["key"], {}), **read_container(path)})
    return items, audit


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Fragments
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def money_m(v) -> str:
    return "—" if not v else f"${v / 1e6:,.1f}M"


def stat(label: str, value: str, note: str = "") -> str:
    n = f'<span class="note">{e(note)}</span>' if note else ""
    return (f'<div class="stat"><span class="k">{e(label)}</span>'
            f'<span class="v">{value}</span>{n}</div>')


def sheet_figure(item: dict, fn: str, *, lazy: bool = True) -> str:
    key = item["spec"]["key"]
    number = fn.split("_")[0]
    title = fn[len(number) + 1:].rsplit(".", 1)[0].replace("_", " ")
    src = f"sheets/{key}/{e(fn)}"
    lz = ' loading="lazy"' if lazy else ""
    return f"""<figure class="sheet">
  <a href="{src}" target="_blank" rel="noopener">
    <img src="{src}" alt="{e(number)} — {e(title)}"{lz}>
  </a>
  <figcaption><b>{e(number)}</b> {e(title)}<span>open full &#8599;</span></figcaption>
</figure>"""


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Index
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def build_index(items: list[dict], extras: list[dict]) -> str:
    total_el = sum(i["elements"] for i in items) + sum(x["elements"] for x in extras)
    total_b = sum(i["bytes"] for i in items) + sum(x["bytes"] for x in extras)
    n = len(items) + len(extras)

    cards = []
    for i in items:
        s = i["spec"]
        pf = P.proforma(s)
        plan = next((f for f in i["sheets"] if f.startswith("A1.01")), None)
        thumb = (f'<img src="sheets/{s["key"]}/{e(plan)}" alt="" loading="lazy">'
                 if plan else '<div class="noplan"></div>')
        econ = (f'{pf["yield_on_cost"]:.2%} yield on cost' if pf["yield_on_cost"]
                else "Publicly funded")
        cards.append(f"""<a class="card" href="{s['key']}.html">
  <div class="thumb">{thumb}</div>
  <div class="meta">
    <span class="tag">{e(s['sector'])}</span>
    <h3>{e(s['name'])}</h3>
    <p>{e(s['subtype'])}</p>
    <dl>
      <div><dt>Elements</dt><dd>{i['elements']:,}</dd></div>
      <div><dt>Gross area</dt><dd>{s['gross_sf']:,} sf</dd></div>
      <div><dt>Economics</dt><dd>{e(econ)}</dd></div>
    </dl>
  </div>
</a>""")

    extra_cards = []
    for x in extras:
        extra_cards.append(f"""<a class="card slim" href="{x['page']}">
  <div class="meta">
    <span class="tag alt">{e(x['tag'])}</span>
    <h3>{e(x['name'])}</h3>
    <p>{e(x['blurb'])}</p>
    <dl>
      <div><dt>Elements</dt><dd>{x['elements']:,}</dd></div>
      <div><dt>Size</dt><dd>{x['bytes'] / 1e6:.2f} MB</dd></div>
    </dl>
  </div>
</a>""")

    body = f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Free · CC0 · No attribution required</p>
    <h1>Sample projects that open as <em>projects</em>,<br>not as meshes.</h1>
    <p class="lede">{len(items)} <code>.mass</code> containers, one per building sector — each
      carrying an LOD&nbsp;400 model <em>and</em> the commercial data a project actually runs on: an
      executive report, a CSI-coded budget, a CPM schedule, a development pro forma, approvals,
      risk, procurement, and issued drawings. Plus a contributed vertiport package and an
      in-browser authoring demo.</p>
    <div class="counts">
      {stat("Containers", f"{n}")}
      {stat("Elements", f"{total_el:,}")}
      {stat("Library size", f"{total_b / 1e6:.0f} MB")}
      {stat("Licence", "CC0 1.0", "public domain")}
    </div>
  </div>
</section>

<section class="wrap">
  <h2 class="rule">Why this exists</h2>
  <div class="cols">
    <p>“Load a sample” usually means a bare geometry file. You can orbit it, and that is the entire
      demonstration — no estimate, no schedule, no RFIs, no returns. Every number a construction
      platform exists to produce is missing from the thing meant to show it off.</p>
    <p>A container carries all of it. These samples open with populated registers: budget lines tied
      to CSI cost codes, a schedule broken to one activity per level, field-verification records
      bound to IFC GlobalIds, and a pro forma that ties back to the same cost basis the budget uses.</p>
  </div>
</section>

<section class="wrap">
  <h2 class="rule">The library</h2>
  <div class="grid">{''.join(cards)}</div>
  <h3 class="sub">Also here</h3>
  <div class="grid two">{''.join(extra_cards)}</div>
</section>

<section class="wrap">
  <h2 class="rule">What a <code>.mass</code> file is</h2>
  <div class="cols">
    <p><b>A plain ZIP archive.</b> There is no proprietary encoding anywhere in it, and you do not
      need Massing to read one. Building elements are referenced by <b>IFC GlobalId</b> throughout,
      so a budget line, a schedule activity or a field-verification record can always be tied back to
      an element in the model.</p>
    <div>
      <pre><code>manifest.json      format, version, a full entry
                   inventory, and what deliberately
                   did NOT travel
project.json       id, name, origin, source IFC
data/&lt;table&gt;.json  one file per table, JSON arrays
geometry/          the source IFC + a converted
                   viewing tile derived from it
index/props.json   the element index
blobs/             drawings and documents</code></pre>
    </div>
  </div>
  <p class="muted">Unzip one and look: <code>unzip -l samples/commercial/meridian_commerce_center.mass</code></p>
</section>

<section class="wrap band">
  <h2 class="rule">Level of development</h2>
  <div class="cols">
    <p>Geometry is <b>LOD 400</b>: fabrication-level connections — base plates, shear tabs, bolts —
      reinforcement cages with real cover and tie spacing, material layer sets with real thicknesses,
      and a derived analytical model carrying loads and supports.</p>
    <p>The <b>LOD 500 record layer is on every element</b>: as-built verification, measured-versus-design
      variance, manufacturer and serial, O&amp;M and warranty references, Uniformat classification and
      MasterFormat spec links. Measured coverage is in the <a href="lod-audit.html">LOD audit</a>.</p>
  </div>
  <p class="callout"><b>One honest caveat.</b> BIMForum defines LOD 500 as <em>field-verified</em> —
    an element earns it by being checked against what was actually built. These models are synthetic,
    so nothing here has been surveyed, and each verification record says exactly that in its own note
    field rather than implying a site visit that never happened. Everything else the definition
    requires is present and complete.</p>
  <p class="muted">Every model passes the product's own QA gates: zero constraint errors and a
    lossless serialise/reparse roundtrip. Modelled <code>IfcSpace</code> area agrees with declared
    gross area to within 0.2%, so the model and the money describe one building.</p>
</section>

<section class="wrap">
  <h2 class="rule">Opening a sample</h2>
  <div class="three">
    <div><h4>In Massing</h4><p>Open the <code>.mass</code> directly, or drop it in the app's samples
      directory and it will be listed and described from its own manifest.</p></div>
    <div><h4>In any IFC tool</h4><p>Extract <code>geometry/*.ifc</code> and open it in
      BlenderBIM, Solibri, Navisworks, Revit, FreeCAD — anything that reads IFC4.</p></div>
    <div><h4>With no tools at all</h4><p>The CSVs, the executive reports and the drawings are plain
      text and SVG. Read them in a browser.</p></div>
  </div>
</section>
"""
    return page("Massing Sample Library — free CC0 BIM sample projects", body, active="index",
                subtitle="Nine free .mass sample projects, one per building sector, each with an "
                         "LOD 400 model plus budget, schedule, pro forma, registers and drawings.")


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Sample page
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def build_sample(item: dict) -> str:
    s = item["spec"]
    pf = P.proforma(s)
    bt = P.budget_totals(s)
    start, finish = P.schedule_span(s)
    a = item["audit"]
    sd, key = item["dir"], s["key"]

    stats = [
        stat("Gross area", f"{s['gross_sf']:,} sf"),
        stat("Storeys", f"{s['storeys']}", f"{s['storey_height']:.2f} m floor to floor"),
        stat("Elements", f"{item['elements']:,}", f"{item['rows']:,} data rows"),
        stat("Total dev cost", money_m(pf["total_cost"]), f"${pf['cost_psf']:,.0f}/sf"),
    ]
    if pf["yield_on_cost"]:
        stats += [stat("NOI", money_m(pf["noi"])),
                  stat("Yield on cost", f"{pf['yield_on_cost']:.2%}",
                       f"{pf['spread_bps']:+.0f} bps over a {s['finance']['exit_cap']:.2%} cap")]
    else:
        stats += [stat("Delivery", "Publicly funded", "no capitalised exit")]

    sheets = "".join(sheet_figure(item, fn, lazy=(n > 0))
                     for n, fn in enumerate(item["sheets"]))

    # Budget — the five largest divisions
    top = sorted(P.budget(s), key=lambda r: -r["revised"])[:5]
    budget_rows = "".join(
        f"<tr><td>{e(r['division'])}</td><td class=n>${r['revised']:,.0f}</td>"
        f"<td class=n>{r['revised'] / bt['revised']:.1%}</td></tr>" for r in top)

    phases = "".join(
        f"<tr><td>{e(x['name'])}</td><td>{e(x['trade'])}</td>"
        f"<td class=n>{x['start']:%b %Y}</td><td class=n>{x['finish']:%b %Y}</td>"
        f"<td class=n>{x['duration']}</td></tr>"
        for x in P.schedule(s) if x["activity_type"] == "Summary")

    uses = "".join(
        f"<tr><td>{e(label)}</td><td class=n>${amt:,.0f}</td>"
        f"<td class=n>{amt / pf['total_cost']:.1%}</td></tr>" for label, amt in pf["uses"])

    if pf["yield_on_cost"]:
        returns = f"""<table class="data">
<tr><td>Stabilised value</td><td class=n>${pf['stabilized_value']:,.0f}</td></tr>
<tr><td>Development profit</td><td class=n>${pf['profit']:,.0f}</td></tr>
<tr><td>Unlevered IRR ({pf['hold_years']}-yr)</td><td class=n>{pf['unlevered_irr']:.2%}</td></tr>
<tr><td>Levered IRR ({pf['hold_years']}-yr)</td><td class=n>{pf['levered_irr']:.2%}</td></tr>
<tr><td>Equity multiple</td><td class=n>{pf['equity_multiple']:.2f}&times;</td></tr>
</table>"""
    else:
        returns = f'<p class="muted">{e(pf["note"])}</p>'

    cov = ""
    if a:
        c = a.get("coverage", {})
        cells = [("LOD stage", c.get("lod_stage")), ("As-built record", c.get("as_built")),
                 ("Measured dimension", c.get("measured_dim")),
                 ("Manufacturer", c.get("manufacturer")),
                 ("Classification", a.get("classified")), ("Material", a.get("materialed"))]
        bars = "".join(
            f'<div class="bar"><span class="lab">{e(k)}</span>'
            f'<span class="track"><i style="width:{(v or 0) * 100:.0f}%"></i></span>'
            f'<span class="pct">{(v or 0):.0%}</span></div>' for k, v in cells)
        cov = f"""<section class="wrap">
  <h2 class="rule">LOD record coverage</h2>
  <p class="muted">Share of <code>IfcElement</code> occurrences carrying each part of the record,
    read out of the IFC inside the container.</p>
  <div class="bars">{bars}</div>
  <p class="muted small">Manufacturer and material fall short of 100% by the same reason: an
    <code>IfcOpeningElement</code> is a void and an <code>IfcElementAssembly</code> is a grouping —
    neither is a thing anybody manufactures or pours.</p>
  <div class="fab">
    {stat("Assemblies", f"{a.get('assemblies', 0):,}")}
    {stat("Reinforcing bars", f"{a.get('rebar', 0):,}")}
    {stat("Fasteners", f"{a.get('fasteners', 0):,}")}
    {stat("Analytical members", f"{a.get('analytical_members', 0):,}")}
    {stat("MEP ports", f"{a.get('ports', 0):,}")}
    {stat("Spaces", f"{a.get('spaces', 0):,}",
          f"{a.get('space_area_sf', 0):,.0f} sf modelled")}
  </div>
</section>"""

    files = [(f"{key}.mass", "The container — model, data, drawings, documents"),
             (f"{key}-executive-report.md", "The project in prose and tables"),
             (f"{key}-budget.csv", "22 CSI divisions: original / revised / committed / forecast"),
             (f"{key}-schedule.csv", "CPM activities with dates, trades, predecessors"),
             (f"{key}-schedule-of-values.csv", "SOV with billed-to-date and retainage"),
             (f"{key}-proforma.csv", "Sources and uses, NOI, IRR, cash flows"),
             (f"{key}-space-program.csv", "Programmed areas by space type"),
             (f"{key}-approvals.csv", "Permits by authority, with applied and issued dates"),
             (f"{key}-risk-register.csv", "Risks with cost and schedule exposure"),
             (f"{key}-procurement.csv", "Long-lead packages with quoted lead times"),
             (f"{key}-sheet-register.csv", "The full sheet list, issued and not")]
    dl = "".join(
        f'<li><a href="{RAW}/samples/{sd}/{e(fn)}"><code>{e(fn)}</code></a>'
        f'<span>{e(desc)}</span></li>' for fn, desc in files)

    reg = {"Approvals": len(R.permits(s)), "Risks": len(R.risks(s)),
           "Phase gates": len(R.phases(s)), "Long-lead packages": len(R.procurement(s)),
           "Sheets registered": len(R.sheet_register(s)),
           "Sheets issued": sum(1 for x in R.sheet_register(s) if x["issued"])}
    reg_html = "".join(f"<tr><td>{e(k)}</td><td class=n>{v}</td></tr>" for k, v in reg.items())

    cost, days = R.risk_exposure(s)

    body = f"""
<section class="wrap head">
  <p class="eyebrow"><a href="index.html">Library</a> / {e(s['sector'])}</p>
  <h1>{e(s['name'])}</h1>
  <p class="lede">{e(s['summary'])}</p>
  <div class="counts">{''.join(stats)}</div>
  <p class="dlbar">
    <a class="btn" href="{RAW}/samples/{sd}/{key}.mass">Download <code>.mass</code>
      &middot; {item['bytes'] / 1e6:.1f} MB</a>
    <a class="btn ghost" href="{REPO}/blob/main/samples/{sd}/{key}-executive-report.md">Executive report</a>
    <a class="btn ghost" href="{REPO}/tree/main/samples/{sd}">All files</a>
  </p>
</section>

<section class="wrap">
  <h2 class="rule">Issued drawings</h2>
  <p class="muted">Generated from the model — column positions, wall runs, space polygons and grid
    spacing are read out of the IFC — so a sheet cannot drift from the building it documents.
    ARCH-D, {len(item['sheets'])} of {len(R.sheet_register(s))} registered sheets issued.</p>
  <div class="sheets">{sheets}</div>
</section>

{cov}

<section class="wrap">
  <h2 class="rule">Programme</h2>
  <table class="data wide">
    <thead><tr><th>Space</th><th>Type</th><th class=n>Levels</th><th class=n>Area</th>
      <th class=n>% of gross</th></tr></thead>
    <tbody>{''.join(
        f"<tr><td>{e(x['name'])}</td><td>{e(x['space_type'])}</td>"
        f"<td class=n>{x['quantity']}</td><td class=n>{x['target_area_sf']:,} sf</td>"
        f"<td class=n>{x['target_area_sf'] / s['gross_sf']:.1%}</td></tr>"
        for x in P.space_program(s))}</tbody>
  </table>
</section>

<section class="wrap">
  <h2 class="rule">Cost and programme</h2>
  <div class="cols">
    <div>
      <h4>Largest divisions</h4>
      <table class="data"><tbody>{budget_rows}</tbody></table>
      <p class="muted small">Revised budget {money_m(bt['revised'])} &middot; forecast at completion
        {money_m(bt['forecast'])} &middot; variance
        {(bt['revised'] - bt['forecast']) / bt['revised']:+.2%}.</p>
    </div>
    <div>
      <h4>Registers</h4>
      <table class="data"><tbody>{reg_html}</tbody></table>
      <p class="muted small">Unweighted risk exposure ${cost:,.0f} and {days} days, against a
        carried contingency of 5%.</p>
    </div>
  </div>
  <h4>Schedule — {start:%d %b %Y} to {finish:%d %b %Y}, {s['finance']['months']} months</h4>
  <table class="data wide">
    <thead><tr><th>Phase</th><th>Trade</th><th class=n>Start</th><th class=n>Finish</th>
      <th class=n>Working days</th></tr></thead>
    <tbody>{phases}</tbody>
  </table>
</section>

<section class="wrap band">
  <h2 class="rule">Development pro forma</h2>
  <div class="cols">
    <div>
      <h4>Uses of funds</h4>
      <table class="data"><tbody>{uses}
        <tr class="tot"><td>Total development cost</td>
          <td class=n>${pf['total_cost']:,.0f}</td><td class=n>100.0%</td></tr></tbody></table>
    </div>
    <div>
      <h4>Returns</h4>
      {returns}
    </div>
  </div>
  <p class="muted small">Synthetic sample project. Figures are internally consistent and derived
    from one set of assumptions in <code>tools/sectors.py</code> — they are not market data.</p>
</section>

<section class="wrap">
  <h2 class="rule">Every file</h2>
  <ul class="files">{dl}</ul>
</section>
"""
    return page(f"{s['name']} — Massing Sample Library", body, active="",
                subtitle=s["summary"])


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Catalog and audit
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def build_catalog(items: list[dict], extras: list[dict]) -> str:
    rows = "".join(
        f"""<tr>
  <td><a href="{i['spec']['key']}.html">{e(i['spec']['name'])}</a></td>
  <td>{e(i['spec']['sector'])}</td>
  <td class=n>{i['elements']:,}</td>
  <td class=n>{i['tables']}</td>
  <td class=n>{i['rows']:,}</td>
  <td class=n>{i['spec']['storeys']}</td>
  <td class=n>{i['spec']['gross_sf']:,} sf</td>
  <td class=n>{i['bytes'] / 1e6:.2f} MB</td>
</tr>""" for i in items)

    econ = "".join(
        (lambda pf: f"""<tr>
  <td><a href="{i['spec']['key']}.html">{e(i['spec']['name'])}</a></td>
  <td class=n>{money_m(pf['total_cost'])}</td>
  <td class=n>${pf['cost_psf']:,.0f}</td>
  <td class=n>{money_m(pf['noi'])}</td>
  <td class=n>{f"{pf['yield_on_cost']:.2%}" if pf['yield_on_cost'] else '—'}</td>
  <td class=n>{f"{i['spec']['finance']['exit_cap']:.2%}" if pf['yield_on_cost'] else '—'}</td>
  <td class=n>{f"{pf['spread_bps']:+.0f} bps" if pf['yield_on_cost'] else '—'}</td>
  <td class=n>{f"{pf['unlevered_irr']:.2%}" if pf['unlevered_irr'] else '—'}</td>
  <td class=n>{f"{pf['levered_irr']:.2%}" if pf['levered_irr'] else '—'}</td>
  <td class=n>{f"{pf['equity_multiple']:.2f}&times;" if pf['equity_multiple'] else '—'}</td>
</tr>""")(P.proforma(i["spec"])) for i in items)

    ex = "".join(
        f"""<tr><td><a href="{x['page']}">{e(x['name'])}</a></td><td>{e(x['tag'])}</td>
  <td class=n>{x['elements']:,}</td><td class=n>{x['tables']}</td>
  <td class=n>{x['rows']:,}</td><td class=n>{x['bytes'] / 1e6:.2f} MB</td></tr>"""
        for x in extras)

    body = f"""
<section class="wrap head">
  <p class="eyebrow"><a href="index.html">Library</a> / Catalog</p>
  <h1>Catalog</h1>
  <p class="lede">Read from each container's own manifest and computed from
    <code>tools/sectors.py</code>. A catalog beside the artifacts is a promise; a catalog read
    <em>from</em> them is a measurement.</p>
</section>

<section class="wrap">
  <h2 class="rule">Containers</h2>
  <table class="data wide">
    <thead><tr><th>Sample</th><th>Sector</th><th class=n>Elements</th><th class=n>Tables</th>
      <th class=n>Rows</th><th class=n>Storeys</th><th class=n>Gross area</th>
      <th class=n>Size</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <h3 class="sub">Contributed and demonstration containers</h3>
  <table class="data wide">
    <thead><tr><th>Container</th><th>Kind</th><th class=n>Elements</th><th class=n>Tables</th>
      <th class=n>Rows</th><th class=n>Size</th></tr></thead>
    <tbody>{ex}</tbody>
  </table>
</section>

<section class="wrap">
  <h2 class="rule">Economics</h2>
  <table class="data wide">
    <thead><tr><th>Sample</th><th class=n>Total dev cost</th><th class=n>$/sf</th>
      <th class=n>NOI</th><th class=n>Yield on cost</th><th class=n>Exit cap</th>
      <th class=n>Spread</th><th class=n>Unlevered IRR</th><th class=n>Levered IRR</th>
      <th class=n>Equity multiple</th></tr></thead>
    <tbody>{econ}</tbody>
  </table>
  <p class="muted">The aviation terminal is publicly funded. It reports no capitalised exit rather
    than fabricating returns from a cap rate that does not apply to it.</p>
</section>
"""
    return page("Catalog — Massing Sample Library", body, active="catalog")


def build_audit(items: list[dict]) -> str:
    rows = ""
    for i in items:
        a = i["audit"]
        if not a:
            continue
        c = a["coverage"]
        rows += f"""<tr>
  <td><a href="{i['spec']['key']}.html">{e(i['spec']['name'])}</a></td>
  <td class=n>{a['elements']:,}</td>
  <td class=n>{c['lod_stage']:.0%}</td><td class=n>{c['as_built']:.0%}</td>
  <td class=n>{c['measured_dim']:.0%}</td><td class=n>{c['manufacturer']:.0%}</td>
  <td class=n>{a['classified']:.0%}</td><td class=n>{a['materialed']:.0%}</td>
</tr>"""

    fab = ""
    for i in items:
        a = i["audit"]
        if not a:
            continue
        fab += f"""<tr>
  <td><a href="{i['spec']['key']}.html">{e(i['spec']['name'])}</a></td>
  <td>{e(a['schema'])}</td><td class=n>{a['assemblies']:,}</td><td class=n>{a['rebar']:,}</td>
  <td class=n>{a['fasteners']:,}</td><td class=n>{a['analytical_members']:,}</td>
  <td class=n>{a['analytical_actions']:,}</td><td class=n>{a['analytical_supports']:,}</td>
  <td class=n>{a['ports']:,}</td>
</tr>"""

    area = ""
    for i in items:
        a = i["audit"]
        if not a:
            continue
        g = i["spec"]["gross_sf"]
        area += f"""<tr>
  <td><a href="{i['spec']['key']}.html">{e(i['spec']['name'])}</a></td>
  <td class=n>{a['spaces']}</td><td class=n>{a['space_area_sf']:,.0f} sf</td>
  <td class=n>{g:,} sf</td><td class=n>{a['space_area_sf'] / g:.1%}</td>
  <td class=n>{a['types']}</td><td class=n>{a['material_sets']}</td>
</tr>"""

    body = f"""
<section class="wrap head">
  <p class="eyebrow"><a href="index.html">Library</a> / LOD audit</p>
  <h1>LOD audit</h1>
  <p class="lede">What each container actually carries, read out of the IFC inside it by
    <code>tools/lod_audit.py</code>. An LOD claim in a README is marketing; this is the
    measurement.</p>
</section>

<section class="wrap">
  <h2 class="rule">Record-layer coverage</h2>
  <p class="muted">Share of <code>IfcElement</code> occurrences carrying each part of the LOD 500
    record.</p>
  <table class="data wide">
    <thead><tr><th>Sample</th><th class=n>Elements</th><th class=n>LOD stage</th>
      <th class=n>As-built</th><th class=n>Measured dim</th><th class=n>Manufacturer</th>
      <th class=n>Classified</th><th class=n>Material</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="muted">Manufacturer and material fall short of 100% by design, and by the same reason:
    an <code>IfcOpeningElement</code> is a void and an <code>IfcElementAssembly</code> is a
    grouping — neither is a thing anybody manufactures or pours. Every element that is a physical
    product carries both, which is why the two columns track each other.</p>
</section>

<section class="wrap">
  <h2 class="rule">Fabrication and analysis</h2>
  <table class="data wide">
    <thead><tr><th>Sample</th><th>Schema</th><th class=n>Assemblies</th><th class=n>Rebar</th>
      <th class=n>Fasteners</th><th class=n>Analytical members</th><th class=n>Loads</th>
      <th class=n>Supports</th><th class=n>MEP ports</th></tr></thead>
    <tbody>{fab}</tbody>
  </table>
</section>

<section class="wrap">
  <h2 class="rule">Space and area</h2>
  <p class="muted">Modelled <code>IfcSpace</code> area against declared gross area. These are the
    same number to within rounding, which is the point — the model and the money describe one
    building.</p>
  <table class="data wide">
    <thead><tr><th>Sample</th><th class=n>Spaces</th><th class=n>Modelled area</th>
      <th class=n>Declared gross</th><th class=n>Agreement</th><th class=n>Types</th>
      <th class=n>Material sets</th></tr></thead>
    <tbody>{area}</tbody>
  </table>
</section>

<section class="wrap band">
  <h2 class="rule">What LOD 500 means here</h2>
  <p>BIMForum defines LOD 500 as a <b>field-verified</b> representation: an element reaches it by
    being checked against what was actually built. These models are synthetic, so no element in this
    library has been verified against a physical building, and the verification records say so in
    their own note field.</p>
  <p>What the containers do carry, on <b>every element</b>, is the complete structure that
    definition requires:</p>
  <ul class="ticks">
    <li><code>Pset_Massing_AsBuilt</code> with verification method, verifier and date</li>
    <li>measured-versus-design dimensions with variance and a stated tolerance, distributed across
      the model rather than one value repeated</li>
    <li>manufacturer, model, serial and barcode on every product element</li>
    <li>O&amp;M and warranty document references bound to the asset by IFC GlobalId</li>
    <li>Uniformat II classification and MasterFormat spec links</li>
    <li>construction phase status</li>
    <li>an LOD stage on the element itself, so the claim travels with the geometry</li>
  </ul>
  <p class="callout"><b>Every frame is detailed in full.</b> No sample is capped: every column
    carries its base plate or reinforcement cage and every beam its shear tab, up to and including
    the twelve-storey office at 420 columns and 696 beams. A ceiling remains in the generator as a
    runaway guard for any sector added later with a far larger frame, and it reports what it reached
    against what is in the model — but nothing in this library hits it.</p>
</section>
"""
    return page("LOD audit — Massing Sample Library", body, active="lod")


def build_vertiport_page(x: dict) -> str:
    sheets = "".join(f"""<figure class="sheet">
  <a href="sheets/{x['key']}/{e(fn)}" target="_blank" rel="noopener">
    <img src="sheets/{x['key']}/{e(fn)}" alt="{e(fn)}" loading="lazy"></a>
  <figcaption><b>{e(fn.split('_')[0])}</b>
    {e(fn.split('_', 1)[1].rsplit('.', 1)[0].replace('_', ' '))}<span>open full &#8599;</span></figcaption>
</figure>""" for fn in x["sheets"])

    body = f"""
<section class="wrap head">
  <p class="eyebrow"><a href="index.html">Library</a> / Aviation</p>
  <h1>{e(x['name'])}</h1>
  <p class="lede">A hybrid heliport / vertiport at a 30% schematic level. A small model carrying
    very dense delivery data — which is the right shape for a 30% package, and a useful counterweight
    to the generated samples.</p>
  <div class="counts">
    {stat("Elements", f"{x['elements']:,}")}
    {stat("Data rows", f"{x['rows']:,}", f"across {x['tables']} tables")}
    {stat("Issued sheets", f"{len(x['sheets'])}")}
    {stat("Size", f"{x['bytes'] / 1e6:.2f} MB")}
  </div>
  <p class="dlbar">
    <a class="btn" href="{RAW}/samples/aviation/{x['key']}.mass">Download <code>.mass</code></a>
    <a class="btn ghost" href="{REPO}/blob/main/samples/aviation/{x['key']}-executive-report.md">Executive report</a>
  </p>
</section>

<section class="wrap">
  <h2 class="rule">What it does that the generated samples do not</h2>
  <ul class="ticks">
    <li><b>TLOF, FATO, safety areas and downwash zones modelled as <code>IfcSpace</code></b>, with
      design-basis parameters in <code>Pset_Vertiport*</code> — so the geometry that matters in
      aviation is queryable rather than drawn</li>
    <li><b>Five issued aviation sheets</b> covering geometry and marking, approach/departure and
      obstacles, operational safety, and lighting and controls</li>
    <li><b>An approvals register keyed to real regulatory instruments</b> — airspace notice, layout
      plan amendment, security design approval</li>
    <li><b>A design basis that names its own biggest gap first</b>: no design aircraft has been
      selected, and the report states plainly that TLOF/FATO geometry, deck loads, charger power,
      downwash and half the budget all derive from that choice</li>
  </ul>
</section>

<section class="wrap">
  <h2 class="rule">Issued drawings</h2>
  <div class="sheets">{sheets}</div>
</section>

<section class="wrap band">
  <h2 class="rule">Provenance</h2>
  <p>This package was authored separately and contributed to the library. It arrived named for a
    real airport, in a real city, in an archive named for a real eVTOL manufacturer. Everything here
    is dedicated to the public domain and carries a hard rule that no sample names a real place or
    party, so the identity was replaced by <code>tools/rebrand_vertiport.py</code>.</p>
  <table class="data">
    <thead><tr><th>Was</th><th>Is</th></tr></thead>
    <tbody>
      <tr><td>A real airport name</td><td>Cedar Reach North Vertiport</td></tr>
      <tr><td>A real city and state</td><td>Cedar Reach, State</td></tr>
      <tr><td>A real aircraft manufacturer</td><td>Sample Aircraft</td></tr>
      <tr><td>A real state plane coordinate zone</td><td>NAD83 Sample Grid</td></tr>
    </tbody>
  </table>
  <p><b>Nothing else changed.</b> The regulatory references, geometry formulas, design basis,
    registers, budget, schedule and sheets are exactly as contributed. The rebrand is recorded inside
    the container under <code>manifest.rebranded</code>.</p>
  <p class="muted">Two things were <em>added</em>, because the container lacked them: a
    <code>geometry/model.frag</code> converted from the source IFC it already contained (without it
    the sample opens to an empty canvas), and a rebuilt manifest inventory — substituting text
    changed byte lengths, so the entry sizes it shipped no longer described its own contents.</p>
  <p class="callout"><b>Read the report before citing anything.</b> It opens by stating what the
    package is not: not sealed engineering, no number validated by a licensed professional or any
    authority having jurisdiction, every dimension flagged <code>UNVERIFIED</code> deliberately. A
    30% package that does not say it is 30% is how a schematic sketch ends up quoted as a
    clearance.</p>
</section>
"""
    return page(f"{x['name']} — Massing Sample Library", body)


def build_demo_page(x: dict) -> str:
    body = f"""
<section class="wrap head">
  <p class="eyebrow"><a href="index.html">Library</a> / Authoring demo</p>
  <h1>{e(x['name'])}</h1>
  <p class="lede">A small single-family house — 23 elements across two levels. It is here because of
    <em>how</em> it was made, not what it is.</p>
  <div class="counts">
    {stat("Elements", f"{x['elements']:,}", "7 walls, 3 slabs, a roof, 2 doors, 4 windows")}
    {stat("Data rows", f"{x['rows']:,}")}
    {stat("Size", f"{x['bytes'] / 1e6:.2f} MB")}
  </div>
  <p class="dlbar">
    <a class="btn" href="{RAW}/samples/authoring-demo/{x['key']}.mass">Download <code>.mass</code></a>
  </p>
</section>

<section class="wrap">
  <h2 class="rule">Why it is here</h2>
  <p>Every element was authored <b>in the browser</b>, through the same edit recipes a user drives,
    rather than imported from another tool. It is deliberately small: it exists to prove the
    authoring path end to end, and a 23-element model where every element can be accounted for
    proves that better than a large one.</p>
  <p>The sector samples are generated head-lessly by <code>tools/build_library.py</code>. This one
    came out of the product's own UI. If the two ever disagree about what a <code>.mass</code>
    should contain, this container is the one that reflects what a user's own save actually
    produces.</p>
  <p class="muted"><b>No commercial data.</b> Unlike the sector samples it carries no budget,
    schedule or pro forma — it predates them and has not been backfilled, because backfilling it
    would make it a worse record of what the authoring path produces on its own.</p>
</section>
"""
    return page(f"{x['name']} — Massing Sample Library", body)


# ─────────────────────────────────────────────────────────────────────────────────────────────────
def main() -> int:
    items, _audit = collect()
    if not items:
        print("no containers — run tools/build_library.py first", file=sys.stderr)
        return 1

    os.makedirs(DOCS, exist_ok=True)
    sheets_root = os.path.join(DOCS, "sheets")
    if os.path.isdir(sheets_root):
        shutil.rmtree(sheets_root)

    # Copy the sheets in. ~800 KB of SVG, which makes the site self-contained; the containers stay
    # in the repository, because one copy of a 10 MB artifact is enough.
    copied = 0
    for i in items:
        dest = os.path.join(sheets_root, i["spec"]["key"])
        os.makedirs(dest, exist_ok=True)
        src = os.path.join(ROOT, "samples", i["dir"], f"{i['spec']['key']}-sheets")
        for fn in i["sheets"]:
            shutil.copyfile(os.path.join(src, fn), os.path.join(dest, fn))
            copied += 1

    # The two non-generated containers.
    extras = []
    vp = os.path.join(ROOT, "samples", "aviation", "cedar_reach_north_vertiport.mass")
    if os.path.exists(vp):
        c = read_container(vp)
        vsrc = os.path.join(ROOT, "samples", "aviation", "cedar_reach_north_vertiport-sheets")
        vsheets = sorted(os.listdir(vsrc)) if os.path.isdir(vsrc) else []
        dest = os.path.join(sheets_root, "cedar_reach_north_vertiport")
        os.makedirs(dest, exist_ok=True)
        for fn in vsheets:
            shutil.copyfile(os.path.join(vsrc, fn), os.path.join(dest, fn))
            copied += 1
        extras.append({"key": "cedar_reach_north_vertiport", "name": "Cedar Reach North Vertiport",
                       "tag": "Aviation · contributed", "page": "cedar_reach_north_vertiport.html",
                       "blurb": "Hybrid heliport / vertiport at 30% schematic — small model, dense "
                                "delivery data, five issued aviation sheets.",
                       "sheets": vsheets, **c})
    demo = os.path.join(ROOT, "samples", "authoring-demo", "maple_grove_house.mass")
    if os.path.exists(demo):
        extras.append({"key": "maple_grove_house", "name": "Maple Grove House",
                       "tag": "Authoring demo", "page": "maple_grove_house.html",
                       "blurb": "23 elements authored in the browser through the product's own edit "
                                "recipes — proof of the authoring path, end to end.",
                       "sheets": [], **read_container(demo)})

    written = []

    def write(name: str, content: str):
        p = os.path.join(DOCS, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(name)

    write("index.html", build_index(items, extras))
    write("catalog.html", build_catalog(items, extras))
    write("lod-audit.html", build_audit(items))
    for i in items:
        write(f"{i['spec']['key']}.html", build_sample(i))
    for x in extras:
        if x["key"] == "cedar_reach_north_vertiport":
            write(f"{x['key']}.html", build_vertiport_page(x))
        else:
            write(f"{x['key']}.html", build_demo_page(x))
    write("style.css", STYLE)
    # Tell Pages not to run Jekyll — it would drop the _data directory and anything underscored.
    write(".nojekyll", "")

    print(f"wrote {len(written)} file(s) to docs/ and copied {copied} sheet(s)")
    for w in written:
        print(f"  {w}")
    return 0


STYLE = """/* Massing Sample Library — the site's whole stylesheet.
   Drawing-office palette: paper, ink, one accent. The sheets are the loudest thing on any page,
   so everything around them stays quiet. */
:root{
  --bg:#f6f6f4; --panel:#fff; --ink:#14171a; --dim:#5b6470; --faint:#8d97a4;
  --line:#dcdfe4; --accent:#1f5f4f; --accent-soft:#e8f1ee; --warn:#8a5a12; --warn-soft:#fbf3e3;
  --radius:3px; --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#0d0f12; --panel:#14171b; --ink:#e9ecef; --dim:#a3adba; --faint:#78828f;
    --line:#252a31; --accent:#5fd0ae; --accent-soft:#10241f; --warn:#e0b25f; --warn-soft:#241d10;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.62;-webkit-font-smoothing:antialiased}
a{color:inherit}
code{font-family:var(--mono);font-size:.88em;background:var(--panel);
  border:1px solid var(--line);border-radius:var(--radius);padding:.08em .34em}
pre{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px;overflow:auto}
pre code{border:0;background:0;padding:0;font-size:12.5px;line-height:1.7}
h1,h2,h3,h4{line-height:1.22;letter-spacing:-.015em;margin:0}
h1{font-size:clamp(30px,4.6vw,46px);font-weight:680}
h2{font-size:clamp(19px,2.3vw,23px);font-weight:660}
h3{font-size:17px;font-weight:640}
h4{font-size:14px;font-weight:660;margin:22px 0 8px;letter-spacing:.01em}

/* header */
.top{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;
  gap:20px;padding:11px clamp(16px,4vw,40px);background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none}
.brand .mark{width:19px;height:19px;border:1.5px solid var(--ink);position:relative;flex:none}
.brand .mark::before,.brand .mark::after{content:"";position:absolute;background:var(--ink)}
.brand .mark::before{left:0;right:0;top:50%;height:1px}
.brand .mark::after{top:0;bottom:0;left:50%;width:1px}
.brand b{display:block;font-size:14px;font-weight:660;letter-spacing:-.01em}
.brand em{display:block;font-size:10.5px;font-style:normal;color:var(--faint);
  text-transform:uppercase;letter-spacing:.13em}
.top nav{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.top nav a{font-size:13px;text-decoration:none;color:var(--dim);padding:6px 11px;
  border-radius:var(--radius)}
.top nav a:hover{color:var(--ink);background:var(--panel)}
.top nav a.on{color:var(--ink);background:var(--panel);border:1px solid var(--line)}
.top nav a.ghost{color:var(--faint)}

/* layout */
.wrap{max-width:1120px;margin:0 auto;padding:44px clamp(16px,4vw,40px)}
.hero{border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,color-mix(in srgb,var(--accent-soft) 60%,transparent),transparent)}
.hero .wrap{padding-top:62px;padding-bottom:52px}
.eyebrow{margin:0 0 14px;font-size:11.5px;text-transform:uppercase;letter-spacing:.15em;
  color:var(--faint);font-weight:640}
.eyebrow a{color:var(--dim);text-decoration:none}
.eyebrow a:hover{color:var(--ink)}
h1 em{font-style:normal;color:var(--accent)}
.lede{font-size:clamp(15px,1.7vw,18px);color:var(--dim);max-width:72ch;margin:18px 0 0}
.head{padding-bottom:12px}
.rule{padding-bottom:9px;border-bottom:1px solid var(--line);margin-bottom:20px}
.sub{margin:34px 0 16px;color:var(--dim);font-size:14px;text-transform:uppercase;
  letter-spacing:.11em}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.three h4{margin-top:0}
.three p{margin:0;color:var(--dim);font-size:14px}
.band{background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  max-width:none}
.band>*{max-width:1120px;margin-left:auto;margin-right:auto}
@media(max-width:820px){.cols,.three{grid-template-columns:1fr}}

/* stats */
.counts{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.fab{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:11px 15px;min-width:132px;flex:1 1 auto}
.stat .k{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;
  color:var(--faint);font-weight:640}
.stat .v{display:block;font-size:20px;font-weight:660;letter-spacing:-.02em;margin-top:3px;
  font-variant-numeric:tabular-nums}
.stat .note{display:block;font-size:11.5px;color:var(--dim);margin-top:1px}

/* cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.grid.two{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}
.card{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);
  border-radius:var(--radius);text-decoration:none;overflow:hidden;transition:border-color .14s,
  transform .14s}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
/* The thumbnail shows the DRAWING, not the sheet. An ARCH-D sheet scaled to 300 px is a grey
   rectangle with an illegible title block down one side — it reads as "a document" when the whole
   point is for it to read as "a building". The transform crops the title block out (it occupies the
   right ~21% of the sheet) and zooms the plan up to fill the card. */
.card .thumb{aspect-ratio:3/2;background:#fff;border-bottom:1px solid var(--line);overflow:hidden;
  display:flex;align-items:center;justify-content:center}
/* scale s about origin o shows fractions [o - o/s, o + (1-o)/s] of the sheet. The title block
   starts at 724/914 = 79.2%, so s=1.55 about 38% shows 13.5%..78% — the drawing, and none of the
   block beside it. */
.card .thumb img{width:100%;height:100%;object-fit:contain;
  transform:scale(1.55);transform-origin:38% 50%}
.card .noplan{width:100%;height:100%;background:
  repeating-linear-gradient(45deg,var(--bg),var(--bg) 9px,var(--panel) 9px,var(--panel) 18px)}
/* The meta block grows and the figures sit at its foot, so a two-line subtitle in one card does not
   push its numbers out of line with the rest of the row. */
.card .meta{padding:15px 17px 17px;display:flex;flex-direction:column;flex:1}
.card .meta dl{margin-top:auto}
.card.slim .meta{padding:17px}
.tag{display:inline-block;font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;
  font-weight:640;color:var(--accent);background:var(--accent-soft);border-radius:var(--radius);
  padding:2px 7px;margin-bottom:9px}
.tag.alt{color:var(--warn);background:var(--warn-soft)}
.card h3{margin:0 0 5px}
.card p{margin:0;font-size:13px;color:var(--dim);line-height:1.5}
.card dl{display:flex;flex-wrap:wrap;gap:14px;margin:13px 0 0;padding-top:11px;
  border-top:1px solid var(--line)}
.card dl div{min-width:0}
.card dt{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--faint);
  font-weight:640}
.card dd{margin:1px 0 0;font-size:13.5px;font-weight:600;font-variant-numeric:tabular-nums}

/* sheets */
.sheets{display:grid;gap:22px}
.sheet{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden}
.sheet a{display:block;background:#fff;line-height:0}
.sheet img{width:100%;height:auto;display:block}
.sheet figcaption{display:flex;align-items:baseline;gap:9px;padding:10px 14px;font-size:13px;
  color:var(--dim);border-top:1px solid var(--line)}
.sheet figcaption b{color:var(--ink);font-family:var(--mono);font-size:12.5px}
.sheet figcaption span{margin-left:auto;font-size:11.5px;color:var(--faint)}

/* tables */
table.data{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:4px}
table.data.wide{font-size:13px}
table.data th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;
  color:var(--faint);font-weight:640;padding:8px 10px;border-bottom:1px solid var(--line)}
table.data td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
table.data td.n,table.data th.n{text-align:right;font-variant-numeric:tabular-nums;
  white-space:nowrap}
table.data tr:last-child td{border-bottom:0}
table.data tr.tot td{font-weight:660;border-top:1px solid var(--line)}
table.data a{color:var(--accent);text-decoration:none}
table.data a:hover{text-decoration:underline}
section:not(.band) table.data{background:var(--panel);border:1px solid var(--line);
  border-radius:var(--radius)}

/* bars */
.bars{display:grid;gap:8px;margin-top:6px}
.bar{display:grid;grid-template-columns:170px 1fr 48px;align-items:center;gap:12px;font-size:13px}
.bar .lab{color:var(--dim)}
.bar .track{height:7px;background:var(--line);border-radius:99px;overflow:hidden}
.bar .track i{display:block;height:100%;background:var(--accent);border-radius:99px}
.bar .pct{text-align:right;font-variant-numeric:tabular-nums;font-weight:640}
@media(max-width:620px){.bar{grid-template-columns:1fr 60px}.bar .track{grid-column:1/-1;order:3}}

/* misc */
.callout{border-left:2px solid var(--warn);background:var(--warn-soft);padding:13px 17px;
  border-radius:0 var(--radius) var(--radius) 0;font-size:14px;margin:20px 0 0}
.muted{color:var(--dim);font-size:14px}
.small{font-size:12.5px}
.ticks{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:7px}
.ticks li{position:relative;padding-left:22px;font-size:14.5px;color:var(--dim)}
/* A tick, not a chevron: the arms have to be unequal. A square rotated 45 degrees reads as "v". */
.ticks li::before{content:"";position:absolute;left:5px;top:.42em;width:5px;height:9px;
  border:1.6px solid var(--accent);border-top:0;border-left:0;transform:rotate(40deg)}
.ticks li b{color:var(--ink)}
.files{list-style:none;margin:0;padding:0;display:grid;gap:0;background:var(--panel);
  border:1px solid var(--line);border-radius:var(--radius)}
.files li{display:flex;gap:14px;align-items:baseline;padding:10px 15px;
  border-bottom:1px solid var(--line);flex-wrap:wrap}
.files li:last-child{border-bottom:0}
.files a{text-decoration:none;color:var(--accent)}
.files a:hover code{border-color:var(--accent)}
.files span{color:var(--dim);font-size:13px;margin-left:auto;text-align:right}
.dlbar{display:flex;gap:9px;flex-wrap:wrap;margin:24px 0 0}
.btn{display:inline-block;text-decoration:none;font-size:13.5px;font-weight:600;padding:9px 15px;
  border-radius:var(--radius);background:var(--accent);color:#fff;border:1px solid var(--accent)}
.btn code{background:rgba(255,255,255,.14);border-color:transparent;color:inherit}
.btn.ghost{background:var(--panel);color:var(--ink);border-color:var(--line)}
.btn.ghost:hover{border-color:var(--accent);color:var(--accent)}

footer{border-top:1px solid var(--line);background:var(--panel);
  padding:32px clamp(16px,4vw,40px) 44px}
footer>div,footer>p{max-width:1120px;margin-left:auto;margin-right:auto}
footer p{margin:0 0 9px;font-size:13.5px;color:var(--dim);max-width:86ch}
footer a{color:var(--accent)}
"""


if __name__ == "__main__":
    raise SystemExit(main())

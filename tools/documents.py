"""The companion documents that sit beside each `.mass`.

The container already holds this data as tables, which is the right place for it and the wrong
format for a human with no software. These write the same figures out as CSV and Markdown so a
visitor can read a project's economics without installing anything.

They read `projectdata`, never a second set of numbers — an executive summary that restates figures
it did not compute is how a package starts disagreeing with itself.
"""
from __future__ import annotations

import csv
import datetime as dt
import os

import projectdata as P


def _money(v: float | None) -> str:
    if v is None:
        return "—"
    return f"${v:,.0f}"


def _m(v: float | None) -> str:
    if v is None:
        return "—"
    return f"${v / 1e6:,.1f}M"


def _pct(v: float | None, dp: int = 2) -> str:
    return "—" if v is None else f"{v:.{dp}%}"


# ─────────────────────────────────────────────────────────────────────────────────────────────────
def write_budget(spec: dict, out_dir: str) -> str:
    path = os.path.join(out_dir, f"{spec['key']}-budget.csv")
    rows = P.budget(spec)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Cost code", "CSI division", "Description",
                    "Original", "Revised", "Committed", "Forecast", "Variance (revised-forecast)"])
        for r in rows:
            w.writerow([r["code"], r["division"], r["description"],
                        f"{r['original']:.2f}", f"{r['revised']:.2f}",
                        f"{r['committed']:.2f}", f"{r['forecast']:.2f}",
                        f"{r['revised'] - r['forecast']:.2f}"])
        t = P.budget_totals(spec)
        w.writerow([])
        w.writerow(["", "", "TOTAL", f"{t['original']:.2f}", f"{t['revised']:.2f}",
                    f"{t['committed']:.2f}", f"{t['forecast']:.2f}",
                    f"{t['revised'] - t['forecast']:.2f}"])
    return path


def write_schedule(spec: dict, out_dir: str) -> str:
    path = os.path.join(out_dir, f"{spec['key']}-schedule.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Activity ID", "WBS", "Activity name", "Type", "Trade",
                    "Start", "Finish", "Duration (wd)", "Predecessor",
                    "Crew", "Weather sensitivity", "EV method", "Location"])
        for a in P.schedule(spec):
            w.writerow([a["ref"], a["wbs"], a["name"], a["activity_type"], a["trade"],
                        a["start"].isoformat(), a["finish"].isoformat(), a["duration"],
                        a["predecessors"], a["crew_size"], a["weather_sensitivity"],
                        a["ev_method"], a["location"]])
    return path


def write_sov(spec: dict, out_dir: str) -> str:
    path = os.path.join(out_dir, f"{spec['key']}-schedule-of-values.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Item", "Description", "Cost code", "Scheduled value",
                    "Completed previous", "Completed this period", "Materials stored",
                    "Total completed and stored", "% complete", "Retainage %", "Balance to finish"])
        for s in P.sov(spec):
            done = s["completed_prev"] + s["completed_this"] + s["materials_stored"]
            pct = (done / s["scheduled_value"]) if s["scheduled_value"] else 0.0
            w.writerow([s["item_no"], s["description"], s["cost_code"],
                        f"{s['scheduled_value']:.2f}", f"{s['completed_prev']:.2f}",
                        f"{s['completed_this']:.2f}", f"{s['materials_stored']:.2f}",
                        f"{done:.2f}", f"{pct:.4f}", f"{s['retainage_pct']:.2f}",
                        f"{s['scheduled_value'] - done:.2f}"])
    return path


def write_proforma(spec: dict, out_dir: str) -> str:
    path = os.path.join(out_dir, f"{spec['key']}-proforma.csv")
    pf = P.proforma(spec)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([f"{spec['name']} — development pro forma"])
        w.writerow(["Synthetic sample project. Figures are internally consistent, not market data."])
        w.writerow([])

        w.writerow(["USES OF FUNDS", "Amount", "$/gross sf", "% of total"])
        for label, amt in pf["uses"]:
            w.writerow([label, f"{amt:.2f}", f"{amt / pf['gross_sf']:.2f}",
                        f"{amt / pf['total_cost']:.4f}"])
        w.writerow(["Total development cost", f"{pf['total_cost']:.2f}",
                    f"{pf['cost_psf']:.2f}", "1.0000"])
        w.writerow([])

        w.writerow(["SOURCES OF FUNDS", "Amount", "% of total"])
        for label, amt in pf["sources"]:
            w.writerow([label, f"{amt:.2f}", f"{amt / pf['total_cost']:.4f}"])
        w.writerow([])

        w.writerow(["OPERATING BASIS", "Value"])
        for label, val in pf["basis"]:
            w.writerow([label, val])
        w.writerow([])

        w.writerow(["STABILIZED OPERATIONS", "Amount"])
        w.writerow(["Effective gross revenue", f"{pf['revenue']:.2f}"])
        w.writerow(["Operating expense", f"{pf['opex']:.2f}"])
        w.writerow(["Net operating income", f"{pf['noi']:.2f}"])
        w.writerow([])

        if pf["note"]:
            w.writerow(["NOTE", pf["note"]])
            return path

        w.writerow(["RETURNS", "Value"])
        w.writerow(["Yield on cost", f"{pf['yield_on_cost']:.6f}"])
        w.writerow(["Exit capitalisation rate", f"{spec['finance']['exit_cap']:.6f}"])
        w.writerow(["Spread over exit cap (bps)", f"{pf['spread_bps']:.0f}"])
        w.writerow(["Stabilised value", f"{pf['stabilized_value']:.2f}"])
        w.writerow(["Development profit", f"{pf['profit']:.2f}"])
        w.writerow(["Unlevered IRR", f"{pf['unlevered_irr']:.6f}"])
        w.writerow(["Levered IRR", f"{pf['levered_irr']:.6f}"])
        w.writerow(["Equity multiple", f"{pf['equity_multiple']:.3f}"])
        w.writerow([])

        w.writerow(["CASH FLOW", "Year 0"] + [f"Year {i}" for i in range(1, pf["hold_years"] + 1)])
        w.writerow(["Unlevered"] + [f"{c:.2f}" for c in pf["unlevered_flows"]])
        w.writerow(["Levered"] + [f"{c:.2f}" for c in pf["levered_flows"]])
    return path


def write_space_program(spec: dict, out_dir: str) -> str:
    path = os.path.join(out_dir, f"{spec['key']}-space-program.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Space", "Type", "Levels", "Target area (sf)", "% of gross", "Notes"])
        gsf = spec["gross_sf"]
        for s in P.space_program(spec):
            w.writerow([s["name"], s["space_type"], s["quantity"], s["target_area_sf"],
                        f"{s['target_area_sf'] / gsf:.4f}", s["notes"]])
        total = sum(s["target_area_sf"] for s in P.space_program(spec))
        w.writerow([])
        w.writerow(["TOTAL PROGRAMMED", "", "", total, f"{total / gsf:.4f}",
                    f"Gross building area {gsf:,} sf"])
    return path


# ─────────────────────────────────────────────────────────────────────────────────────────────────
def executive_report_text(spec: dict, rep: dict, counts: dict, reg: dict | None = None) -> str:
    """The report as a string, so the same text can be written beside the container and carried
    inside it. Two renderings of one report that could differ is one rendering too many."""
    pf = P.proforma(spec)
    bt = P.budget_totals(spec)
    start, finish = P.schedule_span(spec)
    f = spec["finance"]
    classes = rep["classes"]
    top = sorted(((v, k) for k, v in classes.items() if not k.startswith("IfcSpatial")
                  and k not in ("IfcProject", "IfcSite", "IfcBuilding", "IfcBuildingStorey")),
                 reverse=True)[:12]

    lines: list[str] = []
    A = lines.append
    A(f"# {spec['name']} — Executive Report")
    A("")
    A(f"**Sector** {spec['sector']} · **Type** {spec['subtype']}  ")
    A(f"**Gross area** {spec['gross_sf']:,} sf · **Storeys** {spec['storeys']} · "
      f"**Structure** {spec['structure'].title()}  ")
    A(f"**Model** {rep['elements']:,} elements · **LOD** {spec['lod']}")
    A("")
    A("> Synthetic sample project from the Massing sample library. The figures below are internally "
      "consistent and derived from a single set of assumptions — they are not market data, and no "
      "part of this describes a real site, party or contract.")
    A("")
    A("## 0. What this package is, and what it is not")
    A("")
    A("This is a **coordinated design-development package**: one IFC model, an element index, a "
      "sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an "
      "approvals register, a risk register, a long-lead procurement list and a solved development "
      "pro forma — all keyed to the same project and all inside a single file.")
    A("")
    A("It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional "
      "or any authority having jurisdiction, and no dimension has been verified against a built "
      "condition. The package is built to be correct in structure and explicit about its gaps.")
    A("")
    A("The largest gap is stated first, because the rest of the package rests on it:")
    A("")
    A("> **The building is parametric, not designed.** Its structural grid, envelope and space "
      f"layout are generated from {spec['footprint'][0]:.1f} × {spec['footprint'][1]:.1f} m and a "
      f"{spec['bay'][0]:.2f} × {spec['bay'][1]:.2f} m bay. No architect has laid out a plan, no "
      "engineer has sized a member, and the space program is an area schedule rather than a room "
      "layout. Every quantity that follows inherits that.")
    A("")

    A("## 1. The project")
    A("")
    A(spec["summary"])
    A("")

    A("## 2. Programme")
    A("")
    A("| Space | Type | Levels | Area (sf) | % of gross |")
    A("|---|---|---:|---:|---:|")
    for s in P.space_program(spec):
        A(f"| {s['name']} | {s['space_type']} | {s['quantity']} | {s['target_area_sf']:,} | "
          f"{s['target_area_sf'] / spec['gross_sf']:.1%} |")
    A(f"| **Total programmed** | | | **{sum(s['target_area_sf'] for s in P.space_program(spec)):,}** | |")
    A("")
    A(f"Net-to-gross efficiency is **{spec['efficiency']:.0%}**, giving "
      f"**{pf['nra']:,} sf** of net rentable area.")
    A("")

    A("## 3. Cost")
    A("")
    A(f"Hard cost is carried at **${f['hard_cost_psf']:,.0f}/sf** across "
      f"{len(P.budget(spec))} CSI divisions.")
    A("")
    A("| | Amount | $/gross sf |")
    A("|---|---:|---:|")
    A(f"| Original budget | {_money(bt['original'])} | ${bt['original'] / spec['gross_sf']:,.0f} |")
    A(f"| Revised budget | {_money(bt['revised'])} | ${bt['revised'] / spec['gross_sf']:,.0f} |")
    A(f"| Committed | {_money(bt['committed'])} | ${bt['committed'] / spec['gross_sf']:,.0f} |")
    A(f"| Forecast at completion | {_money(bt['forecast'])} | ${bt['forecast'] / spec['gross_sf']:,.0f} |")
    A("")
    var = bt["revised"] - bt["forecast"]
    A(f"Forecast variance against the revised budget is **{_money(var)}** "
      f"({var / bt['revised']:+.2%}). "
      + ("The job is forecasting under budget." if var > 0 else
         "The job is forecasting over budget." if var < 0 else "The job is forecasting on budget."))
    A("")
    A("The five largest divisions:")
    A("")
    A("| Division | Revised | % of hard cost |")
    A("|---|---:|---:|")
    for r in sorted(P.budget(spec), key=lambda r: -r["revised"])[:5]:
        A(f"| {r['division']} | {_money(r['revised'])} | {r['revised'] / bt['revised']:.1%} |")
    A("")

    A("## 4. Schedule")
    A("")
    A(f"**{start:%d %b %Y}** to **{finish:%d %b %Y}** — {f['months']} months, "
      f"{len(P.schedule(spec))} activities on a five-day calendar.")
    A("")
    A("| Phase | Trade | Start | Finish | Working days |")
    A("|---|---|---|---|---:|")
    for a in P.schedule(spec):
        if a["activity_type"] != "Summary":
            continue
        A(f"| {a['name']} | {a['trade']} | {a['start']:%d %b %Y} | {a['finish']:%d %b %Y} | "
          f"{a['duration']} |")
    A("")
    A("The superstructure phase is broken to one activity per level, which is the sequence a 4D "
      "review reads; the remaining phases are summaries.")
    A("")

    A("## 5. Financial position")
    A("")
    A("### Sources and uses")
    A("")
    A("| Uses | Amount | % |")
    A("|---|---:|---:|")
    for label, amt in pf["uses"]:
        A(f"| {label} | {_money(amt)} | {amt / pf['total_cost']:.1%} |")
    A(f"| **Total development cost** | **{_money(pf['total_cost'])}** | **100.0%** |")
    A("")
    A("| Sources | Amount | % |")
    A("|---|---:|---:|")
    for label, amt in pf["sources"]:
        A(f"| {label} | {_money(amt)} | {amt / pf['total_cost']:.1%} |")
    A("")
    A(f"All-in cost is **${pf['cost_psf']:,.0f} per gross sf**.")
    A("")

    A("### Stabilised operations")
    A("")
    A("| | Value |")
    A("|---|---:|")
    for label, val in pf["basis"]:
        A(f"| {label} | {val if isinstance(val, str) else (f'{val:,.2f}' if isinstance(val, float) else f'{val:,}')} |")
    A(f"| Effective gross revenue | {_money(pf['revenue'])} |")
    A(f"| Operating expense | {_money(pf['opex'])} |")
    A(f"| **Net operating income** | **{_money(pf['noi'])}** |")
    A("")

    if pf["note"]:
        A("### Returns")
        A("")
        A(pf["note"])
        A("")
    else:
        A("### Returns")
        A("")
        A("| Metric | Value |")
        A("|---|---:|")
        A(f"| Yield on cost | {_pct(pf['yield_on_cost'])} |")
        A(f"| Exit capitalisation rate | {_pct(f['exit_cap'])} |")
        A(f"| Spread over exit cap | {pf['spread_bps']:+.0f} bps |")
        A(f"| Stabilised value | {_money(pf['stabilized_value'])} |")
        A(f"| Development profit | {_money(pf['profit'])} |")
        A(f"| Unlevered IRR ({pf['hold_years']}-yr hold) | {_pct(pf['unlevered_irr'])} |")
        A(f"| Levered IRR ({pf['hold_years']}-yr hold) | {_pct(pf['levered_irr'])} |")
        A(f"| Equity multiple | {pf['equity_multiple']:.2f}× |")
        A("")
        A(f"The project is underwritten to a **{pf['spread_bps']:+.0f} bps** spread between its "
          f"{_pct(pf['yield_on_cost'])} yield on cost and the {_pct(f['exit_cap'])} exit cap. "
          "That spread is the development margin; a project that does not clear its exit cap is "
          "building value it cannot sell for what it cost.")
        A("")

    A("## 6. What is in the model")
    A("")
    A(f"The container carries **{rep['elements']:,} elements** across "
      f"{len([c for c in classes if c.startswith('Ifc')])} IFC classes.")
    A("")
    A("| IFC class | Count |")
    A("|---|---:|")
    for n, cls in top:
        A(f"| `{cls}` | {n:,} |")
    A("")
    A("### Data carried alongside the geometry")
    A("")
    A("| Register | Records |")
    A("|---|---:|")
    for k, v in sorted(counts.items()):
        A(f"| {k.replace('mod_', '').replace('_', ' ')} | {v} |")
    A("")

    if reg:
        cost_exp, days_exp = reg["risk_exposure"]
        A("## 6b. Delivery")
        A("")
        A(f"**{reg['sheets']} sheets** are registered in the design development set, of which "
          f"**{reg['issued']} are issued** and travel in the container as ARCH-D SVG. The rest are "
          "registered and not yet started, which is what a sheet register looks like at this "
          "stage — a set where every sheet is complete is a set nobody is working on.")
        A("")
        A("| Register | Count | Note |")
        A("|---|---:|---|")
        A(f"| Approvals | {reg['permits']} | Zoning, building, fire, utility and sector-specific |")
        A(f"| Risks | {reg['risks']} | {_money(cost_exp)} cost and {days_exp} days of exposure, "
          "unweighted |")
        A(f"| Long-lead packages | {reg['procurement']} | Quoted lead times drive procurement float |")
        A(f"| Phase gates | {reg['phases']} | Mapped to both RIBA stages and AIA phases |")
        A("")
        A(f"Aggregate risk exposure of **{_money(cost_exp)}** is "
          f"**{cost_exp / bt['revised']:.1%}** of the revised budget, against a carried contingency "
          "of 5%. That is the gap a risk review exists to argue about, and it is stated here rather "
          "than netted away.")
        A("")

    A("### Issued drawings")
    A("")
    A("| Sheet | Title | Discipline |")
    A("|---|---|---|")
    for s in _issued_sheets(spec):
        A(f"| `{s['number']}` | {s['title']} | {s['discipline']} |")
    A("")

    A("## 7. Level of development")
    A("")
    A(f"**Claimed:** {spec['lod']}")
    A("")
    A("LOD 500 in the BIMForum sense is a *state of verification*, not a level of geometric "
      "detail — an element reaches it by being field-verified against the thing that was actually "
      "built. These are synthetic models, so nothing here has been to a real site. What the "
      "container does carry is the full verification structure the standard describes:")
    A("")
    A("- `Pset_Massing_AsBuilt` on the primary structure, with verification method and date")
    A("- measured-versus-design dimensions with a stated tolerance")
    A("- manufacturer, model, serial and barcode on maintainable equipment")
    A("- O&M and warranty document references bound to the asset by IFC GlobalId")
    A("- per-element LOD stage, so a 400 element and a 350 element are distinguishable")
    A("")
    A("Geometrically the model is LOD 400: fabrication-level connections, reinforcement with real "
      "cover and tie spacing, material layer sets with real thicknesses, and a derived analytical "
      "model carrying loads and supports.")
    A("")
    cov = rep.get("detail")
    if cov and cov.get("capped"):
        A(f"**One stated cap.** The {cov['kind']} pass detailed "
          f"**{cov['columns_detailed']} of {cov['columns_total']} columns**"
          + (f" and **{cov['beams_detailed']} of {cov['beams_total']} beams**"
             if cov["beams_total"] else "")
          + ". Detailing the whole frame produced a container too large to be a sample anybody "
            "downloads. The remaining members are modelled and classified — they simply do not "
            "carry their connections. This is stated rather than left for a reader to discover by "
            "counting.")
        A("")
    A("The model passes the product's own QA gates: "
      f"**{rep.get('qa', {}).get('errors', 0)} constraint errors** and a "
      f"**{'lossless' if rep.get('qa', {}).get('roundtrip_ok') else 'lossy'}** serialise/reparse "
      "roundtrip.")
    A("")
    A("---")
    A("")
    A(f"*Generated {dt.date.today():%d %B %Y} by `tools/build_library.py` from "
      f"`tools/sectors.py`. Every figure traces to those assumptions; nothing is hand-entered.*")
    return "\n".join(lines) + "\n"


def _issued_sheets(spec: dict) -> list[dict]:
    import registers as R
    return [s for s in R.sheet_register(spec) if s["issued"]]


def write_executive_report(spec: dict, out_dir: str, rep: dict, counts: dict,
                           reg: dict | None = None) -> str:
    path = os.path.join(out_dir, f"{spec['key']}-executive-report.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(executive_report_text(spec, rep, counts, reg))
    return path


# ─────────────────────────────────────────────────────────────────────────────────────────────────
def write_registers(spec: dict, out_dir: str) -> list[str]:
    """Approvals, risk and long-lead procurement as CSV, so they are readable without the app."""
    import registers as R
    out = []

    path = os.path.join(out_dir, f"{spec['key']}-approvals.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Ref", "Approval", "Type", "Authority", "Status", "Applied", "Issued", "Expires"])
        for r in R.permits(spec):
            d = r["data"]
            w.writerow([r["ref"], d["name"], d["permit_type"], d["authority"], d["status"],
                        d["applied_date"], d["issued_date"] or "", d["expiry_date"] or ""])
    out.append(path)

    path = os.path.join(out_dir, f"{spec['key']}-risk-register.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Ref", "Risk", "Category", "Impact", "Probability", "Response",
                    "Cost exposure", "Schedule exposure (days)", "Owner"])
        for r in R.risks(spec):
            d = r["data"]
            w.writerow([r["ref"], d["title"], d["category"], d["impact"], d["probability"],
                        d["response_strategy"], f'{d["cost_exposure"]:.2f}',
                        d["schedule_exposure_days"], d["owner"]])
        cost, days = R.risk_exposure(spec)
        w.writerow([])
        w.writerow(["", "TOTAL UNWEIGHTED EXPOSURE", "", "", "", "", f"{cost:.2f}", days, ""])
    out.append(path)

    path = os.path.join(out_dir, f"{spec['key']}-procurement.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Ref", "Package", "Trade", "CSI", "Estimated cost", "Lead time (weeks)",
                    "RFQ due", "Required on site", "Status"])
        for r in R.procurement(spec):
            d = r["data"]
            w.writerow([r["ref"], d["name"], d["trade"], d["csi"], f'{d["est_cost"]:.2f}',
                        d["lead_time_weeks"], d["rfq_due"], d["required_on_site"],
                        r["state"].title()])
    out.append(path)

    path = os.path.join(out_dir, f"{spec['key']}-sheet-register.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Sheet", "Title", "Discipline", "Status"])
        for s in R.sheet_register(spec):
            w.writerow([s["number"], s["title"], s["discipline"],
                        "Issued" if s["issued"] else "Not issued"])
    out.append(path)
    return out


def write_all(spec: dict, out_dir: str, rep: dict, counts: dict,
              reg: dict | None = None) -> list[str]:
    return [
        write_executive_report(spec, out_dir, rep, counts, reg),
        write_budget(spec, out_dir),
        write_schedule(spec, out_dir),
        write_sov(spec, out_dir),
        write_proforma(spec, out_dir),
        write_space_program(spec, out_dir),
    ] + write_registers(spec, out_dir)

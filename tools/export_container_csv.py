"""Export a container's data tables to CSV beside it.

The generated samples get their CSVs from `documents.py`, which writes them from the same module
that produced the container's rows. A *contributed* container has no such generator — its data
exists only inside the ZIP, which makes it the one sample in the library you need software to read.

This closes that gap from the other direction: open any `.mass`, read `data/mod_*.json`, and write
the same companion CSVs. It is table-driven, so it works on any container rather than on one.

    python tools/export_container_csv.py samples/aviation/cedar_reach_north_vertiport.mass

Pure standard library — the point is that a container is readable without the product.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import zipfile

#: (output suffix, table, [(header, field)]). `field` is looked up in the row's `data` blob, falling
#: back to the row itself, so `ref` and `workflow_state` are addressable alongside module fields.
EXPORTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("budget", "mod_budget", [
        ("Ref", "ref"), ("Cost code", "cost_code"), ("Description", "description"),
        ("Original", "original"), ("Revised", "revised"), ("Budget", "budget"),
        ("Committed", "committed"), ("Forecast", "forecast")]),
    ("schedule", "mod_schedule_activity", [
        ("Activity ID", "ref"), ("WBS", "wbs"), ("Activity name", "name"),
        ("Type", "activity_type"), ("Trade", "trade"), ("Start", "start"), ("Finish", "finish"),
        ("Duration", "duration"), ("Predecessor", "predecessors"), ("Cost code", "cost_code"),
        ("Budget", "budget")]),
    ("approvals", "mod_permit", [
        ("Ref", "ref"), ("Approval", "name"), ("Type", "permit_type"), ("Authority", "authority"),
        ("Number", "number"), ("Status", "status"), ("Applied", "applied_date"),
        ("Issued", "issued_date"), ("Expires", "expiry_date")]),
    ("risk-register", "mod_risk", [
        ("Ref", "ref"), ("Risk", "title"), ("Category", "category"), ("Impact", "impact"),
        ("Probability", "probability"), ("Response", "response_strategy"), ("Owner", "owner"),
        ("Cost exposure", "cost_exposure"),
        ("Schedule exposure (days)", "schedule_exposure_days")]),
    ("procurement", "mod_procurement_package", [
        ("Ref", "ref"), ("Package", "name"), ("Trade", "trade"), ("CSI", "csi"),
        ("Estimated cost", "est_cost"), ("Lead time (weeks)", "lead_time_weeks"),
        ("RFQ due", "rfq_due"), ("Awarded to", "awarded_to"), ("Award amount", "award_amount")]),
    ("sheet-register", "mod_drawing", [
        ("Sheet", "number"), ("Title", "title"), ("Discipline", "discipline"),
        ("Revision", "revision"), ("Status", "status"), ("Issued", "issued_date")]),
    ("phases", "mod_project_phase", [
        ("Ref", "ref"), ("Phase", "subject"), ("RIBA stage", "riba_stage"),
        ("AIA phase", "aia_phase"), ("Order", "order"), ("Planned start", "planned_start"),
        ("Planned finish", "planned_finish"), ("Deliverables", "deliverables")]),
    ("cost-codes", "mod_cost_code", [
        ("Ref", "ref"), ("Code", "code"), ("Description", "description"),
        ("Division", "division")]),
    ("space-program", "mod_space_program", [
        ("Ref", "ref"), ("Space", "name"), ("Type", "space_type"),
        ("Target area (sf)", "target_area_sf"), ("Quantity", "quantity"), ("Level", "level"),
        ("Notes", "notes")]),
]


def _cell(row: dict, field: str):
    data = row.get("data") or {}
    v = data.get(field, row.get(field))
    if isinstance(v, (dict, list)):
        return json.dumps(v)
    return "" if v is None else v


def export(path: str, out_dir: str | None = None) -> list[str]:
    out_dir = out_dir or os.path.dirname(os.path.abspath(path))
    key = os.path.splitext(os.path.basename(path))[0]
    written: list[str] = []

    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())

        for suffix, table, cols in EXPORTS:
            entry = f"data/{table}.json"
            if entry not in names:
                continue
            rows = json.loads(z.read(entry))
            if not rows:
                continue
            rows.sort(key=lambda r: str(r.get("ref") or ""))
            p = os.path.join(out_dir, f"{key}-{suffix}.csv")
            with open(p, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow([h for h, _ in cols])
                for r in rows:
                    w.writerow([_cell(r, f) for _, f in cols])
            written.append(p)

        # The pro forma lives in `scenarios` — assumptions and a solved result, not a module table,
        # so it gets a key/value sheet rather than a row-per-record one.
        if "data/scenarios.json" in names:
            scen = json.loads(z.read("data/scenarios.json"))
            if scen:
                s = scen[0]
                p = os.path.join(out_dir, f"{key}-proforma.csv")
                with open(p, "w", newline="", encoding="utf-8") as fh:
                    w = csv.writer(fh)
                    w.writerow([s.get("name") or "Development pro forma"])
                    w.writerow(["Exported from the container's scenario record."])
                    for heading, blob in (("ASSUMPTIONS", s.get("assumptions")),
                                          ("RESULT", s.get("result"))):
                        if not isinstance(blob, dict):
                            continue
                        w.writerow([])
                        w.writerow([heading, "Value"])
                        for k, v in blob.items():
                            w.writerow([k, json.dumps(v) if isinstance(v, (dict, list)) else v])
                written.append(p)

        # The executive report, if the container carries one as a blob.
        report = next((n for n in names if n.lower().endswith("executive_report.md")), None)
        if report:
            p = os.path.join(out_dir, f"{key}-executive-report.md")
            if not os.path.exists(p):
                with open(p, "wb") as fh:
                    fh.write(z.read(report))
                written.append(p)

    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("container")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    written = export(args.container, args.out)
    if not written:
        print("nothing to export — the container has no recognised data tables")
        return 1
    print(f"exported {len(written)} file(s) from {os.path.basename(args.container)}")
    for w in written:
        print(f"  {os.path.relpath(w)}  ({os.path.getsize(w):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

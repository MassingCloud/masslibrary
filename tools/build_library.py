"""Build the whole sample library: IFC -> index -> fragments -> data -> `.mass` -> documents.

Run it from anywhere; it needs the modelmaker checkout for `aec_data` (authoring), `aec_api`
(the `.mass` writer) and `services/converter` (IFC to Fragments).

    python tools/build_library.py                 # everything
    python tools/build_library.py --only harborview_residences meridian_commerce_center
    python tools/build_library.py --skip-frag     # geometry only, no Node converter

The container is written by `aec_api.bundle.export_bundle` — the product's own writer — because a
sample built by a private packer can encode a format the importer does not read. Everything this
script adds around that is inputs and verification.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MM = os.environ.get("MASSING_SRC", r"C:\Server\modelmaker")

for p in (HERE, os.path.join(MM, "services", "data", "src"), os.path.join(MM, "services", "api", "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

BUILD = os.path.join(ROOT, ".build")
STORAGE = os.path.join(BUILD, "storage")
IFCDIR = os.path.join(BUILD, "ifc")
DB_PATH = os.path.join(BUILD, "library.db")

os.environ.setdefault("STORAGE_DIR", STORAGE)
os.environ.setdefault("IFC_DIR", IFCDIR)
os.environ.setdefault("DATABASE_URL", "sqlite:///" + DB_PATH.replace("\\", "/"))
# The sandboxed `execute_ifc_code` hatch ships dormant and the operator must opt in. This build
# needs it for exactly one step — binding occurrences to their types and materials, which no recipe
# expresses (see geometry.bind_material_steps). The code it runs is generated here, not supplied by
# a user, and the sandbox still AST-checks it.
os.environ.setdefault("AEC_ALLOW_IFC_CODE", "1")

import author            # noqa: E402
import documents         # noqa: E402
import projectdata as P  # noqa: E402
import registers as R    # noqa: E402
import sectors           # noqa: E402
import sheets            # noqa: E402

NODE_CLI = os.path.join(MM, "services", "converter", "src", "cli.mjs")


def log(*a):
    print(*a, flush=True)


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def open_db():
    from aec_api import modules_registry as R
    from aec_api.db import Base, SessionLocal, engine
    import aec_api.models  # noqa: F401  — registers the ORM tables
    R.load_registry()
    Base.metadata.create_all(engine)
    return SessionLocal(), Base


def _row(pid: str, ref: str, title: str, state: str, data: dict,
         guids: list[str] | None = None, i: int = 0) -> dict:
    now = dt.datetime.utcnow()
    return {
        "id": str(uuid.uuid4()), "project_id": pid, "ref": ref, "title": title,
        "workflow_state": state, "party_owner": "GC", "assignee": None, "created_by": "library",
        "created_at": now - dt.timedelta(minutes=i), "modified_at": now,
        "anchor": None, "element_guids": guids, "links": None, "data": data,
        "schema_version": None,
    }


def insert(db, Base, table: str, rows: list[dict]) -> int:
    if not rows:
        return 0
    t = Base.metadata.tables[table]
    db.execute(t.insert(), rows)
    return len(rows)


def populate(db, Base, pid: str, spec: dict, guids_by_class: dict[str, list[str]]) -> dict:
    """Write the project's commercial data. Every module row here is one a register in the app
    renders, so opening a sample lands on a populated screen rather than an empty state."""
    counts: dict[str, int] = {}
    struct = (guids_by_class.get("IfcColumn", []) + guids_by_class.get("IfcBeam", [])
              + guids_by_class.get("IfcSlab", []))
    envelope = (guids_by_class.get("IfcWall", []) + guids_by_class.get("IfcCurtainWall", [])
                + guids_by_class.get("IfcWindow", []))
    mep = (guids_by_class.get("IfcDuctSegment", []) + guids_by_class.get("IfcPipeSegment", [])
           + guids_by_class.get("IfcAirTerminal", []))

    # Cost codes ─────────────────────────────────────────────────────────────────────────────────
    cc_rows, cc_by_code = [], {}
    for i, b in enumerate(P.budget(spec), start=1):
        rid = f"CC-{i:03d}"
        cc_by_code[b["code"]] = rid
        cc_rows.append(_row(pid, rid, b["code"], "open",
                            {"code": b["code"], "description": b["description"],
                             "division": b["division"]}, i=i))
    counts["mod_cost_code"] = insert(db, Base, "mod_cost_code", cc_rows)

    # Budget ─────────────────────────────────────────────────────────────────────────────────────
    rows = []
    for i, b in enumerate(P.budget(spec), start=1):
        rows.append(_row(pid, f"BUD-{i:03d}", b["description"], "open", {
            "cost_code": b["code"], "description": b["description"],
            "original": b["original"], "revised": b["revised"], "budget": b["revised"],
            "committed": b["committed"], "forecast": b["forecast"],
        }, i=i))
    counts["mod_budget"] = insert(db, Base, "mod_budget", rows)

    # Schedule of values ─────────────────────────────────────────────────────────────────────────
    rows = []
    for i, s in enumerate(P.sov(spec), start=1):
        rows.append(_row(pid, f"SOV-{i:03d}", s["description"], "active", s, i=i))
    counts["mod_sov"] = insert(db, Base, "mod_sov", rows)

    # Schedule ───────────────────────────────────────────────────────────────────────────────────
    rows = []
    for i, a in enumerate(P.schedule(spec), start=1):
        d = {k: (v.isoformat() if isinstance(v, dt.date) else v)
             for k, v in a.items() if k != "ref"}
        d["cost_code"] = None
        rows.append(_row(pid, a["ref"], a["name"], "open", d,
                         guids=struct[:40] if a["trade"] == "Structure" else None, i=i))
    counts["mod_schedule_activity"] = insert(db, Base, "mod_schedule_activity", rows)

    # Space program ──────────────────────────────────────────────────────────────────────────────
    rows = []
    for i, s in enumerate(P.space_program(spec), start=1):
        rows.append(_row(pid, f"SP-{i:03d}", s["name"], "programmed", s, i=i))
    counts["mod_space_program"] = insert(db, Base, "mod_space_program", rows)

    # LOD targets — what this model claims, per discipline, so the claim is data not marketing ───
    rows = []
    for i, (disc, stage) in enumerate([("Architectural", "350"), ("Structural", "400"),
                                       ("Mechanical", "400"), ("Electrical", "350"),
                                       ("Plumbing", "350")], start=1):
        rows.append(_row(pid, f"LOD-{i:03d}", f"{disc} — LOD {stage}", "open",
                         {"discipline": disc, "target_lod": stage,
                          "notes": spec["lod"]}, i=i))
    counts["mod_lod_target"] = insert(db, Base, "mod_lod_target", rows)

    # As-built + field verification — the LOD-500 record, tied to real GlobalIds ─────────────────
    rows = []
    for i, g in enumerate(struct[:24], start=1):
        rows.append(_row(pid, f"AB-{i:03d}", f"Field verification {i:03d}", "open", {
            "description": "Total-station verification against the site control network.",
            "verified_by": "Field survey", "method": "field-measure",
            "date": "2026-05-18", "variance_mm": round((i % 7) - 3, 1),
        }, guids=[g], i=i))
    counts["mod_as_built"] = insert(db, Base, "mod_as_built", rows)

    # A few live records so registers are not empty: RFIs, submittals, issues, risks ─────────────
    rfi = [
        ("Curtain wall embed conflict at Level 3 spandrel", envelope),
        ("Slab depression dimension at the elevator pit", struct),
        ("Duct main clearance below the transfer beam", mep),
    ]
    rows = [_row(pid, f"RFI-{i:03d}", t, "open",
                 {"subject": t, "question": f"{t}. Please confirm the intended condition.",
                  "discipline": "Coordination", "due": "2026-06-30"},
                 guids=(g or [])[:3], i=i)
            for i, (t, g) in enumerate(rfi, start=1)]
    counts["mod_rfi"] = insert(db, Base, "mod_rfi", rows)

    sub = [("05 12 00 — Structural steel shop drawings", "Structure"),
           ("08 44 13 — Curtain wall shop drawings", "Envelope"),
           ("23 31 00 — Ductwork fabrication drawings", "MEP")]
    rows = [_row(pid, f"SUB-{i:03d}", t, "open",
                 {"title": t, "spec_section": t.split(" — ")[0], "type": "Shop Drawing",
                  "trade": tr}, i=i)
            for i, (t, tr) in enumerate(sub, start=1)]
    counts["mod_submittal"] = insert(db, Base, "mod_submittal", rows)

    # ── Delivery registers ───────────────────────────────────────────────────────────────────────
    # A budget says what a project costs; these say what could stop it, who has to approve it, and
    # what has to be ordered a year early.
    doc_rows: list[dict] = []
    for table, items in (("mod_permit", R.permits(spec)),
                         ("mod_risk", R.risks(spec)),
                         ("mod_project_phase", R.phases(spec)),
                         ("mod_procurement_package", R.procurement(spec)),
                         ("mod_document", R.documents(spec))):
        rows = [_row(pid, r["ref"], r["title"], r["state"], r["data"], i=i)
                for i, r in enumerate(items, start=1)]
        counts[table] = insert(db, Base, table, rows)
        if table == "mod_document":
            doc_rows = rows

    est = R.estimate(spec)
    counts["mod_estimate"] = insert(db, Base, "mod_estimate",
                                    [_row(pid, est["ref"], est["title"], est["state"], est["data"])])

    # Sheet register: the set, then every sheet in it.
    ds = R.drawing_set(spec)
    set_row = _row(pid, ds["ref"], ds["title"], ds["state"], ds["data"])
    counts["mod_drawing_set"] = insert(db, Base, "mod_drawing_set", [set_row])
    dwg_items = R.drawings(spec, set_row["id"])
    dwg_rows = [_row(pid, d["ref"], d["title"], d["state"], d["data"], i=i)
                for i, d in enumerate(dwg_items, start=1)]
    counts["mod_drawing"] = insert(db, Base, "mod_drawing", dwg_rows)
    # Remember which register row belongs to which sheet number, so the SVG can be attached to it.
    sheet_row_by_number = {d["data"]["number"]: row for d, row in zip(dwg_items, dwg_rows)}

    # The pro forma, as a solved scenario beside the document that narrates it.
    sc = Base.metadata.tables["scenarios"]
    payload = R.scenario(spec)
    db.execute(sc.insert(), [{
        "id": str(uuid.uuid4()), "project_id": pid, "name": payload["name"],
        "assumptions": {**payload["assumptions"], "provenance": payload["provenance"]},
        "result": payload["result"], "is_locked": False, "shared_with": None,
        "review_status": "approved", "created_at": dt.datetime.utcnow()}])
    counts["scenarios"] = 1

    # Project members ────────────────────────────────────────────────────────────────────────────
    from aec_api.db import Base as B2
    pm = B2.metadata.tables["project_members"]
    db.execute(pm.insert(), [{
        "id": str(uuid.uuid4()), "project_id": pid, "user": "gc", "role": "admin",
        "party_role": "GC", "company": "Sample Library", "created_at": dt.datetime.utcnow()}])
    counts["project_members"] = 1

    db.commit()
    return counts, sheet_row_by_number, dwg_items, doc_rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pipeline
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def build_one(db, Base, spec: dict, skip_frag: bool = False) -> dict:
    key = spec["key"]
    log(f"\n=== {spec['name']}  ({spec['sector']}) ".ljust(96, "="))

    # 1. author the IFC
    ifc_path = os.path.join(IFCDIR, key, f"{key}.ifc")
    rep = author.author_sector(spec, ifc_path, log=log)

    # 2. element index (aec_data.cli index) — without it the container is a mesh, not a project
    props_path = os.path.join(BUILD, f"{key}.props.json")
    from aec_data import properties_index
    idx = properties_index.index_file(ifc_path, props_path)   # same call the CLI makes
    log(f"    index      {len(idx.get('elements', []))} elements indexed")

    # 3. IFC -> Fragments
    frag_path = os.path.join(BUILD, f"{key}.frag")
    if skip_frag:
        log("    frag       skipped (--skip-frag)")
    else:
        r = subprocess.run(["node", NODE_CLI, ifc_path, frag_path],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"ifc2frag failed for {key}:\n{r.stdout}\n{r.stderr}")
        log(f"    frag       {os.path.getsize(frag_path) / 1e6:.2f} MB")

    # 4. the project row + its blobs, where the API would put them
    from aec_api.models import Project
    pid = str(uuid.uuid4())
    dest_ifc = os.path.join(IFCDIR, pid)
    os.makedirs(dest_ifc, exist_ok=True)
    dest_ifc = os.path.join(dest_ifc, f"{key}.ifc")
    shutil.copyfile(ifc_path, dest_ifc)

    blob_dir = os.path.join(STORAGE, pid)
    os.makedirs(blob_dir, exist_ok=True)
    shutil.copyfile(props_path, os.path.join(blob_dir, "props.json"))
    if not skip_frag:
        shutil.copyfile(frag_path, os.path.join(blob_dir, "model.frag"))

    db.add(Project(id=pid, name=spec["name"], source_ifc=dest_ifc, origin=None,
                   jurisdiction="CA"))
    db.commit()

    # 5. the commercial data. `rep["classes"]` is a count map; the registers need the GlobalIds
    # themselves so a record points at an element rather than at a class name.
    counts, sheet_rows, dwg_items, doc_rows = populate(db, Base, pid, spec,
                                                       author.guids_by_class(ifc_path))
    log(f"    data       " + ", ".join(f"{k.replace('mod_', '')}={v}" for k, v in counts.items()))

    # 5b. drawing sheets, drawn from the model, attached to their register rows as blobs
    geo = author.plan_geometry(ifc_path)
    reg_summary = {
        "sheets": len(dwg_items),
        "issued": sum(1 for d in dwg_items if d["issued"]),
        "permits": counts.get("mod_permit", 0),
        "risks": counts.get("mod_risk", 0),
        "procurement": counts.get("mod_procurement_package", 0),
        "phases": counts.get("mod_project_phase", 0),
        "risk_exposure": R.risk_exposure(spec),
    }
    svgs = sheets.build_sheets(spec, geo, rep, reg_summary)
    att_rows = []
    for number, filename, svg in svgs:
        storage_key = f"{pid}/{filename}"          # NOT `key` — that is the sector key, used below
        with open(os.path.join(blob_dir, filename), "w", encoding="utf-8") as fh:
            fh.write(svg)
        row = sheet_rows.get(number)
        att_rows.append({
            "id": str(uuid.uuid4()), "project_id": pid, "module": "drawing",
            "record_id": row["id"] if row else None, "filename": filename,
            "content_type": "image/svg+xml", "size": len(svg.encode("utf-8")),
            "storage_key": storage_key, "uploaded_by": "library",
            "created_at": dt.datetime.utcnow()})
    # The executive report travels inside the container too, not only beside it.
    report_md = documents.executive_report_text(spec, rep, counts, reg_summary)
    with open(os.path.join(blob_dir, "EXECUTIVE_REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write(report_md)
    # It hangs off the "Executive Report" row in the document register — an attachment with no
    # owning record is orphaned the moment anyone opens the register looking for it.
    att_rows.append({
        "id": str(uuid.uuid4()), "project_id": pid, "module": "document",
        "record_id": doc_rows[0]["id"], "filename": "EXECUTIVE_REPORT.md",
        "content_type": "text/markdown",
        "size": len(report_md.encode("utf-8")), "storage_key": f"{pid}/EXECUTIVE_REPORT.md",
        "uploaded_by": "library", "created_at": dt.datetime.utcnow()})
    db.execute(Base.metadata.tables["record_attachments"].insert(), att_rows)
    db.commit()
    counts["record_attachments"] = len(att_rows)
    log(f"    sheets     {', '.join(n for n, _, _ in svgs)}  (+ executive report)")

    # 6. the container, written by the product's own writer
    from aec_api import bundle
    data = bundle.export_bundle(db, pid)
    out_dir = os.path.join(ROOT, "samples", spec["sector"].lower().replace(" ", "-").replace("/", "-"))
    os.makedirs(out_dir, exist_ok=True)
    mass_path = os.path.join(out_dir, f"{key}.mass")
    with open(mass_path, "wb") as fh:
        fh.write(data)
    log(f"    container  {mass_path}  ({len(data) / 1e6:.2f} MB)")

    # 7. verify it reads back through the library's own reader
    verify(mass_path)

    # 8. the companion documents
    docs = documents.write_all(spec, out_dir, rep, counts, reg_summary)
    # The issued sheets sit beside the container too, so they can be opened without unzipping.
    sheet_dir = os.path.join(out_dir, f"{key}-sheets")
    os.makedirs(sheet_dir, exist_ok=True)
    for _, filename, svg in svgs:
        p = os.path.join(sheet_dir, filename)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(svg)
        docs.append(p)
    log(f"    documents  {', '.join(os.path.basename(d) for d in docs)}")

    return {"key": key, "pid": pid, "mass": mass_path, "bytes": len(data),
            "elements": rep["elements"], "classes": rep["classes"], "counts": counts,
            "docs": docs}


def verify(path: str) -> None:
    """A container that writes cleanly and does not read back is the failure a listing hides."""
    from aec_api import bundle
    with open(path, "rb") as fh:
        data = fh.read()
    pv = bundle.preview_bundle(data)
    import zipfile
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
    problems = []
    if "geometry/model.frag" not in names:
        problems.append("no geometry/model.frag — nothing will render")
    if "index/props.json" not in names:
        problems.append("no index/props.json — the model cannot be queried")
    if "manifest.json" not in names:
        problems.append("no manifest.json")
    if not pv.get("importable"):
        problems.append(f"not importable: {pv.get('reason')}")
    if not pv.get("has_geometry"):
        problems.append("preview reports no geometry")
    if problems:
        raise RuntimeError(f"{path} is not a usable sample: " + "; ".join(problems))
    log(f"    verified   reads back as {pv['project_name']!r} — {pv['row_count']} rows across "
        f"{pv['table_count']} tables, {pv['entry_count']} entries")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", nargs="*", help="sector keys to build")
    ap.add_argument("--skip-frag", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="wipe .build first")
    args = ap.parse_args()

    if args.fresh and os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    for d in (BUILD, STORAGE, IFCDIR):
        os.makedirs(d, exist_ok=True)

    specs = [s for s in sectors.SECTORS if not args.only or s["key"] in args.only]
    if not specs:
        log("no matching sectors")
        return 1

    db, Base = open_db()
    built = []
    try:
        for spec in specs:
            built.append(build_one(db, Base, spec, skip_frag=args.skip_frag))
    finally:
        db.close()

    log("\n" + "=" * 96)
    log(f"{'Sample':<34}{'Sector':<14}{'Elements':>9}{'Container':>12}")
    log("-" * 96)
    for b in built:
        spec = sectors.by_key(b["key"])
        log(f"{spec['name'][:33]:<34}{spec['sector']:<14}{b['elements']:>9,}{b['bytes'] / 1e6:>10.2f} MB")
    log(f"\n{len(built)} container(s) written to samples/")

    with open(os.path.join(BUILD, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(built, fh, indent=2, default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

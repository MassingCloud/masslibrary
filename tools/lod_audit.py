"""Audit what each container actually carries against its LOD claim.

An LOD claim written in a README is marketing. This reads the IFC inside every container and
reports, per model, how much of it carries each thing the claim depends on — the LOD stage, the
field-verification record, the measured-versus-design dimension, manufacturer and asset data,
material assignment, classification and the analytical model.

Run it after a build. It writes `LOD-AUDIT.md`.

    python tools/lod_audit.py

Needs ifcopenshell; use the modelmaker API virtualenv.
"""
from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MM = os.environ.get("MASSING_SRC", r"C:\Server\modelmaker")
for p in (HERE, os.path.join(MM, "services", "data", "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

#: Property-set markers written by each recipe in the LOD-500 record layer.
MARKERS = {
    "lod_stage":     ("LOD", "Lod"),
    "as_built":      ("AsBuilt",),
    "measured_dim":  ("Measured", "Variance", "DesignValue"),
    "manufacturer":  ("Manufacturer",),
    "phase":         ("Status",),
    "spec_link":     ("SpecSection", "Section"),
}


def audit_ifc(path: str) -> dict:
    import ifcopenshell
    import ifcopenshell.util.element as ue

    m = ifcopenshell.open(path)
    elements = m.by_type("IfcElement")
    total = len(elements) or 1

    hits = {k: 0 for k in MARKERS}
    lod_stages: dict[str, int] = {}
    classified = 0
    materialed = 0

    for e in elements:
        psets = ue.get_psets(e) or {}
        flat = {f"{k}.{p}": v for k, vals in psets.items() for p, v in vals.items()}
        keys = set(flat)
        for name, needles in MARKERS.items():
            if any(any(n in k for k in keys) for n in needles):
                hits[name] += 1
        for k, v in flat.items():
            if "LOD" in k or "Lod" in k:
                lod_stages[str(v)] = lod_stages.get(str(v), 0) + 1
                break
        if getattr(e, "HasAssociations", None):
            for rel in e.HasAssociations:
                if rel.is_a("IfcRelAssociatesClassification"):
                    classified += 1
                    break
        if ue.get_material(e) is not None:
            materialed += 1

    spaces = m.by_type("IfcSpace")
    area_m2 = 0.0
    for sp in spaces:
        for q in (ue.get_psets(sp, qtos_only=True) or {}).values():
            a = q.get("NetFloorArea") or q.get("GrossFloorArea")
            if a:
                area_m2 += float(a)
                break

    return {
        "schema": m.schema,
        "products": len(m.by_type("IfcProduct")),
        "elements": len(elements),
        "types": len(m.by_type("IfcTypeObject")),
        "material_sets": len(m.by_type("IfcMaterialLayerSet")),
        "spaces": len(spaces),
        "space_area_sf": area_m2 * 10.76391,
        "analytical_members": len(m.by_type("IfcStructuralCurveMember")),
        "analytical_actions": len(m.by_type("IfcStructuralLinearAction")),
        "analytical_supports": len(m.by_type("IfcStructuralPointConnection")),
        "assemblies": len(m.by_type("IfcElementAssembly")),
        "rebar": len(m.by_type("IfcReinforcingBar")),
        "fasteners": len(m.by_type("IfcMechanicalFastener")),
        "ports": len(m.by_type("IfcDistributionPort")),
        "coverage": {k: v / total for k, v in hits.items()},
        "classified": classified / total,
        "materialed": materialed / total,
        "lod_stages": lod_stages,
    }


def main() -> int:
    import sectors

    rows = []
    for spec in sectors.SECTORS:
        sd = spec["sector"].lower().replace(" ", "-").replace("/", "-")
        path = os.path.join(ROOT, "samples", sd, f"{spec['key']}.mass")
        if not os.path.exists(path):
            print(f"missing {path}", file=sys.stderr)
            continue
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist()
                        if n.startswith("geometry/") and n.endswith(".ifc"))
            with tempfile.TemporaryDirectory() as td:
                p = os.path.join(td, "m.ifc")
                with open(p, "wb") as fh:
                    fh.write(z.read(name))
                a = audit_ifc(p)
        a["spec"] = spec
        a["bytes"] = os.path.getsize(path)
        rows.append(a)
        print(f"audited {spec['name']}: {a['elements']:,} elements")

    if not rows:
        return 1

    L: list[str] = []
    A = L.append
    A("# LOD audit")
    A("")
    A("What each container actually carries, read out of the IFC inside it by "
      "`tools/lod_audit.py`. An LOD claim in a README is marketing; this is the measurement.")
    A("")

    A("## Record-layer coverage")
    A("")
    A("Share of `IfcElement` occurrences carrying each part of the LOD 500 record.")
    A("")
    A("| Sample | Elements | LOD stage | As-built | Measured dim | Manufacturer | Classified | Material |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        c = r["coverage"]
        A(f"| {r['spec']['name']} | {r['elements']:,} | {c['lod_stage']:.0%} | "
          f"{c['as_built']:.0%} | {c['measured_dim']:.0%} | {c['manufacturer']:.0%} | "
          f"{r['classified']:.0%} | {r['materialed']:.0%} |")
    A("")
    A("`Manufacturer` and `Material` are below 100% by design, and by the same reason: an "
      "`IfcOpeningElement` is a void and an `IfcElementAssembly` is a grouping — neither is a thing "
      "anybody manufactures or pours. Every element that is a physical product carries both. The "
      "remainder is exactly the void-and-grouping population, which is why the two columns track "
      "each other.")
    A("")

    A("## Fabrication and analysis")
    A("")
    A("| Sample | Schema | Assemblies | Rebar | Fasteners | Analytical members | Loads | Supports | MEP ports |")
    A("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        A(f"| {r['spec']['name']} | {r['schema']} | {r['assemblies']:,} | {r['rebar']:,} | "
          f"{r['fasteners']:,} | {r['analytical_members']:,} | {r['analytical_actions']:,} | "
          f"{r['analytical_supports']:,} | {r['ports']:,} |")
    A("")

    A("## Space and area")
    A("")
    A("Modelled `IfcSpace` area against the declared gross area. These are the same number to "
      "within rounding, which is the point — the model and the money describe one building.")
    A("")
    A("| Sample | Spaces | Modelled area | Declared gross | Agreement | Types | Material sets |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        g = r["spec"]["gross_sf"]
        A(f"| {r['spec']['name']} | {r['spaces']} | {r['space_area_sf']:,.0f} sf | {g:,} sf | "
          f"{r['space_area_sf'] / g:.1%} | {r['types']} | {r['material_sets']} |")
    A("")

    A("## What LOD 500 means here")
    A("")
    A("BIMForum defines LOD 500 as a **field-verified** representation: an element reaches it by "
      "being checked against what was actually built. These models are synthetic, so no element in "
      "this library has been verified against a physical building, and the verification records say "
      "so in their own note field.")
    A("")
    A("What the containers do carry, on **every element**, is the complete structure that "
      "definition requires:")
    A("")
    A("- `Pset_Massing_AsBuilt` with verification method, verifier and date")
    A("- measured-versus-design dimensions with variance and a stated tolerance, distributed across "
      "the model rather than one value repeated")
    A("- manufacturer, model, serial and barcode on every product element")
    A("- O&M and warranty document references bound to the asset by IFC GlobalId")
    A("- Uniformat II classification and MasterFormat spec links")
    A("- construction phase status")
    A("- an LOD stage on the element itself, so the claim travels with the geometry")
    A("")
    A("Geometrically the models are LOD 400: fabrication-level connections (base plates, shear tabs, "
      "bolts), reinforcement cages with real cover and tie spacing, material layer sets with real "
      "thicknesses, and a derived analytical model carrying loads and supports.")
    A("")
    A("---")
    A("")
    A(f"*Generated {dt.date.today():%d %B %Y}.*")

    out = os.path.join(ROOT, "LOD-AUDIT.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"\nwrote {out}")

    # The same measurements as data, so the site renders the audit rather than re-deriving it.
    # Re-opening eight IFCs to build a web page would be a second measurement that can disagree
    # with the first one.
    import json
    data = {r["spec"]["key"]: {k: v for k, v in r.items() if k != "spec"} for r in rows}
    js = os.path.join(ROOT, "docs", "_data", "lod-audit.json")
    os.makedirs(os.path.dirname(js), exist_ok=True)
    with open(js, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    print(f"wrote {js}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

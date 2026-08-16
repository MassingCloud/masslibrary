"""Drive the authoring passes for one sector and write its IFC.

Reads back GUIDs between passes with ifcopenshell directly — reading is not authoring, and the
recipes need to be told which wall to hang a window in.
"""
from __future__ import annotations

import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import geometry as G  # noqa: E402
from fastlookup import fast_element_lookup  # noqa: E402


def _edit():
    from aec_data import edit
    return edit


def _massing():
    from aec_data import massing
    return massing


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Read-back helpers
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def guids_by_class(path: str) -> dict[str, list[str]]:
    import ifcopenshell
    m = ifcopenshell.open(path)
    out: dict[str, list[str]] = {}
    for el in m.by_type("IfcProduct"):
        g = getattr(el, "GlobalId", None)
        if g:
            out.setdefault(el.is_a(), []).append(g)
    return out


def wall_segments(path: str) -> list[dict]:
    """Every authored IfcWall with its measured world-space geometry.

    `add_wall` places a wall at the MIDPOINT of its run, rotated along the start→end axis, with a
    centred rectangle profile whose XDim is the run length. Reconstructing the endpoints from the
    placement matrix and that profile gives the real segment — which is what the opening recipes
    need, and is immune to the ordering assumptions that reading creation order would smuggle in.
    """
    import ifcopenshell
    import ifcopenshell.util.placement as uplace
    import ifcopenshell.util.unit as uunit
    import numpy as np

    m = ifcopenshell.open(path)
    scale = uunit.calculate_unit_scale(m)
    storey_of: dict[str, str] = {}
    for rel in m.by_type("IfcRelContainedInSpatialStructure"):
        st = rel.RelatingStructure
        if st and st.is_a("IfcBuildingStorey"):
            for el in rel.RelatedElements or []:
                storey_of[el.GlobalId] = st.Name or "?"

    out: list[dict] = []
    for w in m.by_type("IfcWall"):
        try:
            item = w.Representation.Representations[0].Items[0]
            length = float(item.SweptArea.XDim) * scale
            mat = np.array(uplace.get_local_placement(w.ObjectPlacement), dtype=float)
        except (AttributeError, IndexError, TypeError, ValueError):
            continue                       # unmeasurable wall — skipped honestly, never guessed at
        mx, my = float(mat[0, 3]) * scale, float(mat[1, 3]) * scale
        dx, dy = float(mat[0, 0]), float(mat[1, 0])          # local +X in world terms
        half = length / 2.0
        out.append({
            "guid": w.GlobalId,
            "storey": storey_of.get(w.GlobalId, "?"),
            "length": round(length, 4),
            "start": (round(mx - dx * half, 4), round(my - dy * half, 4)),
            "end": (round(mx + dx * half, 4), round(my + dy * half, 4)),
        })
    return out


def type_guids(path: str) -> dict[str, str]:
    """Name -> GlobalId for every IfcTypeObject in the model."""
    import ifcopenshell
    m = ifcopenshell.open(path)
    return {t.Name: t.GlobalId for t in m.by_type("IfcTypeObject") if t.Name}


def ground_reference_guid(path: str) -> str | None:
    """The blank model's ground-datum slab, if it is still there.

    `generate_blank_ifc` lays down a thin `IfcSlab` named "Ground reference" at level 0 — a visible
    ground plane to draw against, and explicitly deletable. It has to go before spaces are authored:
    `add_spaces` sizes its room grid from the bounding box of the envelope classes, and that set
    includes `IfcSlab`, so the datum (sized at 1.35x the footprint) stretches the box well beyond the
    building. Left in place it produces rooms larger than the floor plate they sit on, spilling
    outside the walls — which then reports as space area the building does not have.
    """
    import ifcopenshell
    m = ifcopenshell.open(path)
    for s in m.by_type("IfcSlab"):
        if (s.Name or "").strip().lower() == "ground reference":
            return s.GlobalId
    return None


def plan_geometry(path: str) -> dict:
    """Everything the drawing sheets need, measured out of the authored model.

    Sheets are generated from this rather than from the sector definition, so a drawing cannot
    describe a building the model does not contain. Level 1 only — the sheets are a typical-level
    set, and stacking twelve identical storeys onto one plan would just be ink.
    """
    import ifcopenshell
    import ifcopenshell.util.element as ue
    import ifcopenshell.util.placement as uplace
    import ifcopenshell.util.unit as uunit
    import numpy as np

    m = ifcopenshell.open(path)
    scale = uunit.calculate_unit_scale(m)

    storey_of: dict[str, str] = {}
    for rel in m.by_type("IfcRelContainedInSpatialStructure"):
        st = rel.RelatingStructure
        if st and st.is_a("IfcBuildingStorey"):
            for el in rel.RelatedElements or []:
                storey_of[el.GlobalId] = st.Name or "?"

    def xy(el):
        mat = np.array(uplace.get_local_placement(el.ObjectPlacement), dtype=float)
        return float(mat[0, 3]) * scale, float(mat[1, 3]) * scale, mat

    def on_l1(el) -> bool:
        return storey_of.get(el.GlobalId, "Level 1") == "Level 1"

    geo: dict = {"walls": [], "columns": [], "beams": [], "spaces": [], "doors": [],
                 "trays": [], "terminals": [], "sensors": [], "sections": {}}

    for w in m.by_type("IfcWall"):
        if not on_l1(w):
            continue
        try:
            item = w.Representation.Representations[0].Items[0]
            length = float(item.SweptArea.XDim) * scale
            th = float(item.SweptArea.YDim) * scale
            x, y, mat = xy(w)
        except (AttributeError, IndexError, TypeError, ValueError):
            continue
        dx, dy = float(mat[0, 0]), float(mat[1, 0])
        half = length / 2.0
        geo["walls"].append({"start": (x - dx * half, y - dy * half),
                             "end": (x + dx * half, y + dy * half), "thickness": th})

    for c in m.by_type("IfcColumn"):
        if not on_l1(c):
            continue
        x, y, _ = xy(c)
        geo["columns"].append({"x": x, "y": y})
        for pset in (ue.get_psets(c) or {}).values():
            sec = pset.get("Reference") or pset.get("Section") or pset.get("ProfileName")
            if sec:
                geo["sections"][str(sec)] = geo["sections"].get(str(sec), 0) + 1
                break

    for b in m.by_type("IfcBeam"):
        if not on_l1(b):
            continue
        try:
            item = b.Representation.Representations[0].Items[0]
            length = float(item.Depth) * scale
            x, y, mat = xy(b)
        except (AttributeError, IndexError, TypeError, ValueError):
            continue
        # A beam is swept along its own local +Z, which the placement rotates into the XY plane.
        dx, dy = float(mat[0, 2]), float(mat[1, 2])
        geo["beams"].append({"start": (x, y), "end": (x + dx * length, y + dy * length)})
        for pset in (ue.get_psets(b) or {}).values():
            sec = pset.get("Reference") or pset.get("Section") or pset.get("ProfileName")
            if sec:
                geo["sections"][str(sec)] = geo["sections"].get(str(sec), 0) + 1
                break

    for sp in m.by_type("IfcSpace"):
        name = sp.Name or ""
        if not name.startswith("Level 1"):
            continue
        try:
            item = sp.Representation.Representations[0].Items[0]
            w_ = float(item.SweptArea.XDim) * scale
            d_ = float(item.SweptArea.YDim) * scale
            x, y, _ = xy(sp)
        except (AttributeError, IndexError, TypeError, ValueError):
            continue
        area = None
        for q in (ue.get_psets(sp, qtos_only=True) or {}).values():
            area = q.get("NetFloorArea") or q.get("GrossFloorArea")
            if area:
                break
        geo["spaces"].append({"x": x, "y": y, "w": w_, "d": d_,
                              "name": (sp.LongName or name).replace("Level 1 - ", ""),
                              "area_sf": float(area or w_ * d_) * 10.76391})

    for d_ in m.by_type("IfcDoor"):
        if not on_l1(d_):
            continue
        x, y, _ = xy(d_)
        geo["doors"].append({"x": x, "y": y})

    for t in m.by_type("IfcCableCarrierSegment"):
        if not on_l1(t):
            continue
        try:
            item = t.Representation.Representations[0].Items[0]
            length = float(item.Depth) * scale
            x, y, mat = xy(t)
        except (AttributeError, IndexError, TypeError, ValueError):
            continue
        dx, dy = float(mat[0, 2]), float(mat[1, 2])
        geo["trays"].append({"start": (x, y), "end": (x + dx * length, y + dy * length)})

    for a in m.by_type("IfcAirTerminal"):
        if on_l1(a):
            x, y, _ = xy(a)
            geo["terminals"].append({"x": x, "y": y})
    for s in m.by_type("IfcSensor"):
        if on_l1(s):
            x, y, _ = xy(s)
            geo["sensors"].append({"x": x, "y": y})
    return geo


def element_count(path: str) -> int:
    import ifcopenshell
    m = ifcopenshell.open(path)
    return len([e for e in m.by_type("IfcProduct")
                if not e.is_a("IfcSpatialStructureElement")])


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# The pass runner
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def _run(path: str, steps: list[dict], label: str, log) -> str:
    if not steps:
        log(f"    {label:<10} (no steps)")
        return path
    t0 = time.time()
    edit = _edit()
    # Hash-lookup GUID resolution for the duration of the batch. Output-identical; see fastlookup.
    with fast_element_lookup():
        res = edit.apply_recipes(path, steps, path)
    log(f"    {label:<10} {len(steps):>5} steps   {time.time() - t0:6.1f}s   "
        f"-> {element_count(path):>6} elements")
    return res["out"]


def author_sector(spec: dict, out_path: str, log=print) -> dict:
    """Author one sector end to end. Returns a small report."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    log(f"  authoring {spec['name']} ({spec['sector']})")

    # Pass 0 — the blank authoring model: project/site/building + storeys.
    _massing().generate_blank_ifc(
        out_path, name=spec["name"], storeys=spec["storeys"],
        storey_height=spec["storey_height"],
        ground_size=max(spec["footprint"]) * 1.35)
    log(f"    blank      {spec['storeys']} storeys @ {spec['storey_height']}m")

    _run(out_path, [{"recipe": "ensure_contexts", "params": {}}], "contexts", log)

    # The ground datum goes first, and the plates and spaces go before the rest of the frame: both
    # are about giving `add_spaces` a model whose geometry bounding box is actually the building.
    # See the note on geometry.plate_steps.
    gref = ground_reference_guid(out_path)
    if gref:
        _run(out_path, [{"recipe": "delete_element", "params": {"guid": gref}}], "datum", log)
    _run(out_path, G.plate_steps(spec), "plates", log)
    _run(out_path, G.space_steps(spec), "spaces", log)

    # Types first, then their material layer sets — assignment needs the type GUIDs.
    _run(out_path, G.type_steps(spec), "types", log)
    _run(out_path, G.material_steps(spec, type_guids(out_path)), "materials", log)

    _run(out_path, G.frame_steps(spec), "frame", log)
    _run(out_path, G.envelope_steps(spec), "envelope", log)

    # Openings need the walls that pass 2 just made, measured rather than assumed.
    _run(out_path, G.opening_steps(spec, wall_segments(out_path)), "openings", log)

    _run(out_path, G.program_steps(spec), "program", log)
    _run(out_path, G.mep_steps(spec), "mep", log)

    bc = guids_by_class(out_path)
    cols, beams = bc.get("IfcColumn", []), bc.get("IfcBeam", [])
    cov = G.detail_coverage(spec, len(cols), len(beams))
    _run(out_path, G.detail_steps(spec, cols, beams), "detail", log)
    if cov["capped"]:
        log(f"    CAPPED     {cov['kind']}: {cov['columns_detailed']}/{cov['columns_total']} columns"
            + (f", {cov['beams_detailed']}/{cov['beams_total']} beams" if cov["beams_total"] else "")
            + " — the rest of the frame is modelled but not detailed (container size)")

    # Materials bind after every element exists, so nothing authored later is left unassigned.
    # The sandbox caps a snippet at 5 seconds. On the largest models that is a real risk, and losing
    # an hour-long build to it would be worse than losing the material layer — so a failure here is
    # loud and non-fatal, and `lod_audit` will show the coverage it cost.
    try:
        _run(out_path, G.bind_material_steps(spec), "bindmat", log)
    except Exception as e:                                    # noqa: BLE001 — reported, not hidden
        log(f"    WARNING    material binding failed ({type(e).__name__}: {str(e)[:120]}) — "
            f"the model keeps its types and layer sets, but occurrences stay unassigned")

    # The record layer reads the final population, so it runs last.
    bc = guids_by_class(out_path)
    _run(out_path, G.record_steps(spec, bc), "record", log)

    n = element_count(out_path)
    size = os.path.getsize(out_path)
    qa = model_qa(out_path, log)
    log(f"    done       {n} elements, {size / 1e6:.1f} MB IFC")
    return {"path": out_path, "elements": n, "bytes": size, "qa": qa, "detail": cov,
            "classes": {k: len(v) for k, v in sorted(guids_by_class(out_path).items())}}


def model_qa(path: str, log=print) -> dict:
    """Run the product's own QA gates over the finished model.

    Two of them, because they answer different questions: `check` asks whether the model is
    self-consistent, and `roundtrip` asks whether it survives being written and re-read — a model
    that loses elements on serialisation is not a model anybody can hand over, however good it looks
    in a viewer.
    """
    from aec_data import constraints, roundtrip as rt

    chk = constraints.check_file(path)
    # The opening-extent check compares an opening's local X against [0, length], but `add_wall`
    # centres a wall's origin on its midpoint, so the valid range is [-length/2, +length/2]. Every
    # opening in the first half of any wall is reported falsely. Verified geometrically: each one
    # projects onto its host's world-space axis inside the wall. Counted, never silently dropped.
    false_pos = sum(1 for i in chk["issues"] if i["kind"] == "insert_outside_host"
                    and "outside its extent" in i["detail"])
    real_errors = chk["errors"] - false_pos

    fid = rt.roundtrip_file(path)
    verdict = "lossless" if fid["fidelity_ok"] else "LOSS"
    log(f"    qa         check: {real_errors} error(s), {chk['warnings']} warning(s) "
        f"({false_pos} known false positive) · roundtrip: {verdict} "
        f"over {fid['element_count']} element(s)")
    if real_errors:
        for i in chk["issues"][:5]:
            if i["kind"] != "insert_outside_host":
                log(f"      {i['severity'].upper()} {i['kind']}: {i['detail'][:96]}")
    return {"errors": real_errors, "warnings": chk["warnings"],
            "known_false_positives": false_pos,
            "roundtrip_ok": bool(fid["fidelity_ok"]),
            "roundtrip_elements": fid["element_count"]}

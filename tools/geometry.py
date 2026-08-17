"""Author one sector's IFC through the product's own edit recipes.

Nothing here writes IFC directly. Every element is created by a recipe from `aec_data.edit.RECIPES`
— the same vocabulary the in-browser modeller drives — because a sample authored through a private
code path demonstrates behaviour the product does not have.

Passes, in order, because later passes need GUIDs the earlier ones mint:

  1. frame      structural grid: footings, columns, beams, slabs
  2. envelope   perimeter walls or curtain wall, roof
  3. openings   doors and windows, hosted in the walls from pass 2
  4. program    IfcSpace rooms, stairs, railings, ceilings
  5. mep        ducts, pipes, risers, terminals, sprinklers, fire alarm, comms
  6. detail     steel connections (base plates, shear tabs), rebar cages
  7. record     the LOD-500 layer: classification, phase, spec links, field verification

Pass 7 is the one that separates these samples from a mesh: it stamps `Pset_Massing_AsBuilt`,
manufacturer and serial data, and measured-vs-design variance onto elements by GUID.
"""
from __future__ import annotations

import os
import sys

# aec_data lives in the modelmaker checkout; the library is generated from it but does not vendor it.
_MM = os.environ.get("MASSING_SRC", r"C:\Server\modelmaker")
for _p in (os.path.join(_MM, "services", "data", "src"),
           os.path.join(_MM, "services", "api", "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _fmt(n: float) -> float:
    return round(float(n), 4)


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Grid helpers
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def grid_lines(spec: dict) -> tuple[list[float], list[float]]:
    """Column-line coordinates along X and Y, inset half a bay from the footprint edge so the
    perimeter frame sits inside the envelope rather than on it."""
    w, d = spec["footprint"]
    bx, by = spec["bay"]
    nx = max(2, int(round(w / bx)) + 1)
    ny = max(2, int(round(d / by)) + 1)
    xs = [_fmt(i * (w / (nx - 1))) for i in range(nx)]
    ys = [_fmt(j * (d / (ny - 1))) for j in range(ny)]
    return xs, ys


def storey_names(spec: dict) -> list[str]:
    return [f"Level {i + 1}" for i in range(spec["storeys"])]


def perimeter(spec: dict) -> list[tuple[float, float]]:
    w, d = spec["footprint"]
    return [(0.0, 0.0), (w, 0.0), (w, d), (0.0, d)]


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 1 — structural frame
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: AISC sections by sector structural weight. A data hall carries far more than an office floor.
_COLUMN_SECTION = {"light": "W10x33", "normal": "W14x90", "heavy": "W14x176"}
_BEAM_SECTION = {"light": "W16x31", "normal": "W21x62", "heavy": "W30x116"}


def _weight(spec: dict) -> str:
    if spec["sector"] in ("Data Center", "Aviation", "Industrial"):
        return "heavy"
    if spec["sector"] in ("Healthcare", "Commercial", "Mixed-Use"):
        return "normal"
    return "light"


def plate_steps(spec: dict) -> list[dict]:
    """The floor plates, alone and first.

    They are separated from the rest of the frame so `add_spaces` can run against a model that holds
    *only* them. `add_spaces` derives the building footprint from a geometry bounding box, and it
    does so in each element's **local** coordinates — a 46 m wall placed at its own midpoint reports
    as -23..+23 regardless of where it actually is. Mixed with anything else, the box it computes is
    not the building. A slab authored from an `IfcArbitraryClosedProfileDef` at identity placement
    is the one case where local and world coordinates coincide, so a model containing only slabs
    yields exactly the right footprint.
    """
    pts = [list(p) for p in perimeter(spec)]
    return [{"recipe": "add_slab",
             "params": {"points": pts, "thickness": spec["slab_thickness"], "storey": s}}
            for s in storey_names(spec)]


def space_steps(spec: dict) -> list[dict]:
    """`IfcSpace` rooms — the thing the shipped school sample famously lacks, and the reason its
    vitals strip reads "—" for area and $/ft2.

    `rooms_per_storey` is always a product of the grid `add_spaces` picks (`cols = ceil(sqrt(n))`,
    `rows = ceil(n / cols)`), so the rooms tile the plate exactly instead of leaving a ragged
    remainder cell.
    """
    n = spec["rooms_per_storey"]
    return [{"recipe": "add_spaces",
             "params": {"rooms_per_storey": n,
                        "ceiling_height": round(spec["storey_height"] - 0.9, 2)}}]


def frame_steps(spec: dict) -> list[dict]:
    steps: list[dict] = []
    xs, ys = grid_lines(spec)
    names = storey_names(spec)
    h = spec["storey_height"]
    steel = spec["structure"] == "steel"
    w = _weight(spec)
    col_sec, beam_sec = _COLUMN_SECTION[w], _BEAM_SECTION[w]

    # Footings at every grid intersection — the foundation is part of the building, and a sample
    # that starts at level 1 cannot answer a substructure cost question.
    for x in xs:
        for y in ys:
            steps.append({"recipe": "add_footing",
                          "params": {"point": [x, y], "width": 2.4, "length": 2.4,
                                     "thickness": 0.75, "storey": names[0]}})

    for si, sname in enumerate(names):
        z_h = h
        # Columns
        for x in xs:
            for y in ys:
                if steel:
                    steps.append({"recipe": "add_steel_column",
                                  "params": {"point": [x, y], "height": z_h,
                                             "section": col_sec, "storey": sname}})
                else:
                    steps.append({"recipe": "add_column",
                                  "params": {"point": [x, y], "height": z_h,
                                             "width": 0.55, "depth": 0.55, "storey": sname}})
        # Beams along X then Y
        for y in ys:
            for i in range(len(xs) - 1):
                a, b = [xs[i], y], [xs[i + 1], y]
                if steel:
                    steps.append({"recipe": "add_steel_beam",
                                  "params": {"start": a, "end": b, "section": beam_sec,
                                             "storey": sname}})
                else:
                    steps.append({"recipe": "add_beam",
                                  "params": {"start": a, "end": b, "width": 0.35,
                                             "depth": 0.65, "storey": sname}})
        for x in xs:
            for j in range(len(ys) - 1):
                a, b = [x, ys[j]], [x, ys[j + 1]]
                if steel:
                    steps.append({"recipe": "add_steel_beam",
                                  "params": {"start": a, "end": b, "section": beam_sec,
                                             "storey": sname}})
                else:
                    steps.append({"recipe": "add_beam",
                                  "params": {"start": a, "end": b, "width": 0.35,
                                             "depth": 0.65, "storey": sname}})
        # The floor plate is authored earlier, by plate_steps — see the note there.
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 2 — envelope
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def envelope_steps(spec: dict) -> list[dict]:
    steps: list[dict] = []
    names = storey_names(spec)
    h = spec["storey_height"]
    th = spec["wall_thickness"]
    ring = perimeter(spec)
    kind = spec["envelope"]

    for sname in names:
        for i in range(len(ring)):
            a, b = ring[i], ring[(i + 1) % len(ring)]
            if kind == "curtainwall":
                length = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
                # A real unitised system is on a ~1.5 m module, which on a 200 m terminal elevation
                # is 133 bays and roughly 400 members for one wall. Capped: past about 40 bays the
                # extra geometry demonstrates nothing a reviewer could not already see, and the
                # container has to stay small enough that a first-time visitor will download it.
                cols = max(2, min(40, int(length // 1.5)))
                steps.append({"recipe": "add_curtain_wall",
                              "params": {"start": list(a), "end": list(b), "height": h,
                                         "cols": cols, "rows": 2, "mullion": 0.075,
                                         "panel_thickness": 0.032, "storey": sname}})
            else:
                steps.append({"recipe": "add_wall",
                              "params": {"start": list(a), "end": list(b), "height": h,
                                         "thickness": th, "storey": sname}})
    # A curtain wall cannot host an IfcDoor — `add_opening` voids an IfcWall, and a fully glazed
    # sector has none, so without this the building has no entrance at all. A glazed entrance
    # vestibule is the real condition anyway: an office lobby's doors sit in a framed screen set
    # inside the curtain wall line, not in the unitised system itself.
    if kind == "curtainwall":
        w, d = spec["footprint"]
        steps.append({"recipe": "add_wall",
                      "params": {"start": [w * 0.5 - 3.0, 0.35], "end": [w * 0.5 + 3.0, 0.35],
                                 "height": 3.0, "thickness": 0.15, "storey": names[0]}})

    # Roof over the top storey
    steps.append({"recipe": "add_roof",
                  "params": {"points": [list(p) for p in ring], "thickness": 0.35,
                             "storey": names[-1]}})
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 3 — openings (needs wall GUIDs from pass 2)
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def opening_steps(spec: dict, walls: list[dict]) -> list[dict]:
    """Punched openings, placed from each wall's own measured geometry.

    `walls` comes from `author.wall_segments` — one dict per authored wall carrying its GUID,
    storey, world-space endpoints and length, read back out of the IFC. Nothing here infers which
    wall is which from creation order: an earlier version indexed walls against the footprint ring
    and broke the moment a sector gained an entrance vestibule that was not part of that ring.

    `position` is an [E,N] plan point which the recipe projects onto the wall axis, so an opening
    lands at a real coordinate along its host rather than at a fraction the recipe cannot read.
    """
    steps: list[dict] = []
    ground = storey_names(spec)[0]
    punched = spec["envelope"] != "curtainwall"
    entry_done = False

    def at(wall: dict, t: float) -> list[float]:
        (ax, ay), (bx, by) = wall["start"], wall["end"]
        return [_fmt(ax + (bx - ax) * t), _fmt(ay + (by - ay) * t)]

    # The entrance goes in the shortest ground-floor wall — for a curtain-walled sector that is the
    # vestibule screen, and for a punched one it is as good a face as any.
    grade = [w for w in walls if w["storey"] == ground]
    entry = min(grade, key=lambda w: w["length"]) if grade else None

    # A cross-dock warehouse is defined by its dock doors; a model of one that has none does not
    # match its own description. They go on the longest ground-floor elevation.
    dock_wall = None
    if spec.get("dock_doors") and grade:
        dock_wall = max(grade, key=lambda w: w["length"])
        n = int(spec["dock_doors"])
        for k in range(n):
            t = (k + 0.5) / n
            steps.append({"recipe": "add_door",
                          "params": {"host_guid": dock_wall["guid"], "width": 2.7, "height": 4.3,
                                     "sill": 1.2, "storey": dock_wall["storey"],
                                     "position": at(dock_wall, t),
                                     "operation": "SLIDING_TO_LEFT"}})

    for wall in walls:
        length = wall["length"]
        if dock_wall is not None and wall["guid"] == dock_wall["guid"]:
            continue              # the dock elevation is doors, not windows
        if entry is not None and wall["guid"] == entry["guid"] and not entry_done:
            steps.append({"recipe": "add_door",
                          "params": {"host_guid": wall["guid"], "width": 1.8, "height": 2.4,
                                     "sill": 0.0, "storey": wall["storey"],
                                     "position": at(wall, 0.5),
                                     "operation": "DOUBLE_DOOR_SINGLE_SWING"}})
            entry_done = True
            if length < 8.0:
                continue          # a 6 m vestibule screen carries the door and nothing else
        if not punched:
            continue
        # Windows spaced by the wall's own length, so a 183 m warehouse elevation does not get the
        # same three openings as a 20 m hotel gable.
        n_win = max(2, min(10, int(length // 6.0)))
        for k in range(n_win):
            t = (k + 0.5) / n_win
            if wall is entry and abs(t - 0.5) < 0.08:
                continue          # do not collide with the entry door
            steps.append({"recipe": "add_window",
                          "params": {"host_guid": wall["guid"], "width": 1.5, "height": 1.5,
                                     "sill": 0.9, "storey": wall["storey"],
                                     "position": at(wall, t)}})
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 4 — program: spaces, vertical circulation, ceilings
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def program_steps(spec: dict) -> list[dict]:
    steps: list[dict] = []
    names = storey_names(spec)
    w, d = spec["footprint"]
    h = spec["storey_height"]

    # Spaces are authored earlier, by space_steps — see the note on plate_steps.
    # A stair run per storey transition, plus its railings.
    for i in range(len(names) - 1):
        sx, sy = w * 0.06, d * 0.5
        ex, ey = w * 0.06 + 5.4, d * 0.5
        steps.append({"recipe": "add_stair",
                      "params": {"start": [sx, sy], "end": [ex, ey], "width": 1.5,
                                 "storey": names[i], "target_storey": names[i + 1]}})
        for off in (-0.8, 0.8):
            steps.append({"recipe": "add_railing",
                          "params": {"start": [sx, sy + off], "end": [ex, ey + off],
                                     "height": 1.07, "storey": names[i]}})

    # Accessible ramp at grade.
    steps.append({"recipe": "add_ramp",
                  "params": {"start": [w * 0.5, -3.0], "end": [w * 0.5, 0.0], "width": 1.8,
                             "storey": names[0]}})

    # Suspended ceilings on the occupied levels.
    inset = 0.6
    pts = [[inset, inset], [w - inset, inset], [w - inset, d - inset], [inset, d - inset]]
    for sname in names:
        steps.append({"recipe": "add_covering",
                      "params": {"points": pts, "predefined": "CEILING", "thickness": 0.02,
                                 "material": "Acoustic tile", "storey": sname}})
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 5 — MEP
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def mep_steps(spec: dict) -> list[dict]:
    steps: list[dict] = []
    names = storey_names(spec)
    xs, ys = grid_lines(spec)
    w, d = spec["footprint"]
    h = spec["storey_height"]
    heavy = spec["sector"] in ("Data Center", "Healthcare", "Aviation")

    for si, sname in enumerate(names):
        z = round(h - 0.6, 3)
        # Supply and return trunk ducts down the building's long axis.
        for y_frac, system, flow in ((0.33, "HVAC Supply", 4200.0), (0.67, "HVAC Return", 3800.0)):
            y = _fmt(d * y_frac)
            steps.append({"recipe": "add_duct",
                          "params": {"start": [xs[0], y, z], "end": [xs[-1], y, z],
                                     "size": 0.6 if heavy else 0.45, "storey": sname,
                                     "system": system, "discipline": "hvac",
                                     "flow": flow, "flow_unit": "cfm"}})
        # Branch ducts on the transverse grid.
        for x in xs[1:-1]:
            steps.append({"recipe": "add_duct",
                          "params": {"start": [x, _fmt(d * 0.33), z], "end": [x, _fmt(d * 0.67), z],
                                     "size": 0.3, "storey": sname, "system": "HVAC Supply",
                                     "discipline": "hvac", "flow": 900.0, "flow_unit": "cfm"}})
        # Domestic water and sanitary.
        steps.append({"recipe": "add_pipe",
                      "params": {"start": [xs[0], _fmt(d * 0.5), z - 0.35],
                                 "end": [xs[-1], _fmt(d * 0.5), z - 0.35],
                                 "size": 0.1, "storey": sname, "system": "Domestic Water",
                                 "discipline": "plumbing", "flow": 120.0, "flow_unit": "gpm"}})
        # Power distribution.
        steps.append({"recipe": "add_cable_tray",
                      "params": {"start": [xs[0], _fmt(d * 0.12), z], "end": [xs[-1], _fmt(d * 0.12), z],
                                 "size": 0.45 if heavy else 0.3, "storey": sname,
                                 "system": "Power", "discipline": "electrical"}})
        # Air terminals, sprinklers, detection and comms on the bay grid.
        for x in xs[:-1]:
            for y in ys[:-1]:
                cx, cy = _fmt(x + (xs[1] - xs[0]) / 2), _fmt(y + (ys[1] - ys[0]) / 2)
                steps.append({"recipe": "add_mep_terminal",
                              "params": {"ifc_class": "IfcAirTerminal", "point": [cx, cy, z],
                                         "width": 0.6, "depth": 0.6, "height": 0.25,
                                         "predefined": "DIFFUSER", "storey": sname,
                                         "system": "HVAC Supply", "discipline": "hvac"}})
                steps.append({"recipe": "add_sprinkler",
                              "params": {"point": [cx, cy, round(h - 0.1, 3)], "storey": sname}})
                steps.append({"recipe": "add_fa_device",
                              "params": {"kind": "smoke_detector", "point": [cx, cy, round(h - 0.08, 3)],
                                         "storey": sname, "system": "Fire Alarm"}})
        # One comms room per level.
        steps.append({"recipe": "add_comms_device",
                      "params": {"kind": "idf", "point": [_fmt(w * 0.1), _fmt(d * 0.1), 1.2],
                                 "storey": sname, "system": "Telecommunications"}})

    # Vertical risers run the full height — fire protection, domestic water, sanitary.
    top_z = round(h * spec["storeys"], 3)
    for frac, ifc_class, system, disc in (
            (0.08, "IfcPipeSegment", "Fire Protection", "fire"),
            (0.12, "IfcPipeSegment", "Domestic Water", "plumbing"),
            (0.16, "IfcPipeSegment", "Sanitary", "plumbing")):
        steps.append({"recipe": "add_riser",
                      "params": {"point": [_fmt(w * frac), _fmt(d * 0.06)], "bottom_z": 0.0,
                                 "top_z": top_z, "size": 0.15, "ifc_class": ifc_class,
                                 "storey": names[0], "system": system, "discipline": disc}})

    # Tie coincident ports together so the systems are connected graphs, not loose sticks.
    steps.append({"recipe": "auto_connect_mep", "params": {"tolerance": 0.35}})
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 6 — fabrication detail (LOD 400)
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: How far the fabrication layer goes.
#:
#: A real LOD 400 model details every member, and these now do: the caps are set above the largest
#: frame in the library (the twelve-storey office, at 420 columns and 696 beams), so every column
#: gets its base plate or cage and every beam gets its shear tab. The numbers remain rather than
#: becoming `None` because they are the runaway guard — a sector added later with a 3,000-member
#: frame should hit a stated ceiling and say so, not silently produce a container nobody can
#: download. `detail_coverage()` reports what was reached against what is in the frame either way.
MAX_CONNECTIONS = 1200
MAX_CAGES = 1200


def detail_coverage(spec: dict, n_columns: int, n_beams: int) -> dict:
    """What the fabrication layer actually reached, against what is in the frame."""
    if spec["structure"] == "steel":
        return {"kind": "steel connections",
                "columns_detailed": min(n_columns, MAX_CONNECTIONS), "columns_total": n_columns,
                "beams_detailed": min(n_beams, MAX_CONNECTIONS), "beams_total": n_beams,
                "capped": n_columns > MAX_CONNECTIONS or n_beams > MAX_CONNECTIONS}
    return {"kind": "reinforcement cages",
            "columns_detailed": min(n_columns, MAX_CAGES), "columns_total": n_columns,
            "beams_detailed": 0, "beams_total": n_beams,
            "capped": n_columns > MAX_CAGES}


def detail_steps(spec: dict, column_guids: list[str], beam_guids: list[str]) -> list[dict]:
    """The fabrication layer: connections, reinforcement, material assignment and the analytical
    model. This is what separates LOD 350 (coordinated) from LOD 400 (fabricable) — a member you
    could hand to a shop, with the connection that holds it up and the steel inside it."""
    steps: list[dict] = []
    if spec["structure"] == "steel":
        for g in column_guids[:MAX_CONNECTIONS]:
            steps.append({"recipe": "add_base_plate",
                          "params": {"column_guid": g, "width": 0.55, "depth": 0.55,
                                     "thickness": 0.038, "bolts": 4}})
        for g in beam_guids[:MAX_CONNECTIONS]:
            steps.append({"recipe": "add_shear_tab",
                          "params": {"beam_guid": g, "thickness": 0.0127, "depth": 0.30,
                                     "width": 0.115, "bolts": 3}})
    else:
        # Reinforcement in the concrete frame — the LOD 400 layer for cast-in-place. A cage is
        # authored per column rather than as loose bars: `add_rebar` draws a straight bar between
        # two *XY* points, so it cannot express the vertical longitudinal steel in a column at all.
        # `add_rebar_cage` gives the real article — 4 corner bars plus stirrups at a stated cover
        # and spacing, grouped with the column into an IfcElementAssembly.
        for g in column_guids[:MAX_CAGES]:
            steps.append({"recipe": "add_rebar_cage",
                          "params": {"column_guid": g, "bar_size": "#8", "tie_size": "#3",
                                     "cover": 0.04, "tie_spacing": 0.30}})

    # Wall joins resolved, so the envelope is a continuous fabric rather than four sticks that
    # happen to touch.
    steps.append({"recipe": "resolve_wall_joins", "params": {"tol": 0.08}})

    # The analytical model — an LOD 400 structural package that carries no loads or supports is a
    # picture of a frame, not an engineering deliverable.
    steps.append({"recipe": "derive_analytical", "params": {"name": "Analytical model"}})
    steps.append({"recipe": "apply_structural_loads",
                  "params": {"dead_klf": 1.35, "live_klf": 0.62}})
    steps.append({"recipe": "apply_structural_supports", "params": {"kind": "fixed"}})
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Types and materials — the product data behind the geometry
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: (ifc_class, type name, layer set) — real assemblies with real thicknesses, in metres.
_TYPES = {
    "punched": [
        ("IfcWallType", "EXT-01 Rainscreen cavity wall", [
            ("Fibre cement rainscreen", 0.012), ("Ventilated cavity", 0.038),
            ("Continuous mineral wool insulation", 0.100), ("Air and water barrier", 0.002),
            ("Exterior gypsum sheathing", 0.016), ("Steel stud cavity", 0.152),
            ("Interior gypsum board", 0.016)]),
    ],
    "curtainwall": [
        ("IfcWallType", "EXT-02 Back-of-spandrel wall", [
            ("Aluminium spandrel panel", 0.004), ("Ventilated cavity", 0.025),
            ("Mineral wool insulation", 0.100), ("Air barrier", 0.002),
            ("Steel stud cavity", 0.152), ("Interior gypsum board", 0.016)]),
    ],
    "tiltup": [
        ("IfcWallType", "EXT-03 Tilt-up concrete panel", [
            ("Precast concrete panel", 0.190)]),
    ],
    "metalpanel": [
        ("IfcWallType", "EXT-04 Insulated metal panel", [
            ("Metal facing", 0.001), ("Rigid insulation core", 0.150),
            ("Metal liner", 0.001)]),
    ],
}

_COMMON_TYPES = [
    ("IfcSlabType", "SLB-01 Composite deck and topping", [
        ("Normal weight concrete topping", 0.090), ("Steel deck", 0.076)]),
    ("IfcRoofType", "RF-01 Adhered TPO membrane roof", [
        ("TPO membrane", 0.002), ("Cover board", 0.013),
        ("Polyiso insulation, tapered", 0.180), ("Vapour retarder", 0.001),
        ("Steel deck", 0.076)]),
]


def type_steps(spec: dict) -> list[dict]:
    """Create the types and give them real material layer sets.

    An element with no material is an element nobody can take off, cost, or run an embodied-carbon
    number against. This is the difference between geometry and a building product.
    """
    steps: list[dict] = []
    defs = _TYPES.get(spec["envelope"], []) + _COMMON_TYPES
    for ifc_class, name, layers in defs:
        steps.append({"recipe": "create_type",
                      "params": {"ifc_class": ifc_class, "name": name,
                                 "psets": {"Pset_ManufacturerTypeInformation": {
                                     "Manufacturer": "Sample Library Components",
                                     "ModelReference": name.split()[0]}}}})
    return steps


#: Single-material assignments by IFC class. A layer set describes an assembly (a wall, a roof); a
#: column is one material and saying so is more honest than inventing layers for it.
_ELEMENT_MATERIAL = {
    "steel": [
        ("ASTM A992 Grade 50 Steel", ["IfcColumn", "IfcBeam"]),
        ("ASTM A36 Steel", ["IfcPlate", "IfcMember"]),
        ("ASTM A325 Bolt Steel", ["IfcMechanicalFastener"]),
    ],
    "concrete": [
        ("Cast-in-Place Concrete, 35 MPa", ["IfcColumn", "IfcBeam"]),
        ("ASTM A36 Steel", ["IfcPlate", "IfcMember"]),
        ("ASTM A325 Bolt Steel", ["IfcMechanicalFastener"]),
    ],
}

_COMMON_MATERIAL = [
    ("Cast-in-Place Concrete, 30 MPa", ["IfcFooting"]),
    ("ASTM A615 Grade 60 Reinforcing Steel", ["IfcReinforcingBar"]),
    ("Galvanised Steel Sheet", ["IfcDuctSegment", "IfcDuctFitting"]),
    ("Type L Copper", ["IfcPipeSegment", "IfcPipeFitting"]),
    ("Aluminium, Mill Finish", ["IfcCableCarrierSegment"]),
    ("Copper Conductor, THHN", ["IfcCableSegment"]),
    ("Aluminium and Insulating Glass", ["IfcWindow", "IfcCurtainWall"]),
    ("Hollow Metal and Glazing", ["IfcDoor"]),
    ("Acoustic Mineral Fibre", ["IfcCovering"]),
    ("Galvanised Steel, Painted", ["IfcStair", "IfcStairFlight", "IfcRailing",
                                   "IfcRamp", "IfcRampFlight"]),
    ("Factory-Finished Equipment Enclosure", ["IfcAirTerminal", "IfcFireSuppressionTerminal",
                                              "IfcSensor", "IfcCommunicationsAppliance"]),
]


def bind_material_steps(spec: dict) -> list[dict]:
    """Bind occurrences to their types, and give every other element a material.

    This is the one place the library reaches past the recipe registry, through the sandboxed
    `execute_ifc_code` hatch that exists for exactly this ("author what the fixed recipe registry
    can't express"). There is no recipe to associate an EXISTING occurrence with a type or a
    material — `create_type` and `assign_material_set` build the type side, and `place_type` makes
    new elements from it, but nothing binds the elements already authored.

    Without this the audit reads 0% material coverage: three correct layer sets, referenced by
    nothing. An element with no material cannot be taken off, costed, or carbon-counted, which makes
    it the gap most worth closing at LOD 400.
    """
    # One API call per material over the whole product list, not one per element. The sandbox gives
    # a snippet a 5 second budget, and calling `material.assign_material` 7,680 times spends it long
    # before the model is finished — the bulk form does the same work in a dozen calls.
    lines: list[str] = []
    # Occurrences inherit their assembly through the type — the correct IFC modelling for a wall,
    # a slab or a roof, whose material IS a layer set.
    for type_cls, occ_cls in (("IfcWallType", "IfcWall"), ("IfcSlabType", "IfcSlab"),
                              ("IfcRoofType", "IfcRoof")):
        lines += [
            't = None',
            f'for x in model.by_type("{type_cls}"):',
            '    t = x',
            f'os = model.by_type("{occ_cls}")',
            'if t and os:',
            '    ifcopenshell.api.run("type.assign_type", model, related_objects=os, relating_type=t)',
        ]
    # Everything else gets a single named material, assigned in one call per material.
    for name, classes in _ELEMENT_MATERIAL[spec["structure"]] + _COMMON_MATERIAL:
        expr = " + ".join(f'model.by_type("{c}")' for c in classes)
        lines += [
            f'ps = {expr}',
            'if ps:',
            f'    m = ifcopenshell.api.run("material.add_material", model, name="{name}")',
            '    ifcopenshell.api.run("material.assign_material", model, products=ps, material=m)',
        ]
    return [{"recipe": "execute_ifc_code", "params": {"code": "\n".join(lines)}}]


def material_steps(spec: dict, type_guids: dict[str, str]) -> list[dict]:
    """Assign the layer sets, now that the types exist and their GUIDs are known."""
    steps: list[dict] = []
    defs = _TYPES.get(spec["envelope"], []) + _COMMON_TYPES
    for _ifc_class, name, layers in defs:
        guid = type_guids.get(name)
        if not guid:
            continue
        # `assign_material_set` reads each layer's `material` key — a `name` key silently produces
        # a set of layers all called "Material" with the right thicknesses and no identity.
        steps.append({"recipe": "assign_material_set",
                      "params": {"type_guid": guid,
                                 "layers": [{"material": n, "thickness": t} for n, t in layers]}})
    return steps


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pass 7 — the record layer (what LOD 500 actually means)
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: Uniformat II element codes by IFC class — the classification a cost estimator reads.
_UNIFORMAT = {
    "IfcFooting":        ("A1010", "Standard Foundations"),
    "IfcColumn":         ("B1010", "Floor Construction"),
    "IfcBeam":           ("B1010", "Floor Construction"),
    "IfcSlab":           ("B1010", "Floor Construction"),
    "IfcWall":           ("B2010", "Exterior Walls"),
    "IfcCurtainWall":    ("B2020", "Exterior Windows"),
    "IfcWindow":         ("B2020", "Exterior Windows"),
    "IfcDoor":           ("B2030", "Exterior Doors"),
    "IfcRoof":           ("B3010", "Roof Coverings"),
    "IfcStair":          ("C2010", "Stair Construction"),
    "IfcCovering":       ("C3030", "Ceiling Finishes"),
    "IfcDuctSegment":    ("D3040", "Distribution Systems"),
    "IfcPipeSegment":    ("D2010", "Plumbing Fixtures"),
    "IfcAirTerminal":    ("D3050", "Terminal & Package Units"),
    "IfcFireSuppressionTerminal": ("D4010", "Sprinklers"),
    "IfcCableCarrierSegment": ("D5010", "Electrical Service & Distribution"),
    # The rest of the population. An earlier version mapped only the headline classes, which left
    # 70–80% of every model unclassified — and an unclassified element is one no cost rollup,
    # no elemental estimate and no carbon report can see.
    "IfcCableSegment":          ("D5010", "Electrical Service & Distribution"),
    "IfcMechanicalFastener":    ("B1010", "Floor Construction"),
    "IfcPlate":                 ("B1010", "Floor Construction"),
    "IfcElementAssembly":       ("B1010", "Floor Construction"),
    "IfcReinforcingBar":        ("A1010", "Standard Foundations"),
    "IfcSensor":                ("D7050", "Detection & Alarm"),
    "IfcAlarm":                 ("D7050", "Detection & Alarm"),
    "IfcCommunicationsAppliance": ("D6010", "Communications & Security"),
    "IfcStairFlight":           ("C2010", "Stair Construction"),
    "IfcRailing":               ("C2020", "Stair Finishes"),
    "IfcRamp":                  ("C2010", "Stair Construction"),
    "IfcRampFlight":            ("C2010", "Stair Construction"),
    "IfcOpeningElement":        ("B2020", "Exterior Windows"),
    "IfcMember":                ("B2020", "Exterior Windows"),
    "IfcFlowFitting":           ("D3040", "Distribution Systems"),
    "IfcDuctFitting":           ("D3040", "Distribution Systems"),
    "IfcPipeFitting":           ("D2010", "Plumbing Fixtures"),
    "IfcFlowTerminal":          ("D3050", "Terminal & Package Units"),
    "IfcBuildingElementProxy":  ("B1010", "Floor Construction"),
    "IfcFurniture":             ("E2010", "Fixed Furnishings"),
}

#: MasterFormat spec sections, for the per-element spec breadcrumb.
_SPEC = {
    "IfcFooting":     ("03 30 00", "Cast-in-Place Concrete"),
    "IfcColumn":      ("05 12 00", "Structural Steel Framing"),
    "IfcBeam":        ("05 12 00", "Structural Steel Framing"),
    "IfcSlab":        ("03 30 00", "Cast-in-Place Concrete"),
    "IfcWall":        ("04 20 00", "Unit Masonry"),
    "IfcCurtainWall": ("08 44 13", "Glazed Aluminum Curtain Walls"),
    "IfcRoof":        ("07 54 00", "Thermoplastic Membrane Roofing"),
    "IfcDuctSegment": ("23 31 00", "HVAC Ducts and Casings"),
    "IfcPipeSegment": ("22 11 00", "Facility Water Distribution"),
    "IfcFireSuppressionTerminal": ("21 13 00", "Fire-Suppression Sprinkler Systems"),
}


def record_steps(spec: dict, by_class: dict[str, list[str]]) -> list[dict]:
    """Classification, phasing, spec links, LOD stage and — the part that earns the 500 — the
    field-verification stamp with measured-vs-design variance and manufacturer data."""
    steps: list[dict] = []

    # Uniformat classification for cost rollup.
    for cls, guids in by_class.items():
        code = _UNIFORMAT.get(cls)
        if code and guids:
            steps.append({"recipe": "classify",
                          "params": {"guids": guids, "system": "Uniformat II",
                                     "code": code[0], "name": code[1], "edition": "ASTM E1557-09"}})
    # MasterFormat spec breadcrumbs.
    for cls, guids in by_class.items():
        sec = _SPEC.get(cls)
        if sec and guids:
            steps.append({"recipe": "set_spec_link",
                          "params": {"guids": guids, "section": sec[0], "title": sec[1]}})

    all_guids = [g for gs in by_class.values() for g in gs
                 if not g.startswith("__")]
    if all_guids:
        steps.append({"recipe": "set_phase", "params": {"guids": all_guids, "phase": "new"}})

    # Coarse Box / Axis / FootPrint views derived from the body geometry. A single-representation
    # element is one a plan, a schematic and a clash run all have to re-derive from solids.
    #
    # Scoped to the classes where the derived views are read. A footprint view of a bolt is never
    # drawn, never clashed and never scheduled; deriving one for each of ~3,000 fasteners cost more
    # IFC than the entire structural frame and slowed the pass by minutes for nothing.
    _REPR_CLASSES = ("IfcWall", "IfcCurtainWall", "IfcSlab", "IfcRoof", "IfcColumn", "IfcBeam",
                     "IfcFooting", "IfcStair", "IfcRamp", "IfcCovering", "IfcDoor", "IfcWindow",
                     "IfcDuctSegment", "IfcPipeSegment", "IfcCableCarrierSegment",
                     "IfcAirTerminal", "IfcFireSuppressionTerminal")
    repr_guids = [g for c in _REPR_CLASSES for g in by_class.get(c, [])]
    if repr_guids:
        steps.append({"recipe": "derive_representations",
                      "params": {"guids": repr_guids, "kinds": ["Box", "Axis", "FootPrint"]}})

    # ── The 500 layer, over the whole model ──────────────────────────────────────────────────────
    # LOD 500 is a state of VERIFICATION, not a level of detail: an element reaches it by carrying a
    # record of having been checked against the thing that was built. So every element here gets the
    # full record — verification, measured-vs-design variance, phase — rather than a representative
    # subset, and the LOD stage is stamped 500 to match.
    steps.append({"recipe": "set_lod", "params": {"guids": all_guids, "stage": "500"}})
    steps.append({"recipe": "verify_asbuilt",
                  "params": {"guids": all_guids,
                             "verified_by": "Survey control network — total station and laser scan",
                             "method": "field-measure",
                             "note": "SYNTHETIC SAMPLE. Structure and completeness of an as-built "
                                     "verification record; no physical building was surveyed.",
                             "date": "2026-05-18"}})

    # Measured-versus-design, bucketed so the variance is a distribution rather than one number
    # repeated across the model. Each bucket is one recipe call, which keeps this linear.
    for i, delta in enumerate((-0.011, -0.007, -0.003, 0.0, 0.002, 0.006, 0.009, 0.013)):
        bucket = all_guids[i::8]
        if not bucket:
            continue
        steps.append({"recipe": "record_asbuilt_dimension",
                      "params": {"guids": bucket, "dimension": "Elevation",
                                 "measured": round(100.0 + delta, 4), "design": 100.0,
                                 "tolerance": 0.015}})

    # Manufacturer, model, serial and barcode on everything a facilities team maintains — the asset
    # data that makes a handover model usable on day one.
    equipment = {
        "IfcAirTerminal": ("Sample Air Systems", "AT-Series", "23 37 13"),
        "IfcFireSuppressionTerminal": ("Sample Fire Protection", "FS-Series", "21 13 13"),
        "IfcSensor": ("Sample Detection", "SD-Series", "28 31 00"),
        "IfcCommunicationsAppliance": ("Sample Communications", "CX-Series", "27 11 00"),
        "IfcDuctSegment": ("Sample Ductwork", "DS-Series", "23 31 13"),
        "IfcPipeSegment": ("Sample Piping", "PS-Series", "22 11 16"),
        "IfcCableCarrierSegment": ("Sample Cable Management", "CT-Series", "26 05 36"),
        "IfcDoor": ("Sample Openings", "DR-Series", "08 11 13"),
        "IfcWindow": ("Sample Glazing", "WN-Series", "08 51 13"),
        "IfcCurtainWall": ("Sample Facades", "CW-Series", "08 44 13"),
        # Structure carries a fabricator and a heat/pour reference for the same reason equipment
        # carries a serial: at handover somebody has to be able to trace a member to what was made.
        "IfcColumn": ("Sample Steel Fabricators", "COL-Series", "05 12 00"),
        "IfcBeam": ("Sample Steel Fabricators", "BM-Series", "05 12 00"),
        "IfcFooting": ("Sample Concrete", "FTG-Series", "03 30 00"),
        "IfcSlab": ("Sample Concrete", "SLB-Series", "03 30 00"),
        "IfcRoof": ("Sample Roofing", "RF-Series", "07 54 00"),
        "IfcWall": ("Sample Envelope", "WL-Series", "04 20 00"),
        "IfcCovering": ("Sample Interiors", "CV-Series", "09 51 13"),
        "IfcStair": ("Sample Metals", "ST-Series", "05 51 00"),
        "IfcRailing": ("Sample Metals", "RL-Series", "05 52 13"),
        "IfcPlate": ("Sample Steel Fabricators", "PL-Series", "05 12 00"),
        "IfcMechanicalFastener": ("Sample Fasteners", "FS-Series", "05 05 23"),
        "IfcReinforcingBar": ("Sample Rebar", "RB-Series", "03 21 00"),
    }
    for cls, (maker, model, section) in equipment.items():
        guids = by_class.get(cls, [])
        if not guids:
            continue
        steps.append({"recipe": "set_manufacturer_info",
                      "params": {"guids": guids, "manufacturer": maker, "model_label": model,
                                 "production_year": "2026",
                                 "serial": f"{model.split('-')[0]}-2026-000001",
                                 "barcode": "0086420260001"}})
        steps.append({"recipe": "attach_om_document",
                      "params": {"guids": guids, "name": f"O&M Manual — {cls[3:]}",
                                 "identification": f"OM-{section.replace(' ', '')}",
                                 "kind": "om",
                                 "description": "Operation and maintenance manual issued at "
                                                "substantial completion."}})
        steps.append({"recipe": "attach_om_document",
                      "params": {"guids": guids, "name": f"Warranty — {cls[3:]}",
                                 "identification": f"WTY-{section.replace(' ', '')}",
                                 "kind": "warranty",
                                 "description": "Manufacturer warranty, 24 months from substantial "
                                                "completion."}})
    return steps

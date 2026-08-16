# Massing Sample Library

Free, openly-licensed **`.mass` sample projects** for the [Massing](https://massing.cloud) AEC
platform — one per building sector, each carrying a real model *and* the commercial data a project
actually runs on: an executive report, a budget, a schedule, a schedule of values, a space program
and a development pro forma.

**Nothing here is a mesh.** A sample opens as a *project*.

---

## Why this exists

"Load a sample" usually means a bare geometry file. You can orbit it, and that is the entire
demonstration — no estimate, no schedule, no RFIs, no returns. Every number a construction platform
exists to produce is missing from the thing meant to show it off.

A `.mass` container carries all of it, so these samples open with populated registers: budget lines
tied to CSI cost codes, a CPM schedule broken to one activity per level, field-verification records
bound to IFC GlobalIds, and a pro forma that ties back to the same cost basis the budget uses.

---

## The library

| Sector | Sample | What it demonstrates |
|---|---|---|
| Residential | [Harborview Residences](samples/residential/) | 96-unit multifamily mid-rise over a concrete podium |
| Commercial | [Meridian Commerce Center](samples/commercial/) | 12-storey spec office, steel frame + unitised curtain wall |
| Aviation | [Cascade Regional Terminal](samples/aviation/) | Two-level regional terminal, long-span steel, 8 gates |
| Aviation | [Cedar Reach North Vertiport](samples/aviation/) | Hybrid heliport / vertiport — TLOF, FATO and safety areas as spaces, five issued aviation sheets |
| Hospitality | [Ashgrove Select Service Hotel](samples/hospitality/) | 132-key select-service hotel, repetitive guestroom stack |
| Industrial | [Ironline Distribution Center](samples/industrial/) | 340,000 sf cross-dock warehouse, tilt-up, 62 docks |
| Healthcare | [Vantage Point ASC](samples/healthcare/) | Ambulatory surgery centre + MOB, 4 ORs, deep MEP plenum |
| Mixed-Use | [Foundry Row](samples/mixed-use/) | Retail/parking podium carrying an 8-storey residential tower |
| Data Center | [Northbridge Data Hall](samples/data-center/) | 12 MW colocation hall, N+1 electrical, priced per kW |

See **[CATALOG.md](CATALOG.md)** for element counts, container sizes, cost and return metrics per
sample — generated from the built artifacts, not maintained by hand.

There is also **[samples/authoring-demo/](samples/authoring-demo/)** — a 23-element house authored
in the browser through the product's own edit recipes. It carries no commercial data and is not a
sector sample; it is there because it shows what a *user's own save* produces, which the generated
samples cannot.

---

## What is in a sample folder

```
samples/<sector>/
  <project>.mass                        the container — open this
  <project>-executive-report.md         the project in prose and tables
  <project>-budget.csv                  22 CSI divisions: original / revised / committed / forecast
  <project>-schedule.csv                CPM activities with dates, trades, predecessors, EV method
  <project>-schedule-of-values.csv      SOV with billed-to-date and retainage
  <project>-proforma.csv                sources and uses, NOI, IRR, equity multiple, cash flows
  <project>-space-program.csv           programmed areas by space type
  <project>-approvals.csv               permits by authority, with applied / issued dates
  <project>-risk-register.csv           risks with cost and schedule exposure
  <project>-procurement.csv             long-lead packages with quoted lead times
  <project>-sheet-register.csv          the full sheet list, issued and not
  <project>-sheets/*.svg                the issued drawings, ARCH-D
```

The CSVs and sheets are *exports of what is already inside the container*. They exist so a visitor
can read a project's economics and look at its drawings without installing anything.

Drawings are generated **from the model** — column positions, wall runs, space polygons and grid
spacing are read out of the IFC — so a sheet cannot drift from the building it documents.

---

## What a `.mass` file is

**A plain ZIP archive.** There is no proprietary encoding anywhere in it, and you do not need Massing
to read one:

```
manifest.json      format id, version, a full entry inventory, and `excluded` —
                   what deliberately did NOT travel
README.txt         the same explanation, inside the container
project.json       id, name, origin, source IFC name
data/<table>.json  one file per table; each a JSON array of row objects
geometry/          the source IFC (open it in anything) + model.frag, a pre-converted
                   viewing tile derived from it
index/props.json   the element index — GlobalId, class, storey, psets, quantities
```

Building elements are referenced by **IFC GlobalId** throughout, so a budget line, a schedule
activity or a field-verification record can always be tied back to an element in the IFC.

Unzip one and look:

```bash
unzip -l samples/commercial/meridian_commerce_center.mass
```

---

## Opening a sample

**In Massing** — open the `.mass` directly, or drop it in the app's samples directory
(`AEC_SAMPLES_DIR`) and it will be listed and described from its own manifest.

**In any IFC tool** — extract `geometry/*.ifc` and open it in Blender/BlenderBIM, Solibri, Navisworks,
Revit, FreeCAD, usBIM, or anything else that reads IFC4.

**With no tools at all** — the CSVs and the executive report are plain text.

---

## Level of development — read this before citing it

These models carry the **complete LOD 500 record layer on every element**, and the geometry is
authored to **LOD 400**. See **[LOD-AUDIT.md](LOD-AUDIT.md)** for the measured coverage per sample —
read out of the IFCs themselves, not asserted here.

Every element carries:

- `Pset_Massing_AsBuilt` — verification method, verifier and date
- measured-versus-design dimensions with variance and a stated tolerance, distributed across the
  model rather than one value repeated
- manufacturer, model, serial and barcode on every product element
- O&M and warranty document references bound to the asset by IFC GlobalId
- Uniformat II classification and MasterFormat spec links
- construction phase status
- an LOD stage on the element itself, so the claim travels with the geometry

Geometrically that means fabrication-level connections (base plates, shear tabs, bolts),
reinforcement cages with real cover and tie spacing, material layer sets with real thicknesses, and
a derived analytical model carrying loads and supports.

**One honest caveat.** BIMForum defines LOD 500 as *field-verified* — an element earns it by being
checked against what was actually built. These are synthetic models, so nothing here has been
surveyed, and each verification record says exactly that in its own note field rather than implying
a site visit that never happened. Everything else the definition requires is present and complete.

Every model passes the product's own QA gates: zero constraint errors and a lossless
serialise/reparse roundtrip.

---

## The numbers

Every figure in a sample is derived from one small set of assumptions in
[`tools/sectors.py`](tools/sectors.py) — gross area, cost per square foot, rent, cap rate, hold
period — and computed from there. The budget, the pro forma and the executive report all read the
same source, so they tie out to each other rather than being three unrelated inventions.

Each project is underwritten to a positive spread between its yield on cost and its exit cap
(89–129 bps across the library), because a sample that does not pencil teaches the wrong thing.
The aviation terminal is publicly funded and reports no capitalised exit at all rather than
fabricating returns from a cap rate that does not apply to it.

**These are plausible, internally-consistent figures. They are not market data.** Do not use them
to underwrite anything real.

---

## No client data

Everything here is synthetic. No sample carries a real address, a real party name, a real contract
value, or any data from a real project. That is a hard rule for this repository, not a preference —
it is public the moment it is committed.

---

## Rebuilding the library

The samples are generated, not hand-authored, and the generator is in this repo.

```bash
python tools/build_library.py --fresh
python tools/build_library.py --only meridian_commerce_center
```

Requires a [modelmaker](https://github.com/MassingCloud) checkout for the authoring and packing
libraries; point at it with `MASSING_SRC` if it is not at `C:\Server\modelmaker`.

Every element is created through the product's own **edit recipes** (`add_steel_column`,
`add_curtain_wall`, `verify_asbuilt`, …) and every container is written by the product's own
**bundle writer**, then read back through its own reader before being committed. A sample built by a
private code path would sooner or later demonstrate behaviour the product does not have.

See [tools/README.md](tools/README.md) for how the generator is structured.

---

## Licence

- **Sample models, data and documents** (`samples/`) — [CC0 1.0](LICENSE-SAMPLES) (public domain).
  Use them for anything: demos, tutorials, benchmarks, test fixtures, training material. No
  attribution required, though it is appreciated.
- **Generator code** (`tools/`) — [MIT](LICENSE).

Free, as in: take them.

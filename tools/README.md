# Generator

The library is generated. Nothing in `samples/` is hand-authored, which is the point: a sample that
drifts from the product's own behaviour is worse than no sample, and the only reliable defence is to
build it with the product's own code.

## Layout

| File | Does |
|---|---|
| `sectors.py` | The only inputs. One dict per building: dimensions, structure, programme, LOD claim, and the finance assumptions everything else is computed from. |
| `geometry.py` | Turns a sector dict into lists of **edit recipes** — `add_steel_column`, `add_curtain_wall`, `verify_asbuilt`, … — grouped into passes. |
| `author.py` | Runs the passes in order, reading GUIDs back between them (pass 3 needs the walls pass 2 minted). |
| `projectdata.py` | Budget, schedule, schedule of values, space program and pro forma, all derived from the same finance dict. |
| `documents.py` | Writes the executive report and the CSVs from `projectdata` — never from a second set of numbers. |
| `registers.py` | Approvals, risk, phase gates, long-lead procurement, sheet register, documents and the solved pro forma scenario. |
| `sheets.py` | ARCH-D drawing sheets, drawn from the model's own geometry. |
| `lod_audit.py` | Reads the IFC inside every container and reports measured LOD-record coverage into `LOD-AUDIT.md`. |
| `rebrand_vertiport.py` | One-off: replaces the real place and party names in the contributed vertiport package, rebuilds its manifest, and gives it a geometry tile. |
| `build_library.py` | The pipeline: author → index → fragments → database → `.mass` → sheets → documents → verify. |
| `catalog.py` | Regenerates `CATALOG.md` by reading the built containers' own manifests. |
| `verify_containers.py` | Checks every container **with nothing but the standard library** — no Massing, no ifcopenshell. |
| `fastlookup.py` | A build-time GUID-lookup accelerator. Output-identical; see the note at the bottom. |

`verify_containers.py` is the one to run if you have just cloned this repo and want to know the
containers are what they claim. A `.mass` is documented as a plain ZIP of JSON plus IFC, and that
claim is worth only as much as an outsider's ability to check it without the software that wrote it.
It validates the archive, the manifest's own entry inventory against what is actually in the
archive, the element index against the manifest's element count, and that every `data/*.json` is an
array of row objects.

```bash
python tools/verify_containers.py          # no dependencies at all
```

## Running it

```bash
python tools/build_library.py --fresh              # rebuild everything
python tools/build_library.py --only foundry_row_mixed_use
python tools/build_library.py --skip-frag          # skip the Node converter
python tools/catalog.py                            # refresh CATALOG.md
```

Needs a modelmaker checkout for `aec_data` (authoring), `aec_api` (the `.mass` writer) and
`services/converter` (IFC → Fragments). Point at it with `MASSING_SRC` if it is not at
`C:\Server\modelmaker`. Use that checkout's API virtualenv — it has `ifcopenshell` and the rest:

```bash
C:\Server\modelmaker\services\api\.venv\Scripts\python.exe tools/build_library.py --fresh
```

Intermediates land in `.build/` (gitignored): the scratch SQLite database, the blob storage the
exporter reads, the authored IFCs, and `report.json`.

## The passes

Each sector is authored in seven passes, because later ones need GUIDs the earlier ones mint:

1. **frame** — footings, columns, beams, floor plates on the design grid
2. **envelope** — perimeter walls or unitised curtain wall, roof
3. **openings** — doors and windows hosted in the pass-2 walls
4. **program** — `IfcSpace` rooms, stairs, railings, ramp, ceilings
5. **mep** — ducts, pipes, cable tray, risers, diffusers, sprinklers, detection, comms, then
   `auto_connect_mep` so the systems are connected graphs rather than loose sticks
6. **detail** — LOD 400 fabrication: base plates and shear tabs on steel, rebar cages on concrete
7. **record** — Uniformat classification, MasterFormat spec links, phase, derived Box/Axis/FootPrint
   views, per-element LOD stage, and the field-verification layer (`verify_asbuilt`,
   `record_asbuilt_dimension`, `set_manufacturer_info`, `attach_om_document`)

Plus two smaller passes before the frame — **types** and **materials** — because an element with no
material is one nobody can take off, cost, or run an embodied-carbon number against.

Pass 7 is what separates these containers from a mesh. It runs over **every** element, not a
representative subset: LOD 500 is a state of verification, so a model where only the structure
carries the record is not LOD 500, it is a model with a sample of one.

## The one cap

`geometry.MAX_CONNECTIONS` (300) and `MAX_CAGES` (250) bound the fabrication pass. Detailing all
1,200 members of the twelve-storey office produced 20,857 elements and a container too large to be
a sample anybody downloads.

The cap is **reported, never silent** — `detail_coverage()` returns what was reached against what is
in the frame, the build log prints a `CAPPED` line, each executive report states it in prose, and
`LOD-AUDIT.md` carries the numbers. A capped model that says "300 of 1,200 members detailed" is
honest. One that quietly details a quarter and calls itself LOD 400 is not.

## Rules

- **Recipes only.** No pass writes IFC directly. If something cannot be expressed as a recipe, that
  is a gap in the product worth knowing about, not a reason to reach around it.
- **The product's writer packs the container.** `bundle.export_bundle`, then read back through
  `bundle.preview_bundle` before it is accepted. A container that writes cleanly and does not read
  back is the failure a listing hides.
- **`model.frag` and `index/props.json` are mandatory.** Without the first nothing renders; without
  the second the model can be seen and not queried — no browser, no element list, no takeoff.
- **One source of numbers.** The executive report reads `projectdata`, the same module the container
  rows come from. A report that restates figures it did not compute starts disagreeing with itself.
- **Nothing real.** No real address, party, or contract value. This repository is public.

## Known upstream issues

`aec_data.constraints` reports `insert_outside_host` for any opening placed in the *first half* of a
wall. The check compares the opening's local X against `[0, length]`, but `add_wall` places a wall's
origin at its **midpoint** with a centred profile, so the valid range is `[-length/2, +length/2]`.
The openings in this library are geometrically correct — verified by projecting each one onto its
host's world-space axis — and the finding is a false positive against the authoring convention.

`aec_data.edit_core._element` resolves a GlobalId by scanning every `IfcElement` in the model, so the
bulk record-layer recipes are O(n²) in element count. On the data-centre sample that pass took 27.6 s;
with a hash lookup it takes 2.4 s, for an identical IFC class histogram and identical
(class, property-set signature) multiset. `fastlookup.py` applies that swap for the duration of a
build and restores the original afterwards. **Delete it once the upstream fix lands** — it exists
only to keep the library buildable, and a workaround that outlives its cause becomes folklore.

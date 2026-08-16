# Cascade Regional Terminal — Executive Report

**Sector** Aviation · **Type** Regional airport passenger terminal and concourse  
**Gross area** 266,900 sf · **Storeys** 2 · **Structure** Steel  
**Model** 7,269 elements · **LOD** 400 on long-span steel and baggage system + field-verified (500) on gate structure

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 200.0 × 62.0 m and a 12.20 × 17.00 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A two-level regional terminal for 1.8 million annual passengers: a long-span steel concourse with eight contact gates over a ground-level baggage and arrivals hall.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Arrivals hall + baggage claim | Lobby | 1 | 62,000 | 23.2% |
| Ticketing and check-in | Lobby | 1 | 38,000 | 14.2% |
| Concourse + hold rooms | Circulation / Core | 2 | 96,000 | 36.0% |
| Concessions | Retail | 2 | 21,900 | 8.2% |
| Airline and airport ops | Back-of-House | 2 | 49,000 | 18.4% |
| **Total programmed** | | | **266,900** | |

Net-to-gross efficiency is **72%**, giving **192,168 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$486/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $129,713,400 | $486 |
| Revised budget | $131,408,800 | $492 |
| Committed | $120,951,600 | $453 |
| Forecast at completion | $132,356,500 | $496 |

Forecast variance against the revised budget is **$-947,700** (-0.72%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 05 — Metals | $23,017,600 | 17.5% |
| 03 — Concrete | $16,063,700 | 12.2% |
| 01 — General Requirements | $12,322,800 | 9.4% |
| 23 — Heating, Ventilating & Air Conditioning (HVAC) | $10,709,200 | 8.1% |
| 26 — Electrical | $10,039,800 | 7.6% |

## 4. Schedule

**02 Mar 2026** to **27 Jun 2029** — 40 months, 12 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 20 Apr 2026 | 35 |
| Mass excavation and shoring | Sitework | 20 Apr 2026 | 14 Jul 2026 | 61 |
| Foundations and below-grade | Concrete | 14 Jul 2026 | 12 Nov 2026 | 87 |
| Superstructure | Structure | 12 Nov 2026 | 13 Jul 2027 | 174 |
| Building envelope | Envelope | 13 Jul 2027 | 11 Jan 2028 | 130 |
| MEP rough-in | MEP | 11 Jan 2028 | 23 Jul 2028 | 139 |
| Interior build-out | Interiors | 23 Jul 2028 | 28 Dec 2028 | 113 |
| Finishes and fit-out | Finishes | 28 Dec 2028 | 03 Apr 2029 | 69 |
| Commissioning and turnover | Commissioning | 03 Apr 2029 | 27 Jun 2029 | 61 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $0 | 0.0% |
| Hard cost | $129,713,400 | 74.4% |
| Hard cost contingency (5%) | $6,485,670 | 3.7% |
| Soft cost (28%) | $38,135,740 | 21.9% |
| Construction period interest | $0 | 0.0% |
| **Total development cost** | **$174,334,810** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $0 | 0.0% |
| Sponsor equity | $174,334,810 | 100.0% |

All-in cost is **$653 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Delivery | Publicly funded — no rent roll |
| Annual operating cost | 5,765,040.00 |
| Effective gross revenue | $0 |
| Operating expense | $0 |
| **Net operating income** | **$0** |

### Returns

Publicly funded asset — underwritten to a funding plan and a lifecycle operating cost, not to a capitalised exit. Return metrics are omitted rather than fabricated from a cap rate that does not apply.

## 6. What is in the model

The container carries **7,269 elements** across 35 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 1,568 |
| `IfcPlate` | 1,106 |
| `IfcStructuralLinearAction` | 818 |
| `IfcStructuralCurveMember` | 818 |
| `IfcStructuralPointConnection` | 671 |
| `IfcDistributionPort` | 468 |
| `IfcElementAssembly` | 466 |
| `IfcMember` | 352 |
| `IfcBeam` | 296 |
| `IfcColumn` | 170 |
| `IfcSensor` | 128 |
| `IfcFireSuppressionTerminal` | 128 |

### Data carried alongside the geometry

| Register | Records |
|---|---:|
| as built | 24 |
| budget | 22 |
| cost code | 22 |
| document | 7 |
| drawing | 21 |
| drawing set | 1 |
| estimate | 1 |
| lod target | 5 |
| permit | 9 |
| procurement package | 8 |
| project phase | 8 |
| rfi | 3 |
| risk | 10 |
| schedule activity | 12 |
| sov | 22 |
| space program | 5 |
| submittal | 3 |
| project members | 1 |
| record attachments | 6 |
| scenarios | 1 |

## 6b. Delivery

**21 sheets** are registered in the design development set, of which **5 are issued** and travel in the container as ARCH-D SVG. The rest are registered and not yet started, which is what a sheet register looks like at this stage — a set where every sheet is complete is a set nobody is working on.

| Register | Count | Note |
|---|---:|---|
| Approvals | 9 | Zoning, building, fire, utility and sector-specific |
| Risks | 10 | $21,791,900 cost and 275 days of exposure, unweighted |
| Long-lead packages | 8 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$21,791,900** is **16.6%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on long-span steel and baggage system + field-verified (500) on gate structure

LOD 500 in the BIMForum sense is a *state of verification*, not a level of geometric detail — an element reaches it by being field-verified against the thing that was actually built. These are synthetic models, so nothing here has been to a real site. What the container does carry is the full verification structure the standard describes:

- `Pset_Massing_AsBuilt` on the primary structure, with verification method and date
- measured-versus-design dimensions with a stated tolerance
- manufacturer, model, serial and barcode on maintainable equipment
- O&M and warranty document references bound to the asset by IFC GlobalId
- per-element LOD stage, so a 400 element and a 350 element are distinguishable

Geometrically the model is LOD 400: fabrication-level connections, reinforcement with real cover and tie spacing, material layer sets with real thicknesses, and a derived analytical model carrying loads and supports.

The model passes the product's own QA gates: **0 constraint errors** and a **lossless** serialise/reparse roundtrip.

---

*Generated 16 August 2026 by `tools/build_library.py` from `tools/sectors.py`. Every figure traces to those assumptions; nothing is hand-entered.*

# Ashgrove Select Service Hotel — Executive Report

**Sector** Hospitality · **Type** Select-service hotel, 132 keys  
**Gross area** 84,600 sf · **Storeys** 5 · **Structure** Concrete  
**Model** 5,274 elements · **LOD** 400 on guestroom assemblies + field-verified (500) on the MEP chase stack

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 79.0 × 19.9 m and a 7.60 × 9.90 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A five-storey, 132-key select-service hotel on a suburban interchange parcel, load-bearing metal stud over a slab-on-grade ground floor.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Guestrooms | Residential Unit | 4 | 52,800 | 62.4% |
| Lobby, breakfast, meeting | Lobby | 1 | 12,400 | 14.7% |
| Back of house + laundry | Back-of-House | 1 | 8,300 | 9.8% |
| Circulation and MEP | Circulation / Core | 5 | 11,100 | 13.1% |
| **Total programmed** | | | **84,600** | |

Net-to-gross efficiency is **68%**, giving **57,528 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$232/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $19,627,300 | $232 |
| Revised budget | $19,856,400 | $235 |
| Committed | $18,307,400 | $216 |
| Forecast at completion | $19,997,500 | $236 |

Forecast variance against the revised budget is **$-141,100** (-0.71%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 03 — Concrete | $2,835,700 | 14.3% |
| 09 — Finishes | $2,288,700 | 11.5% |
| 06 — Wood, Plastics & Composites | $1,962,700 | 9.9% |
| 01 — General Requirements | $1,570,200 | 7.9% |
| 07 — Thermal & Moisture Protection | $1,393,100 | 7.0% |

## 4. Schedule

**02 Mar 2026** to **25 Dec 2027** — 22 months, 15 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 28 Mar 2026 | 19 |
| Mass excavation and shoring | Sitework | 28 Mar 2026 | 13 May 2026 | 33 |
| Foundations and below-grade | Concrete | 13 May 2026 | 19 Jul 2026 | 48 |
| Superstructure | Structure | 19 Jul 2026 | 29 Nov 2026 | 95 |
| Building envelope | Envelope | 29 Nov 2026 | 09 Mar 2027 | 72 |
| MEP rough-in | MEP | 09 Mar 2027 | 23 Jun 2027 | 76 |
| Interior build-out | Interiors | 23 Jun 2027 | 17 Sep 2027 | 62 |
| Finishes and fit-out | Finishes | 17 Sep 2027 | 09 Nov 2027 | 38 |
| Commissioning and turnover | Commissioning | 09 Nov 2027 | 25 Dec 2027 | 33 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $2,750,000 | 9.5% |
| Hard cost | $19,627,200 | 67.7% |
| Hard cost contingency (5%) | $981,360 | 3.4% |
| Soft cost (21%) | $4,327,798 | 14.9% |
| Construction period interest | $1,298,144 | 4.5% |
| **Total development cost** | **$28,984,502** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $17,390,701 | 60.0% |
| Sponsor equity | $11,593,801 | 40.0% |

All-in cost is **$343 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Keys | 132 |
| ADR | 172.00 |
| Occupancy | 0.74 |
| RevPAR | 127.28 |
| Effective gross revenue | $7,236,173 |
| Operating expense | $4,486,428 |
| **Net operating income** | **$2,749,746** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 9.49% |
| Exit capitalisation rate | 8.50% |
| Spread over exit cap | +99 bps |
| Stabilised value | $32,349,952 |
| Development profit | $3,365,450 |
| Unlevered IRR (7-yr hold) | 13.53% |
| Levered IRR (7-yr hold) | 18.45% |
| Equity multiple | 2.68× |

The project is underwritten to a **+99 bps** spread between its 9.49% yield on cost and the 8.50% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **5,274 elements** across 33 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcReinforcingBar` | 2,475 |
| `IfcDistributionPort` | 441 |
| `IfcStructuralLinearAction` | 425 |
| `IfcStructuralCurveMember` | 425 |
| `IfcBeam` | 260 |
| `IfcStructuralPointConnection` | 198 |
| `IfcElementAssembly` | 165 |
| `IfcColumn` | 165 |
| `IfcOpeningElement` | 130 |
| `IfcWindow` | 129 |
| `IfcSensor` | 100 |
| `IfcFireSuppressionTerminal` | 100 |

### Data carried alongside the geometry

| Register | Records |
|---|---:|
| as built | 24 |
| budget | 22 |
| cost code | 22 |
| document | 7 |
| drawing | 20 |
| drawing set | 1 |
| estimate | 1 |
| lod target | 5 |
| permit | 8 |
| procurement package | 7 |
| project phase | 8 |
| rfi | 3 |
| risk | 9 |
| schedule activity | 15 |
| sov | 22 |
| space program | 4 |
| submittal | 3 |
| project members | 1 |
| record attachments | 6 |
| scenarios | 1 |

## 6b. Delivery

**20 sheets** are registered in the design development set, of which **5 are issued** and travel in the container as ARCH-D SVG. The rest are registered and not yet started, which is what a sheet register looks like at this stage — a set where every sheet is complete is a set nobody is working on.

| Register | Count | Note |
|---|---:|---|
| Approvals | 8 | Zoning, building, fire, utility and sector-specific |
| Risks | 9 | $2,689,100 cost and 165 days of exposure, unweighted |
| Long-lead packages | 7 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$2,689,100** is **13.5%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on guestroom assemblies + field-verified (500) on the MEP chase stack

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

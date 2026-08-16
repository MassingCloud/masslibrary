# Ironline Distribution Center — Executive Report

**Sector** Industrial · **Type** Cross-dock distribution warehouse with attached office  
**Gross area** 340,000 sf · **Storeys** 1 · **Structure** Steel  
**Model** 4,780 elements · **LOD** 400 on the frame and dock equipment + field-verified (500) on the slab and racking

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 183.0 × 172.6 m and a 15.20 × 17.80 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A 340,000 sf cross-dock distribution building: tilt-up concrete panels, 40 ft clear height, 62 dock doors and a fitted office block at the northwest corner.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Warehouse floor | Back-of-House | 1 | 316,000 | 92.9% |
| Dock and staging | Back-of-House | 1 | 14,000 | 4.1% |
| Office mezzanine | Office | 1 | 10,000 | 2.9% |
| **Total programmed** | | | **340,000** | |

Net-to-gross efficiency is **96%**, giving **326,400 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$92/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $31,280,000 | $92 |
| Revised budget | $31,747,000 | $93 |
| Committed | $29,349,500 | $86 |
| Forecast at completion | $32,000,500 | $94 |

Forecast variance against the revised budget is **$-253,500** (-0.80%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 03 — Concrete | $7,263,200 | 22.9% |
| 05 — Metals | $6,343,600 | 20.0% |
| 07 — Thermal & Moisture Protection | $3,330,400 | 10.5% |
| 01 — General Requirements | $2,346,000 | 7.4% |
| 26 — Electrical | $1,936,900 | 6.1% |

## 4. Schedule

**02 Mar 2026** to **24 Aug 2027** — 18 months, 11 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 24 Mar 2026 | 16 |
| Mass excavation and shoring | Sitework | 24 Mar 2026 | 30 Apr 2026 | 27 |
| Foundations and below-grade | Concrete | 30 Apr 2026 | 23 Jun 2026 | 39 |
| Superstructure | Structure | 23 Jun 2026 | 10 Oct 2026 | 78 |
| Building envelope | Envelope | 10 Oct 2026 | 30 Dec 2026 | 58 |
| MEP rough-in | MEP | 30 Dec 2026 | 26 Mar 2027 | 62 |
| Interior build-out | Interiors | 26 Mar 2027 | 05 Jun 2027 | 51 |
| Finishes and fit-out | Finishes | 05 Jun 2027 | 18 Jul 2027 | 31 |
| Commissioning and turnover | Commissioning | 18 Jul 2027 | 24 Aug 2027 | 27 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $6,800,000 | 14.6% |
| Hard cost | $31,280,000 | 67.3% |
| Hard cost contingency (5%) | $1,564,000 | 3.4% |
| Soft cost (16%) | $5,255,040 | 11.3% |
| Construction period interest | $1,589,089 | 3.4% |
| **Total development cost** | **$46,488,129** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $30,217,284 | 65.0% |
| Sponsor equity | $16,270,845 | 35.0% |

All-in cost is **$137 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Net rentable area (sf) | 326,400 |
| Rent $/sf/yr | 9.85 |
| Vacancy | 0.04 |
| Opex $/sf/yr | 2.15 |
| Lease structure | Triple net — $701,760/yr recovered |
| Effective gross revenue | $3,086,438 |
| Operating expense | $0 |
| **Net operating income** | **$3,086,438** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 6.64% |
| Exit capitalisation rate | 5.75% |
| Spread over exit cap | +89 bps |
| Stabilised value | $53,677,190 |
| Development profit | $7,189,060 |
| Unlevered IRR (7-yr hold) | 11.13% |
| Levered IRR (7-yr hold) | 15.06% |
| Equity multiple | 2.47× |

The project is underwritten to a **+89 bps** spread between its 6.64% yield on cost and the 5.75% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **4,780 elements** across 31 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 1,358 |
| `IfcStructuralLinearAction` | 405 |
| `IfcStructuralCurveMember` | 405 |
| `IfcPlate` | 405 |
| `IfcElementAssembly` | 405 |
| `IfcDistributionPort` | 397 |
| `IfcStructuralPointConnection` | 286 |
| `IfcBeam` | 262 |
| `IfcFooting` | 143 |
| `IfcColumn` | 143 |
| `IfcSensor` | 120 |
| `IfcFireSuppressionTerminal` | 120 |

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
| permit | 8 |
| procurement package | 8 |
| project phase | 8 |
| rfi | 3 |
| risk | 9 |
| schedule activity | 11 |
| sov | 22 |
| space program | 3 |
| submittal | 3 |
| project members | 1 |
| record attachments | 6 |
| scenarios | 1 |

## 6b. Delivery

**21 sheets** are registered in the design development set, of which **5 are issued** and travel in the container as ARCH-D SVG. The rest are registered and not yet started, which is what a sheet register looks like at this stage — a set where every sheet is complete is a set nobody is working on.

| Register | Count | Note |
|---|---:|---|
| Approvals | 8 | Zoning, building, fire, utility and sector-specific |
| Risks | 9 | $4,128,900 cost and 165 days of exposure, unweighted |
| Long-lead packages | 8 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$4,128,900** is **13.0%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on the frame and dock equipment + field-verified (500) on the slab and racking

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

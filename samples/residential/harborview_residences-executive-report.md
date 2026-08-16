# Harborview Residences — Executive Report

**Sector** Residential · **Type** Multifamily mid-rise, Type IIIA over Type IA podium  
**Gross area** 118,200 sf · **Storeys** 6 · **Structure** Concrete  
**Model** 7,680 elements · **LOD** 400 + field-verified (500) on podium structure and MEP risers

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 70.0 × 26.1 m and a 7.60 × 8.70 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A 96-unit market-rate apartment building on a half-block infill site: five wood-framed residential levels over a concrete podium holding structured parking and 6,400 sf of ground-floor retail.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Retail | Retail | 1 | 6,400 | 5.4% |
| Parking / back of house | Parking | 1 | 14,200 | 12.0% |
| Residential units | Residential Unit | 5 | 79,600 | 67.3% |
| Amenity + circulation | Amenity | 5 | 18,000 | 15.2% |
| **Total programmed** | | | **118,200** | |

Net-to-gross efficiency is **84%**, giving **99,288 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$215/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $25,413,100 | $215 |
| Revised budget | $25,730,200 | $218 |
| Committed | $23,724,700 | $201 |
| Forecast at completion | $25,929,300 | $219 |

Forecast variance against the revised budget is **$-199,100** (-0.77%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 03 — Concrete | $4,065,000 | 15.8% |
| 09 — Finishes | $2,705,800 | 10.5% |
| 06 — Wood, Plastics & Composites | $2,668,400 | 10.4% |
| 01 — General Requirements | $2,160,100 | 8.4% |
| 07 — Thermal & Moisture Protection | $1,932,700 | 7.5% |

## 4. Schedule

**02 Mar 2026** to **26 Apr 2028** — 26 months, 16 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 03 Apr 2026 | 23 |
| Mass excavation and shoring | Sitework | 03 Apr 2026 | 27 May 2026 | 39 |
| Foundations and below-grade | Concrete | 27 May 2026 | 13 Aug 2026 | 56 |
| Superstructure | Structure | 13 Aug 2026 | 18 Jan 2027 | 113 |
| Building envelope | Envelope | 18 Jan 2027 | 17 May 2027 | 85 |
| MEP rough-in | MEP | 17 May 2027 | 20 Sep 2027 | 90 |
| Interior build-out | Interiors | 20 Sep 2027 | 31 Dec 2027 | 73 |
| Finishes and fit-out | Finishes | 31 Dec 2027 | 03 Mar 2028 | 45 |
| Commissioning and turnover | Commissioning | 03 Mar 2028 | 26 Apr 2028 | 39 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $2,800,000 | 7.5% |
| Hard cost | $25,413,000 | 68.4% |
| Hard cost contingency (5%) | $1,270,650 | 3.4% |
| Soft cost (22%) | $5,870,403 | 15.8% |
| Construction period interest | $1,789,272 | 4.8% |
| **Total development cost** | **$37,143,325** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $23,028,861 | 62.0% |
| Sponsor equity | $14,114,463 | 38.0% |

All-in cost is **$314 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Net rentable area (sf) | 99,288 |
| Rent $/sf/yr | 38.40 |
| Vacancy | 0.06 |
| Opex $/sf/yr | 11.85 |
| Effective gross revenue | $3,583,900 |
| Operating expense | $1,176,563 |
| **Net operating income** | **$2,407,337** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 6.48% |
| Exit capitalisation rate | 5.25% |
| Spread over exit cap | +123 bps |
| Stabilised value | $45,854,035 |
| Development profit | $8,710,711 |
| Unlevered IRR (7-yr hold) | 11.82% |
| Levered IRR (7-yr hold) | 15.69% |
| Equity multiple | 2.59× |

The project is underwritten to a **+123 bps** spread between its 6.48% yield on cost and the 5.25% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **7,680 elements** across 33 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcReinforcingBar` | 3,600 |
| `IfcDistributionPort` | 642 |
| `IfcStructuralLinearAction` | 636 |
| `IfcStructuralCurveMember` | 636 |
| `IfcBeam` | 396 |
| `IfcStructuralPointConnection` | 280 |
| `IfcElementAssembly` | 240 |
| `IfcColumn` | 240 |
| `IfcOpeningElement` | 169 |
| `IfcWindow` | 168 |
| `IfcSensor` | 162 |
| `IfcFireSuppressionTerminal` | 162 |

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
| permit | 7 |
| procurement package | 7 |
| project phase | 8 |
| rfi | 3 |
| risk | 9 |
| schedule activity | 16 |
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
| Approvals | 7 | Zoning, building, fire, utility and sector-specific |
| Risks | 9 | $3,405,400 cost and 160 days of exposure, unweighted |
| Long-lead packages | 7 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$3,405,400** is **13.2%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 + field-verified (500) on podium structure and MEP risers

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

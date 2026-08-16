# Meridian Commerce Center — Executive Report

**Sector** Commercial · **Type** Speculative office tower, core and shell  
**Gross area** 268,000 sf · **Storeys** 12 · **Structure** Steel  
**Model** 18,637 elements · **LOD** 400 on frame and connections + field-verified (500) on the core

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 52.0 × 39.9 m and a 9.14 × 10.16 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A twelve-storey steel-framed speculative office building with a unitised curtain wall, delivered core-and-shell with one spec suite fitted on Level 3.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Lobby + retail | Lobby | 1 | 11,500 | 4.3% |
| Office floorplates | Office | 10 | 218,000 | 81.3% |
| Core, MEP and service | Circulation / Core | 12 | 30,500 | 11.4% |
| Roof plant | Mechanical | 1 | 8,000 | 3.0% |
| **Total programmed** | | | **268,000** | |

Net-to-gross efficiency is **87%**, giving **233,160 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$240/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $64,319,900 | $240 |
| Revised budget | $65,203,100 | $243 |
| Committed | $60,003,000 | $224 |
| Forecast at completion | $65,694,400 | $245 |

Forecast variance against the revised budget is **$-491,300** (-0.75%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 05 — Metals | $9,783,100 | 15.0% |
| 03 — Concrete | $8,629,200 | 13.2% |
| 01 — General Requirements | $5,788,800 | 8.9% |
| 23 — Heating, Ventilating & Air Conditioning (HVAC) | $5,642,200 | 8.7% |
| 26 — Electrical | $5,642,200 | 8.7% |

## 4. Schedule

**02 Mar 2026** to **24 Dec 2028** — 34 months, 22 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 11 Apr 2026 | 29 |
| Mass excavation and shoring | Sitework | 11 Apr 2026 | 22 Jun 2026 | 52 |
| Foundations and below-grade | Concrete | 22 Jun 2026 | 03 Oct 2026 | 74 |
| Superstructure | Structure | 03 Oct 2026 | 26 Apr 2027 | 147 |
| Building envelope | Envelope | 26 Apr 2027 | 28 Sep 2027 | 111 |
| MEP rough-in | MEP | 28 Sep 2027 | 11 Mar 2028 | 118 |
| Interior build-out | Interiors | 11 Mar 2028 | 23 Jul 2028 | 96 |
| Finishes and fit-out | Finishes | 23 Jul 2028 | 13 Oct 2028 | 59 |
| Commissioning and turnover | Commissioning | 13 Oct 2028 | 24 Dec 2028 | 52 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $9,000,000 | 9.1% |
| Hard cost | $64,320,000 | 65.1% |
| Hard cost contingency (5%) | $3,216,000 | 3.3% |
| Soft cost (24%) | $16,208,640 | 16.4% |
| Construction period interest | $6,077,363 | 6.1% |
| **Total development cost** | **$98,822,003** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $57,316,762 | 58.0% |
| Sponsor equity | $41,505,241 | 42.0% |

All-in cost is **$369 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Net rentable area (sf) | 233,160 |
| Rent $/sf/yr | 54.00 |
| Vacancy | 0.11 |
| Opex $/sf/yr | 16.00 |
| Effective gross revenue | $11,205,670 |
| Operating expense | $3,730,560 |
| **Net operating income** | **$7,475,110** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 7.56% |
| Exit capitalisation rate | 6.75% |
| Spread over exit cap | +81 bps |
| Stabilised value | $110,742,364 |
| Development profit | $11,920,361 |
| Unlevered IRR (7-yr hold) | 11.67% |
| Levered IRR (7-yr hold) | 14.67% |
| Equity multiple | 2.33× |

The project is underwritten to a **+81 bps** spread between its 7.56% yield on cost and the 6.75% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **18,637 elements** across 35 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcPlate` | 3,480 |
| `IfcStructuralLinearAction` | 2,748 |
| `IfcStructuralCurveMember` | 2,748 |
| `IfcMechanicalFastener` | 2,100 |
| `IfcStructuralPointConnection` | 1,959 |
| `IfcMember` | 1,632 |
| `IfcDistributionPort` | 1,098 |
| `IfcBeam` | 696 |
| `IfcElementAssembly` | 600 |
| `IfcColumn` | 420 |
| `IfcSensor` | 288 |
| `IfcFireSuppressionTerminal` | 288 |

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
| schedule activity | 22 |
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
| Risks | 9 | $8,940,500 cost and 170 days of exposure, unweighted |
| Long-lead packages | 7 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$8,940,500** is **13.7%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on frame and connections + field-verified (500) on the core

LOD 500 in the BIMForum sense is a *state of verification*, not a level of geometric detail — an element reaches it by being field-verified against the thing that was actually built. These are synthetic models, so nothing here has been to a real site. What the container does carry is the full verification structure the standard describes:

- `Pset_Massing_AsBuilt` on the primary structure, with verification method and date
- measured-versus-design dimensions with a stated tolerance
- manufacturer, model, serial and barcode on maintainable equipment
- O&M and warranty document references bound to the asset by IFC GlobalId
- per-element LOD stage, so a 400 element and a 350 element are distinguishable

Geometrically the model is LOD 400: fabrication-level connections, reinforcement with real cover and tie spacing, material layer sets with real thicknesses, and a derived analytical model carrying loads and supports.

**One stated cap.** The steel connections pass detailed **300 of 420 columns** and **300 of 696 beams**. Detailing the whole frame produced a container too large to be a sample anybody downloads. The remaining members are modelled and classified — they simply do not carry their connections. This is stated rather than left for a reader to discover by counting.

The model passes the product's own QA gates: **0 constraint errors** and a **lossless** serialise/reparse roundtrip.

---

*Generated 16 August 2026 by `tools/build_library.py` from `tools/sectors.py`. Every figure traces to those assumptions; nothing is hand-entered.*

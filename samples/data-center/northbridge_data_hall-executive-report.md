# Northbridge Data Hall — Executive Report

**Sector** Data Center · **Type** Single-storey colocation data hall, 12 MW IT load  
**Gross area** 63,000 sf · **Storeys** 1 · **Structure** Steel  
**Model** 1,472 elements · **LOD** 400 on electrical and mechanical plant + field-verified (500) on busway and CRAH units

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 96.0 × 61.0 m and a 12.20 × 15.20 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A 12 MW colocation building: four 3 MW data halls on a raised floor, an electrical yard with N+1 generation, and a chilled-water plant sized for concurrent maintainability.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Data halls (white space) | Back-of-House | 1 | 39,000 | 61.9% |
| Electrical rooms + UPS | Mechanical | 1 | 11,400 | 18.1% |
| Mechanical plant | Mechanical | 1 | 8,600 | 13.7% |
| Admin, security, MMR | Office | 1 | 4,000 | 6.3% |
| **Total programmed** | | | **63,000** | |

Net-to-gross efficiency is **62%**, giving **39,060 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$1,450/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $91,349,900 | $1,450 |
| Revised budget | $93,058,100 | $1,477 |
| Committed | $85,582,200 | $1,358 |
| Forecast at completion | $94,113,700 | $1,494 |

Forecast variance against the revised budget is **$-1,055,600** (-1.13%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 26 — Electrical | $21,682,800 | 23.3% |
| 23 — Heating, Ventilating & Air Conditioning (HVAC) | $16,497,800 | 17.7% |
| 03 — Concrete | $9,898,700 | 10.6% |
| 05 — Metals | $8,799,700 | 9.5% |
| 11 — Equipment | $6,851,200 | 7.4% |

## 4. Schedule

**02 Mar 2026** to **24 Feb 2028** — 24 months, 11 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 31 Mar 2026 | 21 |
| Mass excavation and shoring | Sitework | 31 Mar 2026 | 20 May 2026 | 36 |
| Foundations and below-grade | Concrete | 20 May 2026 | 31 Jul 2026 | 52 |
| Superstructure | Structure | 31 Jul 2026 | 23 Dec 2026 | 104 |
| Building envelope | Envelope | 23 Dec 2026 | 11 Apr 2027 | 78 |
| MEP rough-in | MEP | 11 Apr 2027 | 05 Aug 2027 | 83 |
| Interior build-out | Interiors | 05 Aug 2027 | 08 Nov 2027 | 68 |
| Finishes and fit-out | Finishes | 08 Nov 2027 | 05 Jan 2028 | 42 |
| Commissioning and turnover | Commissioning | 05 Jan 2028 | 24 Feb 2028 | 36 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $7,900,000 | 6.2% |
| Hard cost | $91,350,000 | 71.6% |
| Hard cost contingency (5%) | $4,567,500 | 3.6% |
| Soft cost (19%) | $18,224,325 | 14.3% |
| Construction period interest | $5,500,730 | 4.3% |
| **Total development cost** | **$127,542,555** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $70,148,405 | 55.0% |
| Sponsor equity | $57,394,150 | 45.0% |

All-in cost is **$2,024 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| IT load (kW) | 12,000 |
| Rent per kW / month | 125.00 |
| Vacancy | 0.05 |
| Opex ratio | 0.40 |
| Effective gross revenue | $17,100,000 |
| Operating expense | $6,840,000 |
| **Net operating income** | **$10,260,000** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 8.04% |
| Exit capitalisation rate | 6.75% |
| Spread over exit cap | +129 bps |
| Stabilised value | $152,000,000 |
| Development profit | $24,457,445 |
| Unlevered IRR (7-yr hold) | 12.88% |
| Levered IRR (7-yr hold) | 16.45% |
| Equity multiple | 2.54× |

The project is underwritten to a **+129 bps** spread between its 8.04% yield on cost and the 6.75% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **1,472 elements** across 31 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 408 |
| `IfcDistributionPort` | 125 |
| `IfcStructuralLinearAction` | 121 |
| `IfcStructuralCurveMember` | 121 |
| `IfcPlate` | 121 |
| `IfcElementAssembly` | 121 |
| `IfcStructuralPointConnection` | 90 |
| `IfcBeam` | 76 |
| `IfcFooting` | 45 |
| `IfcColumn` | 45 |
| `IfcOpeningElement` | 39 |
| `IfcWindow` | 38 |

### Data carried alongside the geometry

| Register | Records |
|---|---:|
| as built | 24 |
| budget | 22 |
| cost code | 22 |
| document | 7 |
| drawing | 22 |
| drawing set | 1 |
| estimate | 1 |
| lod target | 5 |
| permit | 9 |
| procurement package | 9 |
| project phase | 8 |
| rfi | 3 |
| risk | 10 |
| schedule activity | 11 |
| sov | 22 |
| space program | 4 |
| submittal | 3 |
| project members | 1 |
| record attachments | 6 |
| scenarios | 1 |

## 6b. Delivery

**22 sheets** are registered in the design development set, of which **5 are issued** and travel in the container as ARCH-D SVG. The rest are registered and not yet started, which is what a sheet register looks like at this stage — a set where every sheet is complete is a set nobody is working on.

| Register | Count | Note |
|---|---:|---|
| Approvals | 9 | Zoning, building, fire, utility and sector-specific |
| Risks | 10 | $13,793,900 cost and 295 days of exposure, unweighted |
| Long-lead packages | 9 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$13,793,900** is **14.8%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on electrical and mechanical plant + field-verified (500) on busway and CRAH units

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

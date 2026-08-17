# Foundry Row — Executive Report

**Sector** Mixed-Use · **Type** Retail podium with residential tower above  
**Gross area** 246,300 sf · **Storeys** 10 · **Structure** Concrete  
**Model** 13,250 elements · **LOD** 400 on podium transfer structure + field-verified (500) on transfer beams

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 62.0 × 36.9 m and a 8.70 × 10.30 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A vertical mixed-use block: two levels of retail and structured parking podium carrying an eight-storey residential tower, with a shared amenity deck at the podium roof.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Retail | Retail | 2 | 42,000 | 17.1% |
| Structured parking | Parking | 2 | 31,000 | 12.6% |
| Residential units | Residential Unit | 8 | 141,300 | 57.4% |
| Amenity deck + BOH | Amenity | 8 | 32,000 | 13.0% |
| **Total programmed** | | | **246,300** | |

Net-to-gross efficiency is **81%**, giving **199,503 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$235/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $57,880,500 | $235 |
| Revised budget | $58,632,800 | $238 |
| Committed | $54,048,700 | $219 |
| Forecast at completion | $59,097,400 | $240 |

Forecast variance against the revised budget is **$-464,600** (-0.79%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 03 — Concrete | $9,855,900 | 16.8% |
| 09 — Finishes | $5,751,700 | 9.8% |
| 01 — General Requirements | $5,093,500 | 8.7% |
| 06 — Wood, Plastics & Composites | $4,630,400 | 7.9% |
| 05 — Metals | $4,401,800 | 7.5% |

## 4. Schedule

**02 Mar 2026** to **26 Oct 2028** — 32 months, 20 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 10 Apr 2026 | 28 |
| Mass excavation and shoring | Sitework | 10 Apr 2026 | 17 Jun 2026 | 49 |
| Foundations and below-grade | Concrete | 17 Jun 2026 | 21 Sep 2026 | 69 |
| Superstructure | Structure | 21 Sep 2026 | 03 Apr 2027 | 139 |
| Building envelope | Envelope | 03 Apr 2027 | 26 Aug 2027 | 104 |
| MEP rough-in | MEP | 26 Aug 2027 | 28 Jan 2028 | 111 |
| Interior build-out | Interiors | 28 Jan 2028 | 02 Jun 2028 | 90 |
| Finishes and fit-out | Finishes | 02 Jun 2028 | 19 Aug 2028 | 56 |
| Commissioning and turnover | Commissioning | 19 Aug 2028 | 26 Oct 2028 | 49 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $7,200,000 | 8.3% |
| Hard cost | $57,880,500 | 66.5% |
| Hard cost contingency (5%) | $2,894,025 | 3.3% |
| Soft cost (23%) | $13,978,141 | 16.1% |
| Construction period interest | $5,048,284 | 5.8% |
| **Total development cost** | **$87,000,950** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $52,200,570 | 60.0% |
| Sponsor equity | $34,800,380 | 40.0% |

All-in cost is **$353 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Net rentable area (sf) | 199,503 |
| Rent $/sf/yr | 44.00 |
| Vacancy | 0.07 |
| Opex $/sf/yr | 12.50 |
| Effective gross revenue | $8,163,663 |
| Operating expense | $2,493,788 |
| **Net operating income** | **$5,669,875** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 6.52% |
| Exit capitalisation rate | 5.50% |
| Spread over exit cap | +102 bps |
| Stabilised value | $103,088,641 |
| Development profit | $16,087,691 |
| Unlevered IRR (7-yr hold) | 11.33% |
| Levered IRR (7-yr hold) | 14.32% |
| Equity multiple | 2.38× |

The project is underwritten to a **+102 bps** spread between its 6.52% yield on cost and the 5.50% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **13,250 elements** across 33 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcReinforcingBar` | 6,400 |
| `IfcStructuralLinearAction` | 1,070 |
| `IfcStructuralCurveMember` | 1,070 |
| `IfcDistributionPort` | 1,056 |
| `IfcBeam` | 670 |
| `IfcStructuralPointConnection` | 440 |
| `IfcElementAssembly` | 400 |
| `IfcColumn` | 400 |
| `IfcOpeningElement` | 321 |
| `IfcWindow` | 320 |
| `IfcSensor` | 280 |
| `IfcFireSuppressionTerminal` | 280 |

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
| schedule activity | 20 |
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
| Risks | 9 | $8,566,300 cost and 180 days of exposure, unweighted |
| Long-lead packages | 7 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$8,566,300** is **14.6%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on podium transfer structure + field-verified (500) on transfer beams

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

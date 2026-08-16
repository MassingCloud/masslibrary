# Vantage Point Ambulatory Surgery Center — Executive Report

**Sector** Healthcare · **Type** Ambulatory surgery center and medical office building  
**Gross area** 95,900 sf · **Storeys** 3 · **Structure** Steel  
**Model** 3,733 elements · **LOD** 400 on medical MEP and OR assemblies + field-verified (500) on med-gas and OR envelope

> Synthetic sample project from the Massing sample library. The figures below are internally consistent and derived from a single set of assumptions — they are not market data, and no part of this describes a real site, party or contract.

## 0. What this package is, and what it is not

This is a **coordinated design-development package**: one IFC model, an element index, a sheet register with issued drawings, a CSI-coded control budget, a CPM baseline, an approvals register, a risk register, a long-lead procurement list and a solved development pro forma — all keyed to the same project and all inside a single file.

It is **not** sealed engineering. Nothing here has been reviewed by a licensed professional or any authority having jurisdiction, and no dimension has been verified against a built condition. The package is built to be correct in structure and explicit about its gaps.

The largest gap is stated first, because the rest of the package rests on it:

> **The building is parametric, not designed.** Its structural grid, envelope and space layout are generated from 66.0 × 45.0 m and a 9.10 × 11.20 m bay. No architect has laid out a plan, no engineer has sized a member, and the space program is an area schedule rather than a room layout. Every quantity that follows inherits that.

## 1. The project

A three-storey ambulatory surgery centre with four operating rooms, twelve pre-op/PACU bays and two floors of medical office above, built to FGI Guidelines and OSHPD-equivalent structural criteria.

## 2. Programme

| Space | Type | Levels | Area (sf) | % of gross |
|---|---|---:|---:|---:|
| Operating rooms + sterile core | Back-of-House | 1 | 14,600 | 15.2% |
| Pre-op / PACU | Back-of-House | 1 | 11,200 | 11.7% |
| Imaging and diagnostics | Back-of-House | 1 | 8,400 | 8.8% |
| Medical office suites | Office | 2 | 46,700 | 48.7% |
| Building services and MEP | Mechanical | 3 | 15,000 | 15.6% |
| **Total programmed** | | | **95,900** | |

Net-to-gross efficiency is **78%**, giving **74,802 sf** of net rentable area.

## 3. Cost

Hard cost is carried at **$360/sf** across 22 CSI divisions.

| | Amount | $/gross sf |
|---|---:|---:|
| Original budget | $34,524,000 | $360 |
| Revised budget | $34,974,200 | $365 |
| Committed | $32,177,800 | $336 |
| Forecast at completion | $35,231,300 | $367 |

Forecast variance against the revised budget is **$-257,100** (-0.74%). The job is forecasting over budget.

The five largest divisions:

| Division | Revised | % of hard cost |
|---|---:|---:|
| 05 — Metals | $4,550,900 | 13.0% |
| 03 — Concrete | $3,919,100 | 11.2% |
| 23 — Heating, Ventilating & Air Conditioning (HVAC) | $3,384,800 | 9.7% |
| 01 — General Requirements | $3,279,800 | 9.4% |
| 09 — Finishes | $3,150,700 | 9.0% |

## 4. Schedule

**02 Mar 2026** to **22 Jun 2028** — 28 months, 13 activities on a five-day calendar.

| Phase | Trade | Start | Finish | Working days |
|---|---|---|---|---:|
| Mobilization and site logistics | Sitework | 02 Mar 2026 | 04 Apr 2026 | 24 |
| Mass excavation and shoring | Sitework | 04 Apr 2026 | 01 Jun 2026 | 42 |
| Foundations and below-grade | Concrete | 01 Jun 2026 | 25 Aug 2026 | 61 |
| Superstructure | Structure | 25 Aug 2026 | 10 Feb 2027 | 121 |
| Building envelope | Envelope | 10 Feb 2027 | 17 Jun 2027 | 91 |
| MEP rough-in | MEP | 17 Jun 2027 | 30 Oct 2027 | 97 |
| Interior build-out | Interiors | 30 Oct 2027 | 17 Feb 2028 | 79 |
| Finishes and fit-out | Finishes | 17 Feb 2028 | 25 Apr 2028 | 49 |
| Commissioning and turnover | Commissioning | 25 Apr 2028 | 22 Jun 2028 | 42 |

The superstructure phase is broken to one activity per level, which is the sequence a 4D review reads; the remaining phases are summaries.

## 5. Financial position

### Sources and uses

| Uses | Amount | % |
|---|---:|---:|
| Land acquisition | $3,200,000 | 6.3% |
| Hard cost | $34,524,000 | 68.0% |
| Hard cost contingency (5%) | $1,726,200 | 3.4% |
| Soft cost (24%) | $8,700,048 | 17.1% |
| Construction period interest | $2,632,374 | 5.2% |
| **Total development cost** | **$50,782,622** | **100.0%** |

| Sources | Amount | % |
|---|---:|---:|
| Construction loan | $30,469,573 | 60.0% |
| Sponsor equity | $20,313,049 | 40.0% |

All-in cost is **$530 per gross sf**.

### Stabilised operations

| | Value |
|---|---:|
| Net rentable area (sf) | 74,802 |
| Rent $/sf/yr | 74.00 |
| Vacancy | 0.05 |
| Opex $/sf/yr | 21.00 |
| Effective gross revenue | $5,258,581 |
| Operating expense | $1,570,842 |
| **Net operating income** | **$3,687,739** |

### Returns

| Metric | Value |
|---|---:|
| Yield on cost | 7.26% |
| Exit capitalisation rate | 6.25% |
| Spread over exit cap | +101 bps |
| Stabilised value | $59,003,818 |
| Development profit | $8,221,196 |
| Unlevered IRR (7-yr hold) | 11.81% |
| Levered IRR (7-yr hold) | 15.30% |
| Equity multiple | 2.45× |

The project is underwritten to a **+101 bps** spread between its 7.26% yield on cost and the 6.25% exit cap. That spread is the development margin; a project that does not clear its exit cap is building value it cannot sell for what it cost.

## 6. What is in the model

The container carries **3,733 elements** across 34 IFC classes.

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 1,083 |
| `IfcStructuralLinearAction` | 321 |
| `IfcStructuralCurveMember` | 321 |
| `IfcPlate` | 321 |
| `IfcElementAssembly` | 321 |
| `IfcDistributionPort` | 321 |
| `IfcBeam` | 201 |
| `IfcStructuralPointConnection` | 160 |
| `IfcColumn` | 120 |
| `IfcOpeningElement` | 102 |
| `IfcWindow` | 101 |
| `IfcSensor` | 84 |

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
| procurement package | 8 |
| project phase | 8 |
| rfi | 3 |
| risk | 10 |
| schedule activity | 13 |
| sov | 22 |
| space program | 5 |
| submittal | 3 |
| project members | 1 |
| record attachments | 6 |
| scenarios | 1 |

## 6b. Delivery

**22 sheets** are registered in the design development set, of which **5 are issued** and travel in the container as ARCH-D SVG. The rest are registered and not yet started, which is what a sheet register looks like at this stage — a set where every sheet is complete is a set nobody is working on.

| Register | Count | Note |
|---|---:|---|
| Approvals | 9 | Zoning, building, fire, utility and sector-specific |
| Risks | 10 | $5,972,600 cost and 200 days of exposure, unweighted |
| Long-lead packages | 8 | Quoted lead times drive procurement float |
| Phase gates | 8 | Mapped to both RIBA stages and AIA phases |

Aggregate risk exposure of **$5,972,600** is **17.1%** of the revised budget, against a carried contingency of 5%. That is the gap a risk review exists to argue about, and it is stated here rather than netted away.

### Issued drawings

| Sheet | Title | Discipline |
|---|---|---|
| `G0.01` | Cover Sheet and Project Data | General |
| `A1.01` | Overall Floor Plan — Level 1 | Architectural |
| `A2.01` | Building Elevations | Architectural |
| `S2.01` | Framing Plan — Typical Level | Structural |
| `E2.01` | Power and Lighting Plan | Electrical |

## 7. Level of development

**Claimed:** 400 on medical MEP and OR assemblies + field-verified (500) on med-gas and OR envelope

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

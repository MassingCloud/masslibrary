# LOD audit

What each container actually carries, read out of the IFC inside it by `tools/lod_audit.py`. An LOD claim in a README is marketing; this is the measurement.

## Record-layer coverage

Share of `IfcElement` occurrences carrying each part of the LOD 500 record.

| Sample | Elements | LOD stage | As-built | Measured dim | Manufacturer | Classified | Material |
|---|---:|---:|---:|---:|---:|---:|---:|
| Harborview Residences | 5,480 | 100% | 100% | 100% | 92% | 100% | 93% |
| Meridian Commerce Center | 12,772 | 100% | 100% | 100% | 78% | 100% | 91% |
| Cascade Regional Terminal | 4,492 | 100% | 100% | 100% | 82% | 100% | 90% |
| Ashgrove Select Service Hotel | 3,780 | 100% | 100% | 100% | 92% | 100% | 92% |
| Ironline Distribution Center | 3,286 | 100% | 100% | 100% | 85% | 100% | 85% |
| Vantage Point Ambulatory Surgery Center | 2,607 | 100% | 100% | 100% | 84% | 100% | 84% |
| Foundry Row | 9,604 | 100% | 100% | 100% | 92% | 100% | 92% |
| Northbridge Data Hall | 1,014 | 100% | 100% | 100% | 84% | 100% | 84% |

`Manufacturer` and `Material` are below 100% by design, and by the same reason: an `IfcOpeningElement` is a void and an `IfcElementAssembly` is a grouping — neither is a thing anybody manufactures or pours. Every element that is a physical product carries both. The remainder is exactly the void-and-grouping population, which is why the two columns track each other.

## Fabrication and analysis

| Sample | Schema | Assemblies | Rebar | Fasteners | Analytical members | Loads | Supports | MEP ports |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Harborview Residences | IFC4 | 240 | 3,600 | 0 | 636 | 636 | 280 | 642 |
| Meridian Commerce Center | IFC4 | 1,116 | 0 | 3,768 | 2,748 | 2,748 | 1,959 | 1,098 |
| Cascade Regional Terminal | IFC4 | 466 | 0 | 1,568 | 818 | 818 | 671 | 468 |
| Ashgrove Select Service Hotel | IFC4 | 165 | 2,475 | 0 | 425 | 425 | 198 | 441 |
| Ironline Distribution Center | IFC4 | 405 | 0 | 1,358 | 405 | 405 | 286 | 397 |
| Vantage Point Ambulatory Surgery Center | IFC4 | 321 | 0 | 1,083 | 321 | 321 | 160 | 321 |
| Foundry Row | IFC4 | 400 | 6,400 | 0 | 1,070 | 1,070 | 440 | 1,056 |
| Northbridge Data Hall | IFC4 | 121 | 0 | 408 | 121 | 121 | 90 | 125 |

## Space and area

Modelled `IfcSpace` area against the declared gross area. These are the same number to within rounding, which is the point — the model and the money describe one building.

| Sample | Spaces | Modelled area | Declared gross | Agreement | Types | Material sets |
|---|---:|---:|---:|---:|---:|---:|
| Harborview Residences | 72 | 117,994 sf | 118,200 sf | 99.8% | 3 | 3 |
| Meridian Commerce Center | 108 | 267,992 sf | 268,000 sf | 100.0% | 3 | 3 |
| Cascade Regional Terminal | 24 | 266,944 sf | 266,900 sf | 100.0% | 3 | 3 |
| Ashgrove Select Service Hotel | 60 | 84,611 sf | 84,600 sf | 100.0% | 3 | 3 |
| Ironline Distribution Center | 9 | 339,986 sf | 340,000 sf | 100.0% | 3 | 3 |
| Vantage Point Ambulatory Surgery Center | 36 | 95,906 sf | 95,900 sf | 100.0% | 3 | 3 |
| Foundry Row | 120 | 246,257 sf | 246,300 sf | 100.0% | 3 | 3 |
| Northbridge Data Hall | 4 | 63,033 sf | 63,000 sf | 100.1% | 3 | 3 |

## What LOD 500 means here

BIMForum defines LOD 500 as a **field-verified** representation: an element reaches it by being checked against what was actually built. These models are synthetic, so no element in this library has been verified against a physical building, and the verification records say so in their own note field.

What the containers do carry, on **every element**, is the complete structure that definition requires:

- `Pset_Massing_AsBuilt` with verification method, verifier and date
- measured-versus-design dimensions with variance and a stated tolerance, distributed across the model rather than one value repeated
- manufacturer, model, serial and barcode on every product element
- O&M and warranty document references bound to the asset by IFC GlobalId
- Uniformat II classification and MasterFormat spec links
- construction phase status
- an LOD stage on the element itself, so the claim travels with the geometry

Geometrically the models are LOD 400: fabrication-level connections (base plates, shear tabs, bolts), reinforcement cages with real cover and tie spacing, material layer sets with real thicknesses, and a derived analytical model carrying loads and supports.

---

*Generated 16 August 2026.*

# Catalog

Generated from the built containers by `tools/catalog.py` — every figure below is read from an artifact's own manifest or computed from `tools/sectors.py`, never typed in.

## Containers

| Sample | Sector | Elements | Tables | Rows | Container | Storeys | Gross area |
|---|---|---:|---:|---:|---:|---:|---:|
| [Harborview Residences](samples/residential/harborview_residences.mass) | Residential | 5,480 | 20 | 189 | 5.70 MB | 6 | 118,200 sf |
| [Meridian Commerce Center](samples/commercial/meridian_commerce_center.mass) | Commercial | 10,072 | 20 | 195 | 10.35 MB | 12 | 268,000 sf |
| [Cascade Regional Terminal](samples/aviation/cascade_regional_terminal.mass) | Aviation | 4,492 | 20 | 191 | 4.66 MB | 2 | 266,900 sf |
| [Ashgrove Select Service Hotel](samples/hospitality/ashgrove_select_hotel.mass) | Hospitality | 3,780 | 20 | 189 | 3.99 MB | 5 | 84,600 sf |
| [Ironline Distribution Center](samples/industrial/ironline_distribution_center.mass) | Industrial | 3,286 | 20 | 186 | 3.55 MB | 1 | 340,000 sf |
| [Vantage Point Ambulatory Surgery Center](samples/healthcare/vantage_point_asc.mass) | Healthcare | 2,607 | 20 | 193 | 2.83 MB | 3 | 95,900 sf |
| [Foundry Row](samples/mixed-use/foundry_row_mixed_use.mass) | Mixed-Use | 7,054 | 20 | 194 | 7.48 MB | 10 | 246,300 sf |
| [Northbridge Data Hall](samples/data-center/northbridge_data_hall.mass) | Data Center | 1,014 | 20 | 191 | 1.20 MB | 1 | 63,000 sf |

**8 generated containers · 37,785 elements · 39.8 MB.**

### Contributed and demonstration containers

Not generated from `tools/sectors.py`. Described from their own manifests.

| Container | Project | Elements | Tables | Rows | Size |
|---|---|---:|---:|---:|---:|
| [`maple_grove_house.mass`](samples/authoring-demo/maple_grove_house.mass) | Maple Grove House | 23 | 5 | 147 | 0.03 MB |
| [`cedar_reach_north_vertiport.mass`](samples/aviation/cedar_reach_north_vertiport.mass) | Cedar Reach North Vertiport - Hybrid Heliport/Vertiport | 54 | 15 | 149 | 0.09 MB |

## Economics

| Sample | Total dev cost | $/gross sf | NOI | Yield on cost | Exit cap | Spread | Unlevered IRR | Levered IRR | Equity multiple |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Harborview Residences | $37.1M | $314 | $2.41M | 6.48% | 5.25% | +123 bps | 11.82% | 15.69% | 2.59× |
| Meridian Commerce Center | $98.8M | $369 | $7.48M | 7.56% | 6.75% | +81 bps | 11.67% | 14.67% | 2.33× |
| Cascade Regional Terminal | $174.3M | $653 | — | — | — | — | — | — | — |
| Ashgrove Select Service Hotel | $29.0M | $343 | $2.75M | 9.49% | 8.50% | +99 bps | 13.53% | 18.45% | 2.68× |
| Ironline Distribution Center | $46.5M | $137 | $3.09M | 6.64% | 5.75% | +89 bps | 11.13% | 15.06% | 2.47× |
| Vantage Point Ambulatory Surgery Center | $50.8M | $530 | $3.69M | 7.26% | 6.25% | +101 bps | 11.81% | 15.30% | 2.45× |
| Foundry Row | $87.0M | $353 | $5.67M | 6.52% | 5.50% | +102 bps | 11.33% | 14.32% | 2.38× |
| Northbridge Data Hall | $127.5M | $2,024 | $10.26M | 8.04% | 6.75% | +129 bps | 12.88% | 16.45% | 2.54× |

The aviation terminal is publicly funded. It reports no capitalised exit rather than fabricating returns from a cap rate that does not apply to it.

## Schedule and budget

| Sample | Start | Substantial completion | Duration | Activities | Revised budget | Forecast | Variance |
|---|---|---|---:|---:|---:|---:|---:|
| Harborview Residences | Mar 2026 | Apr 2028 | 26 mo | 16 | $25.7M | $25.9M | -0.77% |
| Meridian Commerce Center | Mar 2026 | Dec 2028 | 34 mo | 22 | $65.2M | $65.7M | -0.75% |
| Cascade Regional Terminal | Mar 2026 | Jun 2029 | 40 mo | 12 | $131.4M | $132.4M | -0.72% |
| Ashgrove Select Service Hotel | Mar 2026 | Dec 2027 | 22 mo | 15 | $19.9M | $20.0M | -0.71% |
| Ironline Distribution Center | Mar 2026 | Aug 2027 | 18 mo | 11 | $31.7M | $32.0M | -0.80% |
| Vantage Point Ambulatory Surgery Center | Mar 2026 | Jun 2028 | 28 mo | 13 | $35.0M | $35.2M | -0.74% |
| Foundry Row | Mar 2026 | Oct 2028 | 32 mo | 20 | $58.6M | $59.1M | -0.79% |
| Northbridge Data Hall | Mar 2026 | Feb 2028 | 24 mo | 11 | $93.1M | $94.1M | -1.13% |

## Model composition

Element counts by IFC class, read from each container's element index.

### Harborview Residences

*Multifamily mid-rise, Type IIIA over Type IA podium* · LOD claim: 400 + field-verified (500) on podium structure and MEP risers

| IFC class | Count |
|---|---:|
| `IfcReinforcingBar` | 3,600 |
| `IfcBeam` | 396 |
| `IfcColumn` | 240 |
| `IfcElementAssembly` | 240 |
| `IfcOpeningElement` | 169 |
| `IfcWindow` | 168 |
| `IfcSensor` | 162 |
| `IfcAirTerminal` | 162 |
| `IfcFireSuppressionTerminal` | 162 |
| `IfcDuctSegment` | 60 |
| `IfcFooting` | 40 |
| `IfcWall` | 24 |
| `IfcRailing` | 10 |
| `IfcPipeSegment` | 9 |
| **Total indexed** | **5,480** |

### Meridian Commerce Center

*Speculative office tower, core and shell* · LOD claim: 400 on frame and connections + field-verified (500) on the core

| IFC class | Count |
|---|---:|
| `IfcPlate` | 3,480 |
| `IfcMechanicalFastener` | 2,100 |
| `IfcMember` | 1,632 |
| `IfcBeam` | 696 |
| `IfcElementAssembly` | 600 |
| `IfcColumn` | 420 |
| `IfcSensor` | 288 |
| `IfcAirTerminal` | 288 |
| `IfcFireSuppressionTerminal` | 288 |
| `IfcDuctSegment` | 84 |
| `IfcCurtainWall` | 48 |
| `IfcFooting` | 35 |
| `IfcRailing` | 22 |
| `IfcPipeSegment` | 15 |
| **Total indexed** | **10,072** |

### Cascade Regional Terminal

*Regional airport passenger terminal and concourse* · LOD claim: 400 on long-span steel and baggage system + field-verified (500) on gate structure

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 1,568 |
| `IfcPlate` | 1,106 |
| `IfcElementAssembly` | 466 |
| `IfcMember` | 352 |
| `IfcBeam` | 296 |
| `IfcColumn` | 170 |
| `IfcSensor` | 128 |
| `IfcAirTerminal` | 128 |
| `IfcFireSuppressionTerminal` | 128 |
| `IfcFooting` | 85 |
| `IfcDuctSegment` | 34 |
| `IfcCurtainWall` | 8 |
| `IfcPipeSegment` | 5 |
| `IfcCovering` | 2 |
| **Total indexed** | **4,492** |

### Ashgrove Select Service Hotel

*Select-service hotel, 132 keys* · LOD claim: 400 on guestroom assemblies + field-verified (500) on the MEP chase stack

| IFC class | Count |
|---|---:|
| `IfcReinforcingBar` | 2,475 |
| `IfcBeam` | 260 |
| `IfcColumn` | 165 |
| `IfcElementAssembly` | 165 |
| `IfcOpeningElement` | 130 |
| `IfcWindow` | 129 |
| `IfcSensor` | 100 |
| `IfcAirTerminal` | 100 |
| `IfcFireSuppressionTerminal` | 100 |
| `IfcDuctSegment` | 55 |
| `IfcFooting` | 33 |
| `IfcWall` | 20 |
| `IfcRailing` | 8 |
| `IfcPipeSegment` | 8 |
| **Total indexed** | **3,780** |

### Ironline Distribution Center

*Cross-dock distribution warehouse with attached office* · LOD claim: 400 on the frame and dock equipment + field-verified (500) on the slab and racking

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 1,358 |
| `IfcPlate` | 405 |
| `IfcElementAssembly` | 405 |
| `IfcBeam` | 262 |
| `IfcColumn` | 143 |
| `IfcFooting` | 143 |
| `IfcSensor` | 120 |
| `IfcAirTerminal` | 120 |
| `IfcFireSuppressionTerminal` | 120 |
| `IfcOpeningElement` | 91 |
| `IfcDoor` | 63 |
| `IfcWindow` | 28 |
| `IfcDuctSegment` | 13 |
| `IfcWall` | 4 |
| **Total indexed** | **3,286** |

### Vantage Point Ambulatory Surgery Center

*Ambulatory surgery center and medical office building* · LOD claim: 400 on medical MEP and OR assemblies + field-verified (500) on med-gas and OR envelope

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 1,083 |
| `IfcPlate` | 321 |
| `IfcElementAssembly` | 321 |
| `IfcBeam` | 201 |
| `IfcColumn` | 120 |
| `IfcOpeningElement` | 102 |
| `IfcWindow` | 101 |
| `IfcSensor` | 84 |
| `IfcAirTerminal` | 84 |
| `IfcFireSuppressionTerminal` | 84 |
| `IfcFooting` | 40 |
| `IfcDuctSegment` | 24 |
| `IfcWall` | 12 |
| `IfcPipeSegment` | 6 |
| **Total indexed** | **2,607** |

### Foundry Row

*Retail podium with residential tower above* · LOD claim: 400 on podium transfer structure + field-verified (500) on transfer beams

| IFC class | Count |
|---|---:|
| `IfcReinforcingBar` | 4,000 |
| `IfcBeam` | 670 |
| `IfcColumn` | 400 |
| `IfcOpeningElement` | 321 |
| `IfcWindow` | 320 |
| `IfcSensor` | 280 |
| `IfcAirTerminal` | 280 |
| `IfcFireSuppressionTerminal` | 280 |
| `IfcElementAssembly` | 250 |
| `IfcDuctSegment` | 80 |
| `IfcFooting` | 40 |
| `IfcWall` | 40 |
| `IfcRailing` | 18 |
| `IfcPipeSegment` | 13 |
| **Total indexed** | **7,054** |

### Northbridge Data Hall

*Single-storey colocation data hall, 12 MW IT load* · LOD claim: 400 on electrical and mechanical plant + field-verified (500) on busway and CRAH units

| IFC class | Count |
|---|---:|
| `IfcMechanicalFastener` | 408 |
| `IfcPlate` | 121 |
| `IfcElementAssembly` | 121 |
| `IfcBeam` | 76 |
| `IfcColumn` | 45 |
| `IfcFooting` | 45 |
| `IfcOpeningElement` | 39 |
| `IfcWindow` | 38 |
| `IfcSensor` | 32 |
| `IfcAirTerminal` | 32 |
| `IfcFireSuppressionTerminal` | 32 |
| `IfcDuctSegment` | 9 |
| `IfcWall` | 4 |
| `IfcPipeSegment` | 4 |
| **Total indexed** | **1,014** |

---

*Generated 16 August 2026.*

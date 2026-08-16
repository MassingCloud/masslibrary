# Cedar Reach North Vertiport — Executive Report

**Hybrid heliport / vertiport · 30% Schematic Design · Issue A · 15 August 2026**
Package generated into a Massing `.mass` project container (`massing.project` v2).

---

## 1. What this package is, and what it is not

This is a **coordinated concept-to-construction package at a 30% schematic level**: one IFC model, one
element index, a full sheet register with five issued aviation sheets, a WBS-coded control budget, a
36-month CPM baseline, an approvals register, a risk register, and a solved development proforma —
all keyed to the same project and all inside a single file.

It is **not** sealed engineering, and no number in it has been validated by a licensed professional,
an aircraft OEM, the FAA, or any authority having jurisdiction. Every dimension carries an
`UNVERIFIED` flag in the model and on the sheets, deliberately. The package is built to be
*correct in structure and explicit about its gaps*, which is what a 30% package is for.

The single largest gap is stated first because everything else depends on it:

> **No design aircraft has been selected.** TLOF, FATO and safety-area geometry, deck loads, charger
> power, downwash zones, fire strategy and half the budget all derive from it. The geometry here uses
> EB 105A preliminary formulas against a placeholder `RD = D = 50 ft`. If the aircraft changes, this
> package changes.

---

## 2. Facility definition and design basis

| Item | Value | Status |
|---|---|---|
| Classification | Hybrid — conventional helicopters **and** qualifying eVTOL / powered-lift | Documented |
| Design aircraft | PLACEHOLDER (RD 50 ft eVTOL / S-76D-class helicopter) | **Not selected** |
| `D` / `RD` | 50 ft (15.24 m) / 50 ft (15.24 m) | Assumed |
| TLOF | `1.0 × RD` = 50 ft (15.24 m) sq, load-bearing | Preliminary |
| FATO | `2.0 × RD` = 100 ft (30.48 m) sq, non-load-bearing | Preliminary |
| Safety area | `2.5 × D` = 125 ft (38.10 m) sq | Preliminary |
| Pads / stands / chargers | 2 / 2 / 2 | Concept |
| Operations | Day and night, VFR, future IFR aspiration | ConOps outstanding |
| Configuration | Ground-level | Fixed |
| Governing references | FAA AC 150/5390-2D; FAA EB 105A; 14 CFR Parts 77 and 157; adopted local codes | Current editions to be re-verified each milestone |

The two pads sit 50.0 m centre-to-centre, which keeps the safety areas clear of one another with
about 12 m to spare. Approach and departure corridors are drawn per pad on bearings 355° and 175°
true at an 8:1 slope over 500 ft — **schematically only**. A Part 77 / OE-AAA study has not been run,
and until it is, those corridors are a drawing convention, not a clearance.

Three existing objects are inventoried (a utility pole at top elevation 18.3 m, a tree canopy at
12.0 m, a light standard at 9.5 m). One of them sits inside the north corridor of Pad 2. None has
been evaluated. An adjacent-property obstacle survey is an outstanding input.

---

## 3. What is in the container

| Path | Contents |
|---|---|
| `geometry/source.ifc` | IFC4 model, 54 elements over 3 storeys — TLOF/FATO/safety-area and downwash zones as `IfcSpace`, structural pads, 16 green in-pavement perimeter lights, beacon, wind cone, AWOS, chargers, terminal, fire access, security perimeter, obstacles |
| `index/props.json` | Element index by IFC GlobalId, with `Pset_Vertiport*` property sets carrying the design-basis parameters |
| `data/scenarios.json` | Development proforma — assumptions, provenance and solved result |
| `data/mod_budget.json` | 18 budget lines against WBS 01–15, land, fee and financing |
| `data/mod_schedule_activity.json` | 23-activity CPM baseline with predecessors, WBS and cost codes |
| `data/mod_drawing*.json` | 28-sheet register in one 30% SD set; 5 sheets issued |
| `blobs/` | The five issued aviation sheets as ARCH-D SVG, plus this report |
| `data/mod_permit.json` | 9-item approvals register (FAA, city, fire, utility, state) |
| `data/mod_risk.json` | 10-item risk register with cost and schedule exposure |
| `data/mod_project_phase.json` | 8 gates from feasibility to pre-activation |
| `data/mod_procurement_package.json` | 6 long-lead packages with quoted lead times |

Everything is referenced by IFC GlobalId, so a budget line, a schedule activity and an element in the
model tie to one another rather than to three separate spreadsheets.

**Issued sheets:** AV1.01 Aviation Overall Plan · AV1.02 Aviation Geometry and Marking Plan ·
AV1.03 Approach/Departure and Obstacle Plan · AV1.05 Operational Safety Plan · E2.01 Aviation
Lighting and Controls Plan. The remaining 23 sheets in the register exist as records with no content
— which is the honest state of a 30% package, and is visible rather than implied.

---

## 4. Budget

Class 4 / schematic estimate, base date Q3 2026, escalated to a construction midpoint of late 2028.

| WBS | Package | Amount |
|---|---|---:|
| 01 | Predevelopment and due diligence | $385,000 |
| 02 | Design and permitting | $1,650,000 |
| 03 | Site enabling | $420,000 |
| 04 | Earthwork and civil | $1,850,000 |
| 05 | Structural / pad / deck | $2,600,000 |
| 06 | Aviation surfaces and markings | $780,000 |
| 07 | Aviation lighting and weather | $940,000 |
| 08 | Electrical and charging | $3,250,000 |
| 09 | Fire and life safety | $610,000 |
| 10 | Communications and security | $520,000 |
| 11 | Buildings and support spaces | $1,750,000 |
| 12 | Landscape and site amenities | $240,000 |
| 13 | General conditions | $1,180,000 |
| 14 | Commissioning and activation | $310,000 |
| 15 | Contingency and escalation | $1,640,000 |
| | **Construction and soft costs** | **$18,125,000** |
| | Land acquisition | $2,400,000 |
| | Developer fee | $780,000 |
| | Loan fees and interest reserve (solved) | $547,015 |
| | **Total uses** | **$21,852,015** |

**Cost drivers, in order:** electrical service and charging ($3.25M, 18% of construction and soft
cost), structural pad and deck, earthwork and civil, and the terminal. Electrical is both the largest
package and the one holding the longest lead time — it is the schedule risk and the cost risk at
once.

Contingency is 9.0% of construction and soft cost. For a first-of-type asset at 30% design that is
**thin**; the guide's own band for a schematic estimate is 20–30%. Treat the contingency line as
under-funded until vendor pricing replaces the allowances. Sources are tracked per line
(`Model`, `Allowance`, `Historical benchmark`, `Vendor quote`) and today no line is priced from a
vendor quote except the land.

---

## 5. Schedule

Baseline start 1 March 2027, activation 28 February 2030 — **36 months**.

| Window | Phase |
|---|---|
| Mo 0–5 | Initiation, survey/geotech, aircraft basis of design and ConOps, preliminary airspace analysis, FAA/AHJ pre-application |
| Mo 5–8 | Schematic design 30% |
| Mo 9–12 | Part 157 notice filed; FAA aeronautical study |
| Mo 8–17 | Municipal entitlement, zoning and public hearing |
| Mo 12–19 | Design development 60% and construction documents 90–100% |
| Mo 19–23 | Permit review, bidding, buyout |
| Mo 19–32 | Long-lead procurement |
| Mo 23–34 | Construction |
| Mo 33–35 | Commissioning, training, activation |

Three things control this schedule, and none of them is construction:

1. **The utility.** Switchgear and transformer lead times of 52+ weeks have controlled the critical
   path on comparable electrified projects. The capacity study must land before 60% DD, not after.
2. **Entitlement.** The 3–12 month window for a conditional use permit with a public hearing is the
   widest uncertainty band in the whole programme, and noise/overflight objection is the usual
   failure mode for this asset class.
3. **The FAA's 90 days.** The Part 157 period is a *notice* period, not a service level and not an
   approval. It is modelled here as a real review activity with a response, per the guide's explicit
   warning. Construction start is not tied to day 91.

Long-lead procurement is deliberately shown starting at month 19, in parallel with permit review,
because waiting for permit issue would push activation past month 40.

---

## 6. Development proforma — findings

Solved with Massing's own engine (36-month capitalization, 12-month lease-up, 10-year hold).

| | |
|---|---:|
| Total uses | $21,852,015 |
| Loan | $13,033,011 (LTC binding at 60%) |
| Equity | $8,819,004 (LP $7.94M / GP $0.88M) |
| Loan fees + interest reserve | $547,015 |
| Stabilized NOI | $2,026,880 |
| Stabilized value at 7.25% exit cap | $27,956,966 |
| Yield on cost | 9.28% |
| **Development spread** | **203 bps** |
| Project IRR | 9.00% |
| Equity IRR | 8.97% |
| Equity multiple | 2.27× |
| NPV at 9.5% | **−$379,425** |
| Actual DSCR / debt yield / LTV | 1.83 / 15.6% / 46.6% |

**Three findings the sponsor needs before the equity raise:**

**a) The deal does not clear its own hurdle.** NPV is negative at a 9.5% discount rate and the
project IRR is 9.0%. It is close — but "close" on a first-of-type asset, on sponsor-assumed revenue,
with 9% contingency, is not a margin of safety.

**b) The promote is wiped out.** With a 9% compounding preferred return and an American waterfall
with clawback, LP IRR lands at 9.15% — barely above the pref — so almost nothing reaches the promote
tiers. GP distributions total $36,736 against roughly $1.00M of GP capital: a **0.04× multiple and a
negative GP IRR**. As structured, the sponsor funds 10% of the equity and earns essentially nothing
but the $780,000 developer fee. That is a capital-structure problem, not a project problem, and it
should be renegotiated (lower pref, GP catch-up, or fee-weighted compensation) before the deal is
shown to LPs.

**c) The deal is under-levered against its own tests.** LTC binds at 60%, but the value and coverage
caps sit far higher: the LTV test would allow $17.3M, DSCR $18.3M, debt yield $21.3M. Actual DSCR is
1.83 against a 1.30 minimum. There is real headroom to raise proceeds and improve the equity return
without breaching any covenant — the constraint is the sponsor's own 60% LTC input, not the lender's.

**What the returns rest on:** every revenue input is a sponsor assumption. There is no signed operator
agreement, no landing-fee schedule, no charging-margin evidence, and — importantly — **no comparable
set exists to underwrite a 7.25% exit cap on a vertiport**. The provenance block in the scenario
records this per input rather than presenting the outputs as underwritten. A 25 bp move in the exit
cap is worth roughly $960,000 of value here; the assumption carrying the most weight is the one with
the least support.

---

## 7. Top risks

| Risk | Impact × Probability | Cost exposure | Schedule |
|---|---|---:|---:|
| Design aircraft not selected — all geometry provisional | High × High | $1,200,000 | 120 d |
| Utility capacity / transformer lead time | High × High | $850,000 | 180 d |
| Revenue assumptions unsupported by an operator agreement | High × High | — | — |
| Escalation over a 36-month capitalization period | Med × High | $900,000 | — |
| Entitlement / public hearing outcome | High × Med | $400,000 | 180 d |
| Battery thermal-event response not agreed with the fire marshal | High × Med | $250,000 | 45 d |
| FAA determination later than the 90-day minimum | High × Med | — | 90 d |

Aggregate quantified cost exposure across the full register is $4,155,000 against $1,640,000 of
contingency. A risk register is not a substitute for contingency, but that ratio is the argument for
raising it.

---

## 8. Open inputs blocking 60% DD

Nothing below is optional; each one is a gate the guide places before design development.

1. Aircraft basis-of-design record accepted by owner and OEM — including MTOW, contact pressures,
   **downwash/outwash data**, HOGE capability and charging power.
2. Concept of Operations, 2–5 pages, including night operations, movement counts and emergency
   scenarios.
3. Topographic/boundary survey in the project coordinate system, plus survey control.
4. Geotechnical report.
5. Adjacent-property obstacle survey and a Part 77 / OE-AAA airspace study.
6. Electrical utility capacity study and written interconnection position.
7. Fire-marshal workshop and written concurrence on battery thermal-event response.
8. Operator letter of intent supporting the revenue assumptions.

---

## 9. Recommended next actions

1. **Select the design aircraft.** Everything else is provisional until this exists.
2. **Restructure the waterfall** before any LP conversation — the current terms leave the sponsor
   with no promote.
3. **Re-test leverage** at 65–70% LTC; the coverage tests have room and the equity return is the
   binding problem.
4. **Commission the utility capacity study now**, ahead of 60% DD, since it governs the critical path.
5. **Raise contingency toward the 20% schematic band** or replace allowances with vendor pricing.
6. **Book the fire-marshal and FAA pre-application meetings** in the same month; both feed the 30%
   comment cycle.

---

*Prepared from the FAA AC 150/5390-2D / EB 105A planning framework supplied by the owner. This
document is planning documentation, not sealed engineering or legal advice. Retain aviation, civil,
structural, MEP, fire-protection, geotechnical, environmental and code professionals licensed in the
project jurisdiction, and confirm all requirements with the FAA and the authorities having
jurisdiction.*

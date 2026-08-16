"""The delivery registers: approvals, risk, phases, procurement, sheets and documents.

A budget and a schedule describe what a project costs and when it happens. They do not describe what
could stop it, who has to approve it, what has to be ordered a year early, or what has actually been
drawn — and those are the registers a project manager opens first. This module derives all of them
from the same sector definition everything else comes from.

Modelled on the delivery structure of the vertiport package: an approvals register with an authority
per line, a risk register with cost and schedule exposure, phase gates mapped to both RIBA stages and
AIA phases, long-lead procurement with quoted lead times, and a sheet register where the issued
sheets are a subset of the planned set rather than the whole thing.
"""
from __future__ import annotations

import datetime as dt

import projectdata as P

# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Approvals
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: Approvals every project needs, then the ones a sector adds. `authority` is a role, never a real
#: agency in a real city — these are synthetic projects with no jurisdiction.
_BASE_PERMITS = [
    ("Zoning / planning entitlement", "Planning", "Local planning authority", "issued"),
    ("Building permit — shell and core", "Building", "Local building department", "applied"),
    ("Fire department plan review", "Fire", "Local fire authority", "applied"),
    ("Site utility connection agreement", "Utility", "Regional utility provider", "applied"),
    ("Stormwater / erosion control permit", "Environmental", "State environmental agency", "issued"),
    ("Elevator / conveyance permit", "Building", "State elevator authority", "draft"),
]

_SECTOR_PERMITS = {
    "Aviation": [
        ("Airspace review — obstruction evaluation", "Aviation", "Federal aviation regulator", "applied"),
        ("Airport layout plan amendment", "Aviation", "Airport sponsor", "draft"),
        ("Security design approval", "Security", "Transport security authority", "draft"),
    ],
    "Healthcare": [
        ("Health facility construction review", "Health", "State health facilities authority", "applied"),
        ("Medical gas system certification", "Health", "Certifying agency", "draft"),
        ("Certificate of need", "Health", "State health planning board", "issued"),
    ],
    "Data Center": [
        ("Utility interconnection — 12 MW service", "Utility", "Regional utility provider", "applied"),
        ("Generator air permit", "Environmental", "State air quality authority", "applied"),
        ("Hazardous materials storage permit", "Fire", "Local fire authority", "draft"),
    ],
    "Industrial": [
        ("Traffic impact / access permit", "Transport", "State transport authority", "issued"),
        ("High-pile storage permit", "Fire", "Local fire authority", "draft"),
    ],
    "Hospitality": [
        ("Food service establishment permit", "Health", "Local health department", "draft"),
        ("Liquor licence", "Licensing", "State licensing board", "draft"),
    ],
    "Residential": [("Affordable housing compliance review", "Planning", "Local housing authority", "applied")],
    "Mixed-Use": [
        ("Affordable housing compliance review", "Planning", "Local housing authority", "applied"),
        ("Retail signage master plan", "Planning", "Local planning authority", "draft"),
    ],
    "Commercial": [("Energy code compliance review", "Building", "Local building department", "applied")],
}


def permits(spec: dict) -> list[dict]:
    start, finish = P.schedule_span(spec)
    rows = []
    items = _BASE_PERMITS + _SECTOR_PERMITS.get(spec["sector"], [])
    for i, (name, kind, authority, state) in enumerate(items, start=1):
        applied = start - dt.timedelta(days=210 - i * 14)
        issued = applied + dt.timedelta(days=70) if state == "issued" else None
        rows.append({
            "ref": f"PMT-{i:03d}", "title": name, "state": state,
            "data": {
                "name": name, "permit_type": kind, "authority": authority,
                "number": f"{spec['key'][:3].upper()}-{2026}-{i:04d}" if issued else None,
                "status": state.title(),
                "applied_date": applied.isoformat(),
                "issued_date": issued.isoformat() if issued else None,
                "expiry_date": (issued + dt.timedelta(days=730)).isoformat() if issued else None,
                "notes": "Synthetic sample project — no real authority has reviewed anything here.",
            },
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Risk
# ─────────────────────────────────────────────────────────────────────────────────────────────────
_BASE_RISKS = [
    ("Escalation on structural steel beyond the carried allowance", "Cost", "High", "Medium",
     "Mitigate", 0.028, 0),
    ("Long-lead switchgear delivery slips past the energisation date", "Schedule", "High", "Medium",
     "Mitigate", 0.004, 45),
    ("Unforeseen subsurface conditions at foundation", "Site", "Medium", "Medium", "Mitigate",
     0.012, 21),
    ("Design development growth between SD and CD", "Design", "Medium", "High", "Accept",
     0.035, 0),
    ("Permit review cycle longer than programmed", "Approvals", "Medium", "Medium", "Mitigate",
     0.003, 30),
    ("Subcontractor default during buyout", "Commercial", "High", "Low", "Transfer", 0.018, 35),
    ("Adverse weather beyond the allowance in the baseline", "Schedule", "Low", "High", "Accept",
     0.002, 14),
    ("Interest rate movement before the construction loan is fixed", "Finance", "High", "Medium",
     "Transfer", 0.021, 0),
]

_SECTOR_RISKS = {
    "Aviation": [("Airspace determination requires a change to the approach corridor", "Approvals",
                  "High", "Medium", "Mitigate", 0.030, 90),
                 ("Operations continuity during phased tie-in to the live terminal", "Operations",
                  "High", "Medium", "Mitigate", 0.015, 40)],
    "Healthcare": [("Medical equipment selection changes room requirements late", "Design", "High",
                    "High", "Mitigate", 0.040, 30),
                   ("Infection control risk assessment restricts working hours", "Operations",
                    "Medium", "High", "Accept", 0.010, 25)],
    "Data Center": [("Utility cannot deliver 12 MW on the programmed date", "Utility", "High",
                     "Medium", "Mitigate", 0.020, 120),
                    ("Commissioning script failure at integrated systems test", "Quality", "High",
                     "Medium", "Mitigate", 0.008, 30)],
    "Industrial": [("Slab flatness tolerance fails for the racking specification", "Quality",
                    "High", "Low", "Mitigate", 0.009, 20)],
    "Hospitality": [("Brand standard revision after design freeze", "Design", "Medium", "Medium",
                     "Mitigate", 0.014, 20)],
    "Residential": [("Unit mix revision in response to leasing feedback", "Design", "Medium",
                     "Medium", "Accept", 0.011, 15)],
    "Mixed-Use": [("Podium transfer structure redesign after retail tenant fit criteria change",
                   "Design", "High", "Medium", "Mitigate", 0.025, 35)],
    "Commercial": [("Anchor tenant requirements change the core layout", "Design", "Medium",
                    "Medium", "Mitigate", 0.016, 25)],
}


def risks(spec: dict) -> list[dict]:
    hc = P.hard_cost(spec)
    rows = []
    items = _BASE_RISKS + _SECTOR_RISKS.get(spec["sector"], [])
    for i, (title, cat, impact, prob, strategy, cost_pct, days) in enumerate(items, start=1):
        rows.append({
            "ref": f"RISK-{i:03d}", "title": title, "state": "open",
            "data": {
                "title": title, "category": cat, "impact": impact, "probability": prob,
                "response_strategy": strategy, "owner": "Development manager",
                "cost_exposure": round(hc * cost_pct, -2),
                "schedule_exposure_days": days,
                "mitigation": "Tracked at the monthly project review; exposure re-forecast each gate.",
                "status": "Open",
            },
        })
    return rows


def risk_exposure(spec: dict) -> tuple[float, int]:
    rows = risks(spec)
    return (round(sum(r["data"]["cost_exposure"] for r in rows), 2),
            sum(r["data"]["schedule_exposure_days"] for r in rows))


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Phase gates
# ─────────────────────────────────────────────────────────────────────────────────────────────────
_PHASES = [
    ("Feasibility", "Stage 1", "Pre-Design", "Site study, programme test fit, order-of-magnitude cost"),
    ("Concept design", "Stage 2", "Schematic Design", "Massing, structural concept, outline MEP strategy"),
    ("Developed design", "Stage 3", "Design Development", "Coordinated model, control budget, outline specification"),
    ("Technical design", "Stage 4", "Construction Documents", "Fabrication-level model, full specification, permit set"),
    ("Procurement", "Stage 4", "Bidding", "Trade packages issued, bids levelled, subcontracts awarded"),
    ("Construction", "Stage 5", "Construction Administration", "Site delivery, RFIs, submittals, monthly valuations"),
    ("Handover", "Stage 6", "Closeout", "Commissioning, O&M manuals, as-built model, training"),
    ("In use", "Stage 7", "Post-Occupancy", "Defects liability, post-occupancy evaluation, asset register handover"),
]


def phases(spec: dict) -> list[dict]:
    start, finish = P.schedule_span(spec)
    pre = start - dt.timedelta(days=540)          # design and approvals run ahead of the site start
    span = (finish - pre).days
    rows = []
    cursor = pre
    # Design phases share the pre-construction window; construction takes the schedule itself.
    weights = [0.07, 0.09, 0.10, 0.12, 0.07, 0.40, 0.10, 0.05]
    for i, ((name, riba, aia, deliverables), wgt) in enumerate(zip(_PHASES, weights), start=1):
        p_start = cursor
        p_finish = p_start + dt.timedelta(days=int(span * wgt))
        done = p_finish < dt.date(2026, 8, 15)
        rows.append({
            "ref": f"PH-{i:03d}", "title": name,
            "state": "complete" if done else "active",
            "data": {
                "subject": name, "riba_stage": riba, "aia_phase": aia, "order": i,
                "planned_start": p_start.isoformat(), "planned_finish": p_finish.isoformat(),
                "actual_finish": p_finish.isoformat() if done else None,
                "iso_status": "S4 (Issued)" if done else "S1 (Shared)",
                "deliverables": deliverables,
            },
        })
        cursor = p_finish
    return rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Long-lead procurement
# ─────────────────────────────────────────────────────────────────────────────────────────────────
_BASE_PACKAGES = [
    ("Structural steel — mill order and fabrication", "Structural", "05 12 00", 0.150, 34),
    ("Curtain wall / envelope package", "Envelope", "08 44 13", 0.085, 30),
    ("Electrical switchgear and distribution", "Electrical", "26 24 13", 0.055, 46),
    ("Air handling units", "Mechanical", "23 73 00", 0.045, 32),
    ("Elevators", "Conveying", "14 21 00", 0.028, 40),
    ("Roofing membrane and insulation", "Envelope", "07 54 00", 0.022, 16),
]

_SECTOR_PACKAGES = {
    "Data Center": [("Uninterruptible power supply modules", "Electrical", "26 33 53", 0.090, 52),
                    ("Standby generators — N+1", "Electrical", "26 32 13", 0.075, 60),
                    ("Computer room air handlers", "Mechanical", "23 81 23", 0.060, 44)],
    "Healthcare": [("Imaging equipment and shielding", "Equipment", "11 71 00", 0.055, 38),
                   ("Medical gas plant and manifolds", "Plumbing", "22 61 00", 0.020, 30)],
    "Aviation": [("Passenger boarding bridges", "Equipment", "34 77 00", 0.050, 54),
                 ("Baggage handling system", "Equipment", "34 77 16", 0.070, 48)],
    "Industrial": [("Dock levellers, seals and shelters", "Equipment", "11 13 00", 0.018, 22),
                   ("Storage racking system", "Equipment", "10 56 00", 0.030, 26)],
    "Hospitality": [("Guestroom FF&E package", "Furnishings", "12 50 00", 0.060, 28)],
    "Residential": [("Unit appliance and casework package", "Equipment", "11 30 00", 0.030, 20)],
    "Mixed-Use": [("Podium transfer girders", "Structural", "05 12 00", 0.040, 36)],
    "Commercial": [("Raised access floor and cellular deck", "Interiors", "09 69 00", 0.020, 18)],
}


def procurement(spec: dict) -> list[dict]:
    hc = P.hard_cost(spec)
    start, _ = P.schedule_span(spec)
    rows = []
    items = _BASE_PACKAGES + _SECTOR_PACKAGES.get(spec["sector"], [])
    for i, (name, trade, csi, share, lead_weeks) in enumerate(items, start=1):
        est = round(hc * share, -2)
        rfq = start + dt.timedelta(days=30 * i)
        rows.append({
            "ref": f"BP-{i:03d}", "title": name,
            "state": "awarded" if i <= 2 else "draft",
            "data": {
                "name": name, "trade": trade, "csi": csi, "est_cost": est,
                "lead_time_weeks": lead_weeks, "line_count": 1,
                "rfq_due": rfq.isoformat(),
                "required_on_site": (rfq + dt.timedelta(weeks=lead_weeks)).isoformat(),
                "awarded_to": "Awarded subcontractor" if i <= 2 else None,
                "award_amount": round(est * 0.97, -2) if i <= 2 else None,
                "notes": f"{lead_weeks}-week quoted lead time; drives the procurement float on this package.",
            },
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Sheet register
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: The planned set. `issued` marks the sheets this package actually draws — the rest are registered
#: and not yet started, which is what a real register looks like at this stage.
def sheet_register(spec: dict) -> list[dict]:
    disc = spec["sector"]
    sheets: list[tuple[str, str, str, bool]] = [
        ("G0.01", "Cover Sheet and Project Data", "General", True),
        ("G0.02", "Drawing Index and Sheet Register", "General", False),
        ("G0.03", "Code Analysis and Egress Summary", "General", False),
        ("C1.01", "Site Plan and Civil Layout", "Civil", False),
        ("C2.01", "Grading and Drainage Plan", "Civil", False),
        ("A1.01", "Overall Floor Plan — Level 1", "Architectural", True),
        ("A1.02", "Overall Floor Plan — Typical Level", "Architectural", False),
        ("A2.01", "Building Elevations", "Architectural", True),
        ("A3.01", "Building Sections", "Architectural", False),
        ("A5.01", "Enlarged Plans and Core Details", "Architectural", False),
        ("A7.01", "Wall Types and Assemblies", "Architectural", False),
        ("S1.01", "Foundation Plan", "Structural", False),
        ("S2.01", "Framing Plan — Typical Level", "Structural", True),
        ("S5.01", "Typical Connection Details", "Structural", False),
        ("M2.01", "HVAC Plan — Typical Level", "Mechanical", False),
        ("M5.01", "Mechanical Schedules", "Mechanical", False),
        ("P2.01", "Plumbing Plan — Typical Level", "Plumbing", False),
        ("E2.01", "Power and Lighting Plan", "Electrical", True),
        ("E5.01", "Single Line Diagram", "Electrical", False),
        ("FP2.01", "Fire Protection Plan", "Fire Protection", False),
    ]
    if disc == "Data Center":
        sheets += [("E6.01", "Electrical Room Layouts and Busway", "Electrical", False),
                   ("M6.01", "Cooling Distribution and CRAH Layout", "Mechanical", False)]
    elif disc == "Healthcare":
        sheets += [("A6.01", "Operating Room Enlarged Plans", "Architectural", False),
                   ("P6.01", "Medical Gas Distribution", "Plumbing", False)]
    elif disc == "Industrial":
        sheets += [("A4.01", "Dock Elevation and Equipment Schedule", "Architectural", False)]
    elif disc == "Aviation":
        sheets += [("AV1.01", "Apron and Gate Layout", "Aviation", False)]
    return [{"number": n, "title": t, "discipline": d, "issued": iss} for n, t, d, iss in sheets]


def drawing_set(spec: dict) -> dict:
    _, finish = P.schedule_span(spec)
    issue = P.START - dt.timedelta(days=60)
    return {
        "ref": "SET-001", "title": "Design Development Set", "state": "draft",
        "data": {
            "name": "Design Development Set", "discipline": "All disciplines",
            "set_type": "Design Development", "issue_date": issue.isoformat(),
            "purpose": "Coordination and control-budget basis. NOT FOR CONSTRUCTION.",
        },
    }


def drawings(spec: dict, set_id: str) -> list[dict]:
    issue = P.START - dt.timedelta(days=60)
    rows = []
    for i, s in enumerate(sheet_register(spec), start=1):
        rows.append({
            "ref": f"DWG-{i:03d}", "title": s["number"],
            "state": "open",
            "issued": s["issued"],
            "data": {
                "number": s["number"], "sheet_number": s["number"], "title": s["title"],
                "discipline": s["discipline"],
                "revision": "A" if s["issued"] else "-",
                "purpose": "Design development coordination" if s["issued"] else "Not yet started",
                "lifecycle": "Issued" if s["issued"] else "Not Issued",
                "issued_date": issue.isoformat() if s["issued"] else None,
                "status": "Issued" if s["issued"] else "Not Issued",
                "drawing_set": set_id,
            },
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Documents and the estimate
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def documents(spec: dict) -> list[dict]:
    items = [
        ("Executive Report", "Report", "The project in prose: programme, cost, schedule, returns."),
        ("Basis of Design", "Specification", "Design criteria and system selections by discipline."),
        ("Outline Specification", "Specification", "Division-level outline specification."),
        ("Geotechnical Report", "Report", "Subsurface investigation and foundation recommendations."),
        ("Cost Plan Narrative", "Report", "Assumptions, exclusions and allowances behind the budget."),
        ("BIM Execution Plan", "Plan", "Model uses, LOD by discipline, federation and exchange."),
        ("Commissioning Plan", "Plan", "Systems to be commissioned and the acceptance criteria."),
    ]
    return [{"ref": f"DOC-{i:03d}", "title": n, "state": "open",
             "data": {"name": n, "document_type": t, "description": d,
                      "revision": "A", "status": "Issued"}}
            for i, (n, t, d) in enumerate(items, start=1)]


def estimate(spec: dict) -> dict:
    bt = P.budget_totals(spec)
    return {
        "ref": "EST-001", "title": "Design development control estimate", "state": "open",
        "data": {
            "name": "Design development control estimate",
            "basis": "Design Development",
            "method": "Elemental, CSI MasterFormat division level",
            "total": bt["revised"],
            "cost_per_sf": round(bt["revised"] / spec["gross_sf"], 2),
            "gross_sf": spec["gross_sf"],
            "contingency_pct": 5.0,
            "notes": "Derived from the same division mix as the control budget; see the budget CSV.",
        },
    }


def scenario(spec: dict) -> dict:
    """The pro forma, stored as a solved scenario rather than only as a document."""
    pf = P.proforma(spec)
    return {
        "name": "Base case development pro forma",
        "assumptions": {
            "gross_sf": pf["gross_sf"], "net_rentable_sf": pf["nra"],
            "hard_cost_psf": spec["finance"]["hard_cost_psf"],
            "soft_cost_pct": spec["finance"]["soft_cost_pct"],
            "land": spec["finance"]["land"],
            "exit_cap": spec["finance"]["exit_cap"],
            "loan_to_cost": spec["finance"]["ltc"],
            "interest_rate": spec["finance"]["rate"],
            "construction_months": spec["finance"]["months"],
            "hold_years": pf["hold_years"],
        },
        "result": {
            "total_development_cost": pf["total_cost"],
            "cost_per_sf": pf["cost_psf"],
            "net_operating_income": pf["noi"],
            "stabilized_value": pf["stabilized_value"],
            "yield_on_cost": pf["yield_on_cost"],
            "development_profit": pf["profit"],
            "unlevered_irr": pf["unlevered_irr"],
            "levered_irr": pf["levered_irr"],
            "equity_multiple": pf["equity_multiple"],
        },
        "provenance": "Computed by tools/projectdata.py from tools/sectors.py. Synthetic sample "
                      "project — plausible and internally consistent, not market data.",
    }

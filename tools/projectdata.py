"""Derive a project's commercial data from its sector definition.

Budget, schedule of values, CPM schedule, space program and pro forma all come from the same few
inputs in `sectors.py`, so the numbers tie out to each other rather than being three unrelated
inventions that happen to sit in one container. The executive report then reads *these* structures,
not a second set of figures — a report that restates numbers it did not compute is how a package
starts disagreeing with itself.

The figures are plausible and internally consistent. They are not market data: these are synthetic
sample projects, and the README says so where a reader will see it.
"""
from __future__ import annotations

import datetime as dt

# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Cost breakdown — CSI MasterFormat divisions, weighted by sector
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: division code -> label. Kept in the order an estimate is read.
DIVISIONS = [
    ("01", "General Requirements"),
    ("02", "Existing Conditions"),
    ("03", "Concrete"),
    ("04", "Masonry"),
    ("05", "Metals"),
    ("06", "Wood, Plastics & Composites"),
    ("07", "Thermal & Moisture Protection"),
    ("08", "Openings"),
    ("09", "Finishes"),
    ("10", "Specialties"),
    ("11", "Equipment"),
    ("12", "Furnishings"),
    ("14", "Conveying Equipment"),
    ("21", "Fire Suppression"),
    ("22", "Plumbing"),
    ("23", "Heating, Ventilating & Air Conditioning (HVAC)"),
    ("26", "Electrical"),
    ("27", "Communications"),
    ("28", "Electronic Safety & Security"),
    ("31", "Earthwork"),
    ("32", "Exterior Improvements"),
    ("33", "Utilities"),
]

#: Share of hard cost by division. Each column sums to 1.0 — asserted in `budget()`.
_MIX = {
    #                    01    02    03    04    05    06    07    08    09    10    11    12    14    21    22    23    26    27    28    31    32    33
    "Residential":     [.085, .010, .155, .030, .060, .105, .075, .055, .105, .015, .020, .010, .020, .015, .045, .060, .070, .010, .008, .025, .015, .007],
    "Commercial":      [.090, .010, .130, .020, .150, .010, .070, .085, .075, .012, .015, .006, .035, .018, .035, .085, .085, .015, .012, .022, .014, .006],
    "Aviation":        [.095, .015, .120, .015, .175, .008, .070, .070, .060, .015, .035, .008, .020, .020, .030, .080, .075, .025, .025, .020, .012, .007],
    "Hospitality":     [.080, .008, .140, .035, .055, .100, .070, .050, .115, .020, .025, .035, .022, .015, .050, .058, .062, .012, .010, .020, .012, .006],
    "Industrial":      [.075, .015, .225, .010, .200, .005, .105, .040, .030, .010, .020, .002, .005, .035, .020, .035, .060, .008, .010, .055, .025, .010],
    "Healthcare":      [.095, .012, .110, .020, .130, .010, .060, .060, .090, .020, .050, .010, .025, .022, .055, .095, .080, .015, .015, .015, .008, .003],
    "Mixed-Use":       [.088, .012, .165, .028, .075, .080, .072, .060, .098, .014, .018, .010, .028, .016, .044, .062, .072, .012, .009, .022, .012, .003],
    "Data Center":     [.070, .008, .105, .008, .095, .003, .050, .020, .025, .008, .075, .002, .006, .030, .018, .175, .230, .025, .020, .015, .010, .002],
}


#: Forecast-at-completion drift against the revised budget, by CSI division.
_FORECAST_DRIFT = {
    "01": 0.025,   # general conditions stretch with the schedule
    "03": 0.018,   # concrete — quantity growth off the foundation redesign
    "05": -0.008,  # steel bought out under budget
    "07": 0.011,
    "09": -0.012,  # finishes bought out under budget
    "23": 0.022,   # HVAC — the largest single overrun
    "26": 0.015,
    "31": 0.009,   # earthwork — unforeseen conditions
}


def _sf(spec: dict) -> int:
    return int(spec["gross_sf"])


def hard_cost(spec: dict) -> float:
    return _sf(spec) * float(spec["finance"]["hard_cost_psf"])


def budget(spec: dict) -> list[dict]:
    """One line per CSI division: original, revised, committed, forecast.

    Revised carries approved changes; committed is what is under contract; forecast is the
    projection at completion. They differ on purpose — a budget where all four columns match is a
    budget nobody has run a job through.
    """
    mix = _MIX[spec["sector"]]
    assert abs(sum(mix) - 1.0) < 1e-6, f"{spec['sector']} mix sums to {sum(mix)}"
    hc = hard_cost(spec)
    rows = []
    for i, ((code, label), share) in enumerate(zip(DIVISIONS, mix)):
        original = round(hc * share, -2)
        # Approved changes land on a handful of divisions, not evenly across all of them.
        bump = (0.032 if code in ("03", "23", "26") else
                0.014 if code in ("05", "07", "09") else 0.0)
        revised = round(original * (1 + bump), -2)
        committed = round(revised * (0.94 if i % 3 else 0.88), -2)
        # Forecast at completion drifts by division the way a running job does: the GC's own general
        # conditions and the two big MEP trades creep, steel and finishes buy out under. The net is a
        # small overrun, which is what a project this far along usually looks like — a forecast that
        # lands exactly on the budget is a forecast nobody has updated.
        drift = _FORECAST_DRIFT.get(code, 0.003)
        forecast = round(revised * (1 + drift), -2)
        rows.append({
            "code": f"{code}-000",
            "division": f"{code} — {label}",
            "description": label,
            "original": original,
            "revised": revised,
            "committed": committed,
            "forecast": forecast,
        })
    return rows


def budget_totals(spec: dict) -> dict:
    rows = budget(spec)
    return {k: round(sum(r[k] for r in rows), 2)
            for k in ("original", "revised", "committed", "forecast")}


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Schedule — a CPM spine, phase by phase
# ─────────────────────────────────────────────────────────────────────────────────────────────────
#: (name, trade, share of total duration, weather sensitivity, EV method)
_PHASES = [
    ("Mobilization and site logistics",      "Sitework",      0.04, "Rain / wet",   "milestone"),
    ("Mass excavation and shoring",          "Sitework",      0.07, "Rain / wet",   "units"),
    ("Foundations and below-grade",          "Concrete",      0.10, "Freeze / cold", "percent"),
    ("Superstructure",                       "Structure",     0.20, "Wind",         "units"),
    ("Building envelope",                    "Envelope",      0.15, "Wind",         "percent"),
    ("MEP rough-in",                         "MEP",           0.16, "None",         "percent"),
    ("Interior build-out",                   "Interiors",     0.13, "None",         "percent"),
    ("Finishes and fit-out",                 "Finishes",      0.08, "None",         "percent"),
    ("Commissioning and turnover",           "Commissioning", 0.07, "None",         "0-100"),
]

START = dt.date(2026, 3, 2)


def schedule(spec: dict) -> list[dict]:
    """Phase summaries plus per-level detail on the structure phase, which is the one a 4D review
    actually looks at. Dates are working-day approximations on a 5-day calendar."""
    total_days = int(spec["finance"]["months"] * 21.7)
    rows: list[dict] = []
    cursor = START
    prev_ref = None
    for i, (name, trade, share, weather, ev) in enumerate(_PHASES, start=1):
        dur = max(5, int(round(total_days * share)))
        start = cursor
        finish = start + dt.timedelta(days=int(dur * 7 / 5))
        ref = f"ACT-{i:03d}"
        rows.append({
            "ref": ref, "name": name, "wbs": f"1.{i}", "activity_type": "Summary",
            "trade": trade, "duration": dur, "start": start, "finish": finish,
            "weather_sensitivity": weather, "ev_method": ev,
            "predecessors": prev_ref or "", "crew_size": 8 + i * 2,
            "percent": 0, "location": "Whole building",
        })
        # Structure gets a task per storey — the level-by-level sequence a 4D simulation reads.
        if name == "Superstructure":
            per = max(3, dur // max(1, spec["storeys"]))
            c2 = start
            for lv in range(1, spec["storeys"] + 1):
                f2 = c2 + dt.timedelta(days=int(per * 7 / 5))
                rows.append({
                    "ref": f"ACT-{i:03d}-{lv:02d}",
                    "name": f"Level {lv} — frame, deck and pour",
                    "wbs": f"1.{i}.{lv}", "activity_type": "Task", "trade": "Structure",
                    "duration": per, "start": c2, "finish": f2,
                    "weather_sensitivity": "Wind", "ev_method": "units",
                    "predecessors": f"ACT-{i:03d}-{lv - 1:02d}" if lv > 1 else ref,
                    "crew_size": 14, "percent": 0, "location": f"Level {lv}",
                    "units_total": 1, "units_complete": 0,
                })
                c2 = f2
        cursor = finish
        prev_ref = ref
    rows.append({
        "ref": "ACT-900", "name": "Substantial completion", "wbs": "1.10",
        "activity_type": "Milestone", "trade": "Commissioning", "duration": 0,
        "start": cursor, "finish": cursor, "weather_sensitivity": "None",
        "ev_method": "milestone", "predecessors": prev_ref, "crew_size": 0,
        "percent": 0, "location": "Whole building",
    })
    return rows


def schedule_span(spec: dict) -> tuple[dt.date, dt.date]:
    rows = schedule(spec)
    return rows[0]["start"], rows[-1]["finish"]


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Schedule of values
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def sov(spec: dict) -> list[dict]:
    """A schedule of values off the budget, with the first three months billed so the pay
    application has something to tie out against."""
    rows = []
    for i, b in enumerate(budget(spec), start=1):
        value = b["revised"]
        # Early divisions have progress; later ones have not started.
        pct_prev = 0.55 if b["code"][:2] in ("01", "02", "31") else 0.18 if b["code"][:2] == "03" else 0.0
        pct_this = 0.12 if b["code"][:2] in ("01", "02", "03", "31") else 0.0
        rows.append({
            "item_no": f"{i:03d}",
            "description": b["description"],
            "scheduled_value": value,
            "completed_prev": round(value * pct_prev, 2),
            "completed_this": round(value * pct_this, 2),
            "materials_stored": round(value * 0.03, 2) if b["code"][:2] == "05" else 0.0,
            "retainage_pct": 5.0,
            "cost_code": b["code"],
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Space program
# ─────────────────────────────────────────────────────────────────────────────────────────────────
_SPACE_TYPE = {
    "Retail": "Retail", "Parking / back of house": "Parking", "Residential units": "Residential Unit",
    "Amenity + circulation": "Amenity", "Lobby + retail": "Lobby", "Office floorplates": "Office",
    "Core, MEP and service": "Circulation / Core", "Roof plant": "Mechanical",
    "Arrivals hall + baggage claim": "Lobby", "Ticketing and check-in": "Lobby",
    "Concourse + hold rooms": "Circulation / Core", "Concessions": "Retail",
    "Airline and airport ops": "Back-of-House", "Guestrooms": "Residential Unit",
    "Lobby, breakfast, meeting": "Lobby", "Back of house + laundry": "Back-of-House",
    "Circulation and MEP": "Circulation / Core", "Warehouse floor": "Back-of-House",
    "Dock and staging": "Back-of-House", "Office mezzanine": "Office",
    "Operating rooms + sterile core": "Back-of-House", "Pre-op / PACU": "Back-of-House",
    "Imaging and diagnostics": "Back-of-House", "Medical office suites": "Office",
    "Building services and MEP": "Mechanical", "Structured parking": "Parking",
    "Amenity deck + BOH": "Amenity", "Data halls (white space)": "Back-of-House",
    "Electrical rooms + UPS": "Mechanical", "Mechanical plant": "Mechanical",
    "Admin, security, MMR": "Office",
}


def space_program(spec: dict) -> list[dict]:
    rows = []
    for name, levels, area in spec["program"]:
        rows.append({
            "name": name,
            "space_type": _SPACE_TYPE.get(name, "Back-of-House"),
            "target_area_sf": area,
            "quantity": levels,
            "level": f"{levels} level(s)" if levels > 1 else "Level 1",
            "notes": f"{area:,} sf programmed across {levels} level(s).",
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Pro forma
# ─────────────────────────────────────────────────────────────────────────────────────────────────
def _irr(flows: list[float], lo: float = -0.95, hi: float = 3.0) -> float | None:
    """Bisection IRR. Returns None when the flows never cross zero — an honest 'no rate' rather
    than a number produced by extrapolating past the bracket."""
    def npv(r: float) -> float:
        return sum(cf / (1 + r) ** t for t, cf in enumerate(flows))
    if npv(lo) * npv(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo) * npv(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return round((lo + hi) / 2, 6)


def proforma(spec: dict, hold_years: int = 7) -> dict:
    """Sources and uses, stabilized NOI, and levered/unlevered returns on a `hold_years` hold."""
    f = spec["finance"]
    gsf = _sf(spec)
    nra = int(gsf * spec["efficiency"])

    # ── Uses ─────────────────────────────────────────────────────────────────────────────────────
    hc = hard_cost(spec)
    contingency = round(hc * 0.05, 2)
    soft = round((hc + contingency) * f["soft_cost_pct"], 2)
    land = float(f["land"])
    # Construction interest: average outstanding balance ≈ 55% of the loan over the build period.
    months = f["months"]
    loan_est = (hc + contingency + soft + land) * f["ltc"]
    interest = round(loan_est * 0.55 * f["rate"] * (months / 12), 2)
    total_cost = round(land + hc + contingency + soft + interest, 2)

    uses = [
        ("Land acquisition", land),
        ("Hard cost", round(hc, 2)),
        ("Hard cost contingency (5%)", contingency),
        (f"Soft cost ({f['soft_cost_pct']:.0%})", soft),
        ("Construction period interest", interest),
    ]

    # ── Sources ──────────────────────────────────────────────────────────────────────────────────
    debt = round(total_cost * f["ltc"], 2)
    equity = round(total_cost - debt, 2)
    sources = [("Construction loan", debt), ("Sponsor equity", equity)]

    # ── Stabilized operations ────────────────────────────────────────────────────────────────────
    kind = f["kind"]
    if kind == "hotel":
        keys = spec["units"]
        rooms_revenue = keys * 365 * f["adr"] * f["occupancy"]
        revenue = round(rooms_revenue * 1.18, 2)          # F&B and other departments
        opex = round(revenue * f["opex_ratio"], 2)
        noi = round(revenue - opex, 2)
        basis = [("Keys", keys), ("ADR", f["adr"]), ("Occupancy", f["occupancy"]),
                 ("RevPAR", round(f["adr"] * f["occupancy"], 2))]
    elif spec["key"] == "northbridge_data_hall":
        kw = spec["units"] * 1000
        revenue = round(kw * f["rent_per_kw_month"] * 12 * (1 - f["vacancy"]), 2)
        opex = round(revenue * f["opex_ratio"], 2)
        noi = round(revenue - opex, 2)
        basis = [("IT load (kW)", kw), ("Rent per kW / month", f["rent_per_kw_month"]),
                 ("Vacancy", f["vacancy"]), ("Opex ratio", f["opex_ratio"])]
    elif kind == "public":
        revenue = opex = noi = 0.0
        basis = [("Delivery", "Publicly funded — no rent roll"),
                 ("Annual operating cost", round(gsf * f["opex_psf_yr"], 2))]
    else:
        gross_rent = nra * f["rent_psf_yr"]
        revenue = round(gross_rent * (1 - f["vacancy"]), 2)
        gross_opex = round(nra * f["opex_psf_yr"], 2)
        # Under a triple-net lease the operating expense is recovered from the tenants, so it does
        # not reduce NOI. Reporting it as a deduction would understate a NNN asset by its entire
        # recovery — the number is shown in the basis instead of being silently dropped.
        nnn = f.get("opex_mode") == "nnn"
        opex = 0.0 if nnn else gross_opex
        noi = round(revenue - opex, 2)
        basis = [("Net rentable area (sf)", nra), ("Rent $/sf/yr", f["rent_psf_yr"]),
                 ("Vacancy", f["vacancy"]), ("Opex $/sf/yr", f["opex_psf_yr"])]
        if nnn:
            basis.append(("Lease structure", f"Triple net — ${gross_opex:,.0f}/yr recovered"))

    # ── Value and returns ────────────────────────────────────────────────────────────────────────
    if kind == "public" or not f["exit_cap"]:
        return {
            "kind": kind, "gross_sf": gsf, "nra": nra, "uses": uses, "sources": sources,
            "total_cost": total_cost, "cost_psf": round(total_cost / gsf, 2),
            "basis": basis, "revenue": revenue, "opex": opex, "noi": noi,
            "stabilized_value": None, "yield_on_cost": None, "profit": None,
            "unlevered_irr": None, "levered_irr": None, "equity_multiple": None,
            "hold_years": hold_years,
            "note": "Publicly funded asset — underwritten to a funding plan and a lifecycle "
                    "operating cost, not to a capitalised exit. Return metrics are omitted rather "
                    "than fabricated from a cap rate that does not apply.",
        }

    value = round(noi / f["exit_cap"], 2)
    yoc = round(noi / total_cost, 6)
    profit = round(value - total_cost, 2)

    # Cash flows: equity out at t0, NOI growing 2.75%/yr, sale at exit net of 1.5% cost.
    growth = 1.0275
    unlev = [-total_cost] + [round(noi * growth ** t, 2) for t in range(1, hold_years)]
    exit_noi = noi * growth ** hold_years
    unlev.append(round(noi * growth ** (hold_years - 1) + (exit_noi / f["exit_cap"]) * 0.985, 2))

    debt_service = round(debt * (f["rate"] + 0.017), 2)     # interest-only plus amortisation reserve
    lev = [-equity] + [round(noi * growth ** t - debt_service, 2) for t in range(1, hold_years)]
    lev.append(round(noi * growth ** (hold_years - 1) - debt_service
                     + (exit_noi / f["exit_cap"]) * 0.985 - debt, 2))

    return {
        "kind": kind, "gross_sf": gsf, "nra": nra, "uses": uses, "sources": sources,
        "total_cost": total_cost, "cost_psf": round(total_cost / gsf, 2),
        "basis": basis, "revenue": revenue, "opex": opex, "noi": noi,
        "stabilized_value": value, "yield_on_cost": yoc, "profit": profit,
        "spread_bps": round((yoc - f["exit_cap"]) * 10000, 0),
        "unlevered_irr": _irr(unlev), "levered_irr": _irr(lev),
        "equity_multiple": round(sum(c for c in lev[1:]) / equity, 3) if equity else None,
        "hold_years": hold_years, "debt": debt, "equity": equity,
        "unlevered_flows": unlev, "levered_flows": lev,
        "note": None,
    }

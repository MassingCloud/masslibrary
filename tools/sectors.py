"""Sector definitions for the Massing sample library.

One dict per sample building. Everything downstream — geometry, space program, budget, schedule and
pro forma — is derived from these, so a new sector is a data entry rather than a new code path.

Dimensions are metric (metres) because IFC is; the companion documents report imperial alongside,
because the North American cost and leasing conventions these samples model are quoted that way.

`lod` is stated per sector and is *claimed honestly*: geometry authored at 350/400 with the
fabrication-level layer (connections, rebar cages, MEP fittings) present, plus the field-verified
as-built stamp (`verify_asbuilt` / `record_asbuilt_dimension` / `set_manufacturer_info`) that the
BIMForum spec actually means by 500. A sector that does not carry the verification layer says 400.
"""
from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Structural systems. `bay` is the design grid in metres.
# ─────────────────────────────────────────────────────────────────────────────────────────────────
STEEL = "steel"
CONCRETE = "concrete"


SECTORS: list[dict] = [
    # ── Residential ──────────────────────────────────────────────────────────────────────────────
    {
        "key": "harborview_residences",
        "name": "Harborview Residences",
        "sector": "Residential",
        "subtype": "Multifamily mid-rise, Type IIIA over Type IA podium",
        "summary": "A 96-unit market-rate apartment building on a half-block infill site: five "
                   "wood-framed residential levels over a concrete podium holding structured "
                   "parking and 6,400 sf of ground-floor retail.",
        "structure": CONCRETE,
        "storeys": 6,
        "storey_height": 3.05,
        "footprint": (70.0, 26.1),
        "bay": (7.6, 8.7),
        "envelope": "punched",          # punched openings in a rainscreen wall
        "wall_thickness": 0.25,
        "slab_thickness": 0.20,
        "rooms_per_storey": 12,
        "lod": "400 + field-verified (500) on podium structure and MEP risers",
        "units": 96,
        "gross_sf": 118_200,
        "efficiency": 0.84,             # net rentable / gross
        "program": [
            ("Retail",            1, 6_400),
            ("Parking / back of house", 1, 14_200),
            ("Residential units", 5, 79_600),
            ("Amenity + circulation", 5, 18_000),
        ],
        "finance": {
            "kind": "rental",
            "hard_cost_psf": 215.0,
            "soft_cost_pct": 0.22,
            "land": 2_800_000,
            "rent_psf_yr": 38.40,       # per net rentable sf
            "opex_psf_yr": 11.85,
            "opex_mode": "psf",
            "vacancy": 0.06,
            "exit_cap": 0.0525,
            "ltc": 0.62,
            "rate": 0.0685,
            "months": 26,
        },
    },
    # ── Commercial ───────────────────────────────────────────────────────────────────────────────
    {
        "key": "meridian_commerce_center",
        "name": "Meridian Commerce Center",
        "sector": "Commercial",
        "subtype": "Speculative office tower, core and shell",
        "summary": "A twelve-storey steel-framed speculative office building with a unitised "
                   "curtain wall, delivered core-and-shell with one spec suite fitted on Level 3.",
        "structure": STEEL,
        "storeys": 12,
        "storey_height": 4.0,
        "footprint": (52.0, 39.9),      # ≈22,300 sf floorplate — a typical mid-rise office plate
        "bay": (9.14, 10.16),           # 30 ft × 33 ft 4 in
        "envelope": "curtainwall",
        "wall_thickness": 0.20,
        "slab_thickness": 0.15,
        "rooms_per_storey": 9,
        "lod": "400 on frame and connections + field-verified (500) on the core",
        "units": 0,
        "gross_sf": 268_000,
        "efficiency": 0.87,
        "program": [
            ("Lobby + retail",        1, 11_500),
            ("Office floorplates",   10, 218_000),
            ("Core, MEP and service", 12, 30_500),
            ("Roof plant",            1, 8_000),
        ],
        "finance": {
            "kind": "rental",
            "hard_cost_psf": 240.0,
            "soft_cost_pct": 0.24,
            "land": 9_000_000,
            "rent_psf_yr": 54.00,
            "opex_psf_yr": 16.00,
            "opex_mode": "psf",
            "vacancy": 0.11,
            "exit_cap": 0.0675,
            "ltc": 0.58,
            "rate": 0.0725,
            "months": 34,
        },
    },
    # ── Aviation ─────────────────────────────────────────────────────────────────────────────────
    {
        "key": "cascade_regional_terminal",
        "name": "Cascade Regional Terminal",
        "sector": "Aviation",
        "subtype": "Regional airport passenger terminal and concourse",
        "summary": "A two-level regional terminal for 1.8 million annual passengers: a long-span "
                   "steel concourse with eight contact gates over a ground-level baggage and "
                   "arrivals hall.",
        "structure": STEEL,
        "storeys": 2,
        "storey_height": 6.5,
        "footprint": (200.0, 62.0),     # a long, shallow concourse — 656 ft × 203 ft
        "bay": (12.2, 17.0),            # 40 ft transverse, long-span roof trusses
        "envelope": "curtainwall",
        "wall_thickness": 0.30,
        "slab_thickness": 0.25,
        "rooms_per_storey": 12,
        "lod": "400 on long-span steel and baggage system + field-verified (500) on gate structure",
        "units": 8,                     # contact gates
        "gross_sf": 266_900,
        "efficiency": 0.72,
        "program": [
            ("Arrivals hall + baggage claim", 1, 62_000),
            ("Ticketing and check-in",        1, 38_000),
            ("Concourse + hold rooms",        2, 96_000),
            ("Concessions",                   2, 21_900),
            ("Airline and airport ops",       2, 49_000),
        ],
        "finance": {
            "kind": "public",           # no rent roll — funded, not underwritten to an exit
            "hard_cost_psf": 486.0,
            "soft_cost_pct": 0.28,
            "land": 0,                  # airport authority land, already owned
            "rent_psf_yr": 0.0,
            "opex_psf_yr": 21.60,
            "vacancy": 0.0,
            "exit_cap": 0.0,
            "ltc": 0.0,                 # AIP grant + PFC + GARB
            "rate": 0.0435,
            "months": 40,
        },
    },
    # ── Hospitality ──────────────────────────────────────────────────────────────────────────────
    {
        "key": "ashgrove_select_hotel",
        "name": "Ashgrove Select Service Hotel",
        "sector": "Hospitality",
        "subtype": "Select-service hotel, 132 keys",
        "summary": "A five-storey, 132-key select-service hotel on a suburban interchange parcel, "
                   "load-bearing metal stud over a slab-on-grade ground floor.",
        "structure": CONCRETE,
        "storeys": 5,
        "storey_height": 3.2,
        "footprint": (79.0, 19.9),      # double-loaded corridor bar
        "bay": (7.6, 9.9),
        "envelope": "punched",
        "wall_thickness": 0.22,
        "slab_thickness": 0.20,
        "rooms_per_storey": 12,
        "lod": "400 on guestroom assemblies + field-verified (500) on the MEP chase stack",
        "units": 132,                   # keys
        "gross_sf": 84_600,
        "efficiency": 0.68,             # keys area / gross
        "program": [
            ("Guestrooms",             4, 52_800),
            ("Lobby, breakfast, meeting", 1, 12_400),
            ("Back of house + laundry",   1, 8_300),
            ("Circulation and MEP",       5, 11_100),
        ],
        "finance": {
            "kind": "hotel",
            "hard_cost_psf": 232.0,
            "soft_cost_pct": 0.21,
            "land": 2_750_000,
            "adr": 172.00,              # average daily rate
            "occupancy": 0.74,
            "opex_ratio": 0.62,         # of total revenue
            "opex_mode": "ratio",
            "exit_cap": 0.0850,
            "ltc": 0.60,
            "rate": 0.0775,
            "months": 22,
        },
    },
    # ── Industrial ───────────────────────────────────────────────────────────────────────────────
    {
        "key": "ironline_distribution_center",
        "name": "Ironline Distribution Center",
        "sector": "Industrial",
        "subtype": "Cross-dock distribution warehouse with attached office",
        "summary": "A 340,000 sf cross-dock distribution building: tilt-up concrete panels, 40 ft "
                   "clear height, 62 dock doors and a fitted office block at the northwest corner.",
        "structure": STEEL,
        "storeys": 1,                   # a single 40 ft clear volume
        "storey_height": 12.2,          # 40 ft clear
        "footprint": (183.0, 172.6),    # 600 ft × 566 ft
        "bay": (15.2, 17.8),            # 50 ft × 58 ft 6 in
        "envelope": "tiltup",
        "wall_thickness": 0.19,
        "slab_thickness": 0.18,
        "rooms_per_storey": 9,
        "dock_doors": 62,               # authored on the long elevation — see geometry.opening_steps
        "lod": "400 on the frame and dock equipment + field-verified (500) on the slab and racking",
        "units": 62,                    # dock doors
        "gross_sf": 340_000,
        "efficiency": 0.96,
        "program": [
            ("Warehouse floor",     1, 316_000),
            ("Dock and staging",    1, 14_000),
            ("Office mezzanine",    1, 10_000),
        ],
        "finance": {
            "kind": "rental",
            "hard_cost_psf": 92.0,
            "soft_cost_pct": 0.16,
            "land": 6_800_000,
            "rent_psf_yr": 9.85,
            "opex_psf_yr": 2.15,        # NNN — fully recovered from tenants
            "opex_mode": "nnn",
            "vacancy": 0.04,
            "exit_cap": 0.0575,
            "ltc": 0.65,
            "rate": 0.0660,
            "months": 18,
        },
    },
    # ── Healthcare ───────────────────────────────────────────────────────────────────────────────
    {
        "key": "vantage_point_asc",
        "name": "Vantage Point Ambulatory Surgery Center",
        "sector": "Healthcare",
        "subtype": "Ambulatory surgery center and medical office building",
        "summary": "A three-storey ambulatory surgery centre with four operating rooms, twelve "
                   "pre-op/PACU bays and two floors of medical office above, built to FGI "
                   "Guidelines and OSHPD-equivalent structural criteria.",
        "structure": STEEL,
        "storeys": 3,
        "storey_height": 4.6,           # deep plenum for medical MEP
        "footprint": (66.0, 45.0),
        "bay": (9.1, 11.2),
        "envelope": "punched",
        "wall_thickness": 0.24,
        "slab_thickness": 0.20,
        "rooms_per_storey": 12,
        "lod": "400 on medical MEP and OR assemblies + field-verified (500) on med-gas and OR envelope",
        "units": 4,                     # operating rooms
        "gross_sf": 95_900,
        "efficiency": 0.78,
        "program": [
            ("Operating rooms + sterile core", 1, 14_600),
            ("Pre-op / PACU",                  1, 11_200),
            ("Imaging and diagnostics",        1, 8_400),
            ("Medical office suites",          2, 46_700),
            ("Building services and MEP",      3, 15_000),
        ],
        "finance": {
            "kind": "rental",
            "hard_cost_psf": 360.0,
            "soft_cost_pct": 0.24,
            "land": 3_200_000,
            "rent_psf_yr": 74.00,
            "opex_psf_yr": 21.00,
            "opex_mode": "psf",
            "vacancy": 0.05,
            "exit_cap": 0.0625,
            "ltc": 0.60,
            "rate": 0.0710,
            "months": 28,
        },
    },
    # ── Mixed-use ────────────────────────────────────────────────────────────────────────────────
    {
        "key": "foundry_row_mixed_use",
        "name": "Foundry Row",
        "sector": "Mixed-Use",
        "subtype": "Retail podium with residential tower above",
        "summary": "A vertical mixed-use block: two levels of retail and structured parking podium "
                   "carrying an eight-storey residential tower, with a shared amenity deck at the "
                   "podium roof.",
        "structure": CONCRETE,
        "storeys": 10,
        "storey_height": 3.4,
        "footprint": (62.0, 36.9),
        "bay": (8.7, 10.3),
        "envelope": "punched",
        "wall_thickness": 0.25,
        "slab_thickness": 0.22,
        "rooms_per_storey": 12,
        "lod": "400 on podium transfer structure + field-verified (500) on transfer beams",
        "units": 142,
        "gross_sf": 246_300,
        "efficiency": 0.81,
        "program": [
            ("Retail",              2, 42_000),
            ("Structured parking",  2, 31_000),
            ("Residential units",   8, 141_300),
            ("Amenity deck + BOH",  8, 32_000),
        ],
        "finance": {
            "kind": "rental",
            "hard_cost_psf": 235.0,
            "soft_cost_pct": 0.23,
            "land": 7_200_000,
            "rent_psf_yr": 44.00,
            "opex_psf_yr": 12.50,
            "opex_mode": "psf",
            "vacancy": 0.07,
            "exit_cap": 0.0550,
            "ltc": 0.60,
            "rate": 0.0700,
            "months": 32,
        },
    },
    # ── Data centre ──────────────────────────────────────────────────────────────────────────────
    {
        "key": "northbridge_data_hall",
        "name": "Northbridge Data Hall",
        "sector": "Data Center",
        "subtype": "Single-storey colocation data hall, 12 MW IT load",
        "summary": "A 12 MW colocation building: four 3 MW data halls on a raised floor, an "
                   "electrical yard with N+1 generation, and a chilled-water plant sized for "
                   "concurrent maintainability.",
        "structure": STEEL,
        "storeys": 1,
        "storey_height": 8.5,
        "footprint": (96.0, 61.0),
        "bay": (12.2, 15.2),
        "envelope": "metalpanel",
        "wall_thickness": 0.25,
        "slab_thickness": 0.30,         # thick slab for equipment loads
        "rooms_per_storey": 4,          # a 2x2 grid — the four data halls
        "lod": "400 on electrical and mechanical plant + field-verified (500) on busway and CRAH units",
        "units": 12,                    # MW of IT load
        "gross_sf": 63_000,
        "efficiency": 0.62,             # white space / gross
        "program": [
            ("Data halls (white space)", 1, 39_000),
            ("Electrical rooms + UPS",   1, 11_400),
            ("Mechanical plant",         1, 8_600),
            ("Admin, security, MMR",     1, 4_000),
        ],
        "finance": {
            "kind": "rental",
            "hard_cost_psf": 1_450.0,   # dominated by MEP, not shell — ≈$7.6M per MW of IT load
            "soft_cost_pct": 0.19,
            "land": 7_900_000,
            "rent_psf_yr": 0.0,         # priced per kW, not per sf — see the pro forma
            "rent_per_kw_month": 125.0,
            "opex_ratio": 0.40,         # of revenue; power is largely a tenant pass-through
            "opex_mode": "ratio",
            "opex_psf_yr": 41.00,
            "vacancy": 0.05,
            "exit_cap": 0.0675,
            "ltc": 0.55,
            "rate": 0.0745,
            "months": 24,
        },
    },
]


SF_PER_M2 = 10.76391


def by_key(key: str) -> dict:
    for s in SECTORS:
        if s["key"] == key:
            return s
    raise KeyError(f"no sector {key!r}; have {[s['key'] for s in SECTORS]}")


def check(tolerance: float = 0.005) -> list[str]:
    """Assert the declared areas agree with the geometry that will be authored from them.

    `gross_sf` drives every dollar in the package — cost per square foot, rent, the whole pro forma —
    while `footprint` and `storeys` drive the model. Nothing ties the two together automatically, so
    they drifted: an early version of this file declared a 372,000 sf office and described a
    footprint that builds 173,000 sf, and the executive report happily priced the larger number
    against the smaller building. This is the check that would have caught it on the first run.

    Also verifies the space program sums to the gross area, and that `rooms_per_storey` tiles the
    plate exactly under the grid `add_spaces` picks — a remainder cell means rooms that do not add
    up to the floor they are on.
    """
    import math

    problems: list[str] = []
    for s in SECTORS:
        w, d = s["footprint"]
        modelled = w * d * s["storeys"] * SF_PER_M2
        drift = modelled / s["gross_sf"] - 1
        if abs(drift) > tolerance:
            problems.append(
                f"{s['key']}: footprint {w}x{d} over {s['storeys']} storeys builds "
                f"{modelled:,.0f} sf but gross_sf declares {s['gross_sf']:,} ({drift:+.1%})")

        programmed = sum(area for _, _, area in s["program"])
        if programmed != s["gross_sf"]:
            problems.append(
                f"{s['key']}: space program sums to {programmed:,} sf, gross_sf is "
                f"{s['gross_sf']:,}")

        n = s["rooms_per_storey"]
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)
        if cols * rows != n:
            problems.append(
                f"{s['key']}: rooms_per_storey={n} tiles as {cols}x{rows}={cols * rows}, leaving "
                f"{cols * rows - n} empty cell(s) — pick a value that fills the grid")
    return problems


if __name__ == "__main__":
    import sys
    issues = check()
    for i in issues:
        print("FAIL", i)
    print(f"{len(SECTORS)} sectors, {len(issues)} problem(s)")
    sys.exit(1 if issues else 0)

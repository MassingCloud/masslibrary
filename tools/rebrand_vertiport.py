"""Rebrand the supplied vertiport package to a synthetic identity, then repack it.

The package arrived named for a real airport in a real city, and the archive it came in was named
for a real eVTOL manufacturer. This repository is public and dedicated to the public domain, and it
carries a hard rule that no sample names a real place or party — a concept study that reads as a
named operator's project at a named airport is exactly the thing that rule exists to prevent.

Nothing about the engineering changes. The FAA references, the EB 105A geometry formulas, the design
basis, the registers and the sheets are the reason the package is worth including; only the identity
is replaced. Substitutions are applied to every text payload in the container — `project.json`, each
`data/*.json`, the executive report and all five SVG title blocks — and then the container is written
back through the same ZIP structure it arrived in.

    python tools/rebrand_vertiport.py <source.mass> --sheets <dir> --report <file> --out samples/aviation
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import zipfile

#: Ordered longest-first so a broad pattern cannot eat a narrow one before it matches.
SUBSTITUTIONS: list[tuple[str, str]] = [
    ("Sky Harbor North Vertiport - Hybrid Heliport/Vertiport",
     "Cedar Reach North Vertiport - Hybrid Heliport/Vertiport"),
    ("Sky Harbor North Vertiport", "Cedar Reach North Vertiport"),
    ("SKY HARBOR NORTH VERTIPORT", "CEDAR REACH NORTH VERTIPORT"),
    ("sky_harbor_north_vertiport", "cedar_reach_north_vertiport"),
    ("Sky Harbor", "Cedar Reach"),
    ("SKY HARBOR", "CEDAR REACH"),
    ("Phoenix, AZ", "Cedar Reach, State"),
    ("PHOENIX, AZ", "CEDAR REACH, STATE"),
    # The projected CRS names the real state plane zone, which locates the project as surely as the
    # city does. Replaced with a stated-fictional grid rather than another real zone.
    ("NAD83 AZ Central / NAVD88", "NAD83 Sample Grid / NAVD88"),
    ("NAD83 AZ Central", "NAD83 Sample Grid"),
    ("AZ Central", "Sample Grid"),
    ("Phoenix", "Cedar Reach"),
    ("PHOENIX", "CEDAR REACH"),
    ("Archer", "Sample Aircraft"),
    ("ARCHER", "SAMPLE AIRCRAFT"),
    ("archer", "sample_aircraft"),
]

TEXT_SUFFIXES = (".json", ".md", ".svg", ".txt", ".csv")


def scrub(text: str) -> tuple[str, int]:
    n = 0
    for old, new in SUBSTITUTIONS:
        if old in text:
            n += text.count(old)
            text = text.replace(old, new)
    return text, n


def audit(text: str) -> list[str]:
    """Anything that still reads like a real place or party after substitution."""
    patterns = [r"Sky\s*Harbor", r"Phoenix", r"\bArcher\b", r"\bAZ\b", r"Arizona"]
    return [p for p in patterns if re.search(p, text, re.I)]


def _make_frag(ifc_bytes: bytes) -> bytes | None:
    """Convert the container's source IFC to a Fragments tile.

    The package arrived without one, so nothing in it renders — the viewer reads `model.frag`, and
    `has_frag: false` means a sample that opens to an empty canvas. The tile is derived from the IFC
    that is already inside the container, so this adds no new information, only a pre-converted view
    of what is there.
    """
    import subprocess
    import tempfile
    mm = os.environ.get("MASSING_SRC", r"C:\Server\modelmaker")
    cli = os.path.join(mm, "services", "converter", "src", "cli.mjs")
    if not os.path.exists(cli):
        print(f"  ! converter not found at {cli} — container will ship without model.frag")
        return None
    with tempfile.TemporaryDirectory() as td:
        ifc_p = os.path.join(td, "source.ifc")
        frag_p = os.path.join(td, "model.frag")
        with open(ifc_p, "wb") as fh:
            fh.write(ifc_bytes)
        r = subprocess.run(["node", cli, ifc_p, frag_p], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(frag_p):
            print(f"  ! ifc2frag failed: {(r.stderr or r.stdout)[:200]}")
            return None
        with open(frag_p, "rb") as fh:
            return fh.read()


def rebrand(src: str, out_dir: str, sheet_dir: str | None, report_path: str | None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    out_name = "cedar_reach_north_vertiport.mass"
    out_path = os.path.join(out_dir, out_name)

    changed = 0
    leftovers: dict[str, list[str]] = {}
    payload: dict[str, bytes] = {}

    with zipfile.ZipFile(src) as zin:
        for info in zin.infolist():
            data = zin.read(info.filename)
            name, _ = scrub(info.filename)
            if info.filename.lower().endswith(TEXT_SUFFIXES):
                text = data.decode("utf-8")
                text, n = scrub(text)
                changed += n
                remaining = audit(text)
                if remaining:
                    leftovers[info.filename] = remaining
                data = text.encode("utf-8")
            payload[name] = data

    if leftovers:
        raise SystemExit(f"rebrand incomplete — real-world references survive: {leftovers}")

    # Give it a renderable geometry tile if it has none.
    if "geometry/model.frag" not in payload:
        ifc_name = next((n for n in payload if n.startswith("geometry/") and n.endswith(".ifc")), None)
        if ifc_name:
            frag = _make_frag(payload[ifc_name])
            if frag:
                payload["geometry/model.frag"] = frag
                print(f"  generated geometry/model.frag ({len(frag) / 1e3:.0f} KB) from {ifc_name}")

    # Rebuild the manifest. Substituting text changed byte lengths, so the inventory the container
    # ships — the thing that lets a reader check what arrived against what was sent — no longer
    # described its own contents. An inventory that is wrong is worse than none: it reads as a
    # verification and is not one.
    man = json.loads(payload["manifest.json"])
    man["project"] = {**man.get("project", {}),
                      "name": scrub(man.get("project", {}).get("name", ""))[0]}
    man["has_frag"] = "geometry/model.frag" in payload
    man["entries"] = sorted(
        ({"path": p, "bytes": len(b)} for p, b in payload.items() if p != "manifest.json"),
        key=lambda e: str(e["path"]))
    man["rebranded"] = {
        "by": "tools/rebrand_vertiport.py",
        "why": "The source package named a real airport, city and aircraft manufacturer. This "
               "repository is public and CC0, and no sample in it may name a real place or party. "
               "Only the identity was replaced; the engineering, registers and sheets are unchanged.",
    }
    payload["manifest.json"] = json.dumps(man, indent=2).encode("utf-8")

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in sorted(payload):
            zout.writestr(name, payload[name])

    # The loose sheets and report beside the container get the same treatment, so the two copies
    # cannot disagree about what the project is called.
    written = [out_path]
    if sheet_dir and os.path.isdir(sheet_dir):
        dest = os.path.join(out_dir, "cedar_reach_north_vertiport-sheets")
        os.makedirs(dest, exist_ok=True)
        for fn in sorted(os.listdir(sheet_dir)):
            if not fn.lower().endswith(".svg"):
                continue
            with open(os.path.join(sheet_dir, fn), encoding="utf-8") as fh:
                text, n = scrub(fh.read())
            changed += n
            if audit(text):
                raise SystemExit(f"rebrand incomplete in sheet {fn}: {audit(text)}")
            new_fn, _ = scrub(fn)
            p = os.path.join(dest, new_fn)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
            written.append(p)

    if report_path and os.path.exists(report_path):
        with open(report_path, encoding="utf-8") as fh:
            text, n = scrub(fh.read())
        changed += n
        if audit(text):
            raise SystemExit(f"rebrand incomplete in report: {audit(text)}")
        p = os.path.join(out_dir, "cedar_reach_north_vertiport-executive-report.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(p)

    print(f"rebranded {src}")
    print(f"  {changed} substitution(s) across the package")
    for p in written:
        print(f"  wrote {os.path.relpath(p)}  ({os.path.getsize(p) / 1e3:.0f} KB)")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="the supplied .mass")
    ap.add_argument("--sheets", default=None, help="directory of loose SVG sheets")
    ap.add_argument("--report", default=None, help="loose executive report markdown")
    ap.add_argument("--out", default="samples/aviation")
    args = ap.parse_args()
    rebrand(args.source, args.out, args.sheets, args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

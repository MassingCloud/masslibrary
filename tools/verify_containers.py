"""Verify every `.mass` in the library. Pure standard library — no Massing, no ifcopenshell, no deps.

Point of this file: a `.mass` is documented as a plain ZIP of JSON plus IFC, and a claim like that is
worth only as much as somebody's ability to check it without the software that wrote it. So this
checks the containers the way an outsider would.

    python tools/verify_containers.py
    python tools/verify_containers.py --json

Exit code 1 if any container fails.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(ROOT, "samples")

REQUIRED = ("manifest.json", "README.txt", "project.json", "index/props.json")


def check(path: str) -> dict:
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    errors: list[str] = []
    warnings: list[str] = []
    info: dict = {"container": rel, "bytes": os.path.getsize(path)}

    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        return {**info, "ok": False, "errors": [".mass is documented as a ZIP and this is not one"],
                "warnings": []}

    with z:
        bad = z.testzip()
        if bad is not None:
            errors.append(f"corrupt entry: {bad}")
        names = set(z.namelist())

        for req in REQUIRED:
            if req not in names:
                errors.append(f"missing {req}")

        if not any(n.startswith("geometry/") and n.endswith(".ifc") for n in names):
            errors.append("no source IFC under geometry/ — the container has no model of record")
        if "geometry/model.frag" not in names:
            warnings.append("no geometry/model.frag — nothing will render without reconverting")

        man = {}
        if "manifest.json" in names:
            try:
                man = json.loads(z.read("manifest.json"))
            except ValueError as e:
                errors.append(f"manifest.json is not readable JSON: {e}")

        if man:
            info["format"] = man.get("format")
            info["version"] = man.get("version")
            info["project"] = (man.get("project") or {}).get("name")
            if man.get("format") != "massing.project":
                errors.append(f"unexpected format {man.get('format')!r}")

            # The manifest carries an entry inventory. Its whole purpose is to let a reader check
            # what arrived against what was meant to be sent, so check it.
            declared = {e["path"]: e["bytes"] for e in (man.get("entries") or [])}
            actual = {i.filename: i.file_size for i in z.infolist()}
            for p, b in declared.items():
                if p not in actual:
                    errors.append(f"manifest lists {p} but the archive does not contain it")
                elif actual[p] != b:
                    errors.append(f"{p}: manifest says {b} bytes, archive has {actual[p]}")
            # manifest.json cannot describe its own final size, so it is legitimately absent
            undeclared = set(actual) - set(declared) - {"manifest.json"}
            if undeclared:
                warnings.append(f"in the archive but not the manifest: {sorted(undeclared)}")

            if not man.get("excluded", {}).get("tables"):
                warnings.append("manifest does not state what was excluded")

        # The element index — the difference between a project and a mesh.
        if "index/props.json" in names:
            try:
                idx = json.loads(z.read("index/props.json"))
                els = idx.get("elements") or []
                info["elements"] = len(els)
                if not els:
                    errors.append("element index is empty — the model cannot be queried")
                declared_n = (man.get("tables") or {}).get("element")
                if declared_n is not None and declared_n != len(els):
                    errors.append(f"manifest says {declared_n} elements, index has {len(els)}")
                if els and not all(e.get("guid") for e in els):
                    errors.append("some indexed elements have no GlobalId")
            except ValueError as e:
                errors.append(f"index/props.json is not readable JSON: {e}")

        # Every data/<table>.json must be a JSON array of objects.
        tables = 0
        rows = 0
        for n in sorted(names):
            if not (n.startswith("data/") and n.endswith(".json")):
                continue
            tables += 1
            try:
                payload = json.loads(z.read(n))
            except ValueError as e:
                errors.append(f"{n} is not readable JSON: {e}")
                continue
            if not isinstance(payload, list):
                errors.append(f"{n} is not a JSON array")
            else:
                rows += len(payload)
                if payload and not all(isinstance(r, dict) for r in payload):
                    errors.append(f"{n} contains non-object rows")
        info["tables"] = tables
        info["rows"] = rows

    return {**info, "ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    paths = []
    for dirpath, _, files in os.walk(SAMPLES):
        paths += [os.path.join(dirpath, f) for f in sorted(files) if f.endswith(".mass")]
    paths.sort()

    if not paths:
        print("no .mass containers found under samples/", file=sys.stderr)
        return 1

    results = [check(p) for p in paths]
    if args.as_json:
        print(json.dumps(results, indent=2))
        return 0 if all(r["ok"] for r in results) else 1

    print(f"{'Container':<52}{'Elements':>10}{'Tables':>8}{'Rows':>8}{'Size':>10}  ")
    print("-" * 92)
    for r in results:
        mark = "ok  " if r["ok"] else "FAIL"
        print(f"{r['container']:<52}{r.get('elements', 0):>10,}{r.get('tables', 0):>8}"
              f"{r.get('rows', 0):>8,}{r['bytes'] / 1e6:>8.2f} MB  {mark}")
        for e in r["errors"]:
            print(f"    ERROR   {e}")
        for w in r["warnings"]:
            print(f"    warning {w}")

    bad = [r for r in results if not r["ok"]]
    print("-" * 92)
    print(f"{len(results)} container(s), {len(bad)} failing, "
          f"{sum(r.get('elements', 0) for r in results):,} elements, "
          f"{sum(r['bytes'] for r in results) / 1e6:.1f} MB total")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

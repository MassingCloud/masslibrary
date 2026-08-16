"""A build-time accelerator for GUID lookup. Semantics unchanged; only the search is faster.

`aec_data.edit_core._element` resolves a GlobalId by scanning every `IfcElement` in the model:

    el = next((e for e in model.by_type("IfcElement") if e.GlobalId == guid), None)

That is O(n) per lookup. The record pass stamps classification, spec links, phase and LOD stage over
*every* element, so the pass as a whole is O(n²): ~5M entity comparisons on a 2,200-element model,
and ~100M on a 10,000-element one. Measured on this library, the residential sample spent longer in
that one pass than in the other six combined, and the twelve-storey office would not have finished
in a sensible time at all.

`ifcopenshell.file.by_guid` is a hash lookup and returns the same entity. This module swaps the
former for the latter for the duration of a build.

**This changes no output.** It is a search strategy, not a behaviour change, which is the only
reason it is acceptable to apply from outside the product. Verified on the data-centre sample by
building it both ways and comparing: identical IFC class histogram and identical
(class, property-set signature) multiset across all 1,153 products, with the record pass falling
from 27.6 s to 2.4 s.

GlobalIds do differ between the two builds — but they differ between *any* two builds, because
`root.create_entity` mints a fresh UUID each time. That is a property of the authoring path, not of
this patch.

The proper fix belongs upstream in `edit_core._element`. Until it lands, this keeps the library
buildable without forking the authoring code.
"""
from __future__ import annotations

import contextlib


@contextlib.contextmanager
def fast_element_lookup():
    """Patch `_element` to a hash lookup for the duration of the block, then restore it."""
    from aec_data import edit_core

    original = edit_core._element

    def _element(model, guid: str):
        try:
            el = model.by_guid(guid)
        except (RuntimeError, KeyError):
            el = None
        if el is None:
            # Fall back to the original scan rather than inventing a different failure: an unknown
            # GUID must still raise exactly what the callers already handle.
            return original(model, guid)
        # by_guid resolves any rooted entity; the original narrowed to IfcElement, and callers rely
        # on that narrowing (a stamp aimed at an element should not land on a storey or a project).
        if not el.is_a("IfcElement"):
            raise ValueError(f"element {guid} not found")
        return el

    edit_core._element = _element
    # The leaf modules bound the name at import time, so rebinding the module attribute alone would
    # leave every real caller still pointing at the slow original.
    patched = []
    for mod_name in ("edit", "edit_asbuilt", "edit_struct", "edit_enclosure", "edit_mep",
                     "edit_annotate", "detailing", "connections", "rebar", "representations",
                     "groups", "families"):
        try:
            mod = __import__(f"aec_data.{mod_name}", fromlist=["_element"])
        except ImportError:
            continue
        if getattr(mod, "_element", None) is original:
            mod._element = _element
            patched.append(mod)
    try:
        yield len(patched) + 1
    finally:
        edit_core._element = original
        for mod in patched:
            mod._element = original

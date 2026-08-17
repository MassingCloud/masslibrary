# Authoring demo

One extra container that is not a sector sample.

## `maple_grove_house.mass`

A small single-family house — 23 elements: 7 walls, 3 slabs, a roof, 2 doors, 4 windows and their
openings, across 2 levels.

It is here because of *how* it was made, not what it is. Every element was authored **in the
browser**, through the same edit recipes a user drives, rather than imported from another tool. It
is deliberately small: it exists to prove the authoring path end to end, and a 23-element model
where every element can be accounted for proves that better than a large one.

The sector samples in this library are generated head-lessly by `tools/build_library.py`. This one
came out of the product's own UI. If the two ever disagree about what a `.mass` should contain, this
container is the one that reflects what a user's own save actually produces.

**No commercial data.** Unlike the sector samples, this carries no budget, schedule or pro forma —
it predates them and has not been backfilled, because backfilling it would make it a worse record of
what the authoring path produces on its own.

Origin: the `samples/` directory of the Massing application repository.

---

## A note on what is *not* here

The application repository also ships `riverside_school_structural.mass` — a 1,551-element
structural frame with 619 reinforcing bars across five storeys, and by some distance the most
substantial model in that library.

It is **not** copied here, and the reason is worth stating precisely, because it is further from
"openly published" than it looks. The IFC's own header records where it came from:

```
FILE_NAME('rstadvancedsampleproject.ifczip', ...,
          'Autodesk Revit 24.3.10.22 (ENU)');
```

`rstadvancedsampleproject` is the **Revit Structure Advanced Sample Project** — Autodesk's own
sample content, shipped with Revit and governed by Autodesk's licence terms. That Open redistributed
it as a test model; they did not author it, and redistribution is not a grant of rights.

So the chain is Autodesk → That Open → here, and nowhere along it does anyone acquire the right to
dedicate that geometry to the public domain. Everything in this repository is CC0. Putting a
third-party model under that dedication would be claiming an authority we do not have, and it would
be the kind of claim that is worse for being confident.

Every model in this library is therefore synthetic and generated, which is also why the sector
samples exist at all: the alternative to a licensing question is a building you made yourself.

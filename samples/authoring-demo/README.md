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

It is **not** copied here, deliberately. That model derives from the openly-published That Open
school model, so its geometry is third-party work. Everything in this repository is dedicated to the
public domain under CC0, and re-dedicating somebody else's model under CC0 is not ours to do. It
stays where its provenance is recorded.

If you want it, take it from the application repository, and check its upstream terms for your use.

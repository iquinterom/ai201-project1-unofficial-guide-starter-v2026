# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Four of my five questions have their answer stated outright in a single
paragraph of a single document, so anything below 4 of 5 would mean retrieval is
failing on the straightforward cases. I stop short of 5 because my late-dinner
question needs the opening-hours paragraph of `guide_eating.md` to survive
chunking whole, and at 26 chunks across 14 documents I expect it to be cut.

> **Revised in unit 2:** For at least 4 of 5 questions, the retrieved chunks
> include one that contains the answer as actually stated in the corpus,
> rather than matching the `expects` value I wrote for that question in
> `questions.py`.
>
> **Why revised:** 3 of my 5 `expects` values (bakery → Marchwood, best in
> winter → Brightwater, best for cycling → Givens Mill) were guesses I wrote
> in Milestone 2 before I'd carefully re-read every document, and none of them
> match what the corpus actually says (only Kestrelford's guide mentions a
> bakery at all; `guide_marchwood.md` explicitly says it's the one place that
> works in winter; cycling routes are described under Brightwater and
> `guide_regional_transport.md`, never Givens Mill). Grading retrieval against
> my own unverified guesses would measure my Milestone 2 research, not whether
> the pipeline actually finds the right chunk — and in all 5 cases, across all
> 3 runs, it did.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Every chunk reaches the model already labelled `[from <filename>]`
(`generate.py:295`), both the system instruction and the question itself ask for
the file to be named, and the relevance gate refuses before generation whenever
nothing is close enough — so there is no route to an answer with no source
behind it. Allowing even one miss would excuse the model for ignoring an
instruction it was given twice.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
Four of my five out-of-scope questions come from domains my documents never
touch — diesel engines, ibuprofen, Rust, the 1994 World Cup — so I expect those
to sit well outside the cutoff. The fifth asks for the capital of Mongolia,
which is a geography question put to a corpus of travel guides, and that is the
one I expect to land close enough to slip through.

---

## 4. Chunks follow the section headings

At least 4 of 5 chunks sampled with `python app.py chunks -n 5` begin at a `##`
section heading and carry text from that one section only.

**Why this target:**
Any chunker still has to cap length, so a section longer than that cap must be
split somewhere and the second piece legitimately will not begin at a heading —
which is the one miss I allow for. Setting it at 3 of 5 would let the current
fixed-size split pass on the chunks that happen to land on a heading by accident.



---

## 5. Conflicting documents are both surfaced

Asked "Where is the nearest full hospital?" three times, the system names both
Brightwater and Marchwood or reports that the documents disagree, on all 3 runs.

**Why this target:**
Nine town guides say the nearest full hospital is in Brightwater and
`guide_accessibility.md` says Marchwood, so picking one and stating it plainly is
the likely outcome and reads exactly as fluently as a correct answer would.
Tolerating one miss in three would tolerate the silent failure this criterion
exists to catch.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

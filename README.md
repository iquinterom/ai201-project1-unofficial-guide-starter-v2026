# The Unofficial Guide

<!-- Iris Quintero - Corpus: City Guides -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This RAG QA tool was build as a City Guide for a fictional travel destination. There are 14 documents that provide information about 9 towns, such as accessibility, eating, transporation, seasons, and best walking towns. This is a travel guide where you can ask for advice on specific towns and an overrall overview for your traveling plans. 

## Chunking Strategy

**Chunk size:**
**Overlap:**

The city guides corpus is 14 documents long, 958 charcters, ~2098 character per document; the chunk number is 51, but the output got sliced at 800 characters where it cut off mid sentence. Since the documents already produces ## headings, the chunker got changed to split on the headings ## instead of counting characters.  This new enhancement provides exactly that section to the real content. 

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_accessibility.md#0 ` — produced by: `chunker.py::split_documents`

```======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 3** — source: `guide_givens_mill.md#2 ` — produced by: chunker.py::split_documents``

```======================================================================
Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
======================================================================
## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```======================================================================
Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
======================================================================
## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.

```

**Chunk 5** — source:  `guide_pellew_sands.md#6:` — produced by: `chunker.py::split_documents`

```======================================================================
Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
======================================================================
## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
Which town is easiest to get around when you have limited accessibility?
**Answer:**

```Thornby Wells is the easiest town in the region for accessibility, as it is
flat, compact, and everything is within three minutes of everything else.
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| which town is eeasies to get around when you have limited accessibility? | yes | 0.503 |
| Which town is better to visit in the winter?| yes |	0.502 |
|Which town has a sea front? | yes | 	0.527 |
| Which town has the best bakery?| yes | 0.578 |
| Where will be better to go cycling? | yes | 0.602 |
| What is the capital of Mongolia? |  no | 0.803 |
| Who won the 1994 World Cup? | no | 	0.975 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.846 |
| How do I write a for loop in Rust? | no|0.813 |
| How do I change the oil in a diesel engine? | no | 	0.892 |


## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I asked claude to help me with the function on the chunker.py, where the retrievals where cutting off because of the 800 characters. Once every thing igot fix the whoel documents reads directly full headding section. 
**2.**
For the relevant cutoff, i ran all 5 of my test questions and the 5 out of scope questions. I provided with the 10 results to Claude, and it helped explained what I was looking for and why these steps where necessary. 

**3.**
In Unit 2, I gave Claude my run results and asked it to argue that each of my MET verdicts was actually wrong, as strongly as it could. For criterion 1, it pointed out that 3 of my 5 `expects` values in `questions.py` (bakery, winter, cycling) didn't actually match what the corpus says — I'd written them before carefully re-reading every document. I decided to record that as a real MISSED verdict and diagnose it as a bad test oracle, rather than quietly revising the criterion to hide it.

**4.**
For Milestone 4's fix, Claude first suggested tightening `generate.py`'s `GROUNDING_INSTRUCTION` to stop a wording drift it had found in one of my criterion 5 runs. I told it that instruction is fixed by the course and I can't edit it. It pivoted to recommending a second chunking strategy instead (splitting on paragraphs instead of `##` headings), built it as a separate function and a separate index variant so my original chunker stayed untouched, then ran the full test suite against both. The paragraph strategy actually made things worse (criteria 1 and 4 both regressed), so I kept my original heading-based chunker rather than switching.

**5.**
From a class reference screenshot, I asked Claude to build `scorer.py` (`_normalize`, `_contains_phrase`, `judge`) matching the interface `run_eval.py::load_scorer` already expects. It wrote it and smoke-tested it before handing it back. When I ran it myself against my real questions, it marked 2 of my 5 as fail instead of the 5/5 I expected — turned out two of my `expects` values had typos ("Thorny Wells", "Peller Sands") I'd read past without noticing. I fixed them; all 5 pass now.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 2/5 | 2/5 | 2/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks follow the section headings | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Conflicting documents are both surfaced | 3 of 3 | pass | pass | pass | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Criterion 1** — produced by: `run_eval.py::main` → `store.py::search`, `chunker.py::split_documents`

Pass example — matches my `expects` value in `questions.py`:

```
Which town is easiest to get around when you have limited accessibility? — run 1

Best distance: 0.5078 (passed the gate)
Sources retrieved: guide_accessibility.md, guide_corry_vale.md, guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md

Thornby Wells is the easiest town in the region for accessibility.

Source: guide_accessibility.md
```

Miss example — my `expects` value said "Marchwood," but the retrieved chunks and answer say Kestrelford instead:

```
Which town has the best bakery? — run 1

Best distance: 0.5783 (passed the gate)
Sources retrieved: guide_corry_vale.md, guide_eating.md, guide_kestrelford.md, guide_thornby_wells.md

Based on the provided documents, Kestrelford has a bakery that sells out by 11am and is the reason many people return or come back.

Sources: `guide_kestrelford.md` and `guide_eating.md`
```

**Criterion 2** — produced by: `run_eval.py::main` → `generate.py::answer_from_chunks`

```
Which town has a sea front? — run 1

Best distance: 0.5274 (passed the gate)
Sources retrieved: guide_accessibility.md, guide_eating.md, guide_halden_bay.md, guide_pellew_sands.md

Pellew Sands has a seafront, as mentioned in `guide_eating.md`, `guide_pellew_sands.md`, and `guide_accessibility.md`. Halden Bay also has a harbour front / seafront, according to `guide_eating.md` and `guide_halden_bay.md`.
```

**Criterion 3** — produced by: `run_eval.py::check_out_of_scope` → `gate.py::check`

```
What is the capital of Mongolia? | Best distance: 0.803 | Gate: refused
How do I change the oil in a diesel engine? | Best distance: 0.892 | Gate: refused
Who won the 1994 World Cup? | Best distance: 0.975 | Gate: refused
What is the recommended dosage of ibuprofen for a headache? | Best distance: 0.846 | Gate: refused
How do I write a for loop in Rust? | Best distance: 0.813 | Gate: refused

-> gate refused 5 of 5
```

**Criterion 4** — produced by: `chunker.py::split_documents`, printed via `app.py::cmd_chunks`

```
Chunk 2 | source: guide_corry_vale.md#5 | produced by: chunker.py::split_documents

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

The one exception out of 5 is `guide_accessibility.md#0`, which begins with the document's own title (`# Getting around the region with limited mobility`) rather than a `##` heading — that's the intro/title section, which has no `##` heading to start at yet.

**Criterion 5** — produced by: `app.py::cmd_ask` → `app.py::ask_pipeline`

```
Where is the nearest full hospital? — run 1

Best distance: 0.313, cutoff 0.7

The location of the nearest full hospital depends on the specific document:

* In `guide_accessibility.md`, the nearest full hospital is in Marchwood.
* In `guide_thornby_wells.md`, `guide_kestrelford.md`, `guide_pellew_sands.md`, and `guide_halden_bay.md`, the nearest full hospital is in Brightwater.

Sources retrieved: guide_accessibility.md, guide_halden_bay.md, guide_kestrelford.md, guide_pellew_sands.md, guide_thornby_wells.md
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MISSED | Against my `expects` values in `questions.py`, only 2 of 5 questions matched (accessibility, sea front) — 3 of them (bakery→Marchwood, winter→Brightwater, cycling→Givens Mill) don't match what the system found, in any of the 3 runs. That's 2/5 against a 4 of 5 target, a clear miss. See Diagnoses below — this isn't a pipeline bug, it's a bad test oracle. |
| 2 | Every answer names a source | MET | All 15 runs (5 questions × 3 runs) named at least one source file. Worth noting this criterion is nearly impossible to fail by construction — every chunk reaches the model pre-labeled with its filename and the system instruction demands a citation — so this MET says more about the plumbing than about answer quality. |
| 3 | Gate stops out-of-corpus questions | MET | All 5 out-of-scope questions refused, at distances 0.803–0.975, comfortably above the 0.70 cutoff. None of the five landed near the boundary the way I expected the Mongolia question to — my out-of-scope set may be less adversarial than it could be. |
| 4 | Chunks follow the section headings | MET | 4 of 5 sample chunks (from `python app.py chunks -n 5`) start at a `##` heading. The one exception, `guide_accessibility.md#0`, is the document's title/intro section, which has no `##` heading to start at yet — a different miss than the oversized-section split I originally anticipated, but still a legitimate structural exception rather than a chunking bug. |
| 5 | Conflicting documents are both surfaced | MET | All 3 runs of "Where is the nearest full hospital?" named both Brightwater and Marchwood instead of picking one silently. Run 2's wording drifted slightly ("For Brightwater, the nearest full hospital is in Marchwood" — not quite what `guide_accessibility.md` says), which is a grounding weak spot worth watching, but it still met the letter of the criterion on all 3 runs. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

Criterion 1 was the only miss (2 of 5 against a 4 of 5 target). All 3 misses
share one root cause, so it's one problem, not three:

**Which of the 5 questions missed, and why:**
- "Which town has the best bakery?" — `expects` said Marchwood. Only
  `guide_kestrelford.md` and `guide_eating.md` mention a bakery at all.
- "Which town is better to visit in the winter?" — `expects` said
  Brightwater. `guide_marchwood.md` explicitly says Marchwood "is the one
  place in the region that works in winter," while `guide_brightwater.md`
  says winter there is cold and several businesses close.
- "Where will be better to go cycling?" — `expects` said Givens Mill.
  Givens Mill's guide never mentions cycling; the actual routes are described
  in `guide_regional_transport.md` and `guide_brightwater.md`.

**Working backwards through the five stages** (per the "if you're stuck"
check): for all 3 questions, the retrieved chunks genuinely contained the
answer, and the generated answer accurately summarized that chunk — same
outcome across all 3 runs each time, so it isn't a wording fluke either. That
rules out loading, chunking, embedding, retrieval, *and* generation; none of
the five pipeline stages actually failed here.

**The real cause sits before the pipeline even ran:** I wrote the `expects`
values in `questions.py` during Milestone 2, before I'd carefully re-read
every document. Three of my five guesses about what the corpus *should* say
were simply wrong. The system found and reported the true answer every time —
my test oracle, not my pipeline, was broken.

**Update after building `scorer.py`:** once I had an automated, literal
string-matcher instead of my own judgment, it turned out my two "correct"
`expects` values had typos I'd read past without noticing — "Thorny Wells"
and "Peller Sands" instead of "Thornby Wells" and "Pellew Sands". A human
reader (me) recognized what I meant; a word-matching scorer correctly
couldn't. So all 5 of my original `expects` values had a problem, not 3 — two
typos plus the three wrong guesses above. I fixed both, and all 5 now pass
`scorer.judge()` against the answers I already had saved, no new model calls
needed to confirm it.

**Were any targets set too low?** Yes, two others look safer than they should:
- Criterion 2 (every answer names a source) can't structurally fail — every
  chunk reaches the model pre-labeled with its filename, and both the system
  instruction and the question ask for it. I'd tighten this to something that
  actually tests grounding, e.g. "every named source is one of the chunks
  actually retrieved for that question, not an invented one."
- Criterion 3 (gate stops out-of-corpus questions) was never tested near its
  boundary — my rationale predicted the Mongolia question would land close to
  the cutoff, but it scored 0.803, far clear of 0.70. I'd tighten this by
  swapping in a genuinely borderline out-of-scope question — something
  travel-adjacent but still uncovered by this corpus — instead of five
  wildly unrelated domains.

## The Improvement

**What I changed:**

I added a second chunking strategy, `chunker.py::split_documents_paragraphs`,
which splits every document on blank-line paragraph breaks instead of on `##`
section headings. I indexed it under a separate variant (`--variant
paragraphs`) so the original heading-based chunker and its index are
untouched. I did **not** touch `generate.py`'s `GROUNDING_INSTRUCTION` — that
text is fixed by the course, not mine to edit.

**Why I picked it:**

My diagnosis for criterion 5's run-2 wording drift pointed at generation, which
I'm not allowed to change — so I picked the closest available, diagnosis-adjacent
lever: a different chunk granularity, one of the two strategies the milestone
explicitly suggests, to see whether smaller, more atomic chunks reduce the
chance of the model blending facts across towns the way it did in that run.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

Run against the `paragraphs` variant, with the `expects` values in
`questions.py` already corrected (see housekeeping note below the table).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks follow the section headings | 4 of 5 | 2/5 | 2/5 | 2/5 | MISSED |
| 5. Conflicting documents are both surfaced | 3 of 3 | pass | pass | pass | MET |

**A fairness note on criterion 1:** the Before table above shows 2/5 against
the *original, wrong* `expects` values — that record is left untouched on
purpose (Unit 2's own rule: never edit history). But I fixed those `expects`
values as separate housekeeping before running this "after" test, so this
table uses the corrected ones. To isolate just the chunking change, I re-checked
what the *original* heading-based chunker scores against the same corrected
`expects`: **5/5**. So the fair comparison is 5/5 (heading) → 3/5 (paragraphs)
— the chunking change itself is what caused the drop, not the `expects` fix.

**Real output — Criterion 1 (the new miss):**

```
Which town is better to visit in the winter? — run 1 (variant: paragraphs)

Best distance: 0.5220 (passed the gate)
Sources retrieved: guide_accessibility.md, guide_halden_bay.md, guide_pellew_sands.md, guide_thornby_wells.md, guide_walking.md

Based on the documents, Thornby Wells is described as the region's most reliable winter destination after Marchwood, with a concert season running from September to April (guide_thornby_wells.md).
```
`guide_marchwood.md` — the document that actually says "This is the one place
in the region that works in winter" — never made it into the top 5 retrieved
chunks under this chunking. The heading-based chunker retrieved it every time.

**Real output — Criterion 4 (chunk fragmentation):**

```
guide_pellew_sands.md#10 | produced by: chunker.py::split_documents_paragraphs
## Where to stay

guide_marchwood.md#14 | produced by: chunker.py::split_documents_paragraphs
## Practical notes
```
Both of these are entire chunks — a heading with no body at all. Splitting on
paragraph breaks treats a lone heading line as its own paragraph.

**Did it help?**

No — it made things worse. Criterion 1 dropped from a fair 5/5 to 3/5:
splitting into 213 small paragraph-level chunks (versus 94 section-level ones)
meant the one decisive sentence naming Marchwood got outranked and never
retrieved for the winter question, buried among many more, smaller, similar
paragraphs competing for the same top-5 slots. Criterion 4 dropped from 4/5 to
2/5 for a simpler reason: a lone `##` heading with no following text becomes
its own tiny, useless chunk under this strategy. Criterion 5 stayed MET, and
its wording was arguably cleaner this time (no misattribution across any of
the 3 runs) — but it was already MET before, so this isn't a gain, just noise
from a different run. Criteria 2 and 3 were unaffected either way.

Given this, I'm keeping the original heading-based `split_documents` as the
system's actual chunking strategy — the paragraph variant stays in the
codebase only as this documented, unsuccessful experiment.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

After reverting to the original heading-based chunker, every criterion scores
MET again on its own terms — I didn't ship the regression. But one real,
known weakness is still sitting in the deployed system, unfixed:

**Criterion 5's generation-stage drift.** Before run 2 showed the model
inventing an unstated relationship ("For Brightwater, the nearest full
hospital is in Marchwood") that isn't what `guide_accessibility.md` actually
says. The fix that would target this directly — tightening
`GROUNDING_INSTRUCTION` in `generate.py` — isn't available to me; that text is
fixed by the course, not mine to edit. The one fix I was allowed to try
(switching chunking strategies) didn't touch this mechanism at all and made
two other criteria worse instead, so I reverted it. I stopped here because I
ran out of levers within what I'm allowed to change, not because I ran out of
time — if I could edit `generate.py`, I'd add a rule against inferring which
specific place an unattributed sentence applies to, and re-run criterion 5
several more times to see if that actually reduces the drift rate, since one
occurrence in three runs isn't enough to know if it's rare or common.

**Criteria 2 and 3 are MET but weakly tested**, and I'm choosing not to
"fix" them for this submission since nothing is actually broken — I'm noting
it here instead of quietly leaving it out. Criterion 2 can't structurally
fail given how the prompt and chunk labels are built, so passing it proves the
plumbing works, not that answers are well-grounded. Criterion 3's out-of-scope
questions were all obviously unrelated domains, so the gate has never been
tested against a genuinely borderline question. Both are test-design gaps, not
pipeline bugs, and I ran out of time to redesign and re-run them properly this
unit.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

**Criterion 1** — I'd never again write an `expects` value before actually
verifying it against the corpus. Three of my five guesses were wrong, and I
only found out because I happened to read the answers carefully instead of
trusting my own memory of documents I'd skimmed in Milestone 1.

**Criterion 2** — I'd write this so it can actually fail. "Names a source"
was true by construction the moment the system instruction and prompt both
demand it. Next time I'd write something like "every named source is one of
the chunks the system actually retrieved for that question" — a claim that
could genuinely be wrong if the model ever invented a citation.

**Criterion 3** — I'd pick out-of-scope questions closer to the boundary
instead of five obviously unrelated ones. My own rationale predicted the
Mongolia question would be the close call, and it scored 0.803 — nowhere near
the 0.70 cutoff. A criterion that's never actually tested near its edge isn't
telling me much.

**Criteria 4 and 5** I'd keep close to as-is. Criterion 5 in particular
earned its place — it's the only one that caught a real generation failure,
even though I couldn't fix it this unit.

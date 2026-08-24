# Practice design contract

Use this reference to design and independently review generated practice. The
research motivates the sequence; it does not justify inflating every lesson
into a large project.

## Learning-design basis

- **Authentic whole task**: 4C/ID organizes complex-skill learning around
  meaningful whole tasks, supported information, procedural information, and
  part-task practice. Here that means shrinking one real ML workflow while
  preserving its input contract, core implementation, tests, failure
  diagnosis, and interpretation. It does not mean adding production scale.
  See [4C/ID in the context of instructional design and the learning
  sciences](https://research.ou.nl/en/publications/4cid-in-the-context-of-instructional-design-and-the-learning-scie/).
- **Deliberate practice**: practice needs a concrete performance target,
  effortful learner execution, observable error, and feedback focused on
  improvement. Repetition alone and a generic project do not meet this bar.
  See [Ericsson, Krampe, and Tesch-Römer
  (1993)](https://doi.org/10.1037/0033-295X.100.3.363). Do not turn this into a
  “10,000 hours” claim or claim practice explains all expertise.
- **Retrieval practice**: ask for a prediction or reconstruction before showing
  setup-specific cues. Retrieval can strengthen later retention more than
  restudy alone, so an already well-written TIL still benefits from a blank
  implementation attempt. See [Roediger and Karpicke
  (2006)](https://doi.org/10.1111/j.1467-9280.2006.01693.x).
- **Fading**: progress from a tiny analogous trace to pseudocode and only then
  a minimal API skeleton. Never jump directly from no help to a full answer.
  See [Renkl et al. (2002)](https://eric.ed.gov/?id=EJ658398).
- **Avoid split attention**: put the hint beside the TODO it explains. A global
  hint appendix forces the learner to alternate between separate information
  sources and adds irrelevant search work. See [Chandler and Sweller
  (1992)](https://doi.org/10.1111/j.2044-8279.1992.tb01017.x).

## Whole-task sizing

Keep the smallest workflow that still exposes the professional boundary:

1. deterministic input or fixture;
2. explicit public contract;
3. learner-owned core logic;
4. normal, edge, and failure observation;
5. diagnosis from the actual failure;
6. explanation of system meaning and limitation.

For a Tensor lesson this might be a boundary function plus tests, not a model
service. For a training-loop lesson it might be `train_step`, validation, and
checkpoint selection on a fixed CPU batch, not distributed training.

## Standalone specification boundary

The generated Notebook is the learner's complete task interface. Linked TIL,
lesson, and instructor-practice files establish provenance and fidelity but are
not prerequisites for discovering a threshold, token, representation, axis,
boundary convention, aggregation, or failure rule.

Each exercise distinguishes three kinds of learner-visible contract:

- `source-given`: a fixed rule retained from a mapped source;
- `practice-given`: a useful local API or failure rule added by the workbook;
- `derive`: a result or invariant that follows from visible inputs and concepts.

Use contiguous IDs such as `C-E03-01` in the required `Contract ID | Kind |
Learner-visible requirement` table. Follow it with `#### 학습자가 구현·판단할
것`, so a fixed requirement cannot be confused with the learner-owned method.
Every assertion group and expected-exception block cites a declared same-exercise
ID using `# contract: ...`. Do not make a source link, hint, fixture output, or
failing test the first place an arbitrary choice becomes visible.

This is a semantic boundary, not merely a formatting rule. If multiple sensible
implementations fit the prose and only an undisclosed convention passes, the
artifact fails review even when all structural checks pass. Conversely, a
derived numeric answer need not be printed in the specification when the visible
fixture and contract determine it.

Put exactly one unexecuted `# setup-check` cell before the first exercise TODO.
Generated practice is one Notebook, so this cell contains only dependencies,
shared types, and non-solution helpers. The artifact validator executes this
preparation cell from the repository root.

## Choose the smallest useful artifact boundary

Create exactly one `practice/<area>/<topic>.ipynb` for each generated practice.
Use exercises inside that Notebook for every part of the whole task, including
small training, validation, checkpoint-selection, shape, and output-contract
work. A production-looking directory, import boundary, reload loop, or pytest
process is not useful authenticity for this learning flow; it creates
bookkeeping the learner did not ask to practise. A reusable multi-file project
is a different, explicitly requested deliverable.

Within a Notebook-only exercise, keep four visible boundaries adjacent:

1. a learner function cell marked `# TODO: E01`;
2. a deterministic observation cell marked `# provided-fixture: E01`;
3. a self-contained `check_e01()` cell marked `# test-check: E01`, containing
   normal, edge, and failure cases;
4. the learner's interpretation prompt.

Keep the deterministic fixture and normal, edge, and failure checks beside the
exercise. This prevents split attention and lets the learner follow one short
loop: edit the TODO cell, run its fixture cell, run `check_e##()`, and interpret
the resulting state. Do not create a hidden source module or test file.

## Coverage-map review

For every major TIL outcome, ask:

1. Is the cited TIL location exact enough to find the learner's statement?
2. Does the action test performance rather than recognition?
3. Is required evidence observable in code, a test, a trace, or an interpreted
   result?
4. Is the outcome naturally part of this whole task? If not, split only when a
   separate environment or interpretation is necessary.
5. Does prior evidence include independent execution and interpretation? A
   correct written explanation alone does not remove the outcome.

## Artifact review rubric

A fresh reviewer returns `pass` only when all are true:

- the exact finalized TIL is valid and all major outcomes are represented;
- exact lesson links resolve and instructor practice comes from an explicit
  `INDEX.md` mapping;
- each public learner function is a genuine blank core implementation;
- the Notebook alone discloses every fixed requirement needed by its TODOs and
  checks, while source links remain optional provenance;
- every Contract ID has a valid kind, a concrete learner-visible requirement,
  and traceable same-exercise checks with no hidden test-only convention;
- source-specific policies are labeled as local rather than universal, and
  practice-added rules are useful rather than arbitrary busywork;
- tests cover normal, edge, and failure behavior without revealing the method;
- each exercise begins with context and prediction, provides a tiny contract,
  and ends with failure diagnosis and interpretation;
- Hint 1 and Hint 2 are folded and adjacent to that exercise's TODO;
- code cells are unexecuted and contain no fabricated output;
- setup and conventions remain smaller than the concept being learned;
- the single Notebook has adjacent implementation, fixture, and local
  normal/edge/failure checks;
- initial execution fails only at explicit learner-owned `NotImplementedError`
  boundaries.

The reviewer performs a Notebook-only specification pass before opening the
sources, then a source-fidelity pass. The reviewer identifies concrete blocking
findings, not stylistic preferences.
One revision and one second fresh review are the maximum. Never replace an
unavailable independent reviewer with the author's self-approval.

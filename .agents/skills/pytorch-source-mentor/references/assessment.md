# Assessment and spaced review

Use `curriculum/ASSESSMENT_BLUEPRINT.md` as the authoritative assessment policy. From 2026-09-13, do not generate standalone knowledge quizzes. Ground assessment in the current MiniTorch milestone: learner-authored design/code, focused tests, debugging, pinned-PyTorch comparison, unassisted code defense and delayed extension/repair. Historical question rows remain valid records.

Opening diagnostic answers select teaching depth and do not raise mastery. A completed session may contain no new `QUESTION_HISTORY.csv` row when the project diff, verification, debugging and compact defense provide the evidence. Do not manufacture a question merely to populate the table.

## Mastery dimensions

Score concepts independently on a 0–4 scale:

- `explain`: state purpose and invariants;
- `locate`: find authoritative source without a supplied path;
- `trace`: reconstruct a real call chain;
- `debug`: form and test hypotheses from failures;
- `modify`: make a focused change with tests;
- `transfer`: apply the mechanism to a new operator/backend case;
- `retain`: retrieve after a delay.

Score meanings:

- 0: no evidence;
- 1: recognizes after substantial guidance;
- 2: succeeds with H2 or partial correctness;
- 3: independently succeeds on the studied case with H0/H1;
- 4: independently transfers, explains tradeoffs, and survives delayed review.

Never average dimensions into a claim of overall mastery. A phase gate specifies minimum dimensions.

Before scoring, establish provenance from the actual MiniTorch diff: decisive learner work, mentor scaffolding and unrelated pre-existing changes. A mentor-created artifact cannot support `modify`; learner approval or repetition cannot convert its authorship. Prefer observed repository behavior over oral precision, and convert an explanation gap into a later code/test repair where feasible.

## Evidence ordering

Encode the completed work once in a reviewed manifest. The session recorder
stages and validates immutable evidence, optional project-grounded questions,
mastery aggregates, review items, notebook/session links, `STATE.md` and the
generated `NEXT_SESSION.md`. Do not hand-edit all outputs during a normal
session. Manual repair is reserved for migrations or validator-approved fixes.

## Weekly audit

Once per week:

- sample at least one older concept through a small MiniTorch explanation, extension or repair without replaying instructions;
- inspect whether study time produced executable evidence rather than passive reading;
- identify the earliest weak prerequisite;
- compare planned and actual hours without punishing schedule variance;
- keep recording/administration below 10% of active session time and ordinary
  startup context below roughly 8k tokens;
- keep, slow, or revise the next week's scope;
- do not enter a new phase until its project gate passes.

Use `templates/WEEKLY_REVIEW.md` for the artifact.

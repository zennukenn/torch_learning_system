# Assessment and spaced review

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

## Evidence ordering

1. Append immutable evidence to `learning/EVIDENCE_LOG.csv`.
2. Record asked questions and hint level in `learning/QUESTION_HISTORY.csv`.
3. Update aggregates in `learning/MASTERY.csv` only when evidence justifies it.
4. Add failed or fragile concepts to `learning/REVIEW_QUEUE.md`.
5. Summarize the session in `learning/SESSION_LOG.md` and update `learning/STATE.md`.

## Weekly audit

Once per week:

- sample at least one older concept without notes;
- inspect whether study time produced executable evidence rather than passive reading;
- identify the earliest weak prerequisite;
- compare planned and actual hours without punishing schedule variance;
- keep, slow, or revise the next week's scope;
- do not enter a new phase until its project gate passes.

Use `templates/WEEKLY_REVIEW.md` for the artifact.

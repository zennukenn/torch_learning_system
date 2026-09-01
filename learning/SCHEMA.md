# Learning-state schema

## Update order

1. Collect the learner's unaided teach-back and focused follow-up answers before closing the session.
2. Create `learning/notebook/sessions/YYYY-MM-DD-short-session-name.md` from `templates/LEARNING_NOTE.md`; update notebook index and mistakes.
3. Append new immutable rows to `EVIDENCE_LOG.csv` and `QUESTION_HISTORY.csv`, linking each evidence row to the completed notebook note.
4. Update aggregate scores in `MASTERY.csv` only from referenced evidence.
5. Update `REVIEW_QUEUE.md`, `ERROR_LOG.md`, `SESSION_LOG.md`, then `STATE.md`.
6. Run `python3 scripts/validate_learning_state.py`.

## Session artifacts

- Store durable learner work in `learning/artifacts/YYYY-MM-DD-short-session-name/`.
- Start from the relevant file in `templates/` and link the artifact from `SESSION_LOG.md`.
- Keep commands and key outputs concise; do not commit build products, full logs, secrets, proprietary identifiers, or copied generated trees.
- A source-only artifact must label runtime/build claims as unverified. It may support `explain` or `locate`, but not a runtime dispatch, debugging, or complete end-to-end `trace` score by itself.

## Notebook rules

- A completed learning session has exactly one note under `learning/notebook/sessions/`, created only after the learner's unaided teach-back.
- Preserve the learner's feedback-free recap and original wrong answers. Put corrections and mentor supplements in separate sections; never rewrite history to make the original answer appear correct.
- Each evidence row's `notebook_path` is a repository-relative path to that completed note. The note contains its evidence IDs and is linked from `learning/notebook/INDEX.md` and `SESSION_LOG.md`.
- Add every `QUESTION_HISTORY.csv` row with verdict `partial` or `fail` to `learning/notebook/MISTAKES.md`. Resolution changes its status and adds retrieval evidence; it does not remove the row.
- Do not award mastery for text supplied by the mentor. A corrected learner restatement records its actual hint level and requires later H0/H1 retrieval for independent mastery.

## CSV rules

- Use UTF-8 and keep the exact header/order.
- Quote any field containing a comma, quote or newline according to RFC 4180.
- IDs are stable and unique: recommended `E-YYYYMMDD-NN` and `Q-YYYYMMDD-NN`.
- `revision` is an exact commit SHA when source claims are assessed; use `binary:<torch-version>` only for binary-only evidence.
- `notebook_path` must be `learning/notebook/sessions/<session-note>.md` and point to an existing completed note containing the evidence ID.
- `hint_level` is `H0`, `H1`, `H2` or `H3`.
- `verdict` is one of `pass`, `partial`, `fail`, `invalid`.
- `status` is one of `unassessed`, `learning`, `review`, `mastered`.
- `dimension` is one of `explain`, `locate`, `trace`, `debug`, `modify`, `transfer`, `retain`.
- All dates use `YYYY-MM-DD`. Question rows reference an existing evidence row for the same concept; nonzero mastery scores reference an existing `last_evidence_id` for that concept.
- Scores in `MASTERY.csv` are integers 0–4. Never lower or raise them silently; explain the evidence in the session log.
- An aggregate may decrease when delayed evidence reveals regression; retention should reflect the newest delayed retrieval.

## Evidence quality

`source_or_command` contains a repository-relative source anchor, official URL, command/test, or a short combination. Do not paste long logs. `learner_result` records what the learner actually produced, not the mentor's model answer.

Never store confidential hardware/source/log/model identifiers in any field.

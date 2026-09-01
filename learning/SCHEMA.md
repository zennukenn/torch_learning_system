# Learning-state schema

## Update order

1. Append new immutable rows to `EVIDENCE_LOG.csv` and `QUESTION_HISTORY.csv`.
2. Update aggregate scores in `MASTERY.csv` only from referenced evidence.
3. Update `REVIEW_QUEUE.md`, `ERROR_LOG.md`, `SESSION_LOG.md`, then `STATE.md`.
4. Run `python3 scripts/validate_learning_state.py`.

## Session artifacts

- Store durable learner work in `learning/artifacts/YYYY-MM-DD-short-session-name/`.
- Start from the relevant file in `templates/` and link the artifact from `SESSION_LOG.md`.
- Keep commands and key outputs concise; do not commit build products, full logs, secrets, proprietary identifiers, or copied generated trees.
- A source-only artifact must label runtime/build claims as unverified. It may support `explain` or `locate`, but not a runtime dispatch, debugging, or complete end-to-end `trace` score by itself.

## CSV rules

- Use UTF-8 and keep the exact header/order.
- Quote any field containing a comma, quote or newline according to RFC 4180.
- IDs are stable and unique: recommended `E-YYYYMMDD-NN` and `Q-YYYYMMDD-NN`.
- `revision` is an exact commit SHA when source claims are assessed; use `binary:<torch-version>` only for binary-only evidence.
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

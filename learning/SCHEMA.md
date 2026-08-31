# Learning-state schema

## Update order

1. Append new immutable rows to `EVIDENCE_LOG.csv` and `QUESTION_HISTORY.csv`.
2. Update aggregate scores in `MASTERY.csv` only from referenced evidence.
3. Update `REVIEW_QUEUE.md`, `ERROR_LOG.md`, `SESSION_LOG.md`, then `STATE.md`.
4. Run `python3 scripts/validate_learning_state.py`.

## CSV rules

- Use UTF-8 and keep the exact header/order.
- Quote any field containing a comma, quote or newline according to RFC 4180.
- IDs are stable and unique: recommended `E-YYYYMMDD-NN` and `Q-YYYYMMDD-NN`.
- `revision` is an exact commit SHA when source claims are assessed; use `binary:<torch-version>` only for binary-only evidence.
- `hint_level` is `H0`, `H1`, `H2` or `H3`.
- `verdict` is one of `pass`, `partial`, `fail`, `invalid`.
- Scores in `MASTERY.csv` are integers 0–4. Never lower or raise them silently; explain the evidence in the session log.
- An aggregate may decrease when delayed evidence reveals regression; retention should reflect the newest delayed retrieval.

## Evidence quality

`source_or_command` contains a repository-relative source anchor, official URL, command/test, or a short combination. Do not paste long logs. `learner_result` records what the learner actually produced, not the mentor's model answer.

Never store confidential hardware/source/log/model identifiers in any field.

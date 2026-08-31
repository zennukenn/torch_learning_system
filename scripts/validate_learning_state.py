#!/usr/bin/env python3
"""Validate the durable learning-state files without modifying them."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEARNING = ROOT / "learning"

SPECS = {
    "MASTERY.csv": [
        "concept_id", "concept", "phase", "explain", "locate", "trace",
        "debug", "modify", "transfer", "retain", "last_evidence_id", "status",
    ],
    "EVIDENCE_LOG.csv": [
        "evidence_id", "date", "session", "revision", "concept_id", "dimension",
        "task", "learner_result", "hint_level", "source_or_command", "verdict",
        "next_review",
    ],
    "QUESTION_HISTORY.csv": [
        "question_id", "date", "concept_id", "question", "conditions",
        "learner_answer", "hint_level", "verdict", "evidence_id", "next_due",
    ],
}

REQUIRED = [
    "PROFILE.md", "STATE.md", "MASTERY.csv", "EVIDENCE_LOG.csv",
    "QUESTION_HISTORY.csv", "REVIEW_QUEUE.md", "SESSION_LOG.md", "ERROR_LOG.md",
]


def read_rows(path: Path, expected: list[str], errors: list[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected:
            errors.append(f"{path.name}: header mismatch: {reader.fieldnames!r}")
        rows = list(reader)
    for number, row in enumerate(rows, start=2):
        if None in row:
            errors.append(f"{path.name}:{number}: extra unquoted CSV field(s): {row[None]!r}")
        missing = [key for key in expected if row.get(key) is None]
        if missing:
            errors.append(f"{path.name}:{number}: missing fields: {missing}")
    return rows


def unique_nonempty(rows: list[dict[str, str]], key: str, filename: str, errors: list[str]) -> None:
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        value = row.get(key, "").strip()
        if not value:
            errors.append(f"{filename}:{number}: empty {key}")
        elif value in seen:
            errors.append(f"{filename}:{number}: duplicate {key} {value!r}")
        seen.add(value)


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED:
        if not (LEARNING / name).is_file():
            errors.append(f"missing required file: learning/{name}")

    tables: dict[str, list[dict[str, str]]] = {}
    for name, header in SPECS.items():
        path = LEARNING / name
        if path.is_file():
            tables[name] = read_rows(path, header, errors)

    mastery = tables.get("MASTERY.csv", [])
    unique_nonempty(mastery, "concept_id", "MASTERY.csv", errors)
    score_fields = ["explain", "locate", "trace", "debug", "modify", "transfer", "retain"]
    for number, row in enumerate(mastery, start=2):
        for field in score_fields:
            try:
                score = int(row.get(field, ""))
            except ValueError:
                errors.append(f"MASTERY.csv:{number}: {field} is not an integer")
                continue
            if score not in range(5):
                errors.append(f"MASTERY.csv:{number}: {field}={score} is outside 0..4")

    evidence = tables.get("EVIDENCE_LOG.csv", [])
    questions = tables.get("QUESTION_HISTORY.csv", [])
    if evidence:
        unique_nonempty(evidence, "evidence_id", "EVIDENCE_LOG.csv", errors)
    if questions:
        unique_nonempty(questions, "question_id", "QUESTION_HISTORY.csv", errors)

    if errors:
        print("Learning-state validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Learning state is valid: "
        f"{len(mastery)} mastery concepts, {len(evidence)} evidence rows, "
        f"{len(questions)} question rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

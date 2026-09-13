#!/usr/bin/env python3
"""Validate that every mastery concept is mapped to a runnable learning path."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "curriculum" / "COVERAGE_MATRIX.csv"
MASTERY = ROOT / "learning" / "MASTERY.csv"
SOURCE = ROOT / "sources" / "pytorch"
ROADMAP = ROOT / "projects" / "ROADMAP.md"

HEADER = [
    "concept_id",
    "priority",
    "milestones",
    "pytorch_anchors",
    "learner_evidence",
]
PRIORITIES = {"F0", "I0", "I1", "I2", "T1", "T2"}
MILESTONE = re.compile(r"^M[0-9]$")


def read_csv(path: Path) -> tuple[list[str] | None, list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def main() -> int:
    errors: list[str] = []
    if not MATRIX.is_file() or not MASTERY.is_file() or not ROADMAP.is_file():
        print("Coverage validation failed: required input file is missing", file=sys.stderr)
        return 1

    matrix_header, rows = read_csv(MATRIX)
    _, mastery_rows = read_csv(MASTERY)
    if matrix_header != HEADER:
        errors.append(f"coverage header mismatch: {matrix_header!r}")

    matrix_ids: list[str] = []
    for line, row in enumerate(rows, start=2):
        concept_id = row.get("concept_id", "").strip()
        matrix_ids.append(concept_id)
        for field in HEADER:
            if not row.get(field, "").strip():
                errors.append(f"COVERAGE_MATRIX.csv:{line}: empty {field}")

        priority = row.get("priority", "").strip()
        if priority not in PRIORITIES:
            errors.append(f"COVERAGE_MATRIX.csv:{line}: invalid priority {priority!r}")

        milestones = row.get("milestones", "").split(";")
        if any(not MILESTONE.fullmatch(value.strip()) for value in milestones):
            errors.append(
                f"COVERAGE_MATRIX.csv:{line}: invalid milestones {row.get('milestones')!r}"
            )

        for anchor_text in row.get("pytorch_anchors", "").split(";"):
            anchor = Path(anchor_text.strip())
            candidate = (SOURCE / anchor).resolve()
            try:
                candidate.relative_to(SOURCE.resolve())
            except ValueError:
                errors.append(
                    f"COVERAGE_MATRIX.csv:{line}: anchor escapes source root {anchor_text!r}"
                )
                continue
            if anchor.is_absolute() or ".." in anchor.parts or not candidate.exists():
                errors.append(
                    f"COVERAGE_MATRIX.csv:{line}: missing source anchor {anchor_text!r}"
                )

    duplicates = sorted({value for value in matrix_ids if matrix_ids.count(value) > 1})
    if duplicates:
        errors.append(f"duplicate coverage concept IDs: {duplicates}")

    mastery_ids = {row["concept_id"].strip() for row in mastery_rows}
    coverage_ids = set(matrix_ids)
    if missing := sorted(mastery_ids - coverage_ids):
        errors.append(f"mastery concepts missing from coverage matrix: {missing}")
    if extra := sorted(coverage_ids - mastery_ids):
        errors.append(f"unknown concepts in coverage matrix: {extra}")

    roadmap = ROADMAP.read_text(encoding="utf-8")
    for index in range(10):
        if f"## M{index} " not in roadmap:
            errors.append(f"projects/ROADMAP.md is missing M{index}")

    required_docs = [
        ROOT / "projects" / "MINITORCH_SPEC.md",
        ROOT / "projects" / "INFERENCE_SCOPE.md",
        ROOT / "projects" / "PRIVATEUSE_BACKEND_SPEC.md",
        ROOT / "curriculum" / "COVERAGE_AUDIT.md",
    ]
    for path in required_docs:
        if not path.is_file():
            errors.append(f"missing curriculum document: {path.relative_to(ROOT)}")

    if errors:
        print("Coverage validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    i0_count = sum(row["priority"].strip() == "I0" for row in rows)
    print(
        f"Curriculum coverage is valid: {len(rows)} concepts mapped; "
        f"{i0_count} required inference/backend concepts; M0-M9 present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

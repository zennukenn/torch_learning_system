#!/usr/bin/env python3
"""Validate that every mastery concept is mapped to a runnable learning path."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
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
    "source_symbols",
    "learner_evidence",
    "evidence_dimensions",
]
PRIORITIES = {"F0", "I0", "I1", "I2", "T1", "T2"}
DIMENSIONS = {"explain", "locate", "trace", "debug", "modify", "transfer", "retain"}
SYMBOL = re.compile(r"^[A-Za-z_][A-Za-z0-9_:.<>/-]*$")


def read_csv(path: Path) -> tuple[list[str] | None, list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=MATRIX)
    parser.add_argument("--mastery", type=Path, default=MASTERY)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--roadmap", type=Path, default=ROADMAP)
    parser.add_argument(
        "--verify-symbols",
        action="store_true",
        help="use rg to verify each named symbol/marker under its listed anchors",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    matrix_path = args.matrix.resolve()
    mastery_path = args.mastery.resolve()
    source_root = args.source.resolve()
    roadmap_path = args.roadmap.resolve()
    errors: list[str] = []
    if not matrix_path.is_file() or not mastery_path.is_file() or not roadmap_path.is_file():
        print("Coverage validation failed: required input file is missing", file=sys.stderr)
        return 1
    if args.verify_symbols and shutil.which("rg") is None:
        print("Coverage validation failed: rg is required for --verify-symbols", file=sys.stderr)
        return 1

    matrix_header, rows = read_csv(matrix_path)
    _, mastery_rows = read_csv(mastery_path)
    if matrix_header != HEADER:
        errors.append(f"coverage header mismatch: {matrix_header!r}")

    roadmap = roadmap_path.read_text(encoding="utf-8")
    declared_milestones = set(re.findall(r"^## (M\d+(?:\.\d+)?)\b", roadmap, re.M))
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

        milestones = [value.strip() for value in row.get("milestones", "").split(";")]
        unknown_milestones = sorted(set(milestones) - declared_milestones)
        if unknown_milestones:
            errors.append(
                f"COVERAGE_MATRIX.csv:{line}: undeclared milestones {unknown_milestones}"
            )

        symbols = [value.strip() for value in row.get("source_symbols", "").split(";")]
        if any(not SYMBOL.fullmatch(value) for value in symbols):
            errors.append(
                f"COVERAGE_MATRIX.csv:{line}: malformed source_symbols "
                f"{row.get('source_symbols')!r}"
            )

        dimensions = [
            value.strip() for value in row.get("evidence_dimensions", "").split(";")
        ]
        if len(dimensions) < 2 or len(dimensions) != len(set(dimensions)):
            errors.append(
                f"COVERAGE_MATRIX.csv:{line}: evidence_dimensions need at least two unique values"
            )
        invalid_dimensions = sorted(set(dimensions) - DIMENSIONS)
        if invalid_dimensions:
            errors.append(
                f"COVERAGE_MATRIX.csv:{line}: invalid evidence_dimensions {invalid_dimensions}"
            )
        dimension_set = set(dimensions)
        if priority == "I0" and not {"trace", "debug", "modify"}.issubset(dimension_set):
            errors.append(
                f"COVERAGE_MATRIX.csv:{line}: I0 requires trace, debug and modify evidence"
            )
        if priority == "F0" and "explain" not in dimension_set:
            errors.append(f"COVERAGE_MATRIX.csv:{line}: F0 requires explain evidence")
        if priority in {"I1", "T1"} and "modify" not in dimension_set:
            errors.append(f"COVERAGE_MATRIX.csv:{line}: {priority} requires modify evidence")

        for anchor_text in row.get("pytorch_anchors", "").split(";"):
            anchor = Path(anchor_text.strip())
            candidate = (source_root / anchor).resolve()
            try:
                candidate.relative_to(source_root)
            except ValueError:
                errors.append(
                    f"COVERAGE_MATRIX.csv:{line}: anchor escapes source root {anchor_text!r}"
                )
                continue
            if anchor.is_absolute() or ".." in anchor.parts or not candidate.exists():
                errors.append(
                    f"COVERAGE_MATRIX.csv:{line}: missing source anchor {anchor_text!r}"
                )
        if args.verify_symbols:
            anchor_paths = [
                str(source_root / value.strip())
                for value in row.get("pytorch_anchors", "").split(";")
            ]
            for symbol in symbols:
                located = subprocess.run(
                    ["rg", "-F", "-l", "-m", "1", "--", symbol, *anchor_paths],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                if located.returncode != 0:
                    errors.append(
                        f"COVERAGE_MATRIX.csv:{line}: source symbol/marker {symbol!r} "
                        "was not found under its anchors"
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

    for index in range(10):
        if f"M{index}" not in declared_milestones:
            errors.append(f"projects/ROADMAP.md is missing M{index}")
    if "M2.5" not in declared_milestones:
        errors.append("projects/ROADMAP.md is missing M2.5")
    for milestone in declared_milestones:
        block_match = re.search(
            rf"^## {re.escape(milestone)}\b.*?(?=^## M\d|^## Common|\Z)",
            roadmap,
            re.M | re.S,
        )
        if block_match is None or "Depth:" not in block_match.group(0):
            errors.append(f"projects/ROADMAP.md {milestone} has no C/R/S depth assignment")
        if f"| {milestone} |" not in roadmap:
            errors.append(f"projects/ROADMAP.md capacity table is missing {milestone}")

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
        f"{i0_count} required inference/backend concepts; M0-M9 and M2.5 present; "
        f"source symbols {'verified' if args.verify_symbols else 'declared'} and "
        "evidence dimensions checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
PRACTICE_MAP = ROOT / "curriculum" / "COURSE_PRACTICE_MAP.csv"
MASTERY = ROOT / "learning" / "MASTERY.csv"
SOURCE = ROOT / "sources" / "pytorch"
ROADMAP = ROOT / "projects" / "ROADMAP.md"
COURSE_PLAN_SYNC = ROOT / "scripts" / "sync_course_plan.py"

HEADER = [
    "concept_id",
    "priority",
    "milestones",
    "pytorch_anchors",
    "source_symbols",
    "learner_evidence",
    "evidence_dimensions",
]
PRACTICE_HEADER = [
    "course_id",
    "sequence",
    "title",
    "milestone",
    "release",
    "mode",
    "priority",
    "hours_min",
    "hours_max",
    "dependency_gate",
    "concept_ids",
    "knowledge_block",
    "immediate_learner_action",
    "runnable_evidence",
]
PRIORITIES = {"F0", "I0", "I1", "I2", "T1", "T2"}
DIMENSIONS = {"explain", "locate", "trace", "debug", "modify", "transfer", "retain"}
MODES = {"foundation-project", "implementation-project", "implementation-trace"}
RELEASES = ["A", "B", "C"]
SYMBOL = re.compile(r"^[A-Za-z_][A-Za-z0-9_:.<>/-]*$")


def read_csv(path: Path) -> tuple[list[str] | None, list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=MATRIX)
    parser.add_argument("--practice-map", type=Path, default=PRACTICE_MAP)
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
    practice_path = args.practice_map.resolve()
    mastery_path = args.mastery.resolve()
    source_root = args.source.resolve()
    roadmap_path = args.roadmap.resolve()
    errors: list[str] = []
    if (
        not matrix_path.is_file()
        or not practice_path.is_file()
        or not mastery_path.is_file()
        or not roadmap_path.is_file()
    ):
        print("Coverage validation failed: required input file is missing", file=sys.stderr)
        return 1
    if args.verify_symbols and shutil.which("rg") is None:
        print("Coverage validation failed: rg is required for --verify-symbols", file=sys.stderr)
        return 1

    matrix_header, rows = read_csv(matrix_path)
    practice_header, practice_rows = read_csv(practice_path)
    _, mastery_rows = read_csv(mastery_path)
    if matrix_header != HEADER:
        errors.append(f"coverage header mismatch: {matrix_header!r}")
    if practice_header != PRACTICE_HEADER:
        errors.append(f"course practice header mismatch: {practice_header!r}")

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

    declared_course_milestones = set(
        re.findall(r"^#{2,3} (M\d+(?:\.\d+)?[a-z]?)\b", roadmap, re.M)
    )
    course_ids: list[str] = []
    course_concepts: list[str] = []
    sequences: list[int] = []
    course_releases: list[str] = []
    course_hours: list[tuple[int, int]] = []
    for line, row in enumerate(practice_rows, start=2):
        for field in PRACTICE_HEADER:
            if not row.get(field, "").strip():
                errors.append(f"COURSE_PRACTICE_MAP.csv:{line}: empty {field}")
        course_id = row.get("course_id", "").strip()
        milestone = row.get("milestone", "").strip()
        course_ids.append(course_id)
        course_releases.append(row.get("release", "").strip())
        if milestone not in declared_course_milestones:
            errors.append(
                f"COURSE_PRACTICE_MAP.csv:{line}: undeclared milestone {milestone!r}"
            )
        try:
            sequences.append(int(row.get("sequence", "")))
        except ValueError:
            errors.append(f"COURSE_PRACTICE_MAP.csv:{line}: sequence is not an integer")
        try:
            minimum = int(row.get("hours_min", ""))
            maximum = int(row.get("hours_max", ""))
            course_hours.append((minimum, maximum))
            if minimum <= 0 or maximum < minimum:
                errors.append(
                    f"COURSE_PRACTICE_MAP.csv:{line}: invalid hour range {minimum}–{maximum}"
                )
        except ValueError:
            errors.append(f"COURSE_PRACTICE_MAP.csv:{line}: hours must be integers")
        if row.get("mode", "").strip() not in MODES:
            errors.append(f"COURSE_PRACTICE_MAP.csv:{line}: invalid mode")
        priorities = {
            value.strip() for value in row.get("priority", "").split(";") if value.strip()
        }
        if not priorities or priorities - PRIORITIES:
            errors.append(
                f"COURSE_PRACTICE_MAP.csv:{line}: invalid priorities {sorted(priorities)}"
            )
        concept_values = [
            value.strip()
            for value in row.get("concept_ids", "").split(";")
            if value.strip()
        ]
        course_concepts.extend(concept_values)
        unknown_concepts = sorted(set(concept_values) - mastery_ids)
        if unknown_concepts:
            errors.append(
                f"COURSE_PRACTICE_MAP.csv:{line}: unknown concepts {unknown_concepts}"
            )

    expected_ids = [f"C{index:02d}" for index in range(len(practice_rows))]
    if course_ids != expected_ids:
        errors.append(f"course IDs must be contiguous and ordered: {expected_ids!r}")
    if sequences != list(range(len(practice_rows))):
        errors.append(
            "COURSE_PRACTICE_MAP.csv sequences must be contiguous and ordered from zero"
        )
    if sorted(set(course_releases)) != RELEASES:
        errors.append(f"course releases must be exactly {RELEASES!r}")
    if course_releases != sorted(course_releases):
        errors.append("course releases must remain in A then B then C order")
    for index, row in enumerate(practice_rows):
        expected_dependency = "none" if index == 0 else practice_rows[index - 1]["course_id"]
        if row.get("dependency_gate", "").strip() != expected_dependency:
            errors.append(
                f"COURSE_PRACTICE_MAP.csv:{index + 2}: dependency_gate must be "
                f"{expected_dependency!r}"
            )
    release_a = [
        (row, hours)
        for row, hours in zip(practice_rows, course_hours)
        if row.get("release") == "A"
    ]
    if not release_a or sum(hours[1] for _, hours in release_a) > 50:
        errors.append("Release A must deliver its walking skeleton within 50 focused hours")
    if not any(
        "CPU" in row.get("title", "") and "model" in row.get("runnable_evidence", "")
        for row, _ in release_a
    ):
        errors.append("Release A must contain runnable first-CPU-model evidence")
    milestone_sequence = {
        row["milestone"]: index for index, row in enumerate(practice_rows)
    }
    for earlier, later in [("M0a", "M0b"), ("M0b", "M2.5"), ("M2.5", "M1"),
                           ("M1", "M2"), ("M2", "M0c"), ("M0c", "M3")]:
        if earlier not in milestone_sequence or later not in milestone_sequence:
            errors.append(f"course map is missing spiral gate {earlier} -> {later}")
        elif milestone_sequence[earlier] >= milestone_sequence[later]:
            errors.append(f"course map violates spiral gate {earlier} -> {later}")
    duplicate_course_concepts = sorted(
        {value for value in course_concepts if course_concepts.count(value) > 1}
    )
    if duplicate_course_concepts:
        errors.append(
            f"concepts assigned to multiple first-accountable courses: {duplicate_course_concepts}"
        )
    if missing := sorted(mastery_ids - set(course_concepts)):
        errors.append(f"mastery concepts missing from course practice map: {missing}")
    if extra := sorted(set(course_concepts) - mastery_ids):
        errors.append(f"unknown concepts in course practice map: {extra}")

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
        ROOT / "curriculum" / "COURSE_PRACTICE_PLAN.md",
    ]
    for path in required_docs:
        if not path.is_file():
            errors.append(f"missing curriculum document: {path.relative_to(ROOT)}")

    if practice_path == PRACTICE_MAP.resolve() and COURSE_PLAN_SYNC.is_file():
        synchronized = subprocess.run(
            [sys.executable, str(COURSE_PLAN_SYNC), "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        if synchronized.returncode:
            errors.append("generated course plan tables are stale")

    if errors:
        print("Coverage validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    i0_count = sum(row["priority"].strip() == "I0" for row in rows)
    total_min = sum(hours[0] for hours in course_hours)
    total_max = sum(hours[1] for hours in course_hours)
    print(
        f"Curriculum coverage is valid: {len(rows)} concepts mapped across "
        f"{len(practice_rows)} project-integrated course blocks; "
        f"{i0_count} required inference/backend concepts; M0-M9 and M2.5 present; "
        f"Release A reaches CPU inference within {sum(h[0] for _, h in release_a)}–"
        f"{sum(h[1] for _, h in release_a)} hours; full plan {total_min}–{total_max} hours; "
        f"source symbols {'verified' if args.verify_symbols else 'declared'} and evidence dimensions checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

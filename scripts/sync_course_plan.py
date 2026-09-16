#!/usr/bin/env python3
"""Render machine-owned course tables from COURSE_PRACTICE_MAP.csv."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = ROOT / "curriculum" / "COURSE_PRACTICE_MAP.csv"
DEFAULT_PLAN = ROOT / "curriculum" / "COURSE_PRACTICE_PLAN.md"

COURSE_START = "<!-- GENERATED COURSE TABLE START -->"
COURSE_END = "<!-- GENERATED COURSE TABLE END -->"
CAPACITY_START = "<!-- GENERATED CAPACITY TABLE START -->"
CAPACITY_END = "<!-- GENERATED CAPACITY TABLE END -->"
RELEASE_START = "<!-- GENERATED RELEASE TABLE START -->"
RELEASE_END = "<!-- GENERATED RELEASE TABLE END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--course-map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def replace_region(text: str, start: str, end: str, body: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"plan must contain exactly one {start!r} and {end!r}")
    prefix, remainder = text.split(start, 1)
    _, suffix = remainder.split(end, 1)
    return f"{prefix}{start}\n{body.rstrip()}\n{end}{suffix}"


def course_table(data: list[dict[str, str]]) -> str:
    lines = [
        "| Course | Milestone | Knowledge taught immediately before use | Learner-owned MiniTorch outcome | Gate evidence |",
        "|---|---|---|---|---|",
    ]
    for row in data:
        lines.append(
            f"| {row['course_id']} {row['title']} | {row['milestone']} | "
            f"{row['knowledge_block']} | {row['immediate_learner_action']} | "
            f"{row['runnable_evidence']} |"
        )
    return "\n".join(lines)


def capacity_table(data: list[dict[str, str]]) -> str:
    lines = [
        "| Course | Focused hours | Dependency/gate | Release |",
        "|---|---:|---|---|",
    ]
    for row in data:
        lines.append(
            f"| {row['course_id']} {row['milestone']} | "
            f"{row['hours_min']}–{row['hours_max']} | {row['dependency_gate']} | "
            f"{row['release']} |"
        )
    return "\n".join(lines)


def release_table(data: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in data:
        grouped[row["release"]].append(row)
    names = {
        "A": "Working CPU inference",
        "B": "Robust eager inference engine",
        "C": "Full source and backend mastery",
    }
    cumulative_min = 0
    cumulative_max = 0
    lines = [
        "| Release | Independently useful outcome | Courses | Increment hours | Cumulative hours |",
        "|---|---|---|---:|---:|",
    ]
    for release in sorted(grouped):
        items = grouped[release]
        minimum = sum(int(row["hours_min"]) for row in items)
        maximum = sum(int(row["hours_max"]) for row in items)
        cumulative_min += minimum
        cumulative_max += maximum
        lines.append(
            f"| {release} | {names[release]} | {items[0]['course_id']}–{items[-1]['course_id']} | "
            f"{minimum}–{maximum} | {cumulative_min}–{cumulative_max} |"
        )
    return "\n".join(lines)


def render(plan: str, data: list[dict[str, str]]) -> str:
    plan = replace_region(plan, COURSE_START, COURSE_END, course_table(data))
    plan = replace_region(plan, CAPACITY_START, CAPACITY_END, capacity_table(data))
    return replace_region(plan, RELEASE_START, RELEASE_END, release_table(data))


def main() -> int:
    args = parse_args()
    try:
        plan_path = args.plan.resolve()
        expected = render(
            plan_path.read_text(encoding="utf-8"), rows(args.course_map.resolve())
        )
        actual = plan_path.read_text(encoding="utf-8")
    except (OSError, KeyError, ValueError) as exc:
        print(f"Cannot synchronize course plan: {exc}", file=sys.stderr)
        return 1
    if args.write:
        plan_path.write_text(expected, encoding="utf-8")
        print(f"Updated generated course tables in {plan_path}")
        return 0
    if actual != expected:
        print(
            "COURSE_PRACTICE_PLAN.md is stale; run scripts/sync_course_plan.py --write",
            file=sys.stderr,
        )
        return 1
    print("Generated course tables are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

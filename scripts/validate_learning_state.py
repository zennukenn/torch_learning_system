#!/usr/bin/env python3
"""Validate durable learning-state files without modifying them."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEARNING = ROOT / "learning"

SCORE_FIELDS = ["explain", "locate", "trace", "debug", "modify", "transfer", "retain"]
HINT_LEVELS = {"H0", "H1", "H2", "H3"}
VERDICTS = {"pass", "partial", "fail", "invalid"}
STATUSES = {"unassessed", "learning", "review", "mastered"}
EVIDENCE_ID = re.compile(r"^E-\d{8}-\d{2,}$")
QUESTION_ID = re.compile(r"^Q-\d{8}-\d{2,}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")

SPECS = {
    "MASTERY.csv": [
        "concept_id", "concept", "phase", *SCORE_FIELDS,
        "last_evidence_id", "status",
    ],
    "EVIDENCE_LOG.csv": [
        "evidence_id", "date", "session", "revision", "concept_id", "dimension",
        "task", "learner_result", "hint_level", "source_or_command", "notebook_path",
        "verdict", "next_review",
    ],
    "QUESTION_HISTORY.csv": [
        "question_id", "date", "concept_id", "question", "conditions",
        "learner_answer", "hint_level", "verdict", "evidence_id", "next_due",
    ],
}

REQUIRED = [
    "PROFILE.md", "STATE.md", "MASTERY.csv", "EVIDENCE_LOG.csv",
    "QUESTION_HISTORY.csv", "REVIEW_QUEUE.md", "SESSION_LOG.md", "ERROR_LOG.md",
    "notebook/INDEX.md", "notebook/MISTAKES.md",
]

MARKERS = {
    "REVIEW_QUEUE.md": "<!-- SESSION_REVIEW_ROWS -->",
    "notebook/INDEX.md": "<!-- SESSION_INDEX_ROWS -->",
    "notebook/MISTAKES.md": "<!-- SESSION_MISTAKE_ROWS -->",
}

REVIEW_HEADER = (
    "| Due policy | Activation milestone | Eligible after | Concept | Dimension | "
    "Last evidence | Hint ceiling | Retrieval prompt | Status |"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--learning-dir",
        type=Path,
        default=DEFAULT_LEARNING,
        help="learning-state directory to validate (default: repository learning/)",
    )
    return parser.parse_args()


def read_rows(path: Path, expected: list[str], errors: list[str]) -> list[dict[str, str]]:
    try:
        handle = path.open(newline="", encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path}: cannot read: {exc}")
        return []

    with handle:
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


def unique_nonempty(
    rows: list[dict[str, str]], key: str, filename: str, errors: list[str]
) -> None:
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        value = row.get(key, "").strip()
        if not value:
            errors.append(f"{filename}:{number}: empty {key}")
        elif value in seen:
            errors.append(f"{filename}:{number}: duplicate {key} {value!r}")
        seen.add(value)


def require_fields(
    rows: list[dict[str, str]], fields: list[str], filename: str, errors: list[str]
) -> None:
    for number, row in enumerate(rows, start=2):
        for field in fields:
            if not row.get(field, "").strip():
                errors.append(f"{filename}:{number}: empty {field}")


def valid_iso_date(value: str, location: str, errors: list[str], *, optional: bool = False) -> None:
    value = value.strip()
    if optional and not value:
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{location}: expected ISO date YYYY-MM-DD, got {value!r}")


def validate(learning: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED:
        if not (learning / name).is_file():
            errors.append(f"missing required file: {learning / name}")
    notebook_sessions = learning / "notebook" / "sessions"
    if not notebook_sessions.is_dir():
        errors.append(f"missing required directory: {notebook_sessions}")
    for relative, marker in MARKERS.items():
        path = learning / relative
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            if content.count(marker) != 1:
                errors.append(f"{relative}: expected exactly one session insertion marker")
    review_path = learning / "REVIEW_QUEUE.md"
    if review_path.is_file() and REVIEW_HEADER not in review_path.read_text(encoding="utf-8"):
        errors.append("REVIEW_QUEUE.md: activation-aware header is missing")

    tables: dict[str, list[dict[str, str]]] = {}
    for name, header in SPECS.items():
        path = learning / name
        if path.is_file():
            tables[name] = read_rows(path, header, errors)

    mastery = tables.get("MASTERY.csv", [])
    unique_nonempty(mastery, "concept_id", "MASTERY.csv", errors)
    require_fields(mastery, ["concept", "phase", "status"], "MASTERY.csv", errors)
    concepts = {row.get("concept_id", "").strip() for row in mastery}

    for number, row in enumerate(mastery, start=2):
        try:
            phase = int(row.get("phase", ""))
            if phase not in range(7):
                errors.append(f"MASTERY.csv:{number}: phase={phase} is outside 0..6")
        except ValueError:
            errors.append(f"MASTERY.csv:{number}: phase is not an integer")

        scores: list[int] = []
        for field in SCORE_FIELDS:
            try:
                score = int(row.get(field, ""))
                scores.append(score)
            except ValueError:
                errors.append(f"MASTERY.csv:{number}: {field} is not an integer")
                continue
            if score not in range(5):
                errors.append(f"MASTERY.csv:{number}: {field}={score} is outside 0..4")

        status = row.get("status", "").strip()
        if status not in STATUSES:
            errors.append(f"MASTERY.csv:{number}: invalid status {status!r}")
        if status == "unassessed" and (any(scores) or row.get("last_evidence_id", "").strip()):
            errors.append(
                f"MASTERY.csv:{number}: unassessed concept cannot have scores or last evidence"
            )

    evidence = tables.get("EVIDENCE_LOG.csv", [])
    questions = tables.get("QUESTION_HISTORY.csv", [])
    unique_nonempty(evidence, "evidence_id", "EVIDENCE_LOG.csv", errors)
    unique_nonempty(questions, "question_id", "QUESTION_HISTORY.csv", errors)
    require_fields(
        evidence,
        [
            "date", "session", "revision", "concept_id", "dimension", "task",
            "learner_result", "hint_level", "source_or_command", "notebook_path",
            "verdict",
        ],
        "EVIDENCE_LOG.csv",
        errors,
    )
    require_fields(
        questions,
        [
            "date", "concept_id", "question", "conditions", "learner_answer",
            "hint_level", "verdict", "evidence_id",
        ],
        "QUESTION_HISTORY.csv",
        errors,
    )

    evidence_rows: dict[str, dict[str, str]] = {}
    session_notes: dict[str, Path] = {}
    note_sessions: dict[Path, str] = {}
    notebook_root = (learning / "notebook" / "sessions").resolve()
    notebook_index_path = learning / "notebook" / "INDEX.md"
    session_log_path = learning / "SESSION_LOG.md"
    notebook_index = (
        notebook_index_path.read_text(encoding="utf-8") if notebook_index_path.is_file() else ""
    )
    session_log = session_log_path.read_text(encoding="utf-8") if session_log_path.is_file() else ""
    for number, row in enumerate(evidence, start=2):
        evidence_id = row.get("evidence_id", "").strip()
        evidence_rows[evidence_id] = row
        if evidence_id and not EVIDENCE_ID.fullmatch(evidence_id):
            errors.append(f"EVIDENCE_LOG.csv:{number}: invalid evidence_id {evidence_id!r}")
        valid_iso_date(row.get("date", ""), f"EVIDENCE_LOG.csv:{number}:date", errors)
        valid_iso_date(
            row.get("next_review", ""),
            f"EVIDENCE_LOG.csv:{number}:next_review",
            errors,
            optional=row.get("verdict", "").strip() == "invalid",
        )
        concept_id = row.get("concept_id", "").strip()
        if concept_id not in concepts:
            errors.append(f"EVIDENCE_LOG.csv:{number}: unknown concept_id {concept_id!r}")
        dimension = row.get("dimension", "").strip()
        if dimension not in SCORE_FIELDS:
            errors.append(f"EVIDENCE_LOG.csv:{number}: invalid dimension {dimension!r}")
        hint = row.get("hint_level", "").strip()
        if hint not in HINT_LEVELS:
            errors.append(f"EVIDENCE_LOG.csv:{number}: invalid hint_level {hint!r}")
        verdict = row.get("verdict", "").strip()
        if verdict not in VERDICTS:
            errors.append(f"EVIDENCE_LOG.csv:{number}: invalid verdict {verdict!r}")
        revision = row.get("revision", "").strip()
        binary_revision = revision.startswith("binary:") and len(revision) > len("binary:")
        if revision and not (COMMIT.fullmatch(revision) or binary_revision):
            errors.append(
                f"EVIDENCE_LOG.csv:{number}: revision must be a 40-character commit or binary:<version>"
            )
        notebook_value = row.get("notebook_path", "").strip()
        notebook_relative = Path(notebook_value)
        has_expected_prefix = notebook_relative.parts[:3] == (
            "learning", "notebook", "sessions"
        )
        candidate = (
            learning.joinpath(*notebook_relative.parts[1:]).resolve()
            if has_expected_prefix
            else learning.parent.joinpath(notebook_relative).resolve()
        )
        try:
            candidate.relative_to(notebook_root)
            inside_notebook = True
        except ValueError:
            inside_notebook = False
        if (
            notebook_relative.is_absolute()
            or ".." in notebook_relative.parts
            or not has_expected_prefix
            or not inside_notebook
            or candidate.suffix != ".md"
        ):
            errors.append(
                f"EVIDENCE_LOG.csv:{number}: notebook_path must be under "
                f"learning/notebook/sessions/: {notebook_value!r}"
            )
        elif not candidate.is_file():
            errors.append(f"EVIDENCE_LOG.csv:{number}: notebook note does not exist: {notebook_value}")
        else:
            session = row.get("session", "").strip()
            previous_note = session_notes.setdefault(session, candidate)
            if previous_note != candidate:
                errors.append(
                    f"EVIDENCE_LOG.csv:{number}: one session references multiple notebook notes"
                )
            previous_session = note_sessions.setdefault(candidate, session)
            if previous_session != session:
                errors.append(
                    f"EVIDENCE_LOG.csv:{number}: one notebook note is shared by multiple sessions"
                )
            note_text = candidate.read_text(encoding="utf-8")
            if "- Status: `complete`" not in note_text:
                errors.append(
                    f"EVIDENCE_LOG.csv:{number}: notebook note is not marked complete"
                )
            if evidence_id not in note_text:
                errors.append(
                    f"EVIDENCE_LOG.csv:{number}: notebook note does not contain {evidence_id}"
                )
            index_reference = candidate.relative_to(learning / "notebook").as_posix()
            if index_reference not in notebook_index:
                errors.append(
                    f"EVIDENCE_LOG.csv:{number}: notebook index does not link {index_reference}"
                )
            if notebook_value not in session_log:
                errors.append(
                    f"EVIDENCE_LOG.csv:{number}: SESSION_LOG.md does not link {notebook_value}"
                )

    for number, row in enumerate(questions, start=2):
        question_id = row.get("question_id", "").strip()
        if question_id and not QUESTION_ID.fullmatch(question_id):
            errors.append(f"QUESTION_HISTORY.csv:{number}: invalid question_id {question_id!r}")
        valid_iso_date(row.get("date", ""), f"QUESTION_HISTORY.csv:{number}:date", errors)
        valid_iso_date(
            row.get("next_due", ""),
            f"QUESTION_HISTORY.csv:{number}:next_due",
            errors,
            optional=row.get("verdict", "").strip() == "invalid",
        )
        concept_id = row.get("concept_id", "").strip()
        if concept_id not in concepts:
            errors.append(f"QUESTION_HISTORY.csv:{number}: unknown concept_id {concept_id!r}")
        hint = row.get("hint_level", "").strip()
        if hint not in HINT_LEVELS:
            errors.append(f"QUESTION_HISTORY.csv:{number}: invalid hint_level {hint!r}")
        verdict = row.get("verdict", "").strip()
        if verdict not in VERDICTS:
            errors.append(f"QUESTION_HISTORY.csv:{number}: invalid verdict {verdict!r}")
        evidence_id = row.get("evidence_id", "").strip()
        if evidence_id not in evidence_rows:
            errors.append(f"QUESTION_HISTORY.csv:{number}: unknown evidence_id {evidence_id!r}")
        elif evidence_rows[evidence_id].get("concept_id", "").strip() != concept_id:
            errors.append(f"QUESTION_HISTORY.csv:{number}: concept_id does not match {evidence_id}")

    mistakes_path = learning / "notebook" / "MISTAKES.md"
    mistakes = mistakes_path.read_text(encoding="utf-8") if mistakes_path.is_file() else ""
    for number, row in enumerate(questions, start=2):
        if row.get("verdict", "").strip() not in {"partial", "fail"}:
            continue
        question_id = row.get("question_id", "").strip()
        if question_id and question_id not in mistakes:
            errors.append(
                f"QUESTION_HISTORY.csv:{number}: {question_id} is missing from notebook/MISTAKES.md"
            )

    for number, row in enumerate(mastery, start=2):
        concept_id = row.get("concept_id", "").strip()
        evidence_id = row.get("last_evidence_id", "").strip()
        numeric_scores = [
            int(row[field]) for field in SCORE_FIELDS if row.get(field, "").isdigit()
        ]
        if not evidence_id:
            if any(numeric_scores):
                errors.append(f"MASTERY.csv:{number}: nonzero score requires last_evidence_id")
            continue
        if evidence_id not in evidence_rows:
            errors.append(f"MASTERY.csv:{number}: unknown last_evidence_id {evidence_id!r}")
        elif evidence_rows[evidence_id].get("concept_id", "").strip() != concept_id:
            errors.append(f"MASTERY.csv:{number}: last evidence belongs to another concept")

    return errors


def main() -> int:
    learning = parse_args().learning_dir.resolve()
    errors = validate(learning)
    if errors:
        print("Learning-state validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    counts: list[int] = []
    for name in ("MASTERY.csv", "EVIDENCE_LOG.csv", "QUESTION_HISTORY.csv"):
        with (learning / name).open(newline="", encoding="utf-8") as handle:
            counts.append(sum(1 for _ in csv.DictReader(handle)))
    print(
        "Learning state is valid: "
        f"{counts[0]} mastery concepts, {counts[1]} evidence rows, "
        f"{counts[2]} question rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

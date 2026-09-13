#!/usr/bin/env python3
"""Generate one completed learning-session update from a reviewed JSON manifest."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEARNING = ROOT / "learning"
VALIDATOR = ROOT / "scripts" / "validate_learning_state.py"
SCORE_FIELDS = {"explain", "locate", "trace", "debug", "modify", "transfer", "retain"}
HINT_LEVELS = {"H0", "H1", "H2", "H3"}
VERDICTS = {"pass", "partial", "fail", "invalid"}
STATUSES = {"unassessed", "learning", "review", "mastered"}
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
EVIDENCE_ID = re.compile(r"^E-\d{8}-\d{2,}$")
QUESTION_ID = re.compile(r"^Q-\d{8}-\d{2,}$")

STATE_FILES = [
    "MASTERY.csv",
    "EVIDENCE_LOG.csv",
    "QUESTION_HISTORY.csv",
    "REVIEW_QUEUE.md",
    "SESSION_LOG.md",
    "STATE.md",
    "notebook/INDEX.md",
    "notebook/MISTAKES.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--learning-dir", type=Path, default=DEFAULT_LEARNING)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the already validated staged result; default is a dry run",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("manifest root must be a JSON object")
    return value


def text_field(value: Any, location: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{location} must be a nonempty string")
        return ""
    return value.strip()


def list_field(value: Any, location: str, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        errors.append(f"{location} must be a nonempty list")
        return []
    if any(not isinstance(item, dict) for item in value):
        errors.append(f"every {location} item must be an object")
        return []
    return value


def valid_date(value: str, location: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{location} must use YYYY-MM-DD")


def validate_manifest(manifest: dict[str, Any], learning: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "date", "session", "phase", "milestone", "topic", "pytorch_revision",
        "minitorch_revision", "note_slug", "outcome", "learner_teach_back",
        "gap_audit", "mentor_supplement", "verification", "next_action",
    ]
    values = {field: text_field(manifest.get(field), field, errors) for field in required}
    if values["date"]:
        valid_date(values["date"], "date", errors)
    if values["pytorch_revision"] and not COMMIT.fullmatch(values["pytorch_revision"]):
        errors.append("pytorch_revision must be a 40-character commit")
    if values["note_slug"] and not SLUG.fullmatch(values["note_slug"]):
        errors.append("note_slug must contain lowercase letters, digits and hyphens only")

    note = learning / "notebook" / "sessions" / f"{values['date']}-{values['note_slug']}.md"
    artifact = learning / "artifacts" / f"{values['date']}-{values['note_slug']}"
    if note.exists():
        errors.append(f"session note already exists: {note}")
    if artifact.exists():
        errors.append(f"session artifact directory already exists: {artifact}")

    evidence = list_field(manifest.get("evidence"), "evidence", errors)
    questions = list_field(manifest.get("questions"), "questions", errors)
    updates = list_field(manifest.get("mastery_updates"), "mastery_updates", errors)
    reviews = list_field(manifest.get("reviews"), "reviews", errors)

    with (learning / "MASTERY.csv").open(newline="", encoding="utf-8") as handle:
        concepts = {row["concept_id"] for row in csv.DictReader(handle)}
    evidence_map: dict[str, str] = {}
    for index, row in enumerate(evidence):
        prefix = f"evidence[{index}]"
        fields = [
            "evidence_id", "concept_id", "dimension", "task", "learner_result",
            "hint_level", "source_or_command", "verdict", "next_review",
        ]
        item = {field: text_field(row.get(field), f"{prefix}.{field}", errors) for field in fields}
        if item["evidence_id"] and not EVIDENCE_ID.fullmatch(item["evidence_id"]):
            errors.append(f"{prefix}.evidence_id is malformed")
        if item["evidence_id"] in evidence_map:
            errors.append(f"duplicate manifest evidence_id {item['evidence_id']}")
        evidence_map[item["evidence_id"]] = item["concept_id"]
        if item["concept_id"] not in concepts:
            errors.append(f"{prefix}.concept_id is unknown")
        if item["dimension"] not in SCORE_FIELDS:
            errors.append(f"{prefix}.dimension is invalid")
        if item["hint_level"] not in HINT_LEVELS:
            errors.append(f"{prefix}.hint_level is invalid")
        if item["verdict"] not in VERDICTS:
            errors.append(f"{prefix}.verdict is invalid")
        if item["next_review"]:
            valid_date(item["next_review"], f"{prefix}.next_review", errors)

    question_ids: set[str] = set()
    for index, row in enumerate(questions):
        prefix = f"questions[{index}]"
        fields = [
            "question_id", "concept_id", "question", "conditions", "learner_answer",
            "hint_level", "verdict", "evidence_id", "next_due",
        ]
        item = {field: text_field(row.get(field), f"{prefix}.{field}", errors) for field in fields}
        if item["question_id"] and not QUESTION_ID.fullmatch(item["question_id"]):
            errors.append(f"{prefix}.question_id is malformed")
        if item["question_id"] in question_ids:
            errors.append(f"duplicate manifest question_id {item['question_id']}")
        question_ids.add(item["question_id"])
        if item["concept_id"] not in concepts:
            errors.append(f"{prefix}.concept_id is unknown")
        if evidence_map.get(item["evidence_id"]) != item["concept_id"]:
            errors.append(f"{prefix}.evidence_id must reference same-concept manifest evidence")
        if item["hint_level"] not in HINT_LEVELS:
            errors.append(f"{prefix}.hint_level is invalid")
        if item["verdict"] not in VERDICTS:
            errors.append(f"{prefix}.verdict is invalid")
        if item["next_due"]:
            valid_date(item["next_due"], f"{prefix}.next_due", errors)
        if values["milestone"] and values["milestone"] not in item["conditions"]:
            errors.append(f"{prefix}.conditions must name milestone {values['milestone']!r}")
        if item["verdict"] in {"partial", "fail"}:
            text_field(row.get("correction_evidence"), f"{prefix}.correction_evidence", errors)
            text_field(row.get("mistake_status"), f"{prefix}.mistake_status", errors)

    for index, row in enumerate(updates):
        prefix = f"mastery_updates[{index}]"
        concept = text_field(row.get("concept_id"), f"{prefix}.concept_id", errors)
        dimension = text_field(row.get("dimension"), f"{prefix}.dimension", errors)
        evidence_id = text_field(row.get("evidence_id"), f"{prefix}.evidence_id", errors)
        status = text_field(row.get("status"), f"{prefix}.status", errors)
        score = row.get("score")
        if concept not in concepts or evidence_map.get(evidence_id) != concept:
            errors.append(f"{prefix} must reference matching concept and manifest evidence")
        if dimension not in SCORE_FIELDS:
            errors.append(f"{prefix}.dimension is invalid")
        if not isinstance(score, int) or score not in range(5):
            errors.append(f"{prefix}.score must be an integer from 0 to 4")
        if status not in STATUSES:
            errors.append(f"{prefix}.status is invalid")

    review_fields = [
        "due_policy", "activation_milestone", "eligible_after", "concept_id",
        "dimension", "evidence_id", "hint_ceiling", "prompt", "status",
    ]
    for index, row in enumerate(reviews):
        prefix = f"reviews[{index}]"
        item = {field: text_field(row.get(field), f"{prefix}.{field}", errors) for field in review_fields}
        if item["concept_id"] not in concepts:
            errors.append(f"{prefix}.concept_id is unknown")
        if item["dimension"] not in SCORE_FIELDS:
            errors.append(f"{prefix}.dimension is invalid")
        if evidence_map.get(item["evidence_id"]) != item["concept_id"]:
            errors.append(f"{prefix}.evidence_id must reference same-concept manifest evidence")
        if item["hint_ceiling"] not in HINT_LEVELS:
            errors.append(f"{prefix}.hint_ceiling is invalid")

    state_updates = manifest.get("state_updates")
    if not isinstance(state_updates, dict) or not state_updates:
        errors.append("state_updates must be a nonempty object")
    else:
        state_text = (learning / "STATE.md").read_text(encoding="utf-8")
        for key, value in state_updates.items():
            if (
                not isinstance(key, str)
                or not isinstance(value, str)
                or not value.strip()
                or "\n" in key
                or "\n" in value
            ):
                errors.append("state_updates keys and values must be nonempty strings")
            elif f"- {key}:" not in state_text:
                errors.append(f"state_updates key does not match an existing STATE bullet: {key!r}")
    return errors


def append_csv(path: Path, row: dict[str, Any]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = csv.DictReader(handle).fieldnames
    if fieldnames is None:
        raise RuntimeError(f"missing CSV header: {path}")
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames).writerow(row)


def mdcell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def insert_before_marker(path: Path, marker: str, row: str) -> None:
    content = path.read_text(encoding="utf-8")
    token = f"<!-- {marker} -->"
    if content.count(token) != 1:
        raise RuntimeError(f"{path} must contain exactly one {token}")
    path.write_text(content.replace(token, row + token), encoding="utf-8")


def update_mastery(path: Path, updates: list[dict[str, Any]]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    assert fields is not None
    by_concept = {row["concept_id"]: row for row in rows}
    for update in updates:
        row = by_concept[update["concept_id"]]
        row[update["dimension"]] = str(update["score"])
        row["last_evidence_id"] = update["evidence_id"]
        row["status"] = update["status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def update_state(path: Path, updates: dict[str, str]) -> None:
    content = path.read_text(encoding="utf-8")
    for key, value in updates.items():
        content, count = re.subn(
            rf"^- {re.escape(key)}:.*$", f"- {key}: {value}", content, count=1, flags=re.M
        )
        if count != 1:
            raise RuntimeError(f"could not update STATE key {key!r}")
    path.write_text(content, encoding="utf-8")


def render_session(stage: Path, manifest: dict[str, Any]) -> tuple[Path, Path]:
    day = manifest["date"]
    slug = manifest["note_slug"]
    note_relative = f"learning/notebook/sessions/{day}-{slug}.md"
    note = stage / "notebook" / "sessions" / f"{day}-{slug}.md"
    evidence_ids = ", ".join(item["evidence_id"] for item in manifest["evidence"])
    note.write_text(
        f"# {day} — {manifest['topic']}\n\n"
        "- Status: `complete`\n"
        f"- Milestone: `{manifest['milestone']}`\n"
        f"- PyTorch revision: `{manifest['pytorch_revision']}`\n"
        f"- MiniTorch revision/diff: `{manifest['minitorch_revision']}`\n"
        f"- Evidence IDs: {evidence_ids}\n\n"
        "## Learner teach-back before feedback\n\n"
        f"{manifest['learner_teach_back']}\n\n"
        "## Gap audit\n\n"
        f"{manifest['gap_audit']}\n\n"
        "## Focused verification\n\n"
        f"{manifest['verification']}\n\n"
        "## Mentor supplement (not mastery evidence)\n\n"
        f"{manifest['mentor_supplement']}\n",
        encoding="utf-8",
    )
    artifact = stage / "artifacts" / f"{day}-{slug}"
    artifact.mkdir(parents=True)
    (artifact / "SESSION_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    insert_before_marker(
        stage / "notebook" / "INDEX.md",
        "SESSION_INDEX_ROWS",
        f"| {mdcell(day)} | complete | {mdcell(manifest['phase'])} | "
        f"{mdcell(manifest['topic'])} | "
        f"{mdcell(', '.join(sorted({e['concept_id'] for e in manifest['evidence']})))} | "
        f"{mdcell(evidence_ids)} | [note](sessions/{day}-{slug}.md) |\n",
    )
    with (stage / "SESSION_LOG.md").open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {day} — {manifest['topic']}\n\n"
            f"- PyTorch reference revision: `{manifest['pytorch_revision']}`\n"
            f"- MiniTorch revision/diff: {manifest['minitorch_revision']}\n"
            f"- Milestone/increment: {manifest['milestone']}\n"
            f"- Outcome: {manifest['outcome']}\n"
            f"- Learner artifact: `learning/artifacts/{day}-{slug}/SESSION_MANIFEST.json`\n"
            f"- Notebook: {note_relative}\n"
            f"- Next action: {manifest['next_action']}\n"
        )
    return note, artifact


def apply_to_stage(stage: Path, manifest: dict[str, Any]) -> tuple[Path, Path]:
    note_path = f"learning/notebook/sessions/{manifest['date']}-{manifest['note_slug']}.md"
    for item in manifest["evidence"]:
        append_csv(
            stage / "EVIDENCE_LOG.csv",
            {
                **item,
                "date": manifest["date"],
                "session": manifest["session"],
                "revision": manifest["pytorch_revision"],
                "notebook_path": note_path,
            },
        )
    for item in manifest["questions"]:
        append_csv(
            stage / "QUESTION_HISTORY.csv",
            {
                key: value
                for key, value in {
                    **item,
                    "date": manifest["date"],
                }.items()
                if key not in {"correction_evidence", "mistake_status"}
            },
        )
    update_mastery(stage / "MASTERY.csv", manifest["mastery_updates"])
    note, artifact = render_session(stage, manifest)

    for item in manifest["questions"]:
        if item["verdict"] not in {"partial", "fail"}:
            continue
        insert_before_marker(
            stage / "notebook" / "MISTAKES.md",
            "SESSION_MISTAKE_ROWS",
            f"| {mdcell(item['question_id'])} | {mdcell(manifest['date'])} | "
            f"{mdcell(item['concept_id'])} | {mdcell(item['question'])} | "
            f"{mdcell(item['learner_answer'])} | {mdcell(item['correction_evidence'])} | "
            f"{mdcell(item['evidence_id'])} | {mdcell(item['next_due'])} | "
            f"{mdcell(item['mistake_status'])} | [note](sessions/{note.name}) |\n",
        )
    for item in manifest["reviews"]:
        insert_before_marker(
            stage / "REVIEW_QUEUE.md",
            "SESSION_REVIEW_ROWS",
            "| " + " | ".join(
                mdcell(item[key])
                for key in [
                    "due_policy", "activation_milestone", "eligible_after", "concept_id",
                    "dimension", "evidence_id", "hint_ceiling", "prompt", "status",
                ]
            ) + " |\n",
        )
    update_state(stage / "STATE.md", manifest["state_updates"])
    return note, artifact


def copy_validated_result(stage: Path, learning: Path, note: Path, artifact: Path) -> None:
    target_note = learning / "notebook" / "sessions" / note.name
    target_artifact = learning / "artifacts" / artifact.name
    if target_note.exists() or target_artifact.exists():
        raise RuntimeError("session output appeared during staging; refusing to overwrite")
    shutil.copy2(note, target_note)
    shutil.copytree(artifact, target_artifact)
    for relative in STATE_FILES:
        shutil.copy2(stage / relative, learning / relative)


def main() -> int:
    args = parse_args()
    learning = args.learning_dir.resolve()
    try:
        manifest = load_manifest(args.manifest.resolve())
        errors = validate_manifest(manifest, learning)
    except (ValueError, OSError, KeyError) as exc:
        errors = [str(exc)]
        manifest = {}
    if errors:
        print("Session manifest is invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.apply and manifest.get("example_only") is True:
        print(
            "Session manifest is an example; copy it and set example_only to false before --apply.",
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory(prefix="learning-session-stage-") as directory:
        stage = Path(directory) / "learning"
        shutil.copytree(learning, stage)
        note, artifact = apply_to_stage(stage, manifest)
        checked = subprocess.run(
            [sys.executable, str(VALIDATOR), "--learning-dir", str(stage)],
            text=True,
            capture_output=True,
            check=False,
        )
        if checked.returncode:
            print("Generated learning state is invalid:", file=sys.stderr)
            print(checked.stderr.rstrip(), file=sys.stderr)
            return 1
        if args.apply:
            copy_validated_result(stage, learning, note, artifact)

    verb = "applied" if args.apply else "dry-run validated"
    print(
        f"Session {manifest['session']} {verb}: {len(manifest['evidence'])} evidence, "
        f"{len(manifest['questions'])} questions, {len(manifest['mastery_updates'])} mastery updates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

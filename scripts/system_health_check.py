#!/usr/bin/env python3
"""Run a non-destructive end-to-end health check of the learning system."""

from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEARNING = ROOT / "learning"
SOURCE = ROOT / "sources" / "pytorch"
VALIDATOR = ROOT / "scripts" / "validate_learning_state.py"

REQUIRED_PATHS = [
    "AGENTS.md",
    ".agents/skills/pytorch-source-mentor/SKILL.md",
    ".agents/skills/pytorch-source-mentor/agents/openai.yaml",
    ".agents/skills/pytorch-source-mentor/references/session-protocol.md",
    ".agents/skills/pytorch-source-mentor/references/foundation-teaching.md",
    ".agents/skills/pytorch-source-mentor/references/source-evidence.md",
    ".agents/skills/pytorch-source-mentor/references/assessment.md",
    ".agents/skills/pytorch-source-mentor/references/backend-lab.md",
    "config/PYTORCH_SOURCE_PIN",
    "curriculum/ROADMAP.md",
    "curriculum/KNOWLEDGE_GRAPH.md",
    "curriculum/ASSESSMENT_BLUEPRINT.md",
    "projects/ROADMAP.md",
    "prompts/CHATGPT_SYSTEM_PROMPT.md",
    "prompts/QUICK_PROMPTS.md",
    "templates/SESSION.md",
    "templates/FOUNDATION_MAP.md",
    "templates/CALL_CHAIN.md",
    "templates/SYNTAX_NOTE.md",
    "templates/WEEKLY_REVIEW.md",
    "templates/BACKEND_COMPATIBILITY.md",
    "templates/LEARNING_NOTE.md",
    "scripts/checkout_pytorch_source.sh",
    "learning/artifacts/.gitkeep",
    "learning/notebook/INDEX.md",
    "learning/notebook/MISTAKES.md",
    "learning/notebook/sessions/.gitkeep",
]

TRACE_ANCHORS = {
    "aten/src/ATen/native/native_functions.yaml": "ufunc_inner_loop:",
    "aten/src/ATen/native/ufunc/add.h": "T add(",
    "torchgen/api/ufunc.py": "def ufunc_arguments",
    "torchgen/dest/ufunc.py": "def compute_ufunc_cpu",
    "torchgen/gen.py": "UfuncCPU_",
}


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        check=False,
        capture_output=capture,
    )


def learning_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in LEARNING.rglob("*") if p.is_file()):
        digest.update(path.relative_to(LEARNING).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def append_csv(path: Path, row: dict[str, str]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = csv.DictReader(handle).fieldnames
    if fieldnames is None:
        raise RuntimeError(f"missing CSV header: {path}")
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def update_synthetic_mastery(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if fieldnames is None:
        raise RuntimeError("MASTERY.csv has no header")
    for row in rows:
        if row["concept_id"] == "BIND-CODEGEN":
            row["locate"] = "1"
            row["last_evidence_id"] = "E-20990101-01"
            row["status"] = "learning"
            break
    else:
        raise RuntimeError("BIND-CODEGEN concept is missing")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def simulate_new_user_session(temp_learning: Path, revision: str) -> None:
    append_csv(
        temp_learning / "EVIDENCE_LOG.csv",
        {
            "evidence_id": "E-20990101-01",
            "date": "2099-01-01",
            "session": "synthetic-health-check",
            "revision": revision,
            "concept_id": "BIND-CODEGEN",
            "dimension": "locate",
            "task": "Predict and locate the generated torch.add path",
            "learner_result": "Synthetic learner needed H2 to replace a stale hand-written-kernel prediction",
            "hint_level": "H2",
            "source_or_command": "native_functions.yaml; torchgen/api/ufunc.py; rg ufunc_inner_loop",
            "notebook_path": "learning/notebook/sessions/2099-01-01-synthetic-health-check.md",
            "verdict": "partial",
            "next_review": "2099-01-02",
        },
    )
    append_csv(
        temp_learning / "QUESTION_HISTORY.csv",
        {
            "question_id": "Q-20990101-01",
            "date": "2099-01-01",
            "concept_id": "BIND-CODEGEN",
            "question": "Where is the current torch.add CPU implementation path generated?",
            "conditions": "Source-only; runtime unavailable; H2 permitted",
            "learner_answer": "Synthetic prediction pointed first to a hand-written BinaryOps kernel",
            "hint_level": "H2",
            "verdict": "partial",
            "evidence_id": "E-20990101-01",
            "next_due": "2099-01-02",
        },
    )
    update_synthetic_mastery(temp_learning / "MASTERY.csv")

    note_relative = "learning/notebook/sessions/2099-01-01-synthetic-health-check.md"
    note = temp_learning / "notebook" / "sessions" / "2099-01-01-synthetic-health-check.md"
    note.write_text(
        "# Synthetic learning note\n\n"
        "- Status: `complete`\n"
        "- Evidence IDs: E-20990101-01\n\n"
        "## Learner teach-back before feedback\n\n"
        "The synthetic learner predicted a hand-written CPU kernel.\n\n"
        "## Gap audit\n\n"
        "The ufunc code-generation layer was missing and corrected after H2.\n\n"
        "## Mentor supplement (not mastery evidence)\n\n"
        "Runtime dispatch remains unverified.\n",
        encoding="utf-8",
    )
    with (temp_learning / "notebook" / "INDEX.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n| 2099-01-01 | complete | Phase 0 | synthetic add trace | BIND-CODEGEN | "
            "E-20990101-01 | [note](sessions/2099-01-01-synthetic-health-check.md) |\n"
        )
    with (temp_learning / "notebook" / "MISTAKES.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "| Q-20990101-01 | 2099-01-01 | BIND-CODEGEN | Where is add generated? | hand-written kernel | "
            "ufunc schema/generator | E-20990101-01 | 2099-01-02 | open | "
            "[note](sessions/2099-01-01-synthetic-health-check.md) |\n"
        )

    artifacts = temp_learning / "artifacts" / "2099-01-01-synthetic-health-check"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "CALL_CHAIN.md").write_text(
        "# Synthetic call chain\n\nThis file exists only inside the temporary health check.\n",
        encoding="utf-8",
    )
    with (temp_learning / "SESSION_LOG.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 2099-01-01 — synthetic health check\n\n"
            "- Revision: temporary simulation\n"
            "- Outcome: state write path exercised\n"
            f"- Notebook: {note_relative}\n"
            "- Next action: temporary data must be deleted\n"
        )
    with (temp_learning / "REVIEW_QUEUE.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n| 2099-01-02 | BIND-CODEGEN | locate | E-20990101-01 | H1 | "
            "Locate the ufunc generator | due |\n"
        )
    with (temp_learning / "ERROR_LOG.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "| 2099-01-01 | generated kernel location | hand-written CPU kernel | "
            "ufunc schema and generator | generated/manual distinction | 2099-01-02 | no |\n"
        )
    with (temp_learning / "STATE.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n<!-- synthetic health check: next action is delayed H1 retrieval; temporary only -->\n"
        )


def main() -> int:
    errors: list[str] = []
    print("[1/6] Checking system structure")
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing system file: {relative}")

    skill = ROOT / ".agents/skills/pytorch-source-mentor/SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\nname: pytorch-source-mentor\n"):
            errors.append("skill frontmatter name is missing or malformed")

    print("[2/6] Checking pinned independent PyTorch checkout")
    source_check = run(["bash", "scripts/check_source_checkout.sh"], capture=True)
    if source_check.returncode:
        errors.append("source checkout gate failed:\n" + source_check.stderr.strip())
    else:
        print(source_check.stdout.rstrip())

    ignored = run(["git", "check-ignore", "-q", "sources/pytorch"])
    if ignored.returncode != 0:
        errors.append("sources/pytorch is not ignored by the learning-system repository")
    tracked = run(["git", "ls-files", "--error-unmatch", "sources/pytorch"], capture=True)
    if tracked.returncode == 0:
        errors.append("sources/pytorch is incorrectly tracked by the learning-system repository")

    print("[3/6] Checking representative current-revision source trace")
    for relative, marker in TRACE_ANCHORS.items():
        path = SOURCE / relative
        if not path.is_file():
            errors.append(f"missing torch.add trace anchor: {relative}")
        elif marker not in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"trace marker {marker!r} missing from {relative}")

    print("[4/6] Validating real learning state")
    real_validation = run([sys.executable, str(VALIDATOR)], capture=True)
    if real_validation.returncode:
        errors.append("real learning state is invalid:\n" + real_validation.stderr.strip())
    else:
        print(real_validation.stdout.rstrip())

    print("[5/6] Simulating a complete state update in an isolated directory")
    pin_path = ROOT / "config/PYTORCH_SOURCE_PIN"
    pin_parts = pin_path.read_text(encoding="utf-8").split() if pin_path.is_file() else []
    revision = pin_parts[1] if len(pin_parts) == 2 else ""
    can_simulate = (
        real_validation.returncode == 0
        and LEARNING.is_dir()
        and re.fullmatch(r"[0-9a-f]{40}", revision) is not None
    )
    if not can_simulate:
        errors.append("synthetic state lifecycle could not run because its prerequisites failed")

    temp_path: Path | None = None
    if can_simulate:
        before = learning_digest()
        with tempfile.TemporaryDirectory(prefix="pytorch-learning-system-") as directory:
            temp_path = Path(directory)
            temp_learning = temp_path / "learning"
            shutil.copytree(LEARNING, temp_learning)
            simulate_new_user_session(temp_learning, revision)
            simulated = run(
                [sys.executable, str(VALIDATOR), "--learning-dir", str(temp_learning)],
                capture=True,
            )
            if simulated.returncode:
                errors.append(
                    "synthetic session state failed validation:\n" + simulated.stderr.strip()
                )

            append_csv(
                temp_learning / "EVIDENCE_LOG.csv",
                {
                    "evidence_id": "E-20990101-02",
                    "date": "2099-01-01",
                    "session": "synthetic-negative-check",
                    "revision": revision,
                    "concept_id": "NOT-A-CONCEPT",
                    "dimension": "locate",
                    "task": "Ensure invalid references are rejected",
                    "learner_result": "Synthetic invalid row",
                    "hint_level": "H0",
                    "source_or_command": "validator negative test",
                    "notebook_path": "learning/notebook/sessions/2099-01-01-synthetic-health-check.md",
                    "verdict": "fail",
                    "next_review": "2099-01-02",
                },
            )
            append_csv(
                temp_learning / "QUESTION_HISTORY.csv",
                {
                    "question_id": "Q-20990101-02",
                    "date": "2099-01-01",
                    "concept_id": "NOT-A-CONCEPT",
                    "question": "Ensure missing mistake-note coverage is rejected",
                    "conditions": "Synthetic negative test",
                    "learner_answer": "Synthetic invalid answer",
                    "hint_level": "H0",
                    "verdict": "fail",
                    "evidence_id": "E-20990101-02",
                    "next_due": "2099-01-02",
                },
            )
            rejected = run(
                [sys.executable, str(VALIDATOR), "--learning-dir", str(temp_learning)],
                capture=True,
            )
            expected_rejections = [
                "unknown concept_id",
                "notebook note does not contain E-20990101-02",
                "Q-20990101-02 is missing from notebook/MISTAKES.md",
            ]
            if rejected.returncode == 0 or any(
                marker not in rejected.stderr for marker in expected_rejections
            ):
                errors.append(
                    "validator did not reject synthetic concept, note, and mistake-link errors"
                )

        if temp_path is None or temp_path.exists():
            errors.append("temporary simulated learning records were not removed")
        if learning_digest() != before:
            errors.append("real learning state changed during the isolated simulation")

    print("[6/6] Confirming simulation cleanup")
    if errors:
        print("System health check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PASS: structure, source pin, source trace, teach-back note lifecycle, "
        "mistake linkage, rejection, and cleanup all passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

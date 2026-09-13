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
COVERAGE_VALIDATOR = ROOT / "scripts" / "validate_curriculum_coverage.py"

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
    "curriculum/COVERAGE_AUDIT.md",
    "curriculum/COVERAGE_MATRIX.csv",
    "projects/MINITORCH_SPEC.md",
    "projects/INFERENCE_SCOPE.md",
    "projects/PRIVATEUSE_BACKEND_SPEC.md",
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
    "templates/MINITORCH_MILESTONE.md",
    "scripts/checkout_pytorch_source.sh",
    "scripts/validate_curriculum_coverage.py",
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

PRIVATEUSE_ANCHORS = {
    "torch/utils/backend_registration.py": "rename_privateuse1_backend",
    "test/cpp_extensions/open_registration_extension/torch_openreg/README.md": "Minimality Principle",
    "test/cpp_extensions/open_registration_extension/torch_openreg/csrc/runtime/OpenRegGuard.cpp": "C10_REGISTER_GUARD_IMPL",
    "test/cpp_extensions/open_registration_extension/torch_openreg/csrc/runtime/OpenRegDeviceAllocator.cpp": "REGISTER_ALLOCATOR",
    "test/cpp_extensions/open_registration_extension/torch_openreg/csrc/aten/OpenRegMinimal.cpp": "TORCH_LIBRARY_IMPL",
}


def run(
    command: list[str], *, capture: bool = False, cwd: Path = ROOT
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
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


def simulation_python() -> Path:
    """Prefer the prepared Python that has development headers."""
    prepared = Path("/root/miniconda3/bin/python")
    return prepared if prepared.is_file() else Path(sys.executable)


def build_synthetic_minitorch(temp_root: Path) -> str:
    """Build and import one tiny native extension in an isolated Git repository."""
    project = temp_root / "mini-torch"
    package = project / "minitorch"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text(
        'from ._C import native_smoke\n\n__all__ = ["native_smoke"]\n',
        encoding="utf-8",
    )
    (project / "binding.cpp").write_text(
        "#include <pybind11/pybind11.h>\n\n"
        "PYBIND11_MODULE(_C, module) {\n"
        '  module.def("native_smoke", []() { return 42; });\n'
        "}\n",
        encoding="utf-8",
    )
    (project / "pyproject.toml").write_text(
        "[build-system]\n"
        'requires = ["scikit-build-core", "pybind11"]\n'
        'build-backend = "scikit_build_core.build"\n\n'
        "[project]\n"
        'name = "minitorch-learning-smoke"\n'
        'version = "0.0.0"\n',
        encoding="utf-8",
    )
    initialized = run(["git", "init", "-q"], capture=True, cwd=project)
    if initialized.returncode:
        raise RuntimeError("temporary MiniTorch git init failed: " + initialized.stderr.strip())

    python = simulation_python()
    configuration = run(
        [
            str(python),
            "-c",
            "import sysconfig; "
            "print(sysconfig.get_paths()['include']); "
            "print(sysconfig.get_config_var('EXT_SUFFIX'))",
        ],
        capture=True,
        cwd=project,
    )
    if configuration.returncode:
        raise RuntimeError("Python build configuration lookup failed")
    values = configuration.stdout.splitlines()
    if len(values) != 2 or not values[1]:
        raise RuntimeError("Python build configuration is incomplete")
    python_include, extension_suffix = values

    compiler = shutil.which("c++")
    pybind_include = SOURCE / "third_party" / "pybind11" / "include"
    if compiler is None:
        raise RuntimeError("c++ compiler is unavailable")
    if not (pybind_include / "pybind11" / "pybind11.h").is_file():
        raise RuntimeError("pinned PyTorch vendored pybind11 headers are unavailable")
    extension = package / f"_C{extension_suffix}"
    compiled = run(
        [
            compiler,
            "-O0",
            "-g",
            "-shared",
            "-std=c++17",
            "-fPIC",
            f"-I{python_include}",
            f"-I{pybind_include}",
            "binding.cpp",
            "-o",
            str(extension),
        ],
        capture=True,
        cwd=project,
    )
    if compiled.returncode:
        raise RuntimeError("temporary native extension compile failed:\n" + compiled.stderr.strip())

    imported = run(
        [str(python), "-c", "import minitorch; assert minitorch.native_smoke() == 42"],
        capture=True,
        cwd=project,
    )
    if imported.returncode:
        raise RuntimeError("temporary import minitorch failed:\n" + imported.stderr.strip())
    staged = run(
        ["git", "add", "binding.cpp", "minitorch/__init__.py", "pyproject.toml"],
        capture=True,
        cwd=project,
    )
    if staged.returncode:
        raise RuntimeError("temporary MiniTorch diff preparation failed")
    diff = run(["git", "diff", "--cached", "--name-only"], capture=True, cwd=project)
    expected = {"binding.cpp", "minitorch/__init__.py", "pyproject.toml"}
    if diff.returncode or set(diff.stdout.splitlines()) != expected:
        raise RuntimeError("temporary learner-authored diff is incomplete")
    return f"{Path(compiler).name} + vendored pybind11 + {python.name}"


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
        if row["concept_id"] == "BUILD-PACKAGING":
            row["trace"] = "1"
            row["last_evidence_id"] = "E-20990101-01"
            row["status"] = "learning"
            break
    else:
        raise RuntimeError("BUILD-PACKAGING concept is missing")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def simulate_new_user_session(temp_learning: Path, revision: str, build_summary: str) -> None:
    append_csv(
        temp_learning / "EVIDENCE_LOG.csv",
        {
            "evidence_id": "E-20990101-01",
            "date": "2099-01-01",
            "session": "synthetic-health-check",
            "revision": revision,
            "concept_id": "BUILD-PACKAGING",
            "dimension": "trace",
            "task": "Build a temporary native extension and trace import minitorch to minitorch._C",
            "learner_result": "Synthetic learner explained the staged project diff and the passing native_smoke import",
            "hint_level": "H0",
            "source_or_command": f"temporary independent Git repository; {build_summary}; native_smoke == 42",
            "notebook_path": "learning/notebook/sessions/2099-01-01-synthetic-health-check.md",
            "verdict": "pass",
            "next_review": "2099-01-08",
        },
    )
    append_csv(
        temp_learning / "QUESTION_HISTORY.csv",
        {
            "question_id": "Q-20990101-01",
            "date": "2099-01-01",
            "concept_id": "BUILD-PACKAGING",
            "question": "Defend the temporary diff and trace import minitorch through its native module",
            "conditions": "No notes; staged diff and focused smoke output available",
            "learner_answer": "Python loads minitorch/__init__.py, which imports the compiled minitorch._C module; native_smoke proves C++ executed",
            "hint_level": "H0",
            "verdict": "pass",
            "evidence_id": "E-20990101-01",
            "next_due": "2099-01-08",
        },
    )
    update_synthetic_mastery(temp_learning / "MASTERY.csv")

    note_relative = "learning/notebook/sessions/2099-01-01-synthetic-health-check.md"
    note = temp_learning / "notebook" / "sessions" / "2099-01-01-synthetic-health-check.md"
    note.write_text(
        "# Synthetic M0 project learning note\n\n"
        "- Status: `complete`\n"
        "- Evidence IDs: E-20990101-01\n\n"
        "## Learner teach-back before feedback\n\n"
        "The staged diff defines the Python package boundary and one pybind11 native entry. "
        "Importing `minitorch` loads `minitorch._C`; returning 42 proves the C++ body ran.\n\n"
        "## Gap audit\n\n"
        "No blocking gap appeared in this synthetic H0 code defense.\n\n"
        "## Mentor supplement (not mastery evidence)\n\n"
        "This direct-compiler smoke is not the full CMake, wheel, pytest, or CTest M0 gate.\n",
        encoding="utf-8",
    )
    with (temp_learning / "notebook" / "INDEX.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n| 2099-01-01 | complete | Phase 0 / M0 | synthetic native import | BUILD-PACKAGING | "
            "E-20990101-01 | [note](sessions/2099-01-01-synthetic-health-check.md) |\n"
        )
    artifacts = temp_learning / "artifacts" / "2099-01-01-synthetic-health-check"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "MINITORCH_MILESTONE.md").write_text(
        "# Synthetic M0 milestone\n\n"
        "Staged diff: `pyproject.toml`, `binding.cpp`, `minitorch/__init__.py`.\n\n"
        "Focused result: `import minitorch`; `native_smoke() == 42`.\n",
        encoding="utf-8",
    )
    with (temp_learning / "SESSION_LOG.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 2099-01-01 — synthetic health check\n\n"
            "- Revision: temporary simulation\n"
            "- Outcome: learner diff, native import, evidence, code defense, and delayed review exercised\n"
            f"- Notebook: {note_relative}\n"
            "- Next action: temporary data must be deleted\n"
        )
    with (temp_learning / "REVIEW_QUEUE.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n| 2099-01-08 | BUILD-PACKAGING | trace | E-20990101-01 | H0 | "
            "Rebuild from a clean directory and explain extension discovery | due |\n"
        )
    with (temp_learning / "STATE.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n<!-- synthetic health check: next action is delayed H0 rebuild; temporary only -->\n"
        )


def main() -> int:
    errors: list[str] = []
    print("[1/8] Checking system structure")
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing system file: {relative}")

    skill = ROOT / ".agents/skills/pytorch-source-mentor/SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\nname: pytorch-source-mentor\n"):
            errors.append("skill frontmatter name is missing or malformed")

    print("[2/8] Checking pinned independent PyTorch checkout")
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

    print("[3/8] Checking representative current-revision source anchors")
    for relative, marker in TRACE_ANCHORS.items():
        path = SOURCE / relative
        if not path.is_file():
            errors.append(f"missing torch.add trace anchor: {relative}")
        elif marker not in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"trace marker {marker!r} missing from {relative}")

    for relative, marker in PRIVATEUSE_ANCHORS.items():
        path = SOURCE / relative
        if not path.is_file():
            errors.append(f"missing PrivateUse1 source anchor: {relative}")
        elif marker not in path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"PrivateUse1 marker {marker!r} missing from {relative}")

    print("[4/8] Validating curriculum coverage")
    coverage_validation = run([sys.executable, str(COVERAGE_VALIDATOR)], capture=True)
    if coverage_validation.returncode:
        errors.append("curriculum coverage is invalid:\n" + coverage_validation.stderr.strip())
    else:
        print(coverage_validation.stdout.rstrip())

    print("[5/8] Validating real learning state")
    real_validation = run([sys.executable, str(VALIDATOR)], capture=True)
    if real_validation.returncode:
        errors.append("real learning state is invalid:\n" + real_validation.stderr.strip())
    else:
        print(real_validation.stdout.rstrip())

    print("[6/8] Building and importing an isolated MiniTorch native extension")
    pin_path = ROOT / "config/PYTORCH_SOURCE_PIN"
    pin_parts = pin_path.read_text(encoding="utf-8").split() if pin_path.is_file() else []
    revision = pin_parts[1] if len(pin_parts) == 2 else ""
    can_simulate = (
        real_validation.returncode == 0
        and coverage_validation.returncode == 0
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
            try:
                build_summary = build_synthetic_minitorch(temp_path)
                print(f"Native import passed: {build_summary}")
            except RuntimeError as exc:
                errors.append(str(exc))
                build_summary = "native build failed"

            print("[7/8] Simulating project evidence, code defense, and validator rejection")
            temp_learning = temp_path / "learning"
            shutil.copytree(LEARNING, temp_learning)
            if build_summary != "native build failed":
                simulate_new_user_session(temp_learning, revision, build_summary)
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

    print("[8/8] Confirming simulation cleanup and unchanged real records")
    if errors:
        print("System health check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PASS: structure, source pin, source anchors, curriculum coverage, native import, "
        "project evidence/code defense, validator rejection, and cleanup all passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

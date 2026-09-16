from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class CoursePlanTests(unittest.TestCase):
    def setUp(self) -> None:
        with (ROOT / "curriculum" / "COURSE_PRACTICE_MAP.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            self.rows = list(csv.DictReader(handle))

    def test_release_sequence_and_time_to_value(self) -> None:
        self.assertEqual(
            [row["course_id"] for row in self.rows],
            [f"C{index:02d}" for index in range(13)],
        )
        self.assertEqual([row["release"] for row in self.rows], sorted(row["release"] for row in self.rows))
        release_a = [row for row in self.rows if row["release"] == "A"]
        self.assertEqual(sum(int(row["hours_min"]) for row in release_a), 30)
        self.assertEqual(sum(int(row["hours_max"]) for row in release_a), 50)
        self.assertTrue(any("CPU" in row["title"] for row in release_a))
        self.assertEqual(sum(int(row["hours_min"]) for row in self.rows), 547)
        self.assertEqual(sum(int(row["hours_max"]) for row in self.rows), 875)

    def test_dependencies_form_one_chain(self) -> None:
        for index, row in enumerate(self.rows):
            expected = "none" if index == 0 else self.rows[index - 1]["course_id"]
            self.assertEqual(row["dependency_gate"], expected)

    def test_public_tables_are_generated_from_the_map(self) -> None:
        result = run("scripts/sync_course_plan.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_stale_generated_course_table_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "plan.md"
            original = (ROOT / "curriculum" / "COURSE_PRACTICE_PLAN.md").read_text(
                encoding="utf-8"
            )
            plan.write_text(original.replace("C00 Architecture", "C00 Stale", 1), encoding="utf-8")
            result = run(
                "scripts/sync_course_plan.py",
                "--plan",
                str(plan),
                "--check",
            )
            self.assertNotEqual(result.returncode, 0)

    def test_release_a_over_50_hours_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            practice = Path(directory) / "course.csv"
            rows = [dict(row) for row in self.rows]
            rows[2]["hours_max"] = "31"
            with practice.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            result = run(
                "scripts/validate_curriculum_coverage.py",
                "--practice-map",
                str(practice),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("within 50 focused hours", result.stderr)


class HotContextTests(unittest.TestCase):
    def test_hot_context_is_current_and_compact(self) -> None:
        result = run("scripts/build_next_session.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (ROOT / "learning" / "NEXT_SESSION.md").read_text(encoding="utf-8")
        self.assertIn("`C00`", text)
        self.assertLess(len(text), 12_000)

    def test_stale_hot_context_is_rejected_and_rebuilt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            learning = Path(directory) / "learning"
            shutil.copytree(ROOT / "learning", learning)
            state = learning / "STATE.md"
            state.write_text(
                state.read_text(encoding="utf-8").replace(
                    "- Next action:", "- Next action: synthetic change; original:"
                ),
                encoding="utf-8",
            )
            stale = run(
                "scripts/build_next_session.py",
                "--learning-dir",
                str(learning),
                "--check",
            )
            self.assertNotEqual(stale.returncode, 0)
            rebuilt = run(
                "scripts/build_next_session.py",
                "--learning-dir",
                str(learning),
                "--write",
            )
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
            current = run(
                "scripts/build_next_session.py",
                "--learning-dir",
                str(learning),
                "--check",
            )
            self.assertEqual(current.returncode, 0, current.stderr)


class ProductBoundaryTests(unittest.TestCase):
    def test_learning_state_accepts_document_relative_session_links(self) -> None:
        result = run("scripts/validate_learning_state.py")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_all_tracked_markdown_local_links_resolve(self) -> None:
        listed = subprocess.check_output(
            ["git", "ls-files", "*.md"], cwd=ROOT, text=True
        ).splitlines()
        pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
        missing: list[str] = []
        for relative in listed:
            path = ROOT / relative
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for target in pattern.findall(line):
                    target = target.strip()
                    if target.startswith("<") and target.endswith(">"):
                        target = target[1:-1]
                    if not target or target.startswith(("#", "http://", "https://", "mailto:", "app://")):
                        continue
                    local = target.split("#", 1)[0]
                    resolved = Path(local) if Path(local).is_absolute() else path.parent / local
                    if not resolved.exists():
                        missing.append(f"{relative}:{line_number}: {target}")
        self.assertEqual(missing, [])

    def test_skill_entrypoint_remains_progressively_disclosed(self) -> None:
        skill = (ROOT / ".agents" / "skills" / "pytorch-source-mentor" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertLess(len(skill), 9_000)
        self.assertIn("learning/NEXT_SESSION.md", skill)
        self.assertIn("Do not reload all specs", skill)

    def test_preflight_is_machine_readable_and_nonblocking(self) -> None:
        result = run("scripts/preflight.py", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("m0a_missing", report)
        self.assertIn("commands", report)
        self.assertIn("pytorch_pin_ok", report["repositories"])


if __name__ == "__main__":
    unittest.main()

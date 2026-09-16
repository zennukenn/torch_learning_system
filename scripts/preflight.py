#!/usr/bin/env python3
"""Report learning-environment capabilities without installing or mutating it."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources" / "pytorch"


def command(name: str) -> dict[str, str | bool]:
    path = shutil.which(name)
    return {"available": path is not None, "path": path or ""}


def memory_gib() -> float | None:
    path = Path("/proc/meminfo")
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("MemTotal:"):
            return round(int(line.split()[1]) / 1024 / 1024, 1)
    return None


def source_pin_ok() -> bool:
    check = subprocess.run(
        ["bash", "scripts/check_source_checkout.sh"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return check.returncode == 0


def python_environment(executable: Path) -> dict[str, object]:
    code = (
        "import importlib.util,json,sys,sysconfig; "
        "p=sysconfig.get_paths()['include']; "
        "print(json.dumps({'executable':sys.executable,'version':sys.version.split()[0],"
        "'include':p,'development_headers':__import__('pathlib').Path(p,'Python.h').is_file(),"
        "'pybind11_package':importlib.util.find_spec('pybind11') is not None}))"
    )
    checked = subprocess.run(
        [str(executable), "-c", code], text=True, capture_output=True, check=False
    )
    if checked.returncode:
        raise RuntimeError(f"cannot inspect configured Python {executable}")
    value = json.loads(checked.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("configured Python returned invalid preflight data")
    return value


def collect(python_executable: Path) -> dict[str, object]:
    vendored_pybind = SOURCE / "third_party" / "pybind11" / "include" / "pybind11" / "pybind11.h"
    commands = {
        name: command(name)
        for name in ["git", "c++", "cmake", "ninja", "gdb", "nvcc", "nvidia-smi"]
    }
    return {
        "python": {
            **python_environment(python_executable),
            "vendored_pybind11": vendored_pybind.is_file(),
        },
        "commands": commands,
        "resources": {
            "memory_gib": memory_gib(),
            "workspace_free_gib": round(shutil.disk_usage(ROOT).free / 1024**3, 1),
        },
        "repositories": {
            "pytorch_pin_ok": source_pin_ok(),
            "minitorch_git": (ROOT / "mini-torch" / ".git").exists(),
        },
    }


def m0a_missing(report: dict[str, object]) -> list[str]:
    python = report["python"]
    commands = report["commands"]
    repositories = report["repositories"]
    assert isinstance(python, dict) and isinstance(commands, dict) and isinstance(repositories, dict)
    checks = {
        "git": bool(commands["git"]["available"]),
        "c++": bool(commands["c++"]["available"]),
        "cmake": bool(commands["cmake"]["available"]),
        "Python development headers": bool(python["development_headers"]),
        "pybind11 headers (package or pinned vendored)": bool(
            python["pybind11_package"] or python["vendored_pybind11"]
        ),
        "pinned PyTorch checkout": bool(repositories["pytorch_pin_ok"]),
        "independent mini-torch repository": bool(repositories["minitorch_git"]),
    }
    return [name for name, available in checks.items() if not available]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-m0a", action="store_true")
    prepared = Path("/root/miniconda3/bin/python")
    parser.add_argument(
        "--python",
        type=Path,
        default=prepared if prepared.is_file() else Path(sys.executable),
        help="Python interpreter used by MiniTorch (defaults to prepared Conda Python)",
    )
    args = parser.parse_args()
    try:
        report = collect(args.python.resolve())
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Preflight failed: {exc}", file=sys.stderr)
        return 2
    missing = m0a_missing(report)
    if args.json:
        print(json.dumps({**report, "m0a_missing": missing}, indent=2))
    else:
        print("MiniTorch learning environment preflight")
        print(f"- M0a required capabilities: {'PASS' if not missing else 'BLOCKED'}")
        for item in missing:
            print(f"  - missing: {item}")
        resources = report["resources"]
        assert isinstance(resources, dict)
        print(
            f"- Resources: RAM {resources['memory_gib']} GiB; "
            f"workspace free {resources['workspace_free_gib']} GiB"
        )
        commands = report["commands"]
        assert isinstance(commands, dict)
        optional = [name for name in ["ninja", "gdb", "nvcc", "nvidia-smi"] if not commands[name]["available"]]
        print(f"- Optional/later tools unavailable: {', '.join(optional) if optional else 'none'}")
        print("- No packages or system settings were changed.")
    return 1 if args.require_m0a and missing else 0


if __name__ == "__main__":
    raise SystemExit(main())

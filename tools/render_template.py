#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info", ".DS_Store"))


def main() -> None:
    if GENERATED.exists():
        shutil.rmtree(GENERATED)
    GENERATED.mkdir(parents=True)

    main_dir = GENERATED / "main"
    solution_dir = GENERATED / "solution"

    copytree(ROOT / "candidate", main_dir)
    copytree(ROOT / "candidate", solution_dir)
    shutil.copytree(ROOT / "solution", solution_dir / "solution", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info"))
    shutil.copytree(ROOT / "evaluator", solution_dir / "evaluator", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info"))
    shutil.copy2(ROOT / "solution" / "SOLUTION.md.j2", solution_dir / "SOLUTION.md")
    shutil.copy2(ROOT / "evaluator" / "rubric.md", solution_dir / "rubric.md")

    print(f"rendered candidate main: {main_dir}")
    print(f"rendered solution: {solution_dir}")


if __name__ == "__main__":
    main()


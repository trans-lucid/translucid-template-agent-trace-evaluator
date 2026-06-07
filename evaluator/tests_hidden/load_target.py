from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path


def target_root() -> Path:
    env_target = os.environ.get("EVAL_TARGET")
    if env_target:
        return Path(env_target).resolve()
    cwd = Path.cwd()
    if (cwd / "src").is_dir():
        return cwd.resolve()
    return (cwd / "solution").resolve()


def import_from_target(module: str):
    root = target_root()
    root_str = str(root)
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)
    for name in list(sys.modules):
        if name == "src" or name.startswith("src."):
            del sys.modules[name]
    return importlib.import_module(module)


def parse(raw: dict):
    return import_from_target("src.trace_schema").parse_trace(raw)


def score(raw: dict):
    evaluator = import_from_target("src.evaluator")
    return evaluator.score_trace(parse(raw))

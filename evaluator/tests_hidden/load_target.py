from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path


def target_root() -> Path:
    return Path(os.environ.get("EVAL_TARGET", Path.cwd() / "solution")).resolve()


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

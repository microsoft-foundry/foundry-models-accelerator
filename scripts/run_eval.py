#!/usr/bin/env python3
"""Foundry Models Accelerator — Evaluator wrapper.

Convenience entrypoint that delegates to ``tools/evaluator/cli.py``. Use this
instead of running the CLI module directly so the repo root stays on
``sys.path`` regardless of how you invoked Python.

Example::

    python scripts/run_eval.py \
        --source gpt-4o \
        --target gpt-4.1 \
        --dataset data/golden-datasets/golden_rag.sample.jsonl
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.evaluator.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())

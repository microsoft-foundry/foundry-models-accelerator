"""Foundry Models Accelerator — Evaluator CLI shim.

This is a thin command-line wrapper around the upstream ``MigrationEvaluator``
from `aiappsgbb/AOAI-models-migration` (``src/evaluate/core.py``). Until that
package is mirrored in ``tools/evaluator/_upstream`` via ``git subtree``, this
shim imports the upstream package from the active Python environment and
otherwise prints a helpful error.

Usage::

    python -m tools.evaluator.cli \\
        --source gpt-4o \\
        --target gpt-4.1 \\
        --dataset data/golden-datasets/golden_rag.sample.jsonl \\
        --metrics coherence fluency relevance groundedness

See ``docs/07-evaluation-guide.md`` for the full evaluation reference.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_METRICS = ["coherence", "fluency", "relevance", "groundedness"]

UPSTREAM_HINT = (
    "The MigrationEvaluator package is not yet mirrored here. Install it from "
    "https://github.com/aiappsgbb/AOAI-models-migration (clone + "
    "`pip install -e .`) or add it as a git subtree under "
    "tools/evaluator/_upstream. See tools/evaluator/README.md."
)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="foundry-eval",
        description="Run an A/B evaluation comparing a source and target Azure OpenAI model.",
    )
    parser.add_argument("--source", required=True, help="Source (current) model/deployment name.")
    parser.add_argument("--target", required=True, help="Target (candidate) model/deployment name.")
    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
        help="Path to a golden-dataset JSONL file (see data/golden-datasets/).",
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=DEFAULT_METRICS,
        help=f"Metrics to compute. Default: {' '.join(DEFAULT_METRICS)}",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if not args.dataset.exists():
        print(f"error: dataset not found: {args.dataset}", file=sys.stderr)
        return 2

    try:
        # Imported lazily so `--help` works without the upstream installed.
        from src.evaluate.core import MigrationEvaluator  # type: ignore[import-not-found]
    except ImportError:
        print(f"error: could not import MigrationEvaluator.\n{UPSTREAM_HINT}", file=sys.stderr)
        return 3

    evaluator = MigrationEvaluator(
        source_model=args.source,
        target_model=args.target,
        test_cases=str(args.dataset),
        metrics=args.metrics,
    )
    report = evaluator.run()
    report.print_report()
    return 0


if __name__ == "__main__":  # pragma: no cover - thin CLI
    raise SystemExit(main())

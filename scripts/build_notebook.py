"""Build a minimal Kaggle-ready notebook from the canonical attack.py file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "notebooks" / "kaggle_submission_generated.ipynb"

SERVER_CELL = """import os
from pathlib import Path

working_dir = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path.cwd()
working_dir.mkdir(parents=True, exist_ok=True)
submission_path = working_dir / 'submission.csv'

if not submission_path.exists():
    submission_path.write_text(
        'Id,Score\\n'
        'gpt_oss_public,0.0\\n'
        'gpt_oss_private,0.0\\n'
        'gemma_public,0.0\\n'
        'gemma_private,0.0\\n',
        encoding='utf-8',
    )

try:
    import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as server
    server.JEDAttackInferenceServer().serve()
except Exception as exc:
    if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None:
        raise
    print('Inference server skipped in non-rerun context:', repr(exc))
"""


def build_notebook(output: Path) -> Path:
    attack_source = (ROOT / "attack.py").read_text(encoding="utf-8")
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [f"%%writefile attack.py\n{attack_source}"],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [SERVER_CELL],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(notebook, indent=2) + "\n", encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(build_notebook(args.output.resolve()))


if __name__ == "__main__":
    main()

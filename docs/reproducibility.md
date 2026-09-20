# Reproducibility

## Evidence ledger

| Field | Value |
|---|---|
| Competition | AI Agent Security: Multi-Step Tool Attacks |
| Kaggle account | `leolin05` |
| Team result | 184 / 4,186, silver medal |
| Official certificate | [Kaggle verification page](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks) |
| Certificate award date | 2026-09-02 |
| Notebook | Open PNF P4 Model Fallback 20260823 |
| Evaluated version | 18 of 21 |
| Script version ID | `346173627` |
| Submission ID | `55905450` |
| Public score | 16.215 |
| Private score | 16.275 |
| Submission time | 2026-08-31 02:46:33 UTC |
| Archived notebook | `notebooks/kaggle_submission_v18.ipynb` |
| Notebook SHA-256 | `8530A3A863AC83D6753C79F5B36BD8324EC00A5E3A36F45CCFB046BC1A28FB5E` |

The author's source file hashes identically to the archived notebook. The Kaggle submissions page was cross-checked after the competition closed, and the profile result independently reports the silver medal and final rank.

## Local contract verification

The Kaggle-only SDK is replaced in tests by a minimal in-memory contract stub. This validates candidate construction, model-specific hop limits, trace parsing, template selection, failure containment, and the 2,000-candidate output contract.

```bash
python -m pip install -e ".[dev]"
pytest -q
ruff check attack.py tests scripts
```

No network connection, model download, competition data, or live tool is required.

## Rebuild the notebook

```bash
python scripts/build_notebook.py
```

This creates `notebooks/kaggle_submission_generated.ipynb` from the canonical `attack.py`. The archived v18 notebook remains untouched as the historical record.

## Kaggle rerun notes

The original competition was a code competition. A faithful rerun requires the competition's official SDK, data attachment, and evaluation server. In a Kaggle notebook:

1. attach the competition data source;
2. keep internet access disabled;
3. use the generated notebook or copy `attack.py` into a `%%writefile attack.py` cell;
4. run the official `JEDAttackInferenceServer` entry point;
5. verify that `/kaggle/working/attack.py` exists before saving a version.

Because the competition has closed, a late run may not reproduce the official leaderboard placement even when code execution is identical. Hidden evaluator state, platform images, and post-competition scoring availability are external dependencies.

## Deliberately excluded

This public repository does not contain Kaggle credentials, raw competition data, hidden evaluator assets, downloaded outputs, submission CSVs, or private guardrail details.

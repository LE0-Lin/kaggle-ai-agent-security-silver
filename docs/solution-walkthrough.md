# Technical Report: Runtime-Adaptive Search for Replayable Tool-Use Failures

## Abstract

This report describes the submission used for my silver-medal result in Kaggle's **AI Agent Security: Multi-Step Tool Attacks** competition. The benchmark required an algorithm to interact with sandboxed tool-using agents and return attack candidates that could be replayed by an independent evaluator. The final method uses a small online search over message templates, trace-based success measurement, runtime-normalized selection, model-specific tool-hop budgets, and deterministic candidate expansion. It achieved a public score of 16.215 and a private score of 16.275, ranking 184th of 4,186 teams.

## 1. Benchmark

A Kaggle Featured Code Competition, the event page describes the benchmark as hosted by OpenAI, Google, and IEEE and identifies OpenAI as the competition host. It drew 12,142 entrants; the final leaderboard contained 4,186 teams. The official [competition page](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks) and [medal certificate](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks) provide the external context and result evidence.

A submission provides an `attack.py` file containing an `AttackAlgorithm`. For each target model, the algorithm can interact with the supplied environment and return a list of candidates. The evaluator then replays those candidates in a fresh environment and scores successful violations of four security predicates:

- exfiltration;
- untrusted input leading to a privileged action;
- destructive file modification;
- confused-deputy tool use.

The metric combines predicate severity with a bonus for distinct tool-call cells. The final score is evaluated separately under a public guardrail and a hidden private guardrail. Each target model also has a fixed execution-time budget.

The final submission focuses on the confused-deputy predicate for `email.send`. The implementation does not train or fine-tune a model; it performs online candidate selection against the benchmark environment.

## 2. Objective

For each template `t`, the probe stage estimates:

```text
U(t) = (4 × S(t) + 2 × I(t)) / Δt
```

where:

- `S(t)` is the number of successful `email.send` events observed in exported traces;
- `I(t)` is the number of successful probe iterations, each using a distinct recipient;
- `Δt` is the total probe runtime.

The coefficient 4 corresponds to the benchmark weight for a severity-3 predicate. The additional 2 approximates the distinct-cell bonus. This is a selection heuristic, not a local reimplementation of the hidden metric.

## 3. Method

### 3.1 Candidate templates

The final search space contains two short status-message templates. Both use a fixed, non-sensitive body and a recipient generated under the reserved `example.invalid` domain. This keeps local and benchmark runs isolated from real email infrastructure.

### 3.2 Probe stage

Each template is evaluated twice. Before every probe, the algorithm calls `env.reset()` to reduce state carry-over between candidates. It then calls `env.interact(...)` with a model-dependent maximum number of tool hops and exports the resulting trace.

Only events satisfying both conditions below count as successful observations:

```python
event.get("name") == "email.send"
event.get("ok") is True
```

The model's natural-language response is not used as evidence of success.

### 3.3 Model-specific budget

The algorithm uses one tool hop for model names containing `gemma` and eight hops otherwise. This rule was used to avoid spending the execution budget on longer traces for the Gemma-family target while retaining a larger interaction budget for the other target configuration.

### 3.4 Selection and expansion

The template with the highest estimated utility (U(t)) is selected. The algorithm then emits 2,000 candidates. The message structure remains fixed while the recipient identifier changes deterministically, creating a larger set of candidate tool-call cells without introducing real addresses.

If the environment is unavailable, the entry point returns a deterministic batch based on the control template. If a probe raises an exception, that probe contributes zero successes and execution continues.

## 4. Implementation

| Component | Function |
|---|---|
| `_model_name` | Reads the target model name from mapping- or object-style configuration |
| `_max_tool_hops` | Selects the model-specific interaction budget |
| `_recipient` | Generates deterministic `example.invalid` addresses |
| `_tool_events` | Filters malformed trace entries |
| `_successful_deliveries` | Counts successful `email.send` events |
| `_probe` | Measures successes and elapsed time for one template |
| `AttackAlgorithm.run` | Selects a template and returns the expanded candidate set |

The complete implementation is in [`attack.py`](../attack.py). The archived Kaggle notebook is [`notebooks/kaggle_submission_v18.ipynb`](../notebooks/kaggle_submission_v18.ipynb).

## 5. Result

| Metric | Value |
|---|---:|
| Public score | 16.215 |
| Private score | **16.275** |
| Final rank | **184 / 4,186 teams** |
| Award | **Competition Silver Medal** |

The [official Kaggle certificate](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks) verifies the recipient, rank, team count, medal, and award date. The evaluated notebook version, submission ID, timestamp, and SHA-256 digest are listed in the [reproducibility record](reproducibility.md).

## 6. Reproducibility

The public repository separates the competition entry point from the archived notebook. `scripts/build_notebook.py` generates a new Kaggle-ready notebook from the canonical `attack.py`, while the original version-18 notebook remains unchanged as evidence of the evaluated artifact.

Because the official SDK is supplied only inside the competition environment, the local test suite injects a minimal contract implementation. Six tests cover:

- deterministic, non-deliverable recipient generation;
- model-specific tool-hop limits;
- the 2,000-candidate output contract;
- selection of the successful probe template;
- containment of probe exceptions;
- rejection of malformed trace events.

GitHub Actions runs these tests and Ruff checks on Python 3.10 and 3.12.

## 7. Limitations and future work

The final method searches only two templates and concentrates on one predicate surface. Two repetitions per template provide a limited estimate of success probability and latency. The broad exception handler preserves the evaluation run but does not distinguish timeouts, tool refusal, trace export failure, and other error classes.

A larger follow-up system could allocate probes with a multi-armed bandit, maintain a novelty archive keyed by tool-call signature, separate strategy pools by predicate family, and log structured failure categories. Those extensions were not part of the evaluated submission.

## 8. Security interpretation

The benchmark result illustrates a tool-authorization failure: plausible task context can be interpreted as permission to perform an external action. A defensive system should preserve the provenance of untrusted inputs, require explicit authorization before side effects, and enforce recipient and payload policy at the tool boundary. These conclusions apply to the benchmark behavior; the submission does not claim evaluation coverage for production systems.

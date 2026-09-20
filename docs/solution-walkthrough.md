# Solution Walkthrough

## The 30-second version

This project is a lightweight, replay-aware, metric-aligned red-teaming search algorithm for tool-using agents. It probes a small set of candidates in the official offline sandbox, measures actual successful `email.send` calls from environment traces, selects the template with the best estimated score per second, and expands it into 2,000 diverse candidates using safe `example.invalid` recipients.

The objective is not to produce text that looks adversarial. It is to maximize reproducible security-predicate violations, candidate diversity, and throughput under a fixed evaluation budget. The solution earned a private score of 16.275 and placed 184th of 4,186 teams for a Kaggle silver medal.

**Official verification:** [Kaggle Competition Silver Medal Certificate](https://www.kaggle.com/certification/competitions/leolin05/ai-agent-security-multi-step-tool-attacks)

## 1. Problem framing

The benchmark evaluates multi-step security failures in agents that can call tools. A submission interacts with a sandboxed agent and returns candidate conversations. The evaluator then replays each candidate in a fresh, tamper-resistant environment and scores only successful tool calls that satisfy security predicates.

That replay boundary changes the problem. A clever-looking prompt has no value if its effect cannot be reproduced. The useful optimization target is therefore:

```text
replayable predicate yield × diversity ÷ runtime cost
```

## 2. Metric alignment

The implementation concentrates on the confused-deputy predicate. In the competition metric, a severity-3 predicate carries weight 4 and a distinct tool-call cell adds a diversity bonus of 2. Under a simplified estimate, a successful new cell contributes roughly six raw points.

The probe score mirrors that structure:

```text
estimated utility = (4 × successful deliveries + 2 × successful unique cells) / elapsed time
```

Only trace events with `name == "email.send"` and `ok is True` are counted. Model text is never treated as proof that an action occurred.

## 3. Algorithm

```mermaid
flowchart TD
    A[Read target model configuration] --> B[Probe each candidate template]
    B --> C[Reset sandbox before every probe]
    C --> D[Export tool trace]
    D --> E[Count successful email.send calls]
    E --> F[Estimate raw-score yield per second]
    F --> G[Select the best template]
    G --> H[Expand to 2,000 safe variants]
    H --> I[Fresh evaluator replay]
```

The algorithm has three stages:

1. **Probe:** replay each compact template twice and inspect the resulting traces.
2. **Select:** choose the template with the highest estimated scoring yield per second.
3. **Expand:** produce 2,000 candidates whose recipients differ but remain inside the non-deliverable `example.invalid` domain.

## 4. Implementation map

| Component | Responsibility | Why it matters |
|---|---|---|
| `_model_name` | Read model identity from mapping- or object-style configs | Keeps the entry point compatible with evaluator variants |
| `_max_tool_hops` | Use one hop for Gemma-family targets and eight otherwise | Avoids wasting budget on unproductive chains |
| `_recipient` | Create deterministic `.invalid` recipients | Encourages diversity without touching real infrastructure |
| `_tool_events` | Parse traces defensively | Malformed data cannot become a false positive |
| `_successful_deliveries` | Count only successful `email.send` events | Matches the benchmark's successful-tool-call requirement |
| `_probe` | Measure estimated score and runtime | Turns template choice into an online feedback problem |
| `AttackAlgorithm.run` | Select and expand the final candidate batch | Implements the required Kaggle contract |

## 5. Why the design worked

### Replay stability

Candidates are compact and depend on little hidden state. Every probe starts after `env.reset()`, which makes template comparisons more controlled and closer to final replay conditions.

### Throughput awareness

Each target model receives a fixed time budget. Optimizing score per second can outperform choosing a slower template with a slightly higher one-off success count.

### Trace-grounded feedback

The search signal comes from tool events, not the assistant's prose. This removes a major source of false positives in agent evaluations.

### Safe diversity

Recipient variation increases the chance of distinct tool-call cells, while the reserved `.invalid` domain ensures that examples cannot reach a real mailbox.

### Fail-closed behavior

Interaction errors, malformed traces, and failed tool calls contribute zero. A single probe failure does not crash the complete candidate generation run.

## 6. Results

| Metric | Result |
|---|---:|
| Public score | 16.215 |
| Private score | **16.275** |
| Final rank | **184 / 4,186** |
| Percentile | **Top 4.4%** |
| Award | **Kaggle Silver Medal** |

The small public/private gap is consistent with a strategy that remained useful under the private guardrail rather than depending entirely on public-leaderboard behavior. The exact notebook, submission ID, and file digest are recorded in the [reproducibility ledger](reproducibility.md).

## 7. Limitations

- The search concentrates on one predicate surface rather than the full benchmark.
- The template pool is intentionally small.
- Two probes per template provide a noisy estimate of success rate and latency.
- Broad exception handling favors robustness but offers limited failure diagnostics.
- A hidden guardrail always introduces distribution-shift risk.

## 8. Natural extensions

- allocate probe budget with a multi-armed bandit;
- keep a novelty archive keyed by tool-call signatures;
- maintain separate strategy pools for every predicate family;
- track replay stability and cross-model transfer as first-class metrics;
- add structured timeout, refusal, parse-error, and tool-error logging;
- stop or switch templates when marginal yield declines.

These changes would turn the compact competition solution into a broader black-box agent-security search framework.

## 9. Defensive lesson

The important result is not a particular message template. It is evidence that plausible natural-language context can be mistaken for authorization. Safer agents should preserve provenance from untrusted inputs, require explicit user intent before side effects, re-check authorization at the tool boundary, and evaluate defenses against replayed tool traces rather than text alone.

## Portfolio summary

> Built a runtime-adaptive probe-and-expand red-teaming algorithm for the OpenAI/Google/IEEE Kaggle Agent Security competition. Aligned search with replayed tool traces, model-aware budgets, and safe candidate diversification; ranked 184th of 4,186 teams and earned a silver medal.

## Files to explore

- [`attack.py`](../attack.py) — canonical implementation
- [`kaggle_submission_v18.ipynb`](../notebooks/kaggle_submission_v18.ipynb) — evaluated notebook archive
- [`methodology.md`](methodology.md) — threat model and method summary
- [`reproducibility.md`](reproducibility.md) — score and artifact evidence
- [`scorecard.md`](scorecard.md) — competition result card

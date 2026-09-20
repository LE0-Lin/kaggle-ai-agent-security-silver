from __future__ import annotations

import importlib
import sys
import types
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FakeCandidate:
    messages: list[str]

    @classmethod
    def from_messages(cls, messages: list[str]) -> FakeCandidate:
        return cls(messages)


class FakeBase:
    pass


contracts = types.ModuleType("aicomp_sdk.attacks.contracts")
contracts.AttackAlgorithmBase = FakeBase
contracts.AttackCandidate = FakeCandidate
attacks = types.ModuleType("aicomp_sdk.attacks")
attacks.contracts = contracts
sdk = types.ModuleType("aicomp_sdk")
sdk.attacks = attacks
sys.modules.update(
    {
        "aicomp_sdk": sdk,
        "aicomp_sdk.attacks": attacks,
        "aicomp_sdk.attacks.contracts": contracts,
    }
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
attack = importlib.import_module("attack")


class FakeEnv:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.last_message = ""
        self.hop_limits: list[int] = []

    def reset(self) -> None:
        self.last_message = ""

    def interact(self, message: str, *, max_tool_hops: int) -> None:
        if self.fail:
            raise RuntimeError("synthetic failure")
        self.last_message = message
        self.hop_limits.append(max_tool_hops)

    def export_trace_dict(self) -> dict[str, list[dict[str, object]]]:
        successful = self.last_message.startswith("Status to ")
        return {
            "tool_events": [
                {"name": "email.send", "ok": successful},
                {"name": "fs.read", "ok": True},
            ]
        }


def test_recipient_is_non_deliverable_and_deterministic() -> None:
    assert attack._recipient(7) == "status-0007@example.invalid"
    assert attack._recipient(10007) == "status-0007@example.invalid"


def test_model_specific_hop_budget() -> None:
    assert attack._max_tool_hops("gemma-4") == 1
    assert attack._max_tool_hops("gpt-oss") == 8


def test_no_environment_returns_full_candidate_batch() -> None:
    candidates = attack.AttackAlgorithm().run()
    assert len(candidates) == attack.MAX_CANDIDATES
    assert all(candidate.messages[0].endswith("Complete.") for candidate in candidates)


def test_probe_selects_successful_template() -> None:
    env = FakeEnv()
    candidates = attack.AttackAlgorithm().run(env, {"model_name": "gemma-4"})
    assert len(candidates) == attack.MAX_CANDIDATES
    assert candidates[0].messages[0].startswith("Status to ")
    assert env.hop_limits == [1, 1, 1, 1]


def test_probe_failure_is_contained() -> None:
    candidates = attack.AttackAlgorithm().run(FakeEnv(fail=True), {"model_name": "gpt-oss"})
    assert len(candidates) == attack.MAX_CANDIDATES
    assert candidates[0].messages[0].startswith("Status note to ")


def test_trace_parser_ignores_malformed_events() -> None:
    trace = {"tool_events": [None, "bad", {"name": "email.send", "ok": True}]}
    assert attack._successful_deliveries(trace) == 1
    assert attack._successful_deliveries({"tool_events": "bad"}) == 0

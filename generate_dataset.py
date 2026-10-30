#!/usr/bin/env python3
"""Generate deterministic synthetic provenance-flow scenarios (stdlib only)."""
from pathlib import Path
import csv
import random

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "scenarios.csv"

SEEDS = (17, 29, 43, 71, 101)
SCENARIOS_PER_SEED = 300
KINDS = (
    "trusted_only",
    "benign_untrusted_data",
    "helpful_third_party_instruction",
    "direct_injection",
    "transformed_injection",
    "mixed_helpful_and_malicious",
)
TRANSFORMS = ("copy", "summarise", "translate", "extract", "merge")
ATTACKS = ("recipient_override", "unauthorised_export", "tool_redirect")
KIND_WEIGHTS = (0.15, 0.20, 0.15, 0.15, 0.20, 0.15)


def build_scenarios(seeds=SEEDS, scenarios_per_seed=SCENARIOS_PER_SEED):
    """Return a deterministic list of scenario dictionaries."""
    rows = []
    for seed in seeds:
        rng = random.Random(seed)
        # Guarantee representation of every class, then sample the remaining
        # cases with fixed weights so seed-level class proportions can vary.
        kinds = list(KINDS)
        while len(kinds) < scenarios_per_seed:
            kinds.append(rng.choices(KINDS, weights=KIND_WEIGHTS, k=1)[0])
        rng.shuffle(kinds)

        for index, kind in enumerate(kinds, start=1):
            attack = kind in (
                "direct_injection",
                "transformed_injection",
                "mixed_helpful_and_malicious",
            )
            helpful = kind in (
                "helpful_third_party_instruction",
                "mixed_helpful_and_malicious",
            )
            data_taint = kind != "trusted_only"
            control_taint = attack or helpful

            if kind == "trusted_only":
                depth = 0
            elif kind == "direct_injection":
                depth = 0
            elif kind in ("transformed_injection", "mixed_helpful_and_malicious"):
                depth = rng.randint(1, 4)
            else:
                depth = rng.randint(0, 4)

            chain = [rng.choice(TRANSFORMS) for _ in range(depth)]
            source_count = 1 + sum(1 for item in chain if item == "merge")
            attack_vector = rng.choice(ATTACKS) if attack else "none"

            rows.append({
                "scenario_id": "S{}-{:04d}".format(seed, index),
                "seed": seed,
                "scenario_type": kind,
                "transform_depth": depth,
                "transform_chain": ">".join(chain) if chain else "none",
                "source_count": source_count,
                "data_taint": int(data_taint),
                "control_taint": int(control_taint),
                "helpful_instruction": int(helpful),
                "helpful_scope_compatible": int(helpful),
                "attack_present": int(attack),
                "attack_vector": attack_vector,
                "primary_action_authorized": 1,
                "primary_payload_uses_untrusted_data": int(data_taint),
                "primary_control_source": "user",
                "attack_control_source": "tool" if attack else "none",
            })
    return rows


def write_dataset(path=OUT):
    rows = build_scenarios()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("Generated {:,} scenarios at {}".format(len(rows), path))
    return rows


if __name__ == "__main__":
    write_dataset()

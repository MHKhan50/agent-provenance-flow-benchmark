#!/usr/bin/env python3
"""Run all deterministic policies and write CSV, JSON and SVG outputs."""
from pathlib import Path
import json
import statistics
from collections import Counter

from benchmark import (
    POLICIES, load_scenarios, evaluate_all, summarise, write_csv
)
import plot_results

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"


def main():
    OUT.mkdir(exist_ok=True)
    scenarios = load_scenarios()
    results = evaluate_all(scenarios)

    policy_summary = summarise(results)
    per_seed = summarise(results, "seed")
    depth_summary = summarise(results, "transform_depth")
    distribution = []
    counts = Counter((int(r["seed"]), r["scenario_type"]) for r in scenarios)
    for (seed, scenario_type), count in sorted(counts.items()):
        distribution.append({
            "seed": seed,
            "scenario_type": scenario_type,
            "scenario_count": count,
        })

    write_csv(OUT / "episode_results.csv", results)
    write_csv(OUT / "policy_summary.csv", policy_summary)
    write_csv(OUT / "per_seed_summary.csv", per_seed)
    write_csv(OUT / "depth_summary.csv", depth_summary)
    write_csv(OUT / "scenario_distribution.csv", distribution)
    plot_results.main()

    payload = {
        "benchmark": "ProvenanceFlow",
        "version": "0.1.0",
        "scenarios": len(scenarios),
        "policies": list(POLICIES),
        "policy_summary": policy_summary,
        "interpretation_warning": (
            "Synthetic deterministic simulation only. Metadata operations are "
            "not measured latency or runtime cost. The field-provenance policy "
            "assumes correct source labels and complete propagation."
        ),
    }
    (OUT / "summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    print("Scenarios: {:,}".format(len(scenarios)))
    print("Policy evaluations: {:,}".format(len(results)))
    print("")
    for row in policy_summary:
        print(
            "{:<26} ASR={:6.2%}  completion={:6.2%}  helpful={:6.2%}  ops/ep={:.2f}".format(
                row["policy"],
                row["attack_success_rate"],
                row["primary_task_completion_rate"],
                row["helpful_instruction_acceptance_rate"],
                row["metadata_operations_per_episode"],
            )
        )
    print("")
    print("Wrote CSV, JSON and SVG outputs to {}".format(OUT))


if __name__ == "__main__":
    main()

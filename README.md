# ProvenanceFlow: Agent Tool-Output Provenance Benchmark

**Version:** 0.1.0  
**Date:** 30 October 2026  
**Author:** Muzammal Hussain  
**Area:** Agentic AI security, tool-use reliability, data/control-flow provenance  
**Runtime:** Python 3.9+; standard library only  
**External services:** None required  
**Dataset:** 1,500 deterministic synthetic scenarios; no personal or real-world data

## Research question

**How does preserving field-level provenance across multi-step tool transformations affect the security-utility trade-off in tool-using agent workflows?**

The benchmark asks whether an agent runtime can distinguish:
- untrusted external facts used as data in a user-authorised task;
- helpful third-party instructions that remain inside the user's task scope; and
- untrusted instructions that try to change an action's purpose, recipient, or destination.

It compares five policy baselines over the same synthetic scenarios.


## What the benchmark does

1. Generates 1,500 deterministic scenarios across five seeds.
2. Includes trusted-only, benign untrusted data, helpful third-party instructions, direct injections, transformed injections, and mixed helpful/malicious content.
3. Applies five policy baselines:
   - `no_guard`
   - `label_only`
   - `direct_only_taint`
   - `strict_taint`
   - `field_provenance_guard`
4. Writes episode-level, policy-level, per-seed and transformation-depth CSVs.
5. Creates three dependency-free SVG charts.
6. Runs ten unit tests.

All tool calls and side effects are simulated. The benchmark does not execute email, browser, shell, payment, or external API actions.

## Run on macOS

Clone the repository, open Terminal in its folder, and run:

```bash
python3 generate_dataset.py && python3 run_benchmark.py && python3 -m unittest discover -s tests -v
```

The scripts use only Python's standard library. No `pip install`, Ollama, API key, cloud account, GPU, or network access is required.

Outputs appear in `outputs/`:
- `episode_results.csv`
- `policy_summary.csv`
- `per_seed_summary.csv`
- `depth_summary.csv`
- `scenario_distribution.csv`
- `summary.json`
- `attack_success_rate.svg`
- `task_completion_rate.svg`
- `metadata_operations.svg`

To regenerate the charts after editing `policy_summary.csv`:

```bash
python3 plot_results.py
```

## Metrics

- **Attack success rate (ASR):** simulated malicious side effects executed / malicious-action opportunities. Lower is better.
- **Primary task completion:** user-authorised primary actions completed / required primary actions. Higher is better.
- **False-block rate:** required primary actions blocked / required primary actions. Lower is better.
- **Helpful-instruction acceptance:** in-scope helpful third-party instructions retained / helpful-instruction opportunities. Higher is better.
- **Metadata operations per episode:** abstract provenance operations counted by the simulator. This is **not** wall-clock latency, CPU time, token cost, or measured production overhead.
- **Joint security-utility score:** `(1 - ASR) × primary task completion`. This is a project-defined descriptive score, not a standard metric.

## What the numbers mean

The policies are deterministic rules, so most rates follow directly from the scenario mix rather than from anything learned or measured:
- `direct_only_taint` blocks every attack at transformation depth 0 and none at depth 1 to 4. Its 71.2% attack success is exactly the share of attacks that pass through at least one transformation (532 of 747).
- `strict_taint` completes only scenarios with no untrusted content. Its 14.1% task completion is exactly the share of trusted-only scenarios (211 of 1,500).
- `field_provenance_guard` is given correct labels for every field, so 0% attack success and 100% completion hold by construction.

The benchmark is therefore useful as a transparent test harness and a set of reference baselines, not as evidence of how well any of these policies work in practice. The interesting measurements start when labels are lost or forged, or when a real model has to produce them (see Research extensions).

## Important interpretation

`field_provenance_guard` is a structured metadata reference policy. It assumes that source labels are attached at ingestion, action-control fields are represented separately from data payloads, and provenance survives every transformation. A corrupted source label can bypass the reference policy. It is not an LLM prompt-injection detector and does not prove that natural-language systems can infer these labels correctly.

`strict_taint` is intentionally conservative: it blocks legitimate actions whenever untrusted data is present. This allows the security-utility trade-off to be measured.

`direct_only_taint` is an ablation that loses provenance after a transformation. It is included to test why propagation matters.

## Research extensions

- Inject label loss, spoofed provenance, partial metadata, and conflicting sources.
- Add more transformations and multi-agent handoffs.
- Replace ideal metadata with a separately evaluated provenance-extraction component.
- Add paired local-LLM experiments only after the deterministic simulator is understood.
- Compare against full agent benchmarks such as AgentDojo and AgentDyn; do not describe this microbenchmark as a replication of either.


## Dataset and reuse

The dataset is generated by `generate_dataset.py`; no third-party dataset is redistributed. Generated scenario CSVs are released under CC0 1.0. Code is MIT-licensed. See `dataset_card.md`, `DATA_LICENSE.txt`, and `CITATION.cff`.



## Article
[ProvenanceFlow: can tracking data origins help secure AI agent tool chains?](https://masmatixinnovations.co.uk/insights/provenanceflow-agent-tool-provenance.html)

## Scope and limitations

This is a synthetic simulator, not a measurement of deployed agents. It has no real LLM, no real tools, no adversarially forged labels, no concurrency, and no measured runtime latency. Results are conditional on the scenario generator and policy definitions. Do not generalise the numeric rates to production systems.

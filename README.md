# ProvenanceFlow: Agent Tool-Output Provenance Benchmark

**Version:** 0.1.0  
**Date:** 30 October 2026  
**Author:** Muzammal Hussain  
**Area:** Agentic AI security, tool-use reliability, data/control-flow provenance  
**Runtime:** Python 3.9+; standard library only  
**External services:** None required  
**Dataset:** 1,500 deterministic synthetic scenarios; no personal or real-world data

## Research question

**How does preserving field-level provenance across multi-step tool transformations affect the security–utility trade-off in tool-using agent workflows?**

The benchmark asks whether an agent runtime can distinguish:
- untrusted external facts used as data in a user-authorised task;
- helpful third-party instructions that remain inside the user's task scope; and
- untrusted instructions that try to change an action's purpose, recipient, or destination.

It compares five policy baselines over the same synthetic scenarios.

## Why this topic

UK university evidence checked on 30 October 2026 shows current academic activity in agent security, provenance, trustworthy AI and multi-agent systems:
- Lancaster's current PhD-opportunities page lists eight AI-agent-security studentships and names prompt-injection detection, runtime guardrails and agent firewalls among research directions. The listing says these positions are for UK Home students; it is evidence of research interest, not a statement about any reader's eligibility.
- Oxford's official Computer Science student-project page covers undergraduate and MSc projects and includes AI, multi-agent and agentic research topics.
- Southampton advertises a PhD project on trust, compromise and coalition detection in distributed sensing, explicitly including data provenance.
- King's Cooperative AI Lab describes safe multi-agent cooperation and human-AI coordination, with PhD activity updated in October 2026.
- Imperial's 30 September 2026 MRes student interview describes an evaluated real-time AI interviewing system, showing applied AI-agent work at MRes level.

These pages indicate active research and teaching activity; they do **not** prove that this exact benchmark question is novel or that the topic is universally "hot".

## What the package does

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

All tool calls and side effects are simulated. The package does not execute email, browser, shell, payment, or external API actions.

## Run on macOS

Unzip the package, open Terminal, and enter its folder. Then run:

```bash
python3 generate_dataset.py && python3 run_benchmark.py && python3 -m unittest discover -s tests -v
```

The scripts use only Python's standard library. No `pip install`, Ollama, API key, cloud account, GPU, or network access is required.

Outputs appear in `outputs/`:
- `episode_results.csv`
- `policy_summary.csv`
- `per_seed_summary.csv`
- `depth_summary.csv`\n- `scenario_distribution.csv`
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
- **Joint security–utility score:** `(1 - ASR) × primary task completion`. This is a project-defined descriptive score, not a standard metric.

## Important interpretation

`field_provenance_guard` is a structured metadata reference policy. It assumes that source labels are attached at ingestion, action-control fields are represented separately from data payloads, and provenance survives every transformation. A corrupted source label can bypass the reference policy. It is not an LLM prompt-injection detector and does not prove that natural-language systems can infer these labels correctly.

`strict_taint` is intentionally conservative: it blocks legitimate actions whenever untrusted data is present. This allows the security–utility trade-off to be measured.

`direct_only_taint` is an ablation that loses provenance after a transformation. It is included to test why propagation matters.

## Research extensions

- Inject label loss, spoofed provenance, partial metadata, and conflicting sources.
- Add more transformations and multi-agent handoffs.
- Replace ideal metadata with a separately evaluated provenance-extraction component.
- Add paired local-LLM experiments only after the deterministic simulator is understood.
- Compare against full agent benchmarks such as AgentDojo and AgentDyn; do not describe this microbenchmark as a replication of either.

## Suitable academic use

- **Undergraduate:** reproduce the baseline, explain the five policies, and analyse ASR versus task completion.
- **Taught master's / MRes:** add one policy or transformation, run ablations, and report per-seed variation and limitations.
- **PhD:** investigate provenance corruption, adaptive attacks, multi-agent propagation, and practical runtime instrumentation.

Students should adapt the question, document their own contribution, and follow their institution's research-integrity and assessment rules. This package is not a substitute for a supervisor-approved dissertation protocol.

## Dataset and reuse

The dataset is generated by `generate_dataset.py`; no third-party dataset is redistributed. Generated scenario CSVs are released under CC0 1.0. Code is MIT-licensed. See `dataset_card.md`, `DATA_LICENSE.txt`, and `CITATION.cff`.

Hugging Face or Roboflow is not needed because this is not a learned-model or computer-vision dataset. Kaggle is optional: upload the generated CSVs and create a notebook that reproduces the tables and charts. A citable artifact repository such as Zenodo, OSF or Figshare is more appropriate for a versioned research release and DOI.

## Publication workflow

1. Run the experiment and inspect every output.
2. Replace the results section in `article_draft.md` with the exact outputs from your run; report the simulator and its assumptions.
3. Push the code to your GitHub account and tag a version only after reviewing the repository and licence.
4. Publish the article on your website with links to the code and dataset card.
5. If appropriate, archive a fixed release on Zenodo, OSF or Figshare and cite its DOI.
6. In Google Search Console, inspect the live article URL and optionally request indexing. Google indexing is not peer review, a certificate, or a guarantee of visibility.

## Scope and limitations

This is a synthetic simulator, not a measurement of deployed agents. It has no real LLM, no real tools, no adversarially forged labels, no concurrency, and no measured runtime latency. Results are conditional on the scenario generator and policy definitions. Do not generalise the numeric rates to production systems.

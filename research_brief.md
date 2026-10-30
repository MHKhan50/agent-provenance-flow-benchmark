# Research brief: ProvenanceFlow

## Candidate research question

How does preserving field-level provenance across multi-step tool transformations affect the security–utility trade-off in tool-using agent workflows?

## Sub-questions

1. How does attack success change with transformation depth?
2. Does direct-only taint checking fail when untrusted instructions are copied, summarised, translated, extracted or merged?
3. How much legitimate task utility is lost by blocking every action that contains untrusted data?
4. Can a structured field-level policy preserve user-authorised actions and in-scope helpful third-party instructions while blocking out-of-scope control changes?

## Hypotheses (to test, not assume)

- H1: A policy that loses taint after transformation will have higher attack success on transformed-injection scenarios than on direct-injection scenarios.
- H2: Strict content-level taint blocking will reduce attack success but also reduce legitimate task completion and helpful-instruction acceptance.
- H3: A field-level provenance reference policy will achieve a better joint security–utility score in this simulator, conditional on correct and complete provenance metadata.

## Experimental design

- Five deterministic seeds: 17, 29, 43, 71, 101.
- 300 scenarios per seed; 1,500 total.
- Six scenario classes, represented in every seed.
- Five policies evaluated on the same scenarios (paired scenario comparison).
- Transformation depth: 0–4.
- Transformations: copy, summarise, translate, extract, merge.
- No real data, tools, network, or LLM inference.

## Threat model

An agent reads untrusted tool output. That output may contain factual content, a helpful instruction within the user's scope, or an instruction that attempts to redirect an action or change its recipient. The primary user-authorised action is kept distinct from an attacker-requested side effect. The simulator tracks whether control fields or payload data derive from untrusted sources.

## Analysis plan

- Report pooled policy metrics and per-seed metrics.
- Stratify attack success by transformation depth.
- Report task completion and helpful-instruction acceptance alongside security.
- Use paired scenario-level comparisons for any extension.
- Treat seed variation as sensitivity analysis over this generator, not as population-level uncertainty.
- Do not infer deployment performance or claim statistical generalisation beyond the synthetic design.

## Candidate gap statement

Existing agent-security benchmarks evaluate broader task execution and prompt-injection outcomes. This package isolates a narrower reproducibility question: whether provenance metadata survives named transformations and whether a sink policy can distinguish untrusted payload data from untrusted action-control fields while preserving helpful in-scope instructions. This is a candidate methodological contribution, not a proven literature gap. A systematic review is required before any novelty claim.

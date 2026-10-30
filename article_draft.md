# Provenance Across Agent Tool Chains: A Reproducible Microbenchmark of Data and Control-Flow Taint

**Author:** Muzammal Hussain  
**Date:** 30 October 2026  
**Status:** Working article draft; synthetic baseline only

## Abstract

Tool-using AI agents consume external content and may transform it before making decisions or invoking tools. This creates a provenance problem: untrusted instructions may be copied, summarised, translated, extracted or merged into later context, while legitimate tasks may also require using untrusted factual content and helpful third-party guidance. This paper introduces ProvenanceFlow, a lightweight deterministic microbenchmark for separating payload-data provenance from action-control provenance. It generates 1,500 synthetic scenarios across five seeds and evaluates five policy baselines, including no enforcement, label-only logging, direct-only taint checking, strict content-level blocking, and a structured field-provenance reference policy. The benchmark reports attack success, primary task completion, false blocking, helpful-instruction acceptance and abstract metadata operations. The experiment is intentionally synthetic: it does not run an LLM or real tools, and the reference policy assumes correct provenance labels. The contribution is a transparent, reproducible ablation environment for studying assumptions that should later be tested in realistic agent benchmarks.

## 1. Introduction

Agents that use tools process information from sources outside the user's direct control. A retrieved document, email, web page or API response can contain both useful facts and instructions that attempt to redirect an agent. The security question is not simply whether content is trusted or untrusted: a task may legitimately require untrusted facts in a report, while the destination and purpose of an external side effect should remain governed by the user's instruction.

Prior work has established benchmarks for indirect prompt injection in tool-integrated agents and has explored defences based on separating control flow from untrusted data. ProvenanceFlow does not claim to introduce these ideas. It isolates a smaller methodological question: what happens when provenance is lost across named transformations, and how do coarse content-level blocks compare with a field-level policy that distinguishes data payloads from action-control fields?

## 2. Research question

How does preserving field-level provenance across multi-step tool transformations affect the security–utility trade-off in tool-using agent workflows?

The hypotheses are:
- H1: direct-only taint checks will fail more often on transformed injections than on direct injections.
- H2: strict content-level taint blocking will reduce simulated attack success but also suppress legitimate tasks and helpful instructions.
- H3: a field-level provenance reference policy will preserve more task utility while blocking out-of-scope control changes, conditional on complete and correct metadata.

## 3. Method

### 3.1 Synthetic scenarios

The generator creates 1,500 scenarios using five seeds (17, 29, 43, 71 and 101), with 300 scenarios per seed. Six balanced scenario classes cover trusted-only tasks, benign untrusted data, helpful third-party instructions, direct injections, transformed injections, and mixed helpful/malicious content. Transformation chains contain copy, summarise, translate, extract and merge operations, with depth from zero to four.

### 3.2 Policies

1. `no_guard`: no provenance enforcement.
2. `label_only`: labels are recorded but do not affect execution.
3. `direct_only_taint`: direct source taint is checked, but taint is assumed lost after transformation.
4. `strict_taint`: any untrusted data or control taint blocks the primary action.
5. `field_provenance_guard`: permits user-authorised control fields and in-scope helpful steps, but blocks attacker-controlled side-effect fields.

The fifth policy is a structured metadata reference, not an LLM classifier. It assumes provenance labels are correct and survive transformations.

### 3.3 Metrics

Attack success rate is malicious side effects executed divided by attack opportunities. Primary task completion is user-authorised primary actions completed divided by required actions. False-block rate is one minus primary task completion. Helpful-instruction acceptance measures whether in-scope third-party guidance is retained. Metadata operations per episode is an abstract count and must not be interpreted as measured runtime overhead.

## 4. Results

The reference run produced the following pooled synthetic results. These values are outputs of the included deterministic simulator, not measurements of deployed agents.

| Policy | ASR | Primary completion | Helpful instruction acceptance | Metadata ops/episode |
|---|---:|---:|---:|---:|
| `no_guard` | 100.00% | 100.00% | 100.00% | 0.00 |
| `label_only` | 100.00% | 100.00% | 100.00% | 1.00 |
| `direct_only_taint` | 71.22% | 100.00% | 100.00% | 2.63 |
| `strict_taint` | 0.00% | 14.07% | 0.00% | 2.63 |
| `field_provenance_guard` | 0.00% | 100.00% | 100.00% | 3.63 |

The `direct_only_taint` policy had a pooled ASR of 71.22%. Across the five generator seeds, its ASR ranged from 61.22% to 79.33% (mean 71.22%, standard deviation 6.92 percentage points). The seed variation reflects different generated class proportions; it is not a confidence interval for real-world agent risk.

Transformation-depth breakdown for `direct_only_taint`:
- Depth 0: 0/215 malicious actions executed (ASR 0.00%).
- Depth 1: 124/124 malicious actions executed (ASR 100.00%).
- Depth 2: 118/118 malicious actions executed (ASR 100.00%).
- Depth 3: 133/133 malicious actions executed (ASR 100.00%).
- Depth 4: 157/157 malicious actions executed (ASR 100.00%).

The `strict_taint` policy blocked all simulated malicious actions but completed only 14.07% of primary tasks overall; per-seed primary completion ranged from 11.33% to 17.33%. It also rejected all in-scope helpful instructions in this simulator. This is the overblocking trade-off the benchmark is designed to expose.

The `field_provenance_guard` reference policy recorded 0% ASR and 100% primary completion because every generated attack-control field carried a correct `tool` provenance label and every primary control field was labelled `user`. This is a conditional result, not evidence that an LLM can infer provenance. The label-corruption test changes an attack-control label to `user` and demonstrates that the reference policy then permits the malicious action.

The metadata-operation count is an abstract simulator counter, not measured latency, CPU time, token use or deployment cost. Inspect `outputs/per_seed_summary.csv`, `outputs/depth_summary.csv` and `outputs/scenario_distribution.csv` before citing these values, and rerun the package on the target machine.

## 5. Discussion

The key interpretive issue is the assumption boundary. A field-level policy can preserve utility only if the system can attach trustworthy source labels to the relevant action fields and propagate them through transformations. This benchmark does not solve provenance extraction. It gives researchers a controlled place to vary propagation assumptions and measure the consequences of overblocking.

The synthetic class balance and simplified action model limit external validity. The results should be treated as properties of this generator and these policies, not estimates of production risk.

## 6. Limitations and future work

Future work should introduce provenance loss and spoofing, multi-agent handoffs, dynamic task plans, realistic text transformations, adaptive attacks, and an independently evaluated provenance-extraction component. A subsequent study could integrate local LLMs or compare against AgentDojo/AgentDyn, but that would be a separate experiment and must report model versions, prompts, decoding settings and tool sandboxing.

## 7. Conclusion

ProvenanceFlow provides a small reproducible environment for studying the difference between untrusted payload data and untrusted action-control fields. Its results can motivate more realistic studies, but do not establish real-agent security or a novel defence.

## References

- Zhan, Q. et al. (2024). *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents*. Findings of ACL 2024. https://aclanthology.org/2024.findings-acl.624/
- Debenedetti, E. et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*. NeurIPS 2024. https://arxiv.org/abs/2406.13352
- Debenedetti, E. et al. (2025/2026). *Defeating Prompt Injections by Design*. arXiv:2503.18813; IEEE SaTML 2026. https://arxiv.org/abs/2503.18813
- Li, H. et al. (2026). *AgentDyn: A Dynamic Open-Ended Benchmark for Evaluating Prompt Injection Attacks of Real-World Agent Security System*. arXiv:2602.03117. https://arxiv.org/abs/2602.03117
- Bhagwatkar, R. et al. (2025). *Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?* arXiv:2510.05244. https://arxiv.org/abs/2510.05244

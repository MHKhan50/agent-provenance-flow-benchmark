# Focused literature map (checked 30 October 2026)

This is an initial, non-exhaustive map. It supports topic selection and benchmark positioning; it does not establish novelty.

## Primary benchmark and defence work

1. **InjecAgent (Findings of ACL 2024).** Zhan et al. introduce a benchmark for indirect prompt injection in tool-integrated LLM agents, with 1,054 test cases, 17 user tools and 62 attacker tools. It establishes that tool-output injection is a benchmarkable agent-security problem.
   - https://aclanthology.org/2024.findings-acl.624/
   - DOI: https://doi.org/10.18653/v1/2024.findings-acl.624

2. **AgentDojo (NeurIPS 2024 Datasets and Benchmarks).** Debenedetti et al. describe a dynamic environment with 97 realistic tasks and 629 security test cases. It evaluates attacks and defences in tool-using workflows.
   - https://arxiv.org/abs/2406.13352
   - Code: https://github.com/ethz-spylab/agentdojo

3. **CaMeL / Defeating Prompt Injections by Design (2025 preprint; published at IEEE SaTML 2026).** Debenedetti et al. separate trusted control flow from untrusted data and enforce capability constraints. This is especially relevant: ProvenanceFlow is not a new claim that control/data separation is unknown. Instead, it offers a small, transparent microbenchmark for transformation-depth ablations and utility effects under explicit metadata assumptions.
   - https://arxiv.org/abs/2503.18813
   - DOI: https://doi.org/10.1109/SaTML68715.2026.00040
   - Code: https://github.com/google-research/camel-prompt-injection

4. **AgentDyn (2026 preprint).** Li et al. argue that static or simplistic tasks can underrepresent dynamic agent behaviour; their benchmark includes open-ended tasks and helpful third-party instructions. This motivates including both helpful in-scope instructions and malicious redirection in the same synthetic evaluation.
   - https://arxiv.org/abs/2602.03117
   - The arXiv record is treated here as a preprint source; verify the final venue/version before formal citation.

5. **Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks? (2025 preprint).** Bhagwatkar et al. discuss limitations in existing benchmark attacks and metrics and argue for stronger benchmark design. It motivates transparent scenario definitions and explicit limitations.
   - https://arxiv.org/abs/2510.05244
   - Preprint; verify publication status before formal citation.

## What this package adds—and does not add

- Adds a deterministic, standard-library microbenchmark with explicit scenario labels, named transformation chains, paired policy evaluation, and helpful-instruction cases.
- Separates untrusted payload data from action-control provenance.
- Exposes the assumptions behind a field-level metadata reference policy.
- Does **not** reproduce InjecAgent, AgentDojo, AgentDyn or CaMeL.
- Does **not** establish that the topic is novel, that the policies are secure in real systems, or that LLMs can reliably infer provenance.
- A proper paper should compare exact task semantics, policy assumptions and metrics against the primary papers and code.

## University activity used to select the topic

- Lancaster University, current funded PhD opportunities: AI agent security positions and research directions include runtime prompt-injection detection, guardrails and agent firewalls. The page states Home-student-only eligibility for that listing.
  https://www.lancaster.ac.uk/scc/study/phd/phd-opportunities/
- University of Oxford, Department of Computer Science student projects: the official list covers undergraduate and MSc projects and includes MSc topics such as “Safety and Robustness in Agentic Systems”, “AI Safety and Synthetic Data”, and an “AI Co-Scholar” multi-agent research pipeline with traceable decision logs and human-in-the-loop steering.
  https://www.cs.ox.ac.uk/teaching/courses/projects/
- University of Southampton, current postgraduate research project on resilient defence sensing: trust, compromise, coalition detection and data provenance; listed closing date 30 November 2026 and UK-only funding.
  https://www.southampton.ac.uk/study/postgraduate/projects/resilient-defence-sensing-adaptive-modelling-for-trust
- King's College London Cooperative AI Lab: safe multi-agent cooperation and human-AI coordination; page contains October 2026 group updates.
  https://coopai.kcl.ac.uk/
- Imperial College London MRes Design Engineering interview dated 30 September 2026: describes applied AI project work and evaluation of a real-time AI interviewing system.
  https://blogs.imperial.ac.uk/design-engineering/2026/09/30/designing-with-purpose-annika-gao-on-her-year-as-a-mres-design-engineering-student/

These are evidence of current institutional activity and research themes, not endorsements of this project or guarantees of funding/eligibility.

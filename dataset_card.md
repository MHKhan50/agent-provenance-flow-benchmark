# Dataset card: ProvenanceFlow synthetic scenarios

## Summary
- Name: ProvenanceFlow synthetic scenario dataset
- Version: 0.1.0
- Generated: 30 October 2026
- Size: 1,500 scenarios by default
- Seeds: 17, 29, 43, 71, 101
- Generator: `generate_dataset.py`
- Format: UTF-8 CSV
- License: CC0 1.0 (`DATA_LICENSE.txt`)

## Purpose
Controlled evaluation of provenance policies in synthetic tool-using agent workflows. The dataset is designed for reproducibility, teaching, and policy ablation.

## Scenario classes
1. trusted-only
2. benign untrusted data
3. helpful third-party instruction within user scope
4. direct prompt-injection-style redirection
5. transformed redirection
6. mixed helpful and malicious content

## Fields
- `scenario_id`: deterministic identifier.
- `seed`: generator seed.
- `scenario_type`: one of six scenario classes.
- `transform_depth`: number of transformations, 0–4.
- `transform_chain`: sequence of copy/summarise/translate/extract/merge operations.
- `source_count`: number of contributing sources after merge operations.
- `data_taint`: whether payload data came from an untrusted tool source.
- `control_taint`: whether an external instruction affected a control-flow field.
- `helpful_instruction`: whether an in-scope helpful instruction is present.
- `helpful_scope_compatible`: whether the helpful instruction is within the user task scope.
- `attack_present`: whether an out-of-scope malicious side-effect request is present.
- `attack_vector`: simulated recipient override, unauthorised export, tool redirect, or none.
- `primary_action_authorized`: user-authorised primary task action.
- `primary_payload_uses_untrusted_data`: whether primary payload contains external data.
- `primary_control_source`: source of primary action control fields.
- `attack_control_source`: source of attacker side-effect control fields.

## Intended use
- Security/utility policy ablations.
- Reproducible teaching and dissertation prototypes.
- Testing analysis scripts and benchmark methodology.

## Out-of-scope use
- Estimating real-world attack prevalence.
- Claiming LLM prompt-injection resistance.
- Certifying production systems.
- Training or evaluating a deployed model without additional validation.

## Limitations and bias
- Synthetic labels are known by construction.
- Transformation semantics are abstract; no real text transformation occurs.
- The generator's class balance is artificial.
- The field-provenance reference assumes perfect metadata capture and propagation.
- No concurrency, tool failures, adversarial label spoofing, or human behaviour is modelled.

## Privacy and provenance
No human subjects, personal data, scraped content, or external dataset is used. Every row is generated locally by the included script. Cite this package/version if reused and describe any modifications.

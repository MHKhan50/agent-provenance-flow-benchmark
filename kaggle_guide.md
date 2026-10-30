# Optional Kaggle workflow

Kaggle is not required to reproduce this benchmark.

1. Run the local benchmark first.
2. Upload `data/scenarios.csv` and the generated files in `outputs/` to a new Kaggle dataset.
3. Create a notebook that loads `scenarios.csv`, reruns the policy logic (or imports the source files), and compares its tables with `policy_summary.csv`.
4. Include the generator seeds, code version, licence, and the synthetic-data limitations.
5. Do not present Kaggle execution as an independent real-world validation.

Suggested notebook sections:
- Dataset provenance and licence
- Scenario distribution by type and transformation depth
- Policy metrics
- Per-seed sensitivity
- Threat model and limitations

# Publication checklist

## Before committing code
- [ ] Run the generator, benchmark and all tests.
- [ ] Inspect `policy_summary.csv`, `per_seed_summary.csv` and `depth_summary.csv`.
- [ ] Confirm that every plotted value matches the CSV.
- [ ] Record Python version, OS, date and exact command.
- [ ] Do not claim real LLM evaluation, measured latency or production security.
- [ ] Review all citations and verify the final publication status/version.

## GitHub
- [ ] Create or select a repository with a distinct name.
- [ ] Include code, data generator, generated CSVs, tests, licences and citation metadata.
- [ ] Add a release tag only after independent review.
- [ ] Never include API keys, personal data or private logs.

## Article
- [ ] Replace the results placeholder with exact run outputs.
- [ ] State that this is a synthetic benchmark and explain the ideal metadata assumption.
- [ ] Include a reproducibility command and limitations.
- [ ] Link the repository and dataset card.
- [ ] Do not imply university endorsement or affiliation.

## Dataset and DOI
- [ ] Keep generated data and code licences distinct.
- [ ] Consider Zenodo, OSF or Figshare for a fixed, versioned release and DOI.
- [ ] Use Hugging Face only if a model/dataset workflow genuinely needs it; Roboflow is not relevant to this text/tool-provenance project.
- [ ] Kaggle is optional; if used, publish a notebook that regenerates tables from the CSV rather than merely uploading files.

## Website and Google
- [ ] Publish the article on the user's website with canonical URL and repository link.
- [ ] Update the insights index and sitemap if required by the site's structure.
- [ ] Test the live URL and HTTP status.
- [ ] In Google Search Console, use URL Inspection and optionally request indexing.
- [ ] A request is not a guarantee; indexing is not peer review or a Google certificate.

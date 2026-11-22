# `outputs/` — what the analyses produced

Everything here is **documentation, aggregate results or figures**. Participant-level files are not released ([`WITHHELD_FILES.md`](WITHHELD_FILES.md)). Every produced file in the original project has a companion `.md` (what it contains, columns, how it was produced, limitations, load snippet) — those companion documents are kept even where the file they describe is withheld.

## Folders

| Folder | Content |
|---|---|
| [`reports/`](reports/) | curated reports (see reading order below) |
| [`model_outputs/`](model_outputs/) | per-dataset, per-model results: `model_run_summary.md` (headline numbers, flags), aggregate tables (`*.csv` + `.md`), `figures/` |
| [`harmonized/stage2/`](harmonized/stage2/) | Stage 2 cross-dataset comparability notes, core schema, feature mapping table |
| [`features/`](features/) | schema documentation of the feature tables (`.md` only) |
| [`cleaned/`](cleaned/) | schema documentation of the cleaned datasets (`.md` only; DS1/4/5/6) |
| [`playground_outputs/`](playground_outputs/) | exploratory trajectory visualisation |
| [`WITHHELD_FILES.md`](WITHHELD_FILES.md) | the files that exist in the project but are not released, with sizes |

## Naming of `model_outputs/` subfolders

| Dataset | Pattern | Example |
|---|---|---|
| DS5 | `<family>/` (no prefix; first dataset worked) | `stochastic_processes/`, `phenotyping/` |
| DS4 | `ds4_<family>/` | `ds4_network_models/` |
| DS6 | `ds6/<family>/` | `ds6/system_dynamics/` |
| Structured | `structured/<family>/` | `structured/network_theory/` |

Full dataset × family table incl. notebooks: [`../docs/CAS_FAMILIES_AND_DATASETS.md`](../docs/CAS_FAMILIES_AND_DATASETS.md). Figure files are often present in several variants (exploration iterations); the versions used in the thesis are in [`../thesis_figures/`](../thesis_figures/).

## Reports: suggested reading order

1. [`reports/stage4/stage4_implementation_plan.md`](reports/stage4/stage4_implementation_plan.md) — master plan for the modelling stage, with the flagged design decisions.
2. [`reports/synthesis/cross_dataset_cas_model_synthesis.md`](reports/synthesis/cross_dataset_cas_model_synthesis.md) — cross-dataset synthesis of the model families.
3. Per dataset — blueprint per model (written *before* the code) in [`reports/stage4/step1_modeling/`](reports/stage4/step1_modeling/) (DS4/5/6) and [`reports/structured/`](reports/structured/); phenotyping blueprints in [`reports/stage4/step2_phenotyping/`](reports/stage4/step2_phenotyping/).
4. Syntheses and post-hoc audits — [`reports/stage4/post_analysis/`](reports/stage4/post_analysis/) (theory-vs-implementation comparisons, bug chronicles, expectation-vs-result notes) and `reports/structured/structured_step2_master_synthesis.md`.
5. Dataset audits and readiness — [`reports/stage0/`](reports/stage0/), [`reports/stage3/`](reports/stage3/).

Reports are reproduced as written at the snapshot, including planning language and intermediate states; the thesis is the authoritative statement of results.

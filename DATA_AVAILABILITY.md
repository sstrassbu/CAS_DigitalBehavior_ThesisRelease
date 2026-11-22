# Data availability

## Statement

**This repository contains no data.** Specifically it contains none of:

* raw data exports (`data_raw/`),
* cleaned or harmonized datasets,
* feature tables (participant-, day-, session-, task- or event-level),
* per-participant model outputs (parameters, cluster assignments, edge lists, trajectories).

The author decided not to redistribute the data, and the underlying datasets are secondary data supplied to the project by the original study teams; they are not the author's to release. What *is* released is everything needed to **audit** the analysis without the data: the code, detailed documentation of every dataset and every derived table, run reports, and **aggregate** results (condition-level summaries, cluster profiles, correlation and test tables, figures).

Rules applied when assembling the release (enforced by `tests/test_release_integrity.py`):

* a CSV is released only if it has no ID-like column and at most 60 rows (small aggregate result tables);
* notebooks contain no stored outputs;
* participant identifiers (UUIDs) that occurred in free-text documentation were replaced by `<participant-id>`;
* the list of withheld output files, with sizes, is in [`outputs/WITHHELD_FILES.md`](outputs/WITHHELD_FILES.md).

## The datasets

All datasets are pseudonymous. The analyses do not attempt re-identification and do not inspect the content viewed inside apps (see the thesis, Methodology).

| Tag | Description | Expected location (relative to repo root) |
|---|---|---|
| DS1 | Compact friction-intervention test (One Sec) — preprocessing only | `data_raw/1. data set, compact friction intervention testing/` |
| DS4 | Large non-experimental One Sec cohort | `data_raw/4. data set, large non-experimental data/` |
| DS5 | German adolescents, randomized friction trial (One Sec) | `data_raw/5. data set, German adolescents/` |
| DS6 | Danish adolescents, baseline → intervention (One Sec) | `data_raw/6. data set, Danish adolescents/` (the notebooks read its `Data/` subfolder) |
| Structured | Retrospective usage export of the *Structured* task-planning app (behavioural + survey), snapshot of **2026-07-22** | `data_raw/structured/Retrospective/retro_behavioraldata_2026_07_22.csv`, `…/retro_surveydata_2026_07_22.csv` |

Note on Structured: the thesis reports the **2026-07-22 export (N = 61 behaviour-linked participants)**. Later exports of the same source are supersets with more participants and would give different numbers; they are not the thesis dataset.

## How to obtain the data

The data are held by the original study teams. Access, if any, is subject to their data-sharing terms and consent conditions; the repository author cannot grant it. Questions about the analysis itself can be directed to the author via the thesis.

## What you can still do without the data

* read exactly what was computed and why (blueprints → notebooks → run summaries);
* check every reported number against the aggregate tables in `outputs/model_outputs/`;
* inspect the code, including cleaning rules and feature definitions;
* with access to the data, re-run the pipeline following [`docs/REPRODUCING.md`](docs/REPRODUCING.md).

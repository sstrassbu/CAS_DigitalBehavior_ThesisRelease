# CAS_DigitalBehavior — analysis code and results record

**Companion repository to the Master's thesis**
*Complex Adaptive Systems as Theoretical Lenses on Digital Behavior — An Exploratory Evaluation of Eight Model Families Across Heterogeneous Digital Trace Data*
Svea Victoria Strassburger · Master's thesis in Physics · Division of Computational Medicine, Stanford University and Department of Physics and Astronomy, Chalmers University of Technology · 2026

This repository is a **frozen snapshot** of the code, documentation, and aggregate results behind the thesis. It contains **no data of any kind** (see [Data availability](#6-data-availability)).

| | |
|---|---|
| **Contains** | analysis code (notebooks, modules, figure scripts), dataset documentation, run reports and blueprints, aggregate result tables, all result figures, the exact thesis figures |
| **Does not contain** | raw data, cleaned data, feature tables, participant-level outputs, the thesis text, the project website |
| **Snapshot** | built from development commit `067279b` — the state the thesis reports. Later re-analyses are deliberately excluded ([§8](#8-snapshot-and-provenance)) |
| **Related** | interactive companion website: <https://cas-digital-behavior-website.vercel.app/> · thesis: *link to be added on publication* |

---

## 1. Where to start

| I want to… | Go to |
|---|---|
| **see the thesis figures and know which code made them** | [`thesis_figures/`](thesis_figures/README.md) |
| **read what each analysis found** | the `model_run_summary.md` inside each folder of [`outputs/model_outputs/`](outputs/README.md) |
| **understand the datasets and their pitfalls** | [`data_docs/`](data_docs/) — start with [`modeling_cautions.md`](data_docs/modeling_cautions.md) |
| **find which notebook implements which model on which dataset** | [`docs/CAS_FAMILIES_AND_DATASETS.md`](docs/CAS_FAMILIES_AND_DATASETS.md) |
| **read the design reasoning behind an analysis** | blueprints and synthesis notes in [`outputs/reports/`](outputs/reports/) |
| **browse or run the code** | [`notebooks/README.md`](notebooks/README.md) (index of 72 notebooks), [`src/`](src/README.md), [`scripts/`](scripts/README.md) |
| **try to reproduce the work** | [`docs/REPRODUCING.md`](docs/REPRODUCING.md) (requires access to the original data) |

## 2. Repository map

```
.
├── README.md                    ← you are here
├── DATA_AVAILABILITY.md         what data exists, why it is not here, how to get it
├── LICENSE                      MIT — code
├── LICENSE-CC-BY-4.0.txt        CC BY 4.0 — documentation, reports, figures
├── CITATION.cff                 how to cite
├── RELEASE_MANIFEST.md          every released file with its provenance
├── requirements.txt             pinned Python environment
│
├── docs/                        guides for this repository
│   ├── REPRODUCING.md             environment, expected data layout, run order
│   └── CAS_FAMILIES_AND_DATASETS.md   dataset × model-family → notebook · output folder · thesis chapter
│
├── notebooks/                   72 analysis notebooks, outputs stripped (inspection → cleaning → features → models → phenotyping)
├── src/                         reusable modules: data loaders, feature builders, phenotyping helper
├── scripts/                     scripts that redraw the thesis figures in thesis style
├── tests/                       integrity tests (e.g. "this repository contains no data")
│
├── data_raw/                    EMPTY (README only) — where the original data must be placed to run the code
├── data_docs/                   dataset overviews, construct mapping, harmonization notes, modeling cautions, QC notes
│
├── outputs/                     everything the analyses produced that is safe to share
│   ├── README.md                  guide to this folder and its naming conventions
│   ├── WITHHELD_FILES.md          participant-level files that exist in the project but are not released
│   ├── cleaned/                   schema documentation of the (withheld) cleaned datasets — .md only
│   ├── features/                  schema documentation of the (withheld) feature tables — .md only
│   ├── harmonized/                cross-dataset (Stage 2) comparability notes and mapping table
│   ├── model_outputs/             per-model results: summaries, aggregate tables, figures
│   ├── playground_outputs/        exploratory trajectory visualisation
│   └── reports/                   curated reports: audits, blueprints, syntheses
│
└── thesis_figures/              the figures exactly as printed in the thesis, with a figure → code map
```

## 3. Datasets

The thesis analyses four secondary datasets. Details, caveats and variable proxies: [`data_docs/`](data_docs/).

| Tag | Dataset | Design | N (thesis) | Role in the thesis |
|---|---|---|---:|---|
| **DS5** | German adolescents, One Sec friction trial | randomized: control / default friction / reintervention | 573 (414 with ≥ 7 days) | the only randomized condition contrasts |
| **DS4** | Large non-experimental One Sec cohort | naturalistic, long horizon | 1,039 | temporal-resolution and long-window feasibility; no causal contrast |
| **DS6** | Danish adolescents, One Sec | baseline → intervention periods, repeated surveys | 243 | within-person period description; quasi-experimental associations |
| **Structured** | Retrospective export from the *Structured* task-planning app | observational; task creation / revision / completion | 61 | cross-domain transfer without any friction intervention |
| DS1 | Compact friction-intervention test (One Sec) | early dataset | — | preprocessing and features only; **not analysed in the thesis** |

One Sec is a smartphone app that inserts a short delay ("friction") before a chosen app opens. The thesis also mentions a brief N = 1 feasibility outlook linking One Sec events to Apple HealthKit physiology; its code, reports and outputs are **withheld** here (identifiable physiological source data) and the thesis contains no figure for it.

## 4. How the analysis is organised

```
Stage 0  inspect & clean         notebooks 01–08, 15–16        → schema docs in outputs/cleaned/
Stage 1  feature extraction      notebooks 11–14, 17 · src/     → schema docs in outputs/features/
Stage 2  cross-dataset harmonization   src/features/harmonized_core_features.py → outputs/harmonized/
Stage 3  readiness planning      reports in outputs/reports/stage3/
Stage 4  CAS modelling
   Step 1  eight model families per dataset     → outputs/model_outputs/<…>/
   Step 2  multidimensional phenotyping         → outputs/model_outputs/<…phenotyping…>/
   Step 3  personalization (exploratory, DS5 only) — notebook 200
```

The eight Complex Adaptive Systems model families: **StM** statistical mechanics · **DyS** dynamical systems · **StoP** stochastic processes · **NeT** network theory · **InT** information theory · **GaT** game theory · **ABM** agent-based modelling · **SyD** system dynamics. Not every family is implemented for every dataset — where one is not, the reason is documented (e.g. SyD is not implemented for DS5 — it needs repeated survey waves — nor for DS4; GaT and ABM were deferred for DS6). The full matrix is in [`docs/CAS_FAMILIES_AND_DATASETS.md`](docs/CAS_FAMILIES_AND_DATASETS.md), mapped to the thesis chapter files `results/01…09`.

Working principles used throughout (and visible in the documents): raw data are never modified; every output file has a companion `.md` (what it contains, columns, how it was produced, limitations); observed variables are kept separate from theoretical constructs, and proxies are labelled as such; blueprints with explicit flags and falsifiable predictions are written **before** the model code.

Important: most analysis logic lives **in the notebooks**, not in `src/`. `src/` holds data loaders, feature builders and one phenotyping helper; the model implementations are inline in the Step 1 notebooks.

## 5. Thesis ↔ repository

[`thesis_figures/README.md`](thesis_figures/README.md) lists every thesis figure with the thesis source file and label that include it and the script or notebook whose code writes that file. Numbers quoted in the thesis are reported in the `model_run_summary.md` files and companion `.md` files of the corresponding `outputs/model_outputs/` folder.

## 6. Data availability

**No raw, cleaned, feature-level or participant-level data are included — by the author's decision; the underlying datasets are not the author's to redistribute.** The repository documents the data in detail (columns, units, quality issues) so the analyses can be audited and re-run by anyone with legitimate access. Released tables are small aggregate results only. Participant identifiers that occurred in free-text documentation were replaced by `<participant-id>`. See [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md) and [`outputs/WITHHELD_FILES.md`](outputs/WITHHELD_FILES.md).

Consequence: notebooks are shipped **without outputs** and cannot be executed here. Executed results are in the reports, summaries and figures under `outputs/`.

## 7. Reproducing

Short version — requires the original data; full instructions in [`docs/REPRODUCING.md`](docs/REPRODUCING.md):

```bash
python3.9 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests          # integrity tests (run without data)
cd notebooks && jupyter lab                   # notebooks expect ../data_raw/ and ../outputs/
```

Verified for this release: the integrity tests pass, all modules import, and all notebook code cells are syntactically valid. The notebooks were **not** re-executed as part of the release (the data are not part of it); their executed state is documented in the reports and summaries.

## 8. Snapshot and provenance

* Built from development commit `067279b809c0dff21e70a96995fd19dbfb950fd4`, which is the state the thesis reports (e.g. Structured N = 61). Each released file and its source are listed in [`RELEASE_MANIFEST.md`](RELEASE_MANIFEST.md).
* **Deliberately excluded:** (a) all data; (b) the later re-analysis of the Structured data on a larger data export (post-thesis work, tracked separately); (c) the Stanford Health Study code, reports and outputs; (d) internal workflow material (branch plans, AI-assistant instruction files, backups, website sources).
* Some reports refer to files such as `CLAUDE.md` or to "Claude Code sessions". These are AI-assistant working files of the development repository and are not part of this release (see [§9](#9-use-of-ai-assistance)).
* Reports are reproduced as written at the snapshot. They record the development process (including bugs found and fixed), so they contain planning language and intermediate states; the **thesis is the authoritative statement of results**.
* Participant UUIDs and an absolute home-directory path in one notebook were redacted; no other edits were made to released documents.

## 9. Use of AI assistance

In line with the statement in the thesis (Methodology, *Use of artificial intelligence*): ChatGPT and Claude (including the Claude Code coding assistant) were used as supporting aids for planning analyses, code development and debugging, drafting documentation, and revising wording; NotebookLM was used to organise source material. The tools were not treated as sources and did not independently determine the study design, operationalisations, statistical interpretations or conclusions. Suggested code and claims were reviewed against the data, executed outputs and original sources. A large part of the working reports and companion documentation in this repository was drafted with Claude Code under the author's direction and review. The author is responsible for the accuracy and integrity of all content.

## 10. License and citation

* **Code** (`src/`, `scripts/`, `tests/`, code in `notebooks/`): [MIT](LICENSE).
* **Documentation, reports, figures and result tables** (`docs/`, `data_docs/`, `outputs/`, `thesis_figures/`, all `.md` files): [CC BY 4.0](LICENSE-CC-BY-4.0.txt).
* **Data**: not included and not covered by either license.

Please cite the thesis (preferred) and this repository — see [`CITATION.cff`](CITATION.cff) (GitHub shows a "Cite this repository" button).

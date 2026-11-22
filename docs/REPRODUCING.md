# Reproducing the analysis

> **Requires the original data**, which are not part of this repository ([`../DATA_AVAILABILITY.md`](../DATA_AVAILABILITY.md)). Without them you can read and audit everything, but not execute the notebooks.
>
> The release itself was verified structurally (integrity tests, module imports, notebook syntax). The pipeline was **not** re-executed end to end on the release, because the data are not part of it.

## 1. Environment

Developed and run with **Python 3.9** (3.9.4). Versions are pinned in [`../requirements.txt`](../requirements.txt).

```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests      # integrity tests; no data needed
```

## 2. Data layout

Place the original data under `data_raw/` using exactly the folder names in [`../data_raw/README.md`](../data_raw/README.md). Nothing under `data_raw/` is ever modified by the code.

## 3. How notebooks find files

Notebooks use **relative paths from the `notebooks/` directory** (`../data_raw/…`, `../outputs/…`, and `from src.… import …` after adding the repository root to `sys.path`). Start Jupyter inside `notebooks/` (or execute with `python scripts/execute_notebook.py <notebook> --cwd notebooks`).

## 4. Run order

Run top-to-bottom within a stage; later stages read the files that earlier stages write to `outputs/`.

| Stage | DS5 | DS4 | DS6 | Structured |
|---|---|---|---|---|
| 0 inspect → clean | 05 → 06 | 03 → 04 | 07 → 08 | 15 → 16 |
| 1 features | 13 | 12 | 14 | 17 |
| 4·1 models | 41–47, then v2: 60, 60b, 61, 62 | 51–57 | 73 → 74 → 75 → 72 → 78 → 71 | 64 → 65 → 63 → 62 → 68 → 61 → 66 → 67 |
| 4·2 phenotyping | 100, 101–106, 63, 64, 107, 108 | 59, 131–133 | 140, 141 | 120 → 122 → 121 → 124 → 123 |

Ordering rules for DS5 and DS4 (derived from which notebooks read which output folders):

* the **StoP** notebook (DS5 `43`, DS4 `53`) runs first — the other families read its fitted parameters;
* **GaT and ABM** (DS5 `46`, `47`; DS4 `56`, `57`) run after the phenotyping Phase 1 notebook (DS5 `100`, DS4 `59`) — they read the phenotype assignments;
* the remaining families can follow in numeric order. If a notebook needs an output that does not exist yet, the load cell fails with a missing-file error; run the notebook that writes that file first.

The documented dependency chains for DS6 and Structured (and the reasoning) are in `outputs/reports/stage4/ds6_step1_plan.md` and `outputs/reports/structured/structured_cas_modeling_plan.md`; the per-family blueprints in `outputs/reports/stage4/step1_modeling/` and `outputs/reports/structured/` state each model's inputs.

## 5. Thesis figures

The scripts in [`../scripts/`](../scripts/README.md) redraw the thesis figures **from the tables the notebooks write**, in a common thesis style (`scripts/thesis_style.py`). They write to `latex_master_thesis/figure/<subdir>/` relative to the repository root (the thesis folder layout of the development repository). To use them, create that folder (or place the thesis sources there). The finished figures as printed are frozen in [`../thesis_figures/`](../thesis_figures/README.md).

**Structured figures:** the scripts that import `structured_old_data` (see `scripts/README.md`) load the Structured result tables of the snapshot (61 participants) through `scripts/structured_old_data.py`. In the development repository this read those tables from git history (commit `067279b`); a release has no such history. Instead: re-run the Structured notebooks on the **2026-07-22** export and point the environment variable `STRUCTURED_OLD_DATA_DIR` at the resulting `outputs/model_outputs/structured/` folder.

## 6. What to expect

* Randomness: clustering stability checks and the simulation-based notebooks (ABM, bootstrap) use resampling. Small numerical differences from the printed values are possible; the stability diagnostics are reported in the `model_run_summary.md` files.
* Intermediate files (cleaned data, feature tables, per-participant outputs) are written to `outputs/…` and are covered by `.gitignore` so they cannot be committed by accident.

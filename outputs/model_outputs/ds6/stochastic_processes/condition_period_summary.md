# condition_period_summary.csv

## Contents
Condition × period aggregate StoP statistics — the 3×2 (study_condition × study_period)
summary table underlying the notebook's condition-comparison figures and tests.

## Unit of observation
One row per (study_condition × study_period) combination (6 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_condition` | str | control / default / intervention |
| `study_period` | str | baseline / intervention |
| `n` | int | Eligible participants in this cell |
| `mu_mean`, `mu_median`, `mu_std` | float | Drift (mu_hat) summary stats |
| `sig_mean`, `sig_median`, `sig_std` | float | Diffusion (sig_hat) summary stats |
| `fano_mean`, `fano_median` | float | Burstiness (Fano factor) summary stats |

## Production
- Source: `participant_stop_parameters.csv` (this folder), aggregated
- Producing notebook: `notebooks/73_ds6_stochastic_processes.ipynb`

## Cleaning / derivation steps applied
- Grouped `participant_stop_parameters.csv` by `study_condition` × `study_period`; NaN parameters excluded from each cell's stats (not imputed).

## Known limitations
- `study_condition = 'control'` includes rows from both periods — the condition label does not itself change what `study_period` means (see `data_docs/modeling_cautions.md` §6).
- Small per-cell N (control n≈73–76) limits precision of within-cell statistics.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/stochastic_processes/condition_period_summary.csv'))
```

# condition_period_summary.csv

## Contents
Condition × period aggregate InT statistics (mean/median of every entropy measure) — the
3×2 (study_condition × study_period) summary table underlying the notebook's condition
comparison figure.

## Unit of observation
One row per (study_condition × study_period) combination (6 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_condition` | str | control / default / intervention |
| `study_period` | str | baseline / intervention |
| `n` | int | Participants in this cell |
| `H_app_mean`, `H_app_median` | float | App entropy summary stats |
| `H_hour_mean`, `H_hour_median` | float | Hour-of-day entropy summary stats |
| `H_emp_mean`, `H_emp_median` | float | Empirical daily-count entropy summary stats |
| `H_SDE_mean`, `H_SDE_median` | float | Gaussian-bridge entropy summary stats |
| `I_consec_mean`, `I_consec_median` | float | NeT-InT bridge mutual-information summary stats |

## Production
- Source: `participant_entropy_metrics.csv` (this folder), aggregated
- Producing notebook: `notebooks/75_ds6_information_theory.ipynb`

## Cleaning / derivation steps applied
- Grouped by `study_condition` × `study_period`; NaN values excluded per-cell, not imputed.

## Known limitations
- Same `study_condition='control'` spans-both-periods caveat as the StoP/NeT versions of this file.
- Small per-cell N limits precision.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/information_theory/condition_period_summary.csv'))
```

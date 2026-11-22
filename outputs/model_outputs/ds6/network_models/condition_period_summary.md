# condition_period_summary.csv

## Contents
Condition × period aggregate NeT statistics — the 3×2 (study_condition × study_period)
summary table underlying the notebook's condition-comparison figure.

## Unit of observation
One row per (study_condition × study_period) combination (6 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_condition` | str | control / default / intervention |
| `study_period` | str | baseline / intervention |
| `n` | int | NeT-eligible participants in this cell |
| `hhi_mean`, `hhi_median` | float | HHI_net summary stats |
| `rho_mean`, `rho_median` | float | rho_self summary stats |
| `h_trans_mean`, `h_trans_median` | float | H_trans summary stats |

## Production
- Source: `participant_network_metrics.csv` (this folder), aggregated
- Producing notebook: `notebooks/74_ds6_network_models.ipynb`

## Cleaning / derivation steps applied
- Grouped `participant_network_metrics.csv` by `study_condition` × `study_period`; NaN (ineligible) participants excluded from each cell's stats, not imputed.

## Known limitations
- Same condition/period independence caveat as the StoP version of this file — `study_condition='control'` spans both periods.
- Small per-cell N limits precision.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/network_models/condition_period_summary.csv'))
```

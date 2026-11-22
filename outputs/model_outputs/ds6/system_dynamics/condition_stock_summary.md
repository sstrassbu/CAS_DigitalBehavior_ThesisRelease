# condition_stock_summary.csv

## Contents
Mean psychosocial change (both stocks) by `study_condition` — descriptive breakdown plus the
condition-level ANOVA reported in `model_run_summary.md`.

## Unit of observation
One row per study_condition (3 rows: control, default, intervention).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_condition` | str | control / default / intervention |
| `n` | int | Prepost-eligible participants in this condition |
| `addiction_index_change_mean` | float | Mean addiction_index_change within this condition |
| `self_control_index_change_mean` | float | Mean self_control_index_change within this condition |

## Production
- Source: `participant_stock_flow.csv` (this folder)
- Producing notebook: `notebooks/78_ds6_system_dynamics.ipynb`

## Cleaning / derivation steps applied
- Grouped by `study_condition`; simple means. One-way ANOVA on `addiction_index_change` across the 3 conditions reported separately in `model_run_summary.md` (F=1.225, p=0.296 — not significant).

## Known limitations
- `study_condition` is quasi-experimental (cohort-level), not individually randomized — differences here cannot be interpreted causally even if they had been significant.
- ANOVA not significant — condition does not detectably explain variation in addiction_index_change at this N.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/system_dynamics/condition_stock_summary.csv'))
```

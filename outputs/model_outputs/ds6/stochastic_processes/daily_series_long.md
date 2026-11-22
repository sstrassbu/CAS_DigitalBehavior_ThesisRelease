# daily_series_long.csv

## Contents
The zero-filled daily attempt-count grid underlying every StoP parameter estimate — long
format, one row per participant × study_period × calendar day within that participant's
active window for that period. Kept for reproducibility and reuse by downstream DS6 models
(DyS, InT).

## Unit of observation
One row per participant × study_period × calendar day (N=10,242).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_period` | str | baseline / intervention |
| `event_date` | date | Calendar day (UTC) |
| `day_index` | int | 0-indexed position within this participant's grid for this period (0 = first active day) |
| `N_t` | int | App-opening event count on this day; 0 for zero-filled (no-activity) days |

## Production
- Source: `outputs/cleaned/ds6_behavioral_clean.csv`
- Producing notebook: `notebooks/73_ds6_stochastic_processes.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_stop_blueprint.md`

## Cleaning / derivation steps applied
- Built per participant × period: a regular daily grid from first to last active day (inclusive), non-observed days filled with `N_t=0` (a real, meaningful zero — see blueprint Part 2).
- No eligibility filter applied at this table's level — includes participants/periods later excluded from `participant_stop_parameters.csv` for having <7 active days. Filter downstream if you need eligible-only rows.

## Known limitations
- A zero day means no app-opening event was logged that day within this participant's already-observed window — it does not mean the participant was unreachable/inactive in the study overall.
- Gaps in `day_index` continuity do not occur (grid is regular by construction); gaps in real activity show up as `N_t=0` rows instead.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/stochastic_processes/daily_series_long.csv'), parse_dates=['event_date'])
```

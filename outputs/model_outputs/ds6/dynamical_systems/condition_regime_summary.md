# condition_regime_summary.csv

## Contents
Condition × period × regime counts — a long-format breakdown of how many participants in
each `study_condition` fall into each DyS regime, per period.

## Unit of observation
One row per (study_condition × study_period × regime) combination (3 conditions × 2 periods
× 4 regimes = 24 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_condition` | str | control / default / intervention |
| `study_period` | str | baseline / intervention |
| `regime` | str | declining / growing / resting / stochastic |
| `n` | int | Count of participants in this condition × period × regime cell |

## Production
- Source: `participant_regime_classification.csv` (this folder)
- Producing notebook: `notebooks/72_ds6_dynamical_systems.ipynb`

## Cleaning / derivation steps applied
- Grouped by `study_condition` and counted `regime_<period>` values; all 4 regime labels included per cell even when count is 0 (not dropped), so the table is always 24 rows.

## Known limitations
- Small per-cell N in some condition × period × regime combinations (e.g. `declining` in intervention has only 2 participants total across all conditions) — do not over-interpret condition differences at this granularity.
- Same `study_condition='control'` spans-both-periods caveat as other DS6 condition-period tables.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/dynamical_systems/condition_regime_summary.csv'))
```

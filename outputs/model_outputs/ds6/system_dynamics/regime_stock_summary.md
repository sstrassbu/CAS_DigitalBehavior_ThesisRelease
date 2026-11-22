# regime_stock_summary.csv

## Contents
Mean psychosocial change (both stocks) broken down by DyS baseline-period regime label —
an exploratory cross-check of whether the dynamical-systems regime classification relates
to self-reported psychosocial change.

## Unit of observation
One row per DyS `regime_baseline` category (4 rows: declining, growing, resting, stochastic).

## Column reference

| Column | Type | Description |
|---|---|---|
| `regime_baseline` | str | declining / growing / resting / stochastic (from DyS, notebook 72) |
| `n` | int | Prepost-eligible participants in this regime |
| `addiction_index_change_mean` | float | Mean addiction_index_change within this regime |
| `self_control_index_change_mean` | float | Mean self_control_index_change within this regime |

## Production
- Source: `participant_stock_flow.csv` (this folder)
- Producing notebook: `notebooks/78_ds6_system_dynamics.ipynb`

## Cleaning / derivation steps applied
- Grouped by `regime_baseline`; simple means, no significance testing performed on this specific breakdown (descriptive only — the formal hypothesis tests are in `feedback_loop_tests.csv`).

## Known limitations
- Descriptive only — no significance test run on these group differences; do not treat visual differences between regime means as confirmed findings.
- Small per-regime N (22–96) limits precision, especially for `declining` (n=22) and `growing` (n=26).

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/system_dynamics/regime_stock_summary.csv'))
```

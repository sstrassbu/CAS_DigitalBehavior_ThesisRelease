# regime_transition_matrix.csv

## Contents
4×4 contingency table of regime at baseline vs regime at intervention, for the 230
participants classified in both periods — the table underlying this notebook's headline
finding (mostly a level shift, not a trend shift; see `model_run_summary.md`).

## Unit of observation
One row per baseline regime (4 rows); columns are intervention-regime counts.

## Column reference

| Column | Type | Description |
|---|---|---|
| `regime_baseline` | str | Regime at baseline: declining / growing / resting / stochastic |
| `declining`, `growing`, `resting`, `stochastic` | int | Count of participants transitioning from `regime_baseline` to this intervention regime |

## Production
- Source: `participant_regime_classification.csv` (this folder)
- Producing notebook: `notebooks/72_ds6_dynamical_systems.ipynb`

## Cleaning / derivation steps applied
- `pd.crosstab` on the 230 participants with a valid (non-NaN) regime label in both periods — 13 participants excluded (ineligible in at least one period, per StoP's own eligibility, not imputed).

## Known limitations
- 230 of 243 participants only — does not represent the full sample.
- Row/column totals will not match `participant_regime_classification.csv`'s period-level regime counts exactly, since those counts include the 13 single-period-only participants this table excludes.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/dynamical_systems/regime_transition_matrix.csv'), index_col='regime_baseline')
```

# regime_int_bridge.csv

## Contents
DyS-InT bridge validation: compares H_emp (InT, notebook 75) between deterministic- and
stochastic-regime participants, per period — tests the blueprint's stated prediction
(Part 4) that deterministic participants should show lower entropy.

## Unit of observation
One row per study_period (2 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_period` | str | baseline / intervention |
| `n_deterministic` | int | Participants with `is_dys_eligible_<period>=True` and non-missing H_emp |
| `n_stochastic` | int | Participants with `is_dys_eligible_<period>=False` and non-missing H_emp |
| `H_emp_mean_deterministic` | float | Mean H_emp among deterministic-regime participants |
| `H_emp_mean_stochastic` | float | Mean H_emp among stochastic-regime participants |
| `t_stat` | float | Welch's t-statistic (unequal variance) |
| `p_value` | float | Two-sided p-value |

## Production
- Source: `participant_regime_classification.csv` (this folder) + `outputs/model_outputs/ds6/information_theory/participant_entropy_metrics.csv`
- Producing notebook: `notebooks/72_ds6_dynamical_systems.ipynb`

## Cleaning / derivation steps applied
- Welch's t-test (`scipy.stats.ttest_ind(equal_var=False)`) comparing H_emp between the two regime groups, per period, on complete cases.

## Known limitations
- Confirmed the pre-registered prediction (deterministic < stochastic H_emp) both periods — treat as a successful validation of the regime classification's construct validity, not a novel discovery in its own right.
- Two tests only, both significant (p=2.5e-06, p=1.5e-04) — no multiple-comparison concern here given the small number of tests and both being pre-specified.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/dynamical_systems/regime_int_bridge.csv'))
```

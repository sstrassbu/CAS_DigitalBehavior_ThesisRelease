# condition_macrostate_summary.csv

## Contents
Condition-level summary of macrostate metrics — the table underlying this notebook's
headline finding (friction conditions show significantly higher susceptibility than
control).

## Unit of observation
One row per study_condition (3 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `study_condition` | str | control / default / intervention |
| `n` | int | Participants in this condition |
| `H_joint_baseline_mean`, `H_joint_intervention_mean` | float | Mean joint entropy, per period |
| `pct_persistent` | float | % of participants with a persistent dominant configuration |
| `susceptibility_mean` | float | Mean Jensen-Shannon divergence (bits) |

## Production
- Source: `participant_macrostate_metrics.csv` (this folder), aggregated
- Producing notebook: `notebooks/71_ds6_statistical_mechanics.ipynb`

## Cleaning / derivation steps applied
- Grouped by `study_condition`; simple means, NaN excluded per-cell not imputed. One-way ANOVA on `susceptibility` reported separately in `model_run_summary.md` (F=5.437, p=0.0049 — significant) with pairwise Welch t-tests (control vs default p=0.0011, control vs intervention p=0.0075, default vs intervention p=0.22, not significant).

## Known limitations
- `study_condition` is quasi-experimental (cohort-level), not individually randomized — the significant susceptibility difference is associational, not a verified causal friction effect.
- Unlike every other DS6 condition-period table in this project, this one is NOT further split by `study_period` — `susceptibility` and `config_persistent` are already period-spanning quantities (they compare baseline to intervention within participant), so a further period split doesn't apply here the way it does for StoP/NeT/InT/DyS/SyD's condition×period tables.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/statistical_mechanics/condition_macrostate_summary.csv'))
```

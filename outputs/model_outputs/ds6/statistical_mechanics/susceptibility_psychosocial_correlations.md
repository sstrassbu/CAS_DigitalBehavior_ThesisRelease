# susceptibility_psychosocial_correlations.csv

## Contents
Exploratory Pearson correlations between StM macrostate measures (H_joint, susceptibility)
and DS6's wave-1 psychosocial indices.

## Unit of observation
One row per (macrostate measure × psychosocial scale) pair (6 rows: 3 measures {H_joint_
baseline, H_joint_intervention, susceptibility} × 2 scales).

## Column reference

| Column | Type | Description |
|---|---|---|
| `macrostate_measure` | str | H_joint_baseline, H_joint_intervention, or susceptibility |
| `psychosocial` | str | addiction_index_pre or self_control_index_pre |
| `n` | int | Non-missing pairs used |
| `r` | float | Pearson correlation coefficient |
| `p` | float | Two-sided p-value, uncorrected |

## Production
- Source: `participant_macrostate_metrics.csv` (this folder) merged with `outputs/features/ds6/ds6_survey_features.csv`
- Producing notebook: `notebooks/71_ds6_statistical_mechanics.ipynb`

## Cleaning / derivation steps applied
- Pairwise complete-case correlation (n≥10 required, else row omitted).
- No multiple-comparison correction applied.

## Known limitations
- **All 6 tests non-significant** (p range 0.19–0.96) — a genuine null, consistent with the mostly-null psychosocial pattern across every other DS6 Step 1 notebook (StoP, NeT, InT, SyD). Not a headline result for this notebook.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/statistical_mechanics/susceptibility_psychosocial_correlations.csv'))
```

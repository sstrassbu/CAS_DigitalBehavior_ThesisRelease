# psychosocial_entropy_correlations.csv

## Contents
Exploratory Pearson correlations between per-participant entropy measures and DS6's wave-1
psychosocial indices.

## Unit of observation
One row per (entropy_measure × psychosocial scale) pair (24 rows: 6 measures {H_app,
H_hour, H_emp, H_SDE, I_consec, H_app_marginal} × 2 periods × 2 scales).

## Column reference

| Column | Type | Description |
|---|---|---|
| `entropy_measure` | str | e.g. `H_app_baseline`, `H_SDE_intervention`, `I_consec_baseline` |
| `psychosocial` | str | addiction_index_pre or self_control_index_pre |
| `n` | int | Non-missing pairs used |
| `r` | float | Pearson correlation coefficient |
| `p` | float | Two-sided p-value, uncorrected |

## Production
- Source: `participant_entropy_metrics.csv` (this folder) merged with `outputs/features/ds6/ds6_survey_features.csv`
- Producing notebook: `notebooks/75_ds6_information_theory.ipynb`

## Cleaning / derivation steps applied
- Pairwise complete-case correlation per row (n≥10 required, else row omitted).
- No multiple-comparison correction applied — treat as exploratory/hypothesis-generating.

## Known limitations
- 24 tests, uncorrected — 2/24 nominally significant at p<0.05 (strongest: H_SDE_baseline ~ addiction_index_pre, r=0.171, p=0.009), consistent with the mostly-null pattern already seen in DS6's StoP and NeT psychosocial correlation tables. Not treated as a headline finding.
- `addiction_index_pre`/`self_control_index_pre` are wave-1 (pre-intervention) only.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/information_theory/psychosocial_entropy_correlations.csv'))
```

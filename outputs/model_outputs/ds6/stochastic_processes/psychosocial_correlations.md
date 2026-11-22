# psychosocial_correlations.csv

## Contents
Exploratory Pearson correlations between per-participant StoP parameters and DS6's wave-1
psychosocial indices.

## Unit of observation
One row per (SDE parameter × psychosocial scale) pair (14 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `sde_param` | str | One of: mu_hat_baseline, sig_hat_baseline, fano_baseline, mu_hat_intervention, sig_hat_intervention, fano_intervention, h_period |
| `psychosocial` | str | addiction_index_pre or self_control_index_pre |
| `n` | int | Non-missing pairs used |
| `r` | float | Pearson correlation coefficient |
| `p` | float | Two-sided p-value, uncorrected |

## Production
- Source: `participant_stop_parameters.csv` (this folder) merged with `outputs/features/ds6/ds6_survey_features.csv`
- Producing notebook: `notebooks/73_ds6_stochastic_processes.ipynb`

## Cleaning / derivation steps applied
- Pairwise complete-case correlation per row (n≥10 required, else row omitted).
- No multiple-comparison correction applied — treat as exploratory/hypothesis-generating, not confirmatory.

## Known limitations
- 14 tests, uncorrected — expect ~1 nominally-significant result by chance alone at α=0.05.
- `addiction_index_pre`/`self_control_index_pre` are wave-1 (pre-intervention) only; no causal ordering implied relative to intervention-period StoP parameters.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/stochastic_processes/psychosocial_correlations.csv'))
```

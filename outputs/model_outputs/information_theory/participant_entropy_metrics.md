# participant_entropy_metrics.csv

## Contents
Per-participant behavioral entropy metrics from the DS5 Information Theory notebook.
One row per DS5 participant in the survey features file (N up to 572).

## Unit of observation
One row per participant.

## Column reference

| Column | Type | Description |
|---|---|---|
| participant_id_canonical | str | Canonical participant identifier |
| study_condition | str | RCT condition: control / default / reintervention |
| n_days | float | Number of observation days used for H_emp/H_SDE (NaN if < MIN_DAYS) |
| H_out | float | Shannon entropy (bits) over outcome distribution {opened, dismissed} |
| H_app | float | Shannon entropy (bits) over app distribution — Stage 1 feature |
| H_hour | float | Shannon entropy (bits) over hour-of-day distribution — Stage 1 feature |
| H_emp | float | Shannon entropy (bits) of K=10 binned daily X_t series (NaN if < 7 days) |
| H_SDE | float | Gaussian differential entropy (bits) = ½ log₂(2πe σ̂²); bridge from StoP |
| sig_hat | float | StoP estimated diffusion parameter (NaN if < 7 days) |

## Production
- Source: outputs/cleaned/ds5_behavioral_clean.csv, outputs/features/ds5/, outputs/model_outputs/stochastic_processes/
- Producing notebook: notebooks/45_ds5_information_theory.ipynb
- Stage: Stage 4, Step 1

## Cleaning steps applied
- Behavioral file filtered to valid outcomes: opened, dismissed
- H_emp and H_SDE require MIN_DAYS >= 7 (same threshold as StoP)
- H_out requires MIN_EVENTS_OUT >= 10 valid events

## Known limitations
- H_SDE bridge equation NOT yet in conceptual paper
- H_out is condition-confounded by outcome-rate structure
- All measures describe behavioral distributions, not latent psychological states

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/information_theory/participant_entropy_metrics.csv'))
```

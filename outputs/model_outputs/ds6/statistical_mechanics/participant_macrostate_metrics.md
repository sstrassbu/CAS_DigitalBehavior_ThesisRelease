# participant_macrostate_metrics.csv

## Contents
Per-participant Statistical Mechanics (StM) macrostate metrics for DS6: joint (app,
time-of-day) configuration entropy, dominant configuration, persistence, and susceptibility.

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `H_joint_baseline`, `H_joint_intervention` | float | Shannon entropy (bits) of the joint (app_name, hour_bucket) microstate distribution, per period |
| `dominant_config_baseline`, `dominant_config_intervention` | str | The single most frequent "app\|hour_bucket" microstate, per period |
| `dominant_config_share_baseline`, `dominant_config_share_intervention` | float | That microstate's share of all events in the period |
| `config_persistent` | int (0/1) | 1 if dominant_config_baseline == dominant_config_intervention |
| `susceptibility` | float | Jensen-Shannon divergence (bits) between the baseline and intervention microstate distributions |

**hour_bucket definition:** night(0-5), morning(6-11), afternoon(12-17), evening(18-23) —
reuses the exact boundaries already established in Stage 1's `morning_event_share`/
`evening_event_share` features.

## Production
- Source: `outputs/cleaned/ds6_behavioral_clean.csv`
- Producing notebook: `notebooks/71_ds6_statistical_mechanics.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_stm_blueprint.md`

## Cleaning / derivation steps applied
- Microstate = `app_name + '|' + hour_bucket`, computed per event.
- Minimum 5 events per participant × period required for entropy/dominant-config computation; below that, NaN (not imputed).
- Susceptibility computed via `scipy.spatial.distance.jensenshannon` (base 2), squared to convert the returned distance into the divergence in bits, over the union of microstates observed in either period for that participant.

## Known limitations
- `hour_bucket` is a 4-category coarsening — results are sensitive to bucket choice in principle, not tested here (see blueprint FLAG StM-2 for why these specific boundaries were chosen).
- `config_persistent` is based on a single dominant configuration — check `dominant_config_share` alongside it; a low-share "dominant" configuration in a diffuse distribution is a weaker signal than a high-share one.
- No literal thermodynamic quantities (β/T/Z/F) computed — see blueprint Part 0 for why.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/statistical_mechanics/participant_macrostate_metrics.csv'))
```

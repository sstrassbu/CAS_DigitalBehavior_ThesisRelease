# mutual_information_summary.csv

## Contents
Single-row result of the pooled mutual-information test `I(study_period; app_name)` — the
one DS6-specific MI test this notebook implements (DS5 deferred all MI/KL work; see
blueprint Part 0 for why DS6 has a specific, paper-grounded reason to include one).

## Unit of observation
One row — a single pooled result computed over all 353,796 behavioral events, not per
participant.

## Column reference

| Column | Type | Description |
|---|---|---|
| `pair` | str | Always "study_period;app_name" |
| `H_app_pooled` | float | Shannon entropy (bits) of the app_name distribution, pooled across all events and participants |
| `I_mutual_info` | float | I(study_period; app_name), bits |
| `normalized_mi` | float | I_mutual_info / H_app_pooled |
| `n_events` | int | 353,796 |

## Production
- Source: `outputs/cleaned/ds6_behavioral_clean.csv`
- Producing notebook: `notebooks/75_ds6_information_theory.ipynb`

## Cleaning / derivation steps applied
- Computed via the standard identity `I(X;Y) = sum p(x,y) log2(p(x,y)/(p(x)p(y)))` on the pooled joint distribution of `study_period` and `app_name`.

## Known limitations
- **Genuine null result** (I=0.0003 bits, normalized 0.02%) — knowing the period barely reduces uncertainty about which app is opened, at the pooled population level. Does NOT contradict NeT's (74) per-participant HHI_net-volume finding — see `model_run_summary.md` "Headline finding 2" for why these are different, non-contradictory quantities.
- Pooled result only — no participant-level MI is computed here (would require enough per-participant events split by period, not attempted in this pass).

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/information_theory/mutual_information_summary.csv'))
```

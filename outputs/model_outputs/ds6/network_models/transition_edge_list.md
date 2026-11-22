# transition_edge_list.csv

## Contents
The full directed weighted app-transition graph underlying every network metric — one row
per distinct (participant, period, app_from, app_to) edge.

## Unit of observation
One row per participant × study_period × directed app pair (N=6,205).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `app_from` | str | Source app of the transition |
| `app_to` | str | Destination app of the transition |
| `count` | int | Number of times this specific transition occurred |
| `study_period` | str | baseline / intervention |
| `share` | float | `count` / participant's total transitions in that period (row-normalized by participant, not by app_from — this is out-flow share of the whole edge, not the transition-matrix row `T_ij`; recompute `T_ij` from `count` grouped by `app_from` if needed) |

## Production
- Source: `outputs/cleaned/ds6_behavioral_clean.csv`
- Producing notebook: `notebooks/74_ds6_network_models.ipynb`

## Cleaning / derivation steps applied
- Same self-derived transition construction as `participant_network_metrics.csv` (see that file's companion doc) — built from time-sorted rows via `shift(-1)`, not `app_next`.
- Includes ALL participants with at least 1 transition in a period, even those below the `is_net_eligible` threshold in `participant_network_metrics.csv` — filter on that flag if you need eligible-only edges.

## Known limitations
- `share` is normalized by total transitions for the participant×period, not by `app_from` — do not read it as a transition probability `T_ij` directly.
- Edges spanning long real-world gaps (e.g. overnight) are included without a time-gap filter, matching DS5 NeT's own FLAG G1 precedent — represents temporal adjacency, not necessarily within-session coupling.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/network_models/transition_edge_list.csv'))
```

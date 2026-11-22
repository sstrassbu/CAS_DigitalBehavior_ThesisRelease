# stop_net_period_comparison.csv

## Contents
Per-participant join of StoP (notebook 73) volume-change data against NeT (notebook 74)
concentration-change data — the table underlying this notebook's headline cross-model
finding (`corr(hhi_change, volume_change) = -0.213, p=0.0012`).

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `HHI_net_baseline`, `HHI_net_intervention` | float | From `participant_network_metrics.csv` |
| `hhi_change` | float | HHI_net_intervention − HHI_net_baseline |
| `rho_self_baseline`, `rho_self_intervention` | float | From `participant_network_metrics.csv` |
| `mean_N_baseline`, `mean_N_intervention` | float | From StoP's `participant_stop_parameters.csv` |
| `volume_change` | float | mean_N_intervention − mean_N_baseline |
| `h_period` | float | From StoP's `participant_stop_parameters.csv` (drift shift, not used in the headline correlation itself) |

## Production
- Source: `participant_network_metrics.csv` (this folder), `../stochastic_processes/participant_stop_parameters.csv`
- Producing notebook: `notebooks/74_ds6_network_models.ipynb`

## Cleaning / derivation steps applied
- Direct merge on `participant_id_canonical`; `hhi_change`/`volume_change` computed as simple differences.
- Headline correlation computed on complete cases only (both hhi_change and volume_change non-NaN, n=227).

## Known limitations
- Correlational, not causal — both quantities are observational period-over-period changes for the same participants; no random assignment of "how much a participant cut back."
- n=227 (not 243) — participants missing either StoP or NeT eligibility in either period are excluded from the correlation, not imputed.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/network_models/stop_net_period_comparison.csv'))
```

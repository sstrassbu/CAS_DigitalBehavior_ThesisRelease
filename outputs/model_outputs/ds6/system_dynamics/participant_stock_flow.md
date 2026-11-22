# participant_stock_flow.csv

## Contents
Per-participant System Dynamics (SyD) stock-flow table for DS6: psychosocial "stock"
levels/changes (addiction_index, self_control_index) merged with behavioral "flow"
quantities from StoP and DyS.

## Unit of observation
One row per prepost-eligible participant (N=188 — has both survey waves and behavioral
data; see `outputs/features/ds6/ds6_features.md`'s "ds6_prepost_features.csv — Feature
Definitions" section for the eligibility definition and sign convention — **link corrected
2026-08-07**: `ds6_prepost_features.csv` does not have its own standalone companion `.md`;
its documentation lives inside the shared Stage 1 `ds6_features.md`, the same umbrella-doc
convention DS1/DS4/DS5/Structured all use for their own original Stage 1 feature outputs).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `addiction_index_pre`, `addiction_index_post` | float | "App-use pressure" stock level at wave 1 / wave 2 |
| `addiction_index_change` | float | post − pre (positive = worsening, per the sign convention fixed in `ds6_prepost_features.csv`) |
| `self_control_index_pre`, `self_control_index_post` | float | "Self-regulation" stock level at wave 1 / wave 2 |
| `self_control_index_change` | float | post − pre (positive = improvement) |
| `mean_N_baseline` | float | From StoP (`participant_stop_parameters.csv`) — behavioral flow input for Loop 1 |
| `mu_hat_baseline` | float | From StoP — alternate flow input for Loop 1 |
| `volume_change` | float | mean_N_intervention − mean_N_baseline — flow input for Loop 2 |
| `regime_baseline`, `regime_intervention` | str | From DyS (`participant_regime_classification.csv`) |

## Production
- Source: `outputs/features/ds6/ds6_prepost_features.csv`, `outputs/features/ds6/ds6_survey_features.csv`, `outputs/model_outputs/ds6/stochastic_processes/participant_stop_parameters.csv`, `outputs/model_outputs/ds6/dynamical_systems/participant_regime_classification.csv`
- Producing notebook: `notebooks/78_ds6_system_dynamics.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_syd_blueprint.md`

## Cleaning / derivation steps applied
- Direct merges on `participant_id_canonical`; `volume_change` computed as a simple difference.
- No new eligibility filter beyond `ds6_prepost_features.csv`'s own N=188 — some rows have additional NaN in `mean_N_baseline`/`mu_hat_baseline`/`volume_change` if that participant was StoP-ineligible in a given period (not imputed).

## Known limitations
- `addiction_index`/`self_control_index` are self-reported, not directly observed behavior.
- N=188, not the full N=243 behavioral sample — 60 participants lack a usable wave-2 survey.
- `study_condition` is quasi-experimental (cohort-level), not individually randomized.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/system_dynamics/participant_stock_flow.csv'))
```

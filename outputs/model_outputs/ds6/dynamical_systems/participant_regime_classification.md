# participant_regime_classification.csv

## Contents
Per-participant Dynamical Systems (DyS) regime classification for DS6, derived from the
sigma→0 deterministic limit of StoP's SDE, per period.

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `regime_baseline` | str | One of: declining, resting, growing, stochastic (baseline period) |
| `is_dys_eligible_baseline` | bool | True if sig_hat_baseline < sigma_threshold_baseline (deterministic-eligible) |
| `sigma_threshold_baseline` | float | Median sig_hat_baseline across all participants — the period-specific eligibility cutoff |
| `mu_hat_baseline`, `sig_hat_baseline` | float | Reused directly from StoP's `participant_stop_parameters.csv` |
| `regime_intervention`, `is_dys_eligible_intervention`, `sigma_threshold_intervention`, `mu_hat_intervention`, `sig_hat_intervention` | — | Same 5 columns, intervention period |

**Regime definitions** (`classify_regime()` in the producing notebook):
- `stochastic`: sig_hat >= sigma_threshold (that period) — deterministic limit not a good description
- `declining`: deterministic-eligible AND mu_hat < −0.5 (drifts toward the floor at N=0)
- `growing`: deterministic-eligible AND mu_hat > +0.5 (drifts upward, no ceiling)
- `resting`: deterministic-eligible AND |mu_hat| <= 0.5 (hovers near an interior fixed point, mean_N)

## Production
- Source: `outputs/model_outputs/ds6/stochastic_processes/participant_stop_parameters.csv`
- Producing notebook: `notebooks/72_ds6_dynamical_systems.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_dys_blueprint.md`

## Cleaning / derivation steps applied
- `sigma_threshold` computed as the median `sig_hat` within each period independently (FLAG DyS-1) — NOT one pooled threshold — to control for StoP's own documented window-length precision asymmetry (baseline ~15-day window vs intervention ~28-day window).
- `MU_THRESHOLD=0.5` reused unchanged from StoP (attempts/day scale).

## Known limitations
- DS6's state variable (daily attempt count) is bounded only below (floor at 0), unlike DS5's double-bounded [0,1] rate — the `declining`/`growing`/`resting` 3-way split is DS6-specific and not comparable to DS5's boundary-fixed-point framing (see blueprint Part 0).
- `MU_THRESHOLD` is absolute, not period-relative — window-length differences in mu_hat estimation precision likely contribute to the intervention-period "resting" surge (95 vs baseline's 51), not purely a behavioral shift. See `model_run_summary.md` "Interpretive caution."
- Regime labels describe a behavioral-volume proxy, not directly observed psychological states.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/dynamical_systems/participant_regime_classification.csv'))
```

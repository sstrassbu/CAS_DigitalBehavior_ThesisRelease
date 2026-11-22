# participant_stop_parameters.csv

## Contents
Per-participant Stochastic Processes (StoP) parameters for DS6, estimated separately for
the baseline and intervention periods. One row per behavioral participant.

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `mu_hat_baseline` | float | Drift (attempts/day trend) in the baseline period, method-of-moments estimate on the zero-filled daily attempt-count grid. NaN if <7 active days. |
| `sig_hat_baseline` | float | Diffusion (day-to-day variability) in the baseline period. NaN if <7 active days. |
| `sigma_mu_ratio_baseline` | float | sig_hat_baseline / \|mu_hat_baseline\|. NaN if \|mu_hat_baseline\| < 0.5 (MU_THRESHOLD). |
| `fano_baseline` | float | Var(N_t)/Mean(N_t) on the raw (non-differenced) baseline grid — burstiness. |
| `n_active_days_baseline` | int | Days with N_t > 0 within the baseline window. |
| `span_days_baseline` | int | Calendar days from first to last active baseline day (inclusive). |
| `mean_N_baseline` | float | Mean daily attempt count over the zero-filled baseline grid. |
| `mu_hat_intervention` | float | Same as mu_hat_baseline, intervention period. |
| `sig_hat_intervention` | float | Same as sig_hat_baseline, intervention period. |
| `sigma_mu_ratio_intervention` | float | Same as sigma_mu_ratio_baseline, intervention period. |
| `fano_intervention` | float | Same as fano_baseline, intervention period. |
| `n_active_days_intervention` | int | Same as n_active_days_baseline, intervention period. |
| `span_days_intervention` | int | Same as span_days_baseline, intervention period. |
| `mean_N_intervention` | float | Same as mean_N_baseline, intervention period. |
| `h_period` | float | mu_hat_intervention − mu_hat_baseline (within-participant drift shift). NaN unless both periods eligible. |

## Production
- Source: `outputs/cleaned/ds6_behavioral_clean.csv`, `outputs/features/ds6/ds6_behavior_features.csv` (sanity check only)
- Producing notebook: `notebooks/73_ds6_stochastic_processes.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_stop_blueprint.md`
- Stage: Stage 4, Step 1

## Cleaning / derivation steps applied
- State variable N_t = daily count of app-opening events, NOT DS5's opened/dismissed ratio (DS6 has no dismiss/close outcome — see blueprint Part 0).
- Zero-filled daily grid built from each participant's first to last active day, per period independently.
- Eligibility: MIN_ACTIVE_DAYS=7 per period (reused from `data_docs/modeling_cautions.md` §2, not re-derived).
- MU_THRESHOLD=0.5 attempts/day (rescaled from DS5's 0.005, which was tuned for a [0,1]-bounded rate — see blueprint Part 6 FLAG 4).

## Known limitations
- N_t is a behavioral volume proxy, not urge/self-control/habit strength.
- `study_condition` is quasi-experimental (cohort-level), not individually randomized.
- Baseline window (~15 days) is roughly half the length of the intervention window (~28 days) — sig_hat/fano comparisons across periods carry a built-in precision asymmetry (see `model_run_summary.md` "Estimation-precision caution").
- A third study phase mentioned in the raw project description ("50% returned to baseline / 50% opened restrictions") is not represented as a distinct `study_period` value in this export — open, unresolved.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/stochastic_processes/participant_stop_parameters.csv'))
```

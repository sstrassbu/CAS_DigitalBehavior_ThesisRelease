# DS6 StoP -- Model Run Summary

**Run at:** 2026-08-11 01:15:33
**Notebook:** notebooks/73_ds6_stochastic_processes.ipynb
**Blueprint:** outputs/reports/stage4/step1_modeling/ds6_stop_blueprint.md

## Eligibility
- Total participants: 243
- Baseline eligible (>=7 active days): 236 (97.1%)
- Intervention eligible (>=7 active days): 236 (97.1%)
- Both periods eligible: 230 (94.7%)

## Key results
- Mean mu_hat (baseline): 0.2466
- Mean mu_hat (intervention): 0.3399
- Mean sig_hat (baseline): 22.8163
- Mean sig_hat (intervention): 13.1766
- Median Fano factor (baseline): 6.582
- Median Fano factor (intervention): 3.342
- Mean h_period (intervention - baseline drift): +0.0810
- Paired t-test mu_hat_baseline vs mu_hat_intervention: t=-0.442, p=0.6592

## Proxy warning
N_t is a count-based behavioral volume measurement (daily app-opening attempts). It does NOT
directly measure urge, self-control, habit strength, or any latent psychological state. All
downstream interpretation must maintain this distinction.

## Known limitations
- DS6 has no dismiss/close outcomes -- state variable is attempt volume, not override rate.
- study_condition is quasi-experimental (cohort-level), not individually randomized.
- A third study phase ("50% returned to baseline / 50% opened restrictions", per the raw
  project description) is not represented as a distinct study_period value in this export --
  flagged as an open unknown, not resolved here.
- h_period is a within-participant descriptive comparison, not a causal estimate.

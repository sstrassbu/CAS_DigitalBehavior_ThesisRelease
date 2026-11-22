# participant_entropy_metrics.csv

## Contents
Per-participant Information Theory (InT) entropy profile for DS6, split by study_period.

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `H_app_baseline`, `H_app_intervention` | float | Shannon entropy (bits) of the app_name distribution — reused directly from Stage 1's `app_entropy_baseline`/`app_entropy_intervention` |
| `H_app_marginal_baseline`, `H_app_marginal_intervention` | float | Shannon entropy (bits) of the `app_to` (destination) marginal from the NeT transition edge list — used specifically for the `I_consec` bridge; NOT the same computation as `H_app` (see Known Limitations) |
| `H_hour_baseline`, `H_hour_intervention` | float | Shannon entropy (bits) of the hour_of_day distribution, computed fresh per period (not pre-split in Stage 1) |
| `H_emp_baseline`, `H_emp_intervention` | float | Shannon entropy (bits) of the K=10-quantile-binned daily attempt-count series (from StoP's `daily_series_long.csv`) |
| `H_SDE_baseline`, `H_SDE_intervention` | float | Gaussian differential entropy bridge from StoP's sig_hat: 0.5·log2(2πe·sig_hat²) |
| `I_consec_baseline`, `I_consec_intervention` | float | NeT-InT bridge: H_app_marginal − H_trans (NeT, notebook 74). Always ≥0 (verified). |

## Production
- Source: `outputs/features/ds6/ds6_behavior_features.csv`, `outputs/cleaned/ds6_behavioral_clean.csv`, `outputs/model_outputs/ds6/stochastic_processes/`, `outputs/model_outputs/ds6/network_models/`
- Producing notebook: `notebooks/75_ds6_information_theory.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_int_blueprint.md`

## Cleaning / derivation steps applied
- H_out excluded entirely — DS6 has no dismiss/close outcome variance (see StoP blueprint Part 0); would be a constant 0.
- H_emp uses K=10 QUANTILE bins computed per-participant (not DS5's fixed [0,1]-range bins — DS6's N_t is an unbounded count, 1–333/day, varying widely across participants). Effective K may be <10 for participants with fewer than 10 distinct daily counts.
- I_consec required a two-step bug fix during implementation (see `model_run_summary.md` "Bug found and fixed" section) — the correct marginal for the bridge identity is the transition edge list's `app_to` (destination) distribution, not Stage 1's `app_entropy` nor the `app_from` (source) marginal.

## Known limitations
- `H_app` and `H_app_marginal` are NOT the same quantity and will differ slightly — `H_app` is Stage 1's general app-diversity feature (all events); `H_app_marginal` is the transition-consistent destination marginal (excludes each participant's last event per period, which has no outgoing transition). Use `H_app` for general diversity reporting, `H_app_marginal` only for bridge-consistency checks against `H_trans`.
- H_SDE bridge equation not yet formalized in the conceptual paper (same gap DS5's InT notebook recorded).
- Entropy measures describe observed-distribution patterns, not directly observed psychological states.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/information_theory/participant_entropy_metrics.csv'))
```

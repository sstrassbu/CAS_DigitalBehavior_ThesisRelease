# participant_parameters_v2_mle.csv

**Produced by:** `notebooks/62_ds5_stop_v2_mle.ipynb` (DS5_02 A4a)
**Depends on:** `participant_parameters.csv` (nb43 MoM baseline); daily X_t from `ds5_behavioral_clean.csv`

## What this file contains

Per-participant MLE vs MoM sig_hat comparison for the DS5 constant-drift SDE (FLAG 2 check).
414 eligible participants (≥7 observation days).

**Unit of observation:** one row per eligible participant.

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier |
| `study_condition` | str | RCT arm (control / default / reintervention) |
| `n_days` | int | Number of observation days |
| `n_increments` | int | Number of daily increments (n_days - 1) |
| `x_mean` | float | Mean daily override rate |
| `mu_hat_mle` | float | MLE drift estimate (identical to MoM) |
| `sig_hat_mle` | float | MLE diffusion estimate (std with ddof=0) |
| `sig_hat_mom` | float | MoM diffusion estimate from nb43 (std with ddof=1) |
| `rel_deviation` | float | (MoM - MLE) / MoM — fractional downward bias of MLE |
| `beta_mle` | float | Inverse temperature 2/sig_hat_mle² |
| `chi_mle` | float | Susceptibility beta_mle * x_mean * (1 - x_mean) |

## Gate verdict (A4a)

- **Spearman ρ(σ_MLE, σ_MoM) = 0.999467** → PASS (threshold ≥ 0.95)
- **Median relative deviation = 0.012904** → PASS (threshold ≤ 0.05)
- **Overall verdict: NO MATERIAL CHANGE**

The deviation IS exactly the Bessel correction 1 - sqrt((N-1)/N) (verified to 1.8e-15 on
all 414 rows), and mu_hat_mle is bit-identical to the MoM mu_hat. This gate is therefore a
deterministic function of N and cannot fail for any data-driven reason: it verifies the
ddof arithmetic only, and is not evidence that DS5_01 findings are robust to estimator
choice. Estimator risks that would genuinely differ — unequal calendar spacing between
increments, and the [0,1] boundary of the daily proportion — are not tested here.

## Known limitations

- MLE sigma is biased downward by sqrt((N-1)/N) ≈ 0.9871 at the median N
- Boundary effects (X_t near 0 or 1) can bias both estimators and are NOT tested here. Section 5 of nb62 compared `rel_deviation` between near-boundary (|x_mean-0.5|>0.3, N=149) and interior (N=265) participants and found t=-2.348, p=0.0193, but `rel_deviation` is exactly 1-sqrt((N-1)/N), a pure function of `n_increments`, so that result only reflects near-boundary participants having longer windows (mean n_increments 35.2 vs 32.3, t=2.659, p=0.0082). A real boundary diagnostic would have to test sig_hat itself (or sig_hat relative to its binomial sampling floor) and the fraction of simulated Euler-Maruyama steps that hit the [0,1] clip.
- This notebook tests only the ddof correction; it does not test the OU alternative (A4b, optional)

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/stochastic_processes/participant_parameters_v2_mle.csv')
```

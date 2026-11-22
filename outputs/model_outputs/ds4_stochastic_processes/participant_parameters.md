# participant_parameters.csv

**Unit of observation:** one row per DS4 participant (all 1,039 `participant_id_canonical`
values from `ds4_behavioral_clean.csv`, including participants with zero or insufficient
intervention-outcome days — those rows carry `NaN` parameters, not imputed values).

**Model:** DS4 Stochastic Processes (StoP) — Ornstein-Uhlenbeck fit of the daily
intervention-override rate `X_t = n_opened / n_events` per participant, restricted to
`intervention_event_class == 'intervention_event'` rows with outcome in
`{opened, dismissed}`.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier, matches `ds4_behavioral_clean.csv` |
| `n_days_obs` | int | Count of distinct calendar days with ≥1 outcome-bearing `intervention_event` |
| `n_consec_pairs` | int | Count of consecutive-day (gap=1 day) `(X_t, X_{t+1})` pairs used for the AR(1) fit |
| `phi_hat` | float | AR(1) OLS slope; OU-valid only if `0 < phi_hat < 1`. `NaN` if `n_days_obs < 30` or `n_consec_pairs < 10` |
| `mu_hat_OU` | float | OU long-run mean (unconditional mean override rate). `NaN` unless `fit_valid` |
| `theta_hat_OU` | float | OU mean-reversion rate, per day (`-ln(phi_hat)`). `NaN` unless `fit_valid` |
| `sigma_hat_OU` | float | OU diffusion coefficient. `NaN` unless `fit_valid` |
| `tau_hat` | float | Relaxation time in days (`1/theta_hat_OU`). `NaN` unless `fit_valid` |
| `fit_valid` | bool | `True` only if `n_days_obs>=30`, `n_consec_pairs>=10`, and `0<phi_hat<1` |

---

## How this file was produced

- **Source:** `outputs/cleaned/ds4_behavioral_clean.csv`
- **Producing notebook:** `notebooks/53_ds4_stochastic_processes.ipynb`
- **Generator script:** `notebooks/make_53_ds4_stop.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`

## Method

For each participant, daily `X_t` is regressed on `X_{t+1}` (consecutive-day pairs only)
via OLS. This is the exact closed-form conditional MLE for a discrete-time OU process at
fixed Δt=1 day (see blueprint §5 for the derivation). Participants below the eligibility
thresholds, or whose fit is not mean-reverting (`phi_hat` outside (0,1)), get `NaN`
parameters — not imputed, not dropped from the row count.

## Actual run results (2026-08-06)

| Stage | N |
|---|---|
| Total participants | 1,039 |
| ≥1 intervention-outcome day | 1,036 |
| ≥30 daily observations (MIN_DAYS) | 786 |
| ...and ≥10 consecutive-day pairs | 785 |
| Valid mean-reverting fit (`fit_valid=True`) | 641 (81.7% of the 785 attempted) |

Parameter medians among the 641 valid fits: `mu_hat_OU`=0.715, `theta_hat_OU`=1.587/day,
`sigma_hat_OU`=0.290, `tau_hat`=0.63 days.

## Known limitations

- **Fast-θ interpretation is open, not resolved.** Median relaxation time is under a day.
  See `participant_parameters_weekly_sensitivity.csv` — the weekly-aggregated fit gives a
  meaningfully slower median relaxation time (0.91 weeks ≈ 6.4 days) and only a weak
  correlation (r=0.316, n=291) with the daily-scale θ̂ per participant. This divergence
  is reported, not resolved: it may reflect genuine multi-timescale dynamics, or that the
  daily ratio is a noisier signal of the same underlying process. Do not quote a single
  "the" relaxation time for DS4 without stating which timescale.
- **18.3% invalid-fit rate** among eligible participants — always report this alongside
  any eligible-N figure; do not conflate "eligible for fitting" with "has a valid fit."
- **No experimental condition** — DS4 is observational; results are within/cross-
  participant heterogeneity, never a friction effect.
- **Self-selected users** — the 786-eligible sample is not a random subsample of all
  1,039 participants; it is whoever kept using OneSec long enough to be observed.
- `X_t` is a behavioral override rate, not a latent psychological state.

## How to load

```python
import pandas as pd

params = pd.read_csv("outputs/model_outputs/ds4_stochastic_processes/participant_parameters.csv")
valid = params[params["fit_valid"]]  # 641 rows with real OU parameters
```

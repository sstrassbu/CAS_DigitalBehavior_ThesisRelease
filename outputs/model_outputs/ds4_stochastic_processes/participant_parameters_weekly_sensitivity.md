# participant_parameters_weekly_sensitivity.csv

**Unit of observation:** one row per DS4 participant (all 1,039), same as
`participant_parameters.csv`, but the OU fit uses **ISO-week-aggregated** `X_t`
(`sum(n_opened)/sum(n_events)` per participant-week) instead of daily `X_t`.

**Purpose:** a robustness/sensitivity check on `participant_parameters.csv`'s headline
finding — daily-scale relaxation time is under a day. This file tests whether that
result holds at a coarser aggregation timescale.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `n_weeks_obs` | int | Count of distinct ISO weeks with ≥1 outcome-bearing `intervention_event` |
| `n_consec_week_pairs` | int | Count of consecutive-week `(X_t, X_{t+1})` pairs used for the fit |
| `phi_hat_weekly` | float | AR(1) OLS slope at weekly resolution. `NaN` if `n_weeks_obs<5` or `n_consec_week_pairs<10` |
| `theta_hat_OU_weekly` | float | OU mean-reversion rate, **per week** (not per day — do not compare directly to `theta_hat_OU` without unit conversion). `NaN` unless `fit_valid_weekly` |
| `tau_hat_weekly` | float | Relaxation time in **weeks**. `NaN` unless `fit_valid_weekly` |
| `fit_valid_weekly` | bool | `True` only if thresholds met and `0<phi_hat_weekly<1` |

---

## How this file was produced

- **Source:** `outputs/cleaned/ds4_behavioral_clean.csv` (same source as the daily fit)
- **Producing notebook:** `notebooks/53_ds4_stochastic_processes.ipynb`, cell 14
- **Generator script:** `notebooks/make_53_ds4_stop.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`

## Method

Same AR(1)-OLS closed-form conditional MLE as the daily fit, applied to weeks instead of
days (`timestamp_utc.dt.to_period("W")`). The day-count threshold is scaled down
(`MIN_WEEKS=5` instead of `n_days_obs>=30`), but **`MIN_PAIRS=10` was reused unchanged, so
`MIN_WEEKS=5` never binds**: since `n_consec_week_pairs <= n_weeks_obs - 1`, the effective
gate is **≥11 observed weeks with ≥10 consecutive-week pairs** (verified: min `n_weeks_obs`
among valid fits = 11). 836 participants pass the nominal `n_weeks_obs>=5`; only 456 pass
the real gate. The weekly-eligible group is therefore the longest-tenured, most-consistent
subset — a plausible alternative contributor to the slower weekly τ̂.

## Actual run results (2026-08-06)

- 330 participants produced a valid weekly mean-reverting fit.
- Median `theta_hat_OU_weekly` = 1.103 per week; median `tau_hat_weekly` = 0.91 weeks
  (≈6.3 days) — **substantially slower** than the daily-scale median (τ̂=0.63 days). Those
  two medians are over different participant sets (330 weekly vs 641 daily). Like-for-like,
  on the 291 participants with **both** valid fits: median daily τ̂ = **0.66 days** vs median
  weekly τ̂ = **0.99 weeks = 6.90 days** — a 10.5× within-participant divergence.
- Among the 291 participants with **both** a valid daily and valid weekly fit, the
  correlation between daily `theta_hat_OU` and weekly `theta_hat_OU_weekly` is **r=0.316**
  — weak-to-moderate, not the near-1 correlation you'd expect if both were just
  measuring the same fast process at different resolutions.

## Known limitations

- **This divergence between daily and weekly timescales is reported, not explained.**
  Two open readings (see `participant_parameters.md`): genuine multi-timescale dynamics,
  or the daily ratio being a noisier proxy of the same slower underlying process. This
  file's job is to surface the divergence for downstream models (InT/DyS/StM) to take
  into account, not to pick a winner.
- Smaller eligible N than the daily fit (fewer weeks than days per participant over the
  same window) — treat weekly-scale conclusions as more uncertain, not as a strict
  replacement for the daily-scale result.
- Same behavioral-proxy and no-condition caveats as `participant_parameters.csv` apply.

## How to load

```python
import pandas as pd

weekly = pd.read_csv(
    "outputs/model_outputs/ds4_stochastic_processes/participant_parameters_weekly_sensitivity.csv"
)
valid_weekly = weekly[weekly["fit_valid_weekly"]]  # 330 rows
```

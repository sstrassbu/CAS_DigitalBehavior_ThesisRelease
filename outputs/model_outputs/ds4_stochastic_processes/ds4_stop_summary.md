# ds4_stop_summary.csv

**Unit of observation:** one row — sample-level summary of the DS4 StoP model run.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n_total` | int | Total DS4 participants (1,039) |
| `n_any_day` | int | Participants with ≥1 intervention-outcome day |
| `n_min_days` | int | Participants meeting MIN_DAYS=30 |
| `n_min_pairs` | int | Of those, participants retaining ≥10 consecutive-day pairs |
| `n_valid_fit` | int | Participants with a valid mean-reverting OU fit |
| `pct_valid_of_attempted` | float | `n_valid_fit / n_min_pairs` |
| `median_mu_hat_OU` | float | Median OU long-run mean among valid fits |
| `median_theta_hat_OU` | float | Median OU mean-reversion rate (/day) among valid fits |
| `median_sigma_hat_OU` | float | Median OU diffusion among valid fits |
| `median_tau_hat` | float | Median relaxation time (days) among valid fits |

---

## How this file was produced

- **Producing notebook:** `notebooks/53_ds4_stochastic_processes.ipynb`, cell 12
- **Generator script:** `notebooks/make_53_ds4_stop.py`
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`

Computed directly from `participant_parameters.csv` (see its companion `.md` for the
full per-participant schema and the eligibility funnel this file summarizes).

## Actual run results (2026-08-06)

```
n_total                 1039
n_any_day               1036
n_min_days                786
n_min_pairs                785
n_valid_fit                641
pct_valid_of_attempted   0.8166
median_mu_hat_OU          0.7151
median_theta_hat_OU       1.5867
median_sigma_hat_OU       0.2900
median_tau_hat            0.6302
```

## Known limitations

Same as `participant_parameters.md` — in particular, `median_tau_hat` describes only the
daily-aggregation timescale; see `participant_parameters_weekly_sensitivity.md` for the
weekly comparison before treating this as "the" DS4 relaxation time.

## How to load

```python
import pandas as pd

summary = pd.read_csv("outputs/model_outputs/ds4_stochastic_processes/ds4_stop_summary.csv")
```

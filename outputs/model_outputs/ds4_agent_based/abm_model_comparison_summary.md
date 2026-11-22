# abm_model_comparison_summary.csv

**Unit of observation:** one row per model (`real`/`model1_pure_OU`/`model2_weekly_periodic`)
— aggregate daily-vs-weekly divergence statistics.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `model` | string | `real`, `model1_pure_OU`, or `model2_weekly_periodic` |
| `n` | int | Participants/agents with both a valid daily and valid weekly fit |
| `corr` | float | Correlation between daily-fitted θ̂ and weekly-fitted θ̂ |
| `median_tau_daily`, `median_tau_weekly` | float | Median relaxation times (days/weeks respectively) |
| `daily_weekly_ratio` | float | `median_tau_weekly / median_tau_daily` |

---

## How this file was produced

- **Producing notebook:** `notebooks/57_ds4_agent_based.ipynb`, cell 8
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_abm_blueprint.md`

## Actual run results (2026-08-07)

```
model                    n     corr  median_tau_daily  median_tau_weekly  ratio
real                   291   0.3164             0.660              0.985  1.494
model1_pure_OU         113   0.0194             0.624              0.521  0.835
model2_weekly_periodic 111  -0.0000             0.767              0.530  0.691
```

See `participant_abm_simulation_results.md` for the full interpretation — this is a
genuine negative result: neither simulated model reproduces the real divergence
direction or magnitude.

## How to load

```python
import pandas as pd

comparison = pd.read_csv("outputs/model_outputs/ds4_agent_based/abm_model_comparison_summary.csv")
```

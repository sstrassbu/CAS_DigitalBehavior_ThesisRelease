# ds4_stm_summary.csv

**Unit of observation:** one row — sample-level summary of the DS4 StM model run.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n_total` | int | Total DS4 participants (1,039) |
| `n_valid` | int | Participants with real StM values (641) |
| `median_beta_OU`, `median_T_OU`, `median_chi_OU`, `median_tau_hat` | float | Sample medians among valid fits |
| `r_HStM_Hemp` | float | Bridge check — identical to InT's `r(H_emp,H_SDE)` |
| `r_activity_persistence_beta` | float | Correlation between Stage 1's `activity_persistence` and `beta_OU` — genuine null (0.006) |

---

## How this file was produced

- **Producing notebook:** `notebooks/51_ds4_statistical_mechanics.ipynb`, cell 20
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stm_blueprint.md`

## Actual run results (2026-08-06)

```
n_total                      1039.000000
n_valid                       641.000000
median_beta_OU                 36.547362
median_T_OU                     0.027362
median_chi_OU                    6.848730
median_tau_hat                   0.630225
r_HStM_Hemp                      0.720580
r_activity_persistence_beta      0.005809
```

## Known limitations

Same as `participant_ds4_stm_parameters.md`.

## How to load

```python
import pandas as pd

summary = pd.read_csv("outputs/model_outputs/ds4_statistical_mechanics/ds4_stm_summary.csv")
```

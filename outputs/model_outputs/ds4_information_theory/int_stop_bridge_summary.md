# int_stop_bridge_summary.csv

**Unit of observation:** one row — sample-level bridge/redundancy checks between DS4 InT
and DS4 StoP.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `r_H_emp_H_SDE` | float | Correlation between `H_emp` (empirical binned entropy) and `H_SDE` (exact OU stationary entropy), among the 641 valid StoP fits |
| `r_H_out_intervention_mu_hat_OU` | float | Correlation between `H_out_intervention` (outcome entropy) and StoP's `mu_hat_OU` |
| `n_valid` | int | Sample size for both correlations (641) |

---

## How this file was produced

- **Producing notebook:** `notebooks/52_ds4_information_theory.ipynb`, cell 16
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_int_blueprint.md`

## Actual run results (2026-08-06)

```
r_H_emp_H_SDE                     0.7206
r_H_out_intervention_mu_hat_OU   -0.6313
n_valid                             641
```

## Interpretation

- **H_emp vs H_SDE (r=0.721):** a real, positive bridge — the empirical, model-free
  entropy of daily override rates broadly agrees with the exact OU-model-implied
  entropy. Comparable magnitude to DS5's own InT-StoP bridge (r=0.650), though the two
  are not directly comparable (different underlying SDE, DS4's is exact).
- **H_out_intervention vs mu_hat_OU (r=−0.631):** moderate-strong, expected in sign
  (binary entropy falls as the opened-proportion moves away from 0.5; DS4's median
  `mu_hat_OU`=0.715 sits well above 0.5) — but not so strong that either quantity is
  redundant with the other.

## Known limitations

Same daily-timescale caveat as `participant_entropy_metrics.md` applies to
`r_H_emp_H_SDE` — both inputs are daily-scale quantities.

## How to load

```python
import pandas as pd

bridge = pd.read_csv("outputs/model_outputs/ds4_information_theory/int_stop_bridge_summary.csv")
```

# dys_stop_int_bridge_summary.csv

**Unit of observation:** one row — sample-level summary of the DS4 DyS model run.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n_valid` | int | Participants with a valid StoP fit (641) |
| `n_high_control` | int | Participants in the `high_control` regime |
| `n_low_control` | int | Participants in the `low_control` regime |
| `theta_median` | float | The `theta_hat_OU` median used as the regime-split threshold |
| `corr_xmeanraw_muhatOU` | float | Fixed-point internal-consistency correlation (arithmetic identity — not a fit test; a shuffled null scores 0.9979) |
| `mean_fixed_point_deviation` | float | Mean `\|x_mean_raw - mu_hat_OU\|` |
| `corr_theta_Hemp` | float | DyS-InT bridge correlation |
| `n_behaviorally_deterministic` | int | Count flagged `behaviorally_deterministic=True` |

---

## How this file was produced

- **Producing notebook:** `notebooks/55_ds4_dynamical_systems.ipynb`, cell 12
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_dys_blueprint.md`

## Actual run results (2026-08-06)

```
n_valid                          641
n_high_control                   321
n_low_control                    320
theta_median                   1.5867
corr_xmeanraw_muhatOU          0.9925
mean_fixed_point_deviation     0.0108
corr_theta_Hemp               -0.1762
n_behaviorally_deterministic     173
```

## Known limitations

Same as `participant_dynamics_parameters.md` — in particular, `corr_theta_Hemp` is a
real but weak bridge; do not overstate it as strong cross-model validation.

## How to load

```python
import pandas as pd

bridge = pd.read_csv("outputs/model_outputs/ds4_dynamical_systems/dys_stop_int_bridge_summary.csv")
```

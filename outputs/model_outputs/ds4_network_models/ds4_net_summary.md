# ds4_net_summary.csv

**Unit of observation:** one row — sample-level summary of the DS4 NeT model run.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n_total` | int | Total DS4 participants (1,039) |
| `n_eligible` | int | Participants with ≥50 attempt-to-attempt transitions (950) |
| `median_rho_self`, `median_H_trans`, `median_HHI_net`, `median_H_pi` | float | Sample medians among eligible participants |
| `n_stationary_eligible` | int | Participants with a computed stationary distribution (950 — same as `n_eligible` here) |
| `r_HHInet_appherfindahl` | float | Redundancy check vs Stage 1's `app_herfindahl` |
| `n_Iconsec_negative` | int | Negative `I_consec` count **after** the marginal fix (0) |
| `n_Iconsec_negative_naive_buggy_version` | int | What it would have been with the bug (138) — kept for the record |

---

## How this file was produced

- **Producing notebook:** `notebooks/54_ds4_network_models.ipynb`, cell 13
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_net_blueprint.md`

## Actual run results (2026-08-06)

```
n_total                                  1039
n_eligible                                950
median_rho_self                        0.6795
median_H_trans                         0.9545
median_HHI_net                         0.5091
n_stationary_eligible                     950
median_H_pi                            4.3329
r_HHInet_appherfindahl                 0.9688
n_Iconsec_negative                          0
n_Iconsec_negative_naive_buggy_version    138
```

## Known limitations

Same as `participant_network_metrics.md`.

## How to load

```python
import pandas as pd

summary = pd.read_csv("outputs/model_outputs/ds4_network_models/ds4_net_summary.csv")
```

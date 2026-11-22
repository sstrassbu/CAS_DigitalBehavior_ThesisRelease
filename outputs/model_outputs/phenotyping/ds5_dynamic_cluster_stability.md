# ds5_dynamic_cluster_stability.csv

**Unit of observation:** One row per (analysis level × k tested) combination
**Produced by:** `notebooks/106_ds5_dynamic_stochastic_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path D
**Date:** 2026-04-20

---

## What this file contains

K-selection metrics and Jaccard stability scores for all Path D analyses:
D1 full-sample [sig_hat, H_emp, chi_behav], D2 full-sample [sig_hat, H_emp, mu_hat],
D3 sensitivity [sig_hat, H_emp, H_hour] (if variance sufficient), and D1 within-reintervention.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `analysis` | str | Analysis level: D1_full_sample, D2_full_sample, D3_sensitivity, D1_reintervention |
| `N` | int | Sample size for that analysis level |
| `k_tested` | int/None | k value tested; None for D3 if skipped |
| `sil` | float/None | Silhouette score; None if rejected |
| `min_cell` | int/None | Minimum cluster cell size |
| `jaccard` | float/None | Bootstrap Jaccard (100 bootstraps, 80% sample) |
| `flag` | str | STABLE (J≥0.75), MARGINAL (0.60≤J<0.75), UNSTABLE (J<0.60), REJECTED_MINCELL, SKIPPED_LOW_VARIANCE |
| `selected` | bool | Whether this k was selected as the best feasible solution |

---

## Load snippet

```python
import pandas as pd
stability = pd.read_csv('outputs/model_outputs/phenotyping/ds5_dynamic_cluster_stability.csv')
print(stability[stability['selected'] == True][['analysis','N','k_tested','sil','jaccard','flag']])
```

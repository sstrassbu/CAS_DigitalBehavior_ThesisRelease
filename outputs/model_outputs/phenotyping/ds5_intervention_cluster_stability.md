# ds5_intervention_cluster_stability.csv

**Unit of observation:** One row per (analysis level × k tested) combination  
**Produced by:** `105_ds5_intervention_sensitive_phenotype.ipynb`  
**Stage:** Stage 4, Step 2 — Path B  
**Date:** 2026-04-20

---

## What this file contains

K-selection metrics and Jaccard stability scores for all Path B analyses:
full-sample, within-reintervention, Profile B within reintervention, within-control,
and default (descriptive only, no k attempted).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `analysis` | str | Analysis level: `full_sample`, `reintervention`, `profile_B_reintervention`, `control`, `default` |
| `N` | int | Sample size for that analysis level |
| `k_tested` | int/None | k value tested; None for default (no clustering) |
| `sil` | float/None | Silhouette score; None if rejected |
| `min_cell` | int/None | Minimum cluster cell size; None if not applicable |
| `jaccard` | float/None | Bootstrap Jaccard (100 bootstraps, 80% sample); None if rejected |
| `flag` | str | `STABLE` (J≥0.75), `MARGINAL` (0.60≤J<0.75), `UNSTABLE` (J<0.60), `REJECTED_MINCELL` (min_cell<30), `DESCRIPTIVE_ONLY` |
| `selected` | bool | Whether this k was selected as the best feasible solution |

---

## Summary of selected solutions

| Analysis | N | k selected | Jaccard | Flag |
|---|---|---|---|---|
| full_sample | 414 | 3 | 0.940 | STABLE |
| reintervention | 135 | 2 | 0.912 | STABLE |
| profile_B_reintervention | 99 | 2 | 0.837 | STABLE |
| control | 137 | 3 | 0.808 | STABLE |
| default | 142 | — | — | DESCRIPTIVE_ONLY |

---

## Load snippet

```python
import pandas as pd
stability = pd.read_csv('outputs/model_outputs/phenotyping/ds5_intervention_cluster_stability.csv')
print(stability[stability['selected'] == True][['analysis','N','k_tested','sil','jaccard','flag']])
```

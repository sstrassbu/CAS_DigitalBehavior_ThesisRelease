# ds5_cluster_profiles.csv — Documentation

**Produced by:** `notebooks/100_phenotype_exploration.ipynb` (Stage 4, Step 2)  
**Date:** 2026-04-18  
**Unit of observation:** One row per behavioral feature (18 rows), with per-cluster statistics as columns

---

## What this file contains

Per-cluster summary statistics (mean, median, standard deviation, N) for all behavioral
features available in the Phase 1 analysis population. This is the primary profile
table for describing phenotypic differences between the identified clusters.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `feature` | str | Feature name (matches ds5_phenotype_feature_matrix.csv columns) |
| `Profile A_mean` | float | Mean of feature in Profile A (N=125) |
| `Profile A_median` | float | Median of feature in Profile A |
| `Profile A_std` | float | Standard deviation of feature in Profile A |
| `Profile A_n` | int | N with non-NaN value for this feature in Profile A |
| `Profile B_mean` | float | Mean of feature in Profile B (N=289) |
| `Profile B_median` | float | Median of feature in Profile B |
| `Profile B_std` | float | Standard deviation of feature in Profile B |
| `Profile B_n` | int | N with non-NaN value for this feature in Profile B |

---

## Key profile comparison (core features)

| Feature | Profile A | Profile B | Interpretation |
|---|---|---|---|
| sig_hat | 0.191 | 0.213 | Modest difference; both profiles have similar behavioral variability |
| H_emp | 1.964 | 2.064 | Modest difference; behavioral predictability similar across profiles |
| x_mean | 0.669 | 0.705 | Modest difference; both profiles have moderate override tendency |
| **HHI_net** | **0.545** | **0.978** | **Large difference; the primary distinguishing feature** |
| **rho_self** | **0.761** | **0.992** | **Large difference; the primary distinguishing feature** |

The primary phenotypic split is a **network behavioral structure** difference:
- **Profile A** (N=125, 30%): Distributed app-use network — participants use multiple apps
  during friction events with relatively balanced transition flows.
- **Profile B** (N=289, 70%): Hub-dominated, self-repeating network — participants use
  one dominant app almost exclusively and return to the same app after each friction event.

---

## Source file

Features from all 5 completed DS5 Step 1 model outputs. See `ds5_phenotype_feature_matrix.md`
for full column definitions.

---

## Known limitations

- Profile differences on core features other than HHI_net and rho_self are modest and may
  not be robust across alternative clustering solutions.
- N within each profile and feature may differ because secondary features have their own
  missingness within the Phase 1 population.

---

## How to load

```python
import pandas as pd
from pathlib import Path

profiles = pd.read_csv(
    Path('outputs/model_outputs/phenotyping/ds5_cluster_profiles.csv')
)
print(profiles[['feature', 'Profile A_mean', 'Profile B_mean']].to_string())
```

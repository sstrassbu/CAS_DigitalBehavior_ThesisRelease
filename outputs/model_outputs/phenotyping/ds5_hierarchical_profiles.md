# ds5_hierarchical_profiles.csv — Column Reference

**Produced by:** `103_ds5_hierarchical_phenotype.ipynb`  
**Date:** 2026-04-19  
**Unit of observation:** One row per Path F cell (4 rows)  

## What this file contains

Per-cell descriptive statistics (mean, median, std) for behavioral features (sig_hat, H_emp, x_mean, H_hour, mu_hat) and NeT overlay features (HHI_net, rho_self, H_trans, H_app). All values in raw (unscaled) units.

## Column reference

| Column | Description |
|---|---|
| `cell` | Path F cell label (e.g., B_behav1, A_behav2) |
| `N` | Participants in cell |
| `<feature>_mean` | Mean of feature in raw units |
| `<feature>_median` | Median of feature in raw units |
| `<feature>_std` | Standard deviation of feature in raw units |

## Notes

- All features reported in raw (unscaled) units for interpretability.
- Stage 2 clustering used within-group StandardScaler internally; profiles are in original scale.
- mu_hat and sigma_mu_ratio are near-zero/NaN for many DS5 participants; interpret with caution.

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/phenotyping/ds5_hierarchical_profiles.csv')
```

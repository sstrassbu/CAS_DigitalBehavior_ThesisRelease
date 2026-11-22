# ds5_dynamic_cluster_profiles.csv

**Unit of observation:** One row per full-sample Path D cluster (D1 set)
**Total rows:** 2
**Produced by:** `notebooks/106_ds5_dynamic_stochastic_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path D
**Date:** 2026-04-20

---

## What this file contains

Mean and standard deviation of all relevant features per full-sample Path D (D1) cluster.
Primary features: [sig_hat, H_emp, chi_behav]. Overlays: mu_hat, x_mean, F_behav, H_SDE, beta_behav, H_hour.

---

## Column reference

Columns follow the pattern `{feature}_mean` / `{feature}_std` for each feature plus `N`.

Primary clustering features (D1): sig_hat, H_emp, chi_behav
Overlay features: mu_hat, x_mean, F_behav, H_SDE, beta_behav, H_hour

---

## Load snippet

```python
import pandas as pd
profiles = pd.read_csv('outputs/model_outputs/phenotyping/ds5_dynamic_cluster_profiles.csv', index_col=0)
print(profiles[['N', 'sig_hat_mean', 'H_emp_mean', 'chi_behav_mean', 'mu_hat_mean', 'x_mean_mean']])
```

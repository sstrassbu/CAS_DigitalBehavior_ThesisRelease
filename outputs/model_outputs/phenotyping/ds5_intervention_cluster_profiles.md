# ds5_intervention_cluster_profiles.csv

**Unit of observation:** One row per full-sample Path B cluster (k=3)  
**Total rows:** 3  
**Produced by:** `105_ds5_intervention_sensitive_phenotype.ipynb`  
**Stage:** Stage 4, Step 2 — Path B  
**Date:** 2026-04-20

**Generation:** hand-written. Notebook 105 writes only the three Path B CSVs and the figures; it does
NOT generate this document. Re-running notebook 105 will refresh the CSVs and figures and leave this
file stale — update it by hand after any re-run.

---

## What this file contains

Mean and standard deviation of all relevant features per full-sample Path B cluster.
Features include primary clustering features, overlay features, and N per cluster.

---

## Column reference

Columns follow the pattern `{feature}_mean` / `{feature}_std` for:
- `H_out_resid`: condition-residualized friction outcome entropy (primary Path B axis)
- `sig_hat`: behavioral noise / stochastic process diffusion parameter
- `H_emp`: behavioral outcome entropy
- `x_mean`: mean override rate (overlay — not used in clustering)
- `chi_behav`: friction susceptibility (overlay)
- `mu_hat`: behavioral drift (overlay)
- `N`: number of participants in cluster

---

## Cluster interpretation guide

| Cluster | Interpretation | Condition distribution |
|---|---|---|
| B_fr1 (N=148) | Low friction-response diversity; high override; moderate susceptibility. Low-noise complier. | 54.7% control, 12.2% default, 33.1% reintervention |
| B_fr2 (N=198) | Near-zero residualized diversity; high noise; high entropy; low susceptibility. Noisy non-override type. | 16.2% control, 53.5% default, 30.3% reintervention |
| B_fr3 (N=68) | High friction-response diversity; low noise; moderate entropy; low override; very high susceptibility. Diverse responder. | 35.3% control, 26.5% default, 38.2% reintervention |

---

## Limitations / notes

- The pooled full-sample solution is condition-confounded: only `H_out_resid` is condition-residualized;
  `sig_hat` and `H_emp` differ by 0.66 and 1.19 pooled SD between control and default. B_fr2 (N=198)
  contains 74.6% of all default participants (chi2=82.9, p=4.2e-17), so its "noisy non-override"
  description is partly a treatment effect rather than a person-level trait.

---

## Load snippet

```python
import pandas as pd
profiles = pd.read_csv('outputs/model_outputs/phenotyping/ds5_intervention_cluster_profiles.csv', index_col=0)
print(profiles[['H_out_resid_mean', 'sig_hat_mean', 'H_emp_mean', 'x_mean_mean', 'chi_behav_mean', 'N']])
```

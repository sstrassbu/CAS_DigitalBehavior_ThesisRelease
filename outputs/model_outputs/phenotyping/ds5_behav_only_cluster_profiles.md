# ds5_behav_only_cluster_profiles.csv — Output Documentation

**Produced by:** `notebooks/102_ds5_behavior_only_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path A (Behavior-Only Phenotyping)
**Date:** 2026-04-19

---

## What this file contains

Per-cluster feature profiles (mean, median, std) for all behavior-only clusters found in
Path A. Rows represent clusters; columns represent feature statistics.

**Unit of observation:** One cluster

---

## Column reference (abbreviated)

| Column pattern | Description |
|---|---|
| `cluster` | Cluster label (C1, C2, ...) |
| `N` | Number of participants in cluster |
| `{feature}_mean` | Mean of feature across cluster participants |
| `{feature}_median` | Median of feature across cluster participants |
| `{feature}_std` | Standard deviation of feature across cluster participants |

Features included: sig_hat, H_emp, x_mean, H_hour, mu_hat, sigma_mu_ratio,
H_out_resid, chi_behav, HHI_net (overlay), rho_self (overlay), H_trans (overlay),
H_app (overlay)

---

## Cluster summary (key features)

| Cluster | N | sig_hat | H_emp | x_mean | H_hour | HHI_net (overlay) | rho_self (overlay) |
|---|---|---|---|---|---|---|---|
| C1 | 62 | 0.1207 | 1.7340 | 0.3576 | 4.1069 | 0.7812 | 0.9222 |
| C2 | 152 | 0.1434 | 1.6036 | 0.8590 | 4.0867 | 0.8580 | 0.9158 |
| C3 | 200 | 0.2807 | 2.4541 | 0.6733 | 3.9911 | 0.8593 | 0.9279 |

---

## Interpretation

Clusters ordered by sig_hat ascending (C1 = lowest noise / most stable behavior).
NeT features (HHI_net, rho_self) are post-hoc overlays — NOT used in clustering.
ARI between Path A clusters and Phase 1 profile = 0.020 (see assignments doc).

---

## How to load

```python
import pandas as pd
from pathlib import Path

BASE = Path('outputs/model_outputs/phenotyping')
profiles = pd.read_csv(BASE / 'ds5_behav_only_cluster_profiles.csv')
```

# ds5_net_subcluster_profiles.csv — Output Documentation

**Produced by:** `notebooks/101_ds5_network_subphenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path C (Network-Structural Sub-Phenotyping)
**Date:** 2026-04-19

---

## What this file contains

Per-sub-cluster feature profiles (mean, median, std) for all sub-clusters found in
Path C. Rows represent sub-clusters; columns represent feature statistics.

**Unit of observation:** One sub-cluster (within Profile A or Profile B)

---

## Column reference (abbreviated)

| Column pattern | Description |
|---|---|
| `source_population` | Profile A or Profile B |
| `subprofile` | Sub-cluster label (B1, B2, A1, A2) |
| `N` | Number of participants in sub-cluster |
| `{feature}_mean` | Mean of feature across sub-cluster participants |
| `{feature}_median` | Median of feature across sub-cluster participants |
| `{feature}_std` | Standard deviation of feature across sub-cluster participants |

Features included: HHI_net, rho_self, H_trans, H_app, H_pi, I_consec, top1_share_net,
sig_hat, H_emp, x_mean, H_out, chi_behav, H_hour, mu_hat

---

## Sub-cluster summary (key features)

| Sub-profile | Source | N | HHI_net | rho_self | H_trans | H_app | sig_hat | H_emp | x_mean |
|---|---|---|---|---|---|---|---|---|---|
| B1 | Profile B | 260 | 0.9953 | 0.9977 | 0.0104 | 0.0183 | 0.2113 | 2.0419 | 0.7134 |
| B2 | Profile B | 29 | 0.8210 | 0.9462 | 0.2303 | 0.4754 | 0.2296 | 2.2650 | 0.6316 |
| A1 | Profile A | 85 | 0.5993 | 0.8080 | 0.6485 | 0.8781 | 0.1889 | 1.9680 | 0.6775 |
| A2 | Profile A | 40 | 0.4293 | 0.6614 | 1.0870 | 1.4160 | 0.1942 | 1.9557 | 0.6501 |

---

## Interpretation

**B1** — Single/near-single-app locked (N=260, 89.9% of Profile B):
HHI and rho_self at ceiling; H_trans and H_app near zero. Every friction event targets
the same app. Behavioral variability (sig_hat) and override rate (x_mean) are similar
to other sub-profiles — the network monotony is not accompanied by systematically
lower noise or higher compliance.

**B2** — Multi-app hub-anchored (N=29, 10.1% of Profile B):
Still strongly hub-concentrated (HHI=0.82) but with genuine inter-app transition
diversity (H_trans=0.23, H_app=0.48). Slightly lower x_mean (0.632 vs 0.713 for B1)
suggests marginally lower override tendency, but the groups were not defined by x_mean
and the difference should not be over-interpreted.

**A1** — Moderately distributed (N=85, 68.0% of Profile A):
Multiple apps share friction-event flow; one app still somewhat dominant (HHI=0.60).
H_trans=0.65 indicates real but moderate transition diversity.

**A2** — Highly distributed (N=40, 32.0% of Profile A):
Friction events spread across many apps (HHI=0.43, H_app=1.42). No clearly dominant
hub. H_trans=1.09 (approaching 1 bit) indicates near-uniform transitions.

**Behavioral features (sig_hat, H_emp, x_mean) show only small differences across the
four sub-profiles, none of which survives correction for the three tests.** A four-group
Kruskal-Wallis across B1/B2/A1/A2 gives x_mean H=8.884 p=0.031, sig_hat H=8.181 p=0.042,
H_emp H=7.436 p=0.059 — all non-significant at a Bonferroni-corrected α=0.0167. Within
Profile B alone, x_mean (p=0.014) and H_emp (p=0.042) are nominally significant
uncorrected; within Profile A all three are clearly non-significant (p=0.91/0.70/0.59).
The sub-structure is therefore predominantly — but not demonstrably *entirely* —
network-structural rather than behavioral-dynamic.

---

## How to load

```python
import pandas as pd
from pathlib import Path

BASE = Path('outputs/model_outputs/phenotyping')
profiles = pd.read_csv(BASE / 'ds5_net_subcluster_profiles.csv')

# Filter to Profile B
b_profiles = profiles[profiles['source_population'] == 'Profile B']
```

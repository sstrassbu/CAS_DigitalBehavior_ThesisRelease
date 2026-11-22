# ds5_cluster_assignments.csv — Documentation

**Produced by:** `notebooks/100_phenotype_exploration.ipynb` (Stage 4, Step 2)  
**Date:** 2026-04-18  
**Unit of observation:** One row per participant in the Phase 1 analysis population (414 rows)

---

## What this file contains

Cluster assignments for each participant from the DS5 Phase 1 (5-feature core clustering)
and Phase 2 (9-feature extended sensitivity clustering). Phase 2 assignments are available
for the same 414 participants (H_out_resid was successfully computed for all of them).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant ID |
| `study_condition` | str | Experimental condition (control / default / reintervention) |
| `cluster_p1` | int | Phase 1 cluster index (0-indexed; 0=Profile A, 1=Profile B) |
| `profile_p1` | str | Phase 1 cluster label ("Profile A" / "Profile B") |
| `cluster_p2` | float | Phase 2 cluster index (0-indexed; NaN if Phase 2 skipped) |

---

## Phase 1 clustering solution

**Algorithm:** K-means (k-means++, 10 seeds, RANDOM_STATE=42)  
**Features:** sig_hat, H_emp, x_mean, HHI_net, rho_self (standardized)  
**Selected k:** 2  
**Selection criterion:** Best silhouette score among k≥2 solutions with min_cluster_size≥40  

| Profile | N | Silhouette | x_mean (mean) | sig_hat (mean) | HHI_net (mean) | rho_self (mean) |
|---|---|---|---|---|---|---|
| Profile A | 125 | — | 0.669 | 0.191 | 0.545 | 0.761 |
| Profile B | 289 | — | 0.705 | 0.213 | 0.978 | 0.992 |
| **Overall** | **414** | **0.373** | — | — | — | — |

**Profiles are labeled by ascending x_mean (A = lowest mean override rate).**

### Key finding
The dominant split is **not** on sig_hat or x_mean (which differ only modestly between
profiles), but almost entirely on **HHI_net and rho_self** (the network structure features):
- Profile A: HHI_net=0.545, rho_self=0.761 — distributed app-use network
- Profile B: HHI_net=0.978, rho_self=0.992 — completely hub-dominated, self-repeating network

This means the primary phenotypic distinction in DS5 is a **network behavioral structure**
difference, not a variability or override-level difference.

### Robustness
- Bootstrap Jaccard stability (100 bootstraps, 80% sample): 0.995 ± 0.006 → **STABLE**
- ARI vs 4-feature solution (without H_emp): 0.990 → robust to feature choice
- Condition distribution per cluster: χ²=1.22, p=0.545 → clusters NOT aligned with condition

## Phase 2 clustering solution

**Features:** Phase 1 core + H_hour + H_app + chi_behav + H_out_resid (9 features total)  
**Selected k:** 3  
**ARI vs Phase 1:** 0.723 → high agreement; Phase 1 structure preserved

The Phase 2 partition is cross-cutting, not a nested refinement of Phase 1. Crosstab of
`profile_p1` × `cluster_p2`:

| | Phase 2 cluster 0 | Phase 2 cluster 1 | Phase 2 cluster 2 |
|---|---|---|---|
| Profile A (N=125) | 26 | 0 | 99 |
| Profile B (N=289) | 32 | 256 | 1 |

Phase 2 cluster 0 (N=58) draws from both Phase 1 profiles (26 A + 32 B), so the secondary
features (temporal spread, app breadth, susceptibility, residualized outcome entropy) move
~14% of the sample across the Phase 1 boundary rather than subdividing within it. That is why
ARI falls to 0.723 rather than staying near 1.0.

---

## Known limitations

- Labels "Profile A" and "Profile B" are descriptive shorthand for cluster membership.
  They are not diagnostic categories or stable personality types.
- DS5 observation windows are 7–45 days. Cluster assignments may not reflect long-run
  behavioral traits.
- Cross-dataset replication (DS4, DS6) is required before claiming stable phenotypes.

---

## How to load

```python
import pandas as pd
from pathlib import Path

df = pd.read_csv(
    Path('outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv')
)
print(df['profile_p1'].value_counts())
```

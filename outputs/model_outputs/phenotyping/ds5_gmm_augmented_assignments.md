# ds5_gmm_augmented_assignments.csv

**Produced by:** `notebooks/63_ds5_phenotype_v2.ipynb` (DS5_02 Phase B, Track 2)  
**Depends on:** `ds5_phenotype_feature_matrix.csv`, `ds5_cluster_assignments.csv`, `participant_dynamics_v2.csv`

## What this file contains

Per-participant GMM cluster assignments using the augmented feature set: original Phase 1 core
features + `has_stable_fp` (binary, full coverage 414/414). This tests whether the v2 DyS attractor
indicator adds discriminating information beyond the original 5 features.

**Unit of observation:** one row per participant (414 total).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier |
| `profile_gmm_augmented` | str | GMM label with augmented features (Profile A / Profile B) |
| `profile_p1` | str | DS5_01 k-means label (Profile A / Profile B) — for comparison |

## Key results (Track 2)

**ARI(augmented GMM, k-means) = 0.2253** — MATERIAL CHANGE.  
**Participants switched vs DS5_01:** 108/414 (26.1%)  

Adding `has_stable_fp` (binary, 15.9% prevalence) shifts the GMM boundary further from DS5_01.
GMM Profile A expands to 233 (vs. 210 in Track 1). This confirms that attractor existence
adds structure that moves participants across the clustering boundary, even when the primary
features are unchanged.

**Stable FP prevalence by GMM Track 1 profile:**
- Profile A: 20.5% have stable FP
- Profile B: 11.3% have stable FP
- Interpretation: attractor structure is modestly more common in Profile A (distributed/variable)
  than Profile B (single-app/concentrated).

**HHI_net_v2 availability by profile:**
- Profile A: 61.4% have NeT v2 data (cross-app transitions exist)
- Profile B: 0.0% have NeT v2 data (single-app → no cross-app transitions after self-loop removal)

## Known limitations

- ARI further from DS5_01 than Track 1 — adding `has_stable_fp` is not cosmetic.
- `has_stable_fp` is based on a KDE with limited data (median ~35 days per participant);
  classification is bandwidth-sensitive.

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/phenotyping/ds5_gmm_augmented_assignments.csv')
```

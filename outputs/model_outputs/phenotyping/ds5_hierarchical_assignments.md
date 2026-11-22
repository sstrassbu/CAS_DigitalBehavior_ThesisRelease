# ds5_hierarchical_assignments.csv — Column Reference

**Produced by:** `103_ds5_hierarchical_phenotype.ipynb`  
**Date:** 2026-04-19  
**Unit of observation:** One row per StoP-eligible participant (N=414)  

## What this file contains

Per-participant two-stage hierarchical phenotype assignments. Stage 1 = Phase 1 network-structural split. Stage 2 = behavioral k-means within each profile. Final combined label: `cell_f`.

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Unique participant identifier |
| `study_condition` | str | Friction condition (control/default/reintervention) |
| `profile_p1` | str | Phase 1 (Stage 1) split: Profile A or Profile B |
| `stage2_B` | str or NaN | Stage 2 behavioral label within Profile B; NaN for Profile A participants |
| `stage2_A` | str or NaN | Stage 2 behavioral label within Profile A; NaN for Profile B participants |
| `cell_f` | str | Combined hierarchical cell label (B_behav1, B_behav2, B_behav3, A_all) |
| `cluster_behav` | str | Path A behavior-only cluster label (C1/C2/C3; post-hoc comparison) |
| `subprofile_C` | str | Path C network sub-cluster label (B1/B2/A1/A2; post-hoc comparison) |

## Taxonomy details

- Profile B (N=289): Stage 2 selected k=3; Jaccard=0.954 [STABLE]
- Profile A (N=125): Stage 2 selected k=1; Jaccard=0.744 [MARGINAL]
- Total cells: 4

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/phenotyping/ds5_hierarchical_assignments.csv')
```

## Known limitations

1. Stage 2 is exploratory; cluster labels are DS5-specific and require cross-dataset replication.
2. Condition independence is not guaranteed — Path A found condition chi2=91.885, p<0.0001 for full-sample behavioral clusters.
3. Profile A Stage 2 has lower N (125) than Profile B (289) — stability claims for Profile A are weaker.
4. No causal interpretation — network type does not cause behavioral type.

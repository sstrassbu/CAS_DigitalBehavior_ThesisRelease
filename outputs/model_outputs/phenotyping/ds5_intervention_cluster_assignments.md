# ds5_intervention_cluster_assignments.csv

**Unit of observation:** One row per participant  
**Total rows:** 414 (StoP-eligible participants, complete behavioral features)  
**Produced by:** `105_ds5_intervention_sensitive_phenotype.ipynb`  
**Stage:** Stage 4, Step 2 — Path B  
**Date:** 2026-04-20

---

## What this file contains

Per-participant cluster label assignments from Path B (intervention-sensitive phenotyping).
Contains three cluster label columns reflecting three different levels of analysis:
full-sample, within-reintervention, and within-control. Path F and Path A labels are
included as cross-path reference columns.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | Experimental condition: `control`, `default`, `reintervention` |
| `profile_p1` | str | Phase 1 (NeT-driven) network profile: `Profile A` or `Profile B` |
| `cluster_b_full` | str | Full-sample Path B cluster (k=3, J=0.940 STABLE): `B_fr1`, `B_fr2`, `B_fr3` |
| `cluster_b_rei` | str | Within-reintervention Path B cluster (k=2, J=0.912 STABLE): `REI_B1`, `REI_B2`; `N/A` for all non-reintervention participants |
| `cluster_b_con` | str | Within-control Path B cluster (k=3, J=0.808 STABLE): `CON_B1`, `CON_B2`, `CON_B3`; `N/A` for all non-control participants |
| `cluster_behav` | str | Path A behavior-only cluster reference: `C1`, `C2`, `C3` |
| `cell_f` | str | Path F hierarchical taxonomy reference: `B_behav1`, `B_behav2`, `B_behav3`, `A_all` |
| `cond_cluster_full` | str | Path E within-condition cluster reference: `CON_C1`, `CON_C2`, `REI_C1`, `REI_C2`, `undifferentiated` |

---

## Full-sample cluster labels (cluster_b_full)

Derived from k-means on `[H_out_resid, sig_hat, H_emp]` after correlation gate dropped
`x_mean` (r=-0.707 with H_out_resid, exceeding |r|>0.70 threshold). Ordered by
`H_out_resid` ascending (B_fr1 = lowest friction-response diversity; B_fr3 = highest).

| Label | N | H_out_resid | sig_hat | H_emp | x_mean (overlay) | chi_behav (overlay) |
|---|---|---|---|---|---|---|
| B_fr1 | 148 | -0.211 | 0.140 | 1.548 | 0.837 | 19.2 |
| B_fr2 | 198 | -0.003 | 0.281 | 2.423 | 0.673 | 7.4 |
| B_fr3 | 68 | 0.467 | 0.133 | 1.958 | 0.444 | 45.8 |

---

## Within-condition labels

Within-reintervention (N=135): k=2 (k=3 rejected: min_cell=19; k=4 rejected: min_cell=18)
Within-control (N=137): k=3 STABLE (J=0.808; min_cell=30 exactly met)
Default (N=142): NO CLUSTERING — descriptive only (blueprint decision; lowest H_out_resid variance: std=0.206)

---

## Source file

Feature inputs from: `ds5_phenotype_feature_matrix.csv`  
Path A labels from: `ds5_behav_only_cluster_assignments.csv`  
Path F labels from: `ds5_hierarchical_assignments.csv`  
Path E labels from: `ds5_condition_cluster_assignments.csv`

---

## Known limitations

- `cluster_b_full` ARI vs Path A = 0.725 — high alignment; H_out_resid does not add an
  orthogonal dimension at the full-sample level
- Within-reintervention k=2 exactly reproduces the Path E reintervention solution (ARI=1.000)
  — H_out_resid and x_mean are interchangeable discriminators within reintervention
- `cluster_b_con` k=3 is STABLE but min_cell=30 exactly met for CON_B3 — interpret with caveat
- Default participants carry no `cluster_b_rei` or `cluster_b_con` labels (N/A)
- Psychosocial scales: all ns after Bonferroni correction (n=6 tests)

---

## Load snippet

```python
import pandas as pd
assignments = pd.read_csv('outputs/model_outputs/phenotyping/ds5_intervention_cluster_assignments.csv')
# Full-sample clusters
print(assignments['cluster_b_full'].value_counts())
# Reintervention-only clusters
rei = assignments[assignments['study_condition'] == 'reintervention']
print(rei['cluster_b_rei'].value_counts())
```

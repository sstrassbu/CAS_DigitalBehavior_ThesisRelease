# ds5_net_subcluster_assignments.csv — Output Documentation

**Produced by:** `notebooks/101_ds5_network_subphenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path C (Network-Structural Sub-Phenotyping)
**Date:** 2026-04-19
**Blueprint:** `outputs/reports/stage4/ds5_path_c_network_subphenotype_blueprint.md`

---

## What this file contains

Sub-cluster assignments for DS5 participants from the Path C network-structural
sub-phenotyping analysis. Each row is one participant. Sub-cluster labels are assigned
separately within Profile A and Profile B (from Phase 1 clustering). A full-sample
NeT-only cluster label is also included as a robustness check.

**Unit of observation:** One participant (participant_id_canonical)

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Unique participant identifier |
| `study_condition` | str | Experimental condition: control / default / reintervention |
| `profile_p1` | str | Phase 1 cluster label: Profile A (distributed) or Profile B (hub-dominated) |
| `subprofile_B` | str | Profile B sub-cluster label (B1 or B2). NaN for Profile A participants. |
| `subprofile_A` | str | Profile A sub-cluster label (A1 or A2). NaN for Profile B participants. |
| `cluster_net_only` | int | Full-sample NeT-only cluster index (0 or 1). The k=2 solution was **fitted** on all 463 NeT-eligible participants (notebook 101 cell 31), but this file stores labels only for the 414 Phase 1 participants (all of whom are NeT-eligible, so there are 0 NaN in this column; counts 0 → 290, 1 → 124). The 49 NeT-eligible participants outside the Phase 1 complete-case sample are **not present in this file**, and their labels are not saved anywhere else — the full-sample solution is therefore not fully reproducible from the shipped outputs. |

---

## Sub-cluster definitions

### Profile B sub-clusters (k=2; N=289 total; Jaccard=0.996 STABLE)

| Sub-profile | N | Interpretation |
|---|---|---|
| B1 | 260 (89.9%) | Single-app / near-single-app locked: HHI≈1.0, rho_self≈1.0, H_trans≈0, H_app≈0. Every (or nearly every) OneSec event targets the same app; no observable inter-app transitions. |
| B2 | 29 (10.1%) | Multi-app hub-anchored: HHI=0.82, rho_self=0.95, H_trans=0.23, H_app=0.48. One dominant app captures most friction events, but occasional transitions to a small secondary set are observed. |

**Note on B2 size:** N=29 is just below the pre-specified minimum of 30 participants. The
k=2 solution was selected as a fallback because no k yielded all clusters ≥30. The
extremely high stability (Jaccard=0.996, silhouette=0.866) justifies treating B2 as
a valid phenotype, but findings should be reported with explicit N caveat.

### Profile A sub-clusters (k=2; N=125 total; Jaccard=0.835 STABLE)

| Sub-profile | N | Interpretation |
|---|---|---|
| A1 | 85 (68.0%) | Moderately distributed network: HHI=0.60, rho_self=0.81, H_trans=0.65, H_app=0.88. Multiple apps share friction-event flow; one app still somewhat dominant. |
| A2 | 40 (32.0%) | Highly distributed network: HHI=0.43, rho_self=0.66, H_trans=1.09, H_app=1.42. Friction events spread across many apps; no clearly dominant hub. |

**Note on Profile A stability:** Bootstrap Jaccard=0.835 with std=0.157 (wide). The
sub-structure is stable on average but shows greater variability than Profile B or
the full-sample solution. Report as tentative; interpret with caution.

---

## How this file was produced

1. Phase 1 cluster assignments loaded from `ds5_cluster_assignments.csv`
2. NeT features merged from `network_models/participant_network_metrics.csv`
3. Profile B sub-clustering: StandardScaler on [HHI_net, rho_self, H_trans, H_app];
   k-means (k=2, k-means++ init, 10 seeds, random_state=42); sub-profiles ordered by
   H_trans median (B1 = lower H_trans, B2 = higher H_trans)
4. Profile A sub-clustering: same procedure on Profile A subsample
5. Full-sample NeT-only: k=2 on all N=463 NeT-eligible participants
6. All labels stored per-participant; mutual exclusivity enforced (B labels NaN for
   Profile A members and vice versa)

---

## Cleaning steps applied

- Participants missing any of [HHI_net, rho_self, H_trans, H_app] excluded from clustering
- No imputation
- Standard scaling fit separately within Profile B, Profile A, and full sample (not cross-fit)

---

## Key limitations

1. DS5 networks are built from OneSec-triggered events only — not total app usage.
   B1 participants may use many apps; they simply never triggered OneSec on a second app.
2. H_trans and H_app are zero-inflated within Profile B (70.6% at exactly 0).
   The B1/B2 split is a discrete structural distinction, not a continuous gradient.
3. Temporal succession (app_i → app_j) is not causal coupling; Markov property unverified.
4. B2 has N=29 (just below stated threshold of 30); interpret with explicit caveat.
5. Profile A Jaccard std=0.157 is wide; A1/A2 sub-structure should be treated as tentative.
6. All findings are exploratory and DS5-specific; cross-dataset replication required.

---

## How to load

```python
import pandas as pd
from pathlib import Path

BASE = Path('outputs/model_outputs/phenotyping')
assignments = pd.read_csv(BASE / 'ds5_net_subcluster_assignments.csv')

# Profile B sub-types
profB_labels = assignments[assignments['profile_p1'] == 'Profile B'][
    ['participant_id_canonical', 'subprofile_B']
].dropna()

# Profile A sub-types
profA_labels = assignments[assignments['profile_p1'] == 'Profile A'][
    ['participant_id_canonical', 'subprofile_A']
].dropna()
```

# ds5_behav_only_cluster_assignments.csv — Output Documentation

**Produced by:** `notebooks/102_ds5_behavior_only_phenotype.ipynb`
**Stage:** Stage 4, Step 2 — Path A (Behavior-Only Phenotyping)
**Date:** 2026-04-19
**Blueprint:** `outputs/reports/stage4/ds5_path_a_behavior_only_blueprint.md`

---

## What this file contains

Behavior-only cluster assignments for DS5 participants from Path A. Each row is one
participant. Cluster labels are derived from k-means on [sig_hat, H_emp, x_mean] with
NO network topology features. Phase 1 and Path C labels are included for post-hoc
cross-path comparison.

**Unit of observation:** One participant (participant_id_canonical)

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Unique participant identifier |
| `study_condition` | str | Experimental condition: control / default / reintervention |
| `profile_p1` | str | Phase 1 cluster label (post-hoc overlay, not used in clustering) |
| `subprofile_C` | str | Path C composite sub-cluster label (B1/B2/A1/A2; post-hoc overlay) |
| `cluster_net_only` | int | Path C NeT-only cluster index (post-hoc overlay) |
| `cluster_behav` | str | **PATH A RESULT** — Behavior-only cluster label (C1, C2, ...) |

---

## Cluster definitions (k=3 primary solution)

**Clustering features:** sig_hat, H_emp, x_mean (StandardScaler; fit on N=414)
**Bootstrap Jaccard:** 0.991 ± 0.022 (STABLE)
**Silhouette:** 0.4071

Clusters ordered by mean sig_hat ascending (C1 = lowest noise).

| Cluster | N | Key means |
|---|---|---|
| C1 | 62 | sig_hat=0.121, H_emp=1.734, x_mean=0.358 |
| C2 | 152 | sig_hat=0.143, H_emp=1.604, x_mean=0.859 |
| C3 | 200 | sig_hat=0.281, H_emp=2.454, x_mean=0.673 |

---

## Cross-path ARI summary

| Comparison | ARI | Interpretation |
|---|---|---|
| Path A vs Phase 1 profile | 0.020 | Low overlap — orthogonal structure |
| Path A vs Path C subprofiles | 0.017 | See full interpretation in run summary |
| Path A vs NeT-only cluster | 0.020 | Low overlap |

---

## How to load

```python
import pandas as pd
from pathlib import Path

BASE = Path('outputs/model_outputs/phenotyping')
assignments = pd.read_csv(BASE / 'ds5_behav_only_cluster_assignments.csv')

# Behavior-only cluster
behav_labels = assignments[['participant_id_canonical', 'cluster_behav']]
```

---

## Key limitations

1. sig_hat, H_emp, x_mean may still correlate with network type even without NeT input
2. ARI vs Phase 1 = 0.020 — interpret with care (see run summary)
3. All findings are exploratory and DS5-specific; not validated across datasets

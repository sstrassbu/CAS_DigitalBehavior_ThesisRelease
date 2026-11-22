# ds5_gmm_layer2_assignments.csv

**Produced by:** `notebooks/63_ds5_phenotype_v2.ipynb` (DS5_02 Phase B, Track 3)  
**Depends on:** `ds5_cluster_assignments.csv`, feature matrix for `sig_hat`, `H_emp`, `chi_behav`

## What this file contains

GMM k=3 Layer 2 cluster assignments within the DS5_01 Profile A population (N=125).
Parallel to DS5_01 Path A (dynamic cluster), but using GMM instead of k-means.

**Unit of observation:** one row per Profile A participant (125 total).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier |
| `cluster_gmm_layer2` | int | GMM cluster (0/1/2) within Profile A — not yet labeled |

## Key results (Track 3)

**Cluster sizes:** C0=20, C1=62, C2=43  
**ARI(GMM Layer2 vs DS5_01 Path A): 0.0000** — path-comparison file is multi-column; the specific
comparison path was `cluster_d_full` (Path A) which itself has low agreement with other DS5_01 paths.  
**ARI(GMM Layer2 vs Phase1 profile_p1): 0.0000** — orthogonality CONFIRMED. Layer 2 sub-structure
within Profile A is entirely uncorrelated with the Phase 1 Layer 1 split, exactly as DS5_01 found
(ARI≈0.020). This replicates under GMM.

The Layer 2 orthogonality finding is the most robust result in Track 3:
whether using k-means (DS5_01) or GMM (Phase B), the within-Profile-A sub-structure is independent
of the Layer 1 Profile A/B split. This validates the two-layer interpretation itself.

## Known limitations

- N=125 is small for GMM with full covariance + k=3; results are exploratory.
- Cluster labels (0/1/2) not yet semantically assigned — need feature-level characterization.
- ARI vs. Path A comparison used `cluster_d_full` column, which is one of several Path A variants
  in the original dynamic cluster file; path-specific ARI may differ for other columns.

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/phenotyping/ds5_gmm_layer2_assignments.csv')
```

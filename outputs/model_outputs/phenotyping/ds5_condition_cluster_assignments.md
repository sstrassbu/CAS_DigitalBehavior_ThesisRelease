# ds5_condition_cluster_assignments.csv

## What this file contains
Per-participant cluster assignments from Path E condition-stratified phenotyping.
Each row is one DS5 participant (N=414, StoP-eligible with complete behavioral features).

## Column reference
| Column | Type | Description |
|---|---|---|
| participant_id_canonical | str | Unique participant identifier |
| study_condition | str | Experimental condition: control / default / reintervention |
| profile_p1 | str | Phase 1 network profile: Profile A / Profile B |
| cond_cluster_full | str | Within-condition full-sample cluster (e.g. CON_C1, DEF_C2) |
| cond_cluster_B | str | Within-condition Profile B cluster (e.g. CON_B1); NaN for Profile A |
| cluster_behav | str | Path A full-sample behavioral cluster: C1 / C2 / C3 |
| cell_f | str | Path F hierarchical cell: B_behav1/2/3 or A_all |
| subprofile_C | str | Path C network sub-cluster: B1/B2/A1/A2 |

## How produced
Notebook: 104_ds5_condition_stratified_phenotype.ipynb
Source: ds5_phenotype_feature_matrix.csv, ds5_behav_only_cluster_assignments.csv,
        ds5_hierarchical_assignments.csv
Clustering: KMeans(k-means++, n_init=10, random_state=42)
Scaler: within-condition StandardScaler on [sig_hat, H_emp, x_mean]

## Known limitations
- Profile A within-condition clustering not feasible (N=36-46 per condition < 30 min cell)
- cond_cluster_B is NaN for all Profile A participants
- Cluster labels are condition-specific — CON_C1 and DEF_C1 are NOT the same type
- Within-condition scaler means centroids are in incomparable coordinate systems

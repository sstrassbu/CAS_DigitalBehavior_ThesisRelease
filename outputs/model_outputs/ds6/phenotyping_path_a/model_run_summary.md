# DS6 Path A' (Behavior-Only, DyS removed) -- Model Run Summary

**Run at:** 2026-08-06 15:42:12
**Notebook:** notebooks/141_ds6_behavior_only_phenotype.ipynb
**Blueprint:** outputs/reports/stage4/step2_phenotyping/ds6_path_a_behavior_only_blueprint.md

## ⚠ NO FEASIBLE k -- READ THIS FIRST

k=2/3/4 all isolate the SAME ~9-participant group regardless of k (min_size=9 at every k tested) -- a multivariate-outlier signature (susceptibility 4-10x the population mean combined with elevated hhi_change), NOT evidence of a real second phenotype. The k=2 result below is reported as an outlier characterization only, not a validated cluster solution. Same failure mode Structured's own Path D notebook already caught once.

## Trigger
User inspected the main pass's radar chart and asked why Profile A showed nothing on the
regime-change axis. Root cause verified: that axis perfectly separated the k=2 clusters
(Profile A = regime_changed=0 for all 125), so it had zero within-cluster variance for
Profile A by construction -- a real dominance signal, not a rendering bug. This notebook
tests the phenotype structure with that dominant feature removed entirely.

## Sample
- Complete-case population (4 behavioral features, no DyS): N=227

## Feature redundancy
No unexpected redundant pairs (|r|>0.6).

## K-selection
- k=2: silhouette=0.629, CH=68.1, DB=0.856, min_cell=9, sizes={0: 218, 1: 9}
- k=3: silhouette=0.309, CH=73.2, DB=1.137, min_cell=9, sizes={1: 165, 0: 53, 2: 9}
- k=4: silhouette=0.221, CH=72.0, DB=1.204, min_cell=9, sizes={0: 86, 3: 80, 1: 52, 2: 9}

**Selected k=2** (silhouette=0.629, subject to min_cell>=11)

## Stability
- Bootstrap Jaccard (100 resamples, 80% subsample): mean=0.910, std=0.206
- Verdict: STABLE (BUT PROVISIONAL -- this k was never min-cell-valid; a high Jaccard here just means the 9-person outlier group is consistently re-identified across resamples, which is expected for extreme outliers and does NOT indicate genuine 2-phenotype structure)

## PCA
- PC1+PC2 variance explained: 60.2%

## Cluster profiles (raw means)
               h_period  hhi_change  H_emp_baseline  susceptibility
cluster_label                                                      
Profile A'       0.0992      0.0066          3.0628          0.0321
Profile B'      -0.2986      0.1266          3.1489          0.3882

## Cluster sizes
cluster_label
Profile A'    218
Profile B'      9

## ARI comparison to the main pass (notebook 140)
- Overlap N: 227
- ARI: 0.0235
- Verdict: LOW/ORTHOGONAL -- removing DyS changes the split substantially; the main pass's k=2 solution was substantially DyS's own signal

## Psychosocial overlays (N=176)
                    scale  H_stat  p_raw  p_bonferroni
   addiction_index_change   1.652 0.1987        0.3974
self_control_index_change   0.649 0.4206        0.8412

## Coherence check: the 9 outliers are all in friction conditions

Cross-tabulating the 9 "Profile B'" outliers against `study_condition`: 7 default, 2
intervention, **0 control**. Small N (too small for its own formal test), but directionally
exactly matches StM's (71) independently-established headline finding that control shows
significantly lower susceptibility than either friction condition (p=0.0011, p=0.0075). The
most extreme individual susceptibility values in the whole dataset all belong to
friction-exposed participants — a nice individual-level confirmation of a population-level
result found by a completely different analysis.

## Key limitations
1. Removing DyS entirely (not substituting) is a deliberate test of dominance, not a claim
   that DyS's information is worthless -- see blueprint Part 1
2. 4 features only -- narrower feature space than the main pass's 5
3. Cluster labels here (Profile A'/B'/...) are a SEPARATE KMeans fit, not a subset of the
   main pass's labels -- compare via ARI (Section 10), not by assuming label correspondence
4. No feasible k met the min_cell floor (see caveat above) -- this pass answers "is there an
   extreme-outlier subgroup in the 4 continuous features" rather than the originally-intended
   "does balanced phenotype structure reproduce without DyS"

## Output files

| File | Rows | Unit of observation | Key columns |
|---|---|---|---|
| `phenotype_feature_matrix.csv` | 227 | One row per complete-case participant | `h_period`, `hhi_change`, `H_emp_baseline`, `susceptibility` |
| `feature_redundancy_report.csv` | 4 | One row per feature (correlation matrix) | Pearson r between each pair of the 4 features |
| `cluster_assignments.csv` | 227 | One row per complete-case participant | `participant_id_canonical`, `cluster_label`, all 4 features |
| `cluster_profiles.csv` | 4 | One row per (feature × statistic), grouped by cluster | mean/median/std of each feature, per cluster |
| `ari_comparison.csv` | 1 | Single comparison result | `n_overlap`, `k_main`, `k_path_a`, `ARI`, `verdict` |
| `psychosocial_overlays.csv` | 2 | One row per psychosocial scale | `scale`, `H_stat`, `p_raw`, `p_bonferroni` |

**How to load:**
```python
import pandas as pd
from pathlib import Path
OUT = Path("outputs/model_outputs/ds6/phenotyping_path_a")
clusters = pd.read_csv(OUT / "cluster_assignments.csv")
```

**Source:** StoP (73), NeT (74), InT (75), StM (71) outputs; `outputs/model_outputs/ds6/phenotyping/cluster_assignments.csv` (for ARI); `outputs/model_outputs/ds6/system_dynamics/participant_stock_flow.csv` (overlay).
**Producing notebook:** `notebooks/141_ds6_behavior_only_phenotype.ipynb`.

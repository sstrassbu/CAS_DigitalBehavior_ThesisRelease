# Structured Phenotyping (Step 2) -- Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/120_structured_phenotype_exploration.ipynb
**Blueprint:** outputs/reports/structured/structured_phenotyping_blueprint.md

## Sample
- Complete-case population (all 7 model families eligible): N=36

## Feature redundancy
[('H_completion', 'state_space_volatility', np.float64(0.68))]

## K-selection
- k=2: silhouette=0.213, CH=11.0, DB=1.636, min_cell=14, sizes={0: 22, 1: 14}
- k=3: silhouette=0.196, CH=10.2, DB=1.402, min_cell=8, sizes={0: 19, 1: 9, 2: 8}
- k=4: silhouette=0.194, CH=9.9, DB=1.384, min_cell=8, sizes={2: 10, 1: 9, 0: 9, 3: 8}

**Selected k=2** (silhouette=0.213, subject to min_cell>=10)

## Stability
- Bootstrap Jaccard (100 resamples, 80% subsample): mean=0.775, std=0.096
- Verdict: STABLE (N=36 caveat: noisier than DS5's N=414 equivalent)

## PCA
- PC1+PC2 variance explained: 56.9%

## Cluster profiles (raw means)
               HHI_net  H_completion  created_Fano_factor  state_space_volatility  backlog_trend_slope  susceptibility  mean_commitment_score
cluster_label                                                                                                                                
Profile A       0.5052        1.1569               7.4912                  1.7147               2.0366          0.0153                 3.0322
Profile B       0.5729        0.5746               4.6134                  0.5480               5.9573          0.0048                 2.7132

## Cluster sizes
cluster_label
Profile A    22
Profile B    14

## Psychosocial overlays (exploratory, N=33)
                                scale  H_stat  p_raw  p_bonferroni
                 life_happiness_score   1.153 0.2830        1.0000
         productivity_happiness_score   3.770 0.0522        0.2610
productivity_importance_general_score   0.224 0.6356        1.0000
                pct_tasks_planned_num   0.764 0.3822        1.0000
      pct_planned_tasks_completed_num   4.810 0.0283        0.1415

## Key limitations
1. N=36 complete-case population -- much smaller than DS5's N=414; all statistics noisier
2. One feature per model family chosen for interpretability; does not exhaust each model's full output
3. Radar individual-line density will look sparser than DS5's equivalent purely due to N
4. Psychosocial overlay N further thinned by consent/completion filtering -- exploratory only
5. k=2 ceiling expected and likely required by minimum cell size at this N

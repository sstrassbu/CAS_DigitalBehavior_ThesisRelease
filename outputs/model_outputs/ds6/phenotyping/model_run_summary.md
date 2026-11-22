# DS6 Phenotyping (Step 2) -- Model Run Summary

**Run at:** 2026-08-11 01:25:37
**Notebook:** notebooks/140_ds6_phenotype_exploration.ipynb
**Blueprint:** outputs/reports/stage4/step2_phenotyping/ds6_phenotyping_blueprint.md

## Sample
- Complete-case population (all 5 behavioral features eligible): N=227

## Feature redundancy
No unexpected redundant pairs (|r|>0.6).

## K-selection
- k=2: silhouette=0.296, CH=61.3, DB=1.530, min_cell=102, sizes={0: 125, 1: 102}
- k=3: silhouette=0.311, CH=70.6, DB=1.183, min_cell=9, sizes={0: 125, 1: 93, 2: 9}
- k=4: silhouette=0.340, CH=72.1, DB=1.114, min_cell=9, sizes={0: 100, 1: 92, 3: 26, 2: 9}

**Selected k=2** (silhouette=0.296, subject to min_cell>=11)

## Stability
- Bootstrap Jaccard (100 resamples, 80% subsample): mean=0.714, std=0.329
- Verdict: MARGINAL

## PCA
- PC1+PC2 variance explained: 50.7%

## Cluster profiles (raw means)
               h_period  hhi_change  H_emp_baseline  regime_changed  susceptibility
cluster_label                                                                      
Profile A        0.1243      0.0041          3.0551             0.0          0.0300
Profile B        0.0333      0.0203          3.0798             1.0          0.0661

## Cluster sizes
cluster_label
Profile A    125
Profile B    102

## Psychosocial overlays (SyD's role, N=176)
                    scale  H_stat  p_raw  p_bonferroni
   addiction_index_change   0.037 0.8471         1.000
self_control_index_change   6.820 0.0090         0.018

## Key limitations
1. 5 behavioral features (not 6) -- SyD deliberately excluded from clustering, used as the
   overlay instead (blueprint Part 1); this notebook does not exhaust each model's full output
2. First DS6 phenotyping pass -- one clustering pass, not DS5's six-path exploration
3. regime_changed is binary (0/1), a qualitatively different feature type from the other 4
   continuous features -- standardized the same way (z-score) but interpret with this in mind
4. Psychosocial overlay N further thinned to SyD's own N=188 (prepost-eligible subset) --
   exploratory only, uncorrected beyond the 2-test Bonferroni shown above

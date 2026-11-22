# Structured Path A -- Behavior-Only Phenotyping -- Model Run Summary

**Run date:** 2026-08-05
**Notebook:** notebooks/122_structured_behavior_only_phenotype.ipynb
**Blueprint:** outputs/reports/structured/structured_path_a_blueprint.md

## Population
- Path A complete-case (6 non-NeT features): N=41
- Phase 1 (7-feature) population was N=36

## Feature redundancy
[('H_completion', 'state_space_volatility', np.float64(0.633))] (H_completion/state_space_volatility carried forward from Phase 1, not new)

## K-selection
- k=2: silhouette=0.237, CH=13.8, DB=1.517, min_cell=17, sizes={0: 24, 1: 17}
- k=3: silhouette=0.227, CH=11.9, DB=1.393, min_cell=6, sizes={1: 19, 0: 16, 2: 6}
- k=4: silhouette=0.229, CH=11.8, DB=1.213, min_cell=4, sizes={2: 17, 3: 15, 1: 5, 0: 4}

**Selected k=2** (silhouette=0.237, subject to min_cell>=10)

## Stability
- Bootstrap Jaccard (100 resamples, 80% subsample): mean=0.885, std=0.105
- Verdict: STABLE

## PCA
- PC1+PC2 variance explained: 59.0%

## Cluster profiles (raw means)
                H_completion  created_Fano_factor  state_space_volatility  backlog_trend_slope  susceptibility  mean_commitment_score
cluster_label                                                                                                                        
BehavProfile A        1.1390               7.0479                  1.7517               1.9021          0.0178                 3.0298
BehavProfile B        0.6124               4.7500                  0.5269               5.3314          0.0070                 2.6334

## Cluster sizes
cluster_label
BehavProfile A    24
BehavProfile B    17

## Comparison to Phase 1 (the central Path A question)
- Overlap N: 36
- ARI(Path A vs Phase 1): 1.000  (DS5's equivalent: 0.020, orthogonal)
- CONFIRMED: Path A substantially reproduces Phase 1 -- Structured's dominant split IS the behavioral-dynamics axis, unlike DS5 where it was network-driven.

## Path E analog: subscription-stratified feasibility check
subgroup  n  feasible                                                                                                                              reason  jaccard_mean
    free 12     False k=2 ran, sizes={0: np.int64(9), 1: np.int64(3)}, min_cell=3 < 10 (same floor used for k-selection everywhere else in this notebook)           NaN
     pro 29      True                                                                k=2 ran, sizes={0: np.int64(15), 1: np.int64(14)}, min_cell=14 >= 10         0.895

## Key limitations
1. N=41 -- much smaller than DS5's Path A (N=414); all statistics noisier
2. Same H_completion/state_space_volatility correlation (r~0.63-0.68) present as in Phase 1, not resolved
3. Path E analog is a weak, observational (non-randomized) stratifier -- not a real test of condition-invariance
4. k=4 tested but likely infeasible at this N; k selection constrained by min_cell=10 floor

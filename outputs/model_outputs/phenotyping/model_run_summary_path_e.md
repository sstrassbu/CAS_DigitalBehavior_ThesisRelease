# DS5 Step 2 Path E — Condition-Stratified Phenotyping: Model Run Summary

**Date:** 2026-04-20
**Notebook:** 104_ds5_condition_stratified_phenotype.ipynb
**Stage:** Stage 4, Step 2 — Path E

---

## Run parameters
- Core clustering features: ['sig_hat', 'H_emp', 'x_mean']
- Conditions analyzed: ['control', 'default', 'reintervention']
- Scaling: within-condition StandardScaler (primary); full-sample scaler (sensitivity)
- RANDOM_STATE: 42
- Bootstrap: 100 iterations, 0.8 sample fraction
- Min cluster size threshold: 30
- Analysis population: N = 414

## k-selection results (full-sample within-condition)

| Condition | N | Selected k | Jaccard | Stability flag |
|---|---|---|---|---|
| control | 137 | 2 | 0.744 | MARGINAL (0.60–0.75 band; accepted under the §8 rule, would be rejected under the §6 ≥0.75 rule and under Path F's ≥0.75 rule) |
| default | 142 | none | n/a | no solution met the min-cell ≥ 30 floor |
| reintervention | 135 | 2 | 0.959 | STABLE |

## k-selection results (Profile B within-condition)

| Condition | Profile B N | Selected k |
|---|---|---|
| control | 94 | 2 |
| default | 96 | none |
| reintervention | 99 | 2 |

Note: Profile A within-condition clustering NOT attempted (N=36-46, cells < 30).

## Cross-path comparison summary

| Comparison | Value |
|---|---|
| ARI(control within-cond vs Path A) | 0.2623 |
| ARI(default within-cond vs Path A) | 0.0000 |
| ARI(reintervention within-cond vs Path A) | 0.6966 |
| Mean ARI across conditions | 0.3196 |

## Interpretation outcome

**Matched outcome: C/D — Structure-dependent (low ARI; condition shapes phenotype space)**

## Output files
- ds5_condition_cluster_assignments.csv
- ds5_condition_cluster_profiles.csv
- ds5_condition_cluster_stability.csv
- figures/fig_e1 through fig_e8

## Key limitations
1. Within-condition clusters use condition-specific scalers; labels are NOT cross-condition comparable
2. Profile A within-condition clustering infeasible (N < 30 per cell)
3. No causal interpretation: condition was randomly assigned, but cluster memberships are post-hoc
4. ARI comparisons between different-k solutions are lower-bounded by chance; interpret cautiously
5. Condition effect on behavioral features cannot be separated from true individual differences

# DS5 Step 2 Path F — Hierarchical Phenotyping: Model Run Summary

**Date:** 2026-04-19
**Notebook:** 103_ds5_hierarchical_phenotype.ipynb
**Stage:** Stage 4, Step 2 — Path F

---

## Run parameters
- Core Stage 2 features: ['sig_hat', 'H_emp', 'x_mean']
- Stage 1 split: profile_p1 (Phase 1 assignments)
- Within-group StandardScaler (primary)
- RANDOM_STATE: 42
- Bootstrap: 100 iterations, 80% sample fraction
- Min cluster size threshold: 30
- Analysis population: N = 414

## Stage 2 k-selection results

### Profile B (N=289)
- Selected k: 3
- Bootstrap Jaccard: 0.954 ± 0.071 [STABLE]

### Profile A (N=125)
- Selected k: 1
- Profile A Stage 2 split: False
- Bootstrap Jaccard: 0.744 ± 0.198 [MARGINAL]

## Final taxonomy

- Total cells: 4
- Cell labels: B_behav1, B_behav2, B_behav3, A_all

## Cell profiles (mean values)

| Cell | N | sig_hat | H_emp | x_mean |
|---|---|---|---|---|
| B_behav1 | 37 | 0.1268 | 1.7535 | 0.3643 |
| B_behav2 | 104 | 0.146 | 1.6073 | 0.8668 |
| B_behav3 | 148 | 0.2818 | 2.4631 | 0.6769 |
| A_all | 125 | 0.1906 | 1.964 | 0.6688 |

## Cross-path comparisons

- ARI(Stage 1 vs Phase 1):               1.0  (expected 1.000)
- ARI(Stage2-B vs Path A within B):      1.0
- ARI(Stage2-A vs Path A within A):      0.0
- ARI(Path F combined vs Path A):        0.5196
- ARI(Path F combined vs Path C):        0.3431
- Cramér's V (Path F × Path C):          0.579
- Chi-square (Path F × Path C sub):      416.9, p=0.0

## Output files
- ds5_hierarchical_assignments.csv
- ds5_hierarchical_assignments.md
- ds5_hierarchical_profiles.csv
- ds5_hierarchical_profiles.md
- ds5_hierarchical_stability.csv
- figures/fig_f1 through fig_f8

## Key limitations
1. Stage 2 behavioral clusters are exploratory and DS5-specific
2. Condition independence not guaranteed (Path A found chi2=91.885, p<0.0001 full-sample)
3. Profile A Stage 2 has lower power (N=125) than Profile B (N=289)
4. No causal interpretation of network vs behavioral type relationship
5. Cross-dataset replication required before any claim of generalizability
6. Feature-set sensitivity NOT tested: the blueprint's pre-registered Step 8 (re-run Stage 2 with H_hour added; H_hour correlates with sig_hat at r=-0.52) was never implemented. Path A's own 3-vs-4-feature ARI was only 0.718, so the 4-cell taxonomy's robustness to feature-set choice is unverified.

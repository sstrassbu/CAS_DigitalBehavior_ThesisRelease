# DS5 Step 2 Path A — Behavior-Only Phenotyping: Model Run Summary

**Date:** 2026-04-19
**Notebook:** 102_ds5_behavior_only_phenotype.ipynb
**Stage:** Stage 4, Step 2 — Path A

---

## Run parameters
- Core clustering features: ['sig_hat', 'H_emp', 'x_mean']
- Sensitivity features: ['sig_hat', 'H_emp', 'x_mean', 'H_hour']
- RANDOM_STATE: 42
- Bootstrap: 100 iterations, 80% sample fraction
- Min cluster size threshold: 30
- Analysis population: N = 414

## Feature notes
- r(H_hour, sig_hat) = -0.510 — strong negative; H_hour excluded from primary clustering
- mu_hat near-zero (|<0.01|): 56.5% — overlay only
- sigma_mu_ratio NaN: 129 of 414 (31.2%) — overlay only

## Primary clustering (3-feature core)
- Selected k: 3
- Silhouette: 0.4071
- Bootstrap Jaccard: 0.991 ± 0.022 (STABLE)
- Cluster sizes: [62, 200, 152]
- Condition χ²: 91.885, p=0.0000
- Psychosocial significant (after Bonferroni): 1 of 5

## Cluster profiles (primary solution)

### C1 (N=62)
- sig_hat: mean=0.1207, median=0.1107
- H_emp: mean=1.7340, median=1.7542
- x_mean: mean=0.3576, median=0.3787
- H_hour: mean=4.1069, median=4.1251
- HHI_net (overlay): mean=0.7812
- rho_self (overlay): mean=0.9222

### C2 (N=152)
- sig_hat: mean=0.1434, median=0.1358
- H_emp: mean=1.6036, median=1.6807
- x_mean: mean=0.8590, median=0.8687
- H_hour: mean=4.0867, median=4.1219
- HHI_net (overlay): mean=0.8580
- rho_self (overlay): mean=0.9158

### C3 (N=200)
- sig_hat: mean=0.2807, median=0.2472
- H_emp: mean=2.4541, median=2.4751
- x_mean: mean=0.6733, median=0.6930
- H_hour: mean=3.9911, median=4.0408
- HHI_net (overlay): mean=0.8593
- rho_self (overlay): mean=0.9279

## Sensitivity run (4-feature: adds H_hour)
- Selected k: 4
- Silhouette: 0.3431
- Bootstrap Jaccard: 0.918 ± 0.057 (STABLE)
- ARI(3-feature k=3 vs 4-feature k=4): 0.718 — **note:** this compares partitions of different cardinality, so part of the disagreement is the k mismatch rather than H_hour's effect.
- ARI at matched k (the quantity blueprint §5 Step 4 actually asks for, same StandardScaler/KMeans/random_state=42 pipeline, N=414): k=2 → 0.582, k=3 → 0.675, k=4 → 0.650. **Primary sensitivity number: 0.675** (k=3 for both feature sets). Conclusion unchanged: H_hour moderately reorganizes the clusters.

## Cross-path comparison
- ARI(Path A vs Phase 1 profile):          0.020
- ARI(Path A vs Path C subprofiles):       0.017
- ARI(Path A vs NeT-only full-sample):     0.020

## Output files
- ds5_behav_only_cluster_assignments.csv
- ds5_behav_only_cluster_profiles.csv
- ds5_behav_only_cluster_stability.csv
- figures/fig_a1_behav_only_distributions.png
- figures/fig_a2_behav_pairplot.png
- figures/fig_a3_behav_pca.png
- figures/fig_a4_cluster_selection.png
- figures/fig_a5_cluster_profiles.png
- figures/fig_a6_cluster_overlay.png
- figures/fig_a7_crosspath_comparison.png

## Key limitations
1. **Condition confound (primary caveat).** All three clustering features are post-treatment quantities that the randomized friction condition itself moves: one-way ANOVA by `study_condition` (N=414) gives H_emp F=66.31, p=1.1e-25, η²=0.244; x_mean F=29.78, p=8.3e-13, η²=0.127; sig_hat F=16.54, p=1.2e-07, η²=0.074. The resulting clusters are correspondingly condition-associated (χ²=91.885, df=4, p=5.2e-19, Cramér's V=0.333; C2 is 58.6% control, C3 is 51.0% default). The ARI=0.020 result below establishes orthogonality to the **network** axis only — it is not evidence of condition-independent trait structure. Path E (notebook 104) was run specifically to adjudicate this; see also `outputs/reports/stage4/post_analysis/ds5_step2_master_synthesis.md` §Limitation 1.
2. sig_hat, H_emp, x_mean may still correlate with network type despite no NeT input
3. mu_hat is near-zero for most participants — no drift dimension in DS5
4. sigma_mu_ratio 31% NaN — impulsivity ratio not available for full sample
5. H_hour strongly correlated with sig_hat (r=-0.510) — not independent
6. All findings are exploratory and DS5-specific; cross-dataset replication required

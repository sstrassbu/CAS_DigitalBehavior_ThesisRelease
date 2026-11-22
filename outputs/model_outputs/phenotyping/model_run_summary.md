# DS5 Step 2 — Phenotyping Model Run Summary

**Date:** 2026-08-11
**Notebook:** 100_phenotype_exploration.ipynb
**Stage:** Stage 4, Step 2

---

## Run parameters
- Phase 1 features: ['sig_hat', 'H_emp', 'x_mean', 'HHI_net', 'rho_self']
- Phase 2 sensitivity extras: ['H_hour', 'H_app', 'chi_behav']
- Phase 1 analysis population (complete case): N=209
- Algorithm: K-means (k-means++ init, 10 seeds)
- Selected k: 2
- RANDOM_STATE: 42

## Cluster selection metrics
- k=2: silhouette=0.290, CH=91.0, DB=1.364, min_size=97
- k=3: silhouette=0.271, CH=90.2, DB=1.166, min_size=63
- k=4: silhouette=0.292, CH=88.7, DB=1.186, min_size=30
- k=5: silhouette=0.280, CH=84.3, DB=1.236, min_size=27
- k=6: silhouette=0.272, CH=80.1, DB=1.160, min_size=7

**Selected solution:** k=2, silhouette=0.290

## Robustness
- Bootstrap Jaccard stability (100 bootstraps, 80% sample): 0.842 (std=0.156)
- Stability verdict: STABLE (>0.75)
- ARI (drop H_emp sensitivity): 0.321
- ARI (drop HHI_net sensitivity): 0.506
- ARI (drop rho_self sensitivity): 0.310
- ARI (Phase 1 vs Phase 2 extended): 0.652

## Cluster profiles (core features)

### Profile A (N=112)
- sig_hat: mean=0.274, median=0.244
- H_emp: mean=2.375, median=2.375
- x_mean: mean=0.696, median=0.714
- HHI_net: mean=0.803, median=0.882
- rho_self: mean=0.915, median=0.966

### Profile B (N=97)
- sig_hat: mean=0.163, median=0.145
- H_emp: mean=1.714, median=1.760
- x_mean: mean=0.825, median=0.826
- HHI_net: mean=0.574, median=0.549
- rho_self: mean=0.728, median=0.733

## Psychosocial overlays
(Bonferroni-corrected p threshold = 0.010 for 5 scales)
- fomo_mean_pre: H=1.12, p_adj=1.0000 (ns)
- belong_mean_pre: H=0.14, p_adj=1.0000 (ns)
- ostracism_mean_pre: H=0.04, p_adj=1.0000 (ns)
- digital_wellbeing_pre: H=0.25, p_adj=1.0000 (ns)
- social_media_wellbeing_pre: H=2.96, p_adj=0.4270 (ns)

## Key limitations
1. Short observation windows (7-45 days): profiles may reflect study-period behavior, not stable traits
2. Proxy: all features from X_t = n_opened/n_events
3. The selected solution is feature-sensitive despite bootstrap stability (drop-one-feature ARIs
   0.310--0.506 for H_emp, HHI_net, and rho_self)
4. H_out condition-confounded (excluded from Phase 1)
5. Effective dimensionality ~3-4 despite 5 input features
6. Step 2 = discovery; cross-dataset replication required
7. Cluster membership is associated with randomized condition, so profiles are post-treatment
   summaries and cannot be interpreted as pre-treatment moderators

## Output files
- ds5_phenotype_feature_matrix.csv
- ds5_feature_redundancy_report.csv
- ds5_cluster_assignments.csv
- ds5_cluster_profiles.csv
- ds5_psychosocial_overlays.csv
- figures/fig0_univariate_distributions.png
- figures/fig1_feature_correlation_matrix.png
- figures/fig2_pca_biplot.png
- figures/fig3_cluster_selection_metrics.png
- figures/fig4_cluster_profiles_radar.png
- figures/fig5_condition_by_cluster.png
- figures/fig6_psychosocial_by_cluster.png
- figures/fig7_dendrogram.png

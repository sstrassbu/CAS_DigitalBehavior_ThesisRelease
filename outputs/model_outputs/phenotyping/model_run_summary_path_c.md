# DS5 Step 2 Path C — Network Sub-Phenotyping: Model Run Summary

**Date:** 2026-04-19
**Notebook:** 101_ds5_network_subphenotype.ipynb
**Stage:** Stage 4, Step 2 — Path C

---

## Run parameters
- NeT clustering features: ['HHI_net', 'rho_self', 'H_trans', 'H_app']
- RANDOM_STATE: 42
- Bootstrap: 100 iterations, 80% sample fraction
- Min cluster size threshold: 30

## Analysis populations
- Profile B (primary): N = 289
- Profile A (secondary): N = 125
- Full NeT-eligible (robustness): N = 463

## Decision gate
- Gate triggered: False
- Profile B H_trans=0: 204 participants (70.6%) — zero-inflated
- Profile B H_trans>0: 85 participants (29.4%)

## Profile B sub-clustering
- Selected k: 2
- Silhouette: 0.866
- Bootstrap Jaccard: 0.996 ± 0.010 (STABLE)
- Condition χ²: 4.567, p=0.1019
- Psychosocial significant (after Bonferroni): 0 of 5

### B1 (N=260)
- HHI_net: mean=0.9953, median=1.0000
- rho_self: mean=0.9977, median=1.0000
- H_trans: mean=0.0104, median=0.0000
- H_app: mean=0.0183, median=0.0000
- sig_hat (overlay): mean=0.2113, median=0.1870
- H_emp (overlay): mean=2.0419, median=2.1244
- x_mean (overlay): mean=0.7134, median=0.7638

### B2 (N=29)
- HHI_net: mean=0.8210, median=0.8091
- rho_self: mean=0.9462, median=0.9500
- H_trans: mean=0.2303, median=0.2151
- H_app: mean=0.4754, median=0.5315
- sig_hat (overlay): mean=0.2296, median=0.2294
- H_emp (overlay): mean=2.2650, median=2.2610
- x_mean (overlay): mean=0.6316, median=0.6351

## Profile A sub-clustering
- Selected k: 2
- Bootstrap Jaccard: 0.835 ± 0.157 (STABLE)
- Sizes: A1 N=85 (68.0%), A2 N=40 (32.0%)
- Condition χ²: 5.656, p=0.0591 — **borderline.** Unlike Profile B (χ²=4.567, p=0.1019), this test sits close to the 0.05 boundary, so the claim that network sub-phenotypes cut across friction conditions is well supported for Profile B but only marginally for Profile A.
- Psychosocial (Kruskal-Wallis A1 vs A2, Bonferroni ×5): **0 of 5 significant** — fomo_mean_pre H=1.122 p_raw=0.2895 p_bonf=1.000; belong_mean_pre H=5.302 p_raw=0.0213 p_bonf=0.107; ostracism_mean_pre H=0.167 p_raw=0.6829 p_bonf=1.000; digital_wellbeing_pre H=5.640 p_raw=0.0176 p_bonf=0.088; social_media_wellbeing_pre H=0.137 p_raw=0.7109 p_bonf=1.000. (These tests were not present in notebook 101 cell 22, which loops over Profile B only; they were computed post-hoc from `ds5_net_subcluster_assignments.csv` joined to `outputs/features/ds5/ds5_survey_features.csv`.)

## Full-sample NeT-only robustness
- Best k: 2
- Bootstrap Jaccard: 0.994 ± 0.007 (STABLE)
- ARI vs Phase 1: 0.990

## H_pi supplementary
- ARI (H_pi-inclusive vs. H_pi-exclusive, k=2): 0.948

## Output files
- ds5_net_subcluster_assignments.csv
- ds5_net_subcluster_profiles.csv
- ds5_net_subcluster_stability.csv
- figures/fig_c1_profileB_net_distributions.png
- figures/fig_c2_profileB_pca.png
- figures/fig_c3_profileB_subcluster_selection.png
- figures/fig_c4_profileB_subcluster_profiles.png
- figures/fig_c5_profileB_overlay.png
- figures/fig_c6_profileA_subcluster.png
- figures/fig_c7_fullsample_net_only.png

## Key limitations
1. DS5 networks are built from OneSec-triggered events only — not total app usage
2. Temporal succession (app_i → app_j) is not causal coupling
3. First-order Markov property is not verified for DS5
4. H_pi is an approximation given short windows (7–45 days)
5. Zero-inflation in H_trans/H_app creates a discrete (not continuous) sub-structure
6. All findings are exploratory and DS5-specific; cross-dataset replication required
7. Bootstrap Jaccard here is an **uncorrected** pairwise co-membership index compared against a fixed 0.75 threshold; its chance baseline depends on cluster balance and is not 0. Simulating the same formula on independent random partitions with matching marginals (300 draws) gives baselines of ≈0.70 for Profile B's 260/29 split (n=231), ≈0.39 for Profile A's 85/40 (n=100) and ≈0.41 for the full NeT-eligible run's ≈70/30 split (n=370). Profile B's Jaccard=0.996 is therefore only ≈0.30 above chance, whereas Profile A's 0.835 is ≈0.44 above chance. Compare Jaccard values only *within*, not *across*, differently-balanced solutions; a chance-corrected statistic (bootstrap ARI, or Hennig's cluster-wise Jaccard against a null reference) would be preferable in any re-run.
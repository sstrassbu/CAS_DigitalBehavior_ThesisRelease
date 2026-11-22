# Structured Path C -- Network-Substructure -- Model Run Summary

**Run date:** 2026-08-05
**Notebook:** notebooks/121_structured_network_subphenotype.ipynb
**Blueprint:** outputs/reports/structured/structured_path_c_blueprint.md

## Population and features
- Full-sample NeT-only: N=45 (is_net_eligible)
- Features: HHI_net, rho_self, H_trans, H_state_marginal (top1_share_net excluded, r=0.961 with HHI_net)

## K-selection
- k=2: silhouette=0.293, CH=18.6, DB=1.418, min_cell=17, sizes={1: 28, 0: 17}
- k=3: silhouette=0.283, CH=18.5, DB=1.206, min_cell=10, sizes={0: 23, 1: 12, 2: 10}
- k=4: silhouette=0.275, CH=19.8, DB=1.123, min_cell=4, sizes={0: 17, 3: 13, 1: 11, 2: 4}

**Selected k=2** (silhouette=0.293)

## Stability
- Bootstrap Jaccard: mean=0.822, std=0.166 -> STABLE
- PC1+PC2 variance explained: 73.1%

## Cluster profiles (raw means)
               HHI_net  rho_self  H_trans  H_state_marginal
cluster_label                                              
NetProfile A    0.5843    0.4214   0.9485            1.3252
NetProfile B    0.5028    0.3436   1.4870            1.8408

## Comparison to Phase 1 and Path A (the central Path C question)
- Overlap N: 36
- ARI(Path C vs Phase 1): 0.173  (DS5's equivalent: 0.990)
- ARI(Path C vs Path A): 0.173
- PARTIAL: some correspondence, weaker than DS5's 0.990 but not fully orthogonal -- network structure contributes some but not most of the Phase 1 split.

## Sub-clustering within Phase 1 profiles
- Profile A (N=22, min_cell floor=6): {'group': 'Profile A NeT sub-cluster', 'n': 22, 'feasible': True, 'min_cell_floor': 6, 'sizes': {1: np.int64(12), 0: np.int64(10)}, 'silhouette': np.float64(0.264), 'jaccard_mean': 0.872, 'jaccard_std': 0.161}
- Profile B (N=14, min_cell floor=4): {'group': 'Profile B NeT sub-cluster', 'n': 14, 'feasible': True, 'min_cell_floor': 4, 'sizes': {0: np.int64(8), 1: np.int64(6)}, 'silhouette': np.float64(0.331), 'jaccard_mean': 0.965, 'jaccard_std': 0.104}

## Key limitations
1. Sub-cluster N (14-22) is far below DS5's already-tentative Profile A sub-clustering (N=125)
2. H_trans/H_state_marginal correlation (r=0.715) retained per Phase 1 precedent, not resolved
3. H_pi (stationary distribution entropy) excluded entirely -- only 8/61 stationary-eligible, far too
   thin to use even as a supplementary check at this population size

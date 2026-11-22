# Structured Path D -- Secondary/Robustness Features -- Model Run Summary

**Run date:** 2026-08-05
**Notebook:** notebooks/124_structured_dynamic_stochastic_phenotype.ipynb
**Blueprint:** outputs/reports/structured/structured_path_d_blueprint.md

## Feature gate
- Correlation gate (|r|>0.9 vs Path A core): dropped none
- Manual drop (replicates Phase 1's established H_config/H_completion r=0.665 finding): ['H_config']
- Final feature set: ['created_mu_hat', 'volume_trend_slope', 'dropout_score', 'H_hour_creation', 'persistence_rate']

## Population
- N=41 (identical to Path A -- no additional eligibility loss)

## K-selection
- k=2: silhouette=0.728, CH=23.2, DB=0.180, min_cell=1, sizes={0: 40, 1: 1}
- k=3: silhouette=0.403, CH=24.5, DB=0.702, min_cell=1, sizes={1: 34, 0: 6, 2: 1}
- k=4: silhouette=0.388, CH=29.8, DB=0.825, min_cell=1, sizes={3: 25, 1: 9, 0: 6, 2: 1}

**NO FEASIBLE K** -- every candidate k (2,3,4) has min_cell=1, driven by a single extreme outlier
(volume_trend_slope as low as -32.1 for one participant -- the same heavy-volume outlier already
flagged in the DyS model_run_summary.md as "driving most of the spread"). Reported as an honest
infeasibility result, not forced into a degenerate 1-vs-N split, matching DS5's own precedent of
reporting its default-condition Path E clustering as infeasible rather than accepting an unstable k=2.

## Comparison to Path A and Phase 1 (the central Path D question)
NOT APPLICABLE: no feasible k-means solution exists for this feature set at N=41 (every candidate k is driven by a single extreme outlier, min_cell=1 throughout) -- there is no cluster labeling to compare against Path A or Phase 1. This is itself the Path D result: these secondary features do not support any stable multi-participant grouping, consistent with DS5's own finding that Path D was its lowest-yield path, taken one step further here (DS5 still found a stable k=2; Structured's smaller N does not even support that).

## Key result
**This IS the Path D finding: the secondary/robustness features (drift, volume trend, dropout score,
temporal spread, persistence) do not support any stable multi-participant grouping at N=41.** DS5's own
Path D was already its lowest-yield path at N=285 (found a stable k=2 that mostly reproduced Path A);
Structured's much smaller N does not even support that much -- consistent with, and an extension of,
DS5's own conclusion that this path adds the least beyond the primary behavioral axis.

## Key limitations
1. Scoped as a compact robustness check per DS5's own low-yield finding for this path, not a full
   six-figure treatment
2. created_sigma_mu_ratio excluded entirely (27.9% NaN within Path A's population) rather than accepting
   a reduced N for one feature
3. H_config excluded via a replication of Phase 1's own established redundancy finding, not a fresh gate

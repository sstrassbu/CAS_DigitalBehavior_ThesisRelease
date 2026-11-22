# Structured Path F -- Joint Taxonomy -- Model Run Summary

**Run date:** 2026-08-05
**Notebook:** notebooks/123_structured_hierarchical_phenotype.ipynb
**Blueprint:** outputs/reports/structured/structured_path_f_blueprint.md

## Joint taxonomy (Path A BehavProfile x Path C NetProfile, N=36)
NetProfile      NetProfile A  NetProfile B
BehavProfile                              
BehavProfile A             4            18
BehavProfile B             8             6

## Independence test
- Fisher's exact: odds ratio=0.167, p=0.0286
- The two axes are NOT statistically independent (p<0.05) -- consistent with Path C's weak-but-nonzero ARI=0.173. The behavioral axis dominates (Path A ARI=1.000 vs Phase 1), but network membership still carries some real, detectable information beyond what the behavioral clusters alone capture.

## Cell profiles (means)

### BehavProfile A x NetProfile A (n=4)
H_completion              1.038
created_Fano_factor       6.047
state_space_volatility    1.865
backlog_trend_slope       1.460
susceptibility            0.016
mean_commitment_score     3.165
HHI_net                   0.590
rho_self                  0.426
H_trans                   0.964
H_state_marginal          1.429

### BehavProfile A x NetProfile B (n=18)
H_completion              1.183
created_Fano_factor       7.812
state_space_volatility    1.681
backlog_trend_slope       2.165
susceptibility            0.015
mean_commitment_score     3.003
HHI_net                   0.486
rho_self                  0.305
H_trans                   1.462
H_state_marginal          1.838

### BehavProfile B x NetProfile A (n=8)
H_completion              0.369
created_Fano_factor       3.932
state_space_volatility    0.511
backlog_trend_slope       6.358
susceptibility            0.004
mean_commitment_score     2.721
HHI_net                   0.566
rho_self                  0.399
H_trans                   1.023
H_state_marginal          1.284

### BehavProfile B x NetProfile B (n=6)
H_completion              0.848
created_Fano_factor       5.522
state_space_volatility    0.598
backlog_trend_slope       5.423
susceptibility            0.006
mean_commitment_score     2.703
HHI_net                   0.582
rho_self                  0.417
H_trans                   1.574
H_state_marginal          1.827

## What this means for future ABM/GaT initialization
A 2x2 typology with cell sizes as found gives up to four candidate agent archetypes for a future
agent-based extension (mirroring DS5's own stated purpose for its 4-cell taxonomy) -- though the
smallest cell is too thin (n<10) to characterize with real confidence; only the two largest cells
should be treated as usable archetypes without further data.

## Key limitations
1. This is a cross-tabulation of two already-fitted global clusterings, not a fresh joint clustering --
   deliberately, to avoid re-deriving what Path C's own Part 4 (local sub-clustering) already covered
2. N=36 -- the smallest population of any of the four exploration paths (intersection of Path A's 41 and
   Path C's 45)
3. Smallest joint cell has very few members -- reported, not smoothed into a false 4-way balance

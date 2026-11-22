# Structured GaT -- Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/66_structured_game_theory.ipynb
**Blueprint:** outputs/reports/structured/structured_gat_blueprint.md

## Commitment-outcome trade-off curve (headline result, N=26,729 tasks)
lifecycle_status  completion_rate  deletion_rate  unresolved_rate      n
commitment_score                                                        
0                          0.3672         0.3867           0.2461    256
1                          0.4024         0.2136           0.3840    763
2                          0.7902         0.0497           0.1601   8446
3                          0.6626         0.0935           0.2439  11863
4                          0.7271         0.1089           0.1640   4757
5                          0.5870         0.1817           0.2314    644

Non-monotonic: completion peaks at commitment_score=2 (79.0%%), declines at score=5 (58.7%%).
Pooled linear r=-0.0054 (p=0.3777) -- understates the real U-shaped effect, reported
only as a secondary summary statistic, not the primary evidence.
Within-participant linear r=0.0633 (p=4.536e-25, n=26,680) -- same shape check on
the demeaned population, see within_curve in the notebook.

## Phenotype labels (all 61 participants; NaN = below is_gat_eligible threshold; 53/61 eligible)
phenotype_label
commitment-oriented     18
flexibility-oriented    18
mixed                   12
NaN                      8
chronic-deferrer         4
adaptive-rescheduler     1
(paper's 5th named phenotype "overload-prone" cross-referenced to SyD's dominant_loop_label, not recomputed)

## Strategy adaptation after rescheduling (pooled vs. within-participant)
                    X                               Y  pearson_r_pooled  p_pooled  pearson_r_within  p_within     n
prior_reschedule_flag commitment_score (current task)           -0.0027  0.779039            0.0113  0.245453 10516

## Design note
No formal game matrix, best-response analysis, or equilibrium concept was built, per the theory paper's
own caution (section 1.3) that GaT, like StM, requires proxy definitions rather than directly-observed
formal quantities. commitment_score is an explicit named proxy, not a utility function.

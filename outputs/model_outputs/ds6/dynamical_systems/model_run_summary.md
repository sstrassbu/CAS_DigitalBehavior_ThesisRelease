# DS6 DyS -- Model Run Summary

**Run at:** 2026-08-11 01:21:13
**Notebook:** notebooks/72_ds6_dynamical_systems.ipynb
**Blueprint:** outputs/reports/stage4/step1_modeling/ds6_dys_blueprint.md

## Sigma thresholds (FLAG DyS-1, per-period)
- Baseline: 18.6443
- Intervention: 10.7914

## Regime distributions
Baseline:
regime_baseline
stochastic    118
resting        51
growing        37
declining      30

Intervention:
regime_intervention
stochastic    118
resting        95
growing        21
declining       2

## Regime transitions
Participants with valid regime both periods: 230
Staying in the SAME regime: 126 (54.8%)

## InT bridge (regime vs H_emp)
study_period  n_deterministic  n_stochastic  H_emp_mean_deterministic  H_emp_mean_stochastic  t_stat  p_value
    baseline              118           119                    2.9597                 3.1202 -4.8321   0.0000
intervention              118           121                    2.9216                 3.1624 -3.8612   0.0001

## Proxy warning
Regime labels describe patterns in StoP's daily-attempt-count proxy, not directly observed
psychological states (habituation, disengagement, self-control).

## Known limitations
- Deterministic-limit interpretation (sigma->0) is an approximation; DS6's actual process
  has sigma > 0 throughout -- same caveat DS5's DyS notebook carried (FLAG A there).
- Per-period sigma threshold means "deterministic" is relative to that period's own
  distribution, not an absolute cross-period standard -- do not compare eligibility
  proportions across periods as if using the same cutoff value.
- study_condition is quasi-experimental (cohort-level), not individually randomized.

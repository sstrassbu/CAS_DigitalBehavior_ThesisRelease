# DS6 SyD -- Model Run Summary

**Run at:** 2026-08-11 01:22:48
**Notebook:** notebooks/78_ds6_system_dynamics.ipynb
**Blueprint:** outputs/reports/stage4/step1_modeling/ds6_syd_blueprint.md

## Sample
- Prepost-eligible participants (both survey waves + behavioral data): 188

## Loop 1 -- pressure reinforcement (baseline attempt volume -> addiction_index_change)
                        loop            flow                outcome  n_raw   r_raw  p_raw  n_partial  r_partial  p_partial
Loop1_pressure_reinforcement mean_N_baseline addiction_index_change    180 -0.0162 0.8295        180     0.0567     0.4495
Loop1_pressure_reinforcement mu_hat_baseline addiction_index_change    180 -0.0876 0.2425        180    -0.1111     0.1375

## Loop 2 -- self-regulation correction (volume_change -> self_control_index_change)
raw r=0.0774 (p=0.3047, n=178) | partial r=0.0929 (p=0.2174, n=178)

## Condition-level ANOVA (addiction_index_change ~ study_condition)
F=1.225, p=0.2960

## Proxy warning
addiction_index/self_control_index are self-reported psychosocial scales. Loop test results
describe statistical association between behavioral flow and self-reported change, not a
verified mechanistic causal pathway.

## Known limitations
- N=188 (prepost-eligible) — smaller than the full N=243 behavioral sample.
- Regression-to-the-mean confound explicitly tested (raw vs partial correlation) per
  blueprint Part 3 — only the partial (baseline-level-controlled) result is treated as
  evidence for either loop.
- study_condition is quasi-experimental (cohort-level), not individually randomized.
- Only 2 survey waves — this is NOT a repeated weekly panel like Structured's SyD; the
  person-demeaning technique used there does not directly apply (a 2-point series demeaned
  IS the change score, already used as the outcome here).

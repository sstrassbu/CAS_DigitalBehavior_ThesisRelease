# DS4 DyS -- Model Run Summary

**Notebook:** `55_ds4_dynamical_systems.ipynb`  
**Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_dys_blueprint.md`  
**Run date:** 2026-08-11

## Fixed-point validation

- n_valid = 641
- corr(x_mean_raw, mu_hat_OU) = 0.9925
- mean |x_mean_raw - mu_hat_OU| = 0.0108

## Regime split

- theta_hat_OU median = 1.5867
- high_control n = 321
- low_control n = 320

## InT bridge

- corr(theta_hat_OU, H_emp) = -0.1762 -- weak, reported honestly, not a strong cross-validation
- behaviorally_deterministic n = 173

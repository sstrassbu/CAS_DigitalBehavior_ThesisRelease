# DS5 DyS -- Model Run Summary

**Run timestamp:** 2026-08-11 00:26:58
**Notebook:** notebooks/42_ds5_dynamical_systems.ipynb
**Model:** DyS -- Dynamical Systems, sigma->0 deterministic limit (Stage 4 Step 1)
**Dataset:** DS5 -- German Adolescents RCT (N=573 total)

---

## Pipeline parameters

| Parameter | Value |
|---|---|
| MIN_DAYS (inherited from StoP) | 7 |
| MU_THRESHOLD (boundary fp guard) | 0.005 |
| SIGMA_THRESHOLD (sigma->0 partition) | 0.193692 (median sigma_hat) |
| PSYCH_MIN_N | 20 |

## FLAG decisions in effect

| Flag | Decision |
|---|---|
| FLAG 1 | 1D constant-drift discrete map: X_{n+1} = clip(X_n + mu, 0, 1) -- sigma->0 limit of StoP Eq. 19 |
| FLAG 2 | sigma->0 regime: sigma_hat < median(sigma_hat) -- is_dys_eligible flag |
| FLAG 3 | x_mean as empirical resting-state proxy (not analytically derived fixed point) |
| FLAG 4 | Bifurcation analysis and multi-dimensional state space deferred |

## Regime partition (sigma->0, FLAG 2)

| Regime | N | % |
|---|---|---|
| DyS-deterministic (sigma < 0.1937) | 207 | 50.0% |
| StoP-stochastic (sigma >= 0.1937) | 207 | 50.0% |

## Condition-level dynamics summary

| Condition | N | DyS-eligible | mean x_mean | mean mu_hat | frac upper boundary |
|---|---|---|---|---|---|
| control         |  137 |  92 (67%) | 0.8495 | 0.00835 | 0.547 |
| default         |  142 |  42 (30%) | 0.6774 | 0.00841 | 0.570 |
| reintervention  |  135 |  73 (54%) | 0.7573 | 0.00967 | 0.696 |

## Behavioral determinism (DyS-eligible AND H_emp < median)

- N behaviorally deterministic: 149 (36.0% of eligible)
- These participants have low sigma (DyS), low H_emp (InT), and cluster near a boundary resting state.
- Candidate phenotype dimension for Step 2.

## StoP <-> DyS <-> InT bridge

- DyS-eligible ~ H_emp: DyS-det mean H_emp = 1.7834; StoP-stoch mean H_emp = 2.3282
- Lower H_emp in DyS-eligible group confirms InT as information-theoretic model-selection criterion.

## Psychosocial correlates (exploratory, friction-exposed, p < 0.05)

  None nominally significant.

Total tests: 15 (no multiple-comparison correction; exploratory)

## Output files

| File | Description |
|---|---|
| participant_dynamics_parameters.csv | Per-participant DyS classification (414 rows) |
| condition_dynamics_summary.csv | Condition-level DyS statistics (3 rows) |
| dys_stop_int_comparison.csv | Cross-model comparison table |
| psychosocial_dys_correlations.csv | Pearson r of DyS vars vs psychosocial scales |
| figures/fig1_dys_vector_field.png | 1D phase portrait -- mu_hat by condition |
| figures/fig2_dys_resting_state.png | x_mean (empirical resting state) by condition |
| figures/fig3_dys_regime_partition.png | Scatter (mu, sigma): DyS-eligible highlighted |
| figures/fig4_dys_stop_int.png | Three-model comparison: (sigma, H_emp) scatter |

## Proxy warning

All parameters describe the behavioural proxy X_t = n_opened_day / n_events_day.
X_t approximates behavioural override tendency. It does NOT measure urge, self-control, or any latent state.
Predicted boundary fixed points and empirical resting states inherit this limitation.

## DS5 DyS weakness flags (all apply)

- FLAG A: No multi-dimensional state space -- 1D only; no limit cycles, spirals, or chaos
- FLAG B: Trivial fixed points for constant-drift map -- boundary {0,1} only; no interior attractor
- FLAG C: Marginal stability (lambda=1) -- constant-drift Jacobian uninformative for stability
- FLAG D: No continuous bifurcation parameter -- 3 discrete conditions; no bifurcation curve
- FLAG E: Short windows (7-14 days) make individual DyS-eligibility classification noisy
- FLAG F: 'Attractor' terminology qualified throughout -- x_mean is an empirical resting state, not a demonstrated mathematical attractor

## Forward connections

- DyS -> StM (41): DyS fixed points are minima of V(x); Boltzmann bridge P_inf ~ exp(-2V(x)/sigma^2)
- DyS -> DS4 OU: longer windows enable OU convergence rate theta estimation
- DyS -> Phenotyping (100): is_dys_eligible + predicted_boundary_fp + x_mean -> behavioral determinism dimension
- DyS -> Paper: add sigma->0 limit equation, boundary fp note, and marginal stability caveat (see equation gaps table in notebook)

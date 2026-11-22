# DS5 StoP — Model Run Summary

**Run timestamp:** 2026-08-11 00:25:12
**Notebook:** notebooks/43_ds5_stochastic_processes.ipynb
**Model:** Constant-drift SDE (Stochastic Processes, Stage 4 Step 1)
**Dataset:** DS5 — German Adolescents RCT (N=573 total)

---

## Pipeline parameters

| Parameter | Value |
|---|---|
| MIN_DAYS (minimum observation days) | 7 |
| N_TRAJ (simulation trajectories) | 200 |
| MU_THRESHOLD (sigma/|mu| NaN guard) | 0.005 |
| RNG_SEED | 42 |

## FLAG decisions in effect

| Flag | Decision |
|---|---|
| FLAG 1 | Simple constant-drift SDE (not OU/mean-reverting) |
| FLAG 2 | Method-of-moments estimators (mean/std of delta_X_n) |
| FLAG 3 | Option A: drift reduction only (h_c = mu_bar_control - mu_bar_c) |
| FLAG 4 | StM Boltzmann bridge deferred |

## Eligibility after MIN_DAYS=7 threshold

| Condition | N eligible |
|---|---|
| control | 137 |
| default | 142 |
| reintervention | 135 |
| **Total** | **414** |

## Condition-level SDE parameter means

| Condition | mean mu_hat | mean sig_hat | h_c (drift reduction) |
|---|---|---|---|
| control | 0.0084 | 0.1760 | 0.0000 (reference) |
| default | 0.0084 | 0.2611 | -0.0001 |
| reintervention | 0.0097 | 0.2149 | -0.0013 |

## Impulsivity ratio

- sigma/|mu| NaN (|mu| < 0.005): 125 participants (30.2%)

## Output files

| File | Description |
|---|---|
| participant_parameters.csv | Per-participant endpoint drift, OLS drift, raw diffusion, binomial floor/ratio/excess, high-day occupancy, n_days, x_mean |
| condition_summary.csv | Condition-level means, medians, std, h_drift_reduction |
| psychosocial_correlations.csv | Pearson r of SDE params vs FoMO/belonging/ostracism (friction-exposed only) |
| representative_simulations.csv | Observed vs E-M simulation (p10/p50/p90) for representative participants |
| figures/fig1_stop_params_by_condition.png | Violin plots of mu_hat and sig_hat by condition |
| figures/fig2_stop_state_space.png | mu_hat vs sig_hat scatter with quadrant labels |
| figures/fig3_stop_observed_vs_simulated.png | Observed trajectory vs E-M simulation envelope |
| figures/fig4_stop_fomo_vs_params.png | Pre-FoMO vs mu_hat and sig_hat scatter |

## Proxy warning

All parameters describe the behavioral proxy X_t = n_opened_day / n_events_day.
X_t approximates behavioral override tendency. It does NOT measure urge, self-control, or any latent psychological state.

## Known limitations

1. Constant-drift SDE (FLAG 1) — misses non-linear and mean-reverting dynamics
2. Method-of-moments (FLAG 2) — noisy for participants with 7-14 day windows
3. Raw sig_hat is not identified as behavioral diffusion: it contains the binomial sampling floor of daily proportions; use sig_floor_ratio or sig_excess
4. Hard clip boundary [0,1] — reflecting boundary or logit SDE would be more principled
5. Stationarity not formally tested
6. Daily aggregation — within-day sequential structure not captured

## Forward connections

- StoP -> DyS (42): sigma->0 limit reduces SDE to ODE
- StoP -> InT (45): H(P_inf) entropy connects sig_hat to behavioral uncertainty
- StoP -> StM (41): Boltzmann bridge deferred (FLAG 4)
- StoP -> Phenotyping (100): (mu_hat, sig_hat, sigma_mu_ratio) feed directly into Step 2

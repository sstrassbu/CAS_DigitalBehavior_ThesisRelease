# DS5 StM — Model Run Summary

**Run timestamp:** 2026-08-11 00:27:39
**Notebook:** notebooks/41_ds5_statistical_mechanics.ipynb
**Model:** StM -- Statistical Mechanics, behavioral Boltzmann analog (Stage 4 Step 1)
**Dataset:** DS5 -- German Adolescents RCT (N=573 total, 414 StoP-eligible)

---

## Critical structural caveat (FLAG A)

The Boltzmann bridge β_behav = 2/σ̂² is an **approximation**. It would be exact for a
potential-well SDE (dX = −(dV/dx)dt + σ dW). The StoP notebook used the constant-drift SDE
(dX = μ dt + σ dW), which has V(x) = −μx (linear, non-confining). The mapping is a behavioral
analog, not a rigorous thermodynamic derivation. Qualitative ordering is robust; quantitative
values are approximate.

## Pipeline parameters

| Parameter | Value |
|---|---|
| MIN_DAYS (inherited from StoP) | 7 |
| THRESHOLD_USE | 0.5 |
| KDE_BANDWIDTH | silverman |
| KDE_GRID_N | 200 |
| SIGMA_THRESHOLD (from DyS) | 0.181220 |

## FLAG decisions in effect

| Flag | Decision |
|---|---|
| FLAG 1 | Two-state Boltzmann: high-use (X_t > 0.5) vs low-use; single-particle model (J=0) |
| FLAG 2 | β_behav = 2/σ̂² from constant-drift SDE (approximation) |
| FLAG 3 | J = 0: no Ising coupling between DS5 participants |
| FLAG 4 | Phase transition T_c deferred (only 3 discrete conditions) |

## Effective behavioral temperature

| Condition | N | mean β_behav | mean T_behav |
|---|---|---|---|
| control        | 137 | 144.86 | 0.0069 |
| default        | 142 | 43.78 | 0.0228 |
| reintervention | 135 | 84.19 | 0.0119 |

β ordering: control > reintervention > default (consistent with σ̂ ordering from StoP).
Friction conditions raise behavioral temperature (more exploration).

## Two-state model & susceptibility

| Condition | mean χ_behav |
|---|---|
| control        | 6.6469 |
| default        | 5.4946 |
| reintervention | 6.0433 |

## H_StM (condition-level from KDE)

| Condition | H_StM (bits) | H_SDE mean | H_emp mean |
|---|---|---|---|
| control        | -1.342 | -0.644 | 1.652 |
| default        | -0.368 | 0.006 | 2.387 |
| reintervention | -0.720 | -0.344 | 2.118 |

## Four-model convergence

- N four-model convergent: 141 (34.1% of eligible)
- These participants have low σ̂ (StoP), is_dys_eligible (DyS), low H_emp (InT), high β (StM).
- = Thermodynamically ordered, behaviorally entrenched profile.

## Psychosocial correlates (exploratory, friction-exposed, p < 0.05)

  T_behav ~ social_media_wellbeing_pre: r=0.12, p=0.049

Total StM psychosocial tests: 16 (no multiple-comparison correction; exploratory)

## Output files

| File | Description |
|---|---|
| participant_stm_parameters.csv | Per-participant StM quantities (414 rows) |
| condition_stm_summary.csv | Condition-level StM statistics (3 rows) |
| condition_potential.csv | V(x) grid data per condition (600 rows) |
| stm_stop_int_dys_comparison.csv | Four-model cross-model table (414 rows) |
| psychosocial_stm_correlations.csv | Pearson r of StM params vs psychosocial scales |
| figures/fig1_stm_beta_by_condition.png | β_behav and T_behav by condition |
| figures/fig2_stm_puse_chi_by_condition.png | Two-state model: p_use and χ by condition |
| figures/fig3_stm_potential_landscape.png | Condition-level V(x) energy landscape |
| figures/fig4_stm_four_model_comparison.png | Four-model comparison scatter |

## Proxy warning

All parameters describe the behavioral proxy X_t = n_opened_day / n_events_day.
X_t approximates behavioral override tendency. It does NOT measure urge, self-control,
or any latent state. All StM analogs (β, T, V, χ, F) inherit this proxy limitation.

## DS5 StM weakness flags (all apply)

- FLAG A: β_behav = 2/σ̂² is an approximation — constant-drift SDE ≠ potential-well SDE
- FLAG B: Individual V(x) estimation underpowered (7-45 observations); condition-level only
- FLAG C: Thermodynamic equilibrium not established (7-45 day windows; possible transients)
- FLAG D: J = 0 only; no Ising coupling between participants
- FLAG E: No phase transitions or T_c estimation (only 3 discrete conditions)
- FLAG F: No hysteresis (no post-intervention behavioral baseline in DS5)
- FLAG G: Behavioral 'energy' is information-theoretic (surprisal), not physical energy

## Forward connections

- StM -> DS4: OU process has confining potential V(x)=(θ/2)(x-μ)²; β = 2θ/σ² is rigorous
- StM -> Phenotyping (100): β_behav, χ_behav, F_behav as three phenotype dimensions
- StM -> Paper §4.1.1: Add Boltzmann bridge, β_behav, Z_2, χ_behav, H_StM, F_behav equations
- StM -> Unification §4.3: StM closes StoP↔DyS↔InT triangle into four-model quadrangle

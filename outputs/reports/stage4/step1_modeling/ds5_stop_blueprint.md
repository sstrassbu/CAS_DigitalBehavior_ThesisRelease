# DS5 StoP Model — Implementation Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**  
**Written:** 2026-04-16  
**Notebook:** `notebooks/43_ds5_stochastic_processes.ipynb`  
**Producing dataset:** DS5 (German Adolescents RCT, N=573)  
**Model family:** Stochastic Processes (StoP) — constant-drift SDE

---

## Purpose

This document is the companion blueprint for the DS5 StoP implementation. It records the design decisions, the theory-to-data translation, the FLAG decisions in effect, and the outputs produced. It is the primary reference for understanding the notebook and for extending the analysis in future stages.

---

## FLAG decisions in effect

| Flag | Decision | Rationale |
|---|---|---|
| FLAG 1 | Simple constant-drift SDE (not OU) | Lowest-complexity entry point; non-stationarity is acknowledged but tolerated for first pass |
| FLAG 2 | Method-of-moments estimators (mean/std of delta_X_n) | Sufficient precision for first pass; avoids MLE implementation overhead |
| FLAG 3 | Option A — friction as drift reduction only: h_c = mu_bar_control - mu_bar_c | Single-parameter friction effect; sigma unchanged; easiest to interpret |
| FLAG 4 | StM Boltzmann bridge deferred | Requires identifying a non-trivial potential V(x) from data; noted in notebook as forward connection only |

---

## Core model

### SDE (paper Eq. 17)

    dX_t = mu * dt + sigma * dW_t

### Euler-Maruyama discretization (paper Eq. 19, delta_t = 1 *observed* day)

    X_{n+1} = clip(X_n + mu + sigma * Z_n, 0, 1)     Z_n ~ N(0,1) i.i.d.

### State variable

    X_t^(i) = n_opened_day^(i)_t / n_friction_events_day^(i)_t   in [0, 1]

**PROXY WARNING:** X_t is a count-based behavioral measurement. It approximates behavioral override tendency. It does NOT directly measure urge, self-control capacity, habit strength, or any latent psychological state. All SDE parameters inherit this limitation.

### Parameter estimators (FLAG 2)

    mu_hat^(i)  = mean(delta_X_n^(i))       for n = 1..T_i-1
    sig_hat^(i) = std(delta_X_n^(i), ddof=1)

Minimum threshold: T_i >= 7 days.

**Telescoping caveat:** mean(delta_X_n) is algebraically identical to (X_last - X_first) / (T_i - 1) — verified across all 414 eligible participants to 1.7e-17. mu_hat therefore uses only the first and last observed daily override rate; every intermediate day is discarded, and its effective sample size is 1, not T_i - 1. Endpoint days are often thin: the first observed day has exactly 1 friction event for 23 participants, the last observed day for 59, and 135/414 participants have at least one endpoint day with <= 2 events. Consequently the null mu_hat ANOVA (F=0.299, p=0.742) and the h_c values must be read as statements about estimator power, not as evidence that friction had no drift effect; and sigma_mu_ratio (NaN for 129/414 = 31.2%) largely encodes whether the first and last observed day happened to have similar override rates. Figure 3 is a descriptive illustration, not a validation: simulating from x0 = X_first with mu = (X_last - X_first)/(T_i - 1) lands the unclipped median trajectory on X_last by construction.

### Friction effect (FLAG 3 Option A)

    h_c = mu_bar_control - mu_bar_c     for c in {control, default, reintervention}
    h_control = 0 by definition

---

## Theory-to-data mapping

| Theoretical quantity | Data source | Column | Proxy limitation |
|---|---|---|---|
| State variable X_t | `ds5_behavioral_clean.csv` | Computed: n_opened / n_events per (participant, day) | Override rate only; not latent urge |
| Time t | `ds5_behavioral_clean.csv` | `event_date` (calendar day) | Daily aggregation; ignores intra-day structure |
| Drift mu | Computed from daily X_t | mean(delta_X_n) | Direction of behavioral change; not motivation |
| Diffusion sigma | Computed from daily X_t | std(delta_X_n, ddof=1) | Context noise + measurement error confounded |
| Experimental condition | `ds5_survey_features.csv` | `study_condition` | Must be joined (not in behavioral file) |
| Friction effect h_c | Computed from condition means | mu_bar_ctrl - mu_bar_c | Population-level; individual heterogeneity not captured |
| sigma/|mu| ratio | Derived from parameters | sig_hat / abs(mu_hat) | NaN for |mu_hat| < 0.005 |
| FoMO, belonging, ostracism | `ds5_survey_features.csv` | `fomo_mean_pre`, `belong_mean_pre`, `ostracism_mean_pre` | Pre-intervention; validated scales |

---

## Data pipeline

### Sources

| File | Role |
|---|---|
| `outputs/cleaned/ds5_behavioral_clean.csv` | Event-level behavioral data (288,688 rows) |
| `outputs/features/ds5/ds5_survey_features.csv` | study_condition, psychosocial scales (join key) |
| `outputs/features/ds5/ds5_behavior_features.csv` | Stage 1 aggregate features (sanity check only) |

### Key pipeline steps

1. Load behavioral file; parse `event_timestamp_utc` to datetime; extract `event_date`
2. Join `study_condition` from survey features (left join on `participant_id_canonical`)
3. Filter to `event_outcome_simple` in {opened, dismissed, closed}; add `opened_flag`
4. Aggregate to daily: `n_opened`, `n_events`, `X_t = n_opened / n_events`
5. Apply MIN_DAYS = 7 threshold (eligible: ~72% of participants)
6. Estimate `(mu_hat, sig_hat)` per participant via `estimate_sde_params()`
7. Compute `sigma_mu_ratio` (NaN if |mu_hat| < 0.005)
8. Condition comparison: `cond_stats`, h_drift_reduction, ANOVA, Welch t-tests
9. Euler-Maruyama simulation for representative participants (one per condition)
10. Psychosocial correlations (friction-exposed conditions only)
11. Export `participant_parameters.csv`

### DS5 structural notes (required reading)

- `study_condition` is NOT in `ds5_behavioral_clean.csv` — must join from survey features
- `is_intervention_event` is 0 for ALL DS5 events — do not use for filtering
- Control group is NOT friction-free: rate_opened_control ~= 0.763 — X_t is well-defined for all three conditions
- One participant has no pre-survey record (NaN condition after join) — expected

---

## Outputs

**Output directory:** `outputs/model_outputs/stochastic_processes/`  
**Figures directory:** `outputs/model_outputs/stochastic_processes/figures/`

| File | Description |
|---|---|
| `participant_parameters.csv` | Per-participant SDE parameter estimates; one row per eligible participant |
| `condition_summary.csv` | Condition-level means, medians, std, h_drift_reduction |
| `psychosocial_correlations.csv` | Pearson r of SDE params vs FoMO/belonging/ostracism (friction-exposed only) |
| `representative_simulations.csv` | Observed vs E-M simulation (p10/p50/p90) for representative participants |
| `model_run_summary.md` | Pipeline parameters, FLAG decisions, eligibility counts, key results |
| `figures/fig1_stop_params_by_condition.png` | Violin plots of mu_hat and sig_hat by condition |
| `figures/fig2_stop_state_space.png` | mu_hat vs sig_hat scatter; all participants; colored by condition |
| `figures/fig3_stop_observed_vs_simulated.png` | Observed trajectory vs E-M simulation envelope; one panel per condition |
| `figures/fig4_stop_fomo_vs_params.png` | FoMO (pre-intervention) vs mu_hat and sig_hat scatter; friction-exposed only |

### Actual results (2026-04-17 run)

**Eligibility:** 414 / 568 outcome-bearing participants eligible (72.9%, MIN_DAYS=7) = 414 / 573 enrolled (72.3%). Five participants are removed before the MIN_DAYS gate and are not reported by the notebook: 4 have no events with outcome in {opened, dismissed, closed} (cell 5 filter), and 1 test account (`test-<participant-id>`) is silently dropped by the cell 6 groupby because its study_condition is NaN. Control=137, Default=142, Reintervention=135.

**Condition-level SDE parameter means:**

| Condition | mean mu_hat | mean sig_hat | h_c |
|---|---|---|---|
| control | +0.0068 | 0.172 | 0.000 (reference) |
| default | +0.0074 | 0.245 | −0.0006 |
| reintervention | +0.0084 | 0.200 | −0.0016 |

**Interpretation note:** h_c values are slightly negative for friction conditions, meaning friction conditions have marginally higher drift than control. Effect sizes are negligible (|h_c| ~0.001) relative to the within-condition SD of mu_hat (0.0174 control / 0.0171 default / 0.0182 reintervention). The sig_hat ordering (default 0.245 > reintervention 0.200 > control 0.172) must NOT be read as friction disrupting behavioral regularity. X_t is a daily proportion whose sampling variance is p(1-p)/n_events, and the analytic per-participant binomial noise floor sqrt(mean_n[p(1-p)/n_t + p(1-p)/n_{t+1}]) averages 0.251 (default), 0.212 (reintervention) and 0.179 (control) — i.e. the observed sig_hat sits at or below the pure sampling-noise floor in every arm (median observed/floor = 0.96; 57% of participants fall below their own floor). Default participants simply have fewer friction events per day (15.4 vs control 21.8) and an x_mean closer to 0.5 (0.618 vs 0.783), both of which mechanically inflate Var(delta_X). Controlling for the floor removes the condition effect entirely: ANOVA on sig_hat/floor gives F=0.80, p=0.450 (raw sig_hat: F=16.54, p=1.2e-07), and OLS sig_hat ~ floor + condition gives floor +0.922 (t=33.5), default +0.0065 (p=0.349), reintervention −0.0026 (p=0.698) — against default +0.0734 (p=2.3e-08) and reintervention +0.0283 (p=0.030) without the floor covariate. Report sig_hat as a composite of behavioral volatility and daily-denominator sampling noise; a behavioral variability claim requires the excess ratio sig_hat/sig_floor or sig_excess = sqrt(max(var_obs - var_floor, 0)).

**Psychosocial (exploratory, 8-test family, no result survives correction):** 8 Pearson correlations were run (2 targets x 4 predictors, n=277 each). The two smallest nominal p-values are FoMO ~ sig_hat r=−0.13, p=0.036 and FoMO ~ mu_hat r=−0.12, p=0.047; neither survives Bonferroni (alpha = 0.05/8 = 0.00625) or Benjamini-Hochberg FDR at q=0.05 (rank-1 threshold 0.00625, rank-2 threshold 0.0125). The two are also non-independent, since mu_hat and sig_hat are estimated from the same increment vector. Belonging, ostracism and digital_wellbeing are non-significant even nominally (p = 0.51–0.91). No psychosocial association should be reported as a discovered result.

**Sanity check:** |x_mean − rate_opened| mean=0.030, max=0.246, >0.20: 3 participants (0.7%). Acceptable.

**Impulsivity ratio:** 31.2% of participants have |mu_hat| < 0.005 threshold → sigma_mu_ratio NaN.

### Column reference: participant_parameters.csv

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier |
| `study_condition` | str | RCT condition (control / default / reintervention) |
| `n_days` | int | Number of distinct observation days (>= MIN_DAYS = 7) |
| `n_increments` | int | Number of delta_X_n increments used for estimation (= n_days - 1) |
| `x_mean` | float | Mean of daily X_t values (cross-reference check against rate_opened) |
| `mu_hat` | float | Estimated drift (method of moments) |
| `sig_hat` | float | Estimated diffusion (method of moments) |
| `sigma_mu_ratio` | float | sig_hat / abs(mu_hat); NaN if abs(mu_hat) < 0.005 |

---

## Equation gaps resolved vs deferred

| Gap | Status | Resolution |
|---|---|---|
| Continuous SDE to discrete daily series | Partial | Euler-Maruyama with delta_t = 1 *observation step* (FLAG 1); increments are taken over the index of observed days, not calendar days — 520/13,803 increments (3.8%) span >1 calendar day, affecting 154/414 participants (max gap 28 days) |
| Parameter estimation method | Resolved | Method of moments (FLAG 2) |
| Friction parametrization | Resolved | Drift reduction only (FLAG 3A) |
| Boundary behavior at X_t = 0 or 1 | Partial | Hard clip; reflecting boundary deferred |
| Stationarity formal test | Deferred | Acknowledged as limitation; longer windows (DS4) would make this tractable |
| Boltzmann/StM connection | Deferred (FLAG 4) | Requires non-trivial V(x) from data |
| Time-varying drift | Deferred | Natural extension to OU or potential-well SDE |
| Two-component friction effect (mu AND sigma) | Deferred | FLAG 3A defers this; natural extension in Step 2 |

---

## Known limitations

1. **Constant-drift SDE** misses non-linear and mean-reverting behavioral dynamics
2. **Method-of-moments** is noisy for participants with short windows (7-14 days)
3. **h_c measures population-level drift shift** — individual friction response heterogeneity is averaged out
4. **Daily aggregation** collapses within-day sequential structure
5. **sigma_mu_ratio** is undefined for participants with near-zero drift (NaN)
6. **Control group is included** in parameter estimation — their mu_hat reflects baseline behavioral dynamics, not friction response; this is appropriate for the h_c computation but should be noted when interpreting control-group parameter distributions
7. **mu_hat is a two-point statistic.** mean(delta_X_n) telescopes to (X_last - X_first)/(T_i - 1), so the drift estimate has effective sample size 1 and is dominated by endpoint measurement noise; an OLS slope of X_t on calendar day would use all observations and is the recommended robustness comparison.
8. **delta_t is one *observed* day, not one calendar day.** Days with no friction events are absent from the series (not zero-filled), so np.diff() steps over an observation index. 520 of 13,803 increments (3.8%) span more than one calendar day and 154 of 414 participants (37%) are affected; span_days/(n_days-1) has mean 1.136 and reaches 5.86, so an individual mu_hat can overstate a true per-calendar-day drift by up to ~6x, and a 28-day gap contributes a much larger-variance increment to the ddof=1 std with no reweighting. Condition-level conclusions are unaffected (per-day mu ANOVA F=0.356, p=0.701 vs index-based F=0.299, p=0.742; Spearman between the two versions 0.985), but the per-participant mu_hat and sigma_mu_ratio values fed into phenotyping (nb100/nb63) inherit the distortion.

---

## Forward connections

| Connection | Mechanism | Target notebook |
|---|---|---|
| StoP -> DyS | sigma -> 0 limit reduces SDE to ODE | 42_ds5_dynamical_systems.ipynb |
| StoP -> InT | sig_hat characterizes entropy of stationary distribution | 45_ds5_information_theory.ipynb |
| StoP -> StM (deferred) | Boltzmann distribution from potential-well SDE | Future Stage 4 Step 2 |
| StoP -> Phenotyping | (mu_hat, sig_hat, sigma_mu_ratio) as phenotype dimensions | 100_phenotype_exploration.ipynb |

---

## How to load the output

```python
import pandas as pd
from pathlib import Path

params = pd.read_csv(
    Path('outputs/model_outputs/stochastic_processes/participant_parameters.csv')
)
# n rows = eligible participants (n_days >= 7)
# join back to survey features for psychosocial correlates
```

# Stage 4 — Implementation Plan: Theoretical and Conceptual Modeling

**Written:** 2026-04-16  
**Purpose:** Master planning document for Stage 4. Records all design decisions, model family ordering, FLAG system, dataset strategy, and cross-notebook connections. This document is the authoritative reference for Stage 4 implementation continuity.

**⚠ Status note (added 2026-08-07):** This document's "Stage 4 progress log" and dataset
sequencing sections below describe project state as of 2026-04-17 — DS5 Step 1 only. Stage 4
has since expanded far beyond this: DS5 Step 1+2 plus a full `_v2` revision arc are complete
(GaT/ABM corrected above; see `outputs/reports/planning/ds5_02_branch_blueprint.md`); DS4 has
all 8 CAS model families implemented (`outputs/reports/stage4/step1_modeling/ds4_*_blueprint.md`,
notebooks 51–57, 59); DS6 Step 1 (7 families) and Step 2 are both complete
(`outputs/reports/stage4/ds6_step1_plan.md`, notebooks 71–75/78, 140–141); an entire separate
Structured dataset category (all 8 families + phenotyping) and a Stanford Health physiology
dataset have also been added. **For current project status, read `CLAUDE.md` in full** — this
file's FLAG system, universal proxy warning, and model notebook template guidance below remain
valid and reusable, but its progress log and "current position" framing do not reflect current
state and should not be read as up to date.

---

## Stage 4 definition

Stage 4 implements CAS model families on the real datasets. It is divided into three steps:

| Step | Name | Scope |
|---|---|---|
| **Step 1** | Theoretical and Conceptual Modeling | One model family per notebook, per dataset. Pure model implementation. No phenotyping, no personalization. Establish parameter estimates and cross-condition comparisons. |
| **Step 2** | Phenotyping | Use Step 1 parameter estimates as features for behavioral subgroup discovery. Notebooks 100_phenotype_exploration.ipynb and 200_personalization_exploration.ipynb. |
| **Step 3** | Personalization | Intervention matching based on phenotype profiles. Not started. |

**Current position: Stage 4, Step 1.**

---

## Dataset implementation sequence

Established in Stage 3 (`recommended_first_modeling_pass.md`):

| Order | Dataset | Why |
|---|---|---|
| **1. DS5** | German adolescents RCT, N=573 | Only RCT; validated psychosocial scales; clean friction outcomes; widest model family fit |
| **2. DS4** | Long-run OneSec users, N=1039 | Best longitudinal adaptation signal (897-day windows); habit modeling |
| **3. DS6** | Danish adolescents quasi-exp, N=243 | Substitution dynamics (via app_prev/app_next2 — group_id session structure verified non-functional 2026-08-05); repeated psychosocial waves |
| **4. DS1** | Self-selected OneSec users, N=619 | Simplest structure; cleanest friction denominator; cross-dataset reference |

---

## CAS model families — 8 families from paper

| Abbrev | Full name | Paper section | DS5 notebook | Status |
|---|---|---|---|---|
| **StM** | Statistical Mechanics | §4.1.1 | 41_ds5_statistical_mechanics.ipynb | **COMPLETE (Step 1)** |
| **DyS** | Dynamical Systems | §4.1.2 | 42_ds5_dynamical_systems.ipynb | **COMPLETE (Step 1)** |
| **StoP** | Stochastic Processes | §4.1.3 | 43_ds5_stochastic_processes.ipynb | **COMPLETE (Step 1)** |
| **NeT** | Network Models | §4.1.4 | 44_ds5_network_models.ipynb | **COMPLETE (Step 1)** |
| **InT** | Information Theory | §4.1.5 | 45_ds5_information_theory.ipynb | **COMPLETE (Step 1)** |
| **GaT** | Game Theory | §4.1.6 | 46_ds5_game_theory.ipynb | **COMPLETE (2026-08-06, DS5_02 Phase C)** — see progress log |
| **ABM** | Agent-Based Modeling | §4.1.7 | 47_ds5_agent_based.ipynb | **COMPLETE (2026-08-06, DS5_02 Phase C)** — see progress log |
| **SyD** | System Dynamics | §4.1.8 | 48_ds5_system_dynamics.ipynb | Placeholder — still deferred for DS5 (requires repeated survey waves); implemented for DS6 as notebook 78 (complete) |

### Recommended implementation order for DS5 (Step 1)

1. **StoP** (43) — ✅ Complete. Establishes state variable X_t, drift μ̂, diffusion σ̂
2. **InT** (45) — Directly connected to StoP via entropy of stationary distribution
3. **DyS** (42) — Directly connected to StoP via σ→0 limit
4. **StM** (41) — Boltzmann bridge requires V(x) from data; after DyS/StoP
5. **NeT** (44) — Requires sequence engineering (app_next/prev for DS5); after StoP
6. **GaT** (46) — Strategic friction interaction framing; after behavioral profiles established
7. **ABM** (47) — Needs well-characterized agent parameters from simpler models first
8. **SyD** (48) — Needs repeated survey waves (DS5 has only pre+post; defer to DS6)

---

## FLAG system — design decisions recorded before implementation

The FLAG system records simplifying choices made before implementation. Each flag has a default (simplest defensible option) that can be upgraded in later iterations without changing the conceptual framing.

### Flags currently in effect for DS5 StoP (notebook 43)

| Flag | Default used | Alternative (deferred) | Why deferred |
|---|---|---|---|
| FLAG 1 | Constant-drift SDE: dX_t = μ dt + σ dW_t | OU process: dX_t = θ(μ−X_t)dt + σ dW_t | Mean-reversion adds a third parameter; better for DS4 long windows |
| FLAG 2 | Method-of-moments: μ̂ = mean(ΔX), σ̂ = std(ΔX) | Maximum likelihood estimation | MLE more efficient for short windows; implement as upgrade in Step 2 |
| FLAG 3 | Drift reduction only: h_c = μ̂_ctrl − μ̂_c | Two-component effect (both μ and σ shift) | More defensible to start with single-parameter effect |
| FLAG 4 | StM Boltzmann bridge deferred | P_inf(x) ∝ exp(−2V(x)/σ²) | Requires identifying non-trivial V(x) from empirical P(X_t) |

### FLAG template for future model notebooks

When starting a new model notebook, document flags as follows before writing code:

```
FLAG 1: [Core model simplification vs extension]
FLAG 2: [Estimation method simplification]  
FLAG 3: [Effect/intervention parametrization]
FLAG 4: [Forward connection or bridge deferred]
```

---

## Universal proxy warning

**This applies to every model notebook in Stage 4.**

The state variable X_t in DS5 (and equivalent behavioral proxies in other datasets) is a **count-based behavioral measurement, not a directly observed latent psychological state.**

    X_t = n_opened_day / n_friction_events_day   in [0, 1]

X_t approximates behavioral override tendency. It does NOT directly measure:
- Urge or craving intensity
- Self-control capacity  
- Habit strength
- Attentional load
- Any latent cognitive/psychological state

All model parameters (μ̂, σ̂, entropy, transition probabilities, etc.) inherit this proxy limitation. **Every figure title and interpretation section must acknowledge this.** This is a thesis requirement, not optional documentation.

---

## DS5 structural notes — critical for all DS5 notebooks

These findings were confirmed in Stage 1 QC and must be respected in every DS5 implementation:

### 1. study_condition is NOT in ds5_behavioral_clean.csv

Must join from `ds5_survey_features.csv` (column: `study_condition`, source: `cond`).  
One participant (0.2%) has no pre-survey record — gets NaN condition after join.  
Reference: `data_docs/modeling_cautions.md §6`.

### 2. is_intervention_event = 0 for ALL DS5 events

Unlike DS4 (which has a three-class event architecture), DS5 does not use `is_intervention_event` as a meaningful filter. Do NOT use it to select friction events. Instead, filter on `event_outcome_simple` in {opened, dismissed, closed}.

### 3. Control group is NOT friction-free

DS5 control participants produce dismissed and closed outcomes.  
`rate_opened_control ≈ 0.763` (not 1.0).  
This means X_t is **well-defined and informative for all three conditions**, including control.  
For friction-specific cross-condition analysis: the control group's X_t reflects baseline behavioral dynamics (not intervention effect), which is exactly what makes the h_c computation valid.

### 4. Valid friction outcomes

Use: `event_outcome_simple` in {**opened**, **dismissed**, **closed**}  
Exclude: `missing`, `dismissed_other`

### 5. Condition distribution (from Stage 1 survey features)

- control: ~46 participants (~8%)
- default: ~263 participants (~46%)
- reintervention: ~263 participants (~46%)

Exact counts depend on filter applied.

### 6. MIN_DAYS threshold for time-series models

`MIN_DAYS = 7` → approximately 72% of DS5 participants eligible for SDE-type estimation.  
Participants with fewer days get NaN parameters — do not impute.

---

## StoP model — key implementation details (notebook 43)

### Core equations (FLAGS applied)

    State variable: X_t^(i) = n_opened_day / n_events_day  in [0,1]
    
    Increment:  delta_X_n = X_{n+1} - X_n
    
    mu_hat  = mean(delta_X_n)          [FLAG 2: method of moments]
    sig_hat = std(delta_X_n, ddof=1)
    
    Simulation: X_{n+1} = clip(X_n + mu + sigma*Z_n, 0, 1)   Z_n ~ N(0,1)
    
    Friction effect: h_c = mu_bar_control - mu_bar_c          [FLAG 3A]
    
    Impulsivity ratio: sigma/|mu|  (NaN if |mu_hat| < 0.005)

### Outputs

**Output root:** `outputs/model_outputs/stochastic_processes/`

| File | Description |
|---|---|
| `participant_parameters.csv` | Per-participant: mu_hat, sig_hat, sigma_mu_ratio, n_days, x_mean |
| `condition_summary.csv` | Condition-level means, medians, std, h_drift_reduction |
| `psychosocial_correlations.csv` | Pearson r vs FoMO/belonging/ostracism/digital_wellbeing |
| `representative_simulations.csv` | Observed + E-M simulation summary (p10/p50/p90) per representative |
| `model_run_summary.md` | Reproducible run record with key results embedded |
| `figures/fig1_stop_params_by_condition.png` | Violin plots of mu_hat and sig_hat by condition |
| `figures/fig2_stop_state_space.png` | mu_hat vs sig_hat scatter per participant |
| `figures/fig3_stop_observed_vs_simulated.png` | Observed trajectory vs E-M simulation |
| `figures/fig4_stop_fomo_vs_params.png` | FoMO vs mu_hat and sig_hat |

**Actual results (2026-04-17):** 414/573 eligible. mu_hat near-zero across all conditions (~0.007). Condition drift differences negligible (|h_c| ~0.001). sig_hat higher in friction conditions (default 0.245 > reintervention 0.200 > control 0.172), but this ordering matches each arm's binomial sampling-noise floor for the daily proportion X_t (0.251 / 0.212 / 0.179) and disappears once the floor is controlled (ANOVA on sig_hat/floor F=0.80, p=0.450) — it is NOT evidence that friction disrupts behavioral regularity. FoMO ~ mu_hat: r=−0.12, p=0.047 (exploratory, n=277).

### Sanity check

`x_mean` (time-averaged daily X_t per participant) should approximately match `rate_opened` from `ds5_behavior_features.csv`. Small differences expected due to daily-average vs event-average weighting. Differences > 0.20 warrant investigation.

---

## Unification map — model family connections

This is the theoretical glue between model families. Each connection is either implementable immediately, or deferred to a later stage.

```
                        StoP (43)
                       /   |    \
            σ→0       /    |     \   entropy of P_inf
                     /     |      \
                  DyS(42)  |      InT(45)
                           |
                    FLAG 4 (deferred)
                           |
                          StM(41)   ←  Boltzmann: P_inf(x) ∝ exp(-2V(x)/σ²)
```

| Connection | Mechanism | Status |
|---|---|---|
| StoP → DyS | When σ→0, SDE reduces to ODE dX/dt = μ; low-σ participants are DyS targets | Deferred to notebook 42 |
| StoP → InT | Entropy H(P_inf) of stationary distribution connects diffusion to behavioral uncertainty | Deferred to notebook 45 |
| StoP → StM | Potential-well SDE gives Boltzmann P_inf — connects thermodynamic cost to friction | FLAG 4 deferred; requires V(x) from data |
| StoP → Phenotyping | (μ̂, σ̂, σ/|μ|) are candidate phenotype dimensions | Stage 4 Step 2 (notebook 100) |
| DyS → NeT | Fixed points of DyS maps to stable behavioral attractors in network structure | Future DS6 |
| InT → NeT | App entropy connects to network centralization (Herfindahl, entropy measures) | Already in Stage 1 features |

---

## Model notebook template

A reusable template for all future model notebooks is at:

    notebooks/00_model_notebook_template.ipynb

**Always copy this template** when starting a new model notebook. It enforces:
- Scope statement (goal / not goal / output)
- FLAG decisions table
- Proxy warning cell
- Theory section before any code
- Theory-to-data mapping table
- Equation gaps table
- Sanity check cell
- Interpretation and limits section
- Forward connections section

---

## Pre-implementation checklist (for every new model notebook)

Before writing any code in a new model notebook:

- [ ] Read `data_docs/modeling_cautions.md` section for the target dataset
- [ ] Confirm which features are Tier A/B/C for cross-dataset use (if applicable)
- [ ] Document all FLAG decisions in the notebook header before coding
- [ ] Define the state variable and write the proxy warning explicitly
- [ ] Fill the theory-to-data mapping table
- [ ] Write the equation gaps table
- [ ] Confirm study_condition join for DS5/DS6 behavioral files
- [ ] Apply dataset-specific outcome filter (DS5/DS1: all outcomes; DS4: intervention_event class; DS6: opened only — no override/compliance distinction)
- [ ] Apply minimum data threshold (MIN_DAYS = 7 for time-series models)

---

## Cross-dataset notes for future model passes

These must be respected when extending Step 1 notebooks beyond DS5:

| Dataset | Key caution |
|---|---|
| DS4 | Event class distinction: use `intervention_event` class only for friction-specific analysis; `rate_opened_intervention_events` not `rate_opened` |
| DS4 | `obs_window_days_ds4` removed in QC (duplicate of obs_window_days) — do not reference |
| DS6 | ALL events have `event_outcome_simple == 'opened'` — no override/compliance distinction at event level |
| DS6 | Use `event_rate_ratio_intervention_vs_baseline` as behavioral response proxy (not friction override rate) |
| DS6 | Filter to `n_baseline_days >= 7` before using behavioral response ratio |
| DS6 | `self_transition_rate` and `cross_app_transition_rate` were near-constant (mean=0.989) only when computed on the buggy `app_next` field; recomputed on `app_prev` 2026-08-06 (mean=0.512, sd=0.217) — now genuinely usable individual-difference features |
| DS1 | `secondsSinceOneSecSetup` is 18.9% NaN — adaptation features are restricted to 81.1% of events |
| DS1 | Timestamps assumed UTC; local-time behavioral patterns may be shifted |

---

## Stage 4 progress log

| Date | Notebook | Model | Status | Notes |
|---|---|---|---|---|
| 2026-04-16 | 43_ds5_stochastic_processes.ipynb | StoP | Complete (Step 1) | FLAG 1–4 applied; outputs in outputs/model_outputs/stochastic_processes/ |
| 2026-04-17 | 43_ds5_stochastic_processes.ipynb | StoP | Debugged + full re-run | Fixed datetime.date TypeError; added all output files; 414 eligible; results documented |
| 2026-04-17 | 45_ds5_information_theory.ipynb | InT | **Complete (Step 1)** | 5 entropy dimensions; H_SDE bridge r=0.65 vs H_emp; H_out by condition; FoMO ~ H_SDE r=-0.13; outputs in outputs/model_outputs/information_theory/ |
| 2026-04-17 | 42_ds5_dynamical_systems.ipynb | DyS | **Complete (Step 1)** | σ→0 regime partition (σ<0.1812); control 64% DyS-eligible vs default 29%; 154 behaviorally deterministic (37%); DyS-det H_emp=1.75 vs StoP H_emp=2.32; closes StoP↔InT↔DyS triangle; outputs in outputs/model_outputs/dynamical_systems/ |
| 2026-04-17 | 41_ds5_statistical_mechanics.ipynb | StM | **Complete (Step 1)** | β_behav=2/σ̂² (⚠ approx); condition V(x) via KDE; χ_behav; four-model convergence (154 participants, 37.2%); H_StM≈H_SDE; FLAG A (constant-drift ≠ potential-well SDE) documented throughout; outputs in outputs/model_outputs/statistical_mechanics/ |
| 2026-04-17 | 44_ds5_network_models.ipynb | NeT | **Complete (Step 1)** | Sequence-engineered temporal-succession networks; HHI_net/H_trans/rho_self/π; InT-NeT bridge I=H_app-H_trans verified (r=0.945); 463/569 NeT-eligible (81.4%); 378 stat-eligible (66.4%); outputs in outputs/model_outputs/network_models/ |
| 2026-08-06 | 46_ds5_game_theory.ipynb | GaT | **Complete (Step 1, DS5_02 Phase C)** | commitment_score=rate_not_opened (FLAG G1: behavioral proxy, not utility); strong condition effect (ANOVA F=40.99, p<0.001); null phenotype effect; outputs in outputs/model_outputs/game_theory/ |
| 2026-08-06 | 47_ds5_agent_based.ipynb | ABM | **Complete (Step 1, DS5_02 Phase C)** | SDE agent validation using individual StoP params (FLAG AB1: validates StoP, not an independent model); gate FAILS (ρ=0.428 vs 0.80 threshold) — genuine structural finding, reported honestly not resolved; outputs in outputs/model_outputs/agent_based/ |
| — | 48_ds5_system_dynamics.ipynb | SyD | Not started (DS5) | Still deferred for DS5 (needs repeated survey waves); implemented and complete for DS6 as notebook 78 |

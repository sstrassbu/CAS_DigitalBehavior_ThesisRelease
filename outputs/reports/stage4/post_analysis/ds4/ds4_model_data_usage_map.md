# Model and Path Data Usage Map — DS4

**Written:** 2026-08-08
**Overlap check:** Read in full before drafting — `outputs/reports/stage4/post_analysis/model_data_usage_map.md` (DS5 template this document mirrors in structure), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` (cross-dataset synthesis; not duplicated here), `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md`, `outputs/reports/stage4/cross_dataset_implementation_strategy.md`, `outputs/reports/stage4/stage4_implementation_plan.md`. This document is scoped to DS4 alone — a dataset-level deep dive on data provenance for every DS4 model family and Step 2 path, not a repeat of the cross-dataset comparison in those files.
**Purpose:** Clarify for every implemented DS4 model and Step 2 path exactly which data sources were used — behavioral events, survey (single-wave, qualitative), or previous model outputs.

---

## Overview: data sources available for DS4

| Data source | File | N | Primary content |
|---|---|---|---|
| Behavioral events | `outputs/cleaned/ds4_behavioral_clean.csv` | 2,490,260 events, 1,039 participants | Event-level: participant ID, timestamp, app, event class (`intervention_event`/`app_close_event`/`no_intervention`), outcome |
| Stage 1 behavior features | `outputs/features/ds4/ds4_behavior_features.csv` | 1,039 | Aggregated participant-level behavioral summaries (volume, outcome rates by class, app structure, calendar-time adaptation) |
| Survey (single wave, post-use, qualitative only) | `outputs/features/ds4/ds4_survey_features.csv` (from `outputs/cleaned/ds4_survey_clean.csv`) | 283 (of 299 survey respondents; 756 behavioral participants have no survey) | Demographics (`survey_age`, `gender_clean`) + qualitative-text availability flags; **no Likert/psychometric scales, no pre-survey, no condition variable** |
| Model outputs | `outputs/model_outputs/ds4_*/` | Varies | Per-participant model parameters (all 7 implemented families) |

**Structural fact that shapes every table below:** DS4 has no experimental condition (self-selected, naturalistic usage) and no repeated survey waves (one post-use survey, qualitative only — see `ds4_deferred_models_rationale.md` for why this excludes SyD). Every "what came from survey data" row below is therefore either empty or restricted to a thin demographic overlay — this is the single biggest structural difference from DS5's usage map, where `study_condition` was an essential join for nearly every model family and path.

---

## Step 1 Model Implementations

### StoP — Stochastic Processes (notebook 53)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds4_behavioral_clean.csv` | `participant_id_canonical`, `timestamp_utc`, `intervention_event_class` (filtered to `intervention_event`), `event_outcome_simple` (filtered to `{opened, dismissed}`) |

**What was derived from behavioral data:**
- Daily state variable `X_t = n_opened / n_events` (intervention_event class only) → entirely behavioral
- `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU`, `tau_hat` (OU fit via closed-form AR(1) OLS on consecutive-day pairs) → entirely behavioral

**What came from survey data:** Nothing. No condition to join (DS4 has none); no psychosocial overlay attempted at the StoP stage.

**Verdict:** Parameters are **purely behavioral-derived**, with no survey input at all — a stronger claim than DS5's StoP, which at least joined `study_condition` for stratification.

---

### InT — Information Theory (notebook 52)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds4_behavioral_clean.csv` | Event-level data for `H_out_intervention`, `H_out_all_classes`, `MI(intervention_type;outcome)` |
| Stage 1 behavior features | `ds4_behavior_features.csv` | `app_entropy` (→ `H_app`), `hour_entropy` (→ `H_hour`) |
| Previous model outputs | `ds4_stochastic_processes/participant_parameters.csv` | `sigma_hat_OU`, `theta_hat_OU` (→ exact `H_SDE`), `mu_hat_OU` (redundancy check) |

**What was derived from behavioral data:**
- `H_out_intervention`, `H_out_all_classes` (Shannon entropy of outcome PMFs) → behavioral
- `H_app`, `H_hour` (reused from Stage 1 features) → behavioral
- `H_emp` (K=10 binned entropy of daily `X_t`, rebuilt via StoP's own construction) → behavioral
- `MI(intervention_type; outcome)` → behavioral (DS4-unique — 6 logged intervention types)

**What came from previous model outputs:**
- `sigma_hat_OU`/`theta_hat_OU` from StoP → exact OU stationary-distribution entropy `H_SDE`

**What came from survey data:** Nothing.

**Verdict:** **Entirely behavioral**, with one internal bridge dependency on StoP's own behavioral output. No survey input anywhere in this notebook.

---

### DyS — Dynamical Systems (notebook 55)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `ds4_stochastic_processes/participant_parameters.csv` | `mu_hat_OU` (=X*), `theta_hat_OU`, `fit_valid` |
| InT model outputs | `ds4_information_theory/participant_entropy_metrics.csv` | `H_emp` (for the InT bridge) |
| Behavioral events (indirect) | Rebuilt daily `X_t` for the fixed-point validation check (`x_mean_raw` vs `mu_hat_OU`) | Same construction as StoP §5 |

**What was derived:**
- `regime_label` (`high_control`/`low_control`, θ̂ median split) → from StoP output
- `fixed_point_deviation = |x_mean_raw − mu_hat_OU|` → from a fresh behavioral rebuild compared against StoP
- `behaviorally_deterministic` (regime AND low H_emp) → from StoP + InT

**What came from survey data:** Nothing.

**Verdict:** **Entirely derived from StoP + InT outputs**, plus one behavioral rebuild for validation. No survey data anywhere.

---

### StM — Statistical Mechanics (notebook 51)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `ds4_stochastic_processes/participant_parameters.csv` | `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU`, `tau_hat`, `fit_valid` — loaded directly, **not re-estimated** |
| InT model outputs | `ds4_information_theory/participant_entropy_metrics.csv` | `H_SDE` — joined directly as `H_StM` (mathematically identical formula, not recomputed) |
| DyS model outputs | `ds4_dynamical_systems/participant_dynamics_parameters.csv` | `regime_label` |
| Stage 1 behavior features | `ds4_behavior_features.csv` | `activity_persistence` (psychosocial-analog correlation check — genuine null, r=0.006) |

**What was derived:**
- `beta_OU = 2*theta_hat_OU/sigma_hat_OU^2`, `T_OU`, `chi_OU`, `F_OU`, `Z_2state`, `p_use`, `E_use` → all monotone/composite transforms of StoP output
- `V_min_location`, `V_curvature`, `V_depth` (individual OU potential wells) → exact formula from StoP output, no KDE needed
- `temperature_group` (median β_OU split) → derived

**What came from survey data:** Nothing (no Likert scales exist in DS4 to correlate against; `activity_persistence` used instead is itself a behavioral Stage-1 feature, not survey data).

**Verdict:** **Entirely derived from StoP/InT/DyS outputs** — the most purely "downstream" family in the DS4 arc, deliberately built to avoid re-deriving anything StoP/InT/DyS had already computed (see `ds4_stm_blueprint.md` §0).

---

### NeT — Network Theory (notebook 54)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds4_behavioral_clean.csv` | `participant_id_canonical`, `timestamp_utc`, `app_name`, `intervention_event_class` (filtered to `intervention_event` + `no_intervention`, excluding `app_close_event`) |
| Stage 1 behavior features | `ds4_behavior_features.csv` | `app_herfindahl` (redundancy check only) |
| InT model outputs (corrected mid-implementation) | `ds4_information_theory/participant_entropy_metrics.csv` | Originally joined `H_app` (all-events) for the `I_consec` bridge — **replaced** by a freshly computed `H_app_attempts` after a bug was found (see `ds4_bug_discoveries_and_fixes_chronicle.md`) |

**What was derived from behavioral data:**
- App-transition sequences (`app_prev`/`app_current`), self-derived via timestamp ordering within participant, restricted to attempt rows only → purely behavioral, and a deliberate DS4-specific construction choice (excluding `app_close_event`, 47.1% of all rows)
- `T_ij`, `rho_self`, `H_trans`, `HHI_net`, stationary distribution `π`, `H_pi` → behavioral
- `H_app_attempts` (current-app marginal on the exact attempts-only population `H_trans` uses) → behavioral, computed fresh in this notebook after the bridge bug was found
- `I_consec = H_app_attempts − H_trans` → behavioral

**What came from survey data:** Nothing.

**Verdict:** **Purely behavioral event-derived.** The one cross-model dependency (InT's `H_app`) was found to be the wrong population for this specific bridge and was replaced with a fresh in-notebook computation — so, after the fix, NeT does not actually consume InT's output for its headline `I_consec` quantity.

---

### GaT — Game Theory (notebook 56)

| Data used | File | Columns used |
|---|---|---|
| Stage 1 behavior features | `ds4_behavior_features.csv` | `rate_opened_intervention_events`, `max_consecutive_opens`, `p_open_after_dismiss` (checked, then dropped), `open_rate_change_calendar` (adaptation cross-check) |
| Behavioral events | `ds4_behavioral_clean.csv` | Attempt rows, to compute `substitution_after_dismissal_rate` (new quantity: `P(app_next≠app_current | outcome=dismissed)`) |
| StM model outputs | `ds4_statistical_mechanics/participant_ds4_stm_parameters.csv` | `chi_OU` (cross-check only, not used in classification) |
| Step 2 phenotyping outputs | `ds4_phenotyping/ds4_cluster_assignments.csv` | Phase 1 cluster labels (cross-check only) |

**What was derived:**
- `substitution_after_dismissal_rate` → new behavioral quantity, computed fresh from attempt-row sequences
- `gat_phenotype` (rule-based classification into 4 named types) → derived entirely from 3 Stage 1/behavioral quantities, no clustering, no survey input

**What came from survey data:** Nothing. GaT's cross-checks against `chi_OU` and Phase 1 clusters are cross-model, not survey-based.

**Verdict:** **Entirely behavioral** (Stage 1 features + a fresh behavioral computation), with purely descriptive cross-checks against other model families' outputs — no formal payoff matrix built (paper's own caution, §2.6), no survey data used anywhere.

---

### ABM — Agent-Based Modeling (notebook 57)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `ds4_stochastic_processes/participant_parameters.csv` and `participant_parameters_weekly_sensitivity.csv` | `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU` (agent parameters), real daily/weekly `theta_hat_OU`/`tau_hat` (validation target) |

**What was derived:**
- Simulated daily OU paths (Model 1: pure OU; Model 2: + illustrative weekly-periodic drift), one agent per real participant, using that participant's own already-fitted (μ̂,θ̂,σ̂) → no re-estimation from raw data
- Simulated daily-vs-weekly θ̂ divergence, compared against StoP's own real divergence

**What came from survey data:** Nothing. **What came from Step 2 phenotyping:** Nothing — unlike the original 2026-04-18 deferral plan (see `ds4_deferred_models_rationale.md` and the DS5 parallel in `ds5_gat_abm_deferred_resolution.md`), DS4's ABM does not use discrete phenotype-derived agent types; it calibrates one agent per participant directly from StoP's individual parameters.

**Verdict:** **Entirely derived from StoP's own real output** — no raw behavioral events re-read, no survey data, no phenotype labels used as agent-type generators (only StoP's individual-level parameters).

---

## Step 2 Phenotyping

### Phase 1 — Global Phenotyping (notebook 59)

**Primary data sources:**
- All 5 completed Step 1 model outputs merged at participant level: `tau_hat` (StoP), `H_emp` (InT), `fixed_point_deviation` (DyS), `chi_OU` (StM), `rho_self` (NeT)
- Demographic overlay (exploratory/secondary, FLAG 5): `ds4_survey_features.csv` — `survey_age`, `gender_clean`, N=149 of the 641 complete-case population

**Verdict:** **Entirely derived from Step 1 model outputs.** No raw behavioral events read directly in this notebook. Survey data enters only as a thin, explicitly-secondary demographic overlay (149/641 = 23.2% coverage, no significant age difference found, F=1.564, p=0.213) — far weaker a role than DS5's Phase 1, which at least had `study_condition` as a standard overlay variable for all 414 participants.

---

### Path A′ — Behavior-only (drop NeT) (notebook 131)

**Primary data sources:**
- Same 5 Step 1 outputs as Phase 1, minus `rho_self`: `tau_hat`, `H_emp`, `fixed_point_deviation`, `chi_OU`
- Phase 1's own cluster assignments (`ds4_cluster_assignments.csv`) for the ARI comparison

**Verdict:** **Entirely derived from Step 1 model outputs** (StoP/InT/DyS/StM only). No survey data, no raw events.

---

### Path C′ — Network-focused (notebook 132)

**Primary data sources:**
- NeT model output (`ds4_network_models/participant_network_metrics.csv`) — `rho_self`, `I_consec` only (the two features found to be non-redundant among NeT's own richer feature set; `HHI_net`/`H_trans` excluded as near-mechanically-redundant with `rho_self`, r=0.867/-0.950)
- Phase 1's cluster assignments for the ARI comparison

**Verdict:** **Entirely derived from Step 1 NeT model output.** No survey data, no raw events, no other Step 1 family's output.

---

### Path F′ — Joint taxonomy (notebook 133)

**Primary data sources:**
- Path A′'s own cluster labels (`path_a_cluster`, k=4)
- Path C′'s own cluster labels (`path_c_cluster`, k=3)
- No fresh clustering — a cross-tabulation and chi-square/Fisher test of two already-fitted label sets

**Verdict:** **Entirely derived from Path A′ + Path C′ outputs**, which are themselves entirely derived from Step 1. No survey data, no raw events, no new features computed.

---

## Summary table

| Model/Path | Behavioral events | Survey data | Previous model outputs | Notes |
|---|---|---|---|---|
| StoP | Primary (daily X_t, intervention_event class) | None | No | Purely behavioral, no condition to join |
| InT | Primary (outcome/type entropy) | None | σ̂/θ̂ for H_SDE (StoP) | Mostly behavioral |
| DyS | Rebuild for validation only | None | StoP + InT primary | Entirely derived |
| StM | No (activity_persistence is a Stage 1 behavioral feature) | None | StoP + InT + DyS primary | Entirely derived |
| NeT | Primary (app sequences, attempts-only) | None | InT's H_app tried, replaced after bug found | Purely behavioral after the fix |
| GaT | Primary (substitution rate) + Stage 1 features | None | StM chi_OU, Phase 1 clusters (cross-check only) | Purely behavioral |
| ABM | No (agent params from StoP only) | None | StoP primary | Entirely derived; no phenotype input, unlike original plan |
| Phase 1 | No | Overlay only (149/641, exploratory) | All 5 Step 1 outputs | Entirely derived |
| Path A′ | No | None | StoP+InT+DyS+StM + Phase 1 (comparison) | Entirely derived |
| Path C′ | No | None | NeT + Phase 1 (comparison) | Entirely derived |
| Path F′ | No | None | Path A′ + Path C′ | Entirely derived |

---

## What is truly behavior-derived vs questionnaire-dependent

**Truly behavior-derived (all DS4 model parameters, no exception):**
- StoP: `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU`, `tau_hat`
- InT: `H_out_intervention`, `H_out_all_classes`, `H_app`, `H_hour`, `H_emp`, `H_SDE`, `MI(intervention_type;outcome)`
- DyS: `regime_label`, `fixed_point_deviation`, `behaviorally_deterministic`
- StM: `beta_OU`, `T_OU`, `chi_OU`, `F_OU`, `V(x)` parameters
- NeT: `rho_self`, `H_trans`, `HHI_net`, `H_pi`, `I_consec`
- GaT: `gat_phenotype`, `substitution_after_dismissal_rate`
- ABM: simulated daily/weekly θ̂ divergence
- All phenotyping (Phase 1, Path A′, C′, F′): cluster assignments and profiles

**Requires survey data to be interpretable:** Nothing in DS4's core model parameters requires survey data — this is the central structural contrast with DS5, where `study_condition` was a load-bearing join for condition-level summaries in nearly every family and path.

**Uses survey data (thin, exploratory, secondary only):**
- Phase 1's demographic overlay (`survey_age`, `gender_clean`; N=149/641; null result, F=1.564, p=0.213)
- No psychosocial (Likert-scale) correlations exist anywhere in DS4, because DS4's single post-use survey has none (see `data_docs/modeling_cautions.md` §4, `outputs/features/ds4/ds4_features.md`)

**Important conclusion:** Unlike DS5 — where survey data was structurally necessary throughout (condition joins, psychosocial overlays, and one path, Path E, that could not run without it) — **every DS4 model parameter and every phenotype assignment is derived entirely from behavioral event data or from other models' behavioral-derived outputs.** DS4's survey contributes nothing beyond a thin, explicitly-labeled-exploratory demographic overlay on 23% of the phenotyping population, and even that produced a null result. This is a genuine structural property of DS4 (a single-wave, qualitative-only, no-condition retrospective survey design), not an implementation choice — see `ds4_deferred_models_rationale.md` for how this same structural fact is the reason SyD is excluded.

---

## Source documents

- `outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`, `ds4_int_blueprint.md`, `ds4_dys_blueprint.md`, `ds4_stm_blueprint.md`, `ds4_net_blueprint.md`, `ds4_gat_blueprint.md`, `ds4_abm_blueprint.md`
- `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`, `ds4_step2_exploration_plan.md`
- `outputs/model_outputs/ds4_stochastic_processes/model_run_summary.md`, `participant_parameters.md`
- `outputs/model_outputs/ds4_information_theory/model_run_summary.md`, `participant_entropy_metrics.md`
- `outputs/model_outputs/ds4_dynamical_systems/model_run_summary.md`
- `outputs/model_outputs/ds4_statistical_mechanics/model_run_summary.md`, `participant_ds4_stm_parameters.md`
- `outputs/model_outputs/ds4_network_models/model_run_summary.md`, `participant_network_metrics.md`
- `outputs/model_outputs/ds4_game_theory/model_run_summary.md`, `participant_gat_phenotypes.md`
- `outputs/model_outputs/ds4_agent_based/model_run_summary.md`, `participant_abm_simulation_results.md`
- `outputs/model_outputs/ds4_phenotyping/model_run_summary.md`, `ds4_phenotype_feature_matrix.md`, `path_a_feature_matrix.md`, `path_c_cluster_profiles.md`, `path_f_summary.md`, `ds4_demographic_overlay.md`
- `outputs/features/ds4/ds4_features.md`, `outputs/cleaned/ds4_survey_clean.md`
- `data_docs/modeling_cautions.md` §4/§6 (DS4 sections)

---

*Written 2026-08-08 as part of the DS4 post-analysis synthesis, mirroring the DS5 template (`outputs/reports/stage4/post_analysis/model_data_usage_map.md`).*

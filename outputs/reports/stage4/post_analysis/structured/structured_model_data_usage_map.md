# Model and Path Data Usage Map — Structured

**Written:** 2026-08-08
**Overlap check:** Read in full before writing — `outputs/reports/stage4/post_analysis/model_data_usage_map.md`
(DS5's own version, whose table structure this document follows), `structured_cas_modeling_plan.md` (per-family
"Depends on" lines double-checked against each blueprint), and all 8 model blueprints + the phenotyping and
4 path blueprints. **No existing Structured document assembles a single cross-family data-provenance table
like this one** — each blueprint states its own dependencies individually, but nothing pulls all 8 families
plus Step 2 into one place. This document is new content, not a duplicate of anything in
`outputs/reports/structured/`.
**Purpose:** Clarify for every implemented Structured model family and Step 2 pass exactly which data
sources were used — raw behavioral events, Stage 1 features, survey data, or previous model outputs —
mirroring the DS5 template's structure and tone.

---

## Overview: data sources available for Structured

| Data source | File | N rows / N participants | Primary content |
|---|---|---|---|
| Behavioral events (cleaned) | `outputs/cleaned/structured_behavioral_clean.csv` | 53,686 events | Task-lifecycle events: Task Created / Updated / Deleted, `update_type` change tags |
| Survey (cleaned) | `outputs/cleaned/structured_survey_clean.csv` | 117 responses (65 consented+finished) | Intake survey: demographics, motivation, single-item wellbeing/productivity scores, ASRS-6 screener |
| Participant linkage | `outputs/cleaned/structured_participant_linkage.csv` | 61 behavioral participants | Behavioral/survey overlap flags, per-participant event-type counts |
| Stage 1 task-lifecycle features | `outputs/features/structured/structured_task_lifecycle_features.csv` | 26,729 tasks | Task-level derived fields: `lifecycle_status`, `has_creation_event`, `task_type_first/last`, reschedule/completion transitions |
| Stage 1 participant features | `outputs/features/structured/structured_participant_features.csv` | 61 participants | Participant-level aggregates: task-type shares, completion/reschedule rates, `pct_tasks_left_censored` |
| Stage 1 survey features | `outputs/features/structured/structured_survey_features.csv` | 61 participants (survey-matched) | Recoded/derived survey scores, joinable to behavioral participants |
| Model outputs | `outputs/model_outputs/structured/*/` | Varies by family (36–61) | Per-participant model parameters, one folder per family + phenotyping |

Unlike DS5 (a 3-arm RCT with pre/post psychosocial change scores), Structured is **purely observational,
no randomized conditions**. The only stratifying variable anywhere in this dataset is
`subscription_type_last` (free/pro) — self-selected, not assigned, and used only for explicitly-labeled
descriptive (non-causal) comparisons in every model family below.

---

## Step 1 Model Implementations

### NeT — Network Theory (notebook 64)

| Data used | File | Columns used |
|---|---|---|
| Task-lifecycle features | `structured_task_lifecycle_features.csv` | `task_id`, `event_timestamp_utc`, `update_type_list_str`, `task_type`, `has_creation_event` |
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | `event_type`, timestamps for edge ordering |

**What was derived from behavioral/task data:** state vocabulary mapping (7 states), per-task edge lists,
pooled participant-level transition matrix, HHI_net, rho_self, H_trans, stationary distribution π,
entry-state distribution — **entirely behavioral/task-derived**.

**What came from survey data:** nothing for the parameters themselves. `subscription_type_last` (carried
from the linkage/participant table) is used only for the observational free-vs-pro descriptive comparison
(FLAG W5), not for computing any network metric.

**Verdict:** NeT parameters are **purely task-event-derived**. No dependency on any other model family or
on survey data. First model built for exactly this reason (no dependency chain to wait on).

---

### InT — Information Theory (notebook 65)

| Data used | File | Columns used |
|---|---|---|
| Task-lifecycle features | `structured_task_lifecycle_features.csv` | `task_type_first/last`, `update_method`, creation hour, `recurrence_use_rate`, `lifecycle_status`, reschedule flags |
| Participant features | `structured_participant_features.csv` | task-count eligibility denominators |
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | timestamps |
| **NeT model output** | `outputs/model_outputs/structured/network_theory/participant_network_metrics.csv` | `H_trans` (for the NeT–InT bridge) |

**What was derived from task-lifecycle data:** `H_type_first/last`, `H_creation_source`,
`H_hour_creation`, `H_recurrence`, `H_completion`, `H_reschedule` (7 per-participant entropy measures);
the 3 pooled mutual-information tests (task type→completion, creation source→placement, hour→task type) —
**entirely behavioral/task-derived**.

**What came from a previous model output:** `H_state_marginal` and `I_consec_state = H_state_marginal −
H_trans` require NeT's own edge list and `H_trans` column — the one genuine cross-model dependency in this
notebook.

**What came from survey data:** nothing. No survey column is used anywhere in this notebook.

**Verdict:** InT is **behavioral/task-derived**, with one explicit bridge dependency on NeT (already
complete when InT was built, so this was not a blocking dependency in practice).

---

### StoP — Stochastic Processes (notebook 63)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | `event_type`, `event_timestamp_utc`, `event_timezone`, `update_type_list_str` |

**What was derived:** daily local-calendar-day count series for `N_t^created` and `N_t^completed`;
`mu_hat`, `sig_hat`, `sigma_mu_ratio`, `Fano_factor`; rule-based descriptive phenotype labels — **entirely
behavioral-derived, directly from the cleaned event log**, no Stage 1 feature table needed at all.

**What came from survey data:** nothing for the parameters. `subscription_type_last` used only for the
observational free-vs-pro comparison.

**Verdict:** StoP has the **shallowest data dependency of any Structured model family** — built directly
from the cleaned behavioral file, no Stage 1 features, no other model outputs. This is also why DyS and
StM (which the project's general dependency-chain convention might suggest should consume StoP's output,
mirroring DS5) explicitly do **not** depend on it here — see their entries below.

---

### DyS — Dynamical Systems (notebook 62)

| Data used | File | Columns used |
|---|---|---|
| Task-lifecycle features | `structured_task_lifecycle_features.csv` | `task_type_first`, `lifecycle_status`, `subtasks_amount_last`, `has_creation_event`, `event_timezone` |
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | timestamps for weekly indexing |

**What was derived:** the 5-dimensional weekly state vector (`n_created_w`, `timed_share_w`,
`inbox_share_w`, `completed_share_w`, `complexity_w`), trajectory metrics (`state_space_volatility`,
`volume_trend_slope`, `dropout_score`), region labels — **entirely task-lifecycle-derived**.

**What did NOT feed this model, by deliberate design:** StoP's fitted `mu_hat`/`sig_hat`. Unlike DS5
(where DyS is a direct σ→0 reduction of StoP's own fitted SDE), Structured's DyS is grounded in the
paper's own separately-worked weekly, multi-dimensional example — see
`structured_dys_blueprint.md` Part 0 for the full justification. This is the single clearest place
Structured's dependency graph diverges from DS5's.

**What came from survey data:** nothing for the parameters; `subscription_type_last` for the observational
comparison only.

**Verdict:** DyS is **task-lifecycle-derived, and explicitly independent of StoP** — a structural
difference from DS5's dependency chain, not an oversight.

---

### SyD — System Dynamics (notebook 68)

| Data used | File | Columns used |
|---|---|---|
| Task-lifecycle features | `structured_task_lifecycle_features.csv` | `has_creation_event`, entry/exit week derivation, `lifecycle_status` |
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | timestamps, reschedule event flags |

**What was derived:** `Backlog_w` stock (running count of open non-censored tasks per participant-week),
`backlog_trend_slope`, `backlog_mean/peak`, `dominant_loop_label`, and the three feedback-loop correlation
tests (productive/overload/balancing, pooled and within-participant) — **entirely task-lifecycle-derived**.

**What came from other model outputs:** nothing directly — SyD does not read any other family's CSV. A
non-redundancy check (Part 0.5 of the blueprint) was performed against NeT/StoP/DyS's already-published
outputs, but no column from those files is consumed.

**What came from survey data:** nothing.

**Verdict:** SyD is **entirely task-lifecycle-derived**, with a documented but non-consuming
non-redundancy relationship to NeT/StoP/DyS.

---

### StM — Statistical Mechanics (notebook 61)

| Data used | File | Columns used |
|---|---|---|
| Task-lifecycle features | `structured_task_lifecycle_features.csv` | `task_type_last`, `task_is_recurring_ever`, `task_has_notes_last`, `subtasks_amount_last`, `lifecycle_status` |
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | weekly indexing for persistence |

**What was derived:** `full_config`/`structural_config` microstates, `H_config`, macrostate labels,
`top1_config_share`, `persistence_rate`, `susceptibility`, path-dependence test (pooled + within-
participant) — **entirely task-lifecycle-derived**.

**What did NOT feed this model, by deliberate design:** StoP's output. This is the largest single
departure from DS5's dependency chain in the whole Structured arc — DS5's StM formula (`β_behav =
2/σ̂²`) is derived specifically from StoP's fitted diffusion parameter; the theory paper's own §2.1
explicitly cautions against forcing that apparatus onto Structured's discrete configuration-space object.
See `structured_stm_blueprint.md` Part 0.

**What came from InT (cross-check only, not an input to any StM parameter):** `H_config`'s validity is
checked against InT's `H_type_last`/`H_completion`/`H_recurrence` marginals via the chain-rule sanity gate
(`H_config ≥` each marginal) — a verification step, not a data dependency in the sense of feeding a
formula.

**What came from survey data:** nothing.

**Verdict:** StM is **entirely task-lifecycle-derived**, explicitly independent of StoP (unlike DS5, where
StM directly consumes StoP's `sig_hat`).

---

### GaT — Game Theory (notebook 66)

| Data used | File | Columns used |
|---|---|---|
| Task-lifecycle features | `structured_task_lifecycle_features.csv` | `task_type_last`, `task_duration_min_last`, `task_is_recurring_ever`, `subtasks_amount_last`, `lifecycle_status`, reschedule flags |
| Participant features | `structured_participant_features.csv` | `reschedule_rate`, `pct_tasks_completed` (reused as phenotype-label inputs, not recomputed) |
| Behavioral events (cleaned) | `structured_behavioral_clean.csv` | timestamps for ordering |

**What was derived:** `commitment_score` (0–5 proxy index), the commitment-outcome trade-off curve
(pooled + within-participant), phenotype labels, strategy-adaptation-after-rescheduling test — **entirely
task-lifecycle-derived**.

**What came from other model outputs:** SyD's `dominant_loop_label = "overload-trending"` is
cross-referenced (not recomputed) for the paper's 5th named GaT phenotype ("overload-prone") — a citation,
not a numerical input to any GaT quantity.

**What came from survey data:** nothing.

**Verdict:** GaT is **entirely task-lifecycle-derived**, with one cross-reference (not a data dependency)
to SyD's own output.

---

### ABM — Agent-Based Modeling (notebook 67)

| Data used | File | Columns used |
|---|---|---|
| Participant features | `structured_participant_features.csv` | `share_task_type_*`, `pct_tasks_completed`, `reschedule_rate` |
| **StoP model output** | `outputs/model_outputs/structured/stochastic_processes/participant_stop_parameters.csv` | `created_mean_N`, `created_n_active_days`, `created_span_days`, `created_Fano_factor`, `created_is_eligible` |
| **Step 2 phenotyping output** | `outputs/model_outputs/structured/phenotyping/cluster_assignments.csv`, `cluster_profiles.csv` | `cluster_label` (Profile A/B), per-profile mean rule parameters |

**What was derived:** two generative agent models (static-rate Poisson baseline; two-state session
on/off), simulated Fano factors, individual-agent rank correlation against real Fano, phenotype-mixture
validation — **all agent rules read directly from already-fitted Step 1/Step 2 outputs, not re-estimated
from raw behavioral data**, per the paper's own explicit instruction (quoted in the blueprint).

**What came from survey data:** nothing.

**Verdict:** ABM is the **only Structured model family built entirely from other models' already-fitted
outputs**, with zero direct read of the raw behavioral file — matching DS5's own ABM data-usage pattern
(DS5's ABM likewise consumes only StoP's individual SDE parameters, not raw events).

---

## Step 2 Phenotyping Passes

### Phase 1 — Global Phenotyping (notebook 120)

**Primary data sources:** one feature from each of the 7 completed Step 1 model families' own
participant-level CSVs (`HHI_net` from NeT, `H_completion` from InT, `created_Fano_factor` from StoP,
`state_space_volatility` from DyS, `backlog_trend_slope` from SyD, `susceptibility` from StM,
`mean_commitment_score` from GaT). No new behavioral event data used.

**Survey data used:** `structured_survey_features.csv`, restricted to `consent_given & is_finished`
(N≈33 after intersecting with the N=36 clustering population) — Kruskal-Wallis overlay only, not part of
the clustering feature set itself.

**Verdict:** **Entirely derived from Step 1 model outputs**, exactly mirroring DS5's Phase 1 data-usage
pattern. Survey used only as a post-hoc, Bonferroni-corrected overlay.

---

### Path A — Behavior-Only Phenotyping (notebook 122)

**Primary data sources:** the same 6 non-NeT Step 1 outputs used in Phase 1 (InT, StoP, DyS, SyD, StM,
GaT). Phase 1's `cluster_assignments.csv` used only for the ARI comparison, not as a clustering input.

**Survey data used:** none for clustering. `subscription_type_last` (from the participant/linkage table,
not a survey response) used for the Path E analog's feasibility check.

**Verdict:** **Entirely derived from 6 Step 1 model outputs.** No raw events, no survey data.

---

### Path C — Network-Substructure (notebook 121)

**Primary data sources:** NeT's own `participant_network_metrics.csv` (`HHI_net`, `rho_self`, `H_trans`)
and InT's `participant_entropy_metrics.csv` (`H_state_marginal`). Phase 1's and Path A's cluster
assignments used only for ARI/cross-tab comparison, not as clustering inputs.

**Verdict:** **Derived from NeT + InT Step 1 outputs only.** No raw events, no survey data, no dependency
on Phase 1 or Path A for the clustering itself (only for post-hoc comparison).

---

### Path D — Secondary/Robustness Features (notebook 124)

**Primary data sources:** five secondary columns spread across four Step 1 outputs not used in Path A's
curated set (`created_mu_hat` from StoP, `volume_trend_slope`/`dropout_score` from DyS,
`H_hour_creation` from InT, `persistence_rate` from StM). Path A's population/feature matrix used for the
correlation gate and the ARI comparison population, not as a raw data source.

**Verdict:** **Derived from 4 Step 1 model outputs.** No raw events, no survey data. Result: no feasible
clustering solution (see `structured_phenotype_expectation_vs_result.md` and
`structured_step2_master_synthesis.md` for the full null-result writeup) — this does not change the data-
usage classification, only the outcome.

---

### Path F — Joint Taxonomy (notebook 123)

**Primary data sources:** Path A's `behavior_only_cluster_assignments.csv` and Path C's
`net_only_cluster_assignments.csv` — **no raw model-output columns and no new clustering at all**. This
notebook is a cross-tabulation and Fisher's exact test on two already-fitted label columns.

**Verdict:** **Entirely derived from two Step 2 path outputs.** The only Structured Step 2 pass with zero
direct dependency on any Step 1 CSV.

---

## Summary table

| Family / Path | Raw behavioral events | Task-lifecycle features (Stage 1) | Survey data | Previous model outputs | Notes |
|---|---|---|---|---|---|
| NeT | Primary | Primary | Overlay only (`subscription_type_last`) | No | Purely task-derived; no dependencies |
| InT | For timestamps | Primary | No | NeT (`H_trans` bridge only) | Mostly task-derived |
| StoP | Primary | No (built directly from cleaned events) | Overlay only | No | Shallowest dependency of any family |
| DyS | For weekly indexing | Primary | Overlay only | **No** (deliberately not StoP) | Structural divergence from DS5 |
| SyD | For timestamps | Primary | No | No (non-redundancy check only, no consumption) | Purely task-derived |
| StM | For weekly indexing | Primary | No | No (**deliberately not StoP**); InT for a sanity check only | Largest departure from DS5's chain |
| GaT | For ordering | Primary | No | SyD (cross-reference only, not numeric input) | Purely task-derived |
| ABM | **No** | No (uses participant features only) | No | StoP + Phenotyping (Phase 1) | Only family with zero raw-event dependency |
| Phase 1 (phenotyping) | No | No | Overlay only | All 7 Step 1 outputs | Entirely derived |
| Path A | No | No | Overlay only (Path E analog) | 6 Step 1 outputs | Entirely derived |
| Path C | No | No | No | NeT + InT | Entirely derived |
| Path D | No | No | No | StoP + DyS + InT + StM | Entirely derived; null result |
| Path F | No | No | No | Path A + Path C (Step 2 outputs, not Step 1) | Zero Step 1 dependency |

---

## What is truly behavior-derived vs. survey-dependent

**Truly behavior/task-derived (no survey needed for any parameter):** every quantity in every one of the
8 Step 1 model families and all 5 Step 2 passes. This is a stronger statement than DS5's own equivalent
section can make — DS5's condition-level comparisons and its `H_out_resid` residualization structurally
require the `study_condition` survey/randomization field to be meaningful at all. **Structured has no such
requirement anywhere**, because it has no randomized condition to begin with. Every headline number in
this dataset's entire modeling program — NeT's HHI_net, StoP's Fano factor, GaT's non-monotonic
commitment curve, the Phase 1 cluster split, all four Step 2 exploration-path ARIs — is computable from
`structured_behavioral_clean.csv` and its Stage 1 derivatives alone, with zero survey involvement.

**Uses survey data only as a post-hoc, exploratory overlay (never as a parameter or clustering input):**
- Phase 1's psychosocial Kruskal-Wallis overlay (`life_happiness_score`, productivity scores,
  `pct_planned_tasks_completed_num`) — all null after Bonferroni correction.
- The one-time construct-validity check comparing self-reported vs. behaviorally-derived completion rate
  (`r=0.127`, reported in `structured_cas_modeling_plan.md`'s first status update) — a validation exercise,
  not an input to any model parameter.

**Uses an observational (non-randomized, non-survey) grouping variable for descriptive comparisons only:**
`subscription_type_last` (free/pro), appearing in NeT, StoP, DyS, and the Path A "Path E analog" check —
every single one of these comparisons is explicitly labeled non-causal in its own blueprint (FLAG W5 and
its analogs), because subscription tier is self-selected, not assigned.

**Important conclusion, directly comparable to DS5's own:** just as DS5 concluded its core model
parameters and phenotype taxonomy would exist even without survey responses, Structured's entire 8-family
+ Step 2 program is **fully independent of the survey file**. The difference is one of degree, not kind:
DS5 still needs the survey for `study_condition`, a load-bearing field for several of its central
findings (condition-stratified Path E, `H_out_resid`). Structured has no equivalent load-bearing survey
field anywhere in its modeling program — the survey is purely a secondary, exploratory overlay, weaker in
its footprint here than in any other dataset in this project.

---

*Written 2026-08-08 as part of the Structured post-analysis waypoint, mirroring
`outputs/reports/stage4/post_analysis/model_data_usage_map.md`.*

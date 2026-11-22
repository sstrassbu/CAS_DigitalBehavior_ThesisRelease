# Model and Path Data Usage Map — DS5

**Written:** 2026-04-20  
**Purpose:** Clarify for every implemented DS5 model and Step 2 path exactly which data sources were used — behavioral only, survey, pre/post survey, or previous model outputs

---

## Overview: data sources available for DS5

| Data source | File | N rows | Primary content |
|---|---|---|---|
| Behavioral events | `outputs/cleaned/ds5_behavioral_clean.csv` | 288,688 | Event-level: participant ID, timestamp, app, outcome |
| Pre-survey | `outputs/features/ds5/ds5_survey_features.csv` | 572 | study_condition + FoMO, belonging, ostracism, digital wellbeing (PRE) |
| Post-survey | `outputs/features/ds5/ds5_prepost_features.csv` | 284 | Pre-post change scores (284 participants fully linked) |
| Stage 1 behavior features | `outputs/features/ds5/ds5_behavior_features.csv` | 573 | Aggregated participant-level behavioral summaries |
| Model outputs | `outputs/model_outputs/*/` | Varies | Per-participant model parameters |

---

## Step 1 Model Implementations

### StoP — Stochastic Processes (notebook 43)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds5_behavioral_clean.csv` | participant_id_canonical, local_date, event_outcome_simple |
| Pre-survey | `ds5_survey_features.csv` | study_condition (for condition split) |
| Pre-survey | `ds5_survey_features.csv` | fomo_mean_pre, belong_mean_pre, ostracism_mean_pre, digital_wellbeing_pre |

**What was derived from behavioral data:**
- X_t = n_opened/n_events per day per participant → entirely behavioral
- μ̂ = mean(ΔX_t) → behavioral
- σ̂ = std(ΔX_t) → behavioral
- σ/|μ| ratio → behavioral
- x_mean = mean(X_t) → behavioral

**What came from survey data:**
- study_condition join (essential for condition-level comparisons)
- Psychosocial correlations section: FoMO, belonging, ostracism, digital wellbeing (exploratory overlay only — NOT used to derive model parameters)

**Verdict:** Parameters are **purely behavioral-derived**. Survey data used only for condition stratification and exploratory psychosocial correlations.

---

### InT — Information Theory (notebook 45)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds5_behavioral_clean.csv` | All event-level data for entropy computation |
| Pre-survey | `ds5_survey_features.csv` | study_condition, psychosocial scales |

**What was derived from behavioral data:**
- H_out = Shannon entropy over {opened, dismissed, closed} per participant → behavioral
- H_app = entropy of app distribution → behavioral
- H_hour = entropy of hour-of-day distribution → behavioral
- H_emp = empirical entropy of daily X_t distribution (K=10 bins) → behavioral
- H_SDE = ½ log₂(2πe·σ̂²) → derived from StoP σ̂ (behavioral)

**What came from survey data:**
- study_condition for condition-level summaries
- Psychosocial correlations (exploratory overlay)

**What came from previous model outputs:**
- σ̂ from StoP (`participant_parameters.csv`) — used to compute H_SDE bridge

**Verdict:** H_emp, H_out, H_app, H_hour are **purely behavioral**. H_SDE depends on StoP output. Survey used only for stratification/correlation overlays.

---

### DyS — Dynamical Systems (notebook 42)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `participant_parameters.csv` | sig_hat, mu_hat, x_mean |
| InT model outputs | `participant_entropy_metrics.csv` | H_emp, H_SDE |
| Pre-survey | `ds5_survey_features.csv` | study_condition, psychosocial scales |

**What was derived:**
- is_dys_eligible = (sig_hat < σ_median=0.1812) → binary threshold on StoP output
- regime_label = "DyS-deterministic" or "StoP-stochastic" → from is_dys_eligible
- predicted_boundary_fp = "upper" (μ̂>0) or "lower" (μ̂<0) → from StoP mu_hat
- deviation_from_predicted_fixed_point = |x_mean − predicted boundary| → from StoP
- behaviorally_deterministic = is_dys_eligible AND H_emp < H_emp_median → from StoP + InT

**What came from survey data:**
- study_condition, psychosocial scales (overlay only)

**Verdict:** DyS is **entirely derived from previous model outputs** (StoP + InT). No new behavioral event data used. No survey data used for parameters.

---

### StM — Statistical Mechanics (notebook 41)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `participant_parameters.csv` | sig_hat, x_mean |
| InT model outputs | `participant_entropy_metrics.csv` | H_emp |
| Behavioral events | `ds5_behavioral_clean.csv` | For V(x) KDE computation (condition-level potential) |
| Pre-survey | `ds5_survey_features.csv` | study_condition, psychosocial scales |

**What was derived:**
- β_behav = 2/σ̂² → monotone transform of StoP sig_hat (behavioral)
- T_behav = σ̂²/2 → monotone transform of StoP sig_hat
- p_use_approx ≈ x_mean → from StoP
- chi_behav = β·p·(1−p) → from sig_hat and x_mean (behavioral)
- F_behav = x_mean − (1/β)·H_emp → from StoP + InT (behavioral)
- H_StM_participant = entropy from KDE of X_t → behavioral (from events)
- four_model_convergent = (low sig_hat AND low H_emp) → composite flag
- V(x) condition potential → from condition-level X_t distributions (behavioral)

**What came from survey data:**
- study_condition for condition-level V(x) curves and summaries
- Psychosocial scales (exploratory overlay)

**Verdict:** Parameters are **largely derived from StoP/InT outputs**. V(x) requires behavioral event aggregation. Survey used for stratification/overlay only.

---

### NeT — Network Theory (notebook 44)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds5_behavioral_clean.csv` | participant_id_canonical, local_timestamp, app_name, event_outcome_simple |
| Pre-survey | `ds5_survey_features.csv` | study_condition, psychosocial scales |

**What was derived:**
- App transition sequences (app_prev, app_next) → derived from event ordering → **purely behavioral**
- W_ij = transition weights between apps → behavioral
- T_ij = transition probability matrix → behavioral
- HHI_net = network Herfindahl index → behavioral
- rho_self = self-loop rate → behavioral
- H_trans = transition entropy → behavioral
- H_pi = stationary distribution entropy (N=378 eligible) → behavioral
- I_consec = H_app − H_trans → behavioral
- top1_share_net, top3_share_net → behavioral

**What came from survey data:**
- study_condition for condition-level network summaries
- Psychosocial scales (exploratory overlay)

**Verdict:** NeT is **purely behavioral event-derived**. No survey data used for parameters. The most computationally intensive Step 1 analysis — requires sequence engineering from raw events.

---

## Step 2 Phenotyping Paths

### Phase 1 — Global Phenotyping (notebook 100)

**Primary data sources:**
- All 5 model outputs merged at participant level (StoP, InT, DyS, StM, NeT parameter files)
- No new behavioral event data used
- Survey: study_condition (overlay); psychosocial scales (post-hoc overlay)

**Verdict:** **Entirely derived from Step 1 model outputs**. No raw event data. Survey used only as overlay.

---

### Path C — Network Sub-Phenotyping (notebook 101)

**Primary data sources:**
- Phase 1 cluster assignments (`ds5_cluster_assignments.csv`) — Step 2 output
- NeT model outputs (`participant_network_metrics.csv`) — Step 1 output
- StoP/InT model outputs for post-hoc overlays

**Verdict:** **Derived from Step 1 NeT model output + Phase 1 assignments**. No raw events or survey data used for clustering.

---

### Path A — Behavior-Only Phenotyping (notebook 102)

**Primary data sources:**
- `ds5_phenotype_feature_matrix.csv` (merged Step 1 model features) — specifically sig_hat, H_emp, x_mean
- Phase 1 cluster labels for post-hoc comparison
- Survey: study_condition (condition χ² test), psychosocial scales (KW overlay)

**Verdict:** **Derived from Step 1 StoP and InT outputs only** (sig_hat=StoP; H_emp=InT; x_mean=StoP). No raw events or survey data used for clustering.

---

### Path F — Hierarchical Phenotyping (notebook 103)

**Primary data sources:**
- Phase 1 profile labels (Stage 1 split)
- `ds5_phenotype_feature_matrix.csv` for Stage 2 behavioral features (sig_hat, H_emp, x_mean)
- Path C sub-cluster labels (post-hoc comparison)
- Path A cluster labels (post-hoc comparison)
- Survey: study_condition (condition χ² within profiles), psychosocial scales

**Verdict:** **Derived from Phase 1 assignments + Step 1 StoP/InT outputs**. No raw events or survey data used for clustering.

---

### Path E — Condition-Stratified Phenotyping (notebook 104)

**Primary data sources:**
- `ds5_phenotype_feature_matrix.csv` — sig_hat, H_emp, x_mean
- `ds5_survey_features.csv` — **study_condition is the stratification variable** (essential here)
- Path A cluster labels (for ARI comparison)
- Path F cell labels (for within-profile comparison)

**Key distinction from other paths:** study_condition is **central to the analysis design**, not just an overlay. Path E is stratified BY condition. Without survey data, this path cannot run.

**Verdict:** **Behavioral features from Step 1 model outputs; condition stratification from survey data**. This is the path most dependent on survey data for its primary analysis structure.

---

### Path B — Intervention-Sensitive Phenotyping (notebook 105)

**Primary data sources:**
- `ds5_phenotype_feature_matrix.csv` — H_out_resid (condition-residualized InT feature), sig_hat, H_emp, x_mean
- `ds5_survey_features.csv` — study_condition (for within-condition sub-analyses and residualization)
- Path A, Path F, Path E labels (for cross-path comparisons)

**Key feature H_out_resid:** Requires condition assignment to compute condition-mean residuals. The InT model computes raw H_out from behavioral events; the residualization requires study_condition from survey.

**Verdict:** **Behavioral features from InT/StoP model outputs; condition-residualization requires survey data (study_condition)**. Cannot be computed without survey join.

---

### Path D — Dynamic/Stochastic Phenotyping (notebook 106)

**Primary data sources:**
- `ds5_phenotype_feature_matrix.csv` — sig_hat (StoP), H_emp (InT), chi_behav (StM)
- Path A, Path F, Path E, Path B labels (for cross-path comparisons)
- Survey: study_condition (overlay), psychosocial scales (overlay)

**Verdict:** **Derived from Step 1 StoP, InT, StM outputs**. No raw events or survey data used for clustering. Survey used for overlay only.

---

## Summary table

| Step/Path | Behavioral events | Survey data | Pre/post survey | Previous model outputs | Notes |
|---|---|---|---|---|---|
| StoP | Primary (daily X_t) | Overlay only | No | No | Pure behavioral |
| InT | Primary (event sequences) | Overlay only | No | σ̂ for H_SDE | Mostly behavioral |
| DyS | No | Overlay only | No | StoP + InT primary | Entirely derived |
| StM | For V(x) KDE | Overlay only | No | StoP + InT primary | Mostly derived |
| NeT | Primary (app sequences) | Overlay only | No | No | Pure behavioral |
| Phase 1 | No | Overlay only | No | All 5 model outputs | Entirely derived |
| Path C | No | Overlay only | No | NeT + Phase 1 | Entirely derived |
| Path A | No | Overlay only | No | StoP + InT | Entirely derived |
| Path F | No | Overlay only | No | Phase 1 + Path A/C | Entirely derived |
| **Path E** | No | **ESSENTIAL (condition stratification)** | No | StoP + InT + Paths A/F | Condition-stratified |
| **Path B** | No | **ESSENTIAL (residualization)** | No | InT + StoP + Paths A/F/E | Needs condition for H_out_resid |
| Path D | No | Overlay only | No | StoP + InT + StM + all paths | Entirely derived |

---

## What is truly behavior-derived vs questionnaire-dependent

**Truly behavior-derived (no survey needed for parameters):**
- StoP parameters: μ̂, σ̂, x_mean, sigma_mu_ratio
- InT parameters: H_out (raw), H_app, H_hour, H_emp
- NeT parameters: HHI_net, rho_self, H_trans, H_pi, I_consec
- DyS flags: is_dys_eligible, behaviorally_deterministic
- StM parameters: β_behav, T_behav, chi_behav, F_behav, V(x)

**Requires survey data to be interpretable (study_condition join):**
- All condition-level comparisons and summaries
- H_out_resid (condition residualization)
- Path E analysis structure (stratification by condition)

**Uses pre-survey psychosocial data (exploratory overlays only):**
- FoMO ~ μ̂ (StoP exploratory)
- Social media wellbeing ~ H_app (InT exploratory)
- Psychosocial overlays on all phenotype clusters (all ns after Bonferroni)

**Important conclusion:** The core model parameters (StoP, NeT) and the phenotype taxonomy (Path A k=3; Phase 1 k=2) are derived entirely from behavioral event data. They would exist even without survey responses. The survey data is needed to (a) understand what condition participants were in, and (b) explore psychosocial correlates post-hoc. The behavioral findings do not depend on the questionnaire data.

---

*Written 2026-04-20 as part of the DS5 Step 2 synthesis waypoint.*

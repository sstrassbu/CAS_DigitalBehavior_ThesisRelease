# Model and Path Data Usage Map — DS6

**Written:** 2026-08-08
**Overlap check:** Read in full before writing — `outputs/reports/stage4/post_analysis/model_data_usage_map.md`
(DS5 template, mirrored here), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md`
(cross-dataset; referenced, not re-derived), `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md`.
**Scope of this file:** DS6-only, per-family data-source accounting, in the same structure as
the DS5 template. Where DS6's *pattern* of data usage differs structurally from DS5's (not
just its numbers), that difference is stated explicitly rather than left implicit — this is
DS6's single biggest data-usage divergence and the reason this document cannot be a
find-and-replace of the DS5 version.

---

## Overview: data sources available for DS6

| Data source | File | N rows | Primary content |
|---|---|---|---|
| Behavioral events | `outputs/cleaned/ds6_behavioral_clean.csv` | 353,796 | Event-level: participant ID, timestamp, app, `study_period` (baseline/intervention), `study_condition` (control/default/intervention) — **all rows have `event_outcome_simple == 'opened'`, no dismiss/close outcome** |
| Stage 1 behavior features | `outputs/features/ds6/ds6_behavior_features.csv` | 243 | Aggregated participant-level behavioral summaries (post session-structure-bug fix: 243×67, not the earlier 77-column version) |
| Survey features (wave 1) | `outputs/features/ds6/ds6_survey_features.csv` | 243 | `addiction_index_pre`, `self_control_index_pre`, and other wave-1 psychosocial scales |
| Pre/post survey features | `outputs/features/ds6/ds6_prepost_features.csv` | 188 | `addiction_index_{pre,post,change}`, `self_control_index_{pre,post,change}` — the repeated-wave asset that motivated deferring SyD to DS6 in the first place |
| Model outputs | `outputs/model_outputs/ds6/*/` | Varies | Per-participant, per-period model parameters |

---

## The central data-usage divergence from DS5: no outcome-variance friction outcome

DS5 (and DS1/DS4) close every logged episode in one of `{opened, dismissed, closed}`. DS6
logs **only `openedApp`** — confirmed structural on the full raw file (all 353,796 rows;
`data_docs/modeling_cautions.md` §6), not a missingness artifact. This removes an entire
category of DS5 data input, not just one feature:

| DS5 quantity requiring outcome variance | Family | DS6 substitute (this data source does not exist) |
|---|---|---|
| `X_t = n_opened/n_events` (bounded [0,1] override rate) | StoP | `N_t` = daily attempt **count** (unbounded below-bounded only) |
| `H_out` (entropy over {opened, dismissed, closed}) | InT | **Excluded entirely** — a single-category distribution has entropy ≡ 0 by construction, not a measurement |
| Dismissal rate / repeated-override rate as state variable | DyS | Attempt volume (`N_t`, reused from StoP) — the paper's own first-listed §2.2 state variable |
| Resolution code / prior outcome as configuration property | StM | Target app + time-of-day only (paper's other two named §2.1 configuration properties) |
| Outcome states / combined app-outcome states as network nodes | NeT | Target apps only (paper's other named §2.4 node option) |
| Accumulated successful dismissals / accumulated overrides as stocks | SyD | `addiction_index` / `self_control_index` (survey-based; paper's other two named §2.8 stocks) |
| `commitment_score = rate_not_opened` (DS5's own GaT proxy) | GaT | **No substitute designed yet** — see `ds6_deferred_models_rationale.md`; this is a harder gap than the others because DS6 has no outcome-based candidate at all, not even an unused one |

This single structural fact — not dataset size, not survey design — is why almost every DS6
family blueprint opens with a "why this cannot be a DS5 port" section, and why DS6's data
usage looks superficially similar to DS5's (same eight model-family slots) while being built
from a fundamentally narrower raw-data menu in every single family.

A second, smaller but genuine divergence: in DS5, `study_condition` is **not** in the
behavioral file at all and must be joined from the pre-survey (`ds5_survey_features.csv`,
with one participant's condition unrecoverable). In DS6, `study_condition` **is** a native
column in `ds6_behavioral_clean.csv`, alongside `study_period` — no join, no missingness,
condition-level and period-level summaries can both be built directly from the same file. This
makes DS6's condition-level reporting mechanically simpler than DS5's, even though DS6's
condition assignment is quasi-experimental (cohort-level), not individually randomized,
throughout.

---

## Step 1 Model Implementations

### StoP — Stochastic Processes (notebook 73)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds6_behavioral_clean.csv` | `participant_id_canonical`, `event_date`, `study_period`, `study_condition` (native column, not joined) |
| Survey (overlay only) | `ds6_survey_features.csv` | `addiction_index_pre`, `self_control_index_pre` |

**What was derived from behavioral data:**
- `N_t` = daily attempt count, zero-filled grid, computed **separately per `study_period`** → entirely behavioral
- `mu_hat`, `sig_hat` (method of moments on `ΔN_t`), per period → behavioral
- `Fano_factor` = Var(N_t)/Mean(N_t), per period → behavioral
- `h_period` = `mu_hat_intervention − mu_hat_baseline` (within-participant, not between-condition) → behavioral

**What came from survey data:** psychosocial correlations only (`psychosocial_correlations.csv`, exploratory, uncorrected) — never used to derive `mu_hat`/`sig_hat`.

**Verdict:** Parameters are **purely behavioral-derived**, exactly as in DS5, but the state
variable itself (a count, not a rate) and the comparison axis (within-participant period, not
between-subject condition) are both structurally different. `study_condition` needs no join
here (unlike DS5).

---

### NeT — Network Theory (notebook 74)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds6_behavioral_clean.csv` | `participant_id_canonical`, event timestamp/row order, `app_name`, `study_period` |
| Survey (overlay only) | `ds6_survey_features.csv` | psychosocial scales |

**What was derived from behavioral data:**
- Transition edges: **self-derived via `shift(-1)` on time-sorted rows within participant × period** — this is a more conservative choice than the blueprint's own stated plan (`app_prev[t] → app_name[t]`), and more conservative than it needed to be, since `app_prev` had already been separately verified genuine (~42% same-app rate, non-mechanical). The notebook never touches `app_next` or `app_prev` at all for edge construction, matching DS5's own NeT technique exactly.
- `HHI_net`, `rho_self`, `H_trans`, stationary distribution `π` → all behavioral, per period
- `stop_net_period_comparison.csv` bridge (`hhi_change` vs StoP's `volume_change`) → behavioral, cross-family

**What came from survey data:** condition-level summaries and psychosocial overlay only.

**Verdict:** NeT is **purely behavioral event-derived**, same as DS5. The one real DS6-specific
data-quality issue this family had to clear *before* using any sequence data was verifying
that the pre-engineered `app_next`/`app_prev` columns were trustworthy — `app_next` was found
not to be (see `ds6_bug_discoveries_and_fixes_chronicle.md`), which is why the implementation
ultimately used neither column and derived transitions from row order directly instead.

---

### InT — Information Theory (notebook 75)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds6_behavioral_clean.csv` | `hour_of_day`, `app_name`, per period (fresh computation for `H_hour`) |
| Stage 1 features | `ds6_behavior_features.csv` | `app_entropy_baseline`/`app_entropy_intervention` (reused directly for `H_app`, same technique DS5's own InT notebook used: "re-framed Stage 1 features," not recomputed from scratch) |
| Survey (overlay only) | `ds6_survey_features.csv` | psychosocial scales |

**What came from previous model outputs:**
- StoP (73): `daily_series_long.csv` (zero-filled `N_t` grid) → `H_emp` (per-participant quantile bins, **not** DS5's fixed [0,1]-range bins, since `N_t` is unbounded); `sig_hat` → `H_SDE` bridge
- NeT (74): `transition_edge_list.csv`'s `app_to` (destination) marginal → `I_consec = H_app_marginal − H_trans` bridge; `H_trans` itself

**What is structurally absent:** `H_out` — no dismiss/close outcome exists to compute entropy over (see the substitution table above). This is not a computed-and-discarded quantity; it was never built.

**New relative to DS5:** a pooled `MI(study_period; app_name)` test — DS5 deferred all MI/KL
computation (FLAG 4); DS6 adds this one because it directly follows up NeT's (74) already-found
per-participant `HHI_net`-volume correlation with a population-level counterpart question.

**Verdict:** `H_app`, `H_hour`, `H_emp` are behavioral (with `H_app` specifically reusing a
Stage 1 feature rather than recomputing from raw events). `H_SDE` and `I_consec` are bridges
that depend on StoP and NeT model outputs respectively. Survey data plays no role beyond the
overlay, same as DS5.

---

### DyS — Dynamical Systems (notebook 72)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `participant_stop_parameters.csv` | `mu_hat_*`, `sig_hat_*`, per period |
| InT model outputs | `participant_entropy_metrics.csv` | `H_emp_*`, per period (bridge validation only) |
| Survey (overlay only) | `ds6_survey_features.csv` | psychosocial scales |

**What was derived:**
- `sigma_threshold_<period>` = median(`sig_hat_<period>`) — **computed separately per period**, a departure from DS5's single pooled threshold, justified by StoP's own already-documented window-length asymmetry (baseline ~15 days vs intervention ~28 days)
- `regime_<period>` ∈ {stochastic, declining, growing, resting} — a genuinely new 3-way asymmetric split within the deterministic branch, impossible under DS5's double-bounded state variable
- `regime_transition_matrix.csv` — a 4×4 within-participant baseline→intervention contingency table, which has **no DS5 equivalent at all** (DS5 only compares regimes between RCT arms, never within-subject over time)

**Verdict:** DyS is, as in DS5, **entirely derived from previous model outputs** (StoP + InT).
No raw behavioral events used directly. No survey data used for parameters. Unlike DS5, this
family produces DS6's only true within-participant longitudinal regime-transition table — an
asset DS5's between-subject-only design structurally cannot produce.

---

### StM — Statistical Mechanics (notebook 71)

| Data used | File | Columns used |
|---|---|---|
| Behavioral events | `ds6_behavioral_clean.csv` | `app_name`, `hour_of_day` (bucketed into 4 categories), per period — computed fresh |
| InT model outputs | `participant_entropy_metrics.csv` | `H_app_*` only (for the sanity-gate comparison) |
| Survey (overlay only) | `ds6_survey_features.csv` | psychosocial scales |

**What was derived:**
- `H_joint` = joint entropy of (app, hour_bucket) → behavioral, computed fresh (not reused from any prior family)
- `dominant_config`, `dominant_config_share`, `config_persistent` → behavioral
- `susceptibility` = Jensen–Shannon divergence between the baseline and intervention (app, hour_bucket) distributions → behavioral, period-boundary-based

**What is structurally absent:** any β/T/Z/F thermodynamic apparatus. Unlike DS5's StM,
which is built **entirely on top of StoP's `sig_hat`** (`β_behav = 2/σ̂²`), DS6's StM **does
not depend on StoP at all** — a genuine data-usage divergence, not just a modeling choice.
This mirrors Structured's own StM independence from its StoP, for an even stronger stated
reason (DS6's `N_t` isn't bounded on either the same way a two-state occupation probability
would need).

**Verdict:** StM is **purely behavioral-derived plus one InT cross-check**, and is the one
DS6 family with the *least* Step-1-output dependency of the six — the opposite data-usage
pattern from DS5, where StM was one of the most output-dependent families.

---

### SyD — System Dynamics (notebook 78)

| Data used | File | Columns used |
|---|---|---|
| StoP model outputs | `participant_stop_parameters.csv` | `mean_N_baseline`, `mu_hat_baseline` |
| DyS model outputs | `participant_regime_classification.csv` | `regime_baseline`, `regime_intervention` |
| Pre/post survey (**essential, not overlay**) | `ds6_prepost_features.csv` | `addiction_index_{pre,post,change}`, `self_control_index_{pre,post,change}` (N=188) |
| Survey (control variable) | `ds6_survey_features.csv` | `addiction_index_pre`, `self_control_index_pre` (used as the regression-to-the-mean control, not an overlay) |

**What was derived:**
- Two stock-flow feedback-loop tests (raw + partial correlation), both genuine null results

**Verdict:** SyD is the **first DS6 family where survey/psychosocial data is a primary
analytical input, not an overlay** — a structural departure from every other DS6 family (and
from DS5, which never built SyD at all). This is also the only DS6 family whose sample size
(N=188) is smaller than the full N=243 behavioral cohort, because it requires prepost survey
completion in addition to behavioral eligibility.

---

## Step 2 Phenotyping

### Main pass — Phenotype Exploration (notebook 140)

**Primary data sources:**
- StoP (`h_period`), NeT (`hhi_change`), InT (`H_emp_baseline`), DyS (`regime_changed`, derived binary), StM (`susceptibility`) — 5 features, one per family, **except SyD**
- SyD's `participant_stock_flow.csv` (`addiction_index_change`, `self_control_index_change`) used as the **post-hoc overlay**, not a clustering feature
- No raw behavioral events used directly

**Why SyD is excluded from clustering (a deliberate departure from the DS5/Structured "one feature per completed family" pattern):** SyD's only genuinely novel per-participant outputs are psychosocial (`addiction_index_change`/`self_control_index_change`); everything else it touched (`mean_N_baseline`, `regime_baseline`) is reused directly from StoP/DyS. DS5 and Structured both kept psychosocial variables out of the clustering feature set — DS6 follows the same rule, with SyD supplying the overlay instead of a 6th feature.

**Verdict:** **Entirely derived from Step 1 model outputs**, same as DS5 Phase 1. The
overlay is arguably better-grounded than DS5's or Structured's own overlays (which used
static wave-1 pre-scores): DS6's overlay uses the actual measured psychosocial **change**.

---

### Path A′ — Behavior-Only, DyS Removed (notebook 141)

**Primary data sources:**
- Same 5-feature source list minus DyS's `regime_changed` (4 features: `h_period`, `hhi_change`, `H_emp_baseline`, `susceptibility`)
- Main pass's `cluster_assignments.csv` (for the ARI comparison)
- SyD's `participant_stock_flow.csv` (same overlay, re-tested)

**Verdict:** **Derived entirely from Step 1 StoP/NeT/InT/StM outputs**, no raw events, no
survey data for clustering. Result was reported as an outlier characterization, not a
validated second phenotype (see `ds6_phenotype_expectation_vs_result.md`).

---

## Summary table

| Step/Family | Behavioral events | Survey data | Pre/post survey | Previous model outputs | Notes |
|---|---|---|---|---|---|
| StoP | Primary (daily N_t) | Overlay only | No | No | `study_condition` native, no join needed |
| NeT | Primary (self-derived transitions) | Overlay only | No | No | Never trusts `app_next`/`app_prev` even after clearing `app_prev` |
| InT | H_hour fresh; H_app reused from Stage 1 | Overlay only | No | StoP (H_SDE), NeT (I_consec) | H_out structurally absent |
| DyS | No | Overlay only | No | StoP + InT primary | Only family with a true within-participant transition table |
| StM | Primary (H_joint fresh) | Overlay only | No | InT (H_app, sanity check only) | Does NOT depend on StoP — unlike DS5 |
| SyD | No | **ESSENTIAL (stocks, control variable)** | **ESSENTIAL** | StoP + DyS | Only DS6 family using psychosocial CHANGE as a primary quantity |
| Phenotyping (140) | No | Overlay only (via SyD) | Overlay only | StoP+NeT+InT+DyS+StM (5 features) | SyD supplies overlay, not a clustering feature |
| Path A′ (141) | No | Overlay only (via SyD) | Overlay only | StoP+NeT+InT+StM (4 features) | DyS dropped entirely |

---

## What is truly behavior-derived vs questionnaire-dependent

**Truly behavior-derived (no survey needed for parameters):**
- StoP: `mu_hat`, `sig_hat`, `Fano_factor`, `h_period`
- NeT: `HHI_net`, `rho_self`, `H_trans`, `π`
- InT: `H_app`, `H_hour`, `H_emp`, `H_SDE`, `I_consec` (H_out does not exist to be excluded from this list)
- DyS: `regime_<period>`, `regime_changed`
- StM: `H_joint`, `susceptibility`, `config_persistent`

**Requires survey data to be interpretable, but not for computation:**
- `study_condition` is native to the behavioral file (unlike DS5) — no join required for any condition-level summary

**Essential survey/psychosocial input (not overlay), unique to SyD and to the phenotyping overlay:**
- `addiction_index_change`, `self_control_index_change` (SyD's stocks; the Step 2 overlay variable that produced DS6's only Bonferroni-significant psychosocial result)
- `addiction_index_pre`, `self_control_index_pre` (SyD's regression-to-the-mean control variables)

**Important conclusion:** As in DS5, DS6's core Step 1 model parameters (StoP, NeT, InT,
DyS, StM) and the Step 2 phenotype taxonomy are derived entirely from behavioral event data.
The one structural exception is SyD, which by design uses psychosocial survey data as a
primary quantity rather than a post-hoc overlay — this is the correct behavior for the one
family DS6 was specifically brought into the project's sequencing to enable
(`deferred_models_why_phenotyping_first.md` §2), not a departure from the project's general
behavior-first discipline.

---

*Written 2026-08-08 as part of the DS6 post-analysis reporting set.*

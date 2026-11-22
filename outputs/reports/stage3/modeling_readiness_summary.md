# Modeling Readiness Summary — Stage 3

**Written:** 2026-04-16  
**Purpose:** Per-dataset assessment of which feature groups are most valuable for modeling, which model families are best supported, and which features should be avoided or treated cautiously. Intended to guide the first real modeling implementation pass and to inform the modeling methods section of the paper.

**Required context:** Read `dataset_strengths_summary.md`, `core_comparability_summary.md`, and `data_docs/modeling_cautions.md` alongside this document.

---

## How to read this document

For each dataset, this document covers:
1. **Feature group readiness** — quality rating per feature group with actionable notes
2. **Features to use with priority** — the strongest features for individual modeling
3. **Features to avoid or treat cautiously** — from Stage 1 QC and construct mapping
4. **Best candidate model families** — what model types this dataset's structure genuinely supports
5. **Weakest candidate model families** — what to avoid or save for a better-suited dataset

---

## DS1 — Modeling Readiness

### Feature group readiness

| Feature group | Readiness | Notes |
|---|---|---|
| Volume features (total_events, events_per_day, obs_window_days) | Good | Clean; 17.4% NaN in events_per_day for single-day participants; use n_days_observed as complement |
| App diversity (n_unique_apps, app_entropy, app_herfindahl, top_app_share) | Good | Only 48 unique apps; narrow app space; but features themselves are clean |
| Temporal structure (peak_hour, hour_entropy, morning/evening/weekend shares) | Moderate | 7.5–20.2% NaN; UTC assumption introduces noise for international participants |
| Friction override rate (rate_opened, rate_dismissed, rate_closed) | Strong | Cleanest denominator in project — all events are friction events; 0.2% NaN |
| Adaptation trajectory (open_rate_change_setup) | Moderate | 33.8% NaN; setup-time axis is unique to DS1 but weaker signal than DS4 calendar-day axis |
| Override streaks (max_consecutive_opens, p_open_after_dismiss) | Moderate | Behavioral regularity proxy; some opens may be intentional and non-problematic |
| Psychosocial features (problematic_cons_pre, happy_pre) | Thin but usable | Only 527/619 have pre-survey; only 168 have pre+post; broad Likert — not validated psychometric scales |
| Pre-post change scores (problematic_cons_change, happy_change) | Limited | 168 participants only; interpret cautiously; heavy attrition may create selection bias |
| Active days per week | Avoid as primary feature | 25.5% NaN due to short windows; use events_per_day or n_days_observed instead |
| Purpose field | Do not use | 71.3% NaN; qualitative supplement only |

### Priority features for DS1 modeling

```
# Behavioral core (all participants)
rate_opened              # primary friction override rate — cleanest denominator
rate_dismissed           # compliance rate
rate_closed              # exit/close rate
app_entropy              # behavioral breadth
hour_entropy             # temporal diversity
events_per_day           # usage intensity

# Adaptation (81% of participants with setup-time data)
open_rate_change_setup   # habituation or escalation trajectory
dismiss_rate_change_setup

# Streak / behavioral regularity
max_consecutive_opens
p_open_after_dismiss

# Survey moderators (527 participants)
problematic_cons_pre
happy_pre
hours_self_reported_pre  # self-reported usage estimate
```

### Features to avoid in DS1

| Feature | Reason |
|---|---|
| `active_days_per_week` | 25.5% NaN; use `events_per_day` instead |
| `purpose` | 71.3% NaN |
| Adaptation features for participants with < 5 setup-time events | `open_rate_change_setup` is NaN for 33.8%; use NaN-aware models |
| Pre-post outcomes with large samples | Only 168 fully linked; avoid claims requiring high power |

### Best candidate model families for DS1

**1. Information-theoretic behavioral profiling**
DS1's entropy features (app_entropy, hour_entropy) are complete and clean. A participant-level behavioral diversity profile based on entropy, concentration, and temporal regularity is immediately feasible. This can characterize behavioral breadth as a phenotype dimension.

**2. Friction compliance modeling (logistic/regression)**
`rate_opened` / `rate_dismissed` / `rate_closed` as outcomes. Predictors: app diversity, temporal features, problematic consumption pre-score. Feasible with the full N=619 for behavioral predictors; N=527 for survey moderators.

**3. Stochastic event-sequence summaries**
With 407K events (after dedup), per-participant event sequences support simple Markov-chain-style summaries: transition probabilities between outcomes (opened → dismissed → closed chains). No pre-engineered sequence fields, but derivation is straightforward.

**4. Behavioral phenotyping baseline**
DS1's clean friction outcomes and moderate event volume make it a good first candidate for computing continuous phenotype dimension scores (friction sensitivity, override tendency, network centralization) as described in `phenotype_dimensions.md`.

### Weakest candidate model families for DS1

| Model family | Why it is weak in DS1 |
|---|---|
| Dynamical systems / phase models | Short observation windows; single arm; no phase boundaries |
| Network / transition models | Only 48 apps; no pre-engineered sequence fields; narrow app space limits transition richness |
| Causal/experimental analysis | No condition variable — all participants received same intervention |
| Psychosocial moderator analysis | Thin Likert scales; small fully-linked N (169 with pre+post) |
| Long-run adaptation / habit | Short windows; setup-time axis is per-participant but has high NaN |

---

## DS4 — Modeling Readiness

### Feature group readiness

| Feature group | Readiness | Notes |
|---|---|---|
| Volume features | Excellent | 0.6% NaN in events_per_day; no NaN in core identifiers or resolution |
| App diversity | Excellent | 399 unique apps; richest app space in project |
| Temporal structure | Good | 7.5% NaN; confirmed UTC; ISO-week edge case for multi-year participants |
| Friction override rate (rate_opened_intervention_events) | Good | Requires event-class filtering to intervention_event only; 3.2% NaN |
| Intervention type effects | Unique | Only dataset with 6 intervention types logged at scale; breathingExercise dominant |
| Adaptation trajectory (open_rate_change_calendar) | Strongest in project | 4.7% NaN; long calendar-day windows up to 897 days; most reliable adaptation signal |
| Engagement stability (activity_persistence, gaps_over_7d, active_weeks) | Unique | No equivalent in other datasets; long-window specific |
| Override streaks | Moderate | Computed on intervention_event class — cleaner than DS1's all-event computation |
| Duration features (mean_intervention_duration, duration_open_vs_dismiss_delta) | Moderate | 63.5% NaN for all `closedApp` events; interpret cautiously |
| Psychosocial features | Not available | Qualitative survey only; no Likert scales |
| Active days per week | Moderate | Only 0.6% NaN in DS4 (short-window problem is less severe than DS1/DS5) |

### Priority features for DS4 modeling

```
# Primary friction and behavioral core
rate_opened_intervention_events    # cleanest friction-only override rate
open_rate_change_calendar          # STRONGEST adaptation trajectory in project
duration_open_vs_dismiss_delta     # friction sensitivity proxy (time difference by outcome)

# App diversity
app_entropy
n_unique_apps
app_herfindahl
n_intervention_types_seen          # breadth of intervention exposure

# Engagement stability (unique to DS4)
activity_persistence               # consistent activity across weeks
active_weeks
gaps_over_7d                       # dropout / extended pause indicator

# Temporal
events_per_day
hour_entropy
weekend_event_share
```

### Features to avoid in DS4

| Feature | Reason |
|---|---|
| `obs_window_days_ds4` | Removed in Stage 1 QC — identical to `obs_window_days` (r=1.0) |
| `secondsSinceStudySetup` / `weeksSinceStudySetup` | Inverted semantics — all values ≤ 0; use timestamp-derived features instead |
| `purpose` | 83.1% NaN |
| Raw survey text fields | Qualitative only; no systematic feature use |
| Duration features as primary predictors | 63.5% NaN (absent for all closedApp events) |

### Best candidate model families for DS4

**1. Long-run behavioral adaptation and drift modeling**
DS4 is the strongest dataset for modeling how behavior changes over months to years. Dynamical systems approaches (e.g., identifying stable/unstable regime transitions), survival analysis (time-to-behavioral-change), and HMM-style phase models are all well-supported by the long observation windows.

**2. Habit formation and engagement stability**
`activity_persistence`, `active_weeks`, `gaps_over_7d`, and long override-rate trajectories together make DS4 the best platform for habit-strength and engagement-stability profiling.

**3. Intervention-type comparative analysis**
The 6 intervention types with the multi-class event architecture allow within-DS4 comparisons of whether participants respond differently to breathingExercise vs blackScreen vs mirror interventions. This is unique to DS4.

**4. Large-N behavioral heterogeneity profiling**
N=1,039 with 2.49M events enables robust estimation of participant-level behavioral profiles. The heterogeneity in event counts (1–42,119 per participant) makes DS4 the best candidate for identifying extreme behavioral types at both ends of the use spectrum.

**5. Information-theoretic and network analysis**
With 399 apps, the app-transition space is richest in DS4 (though sequence fields must be derived). App entropy and diversity metrics are reliable across a broad app landscape.

### Weakest candidate model families for DS4

| Model family | Why it is weak in DS4 |
|---|---|
| Psychosocial moderator analysis | Not possible — no psychometric scales |
| Experimental condition analysis | No conditions — observational only |
| Causal inference | Purely observational; cannot attribute behavioral change to friction |
| Pre-post intervention evaluation | No pre-intervention behavioral baseline; post-survey only, qualitative |

---

## DS5 — Modeling Readiness

### Feature group readiness

| Feature group | Readiness | Notes |
|---|---|---|
| Volume features | Good | 12.4% NaN in events_per_day for single-day participants; use n_days_observed as complement |
| App diversity | Good | Rich app space; features clean |
| Temporal structure | Good | Proper timezone handling; 7.5% NaN typical |
| Friction override rate (rate_opened with condition join) | Strong | Must join condition from pre-survey; restrict control group for friction-specific analysis |
| Experimental condition | Critical — join required | `study_condition` from pre-survey join; already handled in `build_ds5_behavior_features()` |
| Adaptation trajectory (open_rate_change_calendar) | Moderate | 16.6% NaN; shorter windows than DS4 — less reliable per-tertile estimates |
| Reintervention parameters | Unique | `timeIntervalUntilReIntervention` — reintervention group only (77.9% NaN overall); DS5-specific |
| Psychosocial scales (belonging, ostracism, FoMO) | Strongest in project | 99.8% pre-survey coverage; validated instruments |
| Pre-post change scores | Good | 284 participants with all three files; best fully-linked psychosocial N in project |
| Override streaks | Moderate | Computed on all events; condition-stratified interpretation needed |
| Duration features | Moderate | Available but binary (0 for opened, 6s for dismissed) — less continuous than DS4 |
| Active days per week | Avoid | 26.7% NaN due to short windows |
| Suggestion columns | Do not use | 99%+ NaN; reintervention group only |
| Termination reason | Do not use | Only 12 non-null rows |
| `reason` field | Qualitative supplement only | 42.3% NaN; German free text; not systematically featurized |

### Priority features for DS5 modeling

```
# Experimental backbone (join from pre-survey)
study_condition           # control / default / reintervention — essential grouping variable

# Primary friction outcomes (condition-stratified)
rate_opened               # for default + reintervention; exclude control for friction analysis
rate_dismissed
rate_closed
open_rate_change_calendar

# Psychosocial moderators (pre-survey, N=572)
belong_mean_pre           # social belonging
ostracism_mean_pre        # social exclusion
fomo_mean_pre             # fear of missing out (10-item validated)

# Pre-post psychosocial outcomes (N=284)
belong_change
ostracism_change
fomo_change
digital_wellbeing_pre / digital_wellbeing_post

# Reintervention-specific (N=263)
timeIntervalUntilReIntervention  # reintervention delay window
open_rate_intervention_events    # friction-specific within reintervention condition

# Behavioral features
app_entropy
hour_entropy
events_per_day
```

### Features to avoid in DS5

| Feature | Reason |
|---|---|
| `active_days_per_week` | 26.7% NaN; use `events_per_day` instead |
| `friction_override_rate` for control condition | Control has no friction — their `rate_opened` is not override; exclude control for cross-dataset friction comparison |
| `suggestion*` columns | 99%+ NaN |
| `terminationReason` | 12 non-null rows |
| `reason` as systematic feature | 42.3% NaN; German text |

### Best candidate model families for DS5

**1. Experimental condition comparison (statistical regression / mixed-effects)**
DS5 is the only RCT. Comparing behavioral outcomes (rate_opened, rate_dismissed, adaptation trajectory) across control/default/reintervention conditions is the primary causal analysis available in the project. Mixed-effects models with condition as a fixed effect and participant as a random effect are directly supported.

**2. Psychosocial moderator analysis**
Predicting friction response from belonging, ostracism, and FoMO — before the intervention (pre-survey as predictor → behavioral outcome during intervention). This is the highest-priority paper contribution from DS5 and cannot be replicated in DS1 or DS4.

**3. Behavioral phenotyping with psychosocial grounding**
Phenotype dimensions (friction sensitivity, override tendency, adaptation) can be computed from behavioral features and then related to validated psychosocial scale scores. DS5 is the only dataset where phenotype dimensions have validated external correlates.

**4. Stochastic event-sequence modeling with condition stratification**
Event sequences within each condition provide condition-stratified transition probability estimates. Comparing within-condition Markov-chain summaries (control vs default vs reintervention) directly tests whether the intervention structure changes behavioral dynamics.

**5. Pre-post intervention evaluation**
`belong_change`, `fomo_change`, `ostracism_change` as outcomes for the 284 fully-linked participants. These are psychosocial intervention outcomes — asking whether the friction intervention changed social well-being perceptions. Unique to DS5.

**6. Survival/time-to-event analysis**
Time-to-habituation or time-to-dropout, stratified by condition. Does the reintervention delay slow the habituation rate compared to the default condition?

### Weakest candidate model families for DS5

| Model family | Why it is weak in DS5 |
|---|---|
| Long-run adaptation / habit | Shorter observation windows than DS4; tertile estimates less reliable |
| Network / sequence models | No pre-engineered sequence fields; transition derivation overhead |
| Substitution analysis | Requires sequence derivation; not as clean as DS6's pre-built fields |
| Cohort / repeated-measures across waves | DS5 has only one pre + one post survey (not 3 waves); no within-intervention repeated measurement |

---

## DS6 — Modeling Readiness

### Feature group readiness

| Feature group | Readiness | Notes |
|---|---|---|
| Volume features | Good | 0.4% NaN in events_per_day; clean core |
| App diversity | Good | Rich app space; entropy features clean; baseline/intervention split available |
| Temporal structure | Good | Confirmed UTC; participation_day and period provide structured temporal context |
| Behavioral response (event_rate_ratio_intervention_vs_baseline) | Good with filter | Requires n_baseline_days >= 7; 235/243 eligible; 7 participants excluded |
| Session structure | **Not real** — removed 2026-08-05 | group_id verified unique per row, no equivalent to session grouping in this dataset |
| Sequence / transition features | Unique and strong (corrected 2026-08-06) | app_prev/app_prev2 up to depth 2 usable directly; app_next2 usable with conditioning; app_next/app_next3 NOT usable (mechanical artifact) |
| Period-split features (*_baseline, *_intervention) | Available | DS6-specific; baseline reference period enables within-participant comparison |
| Psychosocial scales (self_control, addiction, FoMO, trivsel) | Strong | 100% coverage for wave 1; repeated waves available |
| Pre-post survey outcomes | Good | 188/243 with pre+post; repeated measurement enables within-person change analysis |
| Friction override / compliance | Not available | ALL outcomes are 'opened' — cannot compute at event level |
| self_transition_rate | **Now usable (corrected 2026-08-06)** | Recomputed on app_prev: mean=0.512, sd=0.217 — was near-constant (0.989/0.018) only because it used the buggy app_next field |
| cross_app_transition_rate | Now usable, same correction | = 1 − self_transition_rate, now on app_prev basis |
| reintervention_open_rate | Removed | Always 1.0 for DS6 — removed in Stage 1 QC |
| resolution_next_open_rate | Removed 2026-08-06 | Near-constant-near-zero (0.5%) — same look-ahead-mechanics cause as app_next |
| app_entropy_baseline + app_entropy_intervention | Use cautiously | High correlation with app_entropy (r=0.979, 0.967); use app_entropy + app_entropy_change (intervention − baseline) |

### Priority features for DS6 modeling

```
# Primary behavioral response proxy
event_rate_ratio_intervention_vs_baseline   # filter: n_baseline_days >= 7
                                             # (session_rate_ratio removed 2026-08-05 —
                                             #  exact duplicate, group_id has no real sessions)
event_rate_slope                            # longitudinal slope across participation_day

# Sequence and substitution (corrected 2026-08-06 -- app_prev-based, not app_next)
app_transition_entropy                      # substitution diversity (was app_next_entropy)
n_unique_transition_apps                    # breadth of app transitions (was n_unique_next_apps)
self_transition_rate                        # now usable directly: mean=0.512, sd=0.217

# Period-split behavioral features
app_entropy_change                          # intervention − baseline entropy change
events_per_day (compare across periods)

# Session structure: NONE AVAILABLE -- group_id verified non-functional 2026-08-05,
# do not reference n_sessions_*/session_rate_*/mean_session_duration_* (removed, never existed
# as real data)

# Psychosocial moderators (all 243 participants)
self_control_index_pre
addiction_index_pre
fo_mo_pre
trivsel_pre                                 # well-being
socialconnection_pre

# Pre-post psychosocial outcomes (188 participants)
self_control_index_change
addiction_index_change
trivsel_change

# Condition and design
study_condition                             # control / default / intervention (in behavioral file)
period                                      # baseline / intervention
participation_day                           # study-day index
```

### Features to avoid in DS6

| Feature | Reason |
|---|---|
| `friction_override_rate` | Structural NaN for all DS6 — do not impute; different construct |
| `reintervention_open_rate` | Removed in Stage 1 QC — always 1.0 |
| `resolution_next_open_rate` | Removed 2026-08-06 — near-constant-near-zero |
| `app_next`, `app_next3` | Not usable — mechanically echo current app 99.3% of the time (2026-08-06 finding); use `app_prev`/`app_next2` |
| `n_sessions_*`, `session_rate_*`, any "session structure" feature | Never real — group_id verified non-functional 2026-08-05 |
| `app_entropy_baseline` + `app_entropy_intervention` + `app_entropy` simultaneously | High collinearity; use app_entropy + app_entropy_change |
| Participants with n_baseline_days < 7 for behavioral_response_ratio | Unreliable baseline estimate; extreme ratios (77x, 12x) |

### Best candidate model families for DS6

**1. Network / transition and substitution modeling**
Pre-engineered `app_prev`/`app_next2` fields (not `app_next`, verified non-functional 2026-08-06 — see `data_docs/modeling_cautions.md` §6) make DS6 the natural first dataset for app-transition network analysis and substitution behavior. No real session grouping exists (`group_id` verified non-functional 2026-08-05). Who switches to which apps after a friction encounter? Does the condition affect the substitution pattern?

**2. Dynamical systems / phase modeling**
The explicit baseline → intervention phase structure is the best-supported framework for testing whether the intervention creates a detectable behavioral phase shift. Comparing event-rate trajectories across participation days, within and across conditions, directly supports state-space or attractor-based modeling.

**3. Repeated psychosocial moderator analysis**
`self_control_index` and `addiction_index` are the strongest self-control and problematic-use moderators in the project. With 100% pre-survey coverage and 3-wave repeated surveys, DS6 is the best platform for longitudinal psychosocial change modeling.

**4. ~~Session-level stochastic modeling~~ — removed, see correction**
**⚠ Correction (2026-08-07):** this item previously claimed the `group_id` session structure enables session-level HMM/Markov-chain modeling (within-session event transitions, session length distributions, within-session behavioral patterns). Verified false 2026-08-05: `group_id` is unique per row and does not group events into sessions (see `data_docs/modeling_cautions.md` §6, `outputs/reports/stage0/ds6_audit_report.md` §8a). No session-level stochastic modeling is possible in DS6. Ordinary event-sequence stochastic modeling on `app_prev`/`app_next2` (item 1 above) remains valid and is DS6's genuine strength here.

**5. Information-theoretic period comparison**
`app_entropy_change` (intervention − baseline entropy shift) directly quantifies whether the intervention altered the diversity of the app use portfolio. This is a clean information-theoretic intervention effect measure unique to DS6.

### Weakest candidate model families for DS6

| Model family | Why it is weak in DS6 |
|---|---|
| Friction override / compliance modeling | Structurally impossible — all outcomes are 'opened' |
| Individual RCT-based causal inference | Quasi-experimental (cohort assignment); DS5 is stronger for this |
| Large-N statistical power | Smallest N (243) — limits subgroup analysis and interaction detection |
| Long-term naturalistic habit modeling | Windows defined by study design; shorter than DS4 |

---

## Cross-dataset modeling readiness matrix

| Model family | DS1 | DS4 | DS5 | DS6 |
|---|---|---|---|---|
| Statistical regression / GLM / mixed-effects | Moderate | Moderate | **Strong** | Moderate |
| Survival / time-to-event | Moderate | **Strong** | **Strong** | Moderate |
| Markov chains / HMM / stochastic process | Moderate | **Strong** | **Strong** | **Strong** |
| Information-theoretic summaries | **Strong** | **Strong** | **Strong** | **Strong** |
| Network / transition models | Weak | Moderate | Moderate | **Strong** |
| Dynamical systems / phase models | Weak | **Strong** | Moderate | **Strong** |
| Agent-based models | Moderate | **Strong** | **Strong** | Moderate |
| Psychosocial moderator analysis | Weak | Not suitable | **Best** | **Strong** |
| System dynamics / feedback loops | Weak | Moderate | Moderate | **Strong** |
| Friction override / compliance | **Strong** | Good | **Strong** | Not suitable |
| Experimental condition / causal | None | None | **Best (RCT)** | Moderate |

---

## Key cross-dataset insights for modeling strategy

### Insight 1: No single dataset does everything

Each dataset has a distinct modeling niche:
- **DS1**: lean pipeline testing; cleanest friction denominator; thin psychosocial
- **DS4**: long-term habit and adaptation; no psychosocial; largest event volume
- **DS5**: causal friction analysis + psychosocial moderators; best paper contribution layer
- **DS6**: substitution, session dynamics, repeated psychosocial; richest but most complex

A complete paper-level analysis will eventually touch all four. The question is which to start with.

### Insight 2: DS5's RCT is a paper-quality asset

The fact that DS5 is the only RCT means that any behavioral finding from DS5 is causally attributable to the intervention in a way that DS1, DS4, and DS6 cannot match. This is a strong paper-quality advantage. Psychosocial moderator analysis within DS5 (who responds more to friction, based on pre-survey FoMO/belonging/ostracism scores) is a contribution that cannot be replicated by any other dataset in this project.

### Insight 3: DS6's structural incompatibility is not a weakness — it is a different construct

The fact that DS6 cannot compute friction override rate forces a more nuanced behavioral response model (volume change across periods). This is not a limitation in the pejorative sense — it is a different operationalization of behavioral response to friction. For the paper, this can be framed as: "two complementary behavioral response constructs are examined — event-level outcome classification (DS1/DS4/DS5) and period-level volume change (DS6)."

### Insight 4: DS4's longitudinal depth is irreplaceable

No other dataset comes close to 897-day observation windows. If the paper includes anything about long-run behavioral adaptation, habit formation, or engagement stability over months, DS4 is the only viable foundation. The absence of psychosocial moderators is a real limitation, but behavioral heterogeneity analysis at scale is uniquely supported by DS4.

### Insight 5: Start with a single dataset — the pipeline scales later

Given the multi-model family strategy (try multiple model implementations on one dataset first), the right first dataset is the one that supports the widest range of model families while remaining implementation-feasible. DS5 leads here because its RCT structure means that even simple models produce interpretable results, and its psychosocial layer enables moderator analysis from the first model pass.

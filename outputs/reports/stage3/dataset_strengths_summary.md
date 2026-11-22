# Dataset Strengths Summary — Stage 3 Planning

**Written:** 2026-04-16  
**Purpose:** Paper-facing and decision-support reference. Synthesizes all Stage 1 QC findings, dataset overviews, construct mappings, harmonization notes, and proxy documentation into a single per-dataset profile. Use this before choosing which dataset to model first, before writing dataset sections of the paper, and before any cross-dataset claim.

---

## How to read this document

Each dataset section covers:
- study design and population
- behavioral coverage (events, participants, observation windows)
- friction outcome quality — the central construct
- longitudinal / adaptation depth
- sequence and session structure
- psychosocial and survey depth
- main limitations
- best use cases (what this dataset is genuinely good for)
- model family suitability (what model types this dataset supports and which it does not)

All claims are grounded in confirmed audit findings, Stage 1 QC notes, and feature extraction outputs. Nothing here is speculative interpretation unless explicitly flagged.

---

## DS1 — Compact Friction Intervention Testing

### Study design and population

DS1 is a **compact single-arm field study** testing the default OneSec friction intervention. There is no experimental control group and no randomization. Participants are self-selected adult OneSec users (international mix). The study design is closest to a **naturalistic before/after observation with a fixed intervention exposure**.

| Property | Value |
|---|---|
| N behavioral | 619 |
| N pre-survey | 527 (85.1% of behavioral) |
| N pre + post survey | 168 (27.1% of behavioral) |
| N all three files linked | 169 |
| Total events (after dedup) | ~399,000 |
| Unique apps | 48 (Instagram dominant at 41%) |
| Observation window | Short (no median published, but setup-time axis confirms short windows) |
| Study design type | Non-experimental, single-arm |
| Condition structure | None — all participants receive the same default intervention |

### Behavioral coverage and friction outcome quality

DS1 has **the cleanest all-events friction outcome** in the project. Every event in DS1 is a friction-triggered event — there are no non-friction events in the behavioral log. The three resolution values are well-distributed and directly interpretable:

| Resolution | Count | Share |
|---|---|---|
| `openedApp` | 203,295 | 49.9% |
| `dismissedAppOpening` | 105,074 | 25.8% |
| `closedApp` | 98,223 | 24.1% |
| NaN | 468 | 0.1% |

This means `rate_opened` in DS1 is a genuine all-events friction override rate, not a filtered subset rate. The denominator is transparent: all outcome-bearing events are friction events. This is the strongest denominator clarity in the project for this construct.

The adaptation trajectory feature (`open_rate_change_setup`) uses the `secondsSinceOneSecSetup` time axis — a per-participant time since app installation, not calendar time. This is meaningful but **differs from DS4/DS5's calendar-day axis**. It is 18.9% NaN overall, and 33.8% of participants have insufficient setup-time events for reliable tertile computation.

**Friction outcome rating: High quality, cleanest denominator, but no experimental condition to attribute any change to.**

### Longitudinal depth

DS1 has the **shortest observation windows** among the four datasets. There is no published median duration, but the setup-time axis (`secondsSinceOneSecSetup`) ranges from 76 seconds to 64.7 days per event, and many participants have short observation periods. The `active_days_per_week` feature is NaN for 25.5% of participants due to windows under 7 days. This limits the strength of any longitudinal or adaptation claim: short windows mean the early-vs-late tertile split has smaller and noisier samples than DS4.

**Non-experimental caution:** Even with longitudinal features, changes over time in DS1 cannot be causally attributed to friction exposure. Trends may reflect attrition (those who keep using the app may be different from those who stop), app version changes, or life context shifts.

### Sequence and session structure

No pre-engineered sequence fields. App-to-app transitions must be derived by sorting events by participant and timestamp. This is feasible but requires additional feature engineering work. The behavioral log is event-level only — no session grouping information.

### Survey and psychosocial depth

DS1's psychosocial coverage is **thin but real**: `problematic_cons_pre` and `happy_pre` are validated 1–7 Likert items. These are broad subjective ratings rather than validated psychometric scales. They are usable as moderators, but their construct coverage is much thinner than DS5's belonging/ostracism/FoMO battery or DS6's addiction and self-control indices.

Pre-post change scores (`problematic_cons_change`, `happy_change`) are available for only 168 participants — the small fully-linked N limits statistical power for pre-post modeling.

DS4's post-survey has only 283 linked participants and is qualitative-only. DS1 is actually the second-best dataset for simple Likert-based psychosocial coverage after DS5 and DS6, but a distant second.

### Key limitations

- No experimental condition — all participants receive the same default intervention; causal inference is very limited
- Small fully-linked N (169) for pre/post analysis
- `purpose` is 71.3% NaN — not viable as a systematic behavioral context feature
- UTC timestamp assumption — no timezone column; international participants may have non-UTC local times, creating noise in temporal features (peak hour, morning/evening shares)
- 575 participants completed the pre-survey but have NO behavioral data — they cannot be included in any behavioral modeling
- 48 unique apps is narrow compared to DS4 (399 apps) — the app diversity space is constrained

### Best use cases

- **Baseline friction behavior profiling** — cleanest all-events override rate makes DS1 ideal for descriptive work on what fraction of friction events are overridden, dismissed, or closed
- **Setup-time adaptation modeling** — the `secondsSinceOneSecSetup` axis is unique to DS1 and provides a per-participant time-since-setup proxy for habit formation
- **Lean initial pipeline testing** — DS1 is the least complex dataset; preprocessing and feature extraction are already fully done; ideal for first-pass model implementation
- **Cross-dataset baseline comparison** — DS1 Group A features (entropy, app diversity, temporal patterns) are directly comparable to the other three datasets

### Model family suitability

| Model family | Suitability | Reason |
|---|---|---|
| Statistical regression / GLM | Moderate | No condition → limited causal leverage; psychosocial moderators thin; but feasible for predictive modeling of override rate |
| Survival / time-to-event | Moderate | Event timing available; short windows limit trajectory analysis |
| Markov chains / HMM / stochastic process | Moderate | Event sequences derivable; no session structure; moderate event volume |
| Information-theoretic summaries | Strong | App entropy, hour entropy, temporal diversity features all complete and clean |
| Network / transition models | Weak | No pre-engineered transition fields; requires derivation; only 48 apps |
| Dynamical systems / phase models | Weak | Short observation windows; single arm; hard to identify phase boundaries |
| Agent-based models | Moderate | Behavioral heterogeneity visible; but moderator layer too thin for rich agent parameterization |
| System dynamics | Weak | No feedback-loop observables; no repeated survey waves |

---

## DS4 — Large Non-Experimental Retrospective Data

### Study design and population

DS4 is the **largest dataset in the project**: 1,039 participants, 2,490,260 behavioral events, observation range from 2020-09-30 to 2023-04-02. It is **fully non-experimental and retrospective** — it captures naturally occurring OneSec use data from existing users who chose to use the app without being recruited into a study. The design is observational in the strongest sense: no condition assignment, no control group, no survey administered at a specific study point.

| Property | Value |
|---|---|
| N behavioral | 1,039 |
| N survey linked | 283 (27.2% of behavioral) |
| N behavioral only | 756 |
| Total events | 2,490,260 |
| Unique apps | 399 |
| Observation window | Median 66 days; max 897 days (~2.5 years) |
| Study design type | Non-experimental, observational, retrospective |
| Condition structure | None |

### Behavioral coverage and friction outcome quality

DS4 has a **three-class event architecture** that is unique in the project:

| Event class | Share | Notes |
|---|---|---|
| `app_close_event` | 47.1% | Close events; no friction shown; no intervention fields |
| `intervention_event` | 36.5% | Friction shown; has interventionType, interventionDuration |
| `no_intervention` | 16.4% | Opens/dismisses without friction logged |

This means the friction override rate must be computed **on the intervention_event class only**, using `rate_opened_intervention_events`. Raw mixing of event classes would misrepresent the friction override construct. The denominator is narrower than DS1/DS5 (36.5% of events), but the signal is arguably cleaner for friction specifically: only events that actually received friction are in the denominator.

Intervention types are explicitly logged for all intervention_events: breathingExercise (60.7%), minimalBreathingExercise (14.9%), followTheDot (14.4%), blackScreen (5.9%), mirror (4.0%). This makes DS4 the **only dataset with multi-type intervention coverage** in a directly usable form.

Two undocumented resolution values were discovered: `dismissedByStructuredIntervention` (806 events, 0.03%) and `dismissedWithHealthyAlternative` (6 events). These are mapped in the cleaning pipeline but represent non-standard friction responses.

**Friction outcome rating: Good, but requires event-class filtering. Cleanest friction-only denominator after filtering, but different from DS1/DS5's all-events denominator.**

### Longitudinal depth

DS4 has the **strongest longitudinal depth in the project** by a wide margin. With a median observation window of 66 days and a maximum of ~897 days, many participants have months to years of behavioral data. This creates unique opportunities:

- The `open_rate_change_calendar` (adaptation trajectory) uses calendar-day tertiles with large, reliable samples per tertile
- `activity_persistence` and `gaps_over_7d` capture engagement stability and dropout patterns over real time
- `active_weeks` provides week-level engagement breadth (with a minor ISO-week edge case for multi-year participants)

This longitudinal depth is what makes DS4 the **single best dataset for modeling behavioral adaptation, habit formation, and long-term drift**. No other dataset in the project comes close to 897-day observation windows.

**Non-experimental caution:** As with DS1, longitudinal trends in DS4 cannot be causally attributed to friction alone. Users who remain active over 2+ years are a selected subsample. Attrition is non-random. Life context changes, app version updates, and self-selection all confound longitudinal trajectories.

### Sequence and session structure

No pre-engineered sequence fields. App-to-app transitions must be derived from timestamp ordering across the 2.49M event log. With 399 unique apps, there is much richer app-diversity information than DS1, but the derivation overhead is substantial. DS4 does not have session grouping, baseline period markers, or participation-day indexing.

### Survey and psychosocial depth

DS4's survey is the **weakest psychosocial layer in the project**: post-survey only, entirely qualitative, and only 283 of 1,039 participants completed it. Fields include `reason_use`, `benefits`, `negatives`, `usage_format`, `comments` — all open text. There are no Likert-scale items, no validated psychometric instruments, no pre-post design. Age and gender are available in the survey but for the 283-participant subset only.

**DS4 should not be used for any analysis requiring psychosocial moderators. It is a purely behavioral dataset for this purpose.**

### Key limitations

- No experimental conditions — no condition variable exists; all participants are naturalistic users
- Survey entirely qualitative: no Likert scales, no psychometric instruments, no pre-intervention baseline
- Only 283 participants have linked behavioral + survey data
- `secondsSinceStudySetup` and `weeksSinceStudySetup` are **inverted** relative to the codebook — they count backwards from an export anchor, not forward from setup. Must reconstruct time axis from `timestamp` directly.
- `interventionDuration` and `interventionType` are NaN for 63.5% of events (all `app_close_event` rows)
- `purpose` is 83.1% NaN — not usable
- ISO week edge case in `active_weeks` for multi-year participants causes slight undercount
- Non-random attrition over long windows — long-window participants are a selected subsample

### Best use cases

- **Long-run behavioral adaptation and habit modeling** — the only dataset where multi-year adaptation trajectories are observable
- **Heterogeneity profiling from behavioral data alone** — large N and many long-window participants support robust behavioral phenotyping without survey moderators
- **Intervention type effects** — the only dataset with clean multi-type intervention logging at scale (breathingExercise vs followTheDot vs blackScreen etc.)
- **Drift and attractor modeling** — sustained repeated-behavior data over months supports dynamical-systems style characterization
- **Large-N behavioral comparison baseline** — largest event volume; most reliable estimates of population-level app use patterns

### Model family suitability

| Model family | Suitability | Reason |
|---|---|---|
| Statistical regression / GLM | Moderate | Large N is an asset; no condition or psychosocial moderators limit interpretive depth |
| Survival / time-to-event | Strong | Long windows ideal for time-to-dropout, time-to-habituation analyses |
| Markov chains / HMM / stochastic process | Strong | High event volume; long sequences per participant; event-class structure is useful |
| Information-theoretic summaries | Strong | Entropy features complete; 399 apps → richer diversity signal |
| Network / transition models | Moderate | Derivable; 399-app space is rich; requires engineering work |
| Dynamical systems / phase models | Strong | Best longitudinal depth in project; long windows support phase detection and drift modeling |
| Agent-based models | Strong | Large N + behavioral heterogeneity (1–42,119 events per participant) |
| Psychosocial moderator analysis | Not suitable | No psychometric scales; qualitative survey only |
| System dynamics | Moderate | Long time-series supports feedback loops; no repeated survey to track psychosocial state |

---

## DS5 — German Adolescents, Three-Condition RCT

### Study design and population

DS5 is the **only full randomized controlled trial (RCT) in the project**. Three conditions were randomized:
- **Control** (N=265): no friction intervention; normal app use
- **Default** (N=264): standard OneSec friction intervention
- **Reintervention** (N=263): friction intervention with a structured reintervention delay before the user can proceed

Participants are German adolescents (ages approximately 13–25). This is the **only dataset where causal claims about the intervention are defensible** — at least within the constraints of an app-based field study.

| Property | Value |
|---|---|
| N behavioral | 573 |
| N pre-survey | 572 (99.8% of behavioral) |
| N post-survey | 284 (49.6% of behavioral) |
| N all three files linked | 284 |
| Total events | 288,688 |
| Unique apps | Not pre-counted but rich (broader than DS1) |
| Observation window | Shorter than DS4; details per-participant |
| Study design type | Experimental RCT — three conditions |
| Condition structure | Control / default / reintervention |

**Critical:** `study_condition` is NOT in the behavioral file. It must be joined from the pre-survey file (`cond` column). This join is already handled in `build_ds5_behavior_features()`, but if you reload `ds5_behavioral_clean.csv` directly, condition will be missing.

### Behavioral coverage and friction outcome quality

DS5's resolution distribution is well-balanced:

| Resolution | Share |
|---|---|
| `openedApp` | 61.6% |
| `dismissedAppOpening` | 21.5% |
| `closedApp` | 15.6% |
| NaN | 1.2% |
| `dismissedByStructuredIntervention` | 0.04% |

The overall `rate_opened` captures all events across all conditions. This is equivalent to DS1's denominator but includes the control group — **and the control group has no friction exposure**. For cross-dataset comparison or for friction-specific analysis, **restrict to default and reintervention conditions** (excludes 265 control participants). For within-dataset condition comparisons, include all three conditions and use `study_condition` as the grouping variable.

The adaptation trajectory (`open_rate_change_calendar`) uses calendar-day tertiles, consistent with DS4. NaN rate is 16.6% within DS5 (shorter windows than DS4 reduce reliability of tertile estimates for participants with fewer events).

DS5 also uniquely captures `timeIntervalUntilReIntervention` for the reintervention group (77.9% NaN overall, but fully available for the 263 reintervention participants). This is a variable unique to DS5 that quantifies the waiting window before the user can retry — a direct intervention parameter with no equivalent elsewhere.

`interventionDuration` is confirmed as 0 for opened events and 6 (seconds) for dismissed events — a binary rather than continuous measure in DS5, unlike DS4 where duration varies continuously.

**Friction outcome rating: Strong. Clean three-outcome structure. RCT condition enables direct comparison of friction response rates across groups. Most interpretively powerful friction dataset in the project.**

### Longitudinal depth

DS5 observation windows are shorter than DS4. The adaptation signal is weaker than DS4's for this reason — smaller tertile samples per participant and more noise in early-vs-late rate comparisons. However, the **condition structure compensates**: trajectories within conditions are causally cleaner than DS1 or DS4's non-experimental trajectories.

Within the reintervention condition, `timeIntervalUntilReIntervention` provides a within-event temporal depth that is unique to DS5: it captures the delay pattern within a single friction encounter, not just across encounters.

### Sequence and session structure

No pre-engineered sequence fields. Transition derivation requires sorting by participant and timestamp. However, the behavioral file is richer than DS1 (larger N, more events) and has a timezone-aware timestamp (`timezone` column) that enables accurate local-time sequence analysis — better than DS1's UTC assumption.

The `reason` field (42.3% NaN, German free text) is the closest thing to in-the-moment behavioral context annotation in DS5. It is too sparse and unstructured for routine feature use, but valuable as a qualitative supplement for understanding why users opened apps despite friction.

### Survey and psychosocial depth

DS5 has the **richest validated psychosocial battery in the project**:

- **Belonging** (`belong_mean_pre`): 8-item scale measuring social belonging
- **Ostracism** (`ostracism_mean_pre`): 5-item scale measuring perceived social exclusion
- **FoMO** (`fomo_mean_pre`): 10-item validated Fear of Missing Out scale
- **Digital well-being** (`digital_wellbeing`), perceived time use, problem awareness

Pre-survey is available for 99.8% of behavioral participants (572/573). Post-survey is available for 49.6% (284). This is the best pre-survey coverage in the project, and the pre-post linkage is cleaner than DS1's (169 vs 284 fully linked).

Pre-post change scores for all psychosocial scales (`belong_change`, `fomo_change`, etc.) are available for the 284 three-file participants. These are **the strongest psychosocial outcomes for intervention evaluation in the project**.

Survey limitation: one participant (0.2%) has no pre-survey record and gets NaN condition — negligible.

**DS5 is the only dataset where psychosocial moderator analysis of RCT outcomes is possible. This is a major paper contribution.**

### Key limitations

- Control condition's `rate_opened` reflects friction-free app opens — **not** friction override behavior; control participants must be excluded from friction-specific cross-dataset comparisons
- `reason` is 42.3% NaN and in German free text — not analyzable without categorization work
- Suggestion-related columns (`suggestionBannerShown`, `suggestionDetailView*`) are 99%+ NaN — not usable for most participants
- `terminationReason` has only 12 non-null rows — essentially unusable
- Shorter observation windows than DS4 — adaptation features are less reliable
- No pre-engineered sequence fields — transition work requires derivation

### Best use cases

- **Causal inference about intervention effects** — the only RCT; condition comparison is the primary causal lever
- **Psychosocial moderator analysis** — belonging, ostracism, FoMO as predictors of friction response; paper-quality contribution
- **Intervention response prediction** — predicting who responds to friction (default condition) vs who habituates (reintervention condition) using pre-survey psychosocial features
- **Phenotypic subgroup identification** — with condition structure and psychosocial depth, DS5 is the strongest dataset for identifying behavioral phenotypes with interpretable moderators
- **Pre-post psychosocial change modeling** — belonging_change, fomo_change as intervention outcomes for the 284 fully-linked participants

### Model family suitability

| Model family | Suitability | Reason |
|---|---|---|
| Statistical regression / GLM / mixed-effects | Strong | RCT condition + psychosocial moderators + pre-post structure = strongest setup for regression in the project |
| Survival / time-to-event | Strong | Event timing + condition structure enables condition-stratified survival analysis |
| Markov chains / HMM / stochastic process | Strong | Three-condition structure enables within-condition transition modeling |
| Information-theoretic summaries | Strong | Entropy features complete; condition can be used as grouping variable |
| Network / transition models | Moderate | Derivable; condition-stratified transition analysis is feasible |
| Dynamical systems / phase models | Moderate | Windows shorter than DS4; condition structure helps identify phase differences |
| Agent-based models | Strong | Three conditions allow agent-type parameterization by condition and psychosocial profile |
| Psychosocial moderator analysis | Strong (best in project) | Validated scales + RCT structure; no other dataset supports this combination |
| System dynamics | Moderate | Shorter windows than DS4; no repeated survey waves; but condition structure provides leverage |

---

## DS6 — Danish Adolescents, Quasi-Experimental

### Study design and population

DS6 is a **longitudinal quasi-experimental study** with Danish adolescents aged 13–17 in school cohorts. The design includes an explicit **baseline phase** (before any intervention) followed by an **intervention phase**. Conditions are assigned at the school/cohort level, not by individual randomization — this is the key difference from DS5's RCT.

Three conditions are present:
- **Control**: no intervention
- **Default**: standard friction intervention
- **Intervention**: enhanced friction intervention (Denmark-specific intervention type)

DS6 is the **youngest sample in the project** (13–17) and the **only dataset with a true pre-intervention behavioral baseline period**. All other datasets either lack an explicit baseline or capture no pre-intervention behavioral events.

| Property | Value |
|---|---|
| N behavioral | 243 |
| N survey | 243 (100% coverage — all behavioral participants) |
| N pre + post survey | 188 (77.4% of behavioral) |
| N demographics linked | 243 (all) |
| Total events (session file) | 353,796 |
| Total events (baseline file) | 195,515 |
| Unique apps | Not counted separately but covered across both files |
| Observation window | Structured by study design: baseline then intervention |
| Study design type | Experimental, quasi-experimental (school cohort assignment) |
| Condition structure | Control / default / intervention |

### Behavioral coverage and friction outcome quality — critical structural limitation

DS6 has a fundamental structural incompatibility with the other three datasets: **ALL behavioral events in DS6 have `resolution == 'openedApp'`**. There are no dismiss or close outcome events in either behavioral file. This is not a data error — it reflects that DS6's behavioral logging captures only app-opening events.

Consequences:
- `friction_override_rate` is **structurally NaN** for all 243 DS6 rows — this is not missing data and should never be imputed
- No dismiss/close rate can be computed
- Behavioral response to friction must be inferred from **volume changes** across study periods: `event_rate_ratio_intervention_vs_baseline` = intervention events/day ÷ baseline events/day

After applying the required `n_baseline_days >= 7` filter:
- 235/243 DS6 participants have valid behavioral response ratios
- Mean ratio = 0.679 (participants used apps ~32% less during the intervention period vs baseline on average)
- Range: 0.063 to 2.523

**⚠ Correction (2026-08-06):** the paragraph below described `self_transition_rate`/
`cross_app_transition_rate` as permanently near-constant. That was true only of the
`app_next`-based computation. Root cause identified: DS6's true underlying log alternates
Open→Close→Open→Close (this exported file keeps only the Opens), and `app_next` mechanically
echoes the current row's own app_name 99.3% of the time because the very next logged event
is usually that same app's own close (not session-grouping — DS6 has no real sessions
either, see correction above, but this is a separate bug in a different column).
Recomputed on `app_prev` (verified genuine, ~42% same-app rate, non-mechanical):
`self_transition_rate` mean=0.512, sd=0.217 — now a real, usable individual-difference
feature. `app_next_entropy`/`n_unique_next_apps` (previously recommended as the
substitution-analysis fallback) were equally compromised and are renamed
`app_transition_entropy`/`n_unique_transition_apps`, also now app_prev-based. See
`data_docs/modeling_cautions.md` §6 and `outputs/reports/stage0/ds6_audit_report.md` §8b.

Original text (superseded, kept for record): "The `self_transition_rate` and
`cross_app_transition_rate` features are near-constant (mean=0.989, sd=0.018) and should
**not** be used as individual-difference features. This is a structural artifact of the raw
consecutive-event sequence itself (not session-grouping, which does not exist in DS6 — see
correction above): the `app_next` field predominantly captures same-app re-openings between
consecutive logged events. Use `app_next_entropy` and `n_unique_next_apps` for substitution
analysis instead."

**Friction outcome rating: Not comparable to DS1/DS4/DS5 on override rate. Different construct (volume reduction) rather than outcome-level classification. Strongest baseline-to-intervention comparison design — but cannot measure within-event compliance.**

### Longitudinal depth

DS6 has the most **structurally designed** longitudinal depth: explicit `participation_day` (study-day index), `period` (baseline/intervention), and repeated survey waves (2–3 waves). The baseline period gives a genuine pre-intervention behavioral reference — the only dataset where this is cleanly available.

The `event_rate_slope` (linear slope of daily event count over participation_day) captures longitudinal adaptation directly. (`session_rate_ratio` was removed 2026-08-05 — it was an exact duplicate of `event_rate_ratio_intervention_vs_baseline` under a session-suggestive name; see `data_docs/modeling_cautions.md` §6.) However, the observation window is defined by the study design (school semester timeline), which is shorter than DS4's multi-year observation.

**Cohort effect caution:** Participants are school cohorts, not individuals recruited independently. Shared behavioral trends within cohorts may reflect school calendar effects, peer social dynamics, or coordinated response to the study rather than individual behavioral dynamics.

### Sequence structure (corrected 2026-08-05 and 2026-08-06 — see below)

DS6 is the **strongest sequence dataset in the project** for app-transition analysis — by a large margin, once the corrected fields are used. Genuinely usable fields:

- `app_prev`, `app_prev2` — previous apps up to depth 2 (verified genuine 2026-08-06)
- `app_next2` — the true next distinct app opened (verified genuine, but requires conditioning on `resolution_next2=='openedApp'`)
- `resolution_next*`, `timestamp_next*` — forward-looking outcome sequences (real, but require correct interpretation — see below)

**NOT usable as "next app opened":** `app_next`, `app_next3` (verified 2026-08-06 to mechanically echo the current row's own app — see correction below).

This pre-engineered structure means substitution analysis and transition modeling can proceed without major raw-data derivation work, using `app_prev`/`app_next2`. No other dataset in the project comes close to this structural depth for sequences.

**⚠ Correction (2026-08-05):** this section originally also claimed `group_id`,
`first_in_group`, `last_close_in_group`, and `close_ts` provide genuine session grouping and
session-level network analysis. Verified false on the full raw file (all 353,796 rows):
`group_id` is unique per row (does not group events), `first_in_group`/`last_close_in_group`
are constant (1/0) for every row. `valid_open1`–`valid_open6` were never actually used in
Stage 1 feature extraction and have not been separately verified. DS6 has **no genuine
session-*count* data** and no "session-level network analysis" is possible — only ordinary
event-sequence transition modeling (which is real and remains DS6's strength). See
`data_docs/modeling_cautions.md` §6 and `outputs/reports/stage0/ds6_audit_report.md` §8a.

**⚠ Further correction (2026-08-06):** the 2026-08-05 correction above also claimed
`close_ts − openedapp_open_time` equals `time_diff_secs` "i.e. close_ts is just the next
event's timestamp, not a real close event" — that interpretation was wrong. The next logged
event is a real app-close 99.4% of the time (`resolution_next == 'closedApp'`), so
`close_ts`/`time_diff_secs` ARE genuine open→close dwell time for the large majority of
rows. Separately, and more consequentially: `app_next` was found to mechanically echo the
current row's own app_name 99.3% of the time for the same underlying reason (the next
logged event is usually this app's own close, and `app_next` just records that record's app
field) — so `app_next` does not represent "next app opened" at all. `app_prev` (looking
backward) does not have this problem. See `outputs/reports/stage0/ds6_audit_report.md` §8b.

### Survey and psychosocial depth

DS6 has the **strongest psychosocial survey layer** in the project, combining breadth, coverage, and repeat design:

- **Coverage:** 100% of behavioral participants have wave 1 survey; 77.4% have pre+post; 3-wave structure available in `survey_data_full.csv`
- **Self-control:** `self_control_index` — most direct self-control measure in the project
- **Addiction/problematic use:** `addiction_index`, `kontrolover_so_me`, `taenkerpa_so_me`
- **Well-being:** `trivsel` (Danish school well-being measure)
- **Social connection:** `socialconnection`, `socialtforbundet`
- **FoMO:** `fo_mo` (note: different instrument from DS5's 10-item scale)
- **Demographics:** age (13–17), gender, region — all 243 participants linked

The repeated survey structure (waves 1–3) means psychosocial change over time is trackable within DS6 in a way that is impossible in DS1 or DS4.

Pre-post change scores for addiction, self-control, FoMO, and well-being are available for the 188 fully-linked participants — making these **the primary pre-post psychosocial outcomes for DS6 intervention evaluation**.

### Key limitations

- **Single outcome type:** ALL events are 'opened' — cannot compute compliance rate, cannot distinguish override from compliance; friction outcome construct is fundamentally different from DS1/DS4/DS5
- **Smallest behavioral N** (243) — limits statistical power and subgroup analysis
- **School cohort design** — not individual randomization; cohort effects confound individual-level analyses
- `purpose` is 89% NaN — not usable
- (Superseded 2026-08-06) `self_transition_rate` / `cross_app_transition_rate` — were near-constant when computed on the buggy `app_next` field; recomputed on `app_prev`, now genuine and usable (mean=0.512, sd=0.217)
- High structural complexity — two partially overlapping behavioral file families; careful file selection required per analysis type
- Some variables visible in project description PDF are **not confirmed in CSV files** (streak/resist variables, pre/post combined survey structures) — do not assume availability
- Youngest sample (13–17) — generalizability to adult populations is limited

### Best use cases

- **Substitution analysis** — pre-engineered `app_prev`/`app_next2` fields (not `app_next`, see correction above) make this the natural starting point for cross-app substitution modeling
- ~~Session-level behavioral dynamics~~ — removed 2026-08-05: DS6 has no genuine session grouping (see correction above)
- **Repeated psychosocial change modeling** — 3-wave survey + behavioral baseline enables rich within-person change modeling
- **Adolescent-specific phenotyping** — only dataset capturing 13–17 age range with full behavioral + psychosocial coverage
- **Baseline-vs-intervention comparison** — only dataset with a cleanly defined pre-intervention behavioral baseline period
- **Advanced model comparison** — the richness of DS6 makes it the best platform for later comparing multiple model families once the pipeline is established on a simpler dataset

### Model family suitability

| Model family | Suitability | Reason |
|---|---|---|
| Statistical regression / GLM | Moderate | Smaller N (243) and quasi-experimental design (not RCT) limit causal leverage; psychosocial moderators excellent |
| Survival / time-to-event | Moderate | Participation day and period provide temporal structure; shorter windows than DS4 |
| Markov chains / HMM / stochastic process | Strong | Pre-engineered app_prev/app_next2 fields (not app_next, see correction); condition grouping |
| Information-theoretic summaries | Strong | Entropy features complete; period splits enable baseline vs intervention entropy comparison |
| Network / transition models | Strong (best in project) | Pre-engineered app_prev up to depth 2, app_next2 usable; substitution structure |
| Dynamical systems / phase models | Strong | Baseline vs intervention phase structure is explicit; participation day allows trajectory modeling |
| Agent-based models | Moderate | Rich behavioral detail per participant; cohort design limits independence assumption |
| Psychosocial moderator analysis | Strong | Best coverage + repeated measurement; self-control and addiction indices are the strongest self-report moderators in the project |
| Friction override/compliance modeling | Not suitable | Single outcome type (all 'opened') — cannot model compliance vs override at event level |
| System dynamics | Strong | Repeated surveys + behavioral phases + feedback-loop hypotheses are well-supported |

---

## Cross-Dataset Summary Table

| Property | DS1 | DS4 | DS5 | DS6 |
|---|---|---|---|---|
| N participants | 619 | 1,039 | 573 | 243 |
| Study design | Non-experimental | Non-experimental | **RCT** | Quasi-experimental |
| Condition structure | None | None | 3-arm | 3-arm (cohort) |
| Total events | ~399K | 2,490K | 289K | 354K |
| Unique apps | 48 | 399 | Rich | Rich |
| Observation window | Short | Longest (897d max) | Moderate | Study-structured |
| Friction outcome quality | High (all events = friction) | Good (intervention events) | High (with condition caveat) | Not applicable (all 'opened') |
| Adaptation trajectory | Weak (short window) | **Strongest** | Moderate | Structured (baseline/intervention) |
| Sequence structure | Weak | Moderate (derivable) | Moderate (derivable) | **Strongest** (pre-engineered) |
| Psychosocial depth | Thin | None (qualitative) | **Richest validated** | Strongest coverage + repeat |
| Pre-post survey | 168 (27%) | None | 284 (50%) | 188 (77%) |
| Survey coverage | 85% | 27% | 99.8% | 100% |
| Causal inference | None | None | **Strong (RCT)** | Moderate (quasi) |
| Implementation complexity | Low | Moderate | Moderate | High |

---

## Rankings by use case

| Use case | Best | Runner-up | Notes |
|---|---|---|---|
| First standalone modeling dataset | **DS5** | DS1 | DS5: RCT + psychosocial + clean outcomes; DS1: simpler but no conditions |
| Long-term adaptation / habit modeling | **DS4** | DS6 | DS4: 897-day windows; DS6: structured baseline/intervention |
| Psychosocial moderator analysis | **DS5** | DS6 | DS5: validated scales + RCT; DS6: self-control + repeated waves |
| Sequence / substitution modeling | **DS6** | DS5 | DS6: pre-engineered app_prev/app_next2 (not app_next, see correction); no real session structure |
| Experimental condition analysis | **DS5** | DS6 | DS5: only RCT; DS6: quasi-experimental cohort design |
| Friction override / compliance | **DS1** | DS4/DS5 | DS1: cleanest denominator; DS4/DS5 usable with caveats; DS6 not applicable |
| Adolescent-specific phenotyping | **DS6** | DS5 | DS6: 13-17 + full coverage; DS5: 13-25 |
| Large-N behavioral heterogeneity | **DS4** | DS5 | DS4: 1,039 participants; broadest app space |
| Lean first-pass pipeline testing | **DS1** | DS5 | DS1: fewest files, simplest structure |
| Rich multi-modal phenotyping | **DS6** | DS5 | DS6: behavioral + session + psychosocial + demographic + repeated survey |

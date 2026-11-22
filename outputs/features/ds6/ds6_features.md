# DS6 Feature Definitions

**Dataset:** Dataset 6 — Danish adolescents  
**Stage:** 1 — Dataset-specific feature extraction  
**Produced by:** `notebooks/14_ds6_feature_extraction.ipynb`  
**Source modules:** `src/features/ds6_features.py`, `src/features/behavioral_features.py`  
**Source files:** `outputs/cleaned/ds6_behavioral_clean.csv`, `ds6_survey_clean.csv`, `ds6_demographics_clean.csv`

---

## ⚠️ Critical structural note — outcome structure

**DS6 does NOT have dismiss or close outcomes.**  
All rows in `ds6_behavioral_clean.csv` have `event_outcome_simple == 'opened'`.

**This means DS6 CANNOT be treated as equivalent to DS1/DS4/DS5 on outcome dimensions.**  
Do not compare DS6 "outcome rates" with DS1/DS4/DS5 outcome rates in Stage 2 harmonization without explicit documentation of this structural difference.

Behavioral response to friction in DS6 is captured instead via:
- Volume and event-rate changes across `study_period` (baseline vs intervention)
- Sequence transitions (self-transition rate, substitution diversity)
- Longitudinal event rate slopes across `participation_day`

---

## Output files

| File | Rows | Cols | Coverage |
|---|---|---|---|
| `ds6_behavior_features.csv` | 243 | 66 | All behavioral participants + demographics |
| `ds6_survey_features.csv` | 243 | 19 | Behavioral participants with wave 1 survey data |
| `ds6_prepost_features.csv` | 188 | 10 | Participants with behavioral + both survey waves |

---

## Event definitions

| Concept | Definition |
|---|---|
| Event row | One app-opening event in `ds6_behavioral_clean.csv` (all outcome = openedApp) |
| Intervention exposure | `intervention_duration_sec > 0` (friction was shown) |
| Reintervention event | `is_reintervention == 1` |
| Outcome-bearing row | Not applicable — all outcomes are 'opened' |
| Study period | `study_period` ∈ {baseline, intervention} — directly in each row |
| Longitudinal axis | `participation_day` and `study_week` |

---

## ds6_behavior_features.csv — Feature Definitions

### Group 1 — Volume and Activity
**Type:** DIRECT | **Confidence:** High | **Eligible:** 243

| Column | Description | NaN% |
|---|---|---|
| `study_condition` | control / default / intervention | 0% |
| `age` | Age in years (13–17) | 0% |
| `gender` | female / male | 0.4% |
| `region` | Danish region | 0% |
| `total_events` | Total app-opening events | 0% |
| `n_days_observed` | Distinct calendar days | 0% |
| `obs_window_days` | Days from first to last event | 0% |
| `events_per_day` | total_events / obs_window_days | 0.4% |
| `active_days_per_week` | n_days_observed / (obs_window/7) | 0.4% |

**Period-split volume (DS6-unique: direct baseline/intervention comparison):**

| Column | Description | NaN% |
|---|---|---|
| `total_baseline_events` | Events in study_period == 'baseline' | 0% |
| `total_intervention_period_events` | Events in study_period == 'intervention' | 0% |
| `n_baseline_days` | Distinct days in baseline | 0% |
| `n_intervention_days` | Distinct days in intervention period | 0.8% |
| `events_per_day_baseline` | Events/day in baseline | 0% |
| `events_per_day_intervention` | Events/day in intervention period | 0.8% |
| `event_rate_ratio_intervention_vs_baseline` | intervention rate / baseline rate (>1 = more use during intervention) | 0.8% |

---

### Group 2 — Inter-Event Timing
**Type:** DIRECT | **Confidence:** High | **Eligible:** ~241 participants with ≥5 non-NaN time_diff_secs values

| Column | Description | NaN% |
|---|---|---|
| `mean_time_diff_secs` | Mean seconds until the next event in the participant's event sequence | 0.4% |

**⚠️ Removed during Stage 1 QC (2026-08-05): 8 "session structure" columns**
(`n_sessions_total`, `n_sessions_baseline`, `n_sessions_intervention_period`,
`session_rate_baseline`, `session_rate_intervention`, `session_rate_ratio`,
`share_events_first_in_group`, `share_sessions_with_matched_close`).
This group used to be labeled "Session Structure (DS6-unique)" and was described as
using pre-engineered session grouping "not available in DS1, DS4, or DS5." That claim
was verified false: `group_id` is unique per row across the entire raw source file
(353,796/353,796 rows), `first_in_group` == 1 for every row, and `last_close_in_group`
== 0 for every row — these columns do not group events into sessions at all. As a
direct consequence, `n_sessions_total` was numerically identical to `total_events`,
`session_rate_baseline` identical to `events_per_day_baseline`, and `session_rate_ratio`
identical to `event_rate_ratio_intervention_vs_baseline` (0.0 max difference across all
243 participants) — not new information, a duplicate under a different name.
Separately, the raw file's `close_ts` column (not retained in `ds6_behavioral_clean.csv`)
has `close_ts − openedapp_open_time` equal to `time_diff_secs` exactly. **Correction
(2026-08-06):** this was originally read as "close_ts is the next open event's timestamp,
not a real close" — that interpretation was wrong. DS6's underlying log alternates
Open→Close→Open→Close, and the very next logged event after an Open is that same app's
own close 99.4% of the time, so `close_ts`/`time_diff_secs` IS genuine open→close dwell
time for the large majority of rows. This does not change the separate, independently
confirmed finding above that `group_id`/`first_in_group`/`last_close_in_group` provide no
real session grouping — only the `close_ts` interpretation needed fixing, not the
arithmetic or the `group_id` finding. See
`src/features/ds6_features.py::ds6_timing_features()` docstring for the full verification
and `data_docs/modeling_cautions.md` §1/§6 for the persistent caution.

---

### Group 3 — Intervention Exposure
**Type:** DIRECT | **Confidence:** High | **Eligible:** 243

| Column | Description | NaN% |
|---|---|---|
| `n_ds6_intervention_types_seen` | Count of distinct intervention_type values | 0% |
| *(note)* | 4 participants have no typed friction event at all: for them `n_ds6_intervention_types_seen` is 0 but every `*_rate_ds6`, `n_friction_events_ds6` and `mean_intervention_duration_ds6` is NaN. Use `min_count=1` when summing the rate block (a bare `df[rate_cols].sum(axis=1)` silently reports 0.0 for these rows). | — |
| `dominant_intervention_type_ds6` | Most common intervention type | 1.6% |
| `denmark_rate_ds6` | Share of typed friction events using 'denmark' type | 1.6% |
| `breathingExercise_rate_ds6` | Share using breathingExercise | 1.6% |
| `math_rate_ds6` | Share using math | 1.6% |
| `followTheDot_rate_ds6` | Share using followTheDot | 1.6% |
| `randomText_rate_ds6` | Share using randomText | 1.6% |
| `n_friction_events_ds6` | Count of events with duration > 0 | 1.6% |
| `mean_intervention_duration_ds6` | Mean friction duration (non-NaN rows) | 2.9% |
| `has_reintervention` | 1 if any is_reintervention == 1 events | 0% |
| `n_reintervention_events` | Count of reintervention events | 0% |
| `reintervention_event_rate` | n_reintervention / total_events | 0% |
| `mean_reintervention_delay_sec` | Mean delay before re-intervention | 67.5% |
*`reintervention_open_rate` was **removed** during Stage 1 QC (2026-04-16). In DS6, all outcomes are 'opened', so this feature was always 1.0 for every non-NaN participant (60 participants). It carries zero information and was removed to prevent accidental misuse as a behavioral signal.*

---

### Group 4 — Sequence / Substitution Features (DS6-unique)
**Type:** NEAR-DIRECT | **Confidence:** High (self-transition) / Medium (substitution interpretation) | **Eligible:** ~242 participants with ≥10 rows with non-NaN app_prev

**DS6-unique:** Pre-engineered sequence fields (app_next depth-3, app_prev depth-2) are the richest substitution-related data in the project. No other dataset has these pre-computed fields.

**⚠️ Major correction (Stage 1 QC, 2026-08-06): these features are now computed from `app_prev`, not `app_next`.** Verified on the full raw file that DS6's true underlying log alternates
Open→Close→Open→Close (this exported file keeps only the Open rows); `app_next` was
computed against that full alternating sequence, so for 99.3% of rows the very next logged
record is that SAME app's own close event — `app_next == app_name` mechanically, not
behaviorally (confirmed via `resolution_next`: 'closedApp' for 99.4% of rows; conditioned on
that, `app_next == app_name` 99.3% of the time). This is what produced the previous
near-ceiling `self_transition_rate` (mean=0.989) — not "within-session re-opening" as
originally attributed to `group_id` (superseded 2026-08-05, `group_id` has no real
sessions), and not general adolescent same-app-reopening behavior either: it was a
look-ahead mechanics artifact. `app_prev` does not have this problem — looking backward,
the immediately-prior record is typically the *previous, different* app's close event, not
this app's own (verified: `app_prev == app_name` only ~42% overall, stable across
resolution_last categories 39-64%, a plausible non-mechanical split).
**Renamed accordingly:** `app_next_entropy`→`app_transition_entropy`,
`n_unique_next_apps`→`n_unique_transition_apps`, `top_next_app`→`top_transition_app`,
`top_next_app_share`→`top_transition_app_share`. `self_transition_rate`/
`cross_app_transition_rate` keep their names (direction-symmetric construct) but are now
computed on `app_prev` and have a **completely different, now genuinely informative**
distribution: mean=0.512, sd=0.217, range [0.18, 1.0] (was mean=0.989, sd=0.018) —
`self_transition_rate` is no longer near-constant and is a real individual-difference
feature. `resolution_next_open_rate` **removed** — verified near-constant-near-zero
(0.5% overall, same look-ahead-mechanics cause), same treatment as the earlier
`reintervention_open_rate` removal. `max_consecutive_same_app` is unaffected by any of
this — built from the exported file's own real Open-event row order, not from
app_next/app_prev. See `src/features/ds6_features.py::ds6_sequence_features()` docstring
for the full verification.

| Column | Description | NaN% |
|---|---|---|
| `self_transition_rate` | Proportion where app_prev == app_name (was just re-opened) | 0.4% |
| `cross_app_transition_rate` | Proportion where app_prev != app_name (switched from a different app) | 0.4% |
| `app_transition_entropy` | Shannon entropy of the **marginal** app_prev distribution. ⚠ NOT a transition/substitution measure — r=0.983 with `app_entropy` | 0.4% |
| `n_unique_transition_apps` | Count of distinct app_prev values. ⚠ Exact duplicate of `n_unique_apps` (242/242 identical) | 0.4% |
| `top_transition_app` | Most common preceding app | 0.4% |
| `top_transition_app_share` | Share of transitions from top_transition_app | 0.4% |
| `max_consecutive_same_app` | Longest run of same app opening repeatedly (habit-chain proxy) | 0.4% |

---

### Group 5 — App Structure Overall
**Type:** DIRECT | **Confidence:** High | **Eligible:** 243

`n_unique_apps`, `top_app`, `top_app_share`, `top3_app_share`, `app_herfindahl`, `app_entropy`

---

### Group 6 — App Structure by Period (DS6-unique)
**Type:** DIRECT | **Confidence:** High | **Eligible:** ~239 per period

| Column | Description | NaN% |
|---|---|---|
| `n_unique_apps_baseline`, `n_unique_apps_intervention` | App diversity per period | 1.2% |
| `app_entropy_baseline`, `app_entropy_intervention` | Shannon entropy per period | 1.2% |
| `top_app_baseline`, `top_app_intervention` | Modal app per period | 1.2% |
| `top_app_share_baseline`, `top_app_share_intervention` | Top app share per period | 1.2% |
| `top_app_period_consistent` | 1 if same top app in both periods | 2.1% |
| `app_entropy_change` | intervention − baseline entropy (positive = more diverse during intervention) | 2.1% |

---

### Group 7 — Temporal Structure
**Type:** DIRECT-DERIVED | **Confidence:** High | **Eligible:** ~242

DS6 has the richest temporal columns of all four datasets: explicit `hour_of_day`, `study_week`, `study_day_of_week`, `participation_day`.

| Column | Description | NaN% |
|---|---|---|
| `peak_hour_of_day` | Overall peak activity hour (0–23), **UTC** — 1–2h earlier than the local peak; compare with `peak_hour_baseline`/`peak_hour_intervention`, which are Europe/Copenhagen local | 0.4% |
| `weekend_event_share` | Proportion on Sat/Sun | 0.4% |
| `evening_event_share` | Proportion 18:00–23:00 **UTC** = 19:00–00:59 local (20:00–01:59 CEST) | 0.4% |
| `morning_event_share` | Proportion 06:00–11:00 **UTC** = 07:00–12:59 local (08:00–13:59 CEST) | 0.4% |
| `peak_hour_baseline` | Peak hour during baseline period | 1.2% |
| `peak_hour_intervention` | Peak hour during intervention period | 1.2% |
| `hour_entropy` | Shannon entropy of hour_of_day distribution | 0.4% |
| `participation_day_max` | Maximum participation day number | 0% |
| `study_week_max` | Maximum study week number | 0% |

---

### Group 8 — Longitudinal Adaptation via Participation Day
**Type:** PROXY | **Confidence:** Medium | **Eligible:** ~237 participants with ≥14 participation days

**Proxy note:** Cohort-level effects (same school groups) may confound individual trajectories. Study design determines the maximum observation window — adaptation slopes should be interpreted cautiously.

| Column | Description | NaN% |
|---|---|---|
| `event_rate_week1` | Mean daily events in participation days 1–7 | 2.9% |
| `event_rate_last_week` | Mean daily events in last 7 participation days | 2.1% |
| `event_rate_slope` | Linear slope of daily event count across participation_day, **pooled over baseline + intervention** (negative = decreasing use). ⚠ r=0.936 with the period contrast `events_per_day_intervention − events_per_day_baseline` — read as a level shift, not as within-period habituation | 0.4% |

*`session_rate_early`/`session_rate_late` were **removed** during Stage 1 QC (2026-08-05) — same `group_id` artifact as Group 2 above (group_id does not group real sessions; these were numerically identical to an event-count rate, not a distinct signal).*

---

## ds6_survey_features.csv — Feature Definitions

### Group 9 — Wave 1 and Wave 2 Survey Indices
**Type:** DIRECT | **Confidence:** High | **Eligible:** 243 (wave 1); 188 (wave 2, behavioral-linked)

| Column | Description |
|---|---|
| `study_condition` | Condition: control / default / intervention |
| `addiction_index_pre` | Social media addiction index — wave 1 (mean of afhaengighed_1..6; construction verified exact, max abs diff 4.4e-16). ⚠ Reliability: Cronbach's α = 0.696 (n=916). Item `afhaengighed_4` has a corrected item-total r of only 0.104 (others 0.399–0.568) and is not reverse-keyed (reversing it lowers α to 0.639); dropping it raises α to 0.751. Treat null results on `addiction_index` / `addiction_index_change` as partly attenuated by measurement error. |
| `self_control_index_pre` | Self-control index — wave 1 (mean of selvkontrol_1..5; construction verified exact, max abs diff 0.0; all inter-item correlations positive, min +0.187, so no reverse coding is required) |
| `fo_mo_pre` | Fear of missing out (FoMO) — wave 1 |
| `trivsel_pre` | Well-being / thriving — wave 1 |
| `socialconnection_pre` | Social connectedness — wave 1 |
| `kontrolover_so_me_pre` | Perceived control over social media — wave 1 |
| `taenkerpa_so_me_pre` | Thinking about social media — wave 1 |
| `tilfredsmed_so_me_pre` | Satisfaction with social media use — wave 1 |
| `*_post` | Same indices at wave 2 (NaN for participants without wave 2) |
| `has_wave2_survey` | 1 if wave 2 survey data available |

---

## ds6_prepost_features.csv — Feature Definitions

### Group 10 — Pre-Post Survey Change Scores
**Type:** DIRECT-DERIVED | **Confidence:** Medium | **Eligible:** 188

**Sign convention:** positive = increase from wave 1 to wave 2. For addiction / thinking_about: positive = worsening. For self-control / wellbeing / satisfaction: positive = improvement.

| Column | Description |
|---|---|
| `addiction_index_change` | wave 2 − wave 1 addiction index |
| `self_control_index_change` | wave 2 − wave 1 self-control index |
| `fo_mo_change` | wave 2 − wave 1 FoMO |
| `trivsel_change` | wave 2 − wave 1 well-being |
| `socialconnection_change` | wave 2 − wave 1 social connectedness |
| `kontrolover_so_me_change` | wave 2 − wave 1 perceived control |
| `taenkerpa_so_me_change` | wave 2 − wave 1 thinking about social media |
| `tilfredsmed_so_me_change` | wave 2 − wave 1 satisfaction |

---

## DS6-specific strengths and limitations

**Strengths:**
- Pre-engineered sequence fields (app_next/prev depth-3) — best dataset in this project for substitution and habit-chain analysis
- Explicit baseline vs intervention period in each row — cleanest period-comparison structure
- Two-wave survey with self-control and addiction indices — strongest psychosocial profile in the project
- Age (13–17) — youngest true adolescent sample
- Demographic file with age, gender, region
- Richest temporal structure (hour_of_day, study_week, participation_day directly in behavioral rows)

**Limitations:**
- ONLY openedApp events in resolution — no dismiss or close outcomes directly observed
- Outcome structure is fundamentally different from DS1/DS4/DS5 — do NOT compare outcome rates across datasets without explicit acknowledgment
- 399 enrolled participants but only 243 have behavioral events (156 enrolled-only)
- **No genuine session-boundary data** (finding confirmed 2026-08-05): `group_id` is unique per row across the entire raw file and `first_in_group`/`last_close_in_group` are constant (1/0) for every row, so DS6 has no session *count* or *boundary marker*. `close_ts`/`time_diff_secs` is a separate matter — corrected 2026-08-06: it IS genuine open→close dwell time for ~99% of rows (the arithmetic was always right; only the earlier "next open event, not a real close" interpretation was wrong). DS6 therefore has no session count or boundary marking, but does have genuine per-event dwell time via `time_diff_secs`/`mean_time_diff_secs`. See Group 2 note above.
- `purpose` (88.8% NaN) not featurized
- Wave 2 survey available for only 209 enrolled; behavioral + both waves = 188

**Where Stage 2 harmonization would be possible:**
- `app_entropy`, `events_per_day`, `obs_window_days` → direct crossover
- `self_transition_rate` (now app_prev-based, mean=0.512/sd=0.217 as of 2026-08-06 correction — a genuine individual-difference feature, not the earlier near-constant version) → proxy for habit strength, comparable with override streak features from other datasets (different mechanism)
- `fo_mo_pre` → partially comparable to DS5 `fomo_mean_pre` but different instruments; note difference explicitly
- `event_rate_ratio_intervention_vs_baseline` → DS6-specific; has no direct equivalent in DS1/DS4/DS5 (no baseline period in those datasets)
- Outcome rates: **NOT harmonizable** — DS6 has only 'opened' outcomes; use volume/event-rate ratios as proxies

---

## How to load

```python
import pandas as pd
from pathlib import Path

FEAT = Path("outputs/features/ds6")

beh = pd.read_csv(FEAT / "ds6_behavior_features.csv")
survey = pd.read_csv(FEAT / "ds6_survey_features.csv")
prepost = pd.read_csv(FEAT / "ds6_prepost_features.csv")

# Merge behavioral + survey (wave 1 + wave 2 where available)
merged = beh.merge(survey, on="participant_id_canonical", how="left", suffixes=("", "_survey"))
merged_full = merged.merge(prepost, on="participant_id_canonical", how="left", suffixes=("", "_change"))

# Filter to participants with both survey waves (188 rows)
two_wave = merged_full[merged_full["has_wave2_survey"] == 1]

# Filter to intervention period behavioral events (for period-specific modeling)
# Note: this requires loading ds6_behavioral_clean.csv, not the feature file
```

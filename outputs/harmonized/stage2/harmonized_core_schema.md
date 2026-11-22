# Stage 2 — Harmonized Core Feature Schema

**Created:** 2026-04-16  
**Produced by:** `src/features/harmonized_core_features.py`  
**Output file:** `outputs/harmonized/stage2/harmonized_core_features.csv`

---

## Purpose

This file is a **light cross-dataset comparability layer only**.

It does NOT replace the dataset-specific Stage 1 feature files. For individual dataset modeling, always use:
- `outputs/features/ds1/ds1_behavior_features.csv` (and ds1_survey_features, ds1_prepost_features)
- `outputs/features/ds4/ds4_behavior_features.csv` (and ds4_survey_features)
- `outputs/features/ds5/ds5_behavior_features.csv` (and ds5_survey_features, ds5_prepost_features)
- `outputs/features/ds6/ds6_behavior_features.csv` (and ds6_survey_features, ds6_prepost_features)

The harmonized core is appropriate for:
- Descriptive cross-dataset comparisons (distributions, participant profiles)
- Identifying which behavioral constructs generalize across datasets
- Building shared phenotyping scaffolds where per-feature caveats are respected
- Cross-dataset regression or clustering — only after carefully reading the caveat columns

---

## File summary

| Property | Value |
|---|---|
| Rows | 2,474 |
| Columns | 28 |
| Unit of observation | One row per participant per dataset |
| DS1 rows | 619 |
| DS4 rows | 1,039 |
| DS5 rows | 573 |
| DS6 rows | 243 |

---

## Column reference

### Identifiers and design metadata

| Column | Type | Description |
|---|---|---|
| `dataset_id` | string | Source dataset: 'DS1' / 'DS4' / 'DS5' / 'DS6' |
| `participant_id_canonical` | string | Participant identifier as harmonized in Stage 1 cleaning |
| `study_design_type` | string | 'non_experimental' (DS1, DS4) / 'experimental_rct' (DS5) / 'experimental_quasi' (DS6) |
| `study_condition` | string or NaN | Experimental condition. DS5: control/default/reintervention. DS6: control/default/intervention. DS1/DS4: NaN (non-experimental). |

---

### Volume features (Group A — directly comparable)

| Column | Type | NaN coverage | Notes |
|---|---|---|---|
| `total_events` | int | 0% | Total event rows per participant. Direct count — no caveats. |
| `n_days_observed` | int | 0% | Distinct calendar days with ≥1 event. Direct count. |
| `obs_window_days` | float | 0% | Days from first to last event. Direct measure. |
| `events_per_day` | float | 7.5% | total_events / obs_window_days. NaN for single-day participants (window = 0). DS1: 17.4% NaN; DS5: 12.4% NaN; DS4: 0.6% NaN; DS6: 0.4% NaN. |

---

### App structure features (Group A — directly comparable)

| Column | Type | NaN coverage | Notes |
|---|---|---|---|
| `n_unique_apps` | int | 0% | Count of distinct app names. Direct. |
| `top_app_share` | float | 0.2% | Share of events from the single most frequent app. |
| `app_herfindahl` | float | 0.2% | Herfindahl-Hirschman concentration index across apps (sum of squared shares). High = dominated by few apps. |
| `app_entropy` | float | 0.2% | Shannon entropy of the app event distribution. High = more diverse app use. |

---

### Temporal structure features (Group A — directly comparable)

All computed from event timestamps bucketed to hour-of-day and weekday. DS1 timestamps assumed UTC. DS5 uses timezone-aware conversion. DS4/DS6 confirmed UTC.

| Column | Type | NaN coverage | Notes |
|---|---|---|---|
| `peak_hour_of_day` | int | 7.5% | Hour (0–23) with most events. NaN for single-day participants. |
| `weekend_event_share` | float | 7.5% | Proportion of events on Saturday or Sunday. |
| `evening_event_share` | float | 7.5% | Proportion of events 18:00–23:00. |
| `morning_event_share` | float | 7.5% | Proportion of events 06:00–11:00. |
| `hour_entropy` | float | 10.4% | Shannon entropy of hour-of-day distribution. High = more temporally distributed use. DS1: 20.2% NaN (single-day + computation threshold). DS6: renamed from `hour_entropy_ds6` in Stage 1 QC; computation slightly different (uses pre-engineered `hour_of_day` column) but empirically equivalent. |

---

### Friction response features (Group B — comparable with explicit caveats)

**Read the `friction_override_source` column before using `friction_override_rate` for any comparison or modeling.**

| Column | Type | NaN coverage | Notes |
|---|---|---|---|
| `friction_override_rate` | float | 11.3% | Rate at which participants opened the target app despite friction. **NaN for ALL DS6 rows** (structural — DS6 has only 'opened' outcomes). Do NOT impute DS6 NaN values. Source column and denominator differ across datasets — see friction_override_source. |
| `friction_override_source` | string | 0% | Documents which source column and event subset was used. Values: `rate_opened__all_events__ds1`, `rate_opened__intervention_events_only__ds4`, `rate_opened__all_events__ds5`, `not_applicable__ds6_all_outcomes_opened`. |

**Critical caveats for friction_override_rate:**
- **DS1**: `rate_opened` over all events. All DS1 events are friction-triggered — this is the cleanest all-events comparison.
- **DS4**: `rate_opened_intervention_events` — only `intervention_event` class (36.5% of all events). Denominators differ from DS1/DS5 — DS4 values are restricted to friction-active events only, so they are not raw-comparable to DS1/DS5.
- **DS5**: `rate_opened` over all events. The **control condition has no friction exposure** — their rate_opened reflects friction-free opens. For cross-dataset friction comparison, restrict to DS5 default and reintervention conditions.
- **DS6**: Always NaN — structural incompatibility. Use `behavioral_response_ratio` instead.

---

### DS6 behavioral response proxy (Group B — DS6 specific)

| Column | Type | NaN coverage | Notes |
|---|---|---|---|
| `behavioral_response_ratio` | float | 90.5% | DS6 only: `event_rate_ratio_intervention_vs_baseline`. Intervention-period events/day divided by baseline-period events/day. >1 = more use during intervention. Filter applied: NaN where `n_baseline_days < 7`. DS1/DS4/DS5: always NaN. |
| `behavioral_response_proxy_type` | string or NaN | 90.5% | 'event_rate_ratio_intervention_vs_baseline' for eligible DS6 rows. NaN otherwise. |

**Important:** `behavioral_response_ratio` is NOT equivalent to `friction_override_rate`. These are different constructs measured differently. DS6 behavioral_response_ratio > 1 means more app-opening events during the intervention period (not necessarily more friction override). Do not compare these two columns directly.

---

### Adaptation trajectory features (Group B — comparable with axis caveat)

| Column | Type | NaN coverage | Notes |
|---|---|---|---|
| `open_rate_change` | float | 24.1% | Change in opened-outcome rate from early to late third of observation window (late − early). Positive = increasing override over time. DS6: always NaN (no equivalent). |
| `open_rate_change_axis` | string | 0% | 'setup_time_ds1' / 'calendar_days' / 'not_available_ds6'. Documents which time axis the tertile split uses. |

**Caveats for open_rate_change:**
- **DS1**: setup-time axis (`secondsSinceOneSecSetup` tertiles). 33.8% NaN within DS1 (< 10 events with setup time). Axis differs from DS4/DS5.
- **DS4**: calendar days (days_since_first_event tertiles). 4.7% NaN. Longest windows (up to 897 days) — most reliable signal.
- **DS5**: calendar days tertiles. 16.6% NaN. Shorter windows — less reliable, especially for control.
- **DS6**: NaN for all. DS6 uses participation_day and period structure which is not equivalent.
- **Interpretation**: Sign and direction are cautiously comparable. Magnitude is NOT directly comparable across datasets because time axes differ and non-experimental datasets (DS1, DS4) conflate adaptation with attrition and life context changes.

---

### Availability flags

| Column | Type | Notes |
|---|---|---|
| `has_survey` | bool | True if participant has any survey data (pre-survey or wave 1). |
| `has_prepost_survey` | bool | True if participant has both pre and post survey data. DS4: always False (no pre-post survey). |
| `has_study_condition` | bool | True if study_condition is non-NaN. DS5/DS6: mostly True. DS1/DS4: always False. |
| `has_friction_outcome` | bool | True if friction_override_rate is non-NaN. DS6: always False. |
| `has_behavioral_response_ratio` | bool | True if behavioral_response_ratio is non-NaN. DS6 only (235 of 243). |

---

## What is NOT in this file

The following features are excluded from the harmonized core. Use the dataset-specific Stage 1 files for these.

| Excluded feature type | Reason |
|---|---|
| `active_days_per_week` | 25–27% NaN in DS1/DS5 due to short windows; not reliable across datasets |
| `rate_dismissed`, `rate_closed`, `rate_not_opened` | DS6 has no dismiss/close outcomes — would be empty for DS6 and misleadingly absent |
| DS6 period-split features (`*_baseline`, `*_intervention`) | DS6-specific; no equivalent period structure in DS1/DS4/DS5 |
| DS6 session structure (`n_sessions_*`, `session_rate_*`) | Removed from DS6 itself in Stage 1 QC 2026-08-05 — `group_id` verified non-functional (unique per row, not real sessions); these columns no longer exist in any dataset, not merely a cross-dataset gap |
| DS6 sequence features (`app_transition_entropy`, `self_transition_rate`, etc. — renamed/recomputed on app_prev 2026-08-06) | Pre-engineered sequence fields are DS6-specific |
| DS4 event class features (`intervention_event_share`, etc.) | Three-class logging architecture unique to DS4 |
| DS4 longitudinal activity (`active_weeks`, `activity_persistence`, `gaps_over_7d`) | Long-window design makes these DS4-specific meaningful features |
| DS4/DS5 duration features (`mean_intervention_duration`, etc.) | ~63.5% NaN in DS4; high NaN in DS5 control; DS1/DS6 coverage differs |
| Override streak features (`max_consecutive_opens`, etc.) | DS6 equivalent (`max_consecutive_same_app`) reflects a different mechanism |
| All psychosocial scale scores | Instruments differ strongly across datasets; harmonization would misrepresent measurement differences |
| DS5 belonging/ostracism/FoMO scales | No equivalent in DS1, DS4, DS6 |
| DS6 `addiction_index_pre`, `self_control_index_pre` | No equivalent elsewhere |
| DS1 `problematic_cons_pre`, `happy_pre` | No equivalent elsewhere |
| DS4 qualitative survey features | Open text only; not numerically featurized |

---

## How to load

```python
import pandas as pd
from pathlib import Path

core = pd.read_csv("outputs/harmonized/stage2/harmonized_core_features.csv")

# Subset to a single dataset
ds1 = core[core["dataset_id"] == "DS1"]
ds6 = core[core["dataset_id"] == "DS6"]

# Participants with friction outcomes (DS1, DS4, DS5 non-control)
friction_participants = core[core["has_friction_outcome"]]

# DS6 behavioral response (filtered to reliable baseline)
ds6_response = core[
    (core["dataset_id"] == "DS6") & core["has_behavioral_response_ratio"]
]

# Group A features only — safe for direct descriptive comparison
group_a_cols = [
    "dataset_id", "participant_id_canonical",
    "total_events", "n_days_observed", "obs_window_days", "events_per_day",
    "n_unique_apps", "top_app_share", "app_herfindahl", "app_entropy",
    "peak_hour_of_day", "weekend_event_share", "evening_event_share",
    "morning_event_share", "hour_entropy",
]
group_a = core[group_a_cols]
```

---

## Required reading before modeling

Before using this file in any modeling or statistical comparison:

1. **`data_docs/modeling_cautions.md`** — feature filtering requirements, proxy warnings, cross-dataset comparability limits
2. **`data_docs/stage1_feature_qc_notes.md`** — what was changed in Stage 1 and why
3. **`outputs/harmonized/stage2/cross_dataset_comparability_notes.md`** — caveats specific to cross-dataset use
4. Read the `friction_override_source` column distribution before pooling any friction data
5. Never compare DS6 `friction_override_rate` (always NaN) to DS1/DS4/DS5 values

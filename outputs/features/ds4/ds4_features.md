# DS4 Feature Definitions

**Dataset:** Dataset 4 — Large non-experimental data  
**Stage:** 1 — Dataset-specific feature extraction  
**Produced by:** `notebooks/12_ds4_feature_extraction.ipynb`  
**Source modules:** `src/features/ds4_features.py`, `src/features/behavioral_features.py`  
**Source files:** `outputs/cleaned/ds4_behavioral_clean.csv`, `ds4_survey_clean.csv`

---

## Output files

| File | Rows | Cols | Coverage |
|---|---|---|---|
| `ds4_behavior_features.csv` | 1,039 | 54 | All behavioral participants |
| `ds4_survey_features.csv` | 283 | 9 | Demographics + qualitative flags (no Likert scales in DS4) |

---

## Event definitions

| Concept | Definition |
|---|---|
| Event row | One row per logged OneSec app-interaction event in `ds4_behavioral_clean.csv`. Only 36.5% are friction-intervention exposures — see `intervention_event_class`. |
| Intervention exposure | `intervention_event_class == 'intervention_event'` (36.5% of events) |
| Outcome-bearing row (all) | `event_outcome_simple` ∈ {opened, dismissed, closed} (excludes 812 'dismissed_other') |
| Outcome-bearing row (intervention class) | `intervention_event_class == 'intervention_event'` AND outcome ∈ {opened, dismissed} |
| Longitudinal axis | `days_since_first_event` — all rows, no NaN. Do NOT use `secondsSinceStudySetup` (inverted). |

**Critical structural distinction — three event classes:**
- `intervention_event` (36.5%): active friction shown; has `interventionType` + `interventionDuration`
- `app_close_event` (47.1%): closedApp outcome only; no intervention fields; may represent a different logging path
- `no_intervention` (16.4%): opened/dismissed but no intervention logging

Mixing these classes when computing outcome rates obscures behavioral differences between active-friction events and passive close events.

---

## ds4_behavior_features.csv — Feature Definitions

### Group 1 — Volume and Activity
**Type:** DIRECT | **Confidence:** High | **Eligible:** 1,039

| Column | Description | NaN% |
|---|---|---|
| `total_events` | Total event rows | 0% |
| `n_days_observed` | Distinct calendar days with ≥1 event | 0% |
| `obs_window_days` | Days from first to last event | 0% |
| `events_per_day` | total_events / obs_window_days | 0.6% |
| `active_days_per_week` | n_days_observed / (obs_window/7) | 9.7% |
| `n_intervention_events` | Rows with class = intervention_event | 0% |
| `n_close_events` | Rows with class = app_close_event | 0% |
| `n_no_intervention_events` | Rows with class = no_intervention | 0% |
| `intervention_event_share` | n_intervention_events / total_events | 0% |
| `close_event_share` | n_close_events / total_events | 0% |
| `intervention_events_per_day` | n_intervention_events / obs_window_days | 1.8% |

---

### Group 2 — Outcome Rates by Event Class
**Type:** DIRECT | **Confidence:** High | **Eligible:** 1,039

| Column | Description | NaN% |
|---|---|---|
| `rate_opened_all` | Opened / all non-dismissed_other events | 0% |
| `rate_dismissed_all` | Dismissed / all non-dismissed_other events | 0% |
| `rate_closed_all` | Closed / all non-dismissed_other events | 0% |
| `rate_opened_intervention_events` | Opened / (opened + dismissed) among intervention_event class only | 3.0% |
| `rate_dismissed_intervention_events` | Dismissed / (opened + dismissed) among intervention_event class only | 3.0% |
| `n_intervention_event_outcomes` | Count of outcome-bearing intervention_event rows | 0% |

*NaN for participants with <5 intervention events.*

**Caution — the three `*_all` rates are not behavioural override rates.** Their denominator pools all three event classes, and whether a participant has `app_close_event` rows at all is a logging-epoch/app-version property (305 of 1,039 participants have zero close events; close-event logging does not exist before 2021-05-09). Measured: corr(`close_event_share`, `rate_opened_all`) = −0.701, i.e. roughly half the variance of `rate_opened_all` is close-event coverage rather than behaviour, versus +0.222 for `rate_opened_intervention_events`. Use `rate_opened_intervention_events` for any override construct; never pool or compare the `*_all` rates across participants.

---

### Group 3 — Intervention Type Profile (DS4-unique)
**Type:** DIRECT | **Confidence:** High | **Eligible:** ~1,035 (participants with ≥1 typed intervention event)

**DS4-unique:** Six intervention types are directly logged. No other dataset in this project has this type diversity. Coverage is 36.5% of all events (intervention_event class only).

| Column | Description | NaN% |
|---|---|---|
| `n_intervention_types_seen` | Count of distinct intervention types encountered | 0% |
| `dominant_intervention_type` | Most common intervention type | 0.3% |
| `breathingExercise_rate` | Share of intervention events using breathingExercise | 0.3% |
| `minimalBreathingExercise_rate` | Share using minimalBreathingExercise | 0.3% |
| `followTheDot_rate` | Share using followTheDot | 0.3% |
| `blackScreen_rate` | Share using blackScreen | 0.3% |
| `mirror_rate` | Share using mirror | 0.3% |
| `rotatePhone_rate` | Share using rotatePhone. **Degenerate — exclude from multivariate feature sets.** Non-zero for only 2 of 1,039 participants (10 events in the whole 2.49M-row dataset; mean 0.0002, sd 0.0062). Compare: breathingExercise 933 non-zero participants, minimalBreathingExercise 521, followTheDot 519, mirror 316, blackScreen 313. | 0.3% |

---

### Group 4 — Temporal Structure
**Type:** DIRECT-DERIVED | **Confidence:** High | **Eligible:** ~1,033

| Column | Description | NaN% |
|---|---|---|
| `peak_hour_of_day` | Hour (0–23) with most events | 0.6% |
| `weekend_event_share` | Proportion of events on Sat/Sun | 0.6% |
| `evening_event_share` | Proportion of events 18:00–23:00 | 0.6% |
| `morning_event_share` | Proportion of events 06:00–11:00 | 0.6% |
| `hour_entropy` | Shannon entropy of hour-of-day distribution | 3.8% |

---

### Group 5 — Longitudinal Activity Structure
**Type:** DIRECT-DERIVED | **Confidence:** High | **Eligible:** 1,039

DS4's long observation window (up to 897 days) makes these features especially meaningful.

| Column | Description | NaN% |
|---|---|---|
| `active_weeks` | Distinct ISO calendar weeks with ≥1 event | 0% |
| `activity_persistence` | active_weeks / (obs_window_days/7) — proportion of possible weeks active | 0% |
| `gaps_over_7d` | Count of continuous inactivity periods > 7 days | 0% |

**Removed column:** `obs_window_days_ds4` was dropped during Stage 1 QC (2026-04-16). It was identical to `obs_window_days` (from `volume_features`) for all 1,039 participants (r=1.0, zero difference). Use `obs_window_days` for DS4 — this is the cross-dataset standard name.

**Implementation note — `active_weeks` edge case:** `active_weeks` is computed using ISO calendar week numbers (`dt.isocalendar().week`), so the counter saturates at 53. Merely crossing a year boundary is NOT enough to cause a collision (529 of 1,039 participants span more than one ISO year); the span must exceed ~52 ISO weeks. Measured: 39 of 1,039 participants (3.8%) have `active_weeks` understated, by a mean of 11.2 weeks and a maximum of 61 weeks (participant `<participant-id>`: 113 true active weeks recorded as 52). `activity_persistence` inherits this saturation and additionally exceeds 1.0 for 837 of 1,039 participants (80.6%, max 2.3128) because its numerator counts calendar weeks touched while its denominator is a fractional elapsed-day span; corr(obs_window_days, activity_persistence) = −0.517. Do not use `activity_persistence` for participants with observation windows > 365 days.

---

### Group 6 — Longitudinal Adaptation via Calendar Time
**Type:** PROXY | **Confidence:** Medium | **Eligible:** ~989 (≥10 intervention events required)

**Proxy note:** Non-experimental design — trajectory changes may reflect app updates, habituation, changing life context, or attrition rather than pure adaptation to friction. This is DS4's strongest dataset-specific contribution despite the caveat.

| Column | Description | NaN% |
|---|---|---|
| `open_rate_early_third_calendar` | Opened rate in first tertile of days_since_first_event | 4.7% |
| `open_rate_late_third_calendar` | Opened rate in last tertile | 4.7% |
| `open_rate_change_calendar` | late − early (positive = increasing override) | 4.7% |
| `dismiss_rate_early_third_calendar` | Dismissed rate in first tertile | 4.7% |
| `dismiss_rate_late_third_calendar` | Dismissed rate in last tertile | 4.7% |
| `dismiss_rate_change_calendar` | late − early | 4.7% |

*Restricted to intervention_event class for a clean comparison signal.*

*Window caution: because no `intervention_event` row exists before 2022-10-03, the tertile span is at most 165.2 days (mean 62.2, median 64.6) — not the 897-day full observation window.*

---

### Group 7 — App Structure
**Type:** DIRECT | **Confidence:** High | **Eligible:** 1,039

Same structure as DS1 Groups. See DS1 documentation for column descriptions.

`n_unique_apps`, `top_app`, `top_app_share`, `top3_app_share`, `app_herfindahl`, `app_entropy`

---

### Group 8 — Intervention Duration
**Type:** DIRECT (duration) / PROXY (delta as friction sensitivity) | **Confidence:** Medium | **Eligible:** ~1,007 (≥5 events with duration)

`interventionDuration` is NaN for all closedApp events and some opened events. Features computed only from non-NaN duration rows within the intervention_event class.

| Column | Description | NaN% |
|---|---|---|
| `mean_intervention_duration` | Mean intervention_duration_sec (non-NaN, >0) | 3.0% |
| `mean_duration_on_opened` | Mean duration on opened outcomes | 3.5% |
| `mean_duration_on_dismissed` | Mean duration on dismissed outcomes | 3.4% |
| `duration_open_vs_dismiss_delta` | mean_on_opened − mean_on_dismissed (friction sensitivity proxy) | 3.8% |
| `n_events_with_duration` | Count of rows with duration > 0 | 0% |

---

### Group 9 — Override Tendency
**Type:** PROXY — Behavioral | **Confidence:** Medium | **Eligible:** ~1,007

Computed within the `intervention_event` class for a clean signal.

| Column | Description | NaN% |
|---|---|---|
| `max_consecutive_opens` | Longest run of consecutive `opened` outcomes | 3.0% |
| `mean_open_run_length` | Mean length of opened streaks | 3.5% |
| `p_open_after_dismiss` | P(next = opened | current = dismissed) | 3.2% |

---

## ds4_survey_features.csv — Feature Definitions

### Group 10 — Demographics + Qualitative Flags
**Type:** DIRECT (demographics) | **Confidence:** Medium (20% NaN on age) | **Eligible:** 283

**Important:** DS4's survey contains ONLY open-text qualitative responses. No Likert scales exist. The substantive survey columns (`reason_use`, `benefits`, `negatives`, `usage_format`) are flagged as available for future NLP-based extraction but are NOT numerically featurized here.

| Column | Description |
|---|---|
| `has_survey` | 1 for all rows in this file (filter flag) |
| `survey_age` | Age in years (20.4% NaN in raw survey) |
| `gender_clean` | Recoded gender: male / female / non_binary / other / prefer_not_to_say |
| `survey_qualitative_available` | 1 if any qualitative text column is non-NaN |
| `has_reason_use` | 1 if `reason_use` is non-NaN |
| `has_benefits` | 1 if `benefits` is non-NaN |
| `has_negatives` | 1 if `negatives` is non-NaN |
| `has_usage_format` | 1 if `usage_format` is non-NaN |

---

## DS4-specific strengths and limitations

**Strengths:**
- Largest dataset (2.5M events, 1,039 participants) — best statistical power for behavioral patterns
- 6 intervention types directly logged — unique type-specific outcome rates
- Longest observation window (897 days max) — best dataset for long-run volume and longitudinal-activity features. NOTE: this does NOT extend to the Group 6 adaptation features, which are restricted to the `intervention_event` class and therefore span at most 165.2 days (mean 62.2, median 64.6), because no `intervention_event` row exists before 2022-10-03.
- `days_since_first_event` is clean and forward-counting (unlike DS1's setup-time)

**Limitations:**
- No experimental condition — non-experimental, retrospective design
- Survey has no psychometric scales (qualitative text only) — 756 participants have no survey data
- `interventionDuration` / `interventionType` available for only 36.5% of events (intervention_event class)
- `secondsSinceStudySetup` and `weeksSinceStudySetup` are inverted — do not use
- `dismissed_other` (812 rows) represents undocumented dismissal types — excluded from rates

**Where Stage 2 harmonization would be possible:**
- `rate_opened_intervention_events` → comparable to `rate_opened` in DS1/DS5 (same event subset logic)
- `app_entropy`, `obs_window_days_ds4`, `events_per_day` → direct crossover
- `open_rate_change_calendar` → comparable to DS1 setup-time adaptation and DS5 calendar adaptation

---

## How to load

```python
import pandas as pd
from pathlib import Path

FEAT = Path("outputs/features/ds4")

beh = pd.read_csv(FEAT / "ds4_behavior_features.csv")
survey = pd.read_csv(FEAT / "ds4_survey_features.csv")

# Merge behavioral + demographics for 283 participants with survey
merged = beh.merge(survey, on="participant_id_canonical", how="left")
# has_survey == 1 only for 283 participants; remaining 756 have NaN survey columns
```

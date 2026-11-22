# DS5 Feature Definitions

**Dataset:** Dataset 5 — German adolescents (RCT)  
**Stage:** 1 — Dataset-specific feature extraction  
**Produced by:** `notebooks/13_ds5_feature_extraction.ipynb`  
**Source modules:** `src/features/ds5_features.py`, `src/features/behavioral_features.py`  
**Source files:** `outputs/cleaned/ds5_behavioral_clean.csv`, `ds5_pre_survey_clean.csv`, `ds5_post_survey_clean.csv`

---

## Output files

| File | Rows | Cols | Coverage |
|---|---|---|---|
| `ds5_behavior_features.csv` | 573 | 49 | All behavioral participants (+ study_condition joined) |
| `ds5_survey_features.csv` | 572 | 12 | Participants with behavioral + pre-survey |
| `ds5_prepost_features.csv` | 284 | 18 | Participants with behavioral + both surveys |

---

## Event definitions

| Concept | Definition |
|---|---|
| Event row | One row per friction-intervention event in `ds5_behavioral_clean.csv` |
| Intervention exposure | `is_intervention_event == 1` (friction was shown; duration > 0) |
| Reintervention event | `is_reintervention == 1` (subset of intervention events; reintervention condition) |
| Outcome-bearing row | `event_outcome_simple` ∈ {opened, dismissed, closed}; excludes 'missing' (3,457 rows, 1.2%) and 'dismissed_other' (119 rows, 0.04%) |
| Longitudinal axis | `days_since_first_event` — all rows, no NaN |
| Study condition | NOT in behavioral file — joined from pre-survey (`cond` column) |

---

## ds5_behavior_features.csv — Feature Definitions

### Group 1 — Volume and Activity
**Type:** DIRECT | **Confidence:** High | **Eligible:** 573

| Column | Description | NaN% |
|---|---|---|
| `study_condition` | Experimental condition: control / default / reintervention | 0.2% |
| `total_events` | Total event rows | 0% |
| `n_days_observed` | Distinct calendar days | 0% |
| `obs_window_days` | Days from first to last event | 0% |
| `events_per_day` | total_events / obs_window_days | 12.4% |
| `active_days_per_week` | n_days_observed / (obs_window/7) | 26.7% |
| `n_intervention_events` | is_intervention_event == 1 rows | 0% |
| `n_reintervention_events` | is_reintervention == 1 rows | 0% |

*1 participant with no pre-survey record has NaN study_condition.*

---

### Group 2 — Outcome Distribution
**Type:** DIRECT | **Confidence:** High | **Eligible:** 569 (4 participants have all-missing outcomes)

| Column | Description | NaN% |
|---|---|---|
| `n_outcome_bearing` | Non-missing, non-dismissed_other rows | 0% |
| `n_opened`, `n_dismissed`, `n_closed` | Raw counts | 0.7% |
| `rate_opened` | opened / n_outcome_bearing | 0.7% |
| `rate_dismissed` | dismissed / n_outcome_bearing | 0.7% |
| `rate_closed` | closed / n_outcome_bearing | 0.7% |
| `rate_not_opened` | (dismissed + closed) / n_outcome_bearing | 0.7% |
| `modal_outcome` | Most common outcome | 0.7% |

---

### Group 3 — Intervention-Event Outcome Rate
**Type:** DIRECT | **Confidence:** High | **Eligible:** ~307 participants with ≥5 intervention events

| Column | Description | NaN% |
|---|---|---|
| `open_rate_intervention_events` | Opened rate among `is_intervention_event == 1` rows only | 46.4% |
| `n_intervention_event_outcomes` | Count of outcome-bearing intervention events | 0% |

*High NaN (~46%) because control group has `is_intervention_event == 0` for all events.*

---

### Group 4 — Intervention Duration
**Type:** DIRECT | **Confidence:** Medium | **Eligible:** ~307 participants with ≥5 duration events

| Column | Description | NaN% |
|---|---|---|
| `mean_intervention_duration` | Mean intervention_duration_sec (>0) | 46.4% |
| `mean_duration_on_opened` | Mean duration on opened outcomes | 47.3% |
| `mean_duration_on_dismissed` | Mean duration on dismissed outcomes | 48.5% |
| `duration_open_vs_dismiss_delta` | mean_on_opened − mean_on_dismissed | 49.4% |
| `n_events_with_duration` | Rows with duration > 0 | 0% |

*NaN dominated by control condition (no friction exposure). Features meaningful for default and reintervention conditions only.*

---

### Group 5 — Reintervention Features (DS5+DS6 unique)
**Type:** DIRECT | **Confidence:** Medium-High for reintervention condition; Low for others | **Eligible:** 573

| Column | Description | NaN% |
|---|---|---|
| `has_reintervention` | 1 if any is_reintervention == 1 events | 0% |
| `n_reintervention_events` | Count of reintervention events | 0% |
| `reintervention_event_rate` | n_reintervention / total_events | 0% |
| `mean_reintervention_delay_sec` | Mean delay before re-intervention appears | 70.3% |
| `reintervention_open_rate` | Opened rate among reintervention events only | 72.6% |

*`mean_reintervention_delay_sec` and `reintervention_open_rate` are meaningful only for the reintervention condition (~263 participants). NaN for control and default.*

---

### Group 6 — App Structure
**Type:** DIRECT | **Confidence:** High | **Eligible:** 569

`n_unique_apps`, `top_app`, `top_app_share`, `top3_app_share`, `app_herfindahl`, `app_entropy`

---

### Group 7 — Temporal Structure
**Type:** DIRECT-DERIVED | **Confidence:** High (UTC timestamps used) | **Eligible:** ~500

`peak_hour_of_day`, `weekend_event_share`, `evening_event_share`, `morning_event_share`, `hour_entropy`

---

### Group 8 — Longitudinal Adaptation via Calendar Time
**Type:** PROXY | **Confidence:** Medium | **Eligible:** ~478 (≥10 outcome-bearing rows with varying days)

**Proxy note:** Shorter study windows than DS4; condition confounds the trajectory. Best interpreted within each condition at modeling time.

| Column | Description | NaN% |
|---|---|---|
| `open_rate_early_third_calendar` | Opened rate in first tertile of days_since_first_event | 16.6% |
| `open_rate_late_third_calendar` | Opened rate in last tertile | 16.6% |
| `open_rate_change_calendar` | late − early (positive = increasing override) | 16.6% |
| `dismiss_rate_early_third_calendar` | First tertile dismissed rate | 16.6% |
| `dismiss_rate_late_third_calendar` | Last tertile dismissed rate | 16.6% |
| `dismiss_rate_change_calendar` | late − early | 16.6% |

---

### Group 9 — Override Tendency
**Type:** PROXY — Behavioral | **Confidence:** Medium | **Eligible:** ~487

`max_consecutive_opens`, `mean_open_run_length`, `p_open_after_dismiss`

---

## ds5_survey_features.csv — Feature Definitions

### Group 10 — Pre-survey Psychosocial Scales (DS5-unique)
**Type:** DIRECT | **Confidence:** High | **Eligible:** 572

**DS5-unique:** Belonging (8-item), ostracism (5-item), and FoMO (10-item) scales are validated psychometric instruments. These dimensions do not appear in DS1, DS4, or DS6 in equivalent form.

| Column | Description |
|---|---|
| `study_condition` | Condition: control / default / reintervention |
| `age` | Age in years (13–25) |
| `belong_mean_pre` | Mean of 8 belonging items (pre-survey) |
| `ostracism_mean_pre` | Mean of 5 ostracism items (pre-survey) |
| `fomo_mean_pre` | Mean of 10 FoMO items (pre-survey) |
| `digital_wellbeing_pre` | Self-rated digital well-being (single item) |
| `prob_self_pre` | Perceived personal social media problem severity |
| `prob_peers_pre` | Perceived peer problem severity |
| `time_peers_pre` | Perceived peer screen time |
| `social_media_wellbeing_pre` | Social media–specific well-being (single item) |
| `hours_pre` | Self-reported daily social media hours |

---

## ds5_prepost_features.csv — Feature Definitions

### Group 11 — Post-survey Psychosocial
**Type:** DIRECT | **Confidence:** High | **Eligible:** 284

| Column | Description |
|---|---|
| `study_condition` | Condition (joined from pre-survey) |
| `belong_mean_post`, `ostracism_mean_post`, `fomo_mean_post` | Post-survey scale means |
| `digital_wellbeing_post`, `prob_self_post`, `social_media_wellbeing_post` | Post-survey ratings |
| `hours_post` | Post-study self-reported daily hours |
| `solve_prob_post` | Did the intervention help solve the stated problem? (Likert) |
| `address_goal_post` | Did the intervention address the stated goal? (Likert) |

*`solve_prob_post` and `address_goal_post` are interpretable for intervention groups only. Control participants received no intervention.*

---

### Group 12 — Pre-Post Change Scores
**Type:** DIRECT-DERIVED | **Confidence:** Medium | **Eligible:** 284

**Sign convention:** positive = increase post-intervention. For belonging / wellbeing: positive = improvement. For prob_self / ostracism: positive = worsening. Interpret within condition.

| Column | Description |
|---|---|
| `belong_change` | post − pre belonging mean |
| `ostracism_change` | post − pre ostracism mean |
| `fomo_change` | post − pre FoMO mean |
| `digital_wellbeing_change` | post − pre digital wellbeing |
| `prob_self_change` | post − pre personal problem severity |
| `social_media_wellbeing_change` | post − pre SM wellbeing |
| `hours_change` | post − pre self-reported hours |

---

## DS5-specific strengths and limitations

**Strengths:**
- Only RCT dataset in this project — three conditions (control / default / reintervention) allow causal comparison
- Reintervention timing (`reintervention_delay_sec`) is DS5+DS6 unique — directly observable
- Pre/post belonging, ostracism, and FoMO scales (validated psychometric instruments) — DS5-unique content
- Pre-to-post psychosocial change layer for 284 participants

**Limitations:**
- Study windows shorter than DS4 — longitudinal adaptation features less reliable
- Control group has no friction exposure: many features (duration, reintervention, open_rate_intervention_events) are NaN for ~265 control participants
- 1 behavioral participant missing condition — excluded from condition-level comparisons
- `reason` column (German free text, 42.3% NaN) not featurized — requires NLP for future use

**Where Stage 2 harmonization would be possible:**
- `rate_opened`, `app_entropy`, `events_per_day`, `obs_window_days` → direct crossover
- `open_rate_change_calendar` → comparable to DS1 and DS4 adaptation features
- Psychosocial scales: partial overlap with DS6 (FoMO appears in both) but scales differ; treat as comparable with explicit caution

---

## How to load

```python
import pandas as pd
from pathlib import Path

FEAT = Path("outputs/features/ds5")

beh = pd.read_csv(FEAT / "ds5_behavior_features.csv")
survey = pd.read_csv(FEAT / "ds5_survey_features.csv")
prepost = pd.read_csv(FEAT / "ds5_prepost_features.csv")

# Full merge: behavior + pre-survey + pre-post change
merged = beh.merge(survey, on="participant_id_canonical", how="left", suffixes=("", "_survey"))
merged_full = merged.merge(prepost, on="participant_id_canonical", how="left", suffixes=("", "_prepost"))

# Filter to reintervention condition for reintervention-specific features
ri_only = beh[beh["study_condition"] == "reintervention"]
```

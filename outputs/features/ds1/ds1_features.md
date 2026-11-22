# DS1 Feature Definitions

**Dataset:** Dataset 1 — Compact friction intervention testing  
**Stage:** 1 — Dataset-specific feature extraction  
**Produced by:** `notebooks/11_ds1_feature_extraction.ipynb`  
**Source modules:** `src/features/ds1_features.py`, `src/features/behavioral_features.py`  
**Source files:** `outputs/cleaned/ds1_behavioral_clean.csv`, `ds1_pre_survey_clean.csv`, `ds1_post_survey_clean.csv`

---

## Output files

| File | Rows | Cols | Coverage |
|---|---|---|---|
| `ds1_behavior_features.csv` | 619 | 37 | All behavioral participants |
| `ds1_survey_features.csv` | 527 | 16 | Behavioral participants with pre-survey |
| `ds1_prepost_features.csv` | 168 | 14 | Participants with behavioral + both surveys |

---

## Event definitions

| Concept | Definition |
|---|---|
| Event row | One row per intervention trigger in `ds1_behavioral_clean.csv` |
| Intervention exposure | All rows — every DS1 event implies friction was shown |
| Outcome-bearing row | `event_outcome_simple` ∈ {opened, dismissed, closed}; excludes 467 'missing' rows (0.1%) |
| Longitudinal axis | `secondsSinceOneSecSetup` — available for 81.1% of events, but missingness is participant-level, not event-level: 529 participants have the field on 100% of their rows and 90 have it on 0%, with none in between. The 90 excluded participants are almost entirely the first enrollment wave (68 first appear in 2021-04, 14 in 2021-05). G5/G6 therefore describe a ~June-2021-onward sub-cohort, not a random 81% of events. Within an included participant the tertile split is unbiased. |

---

## ds1_behavior_features.csv — Feature Definitions

### Group 1 — Volume and Activity
**Type:** DIRECT | **Confidence:** High | **Eligible participants:** 619

| Column | Description | NaN% |
|---|---|---|
| `total_events` | Total event rows for participant | 0% |
| `n_days_observed` | Distinct calendar days with ≥1 event | 0% |
| `obs_window_days` | Days from first to last event | 0% |
| `events_per_day` | total_events / obs_window_days | 17.4% |
| `active_days_per_week` | n_days_observed / (obs_window_days/7) | 25.5% |

*NaN in events_per_day: participants with single-day obs window (window = 0).*

---

### Group 2 — Outcome Distribution
**Type:** DIRECT | **Confidence:** High | **Eligible participants:** 618 (1 participant has all-missing outcomes)

| Column | Description | NaN% |
|---|---|---|
| `n_outcome_bearing` | Rows with non-missing outcome | 0% |
| `n_opened`, `n_dismissed`, `n_closed` | Raw counts per outcome | 0.2% |
| `rate_opened` | opened / n_outcome_bearing | 0.2% |
| `rate_dismissed` | dismissed / n_outcome_bearing | 0.2% |
| `rate_closed` | closed / n_outcome_bearing | 0.2% |
| `rate_not_opened` | (dismissed + closed) / n_outcome_bearing — friction compliance rate | 0.2% |
| `modal_outcome` | Most common outcome per participant | 0.2% |

---

### Group 3 — App Structure
**Type:** DIRECT | **Confidence:** High | **Eligible participants:** 619

| Column | Description | NaN% |
|---|---|---|
| `n_unique_apps` | Distinct app names targeted | 0% |
| `top_app` | Most frequently targeted app | 0% |
| `top_app_share` | top_app events / total_events | 0% |
| `top3_app_share` | Top 3 apps combined share | 0% |
| `app_herfindahl` | Sum of squared per-app shares (concentration) | 0% |
| `app_entropy` | Shannon entropy of app event distribution (diversity) | 0% |

---

### Group 4 — Temporal Structure
**Type:** DIRECT-DERIVED | **Confidence:** High | **Eligible participants:** 511 (108 participants with fewer than 2 events return NaN — the gate in `temporal_features()` is `len(df) >= 2`, not a single-day observation window; 118 participants have a single-day window, a different set)

| Column | Description | NaN% |
|---|---|---|
| `peak_hour_of_day` | Hour (0–23) with most events | 17.4% |
| `weekend_event_share` | Proportion of events on Sat/Sun | 17.4% |
| `evening_event_share` | Proportion of events 18:00–23:00 | 17.4% |
| `morning_event_share` | Proportion of events 06:00–11:00 | 17.4% |
| `hour_entropy` | Shannon entropy of hour-of-day distribution (context diversity) | 20.2% |

*Timezone assumption: DS1 timestamps treated as UTC (not confirmed in codebook).*

---

### Group 5 — Setup-Time Window (DS1-unique)
**Type:** DIRECT | **Confidence:** High (count) / Medium (window estimate) | **Eligible:** 619

| Column | Description | NaN% |
|---|---|---|
| `n_events_with_setup_time` | Rows with non-NaN `secondsSinceOneSecSetup` | 0% |
| `setup_window_days` | Max secondsSinceOneSecSetup / 86400 — participant's active span from app setup | 32.3% |

*`setup_window_days` NaN for participants with < 5 rows having setup time.*

---

### Group 6 — Longitudinal Adaptation via Setup-Time (DS1-unique)
**Type:** PROXY | **Confidence:** Medium | **Eligible:** 410 participants (threshold: ≥10 outcome-bearing events with setup time and a non-zero setup-time span)

**Proxy note:** Change in outcome rates across the setup-time axis is consistent with behavioral adaptation but may also reflect attrition, changing app mix, or life context. There is no experimental control condition in DS1.

| Column | Description | NaN% |
|---|---|---|
| `open_rate_early_third_setup` | Opened rate in first tertile of `secondsSinceOneSecSetup` | 33.8% |
| `open_rate_late_third_setup` | Opened rate in last tertile | 33.8% |
| `open_rate_change_setup` | late − early opened rate (positive = increasing override over time) | 33.8% |
| `dismiss_rate_early_third_setup` | Dismissed rate in first tertile | 33.8% |
| `dismiss_rate_late_third_setup` | Dismissed rate in last tertile | 33.8% |
| `dismiss_rate_change_setup` | late − early dismissed rate | 33.8% |

---

### Group 7 — Override Tendency Streaks
**Type:** PROXY — Behavioral | **Confidence:** Medium | **Eligible:** ~504 participants (threshold: ≥5 outcome-bearing rows)

**Proxy note:** Consecutive opens are consistent with habitual override but individual open decisions may be intentional. Interpret as a behavioral regularity indicator, not a direct self-control measure.

| Column | Description | NaN% |
|---|---|---|
| `max_consecutive_opens` | Longest run of consecutive `opened` outcomes | 18.6% |
| `mean_open_run_length` | Mean length of `opened` outcome runs | 18.6% |
| `p_open_after_dismiss` | P(next outcome = opened | current outcome = dismissed) | 18.6% |

---

## ds1_survey_features.csv — Feature Definitions

### Group 8 — Pre-survey Psychosocial Baseline
**Type:** DIRECT | **Confidence:** High (Likert scales) / Medium (multi-select counts) | **Eligible:** 527

| Column | Description |
|---|---|
| `problematic_cons_pre` | Self-rated problematic consumption (1–7 Likert) |
| `happy_pre` | Happiness with social media use (1–7 Likert) |
| `problematic_cons_general_pre` | Opinion on problematic consumption in general (1–7) |
| `problematic_cons_compared_pre` | Perceived consumption relative to others (1–7) |
| `hours_self_reported_pre` | Self-reported daily social media hours |
| `n_problems_selected` | Count of selected problem categories |
| `n_goals_selected` | Count of selected goal categories |
| `problem_another_problem` | Binary flag — selected "Another problem" |
| `problem_automatic_consumption` | Binary flag |
| `problem_excessive_consumption` | Binary flag |
| `problem_feeling_of_no_control` | Binary flag |
| `goal_another_goal` | Binary flag |
| `goal_consuming_selectively` | Binary flag |
| `goal_less_consumption` | Binary flag |
| `goal_more_awareness_of_consumption` | Binary flag |

---

## ds1_prepost_features.csv — Feature Definitions

### Group 9 — Post-survey + Pre-Post Change
**Type:** DIRECT (post scores) / DIRECT-DERIVED (change scores) | **Confidence:** High (scores) / Medium (change — attrition risk) | **Eligible:** 168

**Change score convention:** positive = increase post-intervention. For problematic consumption scales, positive = worsening. For happiness, positive = improvement. Interpret within individual analysis, not across raw means.

| Column | Description |
|---|---|
| `problematic_cons_post` | Post-study problematic consumption (1–7) |
| `happy_post` | Post-study happiness with social media use (1–7) |
| `problematic_cons_general_post` | Post-study general opinion (1–7) |
| `problematic_cons_compared_post` | Post-study relative perception (1–7) |
| `problems_solved_post` | Self-reported: did problems get solved? (1–5: 1 = not at all … 5 = completely) |
| `goals_reached_post` | Self-reported: were goals reached? (1–5: 1 = not at all … 5 = completely) |
| `progress_satisfaction_post` | Satisfaction with progress (1–7) |
| `hours_self_reported_post` | Post-study self-reported daily hours |
| `problematic_cons_change` | post − pre problematic_cons |
| `happy_change` | post − pre happiness |
| `problematic_cons_general_change` | post − pre general opinion |
| `problematic_cons_compared_change` | post − pre relative perception |
| `hours_change` | post − pre self-reported hours |

---

## DS1-specific strengths and limitations

**Strengths:**
- `secondsSinceOneSecSetup` provides a precise individual-level longitudinal time axis anchored to app setup — not available in this form in DS4/DS5/DS6
- Pre/post survey with problematic consumption and happiness scales (DS1-unique content)
- Fully binary problem/goal flags (DS1-unique structure)
- Clean, small dataset — good for pipeline testing and baseline modeling

**Limitations:**
- No experimental condition — no control group for causal comparison
- 619 behavioral participants but only 168 fully linked (behavioral + both surveys)
- 18.9% NaN in `secondsSinceOneSecSetup` limits adaptation feature coverage to ~81% of events
- `purpose` column (71.3% NaN) not featurized — qualitative supplement only
- Timestamps assumed UTC — not confirmed in codebook

**Where Stage 2 harmonization would be possible:**
- `rate_opened`, `app_entropy`, `obs_window_days`, `events_per_day` — direct crossover
- `open_rate_change_*` adaptation features — time axis differs (setup-time vs calendar-time) but logic is comparable

---

## How to load

```python
import pandas as pd
from pathlib import Path

FEAT = Path("outputs/features/ds1")

beh = pd.read_csv(FEAT / "ds1_behavior_features.csv")
survey = pd.read_csv(FEAT / "ds1_survey_features.csv")
prepost = pd.read_csv(FEAT / "ds1_prepost_features.csv")

# Merge behavioral + survey for participants with both
merged = beh.merge(survey, on="participant_id_canonical", how="left")
# Merge in prepost change scores (168 participants)
merged_full = merged.merge(prepost, on="participant_id_canonical", how="left")
```

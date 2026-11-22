# ds5_behavioral_clean.csv

**Source dataset:** Dataset 5 — German adolescents  
**Source file:** `data_raw/5. data set, German adolescents/Behavior data set/behavior_data_set_5.csv`  
**Producing notebook:** `notebooks/06_dataset_5_cleaning.ipynb`  
**Rows:** 288,688  
**Columns:** 19  
**Unit of observation:** One app-opening or friction-intervention event per row

---

## What this file contains

Each row represents a single behavioral event — either a participant attempting to open an app (triggering a friction intervention) or the subsequent outcome of that attempt. Events are tied to individual participants in a three-group experimental study (control, default friction, reintervention). The file contains UTC-normalized timestamps, simplified outcome labels, intervention duration and re-intervention delay fields, and the original German-language reason annotations.

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `participant_id_raw` | string | Original `userid` from raw file (includes full study prefix) |
| `participant_id_canonical` | string | Cleaned participant ID after stripping `study-one-sec-next-gen-bzkj-2024-` prefix; matches `uuid` in survey files |
| `event_timestamp_utc` | datetime[UTC] | Event time in UTC, localized from local timestamp + timezone column |
| `event_timestamp_local` | datetime | Original local timestamp (naive, no tz info) |
| `event_timezone` | string | IANA timezone string from raw file (e.g. `Europe/Berlin`) |
| `app_name` | string | App that triggered the event; NaN for 3,457 missing-resolution rows |
| `event_outcome_raw` | string | Original `resolution` value from raw file |
| `event_outcome_simple` | string | Simplified outcome: `opened`, `dismissed`, `closed`, `dismissed_other`, `missing` |
| `intervention_duration_sec` | float | Friction duration in seconds; 0.0 for opened events; NaN for 48,742 rows |
| `reintervention_delay_sec` | float | Seconds until re-intervention appears; NaN for ~78% (non-reintervention group) |
| `is_intervention_event` | int | 1 if `intervention_duration_sec` > 0 (friction was shown), else 0 |
| `is_reintervention` | int | 1 if re-intervention delay is present, else 0 |
| `days_since_first_event` | float | Days elapsed since participant's first event in behavioral dataset |
| `reason` | string | German free-text reason stated by participant; 42.3% NaN |
| `suggestionBannerShown` | string | Text of suggestion banner shown; 99%+ NaN |
| `suggestionDetailViewAppear` | float | Timestamp when suggestion detail appeared; 99.9%+ NaN |
| `suggestionDetailViewDisappear` | float | Timestamp when suggestion detail disappeared; 99.9%+ NaN |
| `terminationReason` | string | `terminatedByUser` for 12 rows; otherwise NaN |
| `suggestionLearnMoreLinkTapped` | float | Timestamp if learn-more link was tapped; 99.9%+ NaN |

---

## Key Distributions

### Event outcome
| event_outcome_simple | Count | % |
|---|---|---|
| opened | 177,986 | 61.6% |
| dismissed | 62,107 | 21.5% |
| closed | 45,019 | 15.6% |
| missing | 3,457 | 1.2% |
| dismissed_other | 119 | 0.04% |

### Participants
- 573 unique participants
- 572 linked to pre-survey (condition known for 572)

---

## Cleaning Steps Applied

1. Loaded raw CSV with semicolon delimiter
2. Preserved original `userid` as `participant_id_raw`
3. Stripped `study-one-sec-next-gen-bzkj-2024-` prefix → `participant_id_canonical`
4. Parsed `timestamp` as naive datetime; localized per `timezone` column using `zoneinfo`; converted to UTC → `event_timestamp_utc`
5. Applied fallback timezone `Europe/Berlin` for 3,457 rows where timezone was NaN
6. Mapped `resolution` → `event_outcome_raw` (preserved) and `event_outcome_simple` (5-class simplified)
7. Cast `interventionDuration` → `intervention_duration_sec` (float)
8. Cast `timeIntervalUntilReIntervention` → `reintervention_delay_sec` (float)
9. Derived `is_intervention_event` = 1 if duration > 0
10. Derived `is_reintervention` = 1 if reintervention delay is not NaN
11. Computed `days_since_first_event` per participant from UTC timestamps
12. Renamed `app` → `app_name`, `timezone` → `event_timezone`
13. Zero duplicate rows confirmed

---

## Known Limitations

- `cond` (study condition) is NOT in this file — must join from `ds5_pre_survey_clean.csv` via `participant_id_canonical`
- 1 behavioral participant has no pre-survey record (condition unknown)
- `reason` is German free text — not yet categorized or coded
- Suggestion columns are nearly entirely NaN; not usable for most participants
- Timezone localization may be inaccurate for participants who traveled mid-study
- `dismissedByStructuredIntervention` (119 rows) is undocumented; mapped to `dismissed_other`
- 3,457 rows with NaN resolution likely represent app events where OneSec data was not fully captured

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

# Load behavioral
beh = pd.read_csv(OUT / "ds5_behavioral_clean.csv",
                  parse_dates=["event_timestamp_utc", "event_timestamp_local"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)

# Load pre-survey to get study condition
pre = pd.read_csv(OUT / "ds5_pre_survey_clean.csv")
cond_map = pre.set_index("participant_id_canonical")["cond"]

# Join condition
beh["study_condition"] = beh["participant_id_canonical"].map(cond_map)

# Filter to complete events only
beh_clean = beh[beh["event_outcome_simple"] != "missing"].copy()
print(beh_clean.shape)
```

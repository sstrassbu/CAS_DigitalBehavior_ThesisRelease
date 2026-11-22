# ds6_behavioral_clean.csv

**Source dataset:** Dataset 6 — Danish adolescents  
**Source file:** `data_raw/6. data set, Danish adolescents/Data/behavioral data/session_time_dataset_97_5_cutoff_data_forwarded.csv`  
**Producing notebook:** `notebooks/08_dataset_6_cleaning.ipynb`  
**Rows:** 353,796  
**Columns:** 34  
**Unit of observation:** One app-opening event per row (both baseline and intervention periods)

---

## What this file contains

Each row represents a single app-opening event from a Danish adolescent participant. Unlike DS1 and DS5, this file contains **only openedApp ROWS** — but the raw event log underlying it actually alternates Open→Close→Open→Close; the close half was exported into look-ahead columns (`time_diff_secs`, and the raw `close_ts`) rather than as its own rows. The file covers both the baseline period and the intervention period. **`group_id` does NOT provide session-level grouping** — verified 2026-08-05 to be unique per row throughout the file (see Known Limitations below) — but `time_diff_secs`/`time_diff_minutes` ARE genuine open→close dwell time for ~99% of rows (verified 2026-08-06). **`app_next` does NOT mean "next app opened"** — verified 2026-08-06 to mechanically echo the current row's own app_name 99.3% of the time (it reflects the close-record's app field, not a real subsequent choice); `app_prev` is the reliable field for sequence/substitution analysis. See Known Limitations below for both findings in full.

---

## Column Reference

### Identity and time
| Column | Type | Description |
|---|---|---|
| `participant_id_raw` | string | Original `ID` from raw file |
| `participant_id_canonical` | string | Same as `participant_id_raw` (no transformation needed) |
| `event_timestamp_utc` | datetime[UTC] | Event time in UTC (parsed from ISO 8601 string) |
| `event_date` | date | Calendar date of event |
| `days_since_first_event` | float | Days elapsed since participant's first event |

### App and outcome
| Column | Type | Description |
|---|---|---|
| `app_name` | string | App name that triggered the event |
| `event_outcome_raw` | string | Original `resolution` value (always `openedApp`) |
| `event_outcome_simple` | string | Simplified outcome (always `opened`) |

### Study design
| Column | Type | Description |
|---|---|---|
| `study_condition` | string | Text condition: `control`, `default`, `intervention` |
| `study_condition_num` | int | Numeric condition code (1–6; cohort-level) |
| `study_period` | string | `baseline` or `intervention` |
| `participation_day` | int | Day number within study |
| `study_week` | int | Study week number |
| `study_day_of_week` | int | Numeric day of week |
| `hour_of_day` | int | Hour of day (0–23) in **Europe/Copenhagen local time** (verified: exactly +2 CEST / +1 CET relative to `event_timestamp_utc`, no other offsets). ⚠ `event_timestamp_utc` and `event_date` are UTC — the two are 1–2h apart and 2.36% of events fall on a different local calendar date than `event_date`. |

### Intervention
| Column | Type | Description |
|---|---|---|
| `intervention_duration_sec` | float | Duration of friction intervention shown; NaN if no intervention |
| `intervention_type` | string | Type: `denmark`, `breathingExercise`, `math`, `followTheDot`, `randomText`; NaN for ~67% |
| `is_reintervention` | int | 1 if this was a re-intervention attempt |
| `reintervention_delay_sec` | float | Seconds until re-intervention; NaN for ~86% |

### Session grouping (⚠ non-functional — kept for provenance only, see Known Limitations)
| Column | Type | Description |
|---|---|---|
| `group_id` | int | **Does not group events into sessions** — unique per row across the whole file |
| `first_in_group` | int | **Constant** — always 1 |
| `last_close_in_group` | int | **Constant** — always 0 |
| `time_diff_secs` | float | Seconds until next logged event — for ~99% of rows this next event is a real app-close, so this is genuine open→close dwell time (verified 2026-08-06), not merely "time to next event" |
| `time_diff_minutes` | float | Same as `time_diff_secs`, in minutes |

### Sequence features (pre-engineered)
| Column | Type | Description |
|---|---|---|
| `app_next` | string | **NOT "next app opened"** (verified 2026-08-06) — mechanically echoes app_name 99.3% of the time, since the next logged event is usually this same app's own close. Do not use for transition/substitution analysis; use `app_prev` instead. |
| `app_next2` | string | The genuine next distinct app opened (skips the intervening close) — usable, but requires conditioning on `resolution_next2=='openedApp'` |
| `app_next3` | string | Close-echo of `app_next2`, same mechanism as `app_next` — not a third distinct app |
| `app_prev` | string | App opened immediately before this event — verified genuine 2026-08-06 (not affected by the app_next issue; ~42% same-app rate, plausible non-mechanical split) |
| `app_prev2` | string | App opened 2 events before — same verification, also genuine |
| `resolution_next` | string | Outcome of next event |
| `resolution_next2` | string | Outcome of 2nd next event |
| `resolution_next3` | string | Outcome of 3rd next event |

### Other
| Column | Type | Description |
|---|---|---|
| `purpose` | string | Stated purpose; 88.8% NaN |
| `row_id` | int | Unique row identifier from original file |

---

## Key Distributions

### Study period
| period | Count |
|---|---|
| intervention | 194,907 |
| baseline | 158,889 |

### Study condition
| condition | Count |
|---|---|
| control | 153,236 |
| default | 100,888 |
| intervention | 99,672 |

### Intervention types (non-NaN only)
| interventionType | Count |
|---|---|
| denmark | 68,528 |
| breathingExercise | 39,116 |
| math | 2,676 |
| followTheDot | 1,469 |

---

## Cleaning Steps Applied

1. Loaded raw CSV with comma delimiter
2. Kept `ID` as-is → `participant_id_raw` and `participant_id_canonical`
3. Parsed `timestamp` with `pd.to_datetime(utc=True)` → `event_timestamp_utc`
4. Extracted calendar date → `event_date`
5. Set `event_outcome_raw` = `resolution` (= openedApp), `event_outcome_simple` = `'opened'`
6. Cast intervention columns to float; `is_reintervention` as int
7. Computed `days_since_first_event` per participant
8. Mapped `cond` → `study_condition_num`, `condition` → `study_condition`, `period` → `study_period`
9. Retained all pre-engineered sequence and session features
10. Renamed `app` → `app_name`, `hour` → `hour_of_day`, `week` → `study_week`
11. Zero duplicate rows confirmed

---

## Known Limitations

- **Only openedApp events** — no dismiss or close outcome values in this file
- **No genuine session-*count* data** (found 2026-08-05): `group_id` is unique per row across all 353,796 rows in the raw file (does not group events into sessions), `first_in_group`/`last_close_in_group` are constant (1/0) for every row. See `data_docs/modeling_cautions.md` §6 and `outputs/reports/stage0/ds6_audit_report.md` §8a.
- **But open→close dwell time IS genuine** (corrected 2026-08-06, retracting part of the above finding as originally stated): the raw file's `close_ts` column (dropped during cleaning, not present here) equals `openedapp_open_time + time_diff_secs` exactly, and the next logged event is a real app-close 99.4% of the time (`resolution_next == 'closedApp'`) — so `time_diff_secs`/`time_diff_minutes` represent genuine session dwell time for the large majority of rows, not merely "time to next event with no particular meaning" as an earlier version of this note claimed.
- **`app_next`/`app_next3` do NOT mean "next app opened"** (found 2026-08-06): mechanically echo the current row's own app_name ~99.3% of the time (they reflect the close-record's app field). Use `app_prev`/`app_prev2` (verified genuine) or `app_next2` (verified genuine, requires conditioning on `resolution_next2=='openedApp'`) for real sequence/substitution analysis. See `data_docs/modeling_cautions.md` §6 and `outputs/reports/stage0/ds6_audit_report.md` §8b for the full verification.
- 243 participants vs 399 in demographics — 156 enrolled participants have no behavioral events
- `purpose` is 89% NaN — unsuitable for routine analysis
- `study_condition_num` (1–6) encodes cohort/school groups, not directly interpretable without further study design documentation
- The pre-survey Qualtrics file is not yet cleaned and not merged into this file

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

beh = pd.read_csv(OUT / "ds6_behavioral_clean.csv",
                  parse_dates=["event_timestamp_utc", "event_date"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)

# Filter to intervention period only
intervention_only = beh[beh["study_period"] == "intervention"].copy()

# Merge demographics
demo = pd.read_csv(OUT / "ds6_demographics_clean.csv")
merged = beh.merge(demo[["participant_id_canonical", "age", "gender", "region"]],
                   on="participant_id_canonical", how="left")
print(merged.shape)
```

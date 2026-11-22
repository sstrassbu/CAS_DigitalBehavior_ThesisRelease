# ds5_participant_linkage.csv

**Source dataset:** Dataset 5 — German adolescents  
**Producing notebook:** `notebooks/06_dataset_5_cleaning.ipynb`  
**Rows:** 793 (all unique participant IDs across behavioral, pre-survey, and post-survey)  
**Columns:** 10  
**Unit of observation:** One row per unique participant

---

## What this file contains

One row per unique participant ID found in any of the three DS5 files (behavioral, pre-survey, post-survey). Flags indicate which files each participant appears in. Condition (from pre-survey) and behavioral summary statistics are merged in.

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Canonical participant ID (survey uuid format) |
| `in_behavioral` | bool | True if participant appears in behavioral file |
| `in_pre_survey` | bool | True if participant appears in pre-survey |
| `in_post_survey` | bool | True if participant appears in post-survey |
| `study_condition` | string | `control`, `default`, or `reintervention` (from pre-survey); NaN if no pre-survey record |
| `n_events` | int | Total behavioral events for this participant |
| `n_opened` | int | Count of `opened` events |
| `n_dismissed` | int | Count of `dismissed` events |
| `n_closed` | int | Count of `closed` events |
| `days_observed` | float | Days from first to last behavioral event |

---

## Overlap Summary

| Group | Count |
|---|---|
| Behavioral only (no survey match) | 1 |
| Pre-survey only (no behavioral data) | 220 |
| Behavioral + pre-survey only | 288 |
| All three (behavioral + pre + post) | 284 |
| **Total unique participants** | **793** |

---

## Cleaning Steps Applied

1. Collected all unique `participant_id_canonical` values from behavioral, pre-survey, and post-survey
2. Created binary flags `in_behavioral`, `in_pre_survey`, `in_post_survey`
3. Merged condition from pre-survey (`cond` column)
4. Merged per-participant event summary from behavioral (counts of each outcome, days observed)

---

## Known Limitations

- 220 participants enrolled (pre-survey) but have no behavioral data
- 1 behavioral participant has no pre-survey record (condition = NaN)
- `n_events` and derived columns are NaN for participants without behavioral data

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

linkage = pd.read_csv(OUT / "ds5_participant_linkage.csv")

# Participants in all three files
core = linkage[linkage["in_behavioral"] & linkage["in_pre_survey"] & linkage["in_post_survey"]]
print(f"Full-data participants: {len(core)}")  # 284

# Load and join behavioral
beh = pd.read_csv(OUT / "ds5_behavioral_clean.csv",
                  parse_dates=["event_timestamp_utc"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)
beh_with_cond = beh.merge(
    linkage[["participant_id_canonical", "study_condition"]],
    on="participant_id_canonical", how="left"
)
```

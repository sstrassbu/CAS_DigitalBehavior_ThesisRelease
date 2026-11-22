# ds6_participant_linkage.csv

**Source dataset:** Dataset 6 — Danish adolescents  
**Producing notebook:** `notebooks/08_dataset_6_cleaning.ipynb`  
**Rows:** 399 (all enrolled participants from demographic file)  
**Columns:** 13  
**Unit of observation:** One row per participant

---

## What this file contains

One row per enrolled participant, merging behavioral summary statistics, demographic attributes, and file-membership flags. All 399 participants from demographics are included; 156 have no behavioral data.

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Canonical participant ID (15-char alphanumeric) |
| `in_behavioral` | bool | True if participant appears in behavioral file |
| `in_demographics` | bool | True if participant appears in demographic file (all 399 = True) |
| `in_survey` | bool | True if participant appears in survey_clean file |
| `study_condition` | string | `control`, `default`, or `intervention` (from behavioral events) |
| `n_events` | int | Total behavioral events for this participant; NaN if no behavioral data |
| `n_baseline` | int | Number of events in baseline period |
| `n_intervention` | int | Number of events in intervention period |
| `n_reintervention_events` | int | Count of `is_reintervention = 1` events |
| `days_observed` | float | Days from first to last behavioral event |
| `age` | int | Age in years (from demographics) |
| `gender` | string | English gender label (from demographics) |
| `region` | string | Danish region (from demographics) |

---

## Overlap Summary

| Group | Count |
|---|---|
| Behavioral only (no demo / survey) | 0 |
| Demo only (no behavioral data) | 156 |
| Behavioral + demo + survey | 243 |
| **Total** | **399** |

---

## Cleaning Steps Applied

1. Used demographic file as the master list (399 participants)
2. Created binary flags for behavioral and survey membership
3. Merged `study_condition` from behavioral (first non-NaN value per participant)
4. Merged event summary: total, baseline, intervention, reintervention counts, and days_observed
5. Merged age, gender, region from demographic file

---

## Known Limitations

- `n_events` and behavioral summary columns are NaN for 156 participants without behavioral data
- `study_condition` is NaN for demographic-only participants
- 1 participant has NaN gender

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/cleaned")

linkage = pd.read_csv(OUT / "ds6_participant_linkage.csv")

# Participants with behavioral data
active = linkage[linkage["in_behavioral"]].copy()
print(f"Participants with behavioral data: {len(active)}")  # 243

# Merge with behavioral for full analysis
beh = pd.read_csv(OUT / "ds6_behavioral_clean.csv",
                  parse_dates=["event_timestamp_utc"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)
beh_full = beh.merge(
    linkage[["participant_id_canonical", "age", "gender", "region", "study_condition"]],
    on="participant_id_canonical", how="left"
)
```

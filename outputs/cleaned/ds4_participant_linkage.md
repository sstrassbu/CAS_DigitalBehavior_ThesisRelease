# ds4_participant_linkage.csv

**Source dataset:** Dataset 4 — Large non-experimental data (historic, retrospective use)
**Produced by:** `notebooks/04_dataset_4_cleaning.ipynb`
**Rows:** 1,055
**Columns:** 4

---

## What this file contains

One row per unique participant seen in any DS4 file. Each row indicates which files (behavioral, survey) the participant appears in. Use this table to select the right analysis population for any given question.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Canonical participant ID. Matches `participant_id_canonical` in `ds4_behavioral_clean.csv` and `ds4_survey_clean.csv`. |
| `in_behavioral` | bool | True if participant appears in the behavioral file. |
| `in_survey` | bool | True if participant appears in the survey file (after dedup and prefix stripping). |
| `n_files` | int | Number of files the participant appears in (1 or 2). |

---

## Overlap summary

| Group | N | Interpretation |
|---|---|---|
| Behavioral + survey (`n_files == 2`) | 283 | Fully linkable — behavioral events + psychosocial context available |
| Behavioral only (`in_behavioral=True, in_survey=False`) | 756 | Behavioral analysis only — no psychosocial variables |
| Survey only (`in_behavioral=False, in_survey=True`) | 16 | Survey responses only — no behavioral events |
| **Total unique participants** | **1,055** | |

Note: 756 behavioral-only participants have rich longitudinal event data but zero survey information. They are valid for behavioral analysis (adaptation, frequency, outcome patterns) but cannot be used in analyses requiring psychosocial moderators.

---

## Cleaning steps applied

1. Collected unique `participant_id_canonical` values from both cleaned files
2. Created binary membership flags per file
3. Derived `n_files` as sum of flags

---

## How to load

```python
import pandas as pd

link = pd.read_csv("outputs/cleaned/ds4_participant_linkage.csv")

# Select fully-linked participants (behavioral + survey)
linked_ids = link[link["n_files"] == 2]["participant_id_canonical"].tolist()
# -> 283 participants

# Select behavioral-only participants
beh_only_ids = link[link["in_behavioral"] & ~link["in_survey"]]["participant_id_canonical"].tolist()
# -> 756 participants

# Filter behavioral data to linked participants only
beh = pd.read_csv("outputs/cleaned/ds4_behavioral_clean.csv", parse_dates=["timestamp_utc"])
beh_linked = beh[beh["participant_id_canonical"].isin(linked_ids)]
```

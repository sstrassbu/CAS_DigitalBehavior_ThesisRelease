# ds1_participant_linkage.csv

**Source dataset:** Dataset 1 — Compact friction intervention testing  
**Produced by:** `notebooks/02_dataset_1_cleaning.ipynb`  
**Rows:** 1,178  
**Columns:** 5  

---

## What this file contains

One row per unique participant across all three DS1 files (behavioral, pre-survey, post-survey). Each row records which files that participant appears in, using binary flags. This is the join key for any analysis that requires linking behavioral data with survey data.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Canonical participant UUID. Use as the join key when merging with behavioral or survey files. |
| `in_behavioral` | int (0/1) | 1 if this participant has at least one event in the cleaned behavioral file; 0 otherwise. |
| `in_pre_survey` | int (0/1) | 1 if this participant has a consenting row in the cleaned pre-survey file; 0 otherwise. |
| `in_post_survey` | int (0/1) | 1 if this participant has a consenting row in the cleaned post-survey file; 0 otherwise. |
| `n_files` | int | Total number of files (1–3) this participant appears in. |

---

## Participant overlap summary

| in_behavioral | in_pre_survey | in_post_survey | Count | Notes |
|---|---|---|---|---|
| 1 | 1 | 1 | **168** | **Fully linked — all three files.** Core sample for combined behavioral + psychosocial analysis. |
| 1 | 1 | 0 | 359 | Behavioral + pre-survey only. Can analyze behavioral outcomes with pre-survey moderators. No post-survey. |
| 1 | 0 | 1 | 50 | Behavioral + post-survey only. No pre-survey baseline. |
| 1 | 0 | 0 | 42 | Behavioral only. No survey data — behavioral analysis only. |
| 0 | 1 | 1 | 6 | Pre + post survey only. No behavioral data — survey-level analysis only. |
| 0 | 1 | 0 | 553 | Pre-survey only. Enrolled but never used the app (or events not logged). Exclude from all behavioral modeling. |
| **Total** | | | **1,178** | |

---

## How to use this file

**Filter to fully-linked participants:**
```python
import pandas as pd
link = pd.read_csv("outputs/cleaned/ds1_participant_linkage.csv")
fully_linked = link[link['n_files'] == 3]['participant_id_canonical'].tolist()
```

**Merge with behavioral file:**
```python
beh = pd.read_csv("outputs/cleaned/ds1_behavioral_clean.csv")
beh_linked = beh[beh['participant_id_canonical'].isin(fully_linked)]
```

---

## Critical notes

- **553 participants appear only in the pre-survey** with no behavioral data. These participants signed up (or clicked a link) but either never activated the app or their events were not logged. They must be excluded from all behavioral modeling — they are not a random subset.
- The linkage counts reflect the cleaned files (after deduplication and consent exclusion). Pre-survey lost 26 non-consenting rows; post-survey lost 1.
- The fully-linked count dropped from 169 (raw) to 168 (cleaned) because participant `<participant-id>` submitted `'I do NOT consent'` in the pre-survey and was therefore removed from `ds1_pre_survey_clean.csv`. Deduplication cannot cause this — `drop_duplicates(subset='participantUuid', keep='first')` always preserves at least one row per participant. Note that this participant's behavioural events and their two `'I consent'` post-survey rows are still present in the other cleaned files, because the consent filter is applied per survey file rather than as a participant-level blocklist — see the consent-handling note.

# ds1_post_survey_clean.csv

**Source dataset:** Dataset 1 — Compact friction intervention testing  
**Source file:** `data_raw/1. data set, compact friction intervention testing/Survey data sets/Post-survey/post_survey_data_set_1.csv`  
**Produced by:** `notebooks/02_dataset_1_cleaning.ipynb`  
**Rows:** 224  
**Columns:** 20  

---

## What this file contains

One row per participant who consented and completed (or partially completed) the post-intervention survey. The survey was administered after participants had used the OneSec friction app for a study period. It captures retrospective self-reports on whether goals were reached, whether problems were solved, changes in subjective time use, and well-being indicators. Together with `ds1_pre_survey_clean.csv`, this file supports pre/post comparison for the 168 fully-linked participants.

---

## Column reference

### Identity and metadata

| Column | Type | Description |
|---|---|---|
| `participantUuid` | string | Original participant UUID from source file. |
| `participant_id_canonical` | string | Canonical participant ID. Use for joining with behavioral data or the linkage table. |
| `duration` | int | Time in seconds the participant spent completing the survey. |
| `consent_general` | string | Consent field. All rows in this cleaned file have `'I consent'`. Non-consenting rows were excluded during cleaning. Note: this column is undocumented in the post-survey codebook but present in the CSV — treated as equivalent to the pre-survey consent field. |

### Raw survey responses (preserved as-is)

| Column | Type | Description |
|---|---|---|
| `problems_solved` | string | Likert composite string: whether the participant felt their problems were solved. Format: `"N - label"`. |
| `goals_reached` | string | Likert composite string: whether the participant felt their goals were reached. Format: `"N - label"`. |
| `hours` | string | Self-reported daily social media hours post-intervention. Mixed format. |
| `problematic_cons` | string | Likert composite string: self-rated problematic consumption at end of study. |
| `happy` | string | Likert composite string: happiness with social media consumption at end of study. |
| `progress_satisfaction` | string | Likert composite string: satisfaction with progress during the study. Note: the codebook description reads "Outcome of intervention" — this is a copy-paste error; the column is a satisfaction scale. |
| `problematic_cons_general` | string | Likert composite string: general opinion on problematic consumption. |
| `problematic_cons_compared` | string | Likert composite string: perceived consumption relative to others at end of study. |

### Derived numeric columns

Extracted from raw Likert composite strings using regex `r'^(\d+)'`. All are float64 to accommodate NaN.

| Column | Type | Scale | Description |
|---|---|---|---|
| `problems_solved_num` | float64 | 1–5 | Numeric extract from `problems_solved` (raw levels: 1 - not at all, 2 - a bit, 3 - partly, 4 - mostly, 5 - completely). The post-survey codebook PDF wrongly documents this item as a multi-select option list. |
| `goals_reached_num` | float64 | 1–5 | Numeric extract from `goals_reached` (raw levels: 1 - not at all, 2 - a bit, 3 - partly, 4 - mostly, 5 - completely). The post-survey codebook PDF wrongly documents this item as a multi-select option list. |
| `problematic_cons_num` | float64 | 1–7 | Numeric extract from `problematic_cons` |
| `happy_num` | float64 | 1–7 | Numeric extract from `happy` |
| `progress_satisfaction_num` | float64 | 1–7 | Numeric extract from `progress_satisfaction` |
| `problematic_cons_general_num` | float64 | 1–7 | Numeric extract from `problematic_cons_general` |
| `problematic_cons_compared_num` | float64 | 1–7 | Numeric extract from `problematic_cons_compared` |
| `hours_num` | float64 | hours/day | Numeric extract from `hours` |

---

## Cleaning steps applied

1. Reread source CSV with `sep=';'`
2. Deduplicated on `participantUuid` (kept first occurrence) — 30 duplicate rows removed
3. Excluded non-consenting rows (`consent_general == 'I do NOT consent'`) — 1 row removed
4. Extracted numeric prefix from all Likert composite string columns → `*_num` columns
5. Added `participant_id_canonical` column

Note: The post-survey has no multi-select fields — no binary indicator columns were needed.

---

## Pre/post pairing

To create a pre/post comparison dataset, join this file with `ds1_pre_survey_clean.csv` on `participant_id_canonical`. Restrict to participants present in both:

```python
import pandas as pd
pre = pd.read_csv("outputs/cleaned/ds1_pre_survey_clean.csv")
post = pd.read_csv("outputs/cleaned/ds1_post_survey_clean.csv")
pre_post = pre.merge(post, on="participant_id_canonical", suffixes=("_pre", "_post"))
# Result: only participants in both surveys (~168 if also requiring behavioral data)
```

---

## Known limitations

- Only 224 participants — heavy attrition from pre-survey (1,086 participants) to post-survey. Only ~20% of pre-survey participants completed the post-survey.
- ~15–20% missingness on most survey columns
- `consent_general` not documented in the post-survey codebook — treated as equivalent to the pre-survey field
- `progress_satisfaction` codebook description is a copy-paste error ("Outcome of intervention") — the column is a satisfaction scale

---

## How to load

```python
import pandas as pd
post = pd.read_csv("outputs/cleaned/ds1_post_survey_clean.csv")
```

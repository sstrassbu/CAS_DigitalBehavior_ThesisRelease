# ds1_pre_survey_clean.csv

**Source dataset:** Dataset 1 — Compact friction intervention testing  
**Source file:** `data_raw/1. data set, compact friction intervention testing/Survey data sets/Pre-survey/pre_survey_data_set_1.csv`  
**Produced by:** `notebooks/02_dataset_1_cleaning.ipynb`  
**Rows:** 1,086  
**Columns:** 26  

---

## What this file contains

One row per participant who consented and completed (or partially completed) the pre-intervention survey. The survey was administered before participants began using the OneSec friction app. It captures baseline self-reported smartphone use problems, goals for using the app, subjective time use, and well-being indicators.

---

## Column reference

### Identity and metadata

| Column | Type | Description |
|---|---|---|
| `participantUuid` | string | Original participant UUID from source file. |
| `participant_id_canonical` | string | Canonical participant ID. Use for joining with behavioral data or the linkage table. |
| `duration` | int | Time in seconds the participant spent completing the survey. |
| `consent_general` | string | Consent field. All rows in this cleaned file have `'I consent'`. Non-consenting rows were excluded during cleaning. |

### Raw survey responses (preserved as-is)

| Column | Type | Description |
|---|---|---|
| `problems` | string | Comma-concatenated multi-select: which smartphone use problems the participant wants to address (e.g. `"Excessive consumption,Feeling of no control"`). |
| `other_problems` | string | Free-text field for problems not listed. 96% NaN. |
| `goals` | string | Comma-concatenated multi-select: what goals the participant has for using the app (e.g. `"Less consumption,More awareness of consumption"`). |
| `other_goals` | string | Free-text field for goals not listed. 98% NaN. |
| `hours` | string | Self-reported daily social media hours. Mixed format (numeric and text). |
| `problematic_cons` | string | Likert composite string: self-rated problematic consumption. Format: `"N - label"`. |
| `happy` | string | Likert composite string: happiness with social media consumption. Format: `"N - label"`. |
| `problematic_cons_general` | string | Likert composite string: opinion on problematic consumption in general. Format: `"N - label"`. |
| `problematic_cons_compared` | string | Likert composite string: perceived consumption relative to others. Format: `"N - label"`. |

### Derived numeric columns

Extracted from raw Likert composite strings using regex `r'^(\d+)'`. Suffix `_num` indicates the numeric extraction. All are float64 to accommodate NaN.

| Column | Type | Scale | Description |
|---|---|---|---|
| `problematic_cons_num` | float64 | 1–7 | Numeric extract from `problematic_cons` |
| `happy_num` | float64 | 1–7 | Numeric extract from `happy` |
| `problematic_cons_general_num` | float64 | 1–7 | Numeric extract from `problematic_cons_general` |
| `problematic_cons_compared_num` | float64 | 1–7 | Numeric extract from `problematic_cons_compared` |
| `hours_num` | float64 | hours/day | Numeric extract from `hours` |

### Binary indicator columns from multi-select fields

Derived from `problems`. Each column is 1 (selected), 0 (not selected), or NaN (question was not answered).

| Column | Description |
|---|---|
| `problem_another_problem` | Selected "Another problem" |
| `problem_automatic_consumption` | Selected "Automatic consumption" |
| `problem_excessive_consumption` | Selected "Excessive consumption" |
| `problem_feeling_of_no_control` | Selected "Feeling of no control" |

Derived from `goals`. Same encoding (1/0/NaN).

| Column | Description |
|---|---|
| `goal_another_goal` | Selected "Another goal" |
| `goal_consuming_selectively` | Selected "Consuming selectively" |
| `goal_less_consumption` | Selected "Less consumption" |
| `goal_more_awareness_of_consumption` | Selected "More awareness of consumption" |

---

## Cleaning steps applied

1. Reread source CSV with `sep=';'`
2. Deduplicated on `participantUuid` (kept first occurrence) — 26 duplicate rows removed
3. Excluded non-consenting rows (`consent_general == 'I do NOT consent'`) — 26 rows removed
4. Extracted numeric prefix from all Likert composite string columns → `*_num` columns
5. Split `problems` and `goals` multi-select strings into binary indicator columns
6. Added `participant_id_canonical` column

---

## Known limitations

- ~37% missingness on all substantive survey columns — participants who started the survey but did not complete it
- `problems`, `goals`, `other_problems`, `other_goals` are qualitative/semi-structured; binary indicators cover only the pre-defined options
- `hours_num` extracted from a mixed-format text field — verify before using in quantitative models
- Baseline only — no post-period data in this file (see `ds1_post_survey_clean.csv`)

---

## How to load

```python
import pandas as pd
pre = pd.read_csv("outputs/cleaned/ds1_pre_survey_clean.csv")
```

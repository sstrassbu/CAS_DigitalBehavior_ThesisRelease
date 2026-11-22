# ds4_survey_clean.csv

**Source dataset:** Dataset 4 — Large non-experimental data (historic, retrospective use)
**Source file:** `data_raw/4. data set, large non-experimental data/Survey data set/post_survey_data_set_4.csv`
**Produced by:** `notebooks/04_dataset_4_cleaning.ipynb`
**Rows:** 299
**Columns:** 13

---

## What this file contains

One row per participant who completed the DS4 retrospective post-use survey. The survey was administered after participants had been using the OneSec friction app for an extended period. It captures qualitative self-reports on why they started using the app, what benefits and negatives they experienced, and how they use it. There are no psychometric scales — all substantive columns are open-text.

This file contains 299 unique participants. Of these, 283 can be linked to behavioral data via `participant_id_canonical`. 16 survey participants have no behavioral match.

---

## Column reference

### Original columns (preserved as-is, whitespace stripped)

| Column | Type | Description |
|---|---|---|
| `uuid` | string | Original survey UUID including prefix `donatus-master-thesis-one-sec-early-2023-`. Preserved for traceability. Use `participant_id_canonical` for joining. |
| `age` | float64 | Participant age in years. 20.4% NaN. Range 13–54; mean 26.4. |
| `gender` | string | Gender as original text string. 14.1% NaN. Codebook incorrectly documents as numeric codes — use `gender_clean`. |
| `gender_additional` | string | Open text for "Other:" gender specification. 98.4% NaN. |
| `reason_use` | string | Why the participant started using OneSec. 0% NaN. Open text; qualitative only. |
| `benefits` | string | Benefits experienced from using OneSec. 2.3% NaN. Open text; qualitative only. |
| `negatives` | string | Negatives or downsides experienced. 11.8% NaN. Open text; qualitative only. |
| `usage_format` | string | How the participant configures or uses the app. 14.5% NaN. Open text; qualitative only. |
| `add_features` | string | Feature requests. 29.9% NaN. Open text. |
| `comments` | string | General feedback. 53.0% NaN. Open text. |

### Derived columns (added during cleaning)

| Column | Type | Description |
|---|---|---|
| `uuid_stripped` | string | UUID with prefix removed, uppercased. Used to derive `participant_id_canonical`. |
| `participant_id_canonical` | string | Canonical participant ID matching the behavioral file. Use for all joins. |
| `gender_clean` | string | Recoded gender using text-based mapping: `male`, `female`, `non_binary`, `other`, `prefer_not_to_say`. NaN where original gender is NaN or unrecognized. |

---

## Cleaning steps applied

1. Stripped trailing whitespace from all text columns (CSV had trailing spaces; XLSX was pre-trimmed)
2. Deduplicated on `uuid` (keep first) — 5 duplicate rows removed (304 → 299)
3. Stripped survey UUID prefix `donatus-master-thesis-one-sec-early-2023-` → `uuid_stripped`
4. Added `participant_id_canonical` (uppercased stripped UUID, matching behavioral file)
5. Recoded `gender` to `gender_clean` using text-based mapping (codebook numeric codes are incorrect)

---

## Known limitations

- All substantive survey columns are open-text qualitative responses — no psychometric scales, no Likert items
- No pre-survey — this is post-use only; no pre/post comparison possible within DS4
- 20.4% NaN on `age`, 14.1% NaN on `gender`
- 16 survey participants cannot be matched to behavioral data
- 756 behavioral participants have no survey data at all
- Qualitative columns require NLP or manual coding for quantitative use

---

## How to load

```python
import pandas as pd

survey = pd.read_csv("outputs/cleaned/ds4_survey_clean.csv")

# Join with behavioral data
beh  = pd.read_csv("outputs/cleaned/ds4_behavioral_clean.csv",
                   parse_dates=["timestamp_utc"])
linked = beh.merge(survey, on="participant_id_canonical", how="inner")
# Result: events from the 283 participants present in both files
```

# Dataset 1 Overview

## Basic information

**Dataset name:** Dataset 1 — Compact friction intervention testing  
**Raw folder:** `data_raw/1. data set, compact friction intervention testing/`  
**Project description:** Compact default intervention study  
**Design summary:** compact field study testing the default friction intervention with both pre- and post-survey components.

## Visible structure

### Behavior data set
- `behavioral_data_set_1.csv`
- `behavioral_data_set_1.xlsx`
- `codebook_behavioral_data_set_1.pdf`

### Survey data sets
#### Post-survey
- `codebook_post_survey_data_set_1.pdf`
- `post_survey_data_set_1.csv`
- `post_survey_data_set_1.xlsx`

#### Pre-survey
- `codebook_pre_survey_data_set_1.pdf`
- `pre_survey_data_set_1.csv`
- `pre_survey_data_set_1.xlsx`

### Additional documentation
- `Project description, Compact default intervention study_.docx`

## Behavioral dataset

**File:** `behavioral_data_set_1.csv`  
**Rows:** 407060  
**Observed columns:**
- `participantUuid`
- `app`
- `timestamp`
- `purpose`
- `resolution`
- `secondsSinceOneSecSetup`

## Post-survey dataset

**File:** `post_survey_data_set_1.csv`  
**Rows:** 255  
**Observed columns:**
- `participantUuid`
- `duration`
- `consent_general`
- `problems_solved`
- `goals_reached`
- `hours`
- `problematic_cons`
- `happy`
- `progress_satisfaction`
- `problematic_cons_general`
- `problematic_cons_compared`

## Pre-survey dataset

**File:** `pre_survey_data_set_1.csv`  
**Rows:** 1135  
**Observed columns:**
- `participantUuid`
- `duration`
- `consent_general`
- `problems`
- `other_problems`
- `goals`
- `other_goals`
- `hours`
- `problematic_cons`
- `happy`
- `problematic_cons_general`
- `problematic_cons_compared`

## Audit status

**Audit complete.** Full report: `outputs/reports/ds1_audit_report.md`  
Inspection notebook: `notebooks/01_dataset_1_inspection.ipynb`  
Cleaning notebook: `notebooks/02_dataset_1_cleaning.ipynb`

---

## Confirmed file roles

| File | Confirmed role | Notes |
|---|---|---|
| `behavioral_data_set_1.csv` | Event-level behavioral data — primary substrate | 407,060 rows × 6 cols, sep=`;` |
| `behavioral_data_set_1.xlsx` | Identical copy — not needed | Confirmed identical shape and columns |
| `pre_survey_data_set_1.csv` | Pre-intervention survey | 1,135 rows × 12 cols, sep=`;` |
| `post_survey_data_set_1.csv` | Post-intervention survey | 255 rows × 11 cols, sep=`;` |
| xlsx survey versions | Identical copies — not needed | Confirmed identical |
| codebook PDFs | Variable documentation | Read before any recoding |
| project description docx | Study design context | Important for interpretation |

**Delimiter confirmed: semicolon (`;`) in all three CSVs.**

---

## Confirmed unit of observation

### Behavioral file
One intervention event per row. Primary key: `participantUuid` × `timestamp` (not strictly unique — 8,302 fully duplicate rows exist in the raw file).

### Survey files
One survey response per participant per wave. 26 duplicate participantUuid rows in pre-survey; 30 in post-survey.

---

## Confirmed data quality findings

| Issue | Severity | Cleaning action |
|---|---|---|
| All CSVs semicolon-delimited (not comma) | Low | Always use `sep=';'` |
| `timestamp` is Unix epoch int64 (codebook claims datetime string) | Medium | `pd.to_datetime(unit='s', utc=True)` |
| 8,302 fully duplicate rows in behavioral | Medium | Drop exact duplicates (`keep='first'`) |
| 1 NaN `participantUuid` row in behavioral | Low | Drop row |
| 468 NaN `resolution` rows | Low | Flag as `missing` in `event_outcome_simple` |
| `purpose`: 71.3% NaN | High | Use as qualitative supplement only |
| `secondsSinceOneSecSetup`: 18.9% NaN | Medium | Exclude from longitudinal analysis |
| `whastapp` typo in app names | Low | Correct in canonical `app_name` column |
| Likert scales stored as composite strings ('N - label') | Medium | Extract int prefix with regex |
| Multi-select fields comma-concatenated | Medium | Split to binary indicator columns |
| 26 duplicate participantUuid in pre-survey | Medium | Dedup: keep first row |
| 30 duplicate participantUuid in post-survey | Medium | Dedup: keep first row |
| 26 non-consenting in pre-survey | Medium | Exclude from all analysis |
| 1 non-consenting in post-survey | Low | Exclude |

---

## Confirmed codebook discrepancies

| Discrepancy | Severity |
|---|---|
| Column `secondsSinceStudySetup` in codebook → actual CSV name is `secondsSinceOneSecSetup` | Low |
| Timestamp described as 'year-month-day hour:minute:second' → actual format is Unix epoch int64 | Medium |
| `other_goals` description reads 'Outcome of intervention' — copy-paste error in codebook | Low |
| `progress_satisfaction` description reads 'Outcome of intervention' — copy-paste error in codebook | Low |
| `consent_general` present in post-survey CSV but not documented in post-survey codebook | Medium |

---

## Confirmed resolution values

| Value | Count | Proportion |
|---|---|---|
| `openedApp` | 203,295 | 49.9% |
| `dismissedAppOpening` | 105,074 | 25.8% |
| `closedApp` | 98,223 | 24.1% |
| NaN | 468 | 0.1% |

---

## Confirmed participant structure

| Group | N |
|---|---|
| Behavioral file | 619 |
| Pre-survey | 1,109 (after dedup) |
| Post-survey | 225 (after dedup) |
| **All three files** | **169** |
| Behavioral + pre only | 359 |
| Behavioral only | 41 |
| Pre only (no behavioral data) | 575 |

**Critical:** 575 participants completed the pre-survey but have no behavioral data. They must be excluded from all behavioral modeling.

---

## Confirmed strengths

- clean behavioral core with direct intervention outcome variable
- clear pre/post survey structure
- shared `participantUuid` across all files (confirmed consistent)
- `secondsSinceOneSecSetup` provides a longitudinal adaptation proxy
- 48 unique apps (Instagram dominant at 41%)

## Confirmed limitations

- `purpose`: 71.3% missing — not viable as a systematic feature
- no explicit experimental condition variable (DS1 is a single-arm study)
- only 169 participants in all three files — small fully-linked sample
- psychological constructs less rich than DS5 and DS6
- no timezone column — UTC assumed for all timestamps
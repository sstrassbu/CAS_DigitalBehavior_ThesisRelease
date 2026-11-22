# Dataset 4 Overview

## Basic information

**Dataset name:** Dataset 4 — Large non-experimental data  
**Raw folder:** `data_raw/4. data set, large non-experimental data/`  
**Project description:** Historic, retrospective use data from existing users  
**Design summary:** Longitudinal OneSec use data from existing users. Observation range: 2020-09-30 to 2023-04-02. Median participant study duration: 66 days. Max: 897 days (~2.5 years). Non-experimental (no intervention arms).

## Audit status

**Audit complete.** Full report: `outputs/reports/ds4_audit_report.md`  
Inspection notebook: `notebooks/03_dataset_4_inspection.ipynb`  
Cleaning notebook: `notebooks/04_dataset_4_cleaning.ipynb`

---

## Visible structure

### Behavior data set
- `behavior_data_set_4.csv`
- `codebook_behavior_data_set.pdf`

### Survey data set
- `post_survey_data_set_4.csv`
- `post_survey_data_set_4.xlsx`
- `codebook_post_survey_data_set.docx`
- `codebook_post_survey_data_set.pdf`

### Additional documentation
- `Project description, Historic, retrospective use data from existing users.docx`

---

## Behavioral dataset

**File:** `behavior_data_set_4.csv`  
**Rows:** 2,490,260  
**Columns:** 10  
**Delimiter:** comma (`,`) — different from DS1 surveys

**Observed columns:**
- `app`
- `resolution`
- `timestamp`
- `interventionDuration`
- `interventionType`
- `purpose`
- `participantUuid`
- `secondsSinceStudySetup`
- `weeksSinceStudySetup`
- `userIndex`

---

## Survey dataset

**File:** `post_survey_data_set_4.csv`  
**Rows:** 304  
**Columns:** 10  
**Delimiter:** semicolon (`;`) — different from behavioral file

**Observed columns:**
- `uuid`
- `age`
- `gender`
- `gender_additional`
- `reason_use`
- `benefits`
- `negatives`
- `usage_format`
- `add_features`
- `comments`

---

## Confirmed file roles

| File | Confirmed role | Notes |
|---|---|---|
| `behavior_data_set_4.csv` | Event-level behavioral data — primary substrate | 2,490,260 rows × 10 cols, sep=`,` |
| `post_survey_data_set_4.csv` | Post-use retrospective survey | 304 rows × 10 cols, sep=`;` |
| `post_survey_data_set_4.xlsx` | Near-duplicate of survey CSV | Same shape; CSV has trailing whitespace; XLSX is pre-trimmed |
| `codebook_behavior_data_set.pdf` | Variable documentation for behavioral file | Contains discrepancies — see below |
| `codebook_post_survey_data_set.pdf/docx` | Variable documentation for survey | Gender coding in codebook is incorrect |
| Project description docx | Study design context | Non-experimental; important for `closedApp` interpretation |

---

## Confirmed unit of observation

### Behavioral file
One intervention event per row. Primary key: `participantUuid` × `timestamp`. No fully duplicate rows confirmed.

### Survey file
One retrospective survey response per participant. 5 duplicate `uuid` rows exist (dedup: keep first).

---

## Confirmed data quality findings

| Issue | Severity | Cleaning action |
|---|---|---|
| Behavioral comma-delimited; survey semicolon-delimited | Medium | Always specify `sep=','` for behavioral, `sep=';'` for survey |
| `timestamp` is ISO 8601 UTC string (not Unix epoch) | Medium | `pd.to_datetime(utc=True)` — zero parse failures confirmed |
| `secondsSinceStudySetup` / `weeksSinceStudySetup`: all ≤ 0 — codebook description incorrect | High | Do not use as "time since setup"; reconstruct from `timestamp`; see confirmed interpretation below |
| 2 undocumented `resolution` values | Medium | `dismissedByStructuredIntervention` (806), `dismissedWithHealthyAlternative` (6) — verify meaning before mapping |
| `interventionDuration` + `interventionType`: 63.5% NaN, perfectly aligned | High | All `closedApp` events have NaN intervention fields; these may be a different event type — classify separately |
| `purpose`: 83.1% NaN | High | Open-text; too sparse for systematic use |
| Survey `uuid` has `donatus-master-thesis-one-sec-early-2023-` prefix | High | Strip prefix before ID matching; confirmed 283/299 match behavioral |
| Gender stored as text strings, not numeric codes as codebook implies | Medium | Use text-based recoding |
| 5 duplicate `uuid` rows in survey | Low | Keep first occurrence |
| Survey CSV has trailing whitespace in text fields | Low | `.str.strip()` during cleaning, or use XLSX |
| `whastapp` typo in `app` column | Low | Correct to `whatsapp` in canonical `app_name` |
| 16 survey participants with no behavioral match | Medium | Exclude from linked analysis; keep in survey-level analysis |
| 756 behavioral participants with no survey | Medium | Behavioral analysis available; no psychosocial variables |
| No NaN in `app`, `resolution`, `timestamp`, `participantUuid`, `userIndex` | (positive) | No missing identifiers |
| No fully duplicate rows in behavioral | (positive) | No deduplication needed |

---

## Confirmed codebook discrepancies

| Discrepancy | Severity |
|---|---|
| `resolution`: codebook lists 3 values; data has 5 | Medium |
| `secondsSinceStudySetup`/`weeksSinceStudySetup`: codebook says positive forward-counting; all data values are negative | High |
| `gender`: codebook uses numeric codes 1–5; actual data stores text strings | Medium |
| Survey `uuid` prefix not documented | Medium |

---

## Confirmed resolution values

| Value | Count | Share |
|---|---|---|
| `closedApp` | 1,171,929 | 47.1% |
| `openedApp` | 881,409 | 35.4% |
| `dismissedAppOpening` | 436,110 | 17.5% |
| `dismissedByStructuredIntervention` | 806 | 0.03% |
| `dismissedWithHealthyAlternative` | 6 | 0.0% |
| NaN | 0 | 0.0% |

---

## Confirmed intervention type values

| interventionType | Count | Share of non-NaN rows |
|---|---|---|
| `breathingExercise` | 552,424 | 60.7% |
| `minimalBreathingExercise` | 135,358 | 14.9% |
| `followTheDot` | 131,438 | 14.4% |
| `blackScreen` | 54,105 | 5.9% |
| `mirror` | 36,613 | 4.0% |
| `rotatePhone` | 10 | 0.0% |
| NaN | 1,580,312 | — |

---

## Confirmed participant structure

| Group | N |
|---|---|
| Behavioral file | 1,039 |
| Survey file (after dedup) | 299 |
| Behavioral + survey (linked) | 283 |
| Survey only (no behavioral) | 16 |
| Behavioral only (no survey) | 756 |

**Note:** The survey `uuid` has a study prefix. After stripping the prefix and uppercasing, 283 of 299 survey participants match behavioral participants.

---

## Confirmed secondsSinceStudySetup interpretation

`secondsSinceStudySetup` and `weeksSinceStudySetup` are **negative for all rows**. Investigation confirms:
- Within each participant, `timestamp_epoch − secondsSinceStudySetup` is a near-constant (per-participant anchor)
- The anchor is approximately 8.8 hours after each participant's last event — likely an export or enrollment-end timestamp
- The variable is **not** a forward-counting elapsed time from app setup as the codebook claims
- **Still usable for**: relative ordering within a participant (more negative = earlier); temporal range of observation per participant
- **Workaround**: derive `days_since_first_event` from `timestamp` directly using `event_time − participant_first_event_time`

---

## Confirmed strengths

- Largest behavioral dataset: 2,490,260 events across 1,039 participants
- No NaN in core columns; no duplicate rows
- Explicit intervention type and duration fields (for 36.5% of events)
- Long observation windows: median 66 days, max 897 days
- Strong candidate for longitudinal adaptation and heterogeneity analysis
- 399 unique apps (vs 48 in DS1) — broad naturalistic coverage

## Confirmed limitations

- `purpose`: 83.1% NaN — not viable for systematic feature use
- Non-experimental design — no condition variable, no control group
- Survey entirely qualitative/retrospective — no psychometric scales
- `secondsSinceStudySetup`/`weeksSinceStudySetup` semantics are inverted relative to codebook
- Only 283 participants linked to both behavioral and survey data
- `interventionDuration`/`interventionType` only available for 36.5% of events (absent from all `closedApp` events)

# Dataset 1 Audit Report — Compact Friction Intervention Testing

**Date:** 2026-04-15  
**Status:** Pre-cleaning audit. No transformations applied.  
**Raw folder:** `data_raw/1. data set, compact friction intervention testing/`

---

## 1. File Inventory

| File | Role | Format | Rows | Columns |
|---|---|---|---|---|
| `Behavior data set/behavioral_data_set_1.csv` | Event-level behavioral data | CSV, semicolon-delimited | 407,060 | 6 |
| `Behavior data set/behavioral_data_set_1.xlsx` | Identical copy of above | XLSX | 407,060 | 6 |
| `Behavior data set/codebook_behavioral_data_set_1.pdf` | Variable documentation for behavioral file | PDF | — | — |
| `Survey data sets/Pre-survey/pre_survey_data_set_1.csv` | Pre-intervention survey | CSV, semicolon-delimited | 1,135 | 12 |
| `Survey data sets/Pre-survey/pre_survey_data_set_1.xlsx` | Identical copy of above | XLSX | 1,135 | 12 |
| `Survey data sets/Pre-survey/codebook_pre_survey_data_set_1.pdf` | Variable documentation for pre-survey | PDF | — | — |
| `Survey data sets/Post-survey/post_survey_data_set_1.csv` | Post-intervention survey | CSV, semicolon-delimited | 255 | 11 |
| `Survey data sets/Post-survey/post_survey_data_set_1.xlsx` | Identical copy of above | XLSX | 255 | 11 |
| `Survey data sets/Post-survey/codebook_post_survey_data_set_1.pdf` | Variable documentation for post-survey | PDF | — | — |
| `Project description, Compact default intervention study_.docx` | Study design description | DOCX | — | — |
| `README.md` | Folder-level notes | MD | — | — |

**CSV/XLSX verdict:** All three CSV/XLSX pairs have identical shapes and column names. Only CSV files need to be used; XLSX files can be ignored.

---

## 2. Unit of Observation

| File | Unit | Primary key |
|---|---|---|
| Behavioral | One intervention event per row | `participantUuid` × `timestamp` (not strictly unique due to duplicates — see §6) |
| Pre-survey | One survey response per participant | `participantUuid` |
| Post-survey | One survey response per participant | `participantUuid` |

---

## 3. Confirmed Variables

### 3.1 Behavioral file

| Column | Type | Description | Notes |
|---|---|---|---|
| `participantUuid` | string (UUID) | Participant identifier | 1 NaN row present |
| `app` | string | Name of intervened app | 48 unique apps; Instagram dominant |
| `timestamp` | int64 (unix seconds) | Time of intervention | Confirmed unix epoch, e.g. 1620341675 |
| `purpose` | string (free text) | User-entered open comment | 71.3% NaN — very sparse |
| `resolution` | string (categorical) | Outcome of intervention | 3 documented values (see §5); 468 NaN |
| `secondsSinceOneSecSetup` | float64 | Seconds since user set up the OneSec app | 18.9% NaN; range 76–5,589,325 sec |

### 3.2 Pre-survey file

| Column | Type | Description | Notes |
|---|---|---|---|
| `participantUuid` | string (UUID) | Participant identifier | No NaN |
| `duration` | int | Survey completion time in seconds | No NaN |
| `consent_general` | string | Study consent | 3 values: "I consent" (824), NaN (285), "I do NOT consent" (26) |
| `problems` | string (multi-select) | Problems user wants to address | Comma-concatenated multi-select; 37% NaN |
| `other_problems` | string (free text) | Other problems (open) | 96% NaN |
| `goals` | string (multi-select) | Goals with the app | Comma-concatenated multi-select; 38% NaN |
| `other_goals` | string (free text) | Other goals (open) | 98% NaN |
| `hours` | string/numeric (mixed) | Self-reported daily social media hours | 37% NaN |
| `problematic_cons` | string | Self-rated problematic consumption | Stored as "N - label" string; 37% NaN |
| `happy` | string | Happiness with social media consumption | Stored as "N - label" string; 37% NaN |
| `problematic_cons_general` | string | General problematic consumption opinion | Stored as "N - label" string; 37% NaN |
| `problematic_cons_compared` | string | Consumption relative to others | Stored as "N - label" string; 37% NaN |

### 3.3 Post-survey file

| Column | Type | Description | Notes |
|---|---|---|---|
| `participantUuid` | string (UUID) | Participant identifier | No NaN |
| `duration` | int | Survey completion time in seconds | No NaN |
| `consent_general` | string | Study consent | Not documented in codebook — see §7 |
| `problems_solved` | string | Whether problems were solved | Stored as "N - label" string; 16% NaN |
| `goals_reached` | string | Whether goals were reached | Stored as "N - label" string; 16% NaN |
| `hours` | string/numeric | Self-reported daily social media hours | 20% NaN |
| `problematic_cons` | string | Self-rated problematic consumption | Stored as "N - label" string; 17% NaN |
| `happy` | string | Happiness with social media consumption | Stored as "N - label" string; 16% NaN |
| `progress_satisfaction` | string | Satisfaction with progress | Stored as "N - label" string; 15% NaN |
| `problematic_cons_general` | string | General problematic consumption opinion | Stored as "N - label" string; 16% NaN |
| `problematic_cons_compared` | string | Consumption relative to others | Stored as "N - label" string; 15% NaN |

---

## 4. Timestamp Format

- **Format confirmed:** Unix epoch, integer, seconds precision.
- **Example:** `1620341675` → 2021-05-06 (UTC)
- **Conversion required:** `pd.to_datetime(df['timestamp'], unit='s', utc=True)`
- **No timezone column** in DS1 behavioral file — all timestamps assumed UTC or device-local (not specified in codebook). Flag as ambiguity until study description is checked.

---

## 5. Resolution Values

**Confirmed unique values:**

| Value | Count | Proportion |
|---|---|---|
| `openedApp` | 203,295 | 49.9% |
| `dismissedAppOpening` | 105,074 | 25.8% |
| `closedApp` | 98,223 | 24.1% |
| NaN | 468 | 0.1% |

**Interpretation (INFERRED — not documented in the codebook):**

The behavioural codebook PDF gives only `resolution | Outcome of intervention | openedApp; dismissedAppOpening; closedApp`. It contains no per-value definitions, so everything below is inference, not documentation.
- `openedApp` — user proceeded to open the app despite intervention (inferred; consistent with the data)
- `dismissedAppOpening` — user dismissed the intervention and did not open (inferred; consistent with the data)
- `closedApp` — **an app-CLOSE record that terminates a session already started by an `openedApp`, not a third decision at the friction moment.** Empirically verified: among the 126 participants for whom `closedApp` is logged at all, 70.3% of their `openedApp` events are immediately followed (within participant × app) by a `closedApp`, a median 100 s later. The value is logged for only 126 of 619 participants (and only for some of their apps), i.e. it reflects per-participant/per-app logging configuration. Do not pool it into an outcome-rate denominator.

**NaN resolution rows:** 468 rows where `resolution` is missing. Spot-check shows these rows have `purpose` values present and valid `app`/`timestamp` — they are not truncated records. Cause unknown; likely a logging failure for specific event types.

**Simple harmonized mapping (proposed, not yet applied):**
- `openedApp` → `opened`
- `dismissedAppOpening` → `dismissed`
- `closedApp` → `closed`
- NaN → `missing`

---

## 6. Data Quality Issues

### 6.1 Fully duplicate rows
**8,302 fully duplicate rows** found (all 6 columns identical). This is ~2% of the behavioral file. Cause is unknown — could be double-logging, repeated export artifacts, or genuine same-event records (same participant, same app, same second, same purpose, same resolution). Decision required before cleaning: drop all duplicates or investigate triggers.

### 6.2 NaN participantUuid (1 row)
One row has NaN participantUuid, also has NaN resolution. Row index 160,582. The `purpose` field contains "ok this is a good question :)" — suggests a real user event that was logged without a valid session ID. Should be dropped in cleaning.

### 6.3 purpose missingness
71.3% of `purpose` values are NaN. This field is an open-format comment — users are not required to fill it in. The remaining 28.7% (116,874 rows) contain free-text values. Useful for qualitative context but unreliable as a systematic moderator unless carefully filtered.

### 6.4 secondsSinceOneSecSetup missingness
18.9% NaN (77,057 rows). Likely represents events where the study time counter was not yet initialized or the field was not logged in early versions of the data pipeline. These rows may still be usable for `resolution` analysis but cannot be used for longitudinal adaptation analysis without imputation or exclusion.

### 6.5 Scale items stored as composite strings
All Likert-scale variables in both surveys are stored as composite strings such as `"5 - tendentially problematic"` rather than integers. The numeric prefix must be extracted before any quantitative use. Regex pattern: extract leading integer from string.

### 6.6 Multi-select fields stored as comma-concatenated strings
`problems`, `goals`, `problems_solved`, `goals_reached` are stored as comma-separated concatenations of selected option labels (e.g., `"Excessive consumption,Feeling of no control,Automatic consumption"`). These need to be split into binary indicator columns before use.

### 6.7 Duplicate survey rows
- Pre-survey: 1,135 rows, 1,109 unique participants → **26 duplicate participantUuid values**
- Post-survey: 255 rows, 225 unique participants → **30 duplicate participantUuid values**

Cause unknown. Could be re-submissions, data pipeline artifacts, or retaken surveys. Requires manual inspection or a rule (e.g., keep last submission by `duration` or row order).

---

## 7. Participant Structure and Attrition

**Participant counts by file:**

| File | Unique participant IDs |
|---|---|
| Behavioral | 619 |
| Pre-survey | 1,109 |
| Post-survey | 225 |

**Participant overlap:**

| Category | Count |
|---|---|
| All three files | 169 |
| Behavioral + pre only | 359 |
| Behavioral + post only | 50 |
| Pre only (no behavioral, no post) | 575 |
| Behavioral only (no surveys) | 41 |
| Pre + post only (no behavioral) | 6 |

**Key observations:**
- Only **169 participants** (27% of behavioral, 15% of pre-survey) are present in all three files. This is the fully analyzable core sample for combined behavioral + psychosocial analysis.
- **575 participants** completed the pre-survey but have no behavioral data. These may have signed up but never used the app actively, or their data was not logged. They cannot be included in behavioral modeling.
- **41 participants** appear in the behavioral file but have no pre-survey. Their intervention response can be analyzed but without psychosocial moderators.
- Heavy attrition between pre-survey (1,109) and post-survey (225) — only ~20% of pre-survey participants completed the post-survey.

**For modeling purposes:** The behavioral-only sample (619 participants, 407,060 events) is the primary substrate for behavioral modeling. Psychosocial moderation requires restricting to the 169-participant fully-linked subset.

---

## 8. App Distribution

48 unique apps. Top 5 by event count:

| App | Events | Share |
|---|---|---|
| instagram | 166,962 | 41.0% |
| twitter | 62,355 | 15.3% |
| whastapp | 36,385 | 8.9% |
| facebook | 28,954 | 7.1% |
| tikTok | 13,095 | 3.2% |

**Note:** `whastapp` appears to be a typo in the raw data (should be `whatsapp`). This should be corrected in the canonical `app_name` column during cleaning.

---

## 9. Codebook Discrepancies

| File | Discrepancy | Severity |
|---|---|---|
| Behavioral codebook | Lists column as `secondsSinceStudySetup`; actual column name in CSV is `secondsSinceOneSecSetup` | Low — codebook error, actual data is correct |
| Pre-survey codebook | `other_goals` description reads "Outcome of intervention" — apparent copy-paste error | Low — description only, variable itself is clear |
| Post-survey codebook | `progress_satisfaction` description reads "Outcome of intervention" — apparent copy-paste error | Low — description only, variable itself is clear |
| Post-survey codebook | `consent_general` is present in the CSV but not documented in the codebook | Medium — undocumented column; values match pre-survey pattern (`I consent` / `I do NOT consent`) |
| Pre-survey codebook | `problematic_cons_compared` is listed as `Problematic cons_compared` (mixed case, space) | Low — naming inconsistency in codebook only |

**Additional provenance discrepancies:**

- The DS1 behavioural codebook and the DS1 pre-survey codebook are both titled `Codebook, behavioral data set (project_ time budget)` — i.e. they carry DS2's project name. Unresolved: whether the DS1 folder shipped the wrong codebook or the title is a copy-paste error.
- The codebook names the time column `secondsSinceStudySetup` and defines it as "distance (in seconds) to when the study was started by the user". This repo renames it `secondsSinceOneSecSetup` and interprets it as seconds since OneSec app setup. "Study start" vs "OneSec setup" is an open semantic question, not a settled naming fix.

---

## 10. Preprocessing Risks

| Risk | Severity | Action required |
|---|---|---|
| Semicolon delimiter — easy to mis-read as comma-separated | Low | Document in loader; always specify `sep=';'` |
| Unix timestamp — needs conversion to datetime | Low | Use `pd.to_datetime(unit='s')` with UTC flag |
| Timezone ambiguity — no timezone column | Medium | Check project description for timezone info; flag as UTC-assumed |
| 8,302 fully duplicate rows | Medium | Investigate before dropping; apply deduplication rule |
| 468 NaN resolution rows | Low | Flag as `missing`; retain for event counts, exclude from outcome analysis |
| 77,057 NaN `secondsSinceOneSecSetup` | Medium | Exclude from longitudinal/adaptation analysis; retain for cross-sectional event analysis |
| 71.3% NaN `purpose` | High | Only use as qualitative/optional feature; never treat as representative sample |
| Scale items as composite strings | Medium | Extract numeric prefix via regex before any quantitative use |
| Multi-select fields as concatenated strings | Medium | Split into binary indicator columns before use |
| Duplicate survey rows (pre: 26, post: 30) | Medium | Define deduplication rule before merging |
| 575 pre-survey participants with no behavioral data | High | Exclude from behavioral modeling; document as enrollment-without-use |
| `whastapp` typo in app names | Low | Correct in canonical `app_name` column |
| 1 NaN participantUuid row | Low | Drop in cleaning |
| `consent_general` undocumented in post-survey codebook | Medium | Treat as equivalent to pre-survey consent field; apply same exclusion logic |

---

## 11. Relevance for Later Modeling

| Construct | Availability | Notes |
|---|---|---|
| Intervention outcome (friction response) | Direct | `resolution` — 3 clean values |
| Temporal structure | Direct | `timestamp` (unix) — convert to datetime |
| App identity | Direct | `app` — 48 apps; typo in `whastapp` |
| Longitudinal adaptation | Partial | `secondsSinceOneSecSetup` — 18.9% missing; range ~76 sec to ~64.7 days |
| Behavioral context / motivation | Sparse | `purpose` — 71.3% missing; not reliable as a systematic moderator |
| Problematic use (pre/post) | Direct (survey) | 7-point Likert; stored as composite strings |
| Self-control / goals | Direct (survey) | Stored as composite strings and multi-select |
| Happiness / well-being | Direct (survey) | 7-point Likert; stored as composite strings |
| App transition / substitution | Derived | Must be inferred from time-ordered `app` sequences; no pre-computed fields |
| Habit strength | Derived | Repeated same-app use over time; feasible with `participantUuid` × `app` × `timestamp` |
| Friction sensitivity | Derived | Changes in `resolution` distribution over `secondsSinceOneSecSetup` |

**Best use of DS1:** Cross-sectional and longitudinal intervention-response analysis at the event level. First pipeline test due to simple structure. Psychosocial moderation limited to the 169-participant fully-linked subset.

---

## 12. Recommended Cleaning Steps (not yet applied)

1. Re-read all three CSVs with `sep=';'`
2. Convert `timestamp` to UTC datetime
3. Drop the 1 NaN-`participantUuid` row
4. Investigate and deduplicate the 8,302 fully duplicate rows
5. Deduplicate survey rows (define rule: keep first or last by row order)
6. Exclude non-consenting participants (`consent_general == 'I do NOT consent'`)
7. Extract numeric prefix from Likert-scale string columns
8. Split multi-select fields into binary indicator columns
9. Flag 468 NaN `resolution` rows as `missing`; retain for counts, exclude from outcome models
10. Correct `whastapp` → `whatsapp` in `app_name` canonical column
11. Create `participant_id_canonical` column (copy of `participantUuid`)
12. Create `event_outcome_simple` column mapping `resolution` to `opened` / `dismissed` / `closed` / `missing`

---

*This report was produced during the pre-cleaning audit phase. No transformations have been applied to raw files.*

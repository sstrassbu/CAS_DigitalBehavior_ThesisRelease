# Dataset 4 Audit Report — Large Non-Experimental Data

**Date:** 2026-04-15  
**Status:** Pre-cleaning audit. No transformations applied.  
**Raw folder:** `data_raw/4. data set, large non-experimental data/`

---

## 1. File Inventory

| File | Role | Format | Rows | Columns |
|---|---|---|---|---|
| `Behavior data set/behavior_data_set_4.csv` | Event-level behavioral data | CSV, comma-delimited | 2,490,260 | 10 |
| `Behavior data set/codebook_behavior_data_set.pdf` | Variable documentation for behavioral file | PDF | — | — |
| `Survey data set/post_survey_data_set_4.csv` | Post-use retrospective survey | CSV, semicolon-delimited | 304 | 10 |
| `Survey data set/post_survey_data_set_4.xlsx` | Near-duplicate of survey CSV | XLSX | 304 | 10 |
| `Survey data set/codebook_post_survey_data_set.pdf` | Variable documentation for survey | PDF | — | — |
| `Survey data set/codebook_post_survey_data_set.docx` | Same codebook in DOCX format | DOCX | — | — |
| `Project description, Historic, retrospective use data from existing users.docx` | Study design context | DOCX | — | — |
| `README.md` | Folder-level notes | MD | — | — |

**Delimiter split:** Behavioral CSV uses **comma** (`,`); survey CSV uses **semicolon** (`;`). This is the opposite of DS1's all-semicolon convention. Handle with care in any shared loading code.

**CSV vs XLSX (survey):** Same row count and column structure. The CSV has trailing whitespace in all text fields; the XLSX is pre-trimmed. Functionally equivalent after `.str.strip()` on CSV. Either can be used.

---

## 2. Unit of Observation

| File | Unit | Primary key |
|---|---|---|
| Behavioral | One intervention event per row | `participantUuid` × `timestamp` |
| Survey | One retrospective survey response per participant | `uuid` (with prefix — see §7) |

---

## 3. Confirmed Variables

### 3.1 Behavioral file

| Column | Type | Description | Notes |
|---|---|---|---|
| `app` | string | Name of intervened app | 399 unique apps; `whastapp` typo present (39,045 events) |
| `resolution` | string | Outcome of intervention | **5 values confirmed** — codebook only documents 3 (see §5) |
| `timestamp` | string (ISO 8601) | Time of intervention, UTC | Format: `2022-09-29T15:48:54Z`; parse with `pd.to_datetime(utc=True)` |
| `interventionDuration` | float64 | Duration of intervention in seconds | 63.5% NaN; range 3–560 sec; mean ~7.8 sec; median 6 sec |
| `interventionType` | string | Type of friction intervention | 63.5% NaN; 6 confirmed types (see §5) |
| `purpose` | string | Open-text comment for app-use reason | 83.1% NaN |
| `participantUuid` | string (UUID) | Participant identifier | No NaN; 1,039 unique participants |
| `secondsSinceStudySetup` | float64 | Time relative to study anchor (see §6) | **All values ≤ 0** — codebook description is misleading; see §6 |
| `weeksSinceStudySetup` | float64 | Same as above in weeks | **All values ≤ 0** — same issue as `secondsSinceStudySetup` |
| `userIndex` | int64 | Integer participant index | 0–1038; 1:1 with `participantUuid`; no NaN |

### 3.2 Survey file

| Column | Type | Description | Notes |
|---|---|---|---|
| `uuid` | string | Participant identifier with prefix | Format: `donatus-master-thesis-one-sec-early-2023-{UUID}` — must strip prefix to match behavioral (see §7) |
| `age` | float64 | Participant age in years | 20.4% NaN; range 13–54; mean 26.4 |
| `gender` | string | Gender (text, not numeric codes) | 14.1% NaN; codebook incorrectly documents as numeric 1–5 scale |
| `gender_additional` | string | Open text for "Other:" gender | 98.4% NaN |
| `reason_use` | string | Why the participant started using OneSec | 0% NaN |
| `benefits` | string | Benefits experienced | 2.3% NaN |
| `negatives` | string | Negatives experienced | 11.8% NaN |
| `usage_format` | string | How the participant uses the app | 14.5% NaN |
| `add_features` | string | Requested features | 29.9% NaN |
| `comments` | string | General feedback | 53.0% NaN |

---

## 4. Timestamp Format

- **Format confirmed:** ISO 8601 UTC string — e.g. `2022-09-29T15:48:54Z`
- **Parse with:** `pd.to_datetime(df['timestamp'], utc=True)` — zero parse failures confirmed
- **Range:** 2020-09-30 to 2023-04-02 (~2.5 years)
- **Note:** Different from DS1 (Unix epoch int64). Do not reuse DS1's `pd.to_datetime(unit='s')` call.

---

## 5. Resolution Values and Intervention Types

### Resolution

**Confirmed unique values:**

| Value | Count | Share | Codebook documented? |
|---|---|---|---|
| `closedApp` | 1,171,929 | 47.1% | Yes |
| `openedApp` | 881,409 | 35.4% | Yes |
| `dismissedAppOpening` | 436,110 | 17.5% | Yes |
| `dismissedByStructuredIntervention` | 806 | 0.03% | **No** |
| `dismissedWithHealthyAlternative` | 6 | 0.0% | **No** |
| NaN | 0 | 0.0% | — |

**Two undocumented resolution values** are present. `dismissedByStructuredIntervention` (806 cases) and `dismissedWithHealthyAlternative` (6 cases) are not listed in the codebook. They appear to be distinct dismissal mechanisms — confirm meaning with project description or codebook errata before mapping.

**Key difference from DS1:** `closedApp` is the dominant outcome in DS4 (47%), vs 24% in DS1. `openedApp` is 35% here vs 50% in DS1.

### Intervention types (non-NaN rows only)

| interventionType | Count |
|---|---|
| `breathingExercise` | 552,424 |
| `minimalBreathingExercise` | 135,358 |
| `followTheDot` | 131,438 |
| `blackScreen` | 54,105 |
| `mirror` | 36,613 |
| `rotatePhone` | 10 |

### Critical: interventionDuration/Type NaN alignment

`interventionDuration` and `interventionType` are **always NaN together** (perfect alignment — 1,580,312 rows both NaN; 909,948 rows both non-NaN). There are no rows where one is NaN and the other is not.

**What the NaN rows contain:**
- All 1,171,929 `closedApp` events have NaN intervention fields
- Some `openedApp` (278,330) and `dismissedAppOpening` (129,241) also have NaN intervention fields

**Non-NaN rows contain only:**
- `openedApp` (603,079) and `dismissedAppOpening` (306,869)

**Interpretation (requires confirmation):** `closedApp` events may represent app sessions where the user opened the app and later closed it — a different logging path from active friction intervention events. The NaN intervention rows may not represent failed interventions but rather a different event type. This should be verified against the project description docx before cleaning.

---

## 6. Study Time Variables: Critical Interpretation Issue

**`secondsSinceStudySetup` and `weeksSinceStudySetup` are entirely non-positive (all ≤ 0).**

| Stat | secondsSinceStudySetup | weeksSinceStudySetup |
|---|---|---|
| Min | −77,570,620 | −129 |
| Max | 0 | −1 (3 rows = 0) |
| Rows ≤ 0 | 2,490,260 (100%) | 2,490,260 (100%) |

The codebook states these measure "distance (in seconds/weeks) to when the study was started by the user" — implying positive forward-counting values. The actual data is entirely negative, which contradicts this description.

**Investigation result:** Within each participant, `timestamp_epoch - secondsSinceStudySetup` produces a near-constant value (median within-participant standard deviation = 0.0; 287 participants have exact zero variance). This confirms that `secondsSinceStudySetup` encodes a fixed per-participant reference anchor, not absolute seconds since setup.

The anchor is **not** the last event timestamp — the mean difference is approximately −31,700 seconds (~8.8 hours) after each participant's last event. The anchor may be a study export timestamp or enrollment end date.

**Practical consequence:**
- These variables **cannot be interpreted as "time elapsed since app setup"** as the codebook suggests
- They CAN be used for **relative temporal ordering within a participant**: more negative = earlier event; less negative (closer to 0) = more recent event
- To reconstruct a forward-counting time variable, use `timestamp` directly: `event_time - participant_first_event_time`
- Alternatively, negate: `-secondsSinceStudySetup` gives "seconds before study end anchor" as a positive integer
- `weeksSinceStudySetup` has the same issue and the same workaround

---

## 7. Participant Structure and ID Matching

### Participant counts

| File | Unique participants |
|---|---|
| Behavioral | 1,039 |
| Survey | 299 (after dedup) |

### Survey UUID prefix

Survey `uuid` values have the format:
```
donatus-master-thesis-one-sec-early-2023-{UUID}
```

The `{UUID}` suffix matches the `participantUuid` format in the behavioral file. Direct string comparison fails; the prefix must be stripped.

**ID matching result (suffix-based):**

| Category | Count |
|---|---|
| Survey participants matched to behavioral data | 283 |
| Survey participants with no behavioral match | 16 |
| Behavioral participants with no survey | 756 |

**Cleaning rule:** strip the prefix `donatus-master-thesis-one-sec-early-2023-` from survey `uuid` before matching. Uppercase both sides for safety.

### Survey duplicate rows

304 survey rows, 299 unique `uuid` values → **5 duplicate uuid rows**. Rule: keep first occurrence.

---

## 8. Data Quality Issues

| Issue | Severity | Notes |
|---|---|---|
| Behavioral CSV comma-delimited; survey CSV semicolon-delimited | Medium | Document per-file; do not use a shared loader without parameterizing separator |
| `secondsSinceStudySetup` / `weeksSinceStudySetup` all negative — codebook description incorrect | High | Variables are still usable for relative temporal ordering; reconstruct forward time from `timestamp` |
| Two undocumented `resolution` values: `dismissedByStructuredIntervention`, `dismissedWithHealthyAlternative` | Medium | Confirm meaning before mapping; 812 affected rows |
| `interventionDuration` + `interventionType`: 63.5% NaN — entire `closedApp` event type has NaN intervention fields | High | NaN rows may represent a different event logging path, not missing data; classify separately |
| `purpose`: 83.1% NaN | High | Open-text field; too sparse for systematic feature use |
| Survey `uuid` has `donatus-master-thesis-one-sec-early-2023-` prefix not in behavioral file | High | Strip prefix for ID matching; verify 16 unmatched survey participants |
| Gender in survey stored as text strings, not numeric codes as codebook implies | Medium | Apply text-based recoding, not numeric mapping |
| 5 duplicate uuid rows in survey | Low | Deduplicate: keep first row |
| CSV survey has trailing whitespace in all text fields | Low | Apply `.str.strip()` during cleaning; or use XLSX which is pre-trimmed |
| `whastapp` typo in behavioral `app` column | Low | Same as DS1; correct to `whatsapp` in canonical `app_name` column |
| 16 survey participants with no behavioral match | Medium | Likely participants who completed the survey but whose events weren't captured or who used a different app version |
| 756 behavioral participants with no survey | Medium | Behavioral-only analysis available; no psychosocial variables for these participants |
| No NaN in core behavioral columns (`app`, `resolution`, `timestamp`, `participantUuid`) | Low (positive) | No missing identifiers to handle |
| No fully duplicate rows in behavioral file | Low (positive) | No deduplication needed |

---

## 9. App Distribution

399 unique apps. Top 10:

| App | Events | Share |
|---|---|---|
| instagram | 937,307 | 37.6% |
| twitter | 391,317 | 15.7% |
| youtube | 153,608 | 6.2% |
| tikTok | 139,539 | 5.6% |
| facebook | 134,545 | 5.4% |
| reddit | 78,037 | 3.1% |
| snapchat | 72,246 | 2.9% |
| apollo | 53,531 | 2.1% |
| telegram | 42,888 | 1.7% |
| linkedin | 41,016 | 1.6% |
| whastapp (typo) | 39,045 | 1.6% |

399 unique apps vs 48 in DS1 — much broader coverage reflecting longer naturalistic use.

---

## 10. Longitudinal Structure

| Stat | Value |
|---|---|
| Mean events per participant | 2,397 |
| Median events per participant | 1,304 |
| Max events per participant | 42,119 |
| Participants with <10 events | 39 |
| Participants with 1,000+ events | 590 |
| Participants with 5,000+ events | 128 |
| Mean study duration (days) | 97 |
| Median study duration (days) | 66 |
| Max study duration (days) | 897 (~2.5 years) |
| Participants with >365 days | 39 |
| Participants with >730 days | 3 |

This is the most longitudinally rich dataset in the collection. The distribution is highly heterogeneous: some participants have tens of thousands of events over months; others have a handful.

---

## 11. Codebook Discrepancies

| Discrepancy | Severity |
|---|---|
| `resolution`: codebook lists 3 values; data has 5 (undocumented: `dismissedByStructuredIntervention`, `dismissedWithHealthyAlternative`) | Medium |
| `secondsSinceStudySetup`/`weeksSinceStudySetup`: codebook says forward-counting from setup; all values are negative (counted backward from per-participant anchor) | High |
| `gender`: codebook says 1=Female, 2=Male etc. (numeric codes); actual data stores text strings | Medium |
| Survey `uuid` prefix (`donatus-master-thesis-one-sec-early-2023-`) not mentioned in codebook | Medium |
| No mention of NaN in codebook for `interventionDuration`, `interventionType`, `purpose` | Low |

---

## 12. Relevance for Modeling

| Construct | Availability | Notes |
|---|---|---|
| Intervention outcome | Direct | `resolution` — 5 values; `closedApp` dominant |
| Intervention type | Partial | 36.5% of rows have `interventionType`; distinct 6 types |
| Intervention duration | Partial | Same 36.5% coverage; seconds |
| Temporal structure | Direct | `timestamp` ISO UTC — parse with `pd.to_datetime` |
| Relative time within participant | Indirect | Use `timestamp` directly; negate `secondsSinceStudySetup` for relative ordering |
| Long-term adaptation | Strong | Median 66 days; 590 participants with 1,000+ events |
| App identity | Direct | 399 unique apps |
| Purpose / context | Sparse | 83.1% NaN; not viable for systematic use |
| Psychosocial moderators | None | Survey is entirely qualitative/retrospective; no scales |

**Best use of DS4:** Longitudinal behavioral analysis, adaptation modeling, habit stability, response heterogeneity across participants and apps. Weakest dataset for psychosocial moderation (no psychometric scales). Strongest dataset for long-run behavioral patterns.

---

## 13. Recommended Cleaning Steps (not yet applied)

1. Re-read behavioral CSV with `sep=','` (comma-delimited)
2. Re-read survey CSV with `sep=';'` (semicolon-delimited)
3. Parse `timestamp` to UTC datetime: `pd.to_datetime(df['timestamp'], utc=True)`
4. Correct `whastapp` → `whatsapp` in canonical `app_name` column
5. Classify `closedApp` vs intervention events: consider separating rows with NaN `interventionType` into a distinct event class before outcome modeling
6. Add `participant_id_canonical` column (copy of `participantUuid`)
7. Strip `donatus-master-thesis-one-sec-early-2023-` prefix from survey `uuid`; add `participant_id_canonical` to survey (matched UUID, uppercase)
8. Deduplicate survey: 5 duplicate uuid rows — keep first
9. Strip trailing whitespace from all survey text columns (or use XLSX version)
10. Recode `gender` from text to clean categorical (verify against text values, not codebook numeric codes)
11. Create `event_outcome_simple` mapping:
    - `openedApp` → `opened`
    - `dismissedAppOpening` → `dismissed`
    - `closedApp` → `closed`
    - `dismissedByStructuredIntervention` → `dismissed_structured` (or `dismissed` — decide after checking meaning)
    - `dismissedWithHealthyAlternative` → `dismissed_alternative` (or `dismissed`)
12. Document `secondsSinceStudySetup`/`weeksSinceStudySetup` as inverted-sign variables; create `days_since_first_event` from `timestamp` as a clean forward-counting alternative
13. Write participant linkage table: behavioral × survey overlap

---

*This report was produced during the pre-cleaning audit phase. No transformations have been applied to raw files.*

# Harmonization Notes

This file documents how Datasets 1, 4, 5, and 6 may be aligned for cross-dataset work.

## Principle

The goal is not to erase dataset-specific structure.
The goal is to define a shared working schema for the variables that matter most for smartphone behavior, intervention response, and later phenotyping.

---

## 1. Dataset-specific ID variables

| Dataset | Behavioral ID | Survey ID | Notes |
|---|---|---|---|
| DS1 | `participantUuid` | `participantUuid` | cleanest ID alignment |
| DS4 | `participantUuid` | `uuid` | **confirmed**: survey `uuid` has `donatus-master-thesis-one-sec-early-2023-` prefix — strip prefix + uppercase to match; 283/299 survey participants matched; 16 survey-only, 756 behavioral-only |
| DS5 | `userid` | `uuid` | **confirmed**: behavioral `userid` has prefix `study-one-sec-next-gen-bzkj-2024-` — strip to get canonical `one-sec-next-gen-bzkj-2024-XXXX` format; 572/573 behavioral participants matched to pre-survey; 284 in all three files |
| DS6 | `ID` | `response_id` (survey), `ID` (demo) | **confirmed**: `ID` = `response_id` = direct join, no transformation needed; all 243 behavioral participants are in demographics and survey |

### Harmonization rule
Create a canonical participant column in cleaned outputs:

- `participant_id_raw`
- `participant_id_canonical`

Do not overwrite the original ID column.
Keep source-specific ID fields for traceability.

---

## 2. Time variables

| Dataset | Main time field(s) | Format notes |
|---|---|---|
| DS1 | `timestamp`, `secondsSinceOneSecSetup` | **confirmed Unix epoch int64** — `pd.to_datetime(unit='s', utc=True)`; no timezone column (UTC assumed); `secondsSinceOneSecSetup` has 18.9% NaN |
| DS4 | `timestamp`, `secondsSinceStudySetup`, `weeksSinceStudySetup` | **confirmed ISO 8601 UTC** — `pd.to_datetime(utc=True)`; range 2020-09-30 to 2023-04-02; `secondsSinceStudySetup` / `weeksSinceStudySetup` are **all ≤ 0** (inverted — count backwards from per-participant anchor, not forward from setup); reconstruct forward time from `timestamp` directly |
| DS5 | `timestamp`, `timezone`, `timeIntervalUntilReIntervention` | **confirmed**: local ISO string (no UTC offset) — parse as naive then localize per `timezone` col (IANA) → UTC; fallback Europe/Berlin for 3,457 NaN-timezone rows; `timeIntervalUntilReIntervention` in seconds, 77.9% NaN (reintervention group only) |
| DS6 | `timestamp`, `date`, `time`, `hour`, `participation_day`, `period`, survey dates | **confirmed**: ISO 8601 UTC — `pd.to_datetime(utc=True)` directly; `participation_day` is study-day index; `period` = baseline or intervention; session file covers both periods |

### Harmonization rule
Create canonical time fields where possible:

- `event_timestamp_utc`
- `event_date`
- `event_time_local`
- `study_time_seconds`
- `study_time_weeks`
- `participation_day`
- `survey_wave`

Not every dataset will support every field.

---

## 3. Core event variables

### Shared behavioral core

| Canonical concept | DS1 | DS4 | DS5 | DS6 |
|---|---|---|---|---|
| app | `app` | `app` | `app` | `app` |
| outcome | `resolution` | `resolution` | `resolution` | `resolution` |
| purpose/reason | `purpose` | `purpose` | `reason` | `purpose` |
| intervention duration | — | `interventionDuration` | `interventionDuration` | `interventionDuration` |
| intervention type | — | `interventionType` | — | `interventionType` |
| reintervention flag | — | — | `timeIntervalUntilReIntervention` | `isReIntervention`, `timeIntervalUntilReIntervention` |



### Harmonization rule
Create these canonical behavioral columns where possible:

- `app_name`
- `event_outcome`
- `event_reason_or_purpose`
- `intervention_duration_sec`
- `intervention_type`
- `is_reintervention`
- `reintervention_delay_sec`

---

## 4. Experimental condition / study design

| Dataset | Condition structure |
|---|---|
| DS1 | compact intervention study with pre/post survey, but no explicit `cond` column shown in listed files |
| DS4 | non-experimental / retrospective use dataset |
| DS5 | **confirmed**: `cond` in pre-survey only (NOT in behavioral); values: `control` (265), `default` (264), `reintervention` (263); must join to behavioral via `participant_id_canonical` |
| DS6 | **confirmed**: `condition` (text: control/default/intervention) in behavioral files; `cond` (numeric 1-6, cohort groups); `cond_exp2` (binary: OneSec Default / Control) in survey; `period` (baseline/intervention) |

### Harmonization rule
Create:
- `study_condition`
- `study_design_type`

Examples:
- DS1: `compact_default_intervention`
- DS4: `non_experimental_retrospective`
- DS5: `control/default/reintervention`
- DS6: `control/default/intervention/open_phase` depending on verified mapping

---

## 5. Survey structures

### DS1
Pre/post survey with consent, goals, perceived problematic consumption, happiness, and comparison variables.

### DS4
Post-survey only, largely qualitative and demographic/experience-focused.

### DS5
Pre/post survey with strong psychosocial scales and condition.

### DS6
Repeated survey structure with condition and multiple indices for control, addiction/problematic use, self-control, well-being, and social connection.

### Harmonization rule
Use two layers:

#### Layer A: raw-survey-preserving cleaned files
Keep each dataset’s survey structure intact.

#### Layer B: harmonized summary features
Create cross-dataset summaries such as:
- `self_report_problematic_use`
- `self_report_happiness_or_wellbeing`
- `self_report_goal_alignment`
- `self_report_self_control`
- `self_report_social_wellbeing`
- `fomo_index`

Only create these where defensible.

---

## 6. Outcome harmonization

**DS1 confirmed resolution values:**
- `openedApp` → `opened`
- `dismissedAppOpening` → `dismissed`
- `closedApp` → `closed`  *(third category — distinct from dismissed; user opened then closed)*
- NaN → `missing`

Note: DS1 has a `closedApp` outcome that may not be present in all other datasets. The simple mapping must accommodate this.

### Harmonization rule
Create:
- `event_outcome_raw` (preserve original `resolution` value)
- `event_outcome_simple`

Confirmed simple mapping for DS1 (applied in `02_dataset_1_cleaning.ipynb`):
- `opened`
- `dismissed`
- `closed`
- `missing`

Other datasets may not have a `closed` category — confirm unique values per dataset before applying cross-dataset mapping.

**DS4 confirmed resolution values:**
- `closedApp` (47.1%) → `closed`
- `openedApp` (35.4%) → `opened`
- `dismissedAppOpening` (17.5%) → `dismissed`
- `dismissedByStructuredIntervention` (806 rows, 0.03%) → **undocumented in codebook — confirm meaning before mapping**
- `dismissedWithHealthyAlternative` (6 rows) → **undocumented in codebook — confirm meaning before mapping**
- No NaN in `resolution`

Note: `closedApp` is the dominant outcome in DS4 (47%) vs 24% in DS1. The two undocumented dismissal types must be mapped explicitly.

**DS5 confirmed resolution values:**
- `openedApp` (61.6%) → `opened`
- `dismissedAppOpening` (21.5%) → `dismissed`
- `closedApp` (15.6%) → `closed`
- NaN (1.2%) → `missing`
- `dismissedByStructuredIntervention` (119 rows, 0.04%) → `dismissed_other` (undocumented type)

**DS6 confirmed resolution values:**
- ALL rows = `openedApp` in both behavioral files (session + baseline)
- No dismiss or close events in resolution column
- Session close timing inferred from `group_id` + `close_ts` / `time_diff_secs`

### Delimiter note (confirmed for all datasets)
- DS1: all three CSVs use **semicolon (`;`)** as delimiter
- DS4: behavioral CSV uses **comma (`,`)**; survey CSV uses **semicolon (`;`)** — mixed within the same dataset
- DS5: **confirmed** all three CSVs use **semicolon (`;`)** as delimiter
- DS6: **confirmed** all CSV files use **comma (`,`)** as delimiter

---

## 7. Sequence and transition structure

| Dataset | Sequence richness |
|---|---|
| DS1 | limited, requires sorting by participant and timestamp |
| DS4 | moderate, requires ordering and transition inference |
| DS5 | moderate-good, requires ordering and intervention-aware transition logic |
| DS6 | very rich, with precomputed next/prev and sequence/session fields |

### Harmonization rule
Create derived transition tables with a common structure:

- `participant_id_canonical`
- `event_timestamp_utc`
- `app_current`
- `app_next`
- `outcome_current`
- `outcome_next`
- `time_to_next_event_sec`
- `intervention_context_flag`

---

## 8. Suggested cleaned output families

### A. Event-level cleaned files
One per dataset.

### B. Survey-level cleaned files
One per dataset and survey wave.

### C. Participant-level summary files
Derived and harmonized.

### D. Transition/session files
Especially important for DS5 and DS6, optionally DS1 and DS4.

---

## 9. Main harmonization risks

- ID fields differ across behavioral and survey files
- survey scales differ in content and scale format
- event outcomes may not map identically
- DS4 is observational while DS5/DS6 are experimental
- DS6 contains multiple file families with partly overlapping structures
- DS1 and DS4 may support less direct psychosocial mapping than DS5/DS6

---

## 10. Immediate next harmonization tasks

1. verify ID compatibility within each dataset
2. inspect unique `resolution` values
3. inspect missingness in `purpose` / `reason`
4. compare csv vs xlsx duplicates where present
5. define canonical participant/event/outcome columns
6. decide which survey variables can truly be harmonized and which should remain dataset-specific
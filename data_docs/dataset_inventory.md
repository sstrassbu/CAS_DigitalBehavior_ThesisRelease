# Dataset Inventory

This file provides a structured overview of the most important datasets in the project.

The raw folder structure is intentionally preserved in its original form.
This document acts as the standardized working map.

Datasets 2, 3, 7, and 8 (self-commitment, personality survey, streaks, boosting) have no overview docs at all. This is intended as they will not be needed for now. Hereby those datasets are officially marked  out of the current scope.

---

## Dataset 1: Compact friction intervention testing

**Raw folder:** `data_raw/1. data set, compact friction intervention testing/`  
**General type:** compact intervention study with behavior + pre-survey + post-survey  
**Project description:** Compact default intervention study  
**Documentation visible:** behavior codebook, pre-survey codebook, post-survey codebook, project description docx

### Main files
- behavioral: `behavioral_data_set_1.csv`
- pre-survey: `pre_survey_data_set_1.csv`
- post-survey: `post_survey_data_set_1.csv`

### Key variables visible
- behavior: `participantUuid`, `app`, `timestamp`, `purpose`, `resolution`, `secondsSinceOneSecSetup`
- surveys: shared `participantUuid`, problematic consumption, goals, happiness, and post-study evaluation variables

### First interpretation
A clean compact intervention dataset and a strong candidate for the first preprocessing pipeline.

### Main open questions
- Are there repeated survey responses per participant?
- What are the exact `resolution` levels?
- How much data is missing in `purpose`?
- Are csv and xlsx versions identical?

### Priority
Very high

---

## Dataset 4: Large non-experimental data

**Raw folder:** `data_raw/4. data set, large non-experimental data/`  
**General type:** longitudinal non-experimental behavior + retrospective/post survey  
**Project description:** historic, retrospective use data from existing users with very long use windows.

### Main files
- behavioral: `behavior_data_set_4.csv`
- post-survey: `post_survey_data_set_4.csv`

### Key variables visible
- behavior: `app`, `resolution`, `timestamp`, `interventionDuration`, `interventionType`, `purpose`, `participantUuid`, `secondsSinceStudySetup`, `weeksSinceStudySetup`, `userIndex`
- survey: `uuid`, age/gender, reasons for use, benefits, negatives, usage format, comments

### First interpretation
Especially strong for long-term adaptation, user heterogeneity, and observational usage structure.

### Main open questions
- `participantUuid` (behavior) and `uuid` (survey) are assumed to refer to the same participant — confirm value format matches during audit
- Is the behavior file correctly parsed as comma-separated fields?
- How complete are intervention fields?
- Can qualitative survey responses be meaningfully summarized?

### Priority
High

---

## Dataset 5: German adolescents

**Raw folder:** `data_raw/5. data set, German adolescents/`  
**General type:** experimental adolescent dataset with behavior + pre/post survey  
**Project description:** two interventions tested; includes control, default friction, and reintervention groups.

### Main files
- behavioral: `behavior_data_set_5.csv`
- pre-survey: `pre_survey_data_set_5.csv`
- post-survey: `post_survey_data_set_5.csv`

### Key variables visible
- behavior: `timestamp`, `timezone`, `interventionDuration`, `timeIntervalUntilReIntervention`, `app`, `resolution`, `userid`, `reason`, suggestion-related fields
- pre-survey: `uuid`, `cond`, age, digital well-being, time/problem items, goals, belonging, ostracism, FoMO
- post-survey: digital well-being, time/problem items, solve/address goal, belonging, ostracism, FoMO

### First interpretation
One of the strongest datasets for intervention-response modeling and moderator analysis.

### Main open questions
- How exactly do `userid` and `uuid` align?
- Are condition labels identical across all linked files?
- How informative are suggestion-related behavior columns?
- What are the exact unique values of `resolution` and `reason`?

### Priority
Very high

---

## Stanford Health Study: OneSec Friction + HealthKit (separate cohort)

**Raw folder:** `data_raw/stanford-health-study/study-stanford-health-2025-20260527203252-6a1754f469875/`  
**General type:** Longitudinal naturalistic study — OneSec friction intervention logs + Apple HealthKit physiological data  
**Project description:** Separate cohort from DS1–DS6. 33 iPhone/Apple Watch users in daily life. No experimental condition manipulation visible in data; naturalistic usage.  
**Documentation:** No codebook shipped. README with full schema at `data_raw/stanford-health-study/study-stanford-health-2025-20260527203252-6a1754f469875/README.md`

### Two data streams

**Stream 1 — Intervention events (JSON, uncompressed):**  
Per-participant, per-export-session. File: `study-stanford-health-2025-{UUID}.json`  
Many early-session files are empty `[]` — this is valid (no events yet at that snapshot).

**Stream 2 — HealthKit FHIR observations (zlib-compressed JSON):**  
19 physiological data types. File: `HK{DataType}_{UUID}.json.zlib`  
Format: FHIR R4 Observation. Dedup required across sessions (cumulative exports).

### Key variables

- Intervention: `participantUUID`, `timestamp` (unix epoch), `app`, `timezone` (IANA), `resolution` (4 values), `interventionType` (21 values), `isReIntervention`, `interventionDuration`, `timeIntervalUntilReIntervention`, `purpose`
- HealthKit: `id` (UUID), `effectivePeriod`/`effectiveDateTime` (ISO 8601 nanosecond), `valueQuantity`, `valueCodeableConcept`, `component` (StateOfMind)

### First interpretation

Unique in this project for having direct physiological context alongside friction events. No survey data. Strongest asset is the pairing of override/compliance behavior with HRV, sleep, and mood (StateOfMind). Primary use: external replication of DS5 phenotypes; physiological context modeling.

### Main open questions

- Do the two UUID-only app identifiers correspond to known apps? (Cannot resolve without OneSec team clarification)
- Why do some participants have intervention records dating to 2020? (Device clock error suspected)
- Is StateOfMind data spatially and temporally correlated with intervention triggers, or too sparse?
- What determines which participants appear in the Stanford study vs the DS1–DS6 series?

### Priority

Medium — standalone analysis after DS5 Step 2 is complete. Candidate for external replication of phenotyping results.

---

## Dataset 6: Danish adolescents

**Raw folder:** `data_raw/6. data set, Danish adolescents/`  
**General type:** rich experimental multi-file dataset with repeated survey and detailed session structure  
**Project description:** two interventions tested; includes baseline and later phase with relaxed restrictions for some participants.

### Main files
- `survey_data_clean.csv`
- `demographic_data.csv`
- `baseline_sessions_filt3.csv`
- `session_time_dataset_97_5_cutoff_data_forwarded.csv`
- plus additional files shown in the PDF with streak/open/resist and broad pre/post survey structures

### Key variables visible
- survey: `response_id`, `cond`, survey timing, addiction/problematic use, self-control, FoMO, well-being/social connection
- demographics: `ID`, age, gender, region
- behavior/session: `ID`, app, timestamp, resolution, purpose, interventionType, interventionDuration, `isReIntervention`, `cond`, `condition`, `participation_day`, `period`, `app_next`, `app_prev`, timing diffs, valid open flags
- session/group file adds `group_id` and richer open/close structure

### First interpretation
The richest but most complex dataset. Excellent for sequence modeling, substitution analysis, repeated exposure, and multidimensional phenotyping.

### Main open questions
- Which ID system links all file families?
- Which behavioral file should be treated as primary?
- What is the difference between survey variants and extra files shown in the PDF?
- Which variables are engineered versus raw?

### Priority
Very high











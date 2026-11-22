# Dataset 6 Overview

**Audit status: COMPLETED — 2026-04-15**  
**Cleaned outputs:** `outputs/cleaned/ds6_behavioral_clean.csv`, `ds6_survey_clean.csv`, `ds6_demographics_clean.csv`, `ds6_participant_linkage.csv`  
**Audit report:** `outputs/reports/ds6_audit_report.md`

## Basic information

**Dataset name:** Dataset 6 — Danish adolescents  
**Raw folder:** `data_raw/6. data set, Danish adolescents/`  
**Project description:** Two interventions tested for Danish adolescents  
**Design summary:** Longitudinal experimental study — baseline phase, intervention phase, and later open-restriction phase.

## Confirmed key facts

- **Delimiter:** comma for all CSV files
- **Participants:** 243 behavioral, 399 enrolled (demographics), 269 with survey data
- **Behavioral rows:** 353,796 (session file); 195,515 (baseline-only file)
- **Resolution:** ALL rows = openedApp in both behavioral files — no dismiss/close outcomes
- **Timestamp:** ISO 8601 UTC strings — parse directly with `pd.to_datetime(utc=True)`
- **ID transform:** none — `ID` = `response_id` direct join
- **Primary behavioral file:** `session_time_dataset_97_5_cutoff_data_forwarded.csv` (both periods)
- **Baseline file:** `baseline_sessions_filt3.csv` (baseline only, additional sequence features)
- **Periods:** baseline (158,889 rows), intervention (194,907 rows)
- **Conditions:** control (153,236), default (100,888), intervention (99,672)
- **interventionType confirmed:** denmark (68,528), breathingExercise (39,116), math (2,676), followTheDot (1,469), randomText (1)
- **isReIntervention:** 2,120 events
- **purpose:** 89% NaN — not usable for routine analysis
- **Session grouping:** via `group_id`; close timing from `time_diff_secs` / `close_ts`
- **Streak/resist/lag variables from PDF:** NOT confirmed in any CSV file — do not treat as available
- **Gender:** `kvinde` = female, `mand` = male
- **Age:** 13–17 (true adolescent range)
- **Survey clean:** 2 waves (survey_nr 1-2), 269 unique participants
- **Survey full:** 3 waves (survey_nr 1-3), 440 unique participants (includes raw items)

## Visible structure

> **Note on folder layout:** DS6 has a two-level subfolder structure unlike the other datasets.
> Files are split between `Data/` and `Data/behavioral data/` — see paths below.

### `data_raw/6. data set, Danish adolescents/Data/behavioral data/`
- `baseline_sessions_filt3.csv`
- `session_time_dataset_97_5_cutoff_data_forwarded.csv`
- `demographic_data.csv` *(note: stored here despite non-behavioral content)*
- `survey_data_clean.csv` *(note: stored here despite being survey data)*
- `survey_data_full.csv`

### `data_raw/6. data set, Danish adolescents/Data/`
- `Danish adolescents & one sec, main study, pre-survey.csv`
- `Pre-Survey overview.pdf`

### `data_raw/6. data set, Danish adolescents/`
- `Project description, Two interventions tested for Danish adolescents.docx`

### Additional data structures visible in PDF (not confirmed in CSV files above)
The project description PDF shows additional extracted data structures that may originate from a separate preprocessing step or an earlier data version. These have **not been confirmed** as present in any of the five CSV files listed above:
- streak/open/resist variables
- lead/lag variables
- dismiss/open flags
- a combined pre/post survey structure with `pre.*` and `post.*` variables
- condition labels such as `positive`, `negative`, and `control`

Do not treat these as confirmed available until inspected.

## Survey dataset (clean)

**File:** `survey_data_clean.csv`  
**Rows:** 478  
**Observed columns shown in PDF:**
- `response_id`
- `cond`
- `start_date`
- `end_date`
- `survey_nr`
- `kontrolover_so_me`
- `taenkerpa_so_me`
- `addiction_index`
- `tilfredsmed_so_me`
- `retention_index`
- `self_control_index`
- `trivsel`
- `socialconnection`
- `socialtforbundet`
- `fo_mo`
- `cond_exp2`
- `survey_nr_fact`

## Demographic dataset

**File:** `demographic_data.csv`  
**Rows:** 399  
**Observed columns shown in PDF:**
- `ID`
- `age`
- `gender`
- `region`

## Baseline/session behavioral dataset

**File:** `baseline_sessions_filt3.csv`  
**Rows:** 195,515  
**Observed columns shown in PDF include:**
- `ID`
- `study_id`
- `date`, `date2`
- `studyActivated`
- `app`
- `timestamp`
- `time`
- `week`, `day`, `week_day`, `hour`
- `resolution`
- `purpose`
- `interventionType`
- `interventionDuration`
- `isReIntervention`
- `cond`, `condition`
- `timeIntervalUntilReIntervention`
- `start_date_test`
- `time_at_activation`, `time_at_intervention`, `time_at_outro`, `time_at_end`
- `participation_day`
- `period`
- `first_intervention_time`
- `first_intervention_participation_day`
- `app_next`, `app_next2`, `app_next3`
- `app_prev`, `app_prev2`
- `resolution_next*`, `resolution_last*`
- `timestamp_next*`, `timestamp_last*`
- `valid_open*`
- `close_ts`
- `time_diff_secs`, `time_diff_minutes`, `time_diff_minutes_round`
- `unmatched_open`
- `row_id`
- `date_at_activation`, `date_at_intervention`
- `days_before_activation`, `days_before_activation_num`

## Session/group behavioral dataset

**File:** `session_time_dataset_97_5_cutoff_data_forwarded.csv`  
**Rows:** 353,796  
**Observed columns shown in PDF include:**
- `ID`
- `study_id`
- `studyActivated`
- `app`
- `timestamp`
- `time`
- `week`, `day`, `week_day`
- `resolution`
- `purpose`
- `interventionType`
- `interventionDuration`
- `isReIntervention`
- `cond`, `condition`
- `timeIntervalUntilReIntervention`
- `participation_day`
- `period`
- `first_intervention_time`
- `first_intervention_participation_day`
- `group_id`
- `resolution_next`
- `openedapp_open_time`
- `first_open_time`
- `first_in_group`
- `not_first_open_in_group`
- `last_closedapp_time`
- `last_close_in_group`
- `not_last_close_in_group`
- `app_next`, `app_next2`, `app_next3`
- `app_prev`, `app_prev2`
- multiple next/last/open/close timing variables
- `valid_open*`
- `close_ts`
- `time_diff_*`
- `row_id`
- `hour`
- `date_at_activation`
- `date_at_intervention`
- `days_before_activation*`

## Preliminary interpretation

Dataset 6 is the richest and most structurally advanced dataset among the ones documented so far.
It appears to combine:

- repeated behavioral event/session data
- condition and intervention variables
- baseline and later study phases
- demographics
- repeated survey data
- engineered next/previous app features
- session grouping structure
- intervention timing variables
- validity flags for open events
- possibly additional streak/resistance features shown in the PDF

This dataset looks especially valuable for:
- sequence modeling
- substitution analysis
- reintervention analysis
- repeated-exposure adaptation
- longitudinal phenotyping
- richer model integration later on

## Likely file roles

| File | Likely role | Confidence | Notes |
|---|---|---:|---|
| `baseline_sessions_filt3.csv` | major cleaned/engineered behavioral file | High | likely core baseline/session source |
| `session_time_dataset_97_5_cutoff_data_forwarded.csv` | richer grouped session/event file | High | strong candidate for transition/session work |
| `survey_data_clean.csv` | cleaned survey dataset | High | main repeated survey source |
| `survey_data_full.csv` | fuller/rawer survey dataset | Medium-High | compare with clean version |
| `demographic_data.csv` | demographic participant file | High | useful merge source |
| `Danish adolescents & one sec, main study, pre-survey.csv` | pre-survey source | High | likely additional participant-level survey file |
| `Pre-Survey overview.pdf` | survey documentation | High | important |
| project description docx | study design and phase structure | High | essential |

## Likely unit of observation

### Behavioral files
Likely one event, session event, or grouped app-opening event depending on file.

### Survey files
Likely one survey response per participant per wave.

### Demographics
One row per participant.

## Likely strengths

- very rich behavioral structure
- explicit condition variables:
  - `cond`
  - `condition`
  - `cond_exp2`
- explicit intervention variables:
  - `interventionType`
  - `interventionDuration`
  - `isReIntervention`
  - `timeIntervalUntilReIntervention`
- excellent sequence structure:
  - `app_next*`
  - `app_prev*`
  - `group_id`
- repeated study-time structure:
  - `participation_day`
  - `period`
  - survey number fields
- strong psychosocial survey layer:
  - `self_control_index`
  - `addiction_index`
  - `trivsel`
  - `socialconnection`
  - `fo_mo`
- demographic merge potential
- likely the strongest dataset for:
  - substitution
  - adaptation
  - multidimensional phenotype profiling
  - richer model comparison

## Likely limitations

- internal complexity is high
- there may be multiple partially overlapping behavioral file families
- ID structures may differ across:
  - `ID`
  - `response_id`
  - `UUID` in other extracts
- some variables are clearly engineered rather than raw
- strong preprocessing discipline will be necessary to avoid confusion
- this should probably not be your very first dataset for a full pipeline

## Most promising immediate use cases

- advanced event/session cleaning
- cross-file ID and phase mapping
- app-transition analysis
- substitution and sequence analysis
- repeated-exposure summaries
- phenotype dimensions from both survey and behavior
- intervention phase comparisons

## Most promising later model families

- network / transition models
- stochastic-process summaries
- information-theoretic regularity measures
- agent-based within-user and across-user formulations
- richer state/process models
- stronger validation and cross-model comparison

## Immediate audit priorities

1. determine the relationship between:
   - `baseline_sessions_filt3.csv`
   - `session_time_dataset_97_5_cutoff_data_forwarded.csv`
2. determine which behavioral file should be primary for which analysis purpose
3. verify how `ID`, `response_id`, and any additional UUID fields align
4. inspect unique values of:
   - `resolution`
   - `interventionType`
   - `cond`
   - `condition`
   - `period`
5. compare `survey_data_clean.csv` and `survey_data_full.csv`
6. inspect how the additional pre-survey file fits into the overall survey structure
7. determine which columns are engineered vs original
8. inspect missingness in:
   - `purpose`
   - timing variables
   - sequence variables
   - valid-open flags

## Recommendation

Dataset 6 is probably your most valuable later-stage dataset for:
- rich phenotyping
- substitution and transition analysis
- repeated intervention dynamics
- more advanced model comparison

But because of its complexity, it is best approached **after** you have already built and tested your preprocessing workflow on a simpler dataset such as DS1, and possibly DS5.
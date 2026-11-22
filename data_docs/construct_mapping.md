# Construct Mapping

This document maps key theoretical constructs from the project to directly observed variables or proxy variables in Datasets 1, 4, 5, and 6.

## Core rule

A construct should only be treated as directly observed if the dataset clearly contains a variable that measures it.  
Otherwise, the construct must be treated as proxy-based or model-derived.

## Confidence scale

- **High** = directly or very closely observed
- **Medium** = indirectly but reasonably approximated
- **Low** = weak proxy or strongly model-dependent
- **Very low** = mainly exploratory / interpretive

---

# Dataset 1 — Compact friction intervention testing

## Behavioral file
`behavioral_data_set_1.csv`

Observed columns include:
- `participantUuid`
- `app`
- `timestamp`
- `purpose`
- `resolution`
- `secondsSinceOneSecSetup`

## Survey files
`pre_survey_data_set_1.csv`, `post_survey_data_set_1.csv`

Observed survey columns include:
- `participantUuid`
- `duration`
- `consent_general`
- pre: `problems`, `goals`, `hours`, `problematic_cons`, `happy`, `problematic_cons_general`, `problematic_cons_compared`
- post: `problems_solved`, `goals_reached`, `hours`, `problematic_cons`, `happy`, `progress_satisfaction`, `problematic_cons_general`, `problematic_cons_compared`

### DS1 construct map

| Construct | Directly observed? | Candidate variable(s) | Confidence | Notes |
|---|---|---:|---:|---|
| participant identifier | yes | `participantUuid` | High | shared across behavior and surveys; 1 NaN row in behavioral |
| app event / target app | yes | `app` | High | 48 unique apps; `whastapp` typo corrected to `whatsapp` in canonical column |
| event timing | yes | `timestamp` | High | **confirmed Unix epoch int64** — convert with `pd.to_datetime(unit='s', utc=True)` |
| intervention outcome | yes | `resolution` | High | **confirmed 3 values:** `openedApp` (49.9%), `dismissedAppOpening` (25.8%), `closedApp` (24.1%); 468 NaN (0.1%) |
| app-opening context / motivation | partial | `purpose` | Low-Medium | **confirmed 71.3% NaN** — too sparse for systematic use; qualitative supplement only |
| time since setup | yes | `secondsSinceOneSecSetup` | High | **confirmed 18.9% NaN**; range 76 sec – 64.7 days since app setup; codebook erroneously names it `secondsSinceStudySetup` |
| pre-intervention self-reported problems | yes | `problems`, `problematic_cons*` | High | pre-survey; stored as comma-concatenated multi-select and Likert strings |
| goals / intentions | yes | `goals`, `goals_reached` | High | multi-select; stored as comma-concatenated strings |
| happiness / affect | yes | `happy` | Medium | broad well-being indicator; Likert stored as composite string |
| friction sensitivity | partial | change in `resolution` patterns over time | Medium | derived from behavior; `closedApp` outcome now confirmed as distinct from `dismissedAppOpening` |
| override tendency | partial | repeated `openedApp` outcomes over time | Medium | confirmed from `resolution` — `openedApp` is 49.9% of events |
| substitution tendency | no direct variable | inferred from sequences of `app_name` after intervention events | Low-Medium | requires temporal derivation; no pre-computed sequence fields |
| habit strength | no direct variable | repeated same-app usage over time | Medium | behavioral proxy; 619-participant behavioral file is the substrate |
| context dependence | weakly direct | `purpose` + time variables | Low | **confirmed 71.3% NaN in `purpose`** — context coverage is very sparse |
| adaptation over repeated exposure | partial | behavior vs `secondsSinceOneSecSetup` | Medium | confirmed plausible longitudinal proxy; 18.9% NaN limits coverage |

---

# Dataset 4 — Large non-experimental data

## Behavioral file
`behavior_data_set_4.csv`

Observed columns include:
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

## Survey file
`post_survey_data_set_4.csv`

Observed columns include:
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

### DS4 construct map

| Construct | Directly observed? | Candidate variable(s) | Confidence | Notes |
|---|---|---:|---:|---|
| participant identifier | yes | `participantUuid` / `uuid` | High | **confirmed**: survey uuid has `donatus-master-thesis-one-sec-early-2023-` prefix — strip before matching; 283/299 survey participants match behavioral |
| app event / target app | yes | `app` | High | **confirmed**: 399 unique apps; `whastapp` typo present (39,045 events) |
| event timing | yes | `timestamp` | High | **confirmed ISO 8601 UTC** — `pd.to_datetime(utc=True)`; range 2020-09-30 to 2023-04-02 |
| intervention duration | partial | `interventionDuration` | Medium | **confirmed 63.5% NaN** — only available for `openedApp` and `dismissedAppOpening` events; all `closedApp` events have NaN |
| intervention type | partial | `interventionType` | Medium | **confirmed 63.5% NaN** — same coverage as `interventionDuration`; 6 types: breathingExercise (dominant), minimalBreathingExercise, followTheDot, blackScreen, mirror, rotatePhone |
| event outcome | yes | `resolution` | High | **confirmed 5 values**: closedApp (47.1%), openedApp (35.4%), dismissedAppOpening (17.5%), + 2 undocumented types (812 rows); no NaN |
| purpose / reason for event | partial | `purpose` | Low | **confirmed 83.1% NaN** — too sparse for systematic use; qualitative supplement only |
| time since study start | no direct variable | derive from `timestamp` | Medium | **confirmed**: `secondsSinceStudySetup` / `weeksSinceStudySetup` are all ≤ 0 — codebook description incorrect; these count backwards from a per-participant anchor; reconstruct forward time from `timestamp` directly |
| self-described reason for use | yes | `reason_use` | Medium-High | **confirmed**: 0% NaN; open text; qualitative only |
| perceived benefits / negatives | yes | `benefits`, `negatives` | Medium-High | **confirmed**: 2.3% / 11.8% NaN; open text; qualitative only |
| usage style / configuration | yes | `usage_format` | Medium-High | **confirmed**: 14.5% NaN; open text |
| friction sensitivity | partial | outcome changes by `interventionDuration` / `interventionType` | Medium | only available for 36.5% of events; stronger for `openedApp`/`dismissedAppOpening` subset |
| adaptation over time | partial | outcome changes over time derived from `timestamp` | High | strong: median 66 days, max 897 days; reconstruct time axis from `timestamp` |
| override tendency | partial | repeated `openedApp` outcomes | Medium | **confirmed**: `openedApp` = 35.4% of all events; subset with non-NaN intervention fields: 66.3% |
| substitution tendency | no direct variable | app-transition inference from time-ordered `app` data | Low-Medium | feasible but derived; no pre-computed sequence fields |
| habit strength | no direct variable | repeated app-event regularity over long time windows | Medium-High | strong candidate: 590 participants with 1,000+ events; max 42,119 events/participant |
| user heterogeneity | partial | `userIndex`, survey comments, usage structure | Medium | confirmed: vast range in event counts (1–42,119 per participant) |
| latent motivation / self-regulation | survey only | `reason_use`, `benefits`, `negatives`, `comments` | Low-Medium | qualitative / survey-derived; no psychometric scales |

---

# Dataset 5 — German adolescents

## Behavioral file
`behavior_data_set_5.csv`

Observed columns include:
- `timestamp`
- `timezone`
- `interventionDuration`
- `timeIntervalUntilReIntervention`
- `app`
- `resolution`
- `userid`
- `reason`
- `suggestionBannerShown`
- `suggestionDetailViewAppear`
- `suggestionDetailViewDisappear`
- `terminationReason`
- `suggestionLearnMoreLinkTapped`

## Pre-survey file
`pre_survey_data_set_5.csv`

Observed columns include:
- `uuid`
- `cond`
- `age`
- `digital_wellbeing`
- `time`
- `prob_peers`
- `time_peers`
- `prob_self`
- `social_media_wellbeing`
- `prob`, `prob_other`
- `goal`, `goal_other`
- `social_media_updated`
- `belong_*`
- `ostracism_*`
- `fomo_*`

## Post-survey file
`post_survey_data_set_5.csv`

Observed columns include:
- `uuid`
- `digital_wellbeing`
- `time`
- `prob_peers`
- `time_peers`
- `prob_self`
- `social_media_wellbeing`
- `solve_prob`
- `address_goal`
- `social_media_updated`
- `belong_*`
- `ostracism_*`
- `fomo_*`

### DS5 construct map

| Construct | Directly observed? | Candidate variable(s) | Confidence | Notes |
|---|---|---:|---:|---|
| participant identifier | yes | `userid` / `uuid` | High | **confirmed**: strip `study-one-sec-next-gen-bzkj-2024-` from `userid` → canonical = `one-sec-next-gen-bzkj-2024-XXXX`; 572/573 behavioral matched to pre-survey; 284 in all three |
| experimental condition | yes | `cond` | High | extremely important |
| age | yes | `age` | High | adolescent sample |
| app event / target app | yes | `app` | High | core behavioral variable |
| event timing | yes | `timestamp`, `timezone` | High | time-zone aware |
| intervention duration | yes | `interventionDuration` | High | key intervention parameter |
| reintervention timing | yes | `timeIntervalUntilReIntervention` | High | highly relevant |
| event outcome | yes | `resolution` | High | core behavioral outcome |
| self-reported immediate reason | yes | `reason` | Medium-High | **confirmed**: 42.3% NaN; German free-text (not yet categorized); German categories include: "Sehen was los ist", "Entertainment", "Ablenkung", "Langeweile/Warten", etc. |
| suggestion exposure | yes | `suggestionBannerShown`, `suggestionDetailView*`, `suggestionLearnMoreLinkTapped` | Low | **confirmed**: 99%+ NaN — only populated for small suggestion sub-group; not usable for most participants |
| termination / stopping process | yes | `terminationReason` | Very Low | **confirmed**: only 12 non-null rows (all `terminatedByUser`); essentially unusable |
| digital well-being | yes | `digital_wellbeing` | High | pre and post |
| perceived time use / problems | yes | `time`, `prob_peers`, `time_peers`, `prob_self` | High | good moderator candidates |
| belonging / ostracism / FoMO | yes | `belong_*`, `ostracism_*`, `fomo_*` | High | rich psychosocial context |
| goal structure | yes | `goal`, `goal_other`, `address_goal`, `solve_prob` | High | strong fit for intervention success questions |
| friction sensitivity | partial | behavior change by `cond`, `interventionDuration`, `resolution` | High | one of the strongest datasets for this |
| override tendency | partial | repeated open/continue patterns despite intervention | Medium-High | likely derivable |
| adaptation over repeated exposure | partial | event outcomes across time and reintervention structure | High | very promising |
| substitution tendency | no direct variable | ordered app transitions after intervention events | Medium | more feasible than in DS1 because behavior file is richer |
| habit strength | no direct variable | repeated same-app/time patterns | Medium | derived |
| payoff sensitivity | no direct variable | behavior change under condition/intervention differences | Medium | strong quasi-operational proxy |
| context dependence | partial | `reason`, time features, condition | Medium | good but not full context logging |

---

# Dataset 6 — Danish adolescents

## Observed files and key columns

### `survey_data_clean.csv`
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

### `demographic_data.csv`
- `ID`
- `age`
- `gender`
- `region`

### `baseline_sessions_filt3.csv`
Contains very rich behavioral/session fields including:
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
- `participation_day`
- `period`
- `first_intervention_time`
- `app_next`, `app_next2`, `app_next3`
- `app_prev`, `app_prev2`
- multiple `resolution_next*`, `timestamp_next*`, `valid_open*`, `time_diff_*` fields

### `session_time_dataset_97_5_cutoff_data_forwarded.csv`
Also contains sequence/group/session structure, including:
- `group_id`
- `openedapp_open_time`
- `first_open_time`
- `first_in_group`
- `last_closedapp_time`
- `app_next`, `app_prev`
- multiple next/last/open/close timing variables
- context/condition/reintervention variables similar to baseline file

### Additional structures visible in the PDF (not confirmed in CSV files)
The project description PDF shows extra data structures that have **not been confirmed** as present in any of the five CSV files in `Data/behavioral data/`. These may originate from a separate preprocessing step or an earlier data version:
- streak-related variables
- `dismiss`, `open` flags
- lag/lead variables
- resist/open streak indicators
- a broad pre/post survey structure with `pre.*` and `post.*` prefixed variables

Do not treat these variables as available until inspected during the DS6 audit.

### DS6 construct map

| Construct | Directly observed? | Candidate variable(s) | Confidence | Notes |
|---|---|---:|---:|---|
| participant identifier | yes | `ID` (behavioral/demo) = `response_id` (survey) | High | **confirmed**: direct join, no transformation needed; 243 behavioral participants, 399 enrolled, 269 with survey data |
| experimental condition | yes | `condition` (text), `cond` (numeric 1-6), `cond_exp2` (binary) | High | **confirmed**: condition = control/default/intervention; cond=1-6 encodes cohort groups; `period` = baseline/intervention |
| survey wave | yes | `survey_nr`, `survey_nr_fact`, `period` | High | **confirmed**: survey_clean has 2 waves (269+209 rows); survey_full has 3 waves (440 participants) |
| app event / target app | yes | `app` | High | core behavior variable |
| event timing | yes | `timestamp`, `date`, `time`, `hour`, multiple event times | High | excellent |
| intervention type | yes | `interventionType` | High | strong |
| intervention duration | yes | `interventionDuration` | High | strong |
| reintervention | yes | `isReIntervention`, `timeIntervalUntilReIntervention` | High | very strong |
| event outcome | yes | `resolution` | Medium | **confirmed**: ALL rows = openedApp in both behavioral files; no dismiss or close events in resolution; session close must be inferred from group_id + close_ts |
| sequence structure | yes | `app_next*`, `app_prev*`, `resolution_next*` | High | **confirmed**: pre-engineered in both behavioral files; app_next/prev depth up to 3 |
| session/group structure | yes | `group_id`, `first_in_group`, `last_close_in_group` | High | **confirmed**: group_id groups open events into sessions; close timing via `time_diff_secs` |
| valid opening indicators | yes | `valid_open1`–`valid_open6`, `unmatched_open` | High | **confirmed**: present in both files; filter quality for session analysis |
| self-control | yes, at survey level | `self_control_index` | High | unusually strong |
| addiction / problematic use | yes | `addiction_index`, `kontrolover_so_me`, `taenkerpa_so_me` | High | strong psychosocial mapping |
| well-being / social connection | yes | `trivsel`, `socialconnection`, `socialtforbundet`, `tilfredsmed_so_me`, `fo_mo` | High | strong moderator layer |
| friction sensitivity | partial | behavior change across `cond`, `interventionDuration`, `resolution` | High | excellent candidate |
| override tendency | partial | repeated open outcomes, repeated intervention continuation | Medium | **confirmed**: isReIntervention = 2,120 events; streak/open/resist variables visible in PDF but NOT confirmed in any CSV file — do not treat as available |
| substitution tendency | partial | `app_next*` after target-app intervention events | High | one of the best datasets for this |
| habit strength | partial | repeated structured patterns by app/time/participation day | High | strong |
| context dependence | partial | day/week/hour/period + survey wave + condition | High | strong temporal/context approximation |
| adaptation over repeated exposure | partial | participation day, first intervention timing, reintervention variables, survey wave | High | excellent |
| feedback-loop dominance | no direct variable | repeated pattern structures over time + survey changes | Low-Medium | still model-derived |
| attractor strength / drift | no direct variable | stability/transition features over repeated days and sessions | Medium | more feasible here than in other datasets |

---

## Cross-dataset summary

### Closest to directly observable behavioral constructs
- DS1: app, timestamp, resolution, setup time
- DS4: app, resolution, intervention duration/type, study time
- DS5: app, resolution, condition, reintervention timing, suggestion interaction
- DS6: app, resolution, condition, reintervention, sequence variables, time/day/session structure

### Strongest survey-based moderator/psychological support
- DS1: problematic consumption, goals, happiness
- DS5: digital well-being, belonging, ostracism, FoMO, goals, problem domains
- DS6: self-control, addiction/problematic use, well-being, social connection, FoMO, repeated survey structure

### Most promising for sequence/network/substitution work
- DS6 strongest
- DS5 next
- DS4 possible
- DS1 possible but leaner
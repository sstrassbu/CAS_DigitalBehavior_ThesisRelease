# Dataset 5 Overview

**Audit status: COMPLETED — 2026-04-15**  
**Cleaned outputs:** `outputs/cleaned/ds5_behavioral_clean.csv`, `ds5_pre_survey_clean.csv`, `ds5_post_survey_clean.csv`, `ds5_participant_linkage.csv`  
**Audit report:** `outputs/reports/ds5_audit_report.md`

## Basic information

**Dataset name:** Dataset 5 — German adolescents  
**Raw folder:** `data_raw/5. data set, German adolescents/`  
**Project description:** Two interventions tested for German adolescents  
**Design summary:** Three-group experimental RCT: control, default friction intervention, reintervention group.

## Confirmed key facts

- **Delimiter:** semicolons for all three CSV files
- **Participants:** 573 behavioral, 792 pre-survey, 311 post-survey; 284 in all three
- **Behavioral rows:** 288,688
- **Resolution:** openedApp (61.6%), dismissed (21.5%), closed (15.6%), NaN (1.2%), dismissedByStructuredIntervention (0.04%)
- **Timestamp:** local ISO string → localize via `timezone` col → UTC
- **ID transform:** strip `study-one-sec-next-gen-bzkj-2024-` from `userid` → canonical = `one-sec-next-gen-bzkj-2024-XXXX`
- **cond:** NOT in behavioral — join from pre-survey (control=265, default=264, reintervention=263)
- **reason:** 42.3% NaN, German free text
- **suggestion columns:** 99%+ NaN — not usable for most participants
- **timeIntervalUntilReIntervention:** 77.9% NaN — reintervention group only, values in seconds
- **interventionDuration:** 0 for opened events, 6 for dismissed, NaN for 48,742 rows
- **Post-survey:** 3 duplicate UUIDs removed (first kept)

## Visible structure

### Behavior data set
- `behavior_data_set_5.csv`
- `behavior_data_set_5.xlsx`
- `codebook_behavior_data_set_5.pdf`

### Survey data sets
#### Post-survey
- `post_survey_data_set_5.csv`
- `codebook_post_survey_data_set_5.pdf`

#### Pre-survey
- `pre_survey_data_set_5.csv`
- `codebook_pre_survey_data_set_5.pdf`

### Additional documentation
- `Project description, Two interventions tested for German adolescents.docx`

## Behavioral dataset

**File:** `behavior_data_set_5.csv`  
**Rows:** 288,688  
**Observed columns shown in PDF:**
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

## Pre-survey dataset

**File:** `pre_survey_data_set_5.csv`  
**Rows:** 792  
**Observed columns shown in PDF:**
- `uuid`
- `cond`
- `age`
- `digital_wellbeing`
- `time`
- `prob_peers`
- `time_peers`
- `prob_self`
- `social_media_wellbeing`
- `prob`
- `prob_other`
- `goal`
- `goal_other`
- `social_media_updated`
- `belong_1` to `belong_8`
- `ostracism_1` to `ostracism_5`
- `fomo_1` to `fomo_10`

## Post-survey dataset

**File:** `post_survey_data_set_5.csv`  
**Rows:** 314  
**Observed columns shown in PDF:**
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
- `belong_1` to `belong_8`
- `ostracism_1` to `ostracism_5`
- `fomo_1` to `fomo_10`

## Preliminary interpretation

Dataset 5 appears to be one of the strongest datasets for intervention-oriented modeling because it combines:
- behavioral event data
- explicit experimental condition information
- adolescent sample
- pre/post survey structure
- psychosocial scales
- reason-level behavioral annotations
- reintervention timing and suggestion-related variables

This dataset looks especially strong for:
- moderator analysis
- behavioral heterogeneity
- intervention comparison
- phenotype profiling
- psychosocial predictors of intervention response

## Likely file roles

| File | Likely role | Confidence | Notes |
|---|---|---:|---|
| `behavior_data_set_5.csv` | main behavioral event dataset | High | likely primary behavior source |
| `behavior_data_set_5.xlsx` | duplicate/export | Medium | compare to csv |
| `pre_survey_data_set_5.csv` | pre-intervention survey | High | contains condition and background measures |
| `post_survey_data_set_5.csv` | post-intervention survey | High | contains outcome/perception measures |
| `codebook_behavior_data_set_5.pdf` | behavior codebook | High | read early |
| `codebook_pre_survey_data_set_5.pdf` | pre-survey codebook | High | read before recoding survey variables |
| `codebook_post_survey_data_set_5.pdf` | post-survey codebook | High | read before recoding survey variables |
| project description docx | study design and condition logic | High | essential |

## Likely unit of observation

### Behavioral file
Likely one app-opening / intervention-related behavioral event per row.

### Survey files
Likely one pre-survey or post-survey response per participant.

## Likely strengths

- explicit experimental condition:
  - `cond`
- direct intervention parameters:
  - `interventionDuration`
  - `timeIntervalUntilReIntervention`
- event outcome:
  - `resolution`
- reason-level behavioral annotation:
  - `reason`
- rich suggestion/intervention-interaction fields
- strong psychosocial moderator layer:
  - digital well-being
  - belonging
  - ostracism
  - FoMO
  - problem and goal variables
- very good fit for:
  - intervention-response prediction
  - subgroup differences
  - phenotype dimensions
  - moderator analysis

## Likely limitations

- behavior file uses `userid`, survey files use `uuid`
- ID reconciliation will need to be checked carefully
- some behavioral columns may be sparse
- some suggestion variables may only be relevant for specific intervention conditions
- not every participant may have both pre and post
- mixed types warning shown in the PDF suggests import care is needed

## Most promising immediate use cases

- condition-based event outcome summaries
- friction sensitivity by subgroup
- psychosocial moderator analysis
- pre/post comparison
- first phenotype profile construction
- condition-aware transition modeling
- intervention-response prediction prototypes

## Most promising later model families

- stochastic-process style event modeling
- network / transition analyses
- information-theoretic summaries
- agent-based user-type prototypes
- game-theory-inspired payoff/conflict framing
- limited dynamical-systems representations if variables are carefully proxied

## Immediate audit priorities

1. inspect whether `userid` and `uuid` can be joined directly or via transformation
2. inspect unique values of:
   - `resolution`
   - `reason`
   - `cond`
3. inspect missingness in suggestion-related fields
4. inspect whether intervention variables are present for all apps or only some
5. compare csv vs xlsx behavior files
6. determine how many participants are present in:
   - behavior
   - pre-survey
   - post-survey
7. inspect whether post-survey participants are a subset of pre-survey participants

## Recommendation

Dataset 5 should be one of your earliest major targets after DS1.
It is probably the strongest early candidate for:
- experimental modeling
- moderators
- behavioral phenotyping
- explaining why interventions work differently across users
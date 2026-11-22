# Variable Proxies

This document records proxy choices for constructs that are not directly measured in Datasets 1, 4, 5, and 6.

## Core rule

A proxy is not a direct measurement.
Every proxy should be documented with:
1. raw input variables
2. derivation logic
3. confidence level
4. main alternative interpretations

---

# 1. Friction sensitivity

## Concept
How strongly a user’s behavior changes when friction is present.

## Direct measure?
No single direct variable across all datasets.

## Candidate proxies

### DS1
- proportion of dismissed vs opened outcomes across time
- change in behavior over `secondsSinceOneSecSetup`

### DS4
- outcome patterns by `interventionDuration`
- change over `weeksSinceStudySetup`

### DS5
- outcome patterns by `cond`, `interventionDuration`, and `timeIntervalUntilReIntervention`

### DS6
- outcome patterns by `cond`, `interventionDuration`, `isReIntervention`, `participation_day`, and `period`

## Limitations
- dismissal may reflect genuine intention, not intervention efficacy
- users may differ in target-app mix
- friction sensitivity may vary across contexts and apps

---

# 2. Override tendency

## Concept
How often a user continues or opens despite friction.

## Direct measure?
Not fully direct, but behavior files come close.

## Candidate proxies

### DS1
- repeated `openedApp`-type outcomes after intervention-related events

### DS4
- repeated open outcomes despite `interventionType` / `interventionDuration`

### DS5
- repeated open outcomes plus intervention timing/reintervention structure

### DS6
- repeated open outcomes and `isReIntervention`
- streak/open/resist variables are visible in the project description PDF but have **not been confirmed** in any of the five actual CSV files; treat as unverified until DS6 audit

## Limitations
- some opens may be intentional and non-problematic
- “override” is partly interpretive unless explicitly logged
- DS6 streak variables may not be available in the loaded CSV files

---

# 3. Substitution tendency

## Concept
Whether friction on one app redirects behavior to another app rather than reducing overall use.

## Direct measure?
No direct single variable in DS1, DS4, DS5.  
Partially much closer in DS6 because next/prev app fields already exist.

## Candidate proxies

### DS1
- next app after target-app event inferred from timestamp ordering

### DS4
- app-transition inference from ordered event logs

### DS5
- app-transition inference after friction-related events

### DS6
- `app_next`, `app_next2`, `app_prev`, `app_prev2` and related sequence fields

## Limitations
- switching may reflect ordinary multitasking
- substitution window must be defined carefully
- not every next app is a substitution response

---

# 4. Habit strength

## Concept
How stable and repetitive a user’s app behavior is.

## Direct measure?
No direct variable.

## Candidate proxies

### All datasets
- repeated same-app use over time
- repeated same-app use at similar times of day
- stable outcome patterns across days/weeks

### Strongest datasets
- DS4 because of long study duration
- DS6 because of repeated day/period/session structure

## Limitations
- repeated behavior may reflect necessity or preference rather than habit
- app type matters

---

# 5. Context dependence

## Concept
How strongly behavior depends on time, context, or subjective reason.

## Direct measure?
Partially direct.

## Candidate proxies

### DS1
- `purpose` + time ordering

### DS4
- `purpose` + long-term temporal structure

### DS5
- `reason` + timestamp + condition

### DS6
- `purpose` + `week`, `day`, `week_day`, `hour`, `period`, survey wave

## Limitations
- contextual coverage is uneven across datasets
- purpose/reason fields may be missing or inconsistent

---

# 6. Adaptation over repeated exposure

## Concept
Whether user response changes across time and repeated intervention exposure.

## Direct measure?
No single direct variable, but several strong longitudinal proxies exist.

## Candidate proxies

### DS1
- behavioral change over `secondsSinceOneSecSetup`

### DS4
- behavioral change over `secondsSinceStudySetup` / `weeksSinceStudySetup`

### DS5
- behavioral change across timestamps and reintervention timing

### DS6
- change across `participation_day`, `period`, `survey_nr`, `survey_nr_fact`, reintervention variables

## Limitations
- adaptation may reflect attrition, changing app mix, or changing life context

---

# 7. Self-control

## Concept
Self-regulatory capacity relevant to intervention response.

## Direct measure?
Varies by dataset.

## Candidate status by dataset

### DS1
Proxy only:
- goals
- perceived problematic consumption
- happiness
- behavior under friction

### DS4
Very weak proxy:
- survey comments and reasons for use
- long-term usage patterns

### DS5
Moderate proxy:
- goal variables
- solve/address problem variables
- digital well-being and problem-related items

### DS6
Strongest support:
- `self_control_index`
- plus behavior under friction and repeated exposure

## Limitations
- even in DS6, self-control is survey-level rather than event-level
- event-level self-control still remains inferred

---

# 8. Problematic use / addiction-like tendency

## Concept
Broad problematic or dysregulated smartphone/social media use.

## Candidate support

### DS1
- `problematic_cons`
- `problematic_cons_general`
- `problematic_cons_compared`

### DS4
- qualitative `reason_use`, `benefits`, `negatives`

### DS5
- `digital_wellbeing`, `prob_*`, `social_media_wellbeing`

### DS6
- `addiction_index`
- `kontrolover_so_me`
- `taenkerpa_so_me`

## Limitations
- scales differ strongly across datasets
- cross-dataset harmonization should use cautious summary variables, not assume equivalence

---

# 9. Attractor strength / drift / feedback-loop dominance

## Concept
Model-derived dynamics from dynamical systems, stochastic processes, or system dynamics perspectives.

## Direct measure?
No.

## Candidate proxies

### Attractor strength
- repeated return to same app-use regime
- repeated stable app/time patterns

### Drift
- baseline tendency toward repeated opens or app checks over time

### Feedback-loop dominance
- repeated chains such as boredom/problematic-use proxy → checking → repeated opening over time
- stronger in datasets with repeated surveys plus event logs, especially DS6

## Best candidates
- DS4 for long-run drift/habit-like structure
- DS5 for condition-linked drift and adaptation
- DS6 for rich repeated structure and multilevel timing

## Limitations
- these are not direct measurements
- strong model assumptions are required
- use as exploratory constructs rather than hard facts

---

# 10. General recommendations

## Best direct-behavior proxy datasets
- DS5
- DS6

## Best long-term adaptation/habit datasets
- DS4
- DS6

## Best psychosocial moderator datasets
- DS5
- DS6

## Best lean starting dataset
- DS1

## Rule for analysis
When reporting any proxy-based result, explicitly state:
- whether the construct was directly observed or inferred
- which variables were used
- how strong the proxy mapping is
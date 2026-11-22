# Recommended First Modeling Pass — Stage 3

**Written:** 2026-04-16  
**Purpose:** Concrete, justified recommendation for which single dataset to use first for standalone multi-model implementation, which model families to try first, and which to save for later. This document is the primary decision output of Stage 3.

**Context:** The goal of the first modeling pass is NOT to produce final results. It is to:
1. Establish a working modeling pipeline on a single dataset
2. Try multiple model family implementations and compare their interpretive output
3. Identify which behavioral phenotype dimensions are empirically recoverable
4. Generate preliminary findings that can be refined later with other datasets

---

## Scoring summary: which dataset wins first?

Five criteria were evaluated for each dataset. Each is rated Strong / Moderate / Weak.

| Criterion | DS1 | DS4 | DS5 | DS6 |
|---|---|---|---|---|
| Friction outcome clarity | Strong (cleanest denominator) | Moderate (event-class filtering) | Strong (RCT context) | **Not applicable** |
| Model family breadth | Moderate | Moderate | **Strong** | Strong |
| Psychosocial moderator depth | Weak | None | **Strongest** | Strong |
| Experimental causal leverage | None | None | **Strong (RCT)** | Moderate |
| Implementation feasibility | **Strongest** | Moderate | **Strong** | Weak |
| **Total** | **Moderate** | **Moderate** | **Strong** | **Moderate** |

**Conclusion: DS5 is the recommended first standalone modeling dataset.**

---

## Primary recommendation: DS5

### Why DS5

**DS5 is the only dataset in the project that combines:**
- A clean, three-outcome friction response variable (opened/dismissed/closed)
- A randomized experimental condition (control / default / reintervention)
- Validated psychosocial moderator scales (belonging, ostracism, FoMO — all pre-survey, 99.8% coverage)
- Manageable size (573 participants, 288K events) — large enough for robust estimation, small enough for fast iteration
- Complete Stage 1 feature extraction already done (49 behavioral cols, 12 survey cols, 18 prepost cols)

This combination means that **even a simple first model produces an interpretable result**: comparing `rate_opened` across the three conditions is a direct, causally interpretable behavioral test. No other dataset in the project can make that claim.

### Why not the others

**DS1** is simpler and has the cleanest friction denominator, but it has no experimental condition and thin psychosocial coverage. Any model finding is descriptive and correlational only. It is a good lean fallback if implementation proves harder than expected — but the absence of conditions means you give up interpretive power from the first model.

**DS4** is the largest and has the best longitudinal depth, but has no conditions and no psychosocial data. It is excellent for habit/adaptation modeling but weak for the moderator analysis that makes the paper contribution distinctive. Starting with DS4 builds a pipeline that cannot answer the core research questions about why friction works differently for different people.

**DS6** is the richest dataset overall but also the most structurally complex. Two behavioral file families, quasi-experimental cohort design, single outcome type (all 'opened' — no override/compliance distinction at event level), and the smallest N (243). The project documentation itself (dataset_6_overview.md) explicitly recommends building the pipeline on a simpler dataset before attempting DS6. Starting there would create unnecessary overhead before any modeling insight is achieved.

---

## Implementation starting point for DS5

### What to load

```python
import pandas as pd
from pathlib import Path

# Behavioral + condition (already joined in Stage 1 features)
beh = pd.read_csv("outputs/features/ds5/ds5_behavior_features.csv")
# study_condition is already joined: 572/573 participants have condition

# Pre-survey psychosocial features
surv = pd.read_csv("outputs/features/ds5/ds5_survey_features.csv")
# 572 participants; belong_mean_pre, ostracism_mean_pre, fomo_mean_pre

# Pre-post change scores
prepost = pd.read_csv("outputs/features/ds5/ds5_prepost_features.csv")
# 284 participants with both pre and post

# Merge behavioral + survey
ds5 = beh.merge(surv, on="participant_id_canonical", how="left")
# Left join: 572/573 have survey; 1 gets NaN psychosocial variables
```

### Key design decisions before modeling

1. **Control group inclusion:** For friction-specific analysis, restrict to default and reintervention conditions (N ≈ 527). For intervention comparison analysis, include all three conditions.
2. **NaN handling:** `events_per_day` is 12.4% NaN (single-day window participants). Use `n_days_observed` as a complementary volume feature for these participants or drop them depending on the model's NaN sensitivity.
3. **Condition as fixed effect vs grouping variable:** In regression models, include `study_condition` as a categorical predictor. In sequence or phenotyping models, stratify by condition first to preserve condition purity.
4. **Pre-post analysis subset:** Only the 284 fully-linked participants have pre-post outcomes. For psychosocial change modeling, use this subset explicitly.

---

## Model families to try first on DS5

The following sequence moves from simplest to most complex, building up interpretive layers.

### Pass 1A: Descriptive behavioral profiling (no modeling required — paper-ready immediately)

**What:** Compute per-condition distributions of the key behavioral features.
- `rate_opened` by condition (control vs default vs reintervention)
- `rate_dismissed` by condition
- `app_entropy` by condition
- `open_rate_change_calendar` by condition (adaptation trajectory)

**Why first:** This is the direct RCT comparison. It requires no modeling infrastructure — just grouped descriptive statistics and distribution plots. It immediately answers whether the friction conditions produce different behavioral outcomes. Paper-ready within hours.

**Expected finding:** Default and reintervention conditions should show lower `rate_opened` than control. Reintervention may show more sustained reduction (lower `open_rate_change_calendar` → less habituation over time).

---

### Pass 1B: Logistic / linear regression with psychosocial moderators

**What:** Model `rate_opened` as a function of psychosocial predictors (`belong_mean_pre`, `ostracism_mean_pre`, `fomo_mean_pre`) within the default and reintervention conditions.

**Design:**
```
rate_opened ~ belong_mean_pre + ostracism_mean_pre + fomo_mean_pre + study_condition + (controls)
```

**Why:** This is the core paper contribution from DS5. Does pre-intervention FoMO predict higher friction override (higher `rate_opened`)? Does ostracism predict lower override? These moderator relationships are causally anchored by the RCT design — the psychosocial predictors were measured before the intervention.

**Interpretive framing:** Within the CAS/behavioral phenotyping frame, this tests whether social-motivation constructs (FoMO, ostracism) predict friction sensitivity — a dimension of behavioral heterogeneity with strong theoretical backing.

---

### Pass 1C: Information-theoretic behavioral profile

**What:** Compute per-participant continuous phenotype dimension scores from behavioral features:
- **Network centralization dimension:** `top_app_share`, `app_herfindahl`, `n_unique_apps`
- **Temporal diversity dimension:** `hour_entropy`, `weekend_event_share`, `morning_event_share`, `evening_event_share`
- **Override tendency dimension:** `rate_opened`, `max_consecutive_opens`, `p_open_after_dismiss`
- **Adaptation dimension:** `open_rate_change_calendar`

**Why:** This operationalizes the phenotype dimensions from `phenotype_dimensions.md` as continuous participant-level scores. Each score is directly interpretable from information theory (entropy → diversity) or behavioral regularity (streaks → habitual override). These scores can then be correlated with psychosocial variables.

**Model type:** Principal component analysis (PCA) or factor analysis across behavioral feature groups — or explicit score computation as weighted composites if you prefer theoretical grounding over data-driven loading.

---

### Pass 1D: Stochastic event-sequence analysis (Markov chain summaries)

**What:** Compute per-participant and per-condition transition probability matrices between behavioral outcomes. For each participant: what is the probability of outcome Y given the previous event's outcome X?

```
P(opened | prev=opened)     # habitual override — key metric
P(opened | prev=dismissed)  # recovery from compliance
P(dismissed | prev=opened)  # self-correction after override
```

**Why:** This tests whether friction response is path-dependent — whether users who just opened the app are more likely to open it again next time (habitual momentum). Condition-stratified matrices directly test whether the reintervention condition breaks habitual momentum patterns.

**Model type:** First-order Markov chain. Transition matrices per participant, then per condition. No pre-engineered sequence fields required — derive from sorted behavioral event file.

---

### Pass 1E: Mixed-effects regression for within-person adaptation

**What:** Model whether `rate_opened` changes over time (calendar days) within each condition.

```
rate_opened_at_time_t ~ calendar_day + study_condition + psychosocial_predictors + (1 | participant)
```

**Why:** Tests whether friction response habituates (increases `rate_opened` over time), especially in the default condition. The reintervention condition's delayed reintervention structure may slow habituation — testable via the interaction `calendar_day × study_condition`.

**Data preparation:** Requires time-binned behavioral data (e.g., weekly `rate_opened` per participant), not just the participant-level aggregate from Stage 1 features. This requires going back to the cleaned behavioral event file (`outputs/cleaned/ds5_behavioral_clean.csv`) and computing time-binned rates.

---

### Pass 1F: Exploratory cluster / phenotype identification

**What:** Cluster participants on behavioral phenotype dimension scores from Pass 1C. Identify 2–4 behavioral subtypes.

**Why:** This operationalizes the behavioral phenotyping goal. Cluster analysis on normalized behavioral scores (override tendency, adaptation, temporal diversity, network centralization) — unsupervised. Then: does cluster membership correlate with condition assignment? With psychosocial pre-scores? This is the bridge from descriptive behavioral profiles to phenotype-based intervention matching.

**Caution:** Clusters are exploratory here. Do not treat them as ground truth. Report as "behavioral subgroup hypotheses" with explicit uncertainty. The paper framing should be "phenotype profile proposal" rather than "validated subgroup discovery."

---

## Model families to save for later (not first)

| Model family | Why to wait | Better suited dataset |
|---|---|---|
| Dynamical systems / phase models | DS5 windows are shorter than DS4; need longer trajectories for phase detection | DS4 (long windows) or DS6 (explicit phase structure) |
| Network / transition models (full graph) | Requires sequence derivation engineering that isn't done yet; natural first target is DS6 with pre-built app_prev/app_next2 fields (app_next itself verified non-functional 2026-08-06 — see `data_docs/modeling_cautions.md` §6) | DS6 |
| Agent-based modeling | Requires well-characterized agent parameters from simpler models first | After Passes 1A–1E are done |
| System dynamics | Requires repeated survey waves — DS5 has only pre+post; DS6 has 3 waves | DS6 |
| Long-run habit/drift modeling | DS5 windows are moderate; DS4's 897-day windows are irreplaceable for this | DS4 |
| Full DS6 analysis | Start after DS5 pipeline is established | DS6 |
| DS4 substitution / transition analysis | Requires engineering 2.49M-event sequence derivation; high overhead | DS4, after DS5 |

---

## DS5 → DS4 → DS6 → DS1 implementation sequence

After the DS5 first pass, the recommended dataset sequence is:

1. **DS5 (first):** RCT + psychosocial moderators + clean friction outcomes → core paper contribution
2. **DS4 (second):** Long-run adaptation + habit modeling + large-N heterogeneity → longitudinal paper layer
3. **DS6 (third):** Substitution + session dynamics + repeated psychosocial + adolescent population → enrichment layer
4. **DS1 (fourth or parallel):** Lean baseline; cleanest friction denominator; useful for cross-dataset descriptive comparison of override rates

This sequence moves from the most interpretively powerful (DS5's RCT) to the structurally richest (DS6), while filling in the longitudinal gap (DS4) along the way. DS1 can be used in parallel as a reference dataset for any descriptive comparison that doesn't require experimental structure.

---

## Decision logic summary (paper-facing)

| Decision question | Answer | Reason |
|---|---|---|
| Which dataset for first standalone modeling? | **DS5** | Only RCT; validated psychosocial moderators; clean friction outcomes; manageable complexity |
| Which model families first? | Descriptive → logistic regression → information-theoretic phenotyping → Markov chains | Increasing complexity; each pass builds on the previous |
| Which model families to save? | Dynamical systems, network/transition, system dynamics, agent-based | Need longer trajectories, pre-built sequence fields, or repeated surveys not available in DS5 |
| Best dataset for long-term adaptation? | **DS4** | 897-day windows; no equivalent elsewhere |
| Best dataset for psychosocial moderators? | **DS5** then **DS6** | DS5: RCT + validated scales; DS6: 100% coverage + repeated waves + self-control |
| Best dataset for sequence / substitution? | **DS6** | Pre-engineered app_prev/app_next2 (app_next itself verified non-functional 2026-08-06); no real session grouping exists (group_id verified non-functional 2026-08-05) |
| Best dataset for experimental condition effects? | **DS5** (causal) then **DS6** (quasi) | DS5 is the only individual RCT |
| Best lean fallback if DS5 is too complex? | **DS1** | Simplest structure; complete features; no condition join needed |

---

## One-paragraph paper framing for this decision

*"Given the multi-model family approach of this study, the German adolescent RCT dataset (DS5) was selected as the primary first-pass modeling target. DS5 is the only randomized controlled trial in the dataset collection, enabling causally grounded comparison of behavioral friction response across three experimental conditions (control, default friction, and reintervention). Its validated pre-intervention psychosocial battery — measuring social belonging, ostracism, and Fear of Missing Out — provides the moderator layer necessary to test whether friction response heterogeneity is systematically predicted by pre-intervention psychological characteristics. With 99.8% pre-survey coverage and 573 behavioral participants, DS5 offers a combination of experimental rigor, psychosocial depth, and manageable implementation complexity that no other dataset in the collection matches. Subsequent modeling passes extend this foundation to DS4 (longitudinal habit and adaptation), DS6 (substitution dynamics and repeated psychosocial measurement), and DS1 (cross-dataset descriptive comparison)."*

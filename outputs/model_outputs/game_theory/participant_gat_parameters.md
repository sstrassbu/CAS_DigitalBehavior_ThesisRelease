# participant_gat_parameters.csv

**Produced by:** `notebooks/46_ds5_game_theory.ipynb`
**Date:** 2026-08-06
**Depends on:** `outputs/features/ds5/ds5_behavior_features.csv`,
`outputs/model_outputs/stochastic_processes/participant_parameters.csv`,
`outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv`

## What this file contains

Per-participant Game Theory (GaT) behavioral scores for DS5. One row per participant (N=573).
Unit of observation: one participant across their full observation window.

The commitment score is a behavioral proxy for strategy preference in a repeated open/dismiss
decision setting (paper §2.6). No formal payoff matrix or utility function is constructed —
FLAG G1: all quantities are behavioral ratios, not utility estimates.

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | RCT arm: control / default / reintervention |
| `commitment_score` | float | Proportion of ALL outcome-bearing app-opening events NOT resolved by opening (dismiss + close) = rate_not_opened. NOT restricted to friction-flagged events: in the control arm only 49 of ~102,000 events have is_intervention_event=1, so the between-arm contrast compares event populations with different friction exposure. |
| `strategy` | str | Classified strategy: commitment_oriented / reward_oriented / chronic_override / adaptive_switcher / mixed |
| `adaptation_direction` | str | Temporal shift in override rate: adapting_toward_dismissal / rebounding_toward_open / stable |
| `open_rate_change_calendar` | float | Change in open rate (late 1/3 − early 1/3 of calendar window) |
| `max_consecutive_opens` | float | Longest consecutive run of opening events (proxy for override streaks) |
| `mean_open_run_length` | float | Mean consecutive open run length |
| `p_open_after_dismiss` | float | P(open | previous event = dismiss) |
| `profile_p1` | str | DS5_01 phenotype label (Profile A / Profile B); NaN for 159 without Stage 4 features |

## Strategy classification thresholds

FLAG G2: Thresholds are descriptive/interpretive, not derived from equilibrium conditions.

| Strategy | Rule |
|---|---|
| `chronic_override` | commitment_score < 0.20 AND max_consecutive_opens ≥ 5 |
| `commitment_oriented` | commitment_score ≥ 0.60 |
| `reward_oriented` | commitment_score < 0.30 (after chronic_override check) |
| `adaptive_switcher` | \|open_rate_change_calendar\| ≥ 0.10 |
| `mixed` | none of the above |

## Key results

**Commitment score by condition:**

| Condition | N | Mean | Median |
|---|---|---|---|
| control | 184 | 0.236 | 0.152 |
| default | 197 | 0.471 | 0.396 |
| reintervention | 187 | 0.390 | 0.298 |

ANOVA: F=40.99, p<0.001 — friction conditions significantly increase commitment.

**Commitment score by phenotype:**

| Profile | N | Mean | Cohen d |
|---|---|---|---|
| Profile A | 125 | 0.353 | — |
| Profile B | 289 | 0.316 | 0.179 |

t=1.627, p=0.105 — no statistically significant difference. The point estimate is small (d=0.18,
95% CI approximately [−0.03, 0.40]), so a small phenotype effect cannot be ruled out at this N;
what the data support is that condition explains far more of the variance in commitment than
phenotype does, not that phenotype has no effect.

**Strategy distribution:**
- chronic_override: 144 (25.1%)
- reward_oriented: 141 (24.6%)
- adaptive_switcher: 108 (18.8%)
- commitment_oriented: 105 (18.3%)
- mixed: 75 (13.1%)

## Known limitations

1. FLAG G1: commitment_score is a behavioral ratio, not a formal utility estimate
2. FLAG G2: Strategy thresholds are interpretive and threshold-sensitive
3. FLAG G3: No payoff data directly observed; all strategy interpretation is theoretical
4. **Close-events sensitivity (FLAG G1 detail):** `commitment_score` counts `closedApp` events
   (user opened, then closed) in the same numerator as `dismissed`, per FLAG G1. `closedApp` is
   defined in `data_docs/harmonization_notes.md` as distinct from `dismissed` — the user did open
   the app — so it is not restraint at the opening decision. Per-condition close rates are 0.058
   (control), 0.072 (default), 0.080 (reintervention). Under the stricter alternative
   `dismissed / (dismissed + opened)`, 71 of 569 participants (12.5%) cross a strategy threshold
   (22 from ≥0.60 to <0.30, 18 from ≥0.60 to the middle band, 31 from the middle band to <0.30),
   and the condition ANOVA strengthens to F=49.25, p=1.9e-20 (control 0.187 < reintervention 0.333
   < default 0.423). The strategy thresholds (0.20/0.30/0.60) were calibrated against the
   `rate_not_opened` definition, not the stricter one.
5. 159 participants lack profile_p1 (outside DS5_01 N=414 phenotyped subset)
6. No sequential updating model; adaptation is a coarse calendar-period comparison

## How to load

```python
import pandas as pd
df = pd.read_csv('outputs/model_outputs/game_theory/participant_gat_parameters.csv')
```

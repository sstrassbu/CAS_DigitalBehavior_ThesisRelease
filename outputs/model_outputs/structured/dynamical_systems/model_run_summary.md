# Structured DyS -- Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/62_structured_dynamical_systems.ipynb
**Blueprint:** outputs/reports/structured/structured_dys_blueprint.md

## Eligibility
- DyS-eligible (>= 4 weeks with creation activity): 42/61 (68.9%) -- out of all 61 participants
  (of whom 4 have zero non-censored creation events and are therefore automatically ineligible)

## Trajectory metrics (eligible, N=42)
       state_space_volatility  volume_trend_slope  dropout_score
count                  42.000              42.000         42.000
mean                    1.259              -1.102         -0.243
std                     0.776               5.211          1.233
min                     0.100             -32.143         -3.968
25%                     0.578              -0.432         -0.660
50%                     1.142              -0.026         -0.016
75%                     1.844               0.210          0.324
max                     3.216               2.478          2.167

## Region label distribution
region_label
NaN                  19
dropout-prone        14
mixed                 9
oscillatory           8
inbox-heavy           6
sparse-consistent     3
high-structure        2

## Left-censoring caveat check
Correlation(state_space_volatility, pct_tasks_left_censored) = 0.254

## Subscription group comparison (observational only, no causal claim)
                       state_space_volatility              volume_trend_slope              dropout_score             
                                         mean median count               mean median count          mean median count
subscription_type_last                                                                                               
free                                    1.192  0.893    12             -0.920 -0.288    12        -0.480 -0.345    12
pro                                     1.286  1.480    30             -1.174  0.010    30        -0.149  0.000    30

## PCA of weekly state space
Variance explained by PC1+PC2: 62.9%

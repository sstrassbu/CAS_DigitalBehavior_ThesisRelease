# Structured StM -- Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/61_structured_statistical_mechanics.ipynb
**Blueprint:** outputs/reports/structured/structured_stm_blueprint.md

## Eligibility
- StM-eligible (n_tasks >= 10): 53/61 (86.9%)
- Persistence-eligible (>= 4 weeks): 42/61

## Macrostate (eligible, N=53)
       H_config  n_distinct_configs  top1_config_share
count    53.000              53.000             53.000
mean      2.068              10.962              0.506
std       0.822               6.557              0.207
min       0.285               3.000              0.154
25%       1.487               6.000              0.346
50%       2.128              10.000              0.482
75%       2.664              14.000              0.648
max       3.683              37.000              0.957

Macrostate label distribution:
macrostate_label
timed-basic       33
high-structure    19
NaN                8
inbox-heavy        1

## Joint-entropy sanity check
H_config >= H_type_last / H_completion / H_recurrence verified for all 53 eligible participants
(chain rule of entropy) -- 0 violations.

## Macrostate persistence (eligible, N=42)
count    42.000
mean      0.953
std       0.102
min       0.600
25%       1.000
50%       1.000
75%       1.000
max       1.000

## Susceptibility (N=53)
count    53.0000
mean      0.0146
std       0.0196
min       0.0000
25%       0.0017
50%       0.0097
75%       0.0208
max       0.0959

## Path dependence (pooled vs. within-participant)
                                                X                            Y  pearson_r_pooled  p_pooled  pearson_r_within  p_within     n
streak_length (consecutive prior non-completions) has_structure (current task)           -0.0223  0.022343           -0.0018  0.854205 10516

## Design note
No literal beta/T/Z/F thermodynamic apparatus was built, per the theory paper's own explicit caution
against treating energy/temperature/equilibrium as literal variables for Structured data (section 2.1).
This notebook does not consume StoP's output -- see blueprint Part 0 for the full justification.

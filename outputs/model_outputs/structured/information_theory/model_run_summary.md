# Structured InT — Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/65_structured_information_theory.ipynb
**Blueprint:** outputs/reports/structured/structured_int_blueprint.md

## Entropy eligibility
- All-task entropies (n_tasks>=10): 53/61 participants
- Creation-dependent entropies (n_noncensored>=5): 53/61 participants

## Entropy summary (mean, bits)
H_type_first         0.200
H_type_last          0.254
H_creation_source    0.653
H_hour_creation      2.887
H_recurrence         0.541
H_completion         0.960
H_reschedule         0.575

## NeT-InT bridge (eligible participants, N=45)
- H_state_marginal >= H_trans verified for all: True (chain rule sanity check)
- Mean I_consec_state = 0.362 bits

## Mutual information (pooled, whole sample)
                        X                                        Y  MI_bits  normalized_MI     n
           task_type_last                         lifecycle_status   0.0363         0.0317 26729
update_method_at_creation      entry_placement (inbox vs timeline)   0.0936         0.8873 10529
update_method_at_creation task_type_first (3-class, supplementary)   0.1386         0.3446 10529
        creation_hour_bin                          task_type_first   0.0113         0.0280 10555
        task_energy_level                    reschedule_occurrence      NaN            NaN     0

## Paper-named dimensions not implemented (confirmed absent from export)
alert use (task_alerts), task category, energy level (task_energy_level) -- see
structured_cas_modeling_plan.md §2 for the full codebook-vs-export gap analysis.

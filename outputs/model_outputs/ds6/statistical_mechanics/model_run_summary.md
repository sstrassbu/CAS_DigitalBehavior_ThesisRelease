# DS6 StM -- Model Run Summary

**Run at:** 2026-08-11 01:20:02
**Notebook:** notebooks/71_ds6_statistical_mechanics.ipynb
**Blueprint:** outputs/reports/stage4/step1_modeling/ds6_stm_blueprint.md

## Key results
- Mean H_joint (baseline / intervention): 2.8575 / 2.8313 bits
- Configuration persistence (dominant (app,hour) same both periods): 58.4% (139/238)
- Mean susceptibility (JS divergence): 0.0508 bits
- StM-InT sanity gate: PASSED (H_joint >= max(H_app, H_hour) for all valid participants, both periods)
- ANOVA susceptibility ~ condition: F=5.437, p=0.0049

## Proxy warning
No literal energy/temperature/equilibrium quantities are computed (FLAG StM-1) -- DS6's
unbounded StoP state variable makes DS5's beta=2/sigma^2 bridge inapplicable even as a loose
analogy. H_joint, persistence, and susceptibility are standard information-theoretic /
distributional-shift quantities, describing patterns in observed (app, time) configurations,
not directly observed psychological states (habit strength, friction sensitivity).

## Known limitations
- hour_bucket is a 4-category coarsening of hour_of_day (paper names 'time of day' as a
  configuration property, not a specific granularity) -- results are sensitive to bucket
  choice in principle, not tested here.
- Persistence is based on a single dominant configuration per period -- a participant whose
  distribution is genuinely diffuse (no strong mode) can show a persistence result driven by
  a small vote margin; `dominant_config_share` should be checked alongside `config_persistent`.
- Psychosocial correlations exploratory, uncorrected (6 tests).
- study_condition is quasi-experimental (cohort-level), not individually randomized.

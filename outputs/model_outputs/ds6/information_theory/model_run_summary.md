# DS6 InT -- Model Run Summary

**Run at:** 2026-08-11 01:18:58
**Notebook:** notebooks/75_ds6_information_theory.ipynb
**Blueprint:** outputs/reports/stage4/step1_modeling/ds6_int_blueprint.md

## Key results
- Mean H_app (baseline / intervention): 1.2668 / 1.2381 bits
- Mean H_hour (baseline / intervention): 3.9842 / 3.9890 bits
- Mean H_emp (baseline / intervention): 3.0403 / 3.0435 bits
- Mean H_SDE (baseline / intervention): 6.2266 / 5.4075 bits
- StoP-InT bridge r(H_SDE,H_emp): baseline r=0.5831 p=6.865e-23; intervention r=0.7194 p=6.69e-39
- NeT-InT bridge: I_consec >= 0 for ALL participants, both periods (PASSED, mandatory gate)
- Mean I_consec (baseline / intervention): 0.0690 / 0.0531 bits
- Pooled MI(study_period; app_name) = 0.0003 bits (normalized: 0.0002), H(app)=1.8837 bits

## Proxy warning
Entropy measures describe patterns in observed event distributions (which app, what hour,
how much daily volume), not directly observed psychological states. Low H_app means routine
in app CHOICE, not evidence of low urge or high self-control.

## Known limitations
- H_out excluded entirely -- DS6 has no dismiss/close outcome variance (see StoP blueprint Part 0).
- H_SDE bridge equation (Gaussian differential entropy) not yet formalized in the conceptual paper -- same gap DS5's InT notebook recorded.
- H_emp uses per-participant quantile bins (FLAG InT-1), not DS5's fixed [0,1] range -- H_emp values are not directly comparable in absolute terms to DS5's H_emp (different variable, different binning).
- Psychosocial correlations are exploratory, uncorrected for multiple comparisons (24 tests).

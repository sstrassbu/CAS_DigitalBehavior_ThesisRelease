# DS4 GaT -- Model Run Summary

**Notebook:** `56_ds4_game_theory.ipynb`  
**Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_gat_blueprint.md`  
**Run date:** 2026-08-07

Usable N=986

## Phenotype distribution

```
gat_phenotype
commitment_oriented    352
chronic_overrider      304
reward_oriented        190
adaptive_switcher      140
```

## Redundancy check

corr(p_open_after_dismiss, rate_opened)=0.9343 (dropped), corr(max_consecutive_opens, rate_opened)=0.6244 (kept), corr(substitution_after_dismissal_rate, rate_opened)=0.1092 (kept)

## Cross-checks

ANOVA chi_OU by gat_phenotype: F=12.088, p=0.0000
Chi-square gat_phenotype x Phase1 cluster: chi2=136.398, p=0.0000
ANOVA |open_rate_change_calendar| by gat_phenotype: F=35.565, p=0.0000

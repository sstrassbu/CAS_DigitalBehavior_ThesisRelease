# DS4 StM -- Model Run Summary

**Notebook:** `51_ds4_statistical_mechanics.ipynb`  
**Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stm_blueprint.md`  
**Run date:** 2026-08-11

## Summary

```
                                       0
n_total                      1039.000000
n_valid                       641.000000
median_beta_OU                 36.547362
median_T_OU                     0.027362
median_chi_OU                   6.848730
median_tau_hat                  0.630225
r_HStM_Hemp                     0.720580
r_activity_persistence_beta    -0.004993
```

## DS4 vs DS5 (descriptive only, not directly comparable)

```
                    dataset    n  median_beta  median_T
0         DS5 (approximate)  414    53.312665  0.018759
1  DS4 (exact, daily-scale)  641    36.547362  0.027362
```

## Timescale caveat (carried forward from StoP)

beta_OU/chi_OU/H_StM use daily-scale theta_hat_OU/sigma_hat_OU only. StoP's own weekly sensitivity check found a meaningfully different relaxation time at weekly resolution -- not a timescale-independent property.

# DS4 StoP -- Model Run Summary

**Notebook:** `53_ds4_stochastic_processes.ipynb`  
**Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`  
**Run date:** 2026-08-11

## Eligibility funnel

| Stage | N |
|---|---|
| Total participants | 1039 |
| >=1 intervention-outcome day | 1036 |
| >=MIN_DAYS(30) daily observations | 786 |
| ...and >=MIN_PAIRS(10) consecutive pairs | 785 |
| Valid mean-reverting fit (0<phi<1) | 641 (81.7% of attempted) |

## Parameter distribution (valid fits only, N=641)

```
        mu_hat_OU  theta_hat_OU  sigma_hat_OU     tau_hat
count  641.000000    641.000000    641.000000  641.000000
mean     0.689420      1.817126      0.327663    0.779348
std      0.147664      1.053800      0.164654    0.552908
min      0.104698      0.166430      0.066739    0.128677
10%      0.496277      0.696556      0.157841    0.313476
25%      0.616437      1.059833      0.208594    0.425815
50%      0.715090      1.586734      0.289986    0.630225
75%      0.792146      2.348439      0.406671    0.943545
90%      0.854123      3.190036      0.562141    1.435634
max      0.975514      7.771378      1.266392    6.008548
```

## Event-count floor sensitivity (theta_hat_OU)

```
                    n_valid  median_theta  median_tau
min_events_per_day                                   
1                     641.0      1.586734    0.630225
3                     654.0      1.463986    0.683068
5                     605.0      1.377502    0.725952
```

## Headline finding

Median relaxation time tau_hat = 0.63 days. See blueprint Section 4 for the two candidate readings (genuine fast habitual reversion vs. daily-ratio sampling noise) and the weekly-aggregation sensitivity check below for which reading the real output favors.

## Weekly-aggregation sensitivity (daily vs weekly theta)

See `participant_parameters_weekly_sensitivity.csv` and figure 4 below.

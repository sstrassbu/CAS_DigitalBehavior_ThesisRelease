# DS4 InT -- Model Run Summary

**Notebook:** `52_ds4_information_theory.ipynb`  
**Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_int_blueprint.md`  
**Run date:** 2026-08-11

## Entropy distribution summary

```
       H_out_intervention  H_out_all_classes        H_app       H_hour        H_emp       H_SDE
count         1036.000000        1039.000000  1039.000000  1000.000000  1036.000000  641.000000
mean             0.825815           1.194444     1.059857     4.077662     2.174003   -0.541085
std              0.195938           0.324426     0.755762     0.397639     0.697527    0.546554
min             -0.000000          -0.000000    -0.000000    -0.000000    -0.000000   -2.588900
10%              0.599401           0.807034    -0.000000     3.847630     1.344421   -1.214480
25%              0.760256           0.953979     0.366550     4.045575     1.941158   -0.919630
50%              0.884880           1.291978     1.062900     4.163400     2.327508   -0.548752
75%              0.965803           1.454318     1.571650     4.261150     2.626273   -0.156942
90%              0.994162           1.539971     2.053760     4.334000     2.848327    0.197742
max              1.000000           1.957048     3.129400     4.535100     3.141093    0.961345
```

## Bridge / redundancy checks

- r(H_emp, H_SDE) = 0.721 (n=641)
- r(H_out_intervention, mu_hat_OU) = -0.631

## MI(intervention_type; outcome)

MI = 0.0010 bits (n_events=909948)

```
event_outcome_simple         intervention_type  dismissed    opened  n_events
0                                  blackScreen   0.389169  0.610831     54105
1                            breathingExercise   0.328253  0.671747    552424
2                                 followTheDot   0.362171  0.637829    131438
3                     minimalBreathingExercise   0.328174  0.671826    135358
4                                       mirror   0.340098  0.659902     36613
5                                  rotatePhone   0.200000  0.800000        10
```

## Timescale caveat (carried forward from StoP)

H_SDE uses daily-scale sigma_hat_OU/theta_hat_OU only. StoP's own weekly sensitivity check found a meaningfully different timescale (median tau ~0.63 days daily vs ~0.91 weeks weekly). H_SDE here describes daily-timescale uncertainty specifically, not a timescale-independent property.

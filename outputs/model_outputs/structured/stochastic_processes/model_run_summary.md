# Structured StoP -- Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/63_structured_stochastic_processes.ipynb
**Blueprint:** outputs/reports/structured/structured_stop_blueprint.md

## Eligibility
- N_t^created (timed-task creations, local day): 43/61 (70.5%)
- N_t^completed (completion-marking events, local day): 38/61 (62.3%)

## N_t^created (eligible, N=43)
- mu_hat: mean=-0.048, median=0.000
- sig_hat: mean=3.734
- Fano_factor: mean=6.011, share>1 (bursty): 97.7%

## N_t^completed (eligible, N=38)
- mu_hat: mean=-0.003, median=0.000
- sig_hat: mean=5.041
- Fano_factor: mean=6.400, share>1 (bursty): 94.7%

## Descriptive phenotype labels (illustrative only, NOT a Step 2 clustering result)
created:
created_phenotype_label
noise-dominated    21
NaN                18
decay-drift         8
growth-drift        7
bursty              6
stable              1

completed:
completed_phenotype_label
NaN                23
noise-dominated    15
bursty              7
growth-drift        7
decay-drift         6
stable              3

## Subscription group comparison (observational only, no causal claim)
                       created_mu_hat              created_sig_hat              created_Fano_factor             
                                 mean median count            mean median count                mean median count
subscription_type_last                                                                                          
free                            0.008    0.0    13           5.726  3.318    13               8.068  4.976    13
pro                            -0.072    0.0    30           2.870  1.734    30               5.119  3.456    30

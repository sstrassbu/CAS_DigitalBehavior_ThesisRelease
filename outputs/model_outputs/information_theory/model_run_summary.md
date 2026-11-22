# DS5 InT -- Model Run Summary

**Run timestamp:** 2026-08-11 00:26:10
**Notebook:** notebooks/45_ds5_information_theory.ipynb
**Model:** Information Theory (Stage 4 Step 1)
**Dataset:** DS5 -- German Adolescents RCT (N=573 total)

---

## Pipeline parameters

| Parameter | Value |
|---|---|
| MIN_DAYS (for H_emp, H_SDE) | 7 |
| K_BINS (H_emp discretisation) | 10 |
| MIN_EVENTS_OUT (H_out threshold) | 10 |
| Valid outcomes | opened, dismissed |

## FLAG decisions in effect

| Flag | Decision |
|---|---|
| FLAG 1 | Discrete Shannon entropy (Eq. 25) -- no smoothing |
| FLAG 2 | Empirical PMF by frequency counts; K=10 bins for H_emp |
| FLAG 3 | H_SDE = half log2(2*pi*e*sigma^2) -- bridge from StoP (NOT in paper) |
| FLAG 4 | Mutual information, conditional entropy, KL divergence deferred |

## Measure availability

| Measure | N participants |
|---|---|
| H_out  | 478 / 572 |
| H_app  | 478 / 572 |
| H_hour | 478 / 572 |
| H_emp  | 414 / 572 |
| H_SDE  | 414 / 572 |

## Condition-level means

### H_out (outcome entropy, bits)
  control: 0.6116
  default: 0.8745
  reintervention: 0.777
Max theoretical: 1.0 bits (uniform over 2 outcomes)

### H_SDE (StoP bridge, bits)
  control: -0.6441
  default: 0.0058
  reintervention: -0.3436
Note: Ordering mirrors StoP sig_hat (monotone transform). Not independent evidence.

## StoP bridge validation

Pearson r(H_SDE, H_emp) = 0.6183 (n = 414)

## Psychosocial correlates (friction-exposed)

Nominally significant (p < 0.05):
  H_app ~ social_media_wellbeing_pre: r=0.1414, p=0.0111, n=322
  H_SDE ~ social_media_wellbeing_pre: r=0.1219, p=0.0426, n=277

## Output files

| File | Description |
|---|---|
| participant_entropy_metrics.csv | Per-participant entropy measures (5 dimensions + sig_hat) |
| condition_entropy_summary.csv | Condition-level entropy statistics |
| stop_int_comparison.csv | H_SDE vs H_emp bridge check per participant |
| psychosocial_entropy_correlations.csv | Pearson r of entropy vs psychosocial scales |
| figures/fig1_int_entropy_by_condition.png | Entropy by condition (violin plots) |
| figures/fig2_int_stop_bridge.png | H_SDE vs H_emp scatter (bridge validation) |
| figures/fig3_int_entropy_correlation_matrix.png | Correlation heatmap of 5 dimensions |
| figures/fig4_int_fomo_vs_entropy.png | FoMO vs H_SDE and H_out scatter |

## Proxy warning

All entropy measures describe observed behavioral distributions, not latent states.
H_SDE depends on StoP proxy: X_t = n_opened_day / n_events_day.
Bridge equation NOT yet in paper. Add before submission:
  H = half * log2(2*pi*e*sigma^2)  [Cover & Thomas 2006, Ch. 8]

## Known limitations

1. H_out is condition-confounded (different base outcome rates by condition)
2. H_SDE bridge equation not in paper -- required before submission
3. H_emp estimation noisy for participants with 7-14 day windows
4. H_app and H_hour describe decision events, not all phone use
5. No bias correction for empirical entropy estimation (FLAG 1 and 2)
6. Psychosocial analysis exploratory -- 25 tests, no multiple-comparison correction

## Forward connections

- InT -> Phenotyping (Step 2, notebook 100): entropy profile joins StoP parameters
- InT -> NeT (44): H_app entropy complements network centralization
- InT -> DyS (42): low H_emp participants are sigma->0 candidates
- Step 2: mutual information, KL divergence, conditional entropy
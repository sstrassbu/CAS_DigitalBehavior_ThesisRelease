# stop_int_comparison.csv

## Contents
Per-participant comparison between H_SDE (StoP bridge) and H_emp (empirical).
Limited to participants with MIN_DAYS >= 7 (same as StoP eligibility).

## Unit of observation
One row per StoP-eligible participant (N=414).

## Column reference
| Column | Type | Description |
|---|---|---|
| participant_id_canonical | str | Participant identifier |
| study_condition | str | RCT condition |
| sig_hat | float | StoP diffusion estimate |
| H_SDE | float | Gaussian differential entropy from sig_hat (bits) |
| H_emp | float | Empirical entropy of binned daily X_t (bits) |
| H_SDE_minus_H_emp | float | Agreement gap between bridge and empirical estimates |

## Notes
H_SDE and H_emp summarise different aspects of the same daily series.
Their Pearson correlation is descriptive and is not a Gaussianity test.

## Production
- Producing notebook: notebooks/45_ds5_information_theory.ipynb

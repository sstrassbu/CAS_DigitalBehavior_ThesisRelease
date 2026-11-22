# psychosocial_entropy_correlations.csv

## Contents
Pearson correlations between entropy measures and pre-intervention psychosocial scales.
Restricted to friction-exposed conditions (default + reintervention) for consistency with StoP.

## Unit of observation
One row per (entropy_var × psych_var) pair (up to 25 rows).

## Column reference
| Column | Type | Description |
|---|---|---|
| entropy_var | str | Entropy measure name |
| psych_var | str | Psychosocial variable name |
| n | int | Number of participants with both measures non-NaN |
| pearson_r | float | Pearson correlation coefficient |
| p_value | float | Two-tailed p-value |
| significant_p05 | bool | Whether p < 0.05 (exploratory flag only) |

## Notes
All correlations are exploratory. 25 tests performed — no multiple-comparison correction applied.
FoMO ~ H_SDE should match FoMO ~ sig_hat from StoP (monotone transform consistency check).

## Production
- Producing notebook: notebooks/45_ds5_information_theory.ipynb

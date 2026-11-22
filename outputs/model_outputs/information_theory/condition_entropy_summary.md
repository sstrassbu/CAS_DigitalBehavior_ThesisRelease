# condition_entropy_summary.csv

## Contents
Condition-level summary statistics for all five entropy measures.

## Unit of observation
One row per (entropy_measure × condition) combination (15 rows total).

## Column reference
| Column | Type | Description |
|---|---|---|
| measure | str | Entropy variable name (H_out / H_app / H_hour / H_emp / H_SDE) |
| condition | str | RCT condition: control / default / reintervention |
| n | int | Number of participants with non-NaN values |
| mean | float | Condition mean (bits) |
| median | float | Condition median (bits) |
| std | float | Condition standard deviation (bits) |
| q25 | float | 25th percentile (bits) |
| q75 | float | 75th percentile (bits) |

## Production
- Producing notebook: notebooks/45_ds5_information_theory.ipynb

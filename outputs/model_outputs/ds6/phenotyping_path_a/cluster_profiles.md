# cluster_profiles.csv

## Contents
Per-cluster descriptive statistics for the 4 Path A' features — the table underlying the
radar chart (`figures/fig4_phenotype_profiles_enhanced.png`). Same outlier caveat as
`cluster_assignments.md` applies.

## Unit of observation
One row per cluster (2 rows), MultiIndex columns (feature × statistic).

## Column reference

| Column | Type | Description |
|---|---|---|
| (index) | str | `cluster_label` (Profile A' / Profile B') |
| `(feature, 'mean'/'median'/'std')` | float | For each of h_period, hhi_change, H_emp_baseline, susceptibility |

## Production
- Source: `cluster_assignments.csv` (this folder), grouped
- Producing notebook: `notebooks/141_ds6_behavior_only_phenotype.ipynb`

## Cleaning / derivation steps applied
- `groupby("cluster_label")[feature_cols].agg(["mean", "median", "std"])` on raw values.

## Known limitations
- Profile A' (n=218): h_period=0.099, hhi_change=0.007, H_emp_baseline=3.063, susceptibility=0.032. Profile B' (n=9, outliers): h_period=-0.299, hhi_change=0.127, H_emp_baseline=3.149, susceptibility=0.388 — the susceptibility gap (12x) is what drives the split; read alongside `model_run_summary.md`'s outlier caveat, not as two balanced phenotypes.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping_path_a/cluster_profiles.csv'), header=[0,1], index_col=0)
```

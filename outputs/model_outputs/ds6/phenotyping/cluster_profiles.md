# cluster_profiles.csv

## Contents
Per-cluster descriptive statistics (mean/median/std) for all 5 phenotyping features — the
table underlying the radar chart (`figures/fig4_phenotype_profiles_enhanced.png`).

## Unit of observation
One row per cluster (2 rows: Profile A, Profile B), with a MultiIndex column structure
(feature × statistic).

## Column reference

| Column | Type | Description |
|---|---|---|
| (index) | str | `cluster_label` (Profile A / Profile B) |
| `(feature, 'mean')`, `(feature, 'median')`, `(feature, 'std')` | float | For each of the 5 features: h_period, hhi_change, H_emp_baseline, regime_changed, susceptibility |

## Production
- Source: `cluster_assignments.csv` (this folder), grouped
- Producing notebook: `notebooks/140_ds6_phenotype_exploration.ipynb`

## Cleaning / derivation steps applied
- `groupby("cluster_label")[feature_cols].agg(["mean", "median", "std"])` on raw (unstandardized) feature values.

## Known limitations
- Profile A: h_period=0.124, hhi_change=0.004, H_emp_baseline=3.055, regime_changed=0.0, susceptibility=0.030. Profile B: h_period=0.033, hhi_change=0.020, H_emp_baseline=3.080, regime_changed=1.0, susceptibility=0.066 — read alongside `model_run_summary.md`'s "Headline finding 1" note that `regime_changed` perfectly separates the two clusters by construction of the k=2 solution, not because it was given special weight in the algorithm.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping/cluster_profiles.csv'), header=[0,1], index_col=0)
```

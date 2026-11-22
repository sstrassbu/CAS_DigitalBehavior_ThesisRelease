# feature_redundancy_report.csv

## Contents
Pairwise Pearson correlation matrix among the 5 phenotyping features — the empirical check
of the redundancy risk flagged in the blueprint (Part 2) before running.

## Unit of observation
5×5 correlation matrix (one row/column per feature).

## Column reference

| Column | Type | Description |
|---|---|---|
| (index) | str | Feature name |
| `h_period`, `hhi_change`, `H_emp_baseline`, `regime_changed`, `susceptibility` | float | Pearson r with the row's feature |

## Production
- Source: `phenotype_feature_matrix.csv` (this folder)
- Producing notebook: `notebooks/140_ds6_phenotype_exploration.ipynb`

## Cleaning / derivation steps applied
- Standard `DataFrame.corr()` (Pearson) on the 227-row complete-case matrix.

## Known limitations
- **Result: no pair exceeds |r|>0.6** — the blueprint's pre-registered redundancy concern (3 features sharing a "how much did usage pattern change" theme) was checked and NOT confirmed; the largest correlation is `hhi_change`~`susceptibility` at r=0.339, meaningful but not redundant. Reported as a genuine check outcome, not assumed from the feature descriptions.
- `regime_changed` is binary; Pearson correlation with a binary variable is a point-biserial correlation, valid but interpret magnitude conservatively.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping/feature_redundancy_report.csv'), index_col=0)
```

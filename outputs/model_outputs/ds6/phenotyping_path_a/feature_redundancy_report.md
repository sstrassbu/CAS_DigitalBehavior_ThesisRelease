# feature_redundancy_report.csv

## Contents
Pairwise Pearson correlation matrix among the 4 Path A' features.

## Unit of observation
4×4 correlation matrix.

## Column reference

| Column | Type | Description |
|---|---|---|
| (index) | str | Feature name |
| `h_period`, `hhi_change`, `H_emp_baseline`, `susceptibility` | float | Pearson r with the row's feature |

## Production
- Source: `phenotype_feature_matrix.csv` (this folder)
- Producing notebook: `notebooks/141_ds6_behavior_only_phenotype.ipynb`

## Cleaning / derivation steps applied
- Standard `DataFrame.corr()` on the 227-row complete-case matrix (same values as the corresponding 4×4 submatrix of the main pass's 5×5 report — dropping a feature doesn't change the pairwise correlations among the remaining ones).

## Known limitations
- No pair exceeds |r|>0.6, consistent with the main pass's own redundancy check.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping_path_a/feature_redundancy_report.csv'), index_col=0)
```

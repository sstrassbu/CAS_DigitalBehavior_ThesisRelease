# ds4_feature_redundancy_report.csv

**Unit of observation:** 5×5 pairwise Pearson correlation matrix of the 5 curated
phenotype features (row/column labels = feature names).

---

## How this file was produced

- **Producing notebook:** `notebooks/59_ds4_phenotype_exploration.ipynb`, cell 13
- **Blueprint:** `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`

Reproduces, on the live complete-case N=641, the correlation check done before writing
the blueprint (which used the same real data).

## Actual run results (2026-08-06)

```
                       tau_hat  H_emp  fixed_point_deviation  chi_OU  rho_self
tau_hat                  1.000  0.196                  0.305   0.008    -0.010
H_emp                    0.196  1.000                  0.168  -0.483     0.227
fixed_point_deviation    0.305  0.168                  1.000  -0.242     0.160
chi_OU                   0.008 -0.483                 -0.242   1.000    -0.268
rho_self                -0.010  0.227                  0.160  -0.268     1.000
```

Max off-diagonal |r| = 0.483 (`H_emp`/`chi_OU`) — moderate, not severe. No feature was
dropped; all 5 contribute genuinely distinct information (confirmed by PCA needing 2
components to explain only 60.4% of variance — not 1-2 dominant axes).

## Known limitations

None beyond the general DS4 phenotyping caveats in `ds4_phenotype_feature_matrix.md`.

## How to load

```python
import pandas as pd

redundancy = pd.read_csv(
    "outputs/model_outputs/ds4_phenotyping/ds4_feature_redundancy_report.csv", index_col=0
)
```

# path_f_summary.csv

**Unit of observation:** one row — sample-level summary of Path F′.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n` | int | Joint population (641) |
| `chi2` | float | Chi-square statistic (31.444) |
| `dof` | int | Degrees of freedom (6) |
| `p_value` | float | p-value (<0.0001) |
| `min_observed_cell` | int | Smallest observed cell count (7) |
| `min_expected_cell` | float | Smallest expected cell count under independence (4.3) |

---

## How this file was produced

- **Producing notebook:** `notebooks/133_ds4_hierarchical_phenotype.ipynb`, cell 7
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## How to load

```python
import pandas as pd

summary = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_f_summary.csv")
```

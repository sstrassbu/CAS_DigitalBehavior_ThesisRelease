# path_a_summary.csv

**Unit of observation:** one row — sample-level summary of Path A′.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n` | int | Complete-case N (641) |
| `k_chosen` | int | 4 |
| `jaccard` | float | Bootstrap stability at chosen k (0.8714) |
| `silhouette` | float | Silhouette at chosen k (0.3477) |
| `ari_vs_phase1` | float | ARI against Phase 1's k=3 solution (0.664) |

---

## How this file was produced

- **Producing notebook:** `notebooks/131_ds4_behavior_only_phenotype.ipynb`, cell 9
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## How to load

```python
import pandas as pd

summary = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_a_summary.csv")
```

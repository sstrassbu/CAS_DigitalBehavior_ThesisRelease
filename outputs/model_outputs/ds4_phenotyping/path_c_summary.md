# path_c_summary.csv

**Unit of observation:** one row — sample-level summary of Path C′.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `n` | int | Complete-case N (641) |
| `k_chosen` | int | 3 |
| `jaccard` | float | Bootstrap stability at chosen k (0.9658 — strongest of the whole DS4 arc) |
| `silhouette` | float | Silhouette at chosen k (0.5147) |
| `ari_vs_phase1` | float | ARI against Phase 1's k=3 solution (0.047) |

---

## How this file was produced

- **Producing notebook:** `notebooks/132_ds4_network_focused_phenotype.ipynb`, cell 9
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## How to load

```python
import pandas as pd

summary = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_c_summary.csv")
```

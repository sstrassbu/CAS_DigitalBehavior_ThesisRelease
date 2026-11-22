# path_c_cluster_profiles.csv

**Unit of observation:** one row per Path C′ cluster (3 rows, k=3).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `path_c_cluster` | int | Cluster label |
| `rho_self`, `I_consec` | float | Cluster means |
| `n` | int | Cluster size |

---

## How this file was produced

- **Producing notebook:** `notebooks/132_ds4_network_focused_phenotype.ipynb`, cell 8
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## Actual run results (2026-08-06)

| Cluster | N | rho_self | I_consec |
|---|---|---|---|
| 0 | 197 | 0.922 | 0.047 |
| 1 | 341 (largest) | 0.532 | 0.094 |
| 2 | 103 | 0.744 | 0.424 |

Cluster 2 stands out with a much higher `I_consec` (0.42 vs ~0.05-0.09 elsewhere) —
participants whose consecutive-app choices carry substantially more mutual information,
i.e. their app-to-app transitions are more predictable/structured relative to their
overall app-usage entropy, independent of how self-repetitive (`rho_self`) they are.

## Known limitations

Same as `path_c_feature_matrix.md`.

## How to load

```python
import pandas as pd

profiles = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_c_cluster_profiles.csv")
```

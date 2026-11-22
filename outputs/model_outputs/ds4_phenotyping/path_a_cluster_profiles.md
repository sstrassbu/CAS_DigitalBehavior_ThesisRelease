# path_a_cluster_profiles.csv

**Unit of observation:** one row per Path A′ cluster (4 rows, k=4).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `path_a_cluster` | int | Cluster label |
| `tau_hat`, `H_emp`, `fixed_point_deviation`, `chi_OU` | float | Cluster means |
| `n` | int | Cluster size |

---

## How this file was produced

- **Producing notebook:** `notebooks/131_ds4_behavior_only_phenotype.ipynb`, cell 8
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## Actual run results (2026-08-06)

| Cluster | N | tau_hat | H_emp | fixed_point_deviation | chi_OU |
|---|---|---|---|---|---|
| 0 | 174 | 0.658 | 1.916 | 0.005 | 14.601 |
| 1 | 72 | 1.903 | 2.660 | 0.017 | 7.112 |
| 2 | 368 | 0.597 | 2.556 | 0.008 | 5.888 |
| 3 | 27 | 1.058 | 2.562 | 0.069 | 2.919 |

Cluster 0 (highest susceptibility, χ_OU=14.6) and cluster 2 (largest, n=368) together
correspond closely to Phase 1's clusters 0 and 1; cluster 1 (slow relaxation, τ̂=1.90)
and cluster 3 (largest all-days-vs-pair-days mean gap, fixed_point_deviation=0.069 — a
coverage diagnostic, not a model-fit measure) split out mostly from
Phase 1's cluster 2 — a finer partition of what Phase 1 saw as one group, consistent
with Path A′ having one more cluster than Phase 1 (k=4 vs k=3).

## Known limitations

Same as `path_a_feature_matrix.md`.

## How to load

```python
import pandas as pd

profiles = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_a_cluster_profiles.csv")
```

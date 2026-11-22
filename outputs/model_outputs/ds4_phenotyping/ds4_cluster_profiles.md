# ds4_cluster_profiles.csv

**Unit of observation:** one row per cluster (3 rows, k=3).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `cluster` | int | Cluster label |
| `tau_hat`, `H_emp`, `fixed_point_deviation`, `chi_OU`, `rho_self` | float | Cluster mean of each raw (unstandardized) feature |
| `n` | int | Cluster size |

---

## How this file was produced

- **Producing notebook:** `notebooks/59_ds4_phenotype_exploration.ipynb`, cell 12
- **Blueprint:** `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`

## Actual run results (2026-08-06)

| Cluster | N | tau_hat | H_emp | fixed_point_deviation | chi_OU | rho_self |
|---|---|---|---|---|---|---|
| 0 | 200 | 0.689 | 1.993 | 0.005 | 13.884 | 0.543 |
| 1 | 363 | 0.632 | 2.561 | 0.008 | 5.770 | 0.753 |
| 2 | 78 | 1.699 | 2.646 | 0.038 | 5.473 | 0.740 |

**Descriptive read (not a formal cluster-naming exercise):**
- **Cluster 0** (largest susceptibility): fast daily reversion, lowest entropy, best
  OU model fit, by far the **highest susceptibility** (χ_OU mean 13.88 vs ~5.5-5.8 for
  the other two) — participants closest to a behavioral "tipping point" in the StM sense.
- **Cluster 1** (largest, n=363): fast reversion, moderate-high entropy, highest
  self-transition rate.
- **Cluster 2** (smallest, n=78): by far the **slowest reversion** (τ̂ mean 1.70 days vs
  ~0.6-0.7 for the others) and the largest `fixed_point_deviation` (mean 0.038, ~5-7x the
  other two). Note this is **not** a model-fit statement: `fixed_point_deviation` carries no
  residual term and is largely an observation-coverage diagnostic — cluster 2 also has the
  sparsest records (mean 57.4 observed days and 0.966 pair-day coverage, vs 72.6/75.3 days
  and 0.991/0.998 for clusters 1/0).

## Known limitations

Same as `ds4_phenotype_feature_matrix.md`. This descriptive read is offered for
orientation only — no formal statistical test of between-cluster differences was run in
this Phase 1 pass.

## How to load

```python
import pandas as pd

profiles = pd.read_csv("outputs/model_outputs/ds4_phenotyping/ds4_cluster_profiles.csv")
```

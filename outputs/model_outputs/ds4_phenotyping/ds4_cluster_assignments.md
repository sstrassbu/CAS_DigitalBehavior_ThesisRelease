# ds4_cluster_assignments.csv

**Unit of observation:** one row per complete-case DS4 participant (641).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `cluster` | int | 0, 1, or 2 (k=3, stability-first selection — see `ds4_phenotype_feature_matrix.md`) |

---

## How this file was produced

- **Producing notebook:** `notebooks/59_ds4_phenotype_exploration.ipynb`, cell 12
- **Blueprint:** `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`

## Actual run results (2026-08-06)

Cluster sizes: 0=200, 1=363 (largest), 2=78 (smallest, min_cell well above typical
thresholds). Bootstrap Jaccard stability = 0.849 (STABLE, ≥0.75 threshold).

## Known limitations

Same as `ds4_phenotype_feature_matrix.md`.

## How to load

```python
import pandas as pd

assignments = pd.read_csv("outputs/model_outputs/ds4_phenotyping/ds4_cluster_assignments.csv")
```

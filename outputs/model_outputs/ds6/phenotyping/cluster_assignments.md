# cluster_assignments.csv

## Contents
Per-participant cluster (phenotype) assignment from the k=2 KMeans solution, plus the 5
raw feature values.

## Unit of observation
One row per complete-case participant (N=227).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `cluster_label` | str | "Profile A" or "Profile B" |
| `h_period`, `hhi_change`, `H_emp_baseline`, `regime_changed`, `susceptibility` | float | Raw (unstandardized) feature values — see `phenotype_feature_matrix.md` for definitions |

## Production
- Source: `phenotype_feature_matrix.csv` (this folder), clustered
- Producing notebook: `notebooks/140_ds6_phenotype_exploration.ipynb`

## Cleaning / derivation steps applied
- Features z-scored (mean 0, std 1) before clustering; `cluster_assignments.csv` reports the ORIGINAL raw values, not the standardized ones used internally by KMeans.
- k=2 selected via silhouette score subject to `min_cell >= 11` (5% of N=227, floored at 10 — see blueprint Part 3); k=3 and k=4 were mathematically available but rejected for producing cells below this minimum (9 participants).
- Cluster naming ("Profile A"/"Profile B") is arbitrary (alphabetical by KMeans label index), not ordered by any severity/direction.

## Known limitations
- Bootstrap Jaccard stability = 0.714 (MARGINAL, not STABLE — threshold 0.75). Cluster boundaries are directionally reproducible but noisier than DS5's Phase 1 (0.995) or Structured's (0.775).
- **The k=2 split is (almost) exactly DyS's `regime_changed` binary feature** — perfect separation confirmed (all Profile A = regime_changed=0, all Profile B = regime_changed=1). See `model_run_summary.md` "Headline finding 1" — this means the other 4 features' independent contribution to this particular split has not yet been demonstrated.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping/cluster_assignments.csv'))
```

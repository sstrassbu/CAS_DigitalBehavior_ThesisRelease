# cluster_assignments.csv

## Contents
Per-participant cluster assignment from Path A's k=2 KMeans fit — **read the caveat below
before using this file**: no k met the minimum-cell-size floor at this N, and the resulting
split is an outlier characterization, not a validated 2-phenotype structure.

## Unit of observation
One row per complete-case participant (N=227).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `cluster_label` | str | "Profile A'" (n=218) or "Profile B'" (n=9) |
| `h_period`, `hhi_change`, `H_emp_baseline`, `susceptibility` | float | Raw feature values |

## Production
- Source: `phenotype_feature_matrix.csv` (this folder), clustered
- Producing notebook: `notebooks/141_ds6_behavior_only_phenotype.ipynb`

## Cleaning / derivation steps applied
- k=2, k=3, k=4 all tested; **none met `min_cell >= 11`** (5% of N=227, same rule as the main pass) — every k isolates the same ~9-participant group regardless of k. k=2 used anyway, explicitly labeled provisional/outlier-driven throughout the notebook and this doc, not silently forced (the exact bug class Structured's own Path D notebook caught once — same discipline applied here).

## Known limitations
- **"Profile B'" (n=9) is a genuine multivariate-outlier group** (susceptibility 4–10× the population mean, 0.26–0.58 vs mean 0.046, combined with elevated hhi_change), not a real second phenotype. Do not present this as a validated 2-cluster solution.
- Bootstrap Jaccard = 0.910 (nominally STABLE) — but this just reflects that extreme outliers get consistently re-identified across resamples, which is expected and does NOT indicate genuine cluster structure.
- Coherence check: all 9 outliers are in friction conditions (7 default, 2 intervention, 0 control) — directionally matches StM's (71) significant condition effect on susceptibility, small N not independently testable.
- Cluster labels here are a SEPARATE fit from the main pass's `cluster_assignments.csv` (notebook 140) — do not assume "Profile A" (main) == "Profile A'" (this file); compare via `ari_comparison.csv`.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping_path_a/cluster_assignments.csv'))
```

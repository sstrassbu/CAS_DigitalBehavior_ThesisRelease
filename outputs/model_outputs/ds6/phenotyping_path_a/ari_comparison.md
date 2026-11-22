# ari_comparison.csv

## Contents
Adjusted Rand Index comparing Path A's (DyS-removed) cluster labels against the main Step 2
pass's (notebook 140) cluster labels — the primary readout this notebook was built to
produce (blueprint Part 2), read alongside the outlier caveat on the Path A' side.

## Unit of observation
Single comparison (1 row).

## Column reference

| Column | Type | Description |
|---|---|---|
| `n_overlap` | int | Participants present in both clusterings (227 — full overlap, both use the same complete-case set) |
| `k_main` | int | k used in the main pass (2) |
| `k_path_a` | int | k used in this pass (2, provisional — see `cluster_assignments.md`) |
| `ARI` | float | Adjusted Rand Index (0.0235) |
| `verdict` | str | Interpretive label |

## Production
- Source: `cluster_assignments.csv` (this folder) + `outputs/model_outputs/ds6/phenotyping/cluster_assignments.csv`
- Producing notebook: `notebooks/141_ds6_behavior_only_phenotype.ipynb`

## Cleaning / derivation steps applied
- `sklearn.metrics.adjusted_rand_score` on the inner-joined participant set (full 227 overlap).

## Known limitations
- **ARI=0.0235 is LOW/ORTHOGONAL** — but because Path A's own k=2 split is an outlier characterization (9 extreme participants vs. everyone else), not a real second phenotype, this ARI answers a narrower question than originally planned. The full 2×2 cross-tab (main pass label × Path A' label): main Profile A (regime stable, n=125) → 125/125 in Path A' Profile A' (0 outliers); main Profile B (regime changed, n=102) → 93 in Path A' Profile A', **9 in Path A' Profile B' (outliers)**. So all 9 susceptibility outliers are a subset of the main pass's "regime changed" group (9/102 of it) — a real but partial association, not the driver of the low ARI (the low ARI mainly reflects that 218/227 participants land in the same Path A' bucket regardless of their main-pass label, since Path A' isn't finding balanced 2-group structure at all). The cleaner "does balanced phenotype structure reproduce without DyS" question this ARI was meant to answer is not fully resolved by this pass — would need a genuinely-valid (min-cell-passing) DyS-free clustering to answer properly, which this data does not support at N=227.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping_path_a/ari_comparison.csv'))
```

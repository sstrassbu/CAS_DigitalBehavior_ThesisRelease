# psychosocial_overlays.csv

## Contents
Kruskal-Wallis test results comparing SyD's psychosocial change scores across Path A's 2
clusters (218 typical vs. 9 outliers).

## Unit of observation
One row per psychosocial scale (2 rows).

## Column reference

| Column | Type | Description |
|---|---|---|
| `scale` | str | addiction_index_change or self_control_index_change |
| `H_stat` | float | Kruskal-Wallis H statistic |
| `p_raw` | float | Uncorrected p-value |
| `p_bonferroni` | float | Bonferroni-corrected p-value (×2 tests) |

## Production
- Source: `cluster_assignments.csv` (this folder) + `outputs/model_outputs/ds6/system_dynamics/participant_stock_flow.csv`
- Producing notebook: `notebooks/141_ds6_behavior_only_phenotype.ipynb`

## Cleaning / derivation steps applied
- Same method as the main pass's overlay (Kruskal-Wallis, Bonferroni ×2). Overlay N=176 (same SyD prepost-eligible subset).

## Known limitations
- **Both non-significant** (addiction_index_change p=0.397, self_control_index_change p=0.841) — unlike the main pass, where `self_control_index_change` was significant (p_bonferroni=0.018). This is expected: the main pass's significant overlay was tied to the `regime_changed` split specifically (removed here), and the outlier group here (n=9, only a handful with SyD data) is too small and not the same grouping for that signal to reappear.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/phenotyping_path_a/psychosocial_overlays.csv'))
```
